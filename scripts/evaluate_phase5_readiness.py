from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.models import LocationContext, Product
from buyermoment.readiness import score_test_readiness
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import SpendSafetyPolicy, spend_safety


def rows_from(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def evaluate(rows: list[dict], policy: SpendSafetyPolicy) -> tuple[dict, list[dict]]:
    results = []
    for row in rows:
        product = Product.model_validate(row["product"])
        context = build_context(row["context_text"], source="phase5_control", context_id=row["record_id"])
        if product.service_regions and not context.location.country:
            context = context.model_copy(update={"location": LocationContext(country=product.service_regions[0])})
        contextfit = score(context, product)
        readiness = score_test_readiness(context, product, contextfit)
        decision = spend_safety(context, product, contextfit, policy)
        results.append({"record_id": row["record_id"], "label": row["label"], "split": row["split"], "context": row["context_text"], "contextfit": contextfit.model_dump(mode="json"), "test_readiness": readiness.model_dump(mode="json"), "spend_decision": decision.model_dump(mode="json")})
    total = len(results)
    predicted_test = [item for item in results if item["spend_decision"]["decision"] == "TEST"]
    predicted_watch = [item for item in results if item["spend_decision"]["decision"] == "WATCH"]
    gold_test = [item for item in results if item["label"] == "TEST"]
    gold_watch = [item for item in results if item["label"] == "WATCH"]
    non_test = [item for item in results if item["label"] != "TEST"]
    metrics = {
        "count": total,
        "test_precision": sum(item["label"] == "TEST" for item in predicted_test) / len(predicted_test) if predicted_test else None,
        "test_recall": sum(item["spend_decision"]["decision"] == "TEST" for item in gold_test) / len(gold_test) if gold_test else None,
        "test_coverage": len(predicted_test) / total if total else None,
        "watch_precision": sum(item["label"] == "WATCH" for item in predicted_watch) / len(predicted_watch) if predicted_watch else None,
        "watch_recall": sum(item["spend_decision"]["decision"] == "WATCH" for item in gold_watch) / len(gold_watch) if gold_watch else None,
        "waste_risk_rate": sum(item["spend_decision"]["decision"] == "TEST" for item in non_test) / len(non_test) if non_test else None,
        "false_abstention_rate": sum(item["spend_decision"]["decision"] in {"ABSTAIN", "BLOCK"} for item in gold_test) / len(gold_test) if gold_test else None,
        "decision_distribution": {decision: sum(item["spend_decision"]["decision"] == decision for item in results) for decision in ("TEST", "WATCH", "ABSTAIN", "BLOCK")},
        "mean_evidence_strength_test": sum(item["test_readiness"]["evidence_strength"] for item in gold_test) / len(gold_test) if gold_test else None,
        "mean_evidence_strength_watch": sum(item["test_readiness"]["evidence_strength"] for item in gold_watch) / len(gold_watch) if gold_watch else None,
        "mean_ambiguity_test": sum(item["test_readiness"]["ambiguity_score"] for item in gold_test) / len(gold_test) if gold_test else None,
        "mean_ambiguity_watch": sum(item["test_readiness"]["ambiguity_score"] for item in gold_watch) / len(gold_watch) if gold_watch else None,
    }
    return metrics, results


def choose_policy(validation_rows: list[dict]) -> tuple[SpendSafetyPolicy, list[dict]]:
    candidates = []
    for readiness in (0.55, 0.60, 0.65, 0.70, 0.75):
        for evidence in (0.55, 0.60, 0.65, 0.70):
            for ambiguity in (0.00, 0.05, 0.10, 0.15, 0.20, 0.30, 0.45):
                for actionability in (0.20, 0.30, 0.35, 0.40, 0.42):
                    # The relevance calibration analysis supports a conservative
                    # floor of 0.68. Lower candidates are still reported only as
                    # exploratory threshold rows, never selected for spend safety.
                    for confidence in (0.68,):
                        policy = SpendSafetyPolicy(min_test_readiness=readiness, min_test_evidence_strength=evidence, max_test_ambiguity=ambiguity, min_test_actionability=actionability, min_test_overall=0.70, min_test_confidence=confidence)
                        metrics, _ = evaluate(validation_rows, policy)
                        precision = metrics["test_precision"] or 0.0
                        coverage = metrics["test_coverage"] or 0.0
                        candidates.append((precision >= 0.90, precision, coverage, policy, metrics))
    acceptable = [item for item in candidates if item[0]]
    chosen = max(acceptable or candidates, key=lambda item: (item[1], item[2], -item[3].max_test_ambiguity, item[3].min_test_readiness, item[3].min_test_evidence_strength, -item[3].min_test_confidence, -item[3].min_test_actionability))
    return chosen[3], [{"policy": item[3].__dict__, "metrics": item[4]} for item in sorted(candidates, key=lambda item: (item[1], item[2]), reverse=True)[:20]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark Phase 5 TestReadiness and TEST-vs-WATCH policies.")
    parser.add_argument("--input", type=Path, default=Path("data/ccb1/phase5/test_vs_watch.jsonl"))
    args = parser.parse_args()
    rows = rows_from(args.input)
    validation = [row for row in rows if row["split"] == "validation"]
    hidden = [row for row in rows if row["split"] == "hidden_test"]
    chosen, top_candidates = choose_policy(validation)
    validation_metrics, validation_results = evaluate(validation, chosen)
    hidden_metrics, hidden_results = evaluate(hidden, chosen)
    artifact = {"benchmark": "Phase 5 TEST-vs-WATCH and TestReadiness", "policy": chosen.__dict__, "validation": validation_metrics, "hidden": hidden_metrics, "top_validation_candidates": top_candidates, "results": validation_results + hidden_results, "status": "manually authored readiness controls; no campaign outcome claim"}
    Path("artifacts/test_readiness_benchmark.json").write_text(json.dumps(artifact, indent=2) + "\n")
    Path("reports/test_readiness_benchmark.md").write_text("# TestReadiness benchmark\n\n" + json.dumps({key: value for key, value in artifact.items() if key != "results"}, indent=2) + "\n\nThreshold selection maximized validation TEST coverage among candidates with validation TEST precision at least 0.90 while retaining the empirically conservative confidence floor of 0.68. The hidden result is reported without retuning.\n")
    evidence_artifact = {"benchmark": "Phase 5 evidence-strength analysis", "validation": {"mean_test": validation_metrics["mean_evidence_strength_test"], "mean_watch": validation_metrics["mean_evidence_strength_watch"]}, "hidden": {"mean_test": hidden_metrics["mean_evidence_strength_test"], "mean_watch": hidden_metrics["mean_evidence_strength_watch"]}, "policy": chosen.__dict__}
    ambiguity_artifact = {"benchmark": "Phase 5 ambiguity analysis", "validation": {"mean_test": validation_metrics["mean_ambiguity_test"], "mean_watch": validation_metrics["mean_ambiguity_watch"]}, "hidden": {"mean_test": hidden_metrics["mean_ambiguity_test"], "mean_watch": hidden_metrics["mean_ambiguity_watch"]}, "policy": chosen.__dict__}
    Path("artifacts/evidence_strength_benchmark.json").write_text(json.dumps(evidence_artifact, indent=2) + "\n")
    Path("artifacts/ambiguity_benchmark.json").write_text(json.dumps(ambiguity_artifact, indent=2) + "\n")
    Path("reports/evidence_strength_benchmark.md").write_text("# Evidence-strength benchmark\n\n" + json.dumps(evidence_artifact, indent=2) + "\n")
    Path("reports/ambiguity_benchmark.md").write_text("# Ambiguity benchmark\n\n" + json.dumps(ambiguity_artifact, indent=2) + "\n")
    print(json.dumps({"policy": chosen.__dict__, "validation": validation_metrics, "hidden": hidden_metrics}, indent=2))


if __name__ == "__main__":
    main()
