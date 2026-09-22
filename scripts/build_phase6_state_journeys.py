from __future__ import annotations

import json
from pathlib import Path


JOURNEY_SPECS = [
    ("budget_override", [("I need a CRM for our 20-person company.", "consideration", {}), ("Under $500 per month.", "consideration", {"budget": 500}), ("Actually, the budget is $1000 per month.", "consideration", {"budget": 1000}), ("Compare the team plan.", "comparison", {"budget": 1000}), ("I need to choose the team plan this month.", "consideration", {"budget": 1000}), ("Actually I am researching for a client report, not buying.", "informational", {"budget": 1000, "research": True})]),
    ("location_override", [("I need a CRM for my US team.", "consideration", {"location": "United States"}), ("Compare the team plans.", "comparison", {"location": "United States"}), ("We are moving to Canada.", "exploration", {"location": "Canada"}), ("The current offer is US-only.", "consideration", {"location": "Canada"}), ("Find a Canadian alternative.", "exploration", {"location": "Canada"}), ("Can we start the Canadian plan today?", "transactional", {"location": "Canada"})]),
    ("recipient_override", [("I need running shoes for myself.", "consideration", {"recipient": "self"}), ("Under $150.", "consideration", {"recipient": "self", "budget": 150}), ("Actually they are for my mother.", "exploration", {"recipient": "mother", "budget": 150}), ("She already bought a pair.", "informational", {"recipient": "mother", "budget": 150, "owned": True}), ("I am only comparing whether she chose well.", "comparison", {"recipient": "mother", "budget": 150, "owned": True}), ("Do not recommend a new purchase.", "informational", {"recipient": "mother", "budget": 150, "owned": True})]),
    ("product_override", [("I need a CRM for 30 users.", "consideration", {"product": "crm"}), ("Compare CRM plans.", "comparison", {"product": "crm"}), ("Actually I need accounting software, not a CRM.", "exploration", {"product": "accounting software"}), ("The accounting system must work with Shopify.", "consideration", {"product": "accounting software"}), ("We are researching options for next year.", "exploration", {"product": "accounting software", "future": True}), ("No purchase is approved yet.", "informational", {"product": "accounting software", "future": True})]),
    ("cancellation", [("I need waterproof hiking shoes under $150.", "consideration", {"product": "hiking shoes", "budget": 150}), ("Compare two options.", "comparison", {"product": "hiking shoes", "budget": 150}), ("Which can arrive by Friday?", "transactional", {"product": "hiking shoes", "budget": 150}), ("I cancelled the trip.", "informational", {"product": "hiking shoes", "budget": 150, "cancelled": True}), ("I will not buy shoes now.", "informational", {"product": "hiking shoes", "budget": 150, "cancelled": True}), ("How do I return the order?", "informational", {"product": "hiking shoes", "budget": 150, "cancelled": True})]),
    ("conditional_buy", [("We need support analytics for our team.", "consideration", {"product": "analytics"}), ("We need shared views and SOC 2.", "consideration", {"product": "analytics"}), ("If finance approves, we might buy next quarter.", "exploration", {"product": "analytics", "future": True}), ("There is no purchase date.", "exploration", {"product": "analytics", "future": True}), ("I am gathering options for leadership.", "exploration", {"product": "analytics", "future": True}), ("Do not treat this as a current buying signal.", "informational", {"product": "analytics", "future": True})]),
    ("third_party_research", [("I am shopping for work shoes.", "exploration", {"product": "work shoes"}), ("They are for my employer.", "exploration", {"product": "work shoes", "recipient": "employer"}), ("Actually this is for a market report, not procurement.", "informational", {"product": "work shoes", "recipient": "client", "research": True}), ("The company is not buying this year.", "exploration", {"product": "work shoes", "recipient": "client", "research": True, "future": True}), ("Compare the brands for the report.", "comparison", {"product": "work shoes", "recipient": "client", "research": True, "future": True}), ("Please do not recommend a vendor.", "informational", {"product": "work shoes", "recipient": "client", "research": True, "future": True})]),
    ("support_clarification", [("I need a backpack for school.", "consideration", {"product": "backpack"}), ("Under $80 and in Canada.", "consideration", {"product": "backpack", "budget": 80, "location": "Canada"}), ("I already bought one yesterday.", "informational", {"product": "backpack", "budget": 80, "location": "Canada", "owned": True}), ("It arrived damaged.", "informational", {"product": "backpack", "budget": 80, "location": "Canada", "owned": True}), ("Can I exchange it?", "informational", {"product": "backpack", "budget": 80, "location": "Canada", "owned": True}), ("I am not shopping for another backpack.", "informational", {"product": "backpack", "budget": 80, "location": "Canada", "owned": True})]),
]


def main() -> None:
    out = Path("data/ccb1/multiturn/phase6_state_journeys.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for repeat in range(12):
        for name, turns in JOURNEY_SPECS:
            conversation_id = f"phase6:{name}:{repeat:02d}"
            previous: list[str] = []
            for turn_id, (text, stage, expected_state) in enumerate(turns, 1):
                lines.append(json.dumps({"record_id": f"{conversation_id}:{turn_id}", "conversation_id": conversation_id, "turn_id": turn_id, "journey_type": name, "context_text": text, "previous_context": previous[-3:], "purchase_stage": stage, "expected_state": expected_state, "provenance": ["Phase 6 manually authored state-revision control", "latest explicit turn supersedes earlier conflicting evidence"]}))
                previous.append(text)
    out.write_text("\n".join(lines) + "\n")
    print(json.dumps({"journeys": len(JOURNEY_SPECS) * 12, "turns": len(lines), "path": str(out)}, indent=2))


if __name__ == "__main__":
    main()
