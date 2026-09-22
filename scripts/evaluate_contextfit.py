from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from buyermoment.models import CommercialContextRecord, Product
from buyermoment.scoring import build_context, score


RELEVANCE_THRESHOLD = 0.40


def records_from(paths: Iterable[Path]) -> Iterable[CommercialContextRecord]:
    for path in paths:
        with path.open() as stream:
            for line in stream:
                if line.strip():
                    yield CommercialContextRecord.model_validate_json(line)


def product_for(record: CommercialContextRecord) -> Product:
    attributes = record.product_attributes
    raw_features = attributes.get("product_features") or attributes.get("features") or ""
    features = [item.strip() for item in str(raw_features).replace(",", "|").split("|") if item.strip()]
    name = record.product_title or record.product_id or "unknown product"
    evidence = [item for item in record.evidence if "product" in item.id]
    return Product(
        id=record.product_id or record.record_id,
        name=name,
        category=str(attributes.get("product_class") or attributes.get("query_class") or "unknown"),
        description=record.product_description or name,
        features=features,
        service_regions=list(attributes.get("service_regions") or []),
        evidence=evidence or record.evidence,
    )


def binary_metrics(pairs: list[tuple[bool, bool]]) -> dict[str, float | int | None]:
    tp = sum(actual and predicted for actual, predicted in pairs)
    fp = sum(not actual and predicted for actual, predicted in pairs)
    fn = sum(actual and not predicted for actual, predicted in pairs)
    tn = sum(not actual and not predicted for actual, predicted in pairs)
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = 2 * precision * recall / (precision + recall) if precision is not None and recall else None
    return {"count": len(pairs), "tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": precision, "recall": recall, "f1": f1}


def macro_f1(actual: list[str], predicted: list[str]) -> float | None:
    labels = sorted(set(actual) | set(predicted))
    values: list[float] = []
    for label in labels:
        metrics = binary_metrics([(a == label, p == label) for a, p in zip(actual, predicted, strict=True)])
        if metrics["f1"] is not None:
            values.append(float(metrics["f1"]))
    return sum(values) / len(values) if values else None


def ndcg(gains: list[float], k: int | None = None) -> float | None:
    if not gains or max(gains, default=0) <= 0:
        return None
    limit = min(len(gains), k) if k else len(gains)
    dcg = sum(gain / math.log2(index + 2) for index, gain in enumerate(gains[:limit]))
    ideal = sorted(gains, reverse=True)
    idcg = sum(gain / math.log2(index + 2) for index, gain in enumerate(ideal[:limit]))
    return dcg / idcg if idcg else None


def relevance_gain(record: CommercialContextRecord) -> float | None:
    label = record.metadata.get("original_label")
    if record.source_dataset == "amazon_esci":
        return {"E": 3.0, "S": 2.0, "C": 1.0, "I": 0.0}.get(record.metadata.get("original_esci_label"))
    if record.source_dataset == "wayfair_wands":
        return {"Exact": 2.0, "Partial": 1.0, "Irrelevant": 0.0}.get(label)
    return None


def query_group(record: CommercialContextRecord) -> str | None:
    if record.source_dataset in {"amazon_esci", "wayfair_wands"}:
        return f"{record.source_dataset}:{record.metadata.get('query_id', record.original_query)}"
    return None


