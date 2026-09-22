from __future__ import annotations

import json
from pathlib import Path

from buyermoment.models import CommercialContextRecord
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import SpendSafetyPolicy, spend_safety
from evaluate_spend_safety import product_for


def evaluate(rows: list[CommercialContextRecord], threshold: float) -> dict:
    policy = SpendSafetyPolicy(min_test_confidence=threshold)
    predictions = []
    for row in rows:
        context = build_context(row.context_text, source=row.source_dataset, context_id=row.record_id).model_copy(update={"location": row.location})
        result = score(context, product_for(row))
        predictions.append((str(row.metadata["gold_spend_decision"]), spend_safety(context, product_for(row), result, policy).decision))
    test_preds = [pair for pair in predictions if pair[1] == "TEST"]
    non_test = sum(actual != "TEST" for actual, _ in predictions)
    return {
        "threshold": threshold,
        "test_precision": sum(actual == "TEST" for actual, _ in test_preds) / len(test_preds) if test_preds else None,
        "test_recall": sum(predicted == "TEST" for actual, predicted in predictions if actual == "TEST") / sum(actual == "TEST" for actual, _ in predictions),
        "waste_risk_rate": sum(predicted == "TEST" and actual != "TEST" for actual, predicted in predictions) / non_test if non_test else None,
        "abstain_rate": sum(predicted == "ABSTAIN" for _, predicted in predictions) / len(predictions),
        "coverage": sum(predicted in {"TEST", "WATCH"} for _, predicted in predictions) / len(predictions),
    }


def main() -> None:
    rows = [CommercialContextRecord.model_validate_json(line) for line in Path("data/ccb1/adversarial/adversarial_v2.jsonl").read_text().splitlines() if line.strip()]
    validation = [row for row in rows if row.split == "validation"]
    hidden = [row for row in rows if row.split == "hidden_test"]
    thresholds = [0.50, 0.60, 0.68, 0.75, 0.80, 0.90, 0.95]
    table = [{"threshold": threshold, "validation": evaluate(validation, threshold), "hidden": evaluate(hidden, threshold)} for threshold in thresholds]
    artifact = {
        "benchmark": "Phase 4 abstention threshold analysis",
        "table": table,
        "interpretation": "Thresholds are compared on the manually authored validation/hidden adversarial controls. ScoreResult confidence is a raw heuristic, not a calibrated purchase-stage probability; no customer-facing probability is exposed.",
    }
    Path("artifacts/abstention_thresholds.json").write_text(json.dumps(artifact, indent=2) + "\n")
    lines = ["# Abstention threshold analysis", "", "The policy uses validation-selected thresholds and keeps raw confidence separate from calibrated probability. The table below shows the safety/coverage tradeoff on controlled adversarial data.", "", "| Threshold | Validation TEST precision | Validation waste risk | Hidden TEST precision | Hidden waste risk | Hidden coverage |", "|---:|---:|---:|---:|---:|---:|"]
    lines.extend(f"| {row['threshold']:.2f} | {row['validation']['test_precision']!s} | {row['validation']['waste_risk_rate']!s} | {row['hidden']['test_precision']!s} | {row['hidden']['waste_risk_rate']!s} | {row['hidden']['coverage']!s} |" for row in table)
    lines.extend(["", "The selected policy keeps the existing `0.68` raw confidence threshold. This is a safety gate, not a calibrated probability; purchase-stage confidence remains analysis-only until a reliable reviewed calibration set exists."])
    Path("reports/abstention_thresholds.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(artifact, indent=2))


if __name__ == "__main__":
    main()
