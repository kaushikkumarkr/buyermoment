from __future__ import annotations

import json
from pathlib import Path


JOURNEYS = [
    ("research_clarifies", [("Why do teams use CRM software?", "informational", "ABSTAIN"), ("What should a construction company look for?", "exploration", "ABSTAIN"), ("I need a CRM for our 20-person company this month.", "consideration", "WATCH"), ("Compare two plans.", "comparison", "WATCH"), ("Actually I am writing a market report, not buying.", "informational", "ABSTAIN"), ("Please do not recommend a vendor.", "informational", "ABSTAIN")]),
    ("third_party_research", [("I need shoes for my mother.", "exploration", "WATCH"), ("She needs slip resistance and size 9.", "consideration", "WATCH"), ("I am only researching for her, not purchasing yet.", "informational", "ABSTAIN"), ("She may decide next year.", "exploration", "ABSTAIN"), ("Compare materials for my report.", "comparison", "ABSTAIN"), ("We will not order today.", "exploration", "ABSTAIN")]),
    ("budget_reversal", [("I need analytics for my team this month.", "consideration", "WATCH"), ("We need SOC 2 and shared views.", "consideration", "WATCH"), ("The budget is $600 per month.", "consideration", "WATCH"), ("Actually the budget is $50 total.", "consideration", "BLOCK"), ("Do not recommend anything until finance approves.", "informational", "ABSTAIN"), ("We might revisit next quarter.", "exploration", "ABSTAIN")]),
    ("location_reversal", [("I need a plan for my US team this month.", "consideration", "WATCH"), ("Compare the team plans.", "comparison", "WATCH"), ("We are moving to Canada next month.", "exploration", "ABSTAIN"), ("The current offer is US-only.", "consideration", "BLOCK"), ("Find a Canadian alternative.", "exploration", "ABSTAIN"), ("Start the Canadian plan today.", "transactional", "WATCH")]),
    ("purchase_cancelled", [("I need waterproof hiking shoes under $150.", "consideration", "WATCH"), ("Compare two options.", "comparison", "WATCH"), ("Which arrives by Friday?", "transactional", "WATCH"), ("I cancelled the trip.", "informational", "ABSTAIN"), ("I will not buy shoes now.", "informational", "ABSTAIN"), ("How do I return the order?", "informational", "BLOCK")]),
    ("product_switch", [("I need a CRM for 20 users.", "consideration", "WATCH"), ("Compare the core plan.", "comparison", "WATCH"), ("Actually I need accounting software, not CRM.", "exploration", "ABSTAIN"), ("Do not carry over the CRM constraints.", "informational", "ABSTAIN"), ("I am only gathering options.", "exploration", "ABSTAIN"), ("Maybe we buy next year.", "exploration", "ABSTAIN")]),
]


def main() -> None:
    out = Path("data/ccb1/multiturn/phase5_stress.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for index in range(10):
        for name, turns in JOURNEYS:
            conversation_id = f"phase5:{name}:{index:02d}"
            previous: list[str] = []
            for turn_id, (text, stage, decision) in enumerate(turns, 1):
                lines.append(json.dumps({"record_id": f"{conversation_id}:{turn_id}", "conversation_id": conversation_id, "turn_id": turn_id, "journey_type": name, "context_text": text, "previous_context": previous[-3:], "purchase_stage": stage, "expected_decision": decision, "expected_transition_stage": stage, "expects_intent_reversal": name in {"research_clarifies", "purchase_cancelled", "product_switch"} and turn_id >= 5, "expects_downgrade": decision in {"ABSTAIN", "BLOCK"} and turn_id > 2, "country": "Canada" if name == "location_reversal" and turn_id >= 3 else "US", "provenance": ["Phase 5 manually authored multi-turn stress control", "gold follows docs/PURCHASE_STAGE_GUIDE.md"]}))
                previous.append(text)
    out.write_text("\n".join(lines) + "\n")
    print(json.dumps({"journeys": 60, "turns": len(lines), "path": str(out)}, indent=2))


if __name__ == "__main__":
    main()