def run(paths: list[Path]) -> dict[str, Any]:
    stage_pairs: list[tuple[str, str]] = []
    intent_pairs: list[tuple[bool, bool]] = []
    hard_negative_pairs: list[tuple[bool, bool]] = []
    relevance_pairs: list[tuple[bool, bool]] = []
    ranking: dict[str, list[tuple[float, float]]] = defaultdict(list)
    evidence_total = 0
    score_count = 0
    elapsed = 0.0
    source_counts: Counter[str] = Counter()
    subset_counts: Counter[str] = Counter()
    constraint_pairs: list[tuple[set[str], set[str]]] = []
    location_pairs: list[tuple[bool, bool]] = []

    for record in records_from(paths):
        source_counts[record.source_dataset] += 1
        subset = "real" if record.relevance is not None or record.source_dataset == "google_convapparel" else "controlled"
        if record.metadata.get("hard_negative_type"):
            subset = "hard_negative"
        elif record.metadata.get("augmentation_variant"):
            subset = "conversational_augmentation"
        subset_counts[subset] += 1
        started = time.perf_counter()
        context = build_context(record.context_text, source=record.source_dataset, context_id=record.record_id).model_copy(update={"location": record.location})
        result = score(context, product_for(record))
        elapsed += time.perf_counter() - started
        score_count += 1
        evidence_total += bool(result.evidence)

        if record.purchase_stage and record.metadata.get("label_origin") in {"controlled_variant_target", "controlled_hard_negative_target"}:
            stage_pairs.append((record.purchase_stage, result.purchase_stage))
        if "gold_commerciality_positive" in record.metadata:
            actual = bool(record.metadata["gold_commerciality_positive"])
            predicted = result.commerciality >= 0.5
            intent_pairs.append((actual, predicted))
            if record.metadata.get("hard_negative_type"):
                hard_negative_pairs.append((actual, predicted))
        if "location_fit_gold" in record.metadata:
            location_pairs.append((bool(record.metadata["location_fit_gold"]), result.location_fit >= 0.5))

        gain = relevance_gain(record)
        if gain is not None:
            predicted_relevant = result.product_fit >= RELEVANCE_THRESHOLD
            relevance_pairs.append((gain > 0, predicted_relevant))
            group = query_group(record)
            if group:
                ranking[group].append((result.product_fit, gain))

        expected = set(record.constraints.required_features)
        if expected:
            constraint_pairs.append((expected, set(result.extracted_constraints)))

    ranking_scores = []
    mrr_scores = []
    for candidates in ranking.values():
        ordered = sorted(candidates, key=lambda item: item[0], reverse=True)
        gains = [gain for _, gain in ordered]
        value = ndcg(gains)
        if value is not None:
            ranking_scores.append(value)
        first_relevant = next((index + 1 for index, gain in enumerate(gains) if gain > 0), None)
        if first_relevant:
            mrr_scores.append(1 / first_relevant)

    constraint_tp = constraint_fp = constraint_fn = 0
    for expected, predicted in constraint_pairs:
        constraint_tp += len(expected & predicted)
        constraint_fp += len(predicted - expected)
        constraint_fn += len(expected - predicted)
    constraint_precision = constraint_tp / (constraint_tp + constraint_fp) if constraint_tp + constraint_fp else None
    constraint_recall = constraint_tp / (constraint_tp + constraint_fn) if constraint_tp + constraint_fn else None
    constraint_f1 = 2 * constraint_precision * constraint_recall / (constraint_precision + constraint_recall) if constraint_precision is not None and constraint_recall else None

    return {
        "benchmark": "CCB-1 v0.1 ContextFit hidden evaluation",
        "inputs": [str(path) for path in paths],
        "source_counts": dict(source_counts),
        "subset_counts": dict(subset_counts),
        "model_configuration": {"scorer": "deterministic-contextfit-v0.1", "provider": "local", "azure_roles": {"bulk_generator": "buyermoment-bulk-generator (Stage A generated inputs)", "extractor": "buyermoment-extractor (comparison only; not used for score labels)", "judge": "not_deployed; original human labels take precedence"}},
        "metrics": {
            "commercial_intent": {**binary_metrics(intent_pairs), "scope": "controlled hard-negative targets only"},
            "purchase_stage": {"count": len(stage_pairs), "accuracy": sum(a == p for a, p in stage_pairs) / len(stage_pairs) if stage_pairs else None, "macro_f1": macro_f1([a for a, _ in stage_pairs], [p for _, p in stage_pairs]), "scope": "controlled augmentation/hard-negative targets only"},
            "constraint_extraction": {"count": len(constraint_pairs), "precision": constraint_precision, "recall": constraint_recall, "f1": constraint_f1, "scope": "records with explicit canonical required_features only"},
            "location_fit": {**binary_metrics(location_pairs), "scope": "controlled explicit city/serviceability targets only"},
            "product_relevance": {**binary_metrics(relevance_pairs), "ndcg": sum(ranking_scores) / len(ranking_scores) if ranking_scores else None, "mrr": sum(mrr_scores) / len(mrr_scores) if mrr_scores else None, "queries_with_labels": len(ranking), "scope": "original ESCI/WANDS labels; no LLM judge"},
            "hard_negative": {"false_positive_rate": (sum(predicted for actual, predicted in hard_negative_pairs if not actual) / sum(not actual for actual, _ in hard_negative_pairs)) if any(not actual for actual, _ in hard_negative_pairs) else None, "count": len(hard_negative_pairs)},
            "evidence_grounding": {"evidence_coverage": evidence_total / score_count if score_count else None, "unsupported_inference_rate": None, "unsupported_inference_status": "not_computed_without_human_annotations"},
            "structured_output": {"schema_validity": 1.0 if score_count else None, "valid_records": score_count},
            "economics": {"scored_records": score_count, "mean_latency_ms": (elapsed / score_count * 1000) if score_count else None, "tokens": 0, "estimated_cost_per_1000": 0.0, "cost_basis": "deterministic local scorer; Azure generation is tracked separately"},
        },
        "status": "measured_baseline; controlled labels are not human ground truth; Azure generation completed Stage A but is not used as a scorer label",
    }


