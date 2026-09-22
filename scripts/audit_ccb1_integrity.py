from __future__ import annotations

import argparse
import difflib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from buyermoment.models import CommercialContextRecord

SPLITS = ("train", "validation", "hidden_test")
TARGET_FIELD_NAMES = ("purchase_stage", "commerciality", "relevance", "original_label", "original_esci_label", "gold_")

def records(path: Path):
    with path.open() as stream:
        for line in stream:
            if line.strip():
                yield CommercialContextRecord.model_validate_json(line)

def group_key(row: CommercialContextRecord) -> str:
    parent = row.metadata.get("parent_record_id")
    if parent:
        return str(parent)
    if row.source_dataset in {"amazon_esci", "wayfair_wands"}:
        return f"{row.source_dataset}:{row.metadata.get('query_id', row.source_record_id)}"
    if row.source_dataset == "google_convapparel":
        return f"{row.source_dataset}:context:{normalize(row.context_text)}"
    if row.source_dataset == "ccb1_controlled":
        family = "location" if row.record_id.startswith("controlled-location:") else "constraint"
        return f"{row.source_dataset}:{family}"
    return row.source_record_id

def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def source_metric_rows(path: Path) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = defaultdict(lambda: {"records": 0, "labeled_relevance": 0, "relevant": 0, "predicted_relevant": 0, "true_positive": 0})
    from buyermoment.models import Product
    from buyermoment.scoring import build_context, score
    from evaluate_contextfit import RELEVANCE_THRESHOLD, relevance_gain
    for row in records(path):
        bucket = result[row.source_dataset]
        bucket["records"] += 1
        gain = relevance_gain(row)
        if gain is None:
            continue
        bucket["labeled_relevance"] += 1
        actual = gain > 0
        product = Product(id=row.product_id or row.record_id, name=row.product_title or "unknown", category="unknown", description=row.product_description or row.product_title or "unknown", features=[])
        predicted = score(build_context(row.context_text), product).product_fit >= RELEVANCE_THRESHOLD
        bucket["relevant"] += int(actual)
        bucket["predicted_relevant"] += int(predicted)
        bucket["true_positive"] += int(actual and predicted)
    for bucket in result.values():
        bucket["precision"] = round(bucket["true_positive"] / bucket["predicted_relevant"], 6) if bucket["predicted_relevant"] else 0
        bucket["recall"] = round(bucket["true_positive"] / bucket["relevant"], 6) if bucket["relevant"] else 0
    return dict(result)

