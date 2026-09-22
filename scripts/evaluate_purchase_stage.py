from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from buyermoment.scoring import infer_stage, infer_stage_with_history

def f1_by_label(actual: list[str], predicted: list[str]) -> dict[str, dict[str, float | int]]:
    labels = sorted(set(actual) | set(predicted))
    result = {}
    for label in labels:
        tp = sum(a == label and p == label for a, p in zip(actual, predicted, strict=True))
        fp = sum(a != label and p == label for a, p in zip(actual, predicted, strict=True))
        fn = sum(a == label and p != label for a, p in zip(actual, predicted, strict=True))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        result[label] = {"count": sum(a == label for a in actual), "precision": precision, "recall": recall, "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0}
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate purchase-stage baselines and multi-turn state retention.")
    parser.add_argument("--input", type=Path, default=Path("data/ccb1/multiturn/journeys_v0_1.jsonl"))
    parser.add_argument("--json-output", type=Path, default=Path("artifacts/purchase_stage_benchmark.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/purchase_stage_benchmark.md"))
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    actual = [row["purchase_stage"] for row in rows]
    baseline = [infer_stage(row["context_text"]) for row in rows]
    stateful = []
    previous = None
    last_conversation = None
    for row in rows:
        if row["conversation_id"] != last_conversation:
            previous = None
            last_conversation = row["conversation_id"]
        prediction = infer_stage_with_history(row["context_text"], previous)
        stateful.append(prediction)
        previous = prediction
    confusion = Counter((a, p) for a, p in zip(actual, stateful, strict=True))
    transitions = [(a, p) for a, p in zip(actual, stateful, strict=True) if p != a]
    summary = {
        "benchmark": "Phase 3 purchase-stage and multi-turn benchmark",
        "turn_count": len(rows), "conversation_count": len({row["conversation_id"] for row in rows}),
        "baseline": {"accuracy": sum(a == p for a, p in zip(actual, baseline, strict=True)) / len(rows) if rows else None, "per_stage": f1_by_label(actual, baseline)},
        "stateful_rule_assisted": {"accuracy": sum(a == p for a, p in zip(actual, stateful, strict=True)) / len(rows) if rows else None, "per_stage": f1_by_label(actual, stateful)},
        "confusion_matrix": {f"{a}->{p}": count for (a, p), count in sorted(confusion.items())},
        "stage_transition_errors": len(transitions),
        "constraint_memory_accuracy": sum(("under" not in row["context_text"] or any("under" in item for item in row["constraints_accumulated"])) for row in rows) / len(rows) if rows else None,
        "status": "measured_on_manual_phase3_journey_templates; not human customer outcome data",
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(summary, indent=2) + "\n")
    args.report_output.write_text("# Purchase-stage benchmark\n\n" + json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