def markdown(summary: dict[str, Any]) -> str:
    metrics = summary["metrics"]
    rows = [
        ("Commercial intent F1", metrics["commercial_intent"]["f1"]),
        ("Purchase-stage accuracy", metrics["purchase_stage"]["accuracy"]),
        ("Constraint F1", metrics["constraint_extraction"]["f1"]),
        ("Product relevance NDCG", metrics["product_relevance"]["ndcg"]),
        ("Product relevance MRR", metrics["product_relevance"]["mrr"]),
        ("Hard-negative FPR", metrics["hard_negative"]["false_positive_rate"]),
        ("Structured-output validity", metrics["structured_output"]["schema_validity"]),
        ("Mean latency (ms)", metrics["economics"]["mean_latency_ms"]),
        ("Estimated cost / 1,000", metrics["economics"]["estimated_cost_per_1000"]),
    ]
    lines = ["# ContextFit v0.1 benchmark", "", "This report contains measured baseline outputs only. Null means the current data does not support a defensible metric.", "", "| metric | value |", "|---|---:|"]
    lines.extend(f"| {name} | {value if value is not None else 'not computed'} |" for name, value in rows)
    lines.extend(["", "## Scope and limitations", "", f"- Inputs: {', '.join(summary['inputs'])}", "- ESCI/WANDS relevance metrics use original human labels; no LLM judge was used.", "- Controlled augmentation and hard-negative labels are targets for pipeline evaluation, not claims of human truth.", "- Unsupported-inference rate requires human evidence annotations and is intentionally not fabricated.", "- Azure-generated Stage A contexts are evaluated only as controlled transformations; the local deterministic scorer remains the measured scoring baseline.", "", "```json", json.dumps(summary, indent=2), "```", ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reproducible ContextFit benchmark.")
    parser.add_argument("--input", action="append", type=Path, default=None)
    parser.add_argument("--json-output", type=Path, default=Path("artifacts/contextfit_v0_1_benchmark.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/contextfit_v0_1_benchmark.md"))
    args = parser.parse_args()
    paths = args.input or [Path("data/ccb1/hidden_test/real.jsonl")]
    summary = run(paths)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(summary, indent=2) + "\n")
    args.report_output.write_text(markdown(summary))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
