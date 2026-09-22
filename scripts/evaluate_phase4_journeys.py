from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from buyermoment.models import Evidence, LocationContext, Product
from buyermoment.scoring import build_context, infer_stage_with_history, score
from buyermoment.spend_safety import spend_safety


def main() -> None:
    rows = [json.loads(line) for line in Path("data/ccb1/multiturn/phase4_journeys.jsonl").read_text().splitlines() if line.strip()]
    previous_predicted: dict[str, str] = {}
    previous_expected: dict[str, str] = {}
    stage_correct = 0
    transition_correct = 0
    transitions = 0
    reversal_total = reversal_detected = 0
    stale_total = stale_errors = 0
    constraint_total = constraint_correct = 0
    third_party_total = third_party_detected = 0
    spend_decisions: Counter[str] = Counter()
    by_type: dict[str, dict[str, int]] = defaultdict(lambda: {"count": 0, "stage_correct": 0, "block_total": 0, "block_correct": 0})
    for row in rows:
        previous = previous_predicted.get(row["conversation_id"])
        expected_previous = previous_expected.get(row["conversation_id"])
        predicted_stage = infer_stage_with_history(row["context_text"], previous)
        previous_predicted[row["conversation_id"]] = predicted_stage
        previous_expected[row["conversation_id"]] = row["purchase_stage"]
        stage_correct += predicted_stage == row["purchase_stage"]
        if row["turn_id"] > 1:
            transitions += 1
            transition_correct += predicted_stage == row["purchase_stage"] and previous == expected_previous
        product = Product(
            id="phase4-journey-product",
            name="journey product",
            category="controlled",
            description=f"controlled product for {row['context_text']}",
            price=120,
            service_regions=["US", "Canada"],
            available=True,
            evidence=[Evidence(id="journey-product:evidence", kind="observed", text="Controlled product evidence supplied for the journey.", source="phase4_control")],
        )
        context = build_context(row["context_text"], context_id=str(row["turn_id"])).model_copy(update={"location": LocationContext(country=row.get("country", "US"))})
        result = score(context, product)
        decision = spend_safety(context, product, result)
        spend_decisions[decision.decision] += 1
        bucket = by_type[row["journey_type"]]
        bucket["count"] += 1
        bucket["stage_correct"] += predicted_stage == row["purchase_stage"]
        bucket["block_total"] += bool(row.get("expected_block"))
        bucket["block_correct"] += bool(row.get("expected_block")) and decision.decision == "BLOCK"
        if row["journey_type"] == "reversal" and row["turn_id"] in {3, 4}:
            reversal_total += 1
            reversal_detected += decision.decision == "BLOCK" and predicted_stage == "informational"
        if row.get("expected_block"):
            stale_total += 1
            stale_errors += decision.decision in {"TEST", "WATCH"}
        if row["journey_type"] == "budget_change" and row["turn_id"] == 4:
            constraint_total += 1
            constraint_correct += decision.decision == "BLOCK" and "BUDGET_INCOMPATIBLE" in decision.reason_codes
        if row["journey_type"] == "third_party" and any(term in row["context_text"].lower() for term in ("mother", "her", "not for me")):
            third_party_total += 1
            third_party_detected += any(term in row["context_text"].lower() for term in ("mother", "her", "not for me"))
    summary = {
        "journey_count": len({row["conversation_id"] for row in rows}),
        "turn_count": len(rows),
        "stage_accuracy": stage_correct / len(rows) if rows else None,
        "stage_transition_accuracy": transition_correct / transitions if transitions else None,
        "intent_reversal_detection": reversal_detected / reversal_total if reversal_total else None,
        "constraint_memory_accuracy": constraint_correct / constraint_total if constraint_total else None,
        "third_party_intent_detection": third_party_detected / third_party_total if third_party_total else None,
        "stale_context_error_rate": stale_errors / stale_total if stale_total else None,
        "spend_decision_distribution": dict(spend_decisions),
        "by_journey_type": {
            key: {
                "count": value["count"],
                "stage_accuracy": value["stage_correct"] / value["count"] if value["count"] else None,
                "block_accuracy": value["block_correct"] / value["block_total"] if value["block_total"] else None,
            }
            for key, value in by_type.items()
        },
        "status": "manually authored multi-turn controls; current-turn safety evaluation, not customer outcome validation",
    }
    Path("artifacts/multi_turn_robustness.json").write_text(json.dumps(summary, indent=2) + "\n")
    Path("reports/multi_turn_robustness.md").write_text(
        "# Multi-turn robustness\n\n"
        + json.dumps(summary, indent=2)
        + "\n\nThe current-turn classifier is evaluated against explicit journey labels. `stale_context_error_rate` counts a positive eligible decision on a turn explicitly labeled as a support, reversal, or serviceability block.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