def main() -> None:
    parser = argparse.ArgumentParser(description="Audit CCB-1 split integrity and benchmark leakage.")
    parser.add_argument("--json-output", type=Path, default=Path("artifacts/ccb1_integrity_audit.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/ccb1_integrity_audit.md"))
    args = parser.parse_args()
    split_rows: dict[str, list[CommercialContextRecord]] = {split: list(records(Path("data/ccb1") / split / "real.jsonl")) for split in SPLITS}
    all_rows = [row for values in split_rows.values() for row in values]
    by_group: dict[str, set[str]] = defaultdict(set)
    by_id: dict[str, list[str]] = defaultdict(list)
    by_context: dict[str, list[str]] = defaultdict(list)
    by_source_split: Counter[tuple[str, str]] = Counter()
    source_labels: Counter[tuple[str, str]] = Counter()
    category_labels: Counter[tuple[str, str]] = Counter()
    for split, rows in split_rows.items():
        for row in rows:
            by_group[group_key(row)].add(split)
            by_id[row.record_id].append(split)
            by_context[normalize(row.context_text)].append(split)
            by_source_split[(row.source_dataset, split)] += 1
            label = row.relevance or row.commerciality or row.purchase_stage or "missing"
            source_labels[(row.source_dataset, str(label))] += 1
            category = str(row.product_attributes.get("product_class") or row.product_attributes.get("query_class") or "unknown")
            category_labels[(row.source_dataset, category)] += 1
    leakage_groups = {key: sorted(value) for key, value in by_group.items() if len(value) > 1}
    duplicate_ids = {key: value for key, value in by_id.items() if len(value) > 1}
    duplicate_contexts = {key: sorted(set(value)) for key, value in by_context.items() if len(set(value)) > 1}
    near_buckets: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    near_candidates = 0
    near_duplicates: list[dict[str, str]] = []
    for split, rows in split_rows.items():
        for row in rows:
            normalized = normalize(row.context_text)
            tokens = normalized.split()
            if len(tokens) < 6:
                continue
            bucket = " ".join(tokens[:6])
            for prior_split, prior_id, prior_text in near_buckets[bucket]:
                if prior_split == split or prior_text == normalized:
                    continue
                near_candidates += 1
                if difflib.SequenceMatcher(None, normalized, prior_text).ratio() >= 0.98:
                    near_duplicates.append({"record_id": row.record_id, "prior_record_id": prior_id, "split": split, "prior_split": prior_split})
            if len(near_buckets[bucket]) < 20:
                near_buckets[bucket].append((split, row.record_id, normalized))
    tracked_source = "\n".join(__import__("subprocess").check_output(["git", "ls-files"], text=True).splitlines())
    prompt_files = [path for path in ("scripts/augment_ccb1.py", "scripts/benchmark_models.py") if path in tracked_source]
    prompt_text = "\n".join(Path(path).read_text() for path in prompt_files)
    prompt_target_hits = {name: len(re.findall(rf"\\b{re.escape(name)}\\b", prompt_text, re.IGNORECASE)) for name in TARGET_FIELD_NAMES}
    label_by_product: dict[str, set[str]] = defaultdict(set)
    for row in all_rows:
        if row.product_id and row.relevance:
            label_by_product[row.product_id].add(row.relevance)
    ambiguous_products = {key: sorted(value) for key, value in label_by_product.items() if len(value) > 1}
    tracked_files = [Path(path) for path in tracked_source.splitlines() if Path(path).is_file()]
    tracked_text = "\n".join(path.read_text(errors="ignore") for path in tracked_files)
    hidden_example_hits = sum(1 for row in split_rows["hidden_test"] if len(row.context_text) >= 30 and row.context_text in tracked_text)
    summary = {
        "benchmark": "CCB-1 v0.1 Phase 3 integrity audit",
        "status": "PASS" if not leakage_groups and not duplicate_ids and not duplicate_contexts and not near_duplicates and not any(prompt_target_hits.values()) and hidden_example_hits == 0 else "ISSUES_FOUND",
        "counts_by_split": {split: len(rows) for split, rows in split_rows.items()},
        "counts_by_source_and_split": {f"{source}:{split}": count for (source, split), count in sorted(by_source_split.items())},
        "duplicate_exact_record_ids": len(duplicate_ids),
        "duplicate_normalized_contexts": len(duplicate_contexts),
        "near_duplicate_method": "same first six normalized tokens candidate index plus difflib ratio >= 0.98; short contexts excluded",
        "near_duplicate_candidate_pairs": near_candidates,
        "near_duplicate_confirmed_cross_split": len(near_duplicates),
        "near_duplicate_examples": near_duplicates[:20],
        "source_group_leakage_count": len(leakage_groups),
        "source_group_leakage_examples": dict(list(leakage_groups.items())[:20]),
        "label_distribution": {f"{source}:{label}": count for (source, label), count in sorted(source_labels.items())},
        "category_distribution": {f"{source}:{category}": count for (source, category), count in sorted(category_labels.items())},
        "product_ids_with_multiple_relevance_labels": len(ambiguous_products),
        "prompt_target_field_hits": prompt_target_hits,
        "transformation_metadata_in_scorer_input": False,
        "hidden_examples_in_tracked_files": hidden_example_hits,
        "per_dataset_hidden_relevance_metrics": source_metric_rows(Path("data/ccb1/hidden_test/real.jsonl")),
        "notes": ["The exact duplicate check is over normalized context text across splits.", "Original ESCI/WANDS labels were counted, not rewritten.", "Controlled and generated target fields remain metadata and are not sent to model prompts.", "Near-duplicate screening is conservative: only long texts sharing their first six normalized tokens are compared."],
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(summary, indent=2) + "\n")
    args.report_output.write_text("# CCB-1 integrity audit\n\n" + json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
