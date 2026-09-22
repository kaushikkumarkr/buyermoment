from __future__ import annotations

import argparse
import json
from pathlib import Path

JOURNEYS = (
    ("footwear", (("Why do my feet hurt after standing all day?", "informational"), ("Could my shoes be causing it?", "exploration"), ("What should nurses look for in work shoes?", "exploration"), ("I need something slip-resistant under $120.", "consideration"), ("Compare these two options.", "comparison"), ("Which one can arrive by Friday?", "transactional"))),
    ("skincare", (("Why does my skin react to fragrance?", "informational"), ("What kind of routine could help?", "exploration"), ("What should I look for in a fragrance-free moisturizer?", "exploration"), ("I need one for sensitive skin under $50.", "consideration"), ("Compare the cream and the set.", "comparison"), ("Where can I order the cream for delivery this week?", "transactional"))),
    ("saas", (("What does support analytics software do?", "informational"), ("Could it help a growing support team?", "exploration"), ("What should a team evaluate before choosing one?", "exploration"), ("I need SOC 2 support analytics for 20 users under $600 per month.", "consideration"), ("Compare the team and core plans.", "comparison"), ("Can I start the pilot this week?", "transactional"))),
)

def main() -> None:
    parser = argparse.ArgumentParser(description="Create manually authored multi-turn commercial journeys.")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--output", type=Path, default=Path("data/ccb1/multiturn/journeys_v0_1.jsonl"))
    args = parser.parse_args()
    rows = []
    for index in range(args.count):
        domain, turns = JOURNEYS[index % len(JOURNEYS)]
        conversation_id = f"journey:{domain}:{index:04d}"
        accumulated: list[str] = []
        for turn_id, (text, stage) in enumerate(turns, start=1):
            accumulated.append(text)
            rows.append({"conversation_id": conversation_id, "turn_id": turn_id, "domain": domain, "context_text": text, "previous_context": accumulated[:-1], "constraints_accumulated": [item for item in accumulated if "$" in item or "under" in item or "SOC 2" in item or "sensitive" in item or "slip-resistant" in item], "purchase_stage": stage, "commerciality": stage not in {"informational", "exploration"}, "provenance": ["phase3 manually authored journey template", "gold label follows docs/PURCHASE_STAGE_GUIDE.md"]})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
    print(json.dumps({"conversations": args.count, "turns": len(rows), "output": str(args.output)}, indent=2))

if __name__ == "__main__":
    main()
