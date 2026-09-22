from __future__ import annotations

import json
from pathlib import Path


TEST_VS_WATCH = [
    ("TEST", "accounting software for a 20-person construction company; we use QuickBooks and need to choose a replacement this month", "accounting software", ["QuickBooks integration", "job costing"], 299, ["US"]),
    ("TEST", "CRM for our 30-person sales team; we need to select a plan and start the pilot this quarter", "CRM software", ["shared pipeline", "team permissions"], 499, ["US"]),
    ("TEST", "waterproof hiking boots under $150 for Yellowstone; I want to order them today", "hiking boots", ["waterproof", "traction"], 129, ["US"]),
    ("TEST", "fragrance-free skincare for sensitive skin; I need the set delivered this week", "skincare set", ["fragrance-free", "sensitive skin"], 72, ["US", "Canada"]),
    ("TEST", "support analytics with SOC 2 and shared views for our team; finance approved a plan for this month", "support analytics", ["SOC 2", "shared views"], 299, ["US", "Canada"]),
    ("TEST", "I am ready to order a fragrance-free gift set for my mother today", "skincare set", ["fragrance-free", "gift"], 72, ["US"]),
    ("TEST", "compare the team and core plans; we will choose one for our support team this quarter", "support analytics", ["SOC 2", "shared views"], 299, ["US", "Canada"]),
    ("TEST", "I need slip-resistant work shoes under $130 and they must arrive by Friday", "work shoes", ["slip-resistant", "cushioning"], 119, ["US"]),
    ("TEST", "we are buying a CRM for our Canada office and need the contract signed this month", "CRM software", ["shared pipeline", "team permissions"], 499, ["Canada"]),
    ("TEST", "please order size 9 work shoes for my mother; she needs them for her shift next week", "work shoes", ["slip-resistant", "size 9"], 119, ["US"]),
    ("TEST", "our team has selected the plan and I need a checkout link for the $299 monthly option", "support analytics", ["SOC 2", "shared views"], 299, ["US"]),
    ("TEST", "I need a replacement moisturizer now because my current one is empty; fragrance-free is required", "moisturizer", ["fragrance-free", "sensitive skin"], 34, ["US"]),
    ("WATCH", "we may replace our accounting software next year; I am exploring what is available", "accounting software", ["job costing"], 299, ["US"]),
    ("WATCH", "I am researching CRM vendors for a market report and will not purchase this quarter", "CRM software", ["shared pipeline"], 499, ["US"]),
    ("WATCH", "what should a company look for when it evaluates support analytics?", "support analytics", ["SOC 2", "shared views"], 299, ["US"]),
    ("WATCH", "if finance approves the budget, we might buy a CRM next quarter", "CRM software", ["team permissions"], 499, ["US"]),
    ("WATCH", "I am comparing hiking boot categories for an article, not shopping for myself", "hiking boots", ["waterproof"], 129, ["US"]),
    ("WATCH", "would this skincare set work for me?", "skincare set", ["fragrance-free"], 72, ["US"]),
    ("WATCH", "my client asked me to gather accounting software options, but they may not buy anything", "accounting software", ["job costing"], 299, ["US"]),
    ("WATCH", "I am thinking about buying work shoes when I move to Boston next year", "work shoes", ["slip-resistant"], 119, ["US"]),
    ("WATCH", "compare these plans so I can understand the market; there is no current purchase", "support analytics", ["shared views"], 299, ["US"]),
    ("WATCH", "I already bought the moisturizer and want to know how to use it", "moisturizer", ["fragrance-free"], 34, ["US"]),
    ("WATCH", "our team is curious whether a CRM would help someday; no budget has been approved", "CRM software", ["team permissions"], 499, ["US"]),
    ("WATCH", "I am reading about waterproof boots because they are popular, not because I need to buy them", "hiking boots", ["waterproof"], 129, ["US"]),
]


