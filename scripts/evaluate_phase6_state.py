from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from buyermoment.conversation_state import score_with_state, update_conversation_state
from buyermoment.models import Evidence, Product
from buyermoment.scoring import infer_stage_with_history


def product() -> Product:
    return Product(id="phase6-state-product", name="controlled product", category="controlled", description="CRM, footwear, backpack, and software control product", price=120, service_regions=["United States", "Canada"], available=True, evidence=[Evidence(id="phase6:product", kind="observed", text="First-party controlled product evidence.", source="phase6_control")])


def matches(state, expected: dict) -> bool:
    for key, value in expected.items():
        if key == "budget" and state.active_constraints.get("budget") != value:
            return False
        if key == "location" and state.location.country != value:
            return False
        if key == "recipient" and state.recipient != value:
            return False
        if key == "product" and (not state.current_product_interest or state.current_product_interest[0] != value):
            return False
        if key == "research" and value and state.commerciality > 0.2:
            return False
        if key in {"owned", "cancelled", "future"} and value and state.commerciality > 0.2:
            return False
    return True


def main() -> None:
    rows = [json.loads(line) for line in Path("data/ccb1/multiturn/phase6_state_journeys.jsonl").read_text().splitlines() if line.strip()]
    by_conversation: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_conversation[row["conversation_id"]].append(row)
    records = []
    state_stage_correct = baseline_stage_correct = state_transition_correct = baseline_transition_correct = state_memory_correct = 0
    state_actionability_correct = 0
    state_revision_counts: Counter[str] = Counter()
    stale_by_type: Counter[str] = Counter()
    assertion_count = 0
    for conversation_id, turns in by_conversation.items():
        state = None
        previous_baseline = None
        for row in turns:
            baseline = infer_stage_with_history(row["context_text"], previous_baseline)
            state = update_conversation_state(state, row["context_text"], conversation_id=conversation_id, turn_id=row["turn_id"])
            _, _, decision = score_with_state(state, row["context_text"], product())
            stage_ok = state.current_purchase_stage == row["purchase_stage"]
            baseline_ok = baseline == row["purchase_stage"]
            state_stage_correct += stage_ok
            baseline_stage_correct += baseline_ok
            if row["turn_id"] > 1:
                state_transition_correct += int(stage_ok)
                baseline_transition_correct += int(baseline_ok)
            assertion_ok = matches(state, row["expected_state"])
            assertion_count += len(row["expected_state"])
            state_memory_correct += len(row["expected_state"]) if assertion_ok else 0
            if row["expected_state"].get("research") or row["expected_state"].get("owned") or row["expected_state"].get("cancelled") or row["expected_state"].get("future"):
                state_actionability_correct += int(decision.decision != "TEST")
            if not assertion_ok:
                for key in row["expected_state"]:
                    if key in {"budget", "location", "recipient", "product", "research", "owned", "cancelled", "future"}:
                        stale_by_type[key] += 1
            if state.state_revision_reason:
                state_revision_counts.update(state.state_revision_reason.split(";"))
            records.append({"record_id": row["record_id"], "journey_type": row["journey_type"], "expected_stage": row["purchase_stage"], "baseline_stage": baseline, "state_stage": state.current_purchase_stage, "stage_correct": stage_ok, "baseline_correct": baseline_ok, "expected_state": row["expected_state"], "state": state.model_dump(mode="json"), "spend_decision": decision.model_dump(mode="json")})
            previous_baseline = baseline
    total = len(rows)
    transition_total = sum(len(turns) - 1 for turns in by_conversation.values())
    actionability_total = sum(bool(row["expected_state"].get("research") or row["expected_state"].get("owned") or row["expected_state"].get("cancelled") or row["expected_state"].get("future")) for row in rows)
    summary = {"journey_count": len(by_conversation), "turn_count": total, "baseline_stage_accuracy": baseline_stage_correct / total, "stateful_stage_accuracy": state_stage_correct / total, "baseline_transition_accuracy": baseline_transition_correct / transition_total, "stateful_transition_accuracy": state_transition_correct / transition_total, "constraint_and_identity_memory_accuracy": state_memory_correct / assertion_count if assertion_count else None, "intent_reversal_actionability_accuracy": state_actionability_correct / actionability_total if actionability_total else None, "stale_context_error_rate": sum(stale_by_type.values()) / assertion_count if assertion_count else None, "stale_context_by_type": {key: value for key, value in stale_by_type.items()}, "state_revision_reasons": dict(state_revision_counts), "decision_distribution": dict(Counter(item["spend_decision"]["decision"] for item in records)), "status": "manually authored Phase 6 state-revision controls; no campaign outcome claim"}
    Path("artifacts/phase6_state_benchmark.json").write_text(json.dumps({"summary": summary, "records": records}, indent=2) + "\n")
    Path("reports/multi_turn_state_benchmark.md").write_text("# Multi-turn state benchmark\n\n" + json.dumps(summary, indent=2) + "\n\nThe stateful path stores current constraints, recipient, location, product interest, timing, commerciality, and revision reasons. Later explicit evidence is permitted to override earlier state.\n")
    Path("reports/stale_context_analysis.md").write_text("# Stale-context analysis\n\n" + json.dumps({"stale_context_error_rate": summary["stale_context_error_rate"], "by_type": summary["stale_context_by_type"], "revision_reasons": summary["state_revision_reasons"]}, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
