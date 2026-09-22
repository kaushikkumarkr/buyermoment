from __future__ import annotations

import argparse
import json
from pathlib import Path

JOURNEYS = (
    ("reversal", (("I need waterproof hiking shoes under $150.", "consideration", False, "US"), ("Compare two options for me.", "comparison", False, "US"), ("I already bought the shoes. How do I clean them?", "informational", True, "US"), ("Should I return them?", "informational", True, "US"), ("I am researching alternatives for a paper.", "informational", False, "US"), ("Where can I buy a replacement today?", "transactional", False, "US"))),
    ("location_change", (("I need a CRM for my team under $600.", "consideration", False, "US"), ("Compare the team and core plans.", "comparison", False, "US"), ("We are moving the company to Canada.", "exploration", False, "Canada"), ("The offer is US-only; can we use it there?", "consideration", True, "Canada"), ("What alternatives serve Canada?", "exploration", False, "Canada"), ("Can I start the Canadian plan this week?", "transactional", False, "Canada"))),
    ("third_party", (("I am shopping for work shoes.", "exploration", False, "US"), ("They are for my mother, not for me.", "exploration", False, "US"), ("She lives in Nevada and needs size 9.", "consideration", False, "US"), ("Compare these two for her shift.", "comparison", False, "US"), ("She wants the one that arrives Friday.", "transactional", False, "US"), ("Please order it for her today.", "transactional", False, "US"))),
    ("budget_change", (("I need support analytics for my team.", "consideration", False, "US"), ("We need SOC 2 and shared views.", "consideration", False, "US"), ("The budget is $600 a month.", "consideration", False, "US"), ("Actually, the budget is $50 total.", "consideration", True, "US"), ("What lower-cost options exist?", "exploration", False, "US"), ("Do not recommend a plan until finance approves it.", "informational", False, "US"))),
    ("research_to_buy", (("Why do feet hurt after standing all day?", "informational", False, "US"), ("Could shoes be causing it?", "exploration", False, "US"), ("What should nurses look for?", "exploration", False, "US"), ("I need slip-resistant shoes under $130.", "consideration", False, "US"), ("Compare these options.", "comparison", False, "US"), ("Which arrives by Friday?", "transactional", False, "US"))),
)

def main() -> None:
    parser = argparse.ArgumentParser(description="Build Phase 4 difficult multi-turn journeys.")
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--output", type=Path, default=Path("data/ccb1/multiturn/phase4_journeys.jsonl"))
    args = parser.parse_args()
    rows = []
    for index in range(args.count):
        kind, turns = JOURNEYS[index % len(JOURNEYS)]
        conversation_id = f"phase4-journey:{kind}:{index:04d}"
        previous: list[str] = []
        for turn_id, (text, stage, expected_block, country) in enumerate(turns, start=1):
            rows.append({"conversation_id": conversation_id, "turn_id": turn_id, "journey_type": kind, "context_text": text, "previous_context": previous[-3:], "purchase_stage": stage, "expected_block": expected_block, "country": country, "provenance": ["phase4 manually authored reversal/location/budget/third-party journey", "gold label follows docs/PURCHASE_STAGE_GUIDE.md"]})
            previous.append(text)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
    print(json.dumps({"conversations": args.count, "turns": len(rows), "output": str(args.output)}, indent=2))

if __name__ == "__main__":
    main()