THIRD_PARTY = [
    ("TEST", "I need to buy size 9 work shoes for my mother and can order them today.", "work shoes"),
    ("TEST", "Please order the fragrance-free gift set for my sister before Friday.", "skincare set"),
    ("TEST", "Our procurement team selected the CRM; I am buying it for my employer this month.", "CRM software"),
    ("TEST", "My child needs a replacement backpack for school and I am ready to buy it now.", "backpack"),
    ("WATCH", "I am researching shoe brands for my client's market report.", "work shoes"),
    ("WATCH", "My employer asked me to collect CRM options; there is no purchase date.", "CRM software"),
    ("WATCH", "I am comparing skincare gifts for someone else but I am only gathering ideas.", "skincare set"),
    ("WATCH", "I might buy a backpack for my child next year if the school changes.", "backpack"),
]


FUTURE_INTENT = [
    ("TEST", "I need this delivered tomorrow and will place the order today.", "work shoes"),
    ("TEST", "We are buying the CRM this Friday after the final approval.", "CRM software"),
    ("TEST", "I need the skincare set this week for a trip and am ready to purchase.", "skincare set"),
    ("WATCH", "I might buy this next year.", "work shoes"),
    ("WATCH", "I will need a CRM when we move next quarter, if the budget is approved.", "CRM software"),
    ("WATCH", "If I get promoted, I may buy the premium skincare set later.", "skincare set"),
    ("WATCH", "I am planning for a possible purchase someday and have no timing yet.", "work shoes"),
]


def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")


def labeled_rows(cases: list[tuple[str, str, str]], prefix: str, evidence_text: str) -> list[dict]:
    counts: dict[str, int] = {}
    per_label = {label: sum(item[0] == label for item in cases) // 2 for label in {item[0] for item in cases}}
    rows = []
    for index, (label, text, category) in enumerate(cases):
        split = "validation" if counts.get(label, 0) < per_label[label] else "hidden_test"
        counts[label] = counts.get(label, 0) + 1
        rows.append({"record_id": f"phase5-{prefix}:{index:03d}", "label": label, "context_text": text, "product": {"id": f"{prefix}-product:{index:03d}", "name": category, "category": category, "description": f"First-party {category} catalog entry.", "features": [], "price": 120, "service_regions": ["US", "Canada"], "available": True, "evidence": [{"id": f"{prefix}-evidence:{index:03d}", "kind": "observed", "text": evidence_text, "source": "first_party_catalog"}]}, "split": split, "provenance": [f"phase5 {prefix} control"]})
    return rows


def main() -> None:
    root = Path("data/ccb1/phase5")
    rows = []
    label_counts: dict[str, int] = {"TEST": 0, "WATCH": 0}
    for index, (label, text, category, features, price, regions) in enumerate(TEST_VS_WATCH):
        split = "validation" if label_counts[label] < sum(item[0] == label for item in TEST_VS_WATCH) // 2 else "hidden_test"
        label_counts[label] += 1
        rows.append({"record_id": f"phase5-test-watch:{index:03d}", "label": label, "context_text": text, "product": {"id": f"phase5-product:{index:03d}", "name": category, "category": category, "description": f"First-party {category} catalog entry with {', '.join(features)}.", "features": features, "price": price, "service_regions": regions, "available": True, "evidence": [{"id": f"phase5-product-evidence:{index:03d}", "kind": "observed", "text": f"First-party catalog lists {category}, {', '.join(features)}, and price ${price}.", "source": "first_party_catalog"}]}, "split": split, "provenance": ["phase5 manually authored TEST-vs-WATCH control", "label is readiness target, not a campaign outcome"]})
    write_rows(root / "test_vs_watch.jsonl", rows)
    write_rows(root / "third_party_intent.jsonl", labeled_rows(THIRD_PARTY, "third-party", "First-party catalog evidence."))
    write_rows(root / "future_intent.jsonl", labeled_rows(FUTURE_INTENT, "future", "First-party catalog evidence."))
    print(json.dumps({"test_vs_watch": len(rows), "third_party": len(THIRD_PARTY), "future_intent": len(FUTURE_INTENT)}, indent=2))


if __name__ == "__main__":
    main()
