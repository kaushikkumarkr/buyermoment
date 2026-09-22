from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from buyermoment.models import Evidence, LocationContext, Product
from buyermoment.scoring import build_context, infer_stage_with_history, score
from buyermoment.spend_safety import load_policy, spend_safety


def product_for(text: str) -> Product:
    return Product(
        id="phase5-stress-product",
        name="phase5 product",
        category="software and footwear",
        description=f"Controlled product evidence for {text}",
        price=120,
        service_regions=["US", "Canada"],
        available=True,
        evidence=[Evidence(id="phase5:product", kind="observed", text="Controlled first-party product evidence.", source="phase5_control")],
    )


def main() -> None:
    path = Path("data/ccb1/multiturn/phase5_stress.jsonl")
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    policy = load_policy()
    stage_correct = transitions = reversal_detected = reversal_total = stale_errors = decision_correct = 0
    total = len(rows)
    records = []
    previous_by_conversation: dict[str, str | None] = {}
    decision_counts: Counter[str] = Counter()
    for row in rows:
        previous = previous_by_conversation.get(row["conversation_id"])
        stage = infer_stage_with_history(row["context_text"], previous)
        context = build_context(row["context_text"], source="phase5_multiturn", context_id=row["record_id"]).model_copy(update={"location": LocationContext(country=row.get("country", "US"))})
        product = product_for(row["context_text"])
        result = score(context, product)
        decision = spend_safety(context, product, result, policy)
        stage_ok = stage == row["purchase_stage"]
        decision_ok = decision.decision == row["expected_decision"]
        stage_correct += stage_ok
        decision_correct += decision_ok
        if row["turn_id"] > 1:
            transitions += int(stage == row.get("expected_transition_stage", row["purchase_stage"]))
        if row.get("expects_intent_reversal"):
            reversal_total += 1
            reversal_detected += int(decision.decision != "TEST")
        stale_errors += int(row.get("expects_downgrade") and decision.decision == "TEST")
        decision_counts[decision.decision] += 1
        previous_by_conversation[row["conversation_id"]] = stage
        records.append({"record_id": row["record_id"], "expected_stage": row["purchase_stage"], "predicted_stage": stage, "expected_decision": row["expected_decision"], "predicted_decision": decision.decision, "stage_correct": stage_ok, "decision_correct": decision_ok, "reason_codes": decision.reason_codes})
    summary = {
        "journey_count": len({row["conversation_id"] for row in rows}),
        "turn_count": total,
        "stage_accuracy": stage_correct / total if total else None,
        "stage_transition_accuracy": transitions / sum(row["turn_id"] > 1 for row in rows) if any(row["turn_id"] > 1 for row in rows) else None,
        "decision_accuracy": decision_correct / total if total else None,
        "intent_reversal_detection": reversal_detected / reversal_total if reversal_total else None,
        "stale_context_error_rate": stale_errors / sum(bool(row.get("expects_downgrade")) for row in rows) if any(row.get("expects_downgrade") for row in rows) else None,
        "decision_distribution": dict(decision_counts),
        "status": "manually authored Phase 5 stress controls; no campaign outcome claim",
    }
    artifact = {"summary": summary, "records": records}
    Path("artifacts/phase5_multiturn_stress.json").write_text(json.dumps(artifact, indent=2) + "\n")
    Path("reports/phase5_multiturn_stress.md").write_text("# Phase 5 multi-turn stress benchmark\n\n" + json.dumps(summary, indent=2) + "\n\nLater-turn contradictions and cancellations are treated as current-state evidence; prior buying intent is not allowed to force TEST.\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
