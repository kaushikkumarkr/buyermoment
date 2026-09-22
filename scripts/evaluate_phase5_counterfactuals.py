from __future__ import annotations

import json
from pathlib import Path

from buyermoment.models import Evidence, LocationContext, Product
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import load_policy, spend_safety


GROUPS = [
    ("direct_buy", "I need waterproof hiking shoes under $150 and can order today.", "TEST", {}),
    ("future", "I might buy waterproof hiking shoes next year.", "ABSTAIN", {}),
    ("research", "I am researching waterproof hiking shoes for an article.", "ABSTAIN", {}),
    ("owner", "I already own waterproof hiking shoes. How do I clean them?", "BLOCK", {}),
    ("budget", "I need waterproof hiking shoes under $50 and can order today.", "BLOCK", {}),
    ("location", "I need waterproof hiking shoes in Canada and can order today.", "BLOCK", {"service_regions": ["US"]}),
    ("shipping", "I need waterproof hiking shoes tomorrow, but they cannot ship by then.", "BLOCK", {"shipping_deadline_met": False}),
    ("third_party_research", "I am researching waterproof hiking shoes for my client's report.", "ABSTAIN", {}),
    ("conditional", "If my company approves the budget, I may buy waterproof hiking shoes next quarter.", "ABSTAIN", {}),
    ("cancelled", "I was going to buy waterproof hiking shoes, but I cancelled the trip.", "ABSTAIN", {}),
]


def main() -> None:
    policy = load_policy()
    cases = []
    for name, text, expected, overrides in GROUPS:
        for index in range(6):
            product_values = {"id": f"cf-{name}-{index}", "name": "TrailShield", "category": "hiking shoes", "description": "Waterproof hiking shoes", "features": ["waterproof", "hiking", "slip-resistant"], "price": 120, "service_regions": ["US", "Canada"], "available": True, "evidence": [Evidence(id=f"cf:{name}:{index}", kind="observed", text="First-party controlled product evidence.", source="phase5_control")]}
            product_values.update(overrides)
            product = Product(**product_values)
            country = "Canada" if name == "location" else "US"
            context = build_context(text, source="phase5_counterfactual", context_id=f"cf:{name}:{index}").model_copy(update={"location": LocationContext(country=country)})
            result = score(context, product)
            decision = spend_safety(context, product, result, policy)
            cases.append({"group": name, "record_id": f"cf:{name}:{index}", "context": text, "expected_decision": expected, "predicted_decision": decision.decision, "expected": expected == decision.decision, "reason_codes": decision.reason_codes, "test_readiness": decision.test_readiness})
    summary = {"group_count": len(GROUPS), "case_count": len(cases), "decision_accuracy": sum(case["expected"] for case in cases) / len(cases), "counterfactual_consistency": sum(case["expected"] for case in cases) / len(cases), "by_group": {name: {"count": sum(case["group"] == name for case in cases), "accuracy": sum(case["expected"] for case in cases if case["group"] == name) / 6} for name, *_ in GROUPS}, "status": "one-feature policy counterfactual controls; no campaign outcome claim"}
    artifact = {"summary": summary, "cases": cases}
    Path("artifacts/phase5_counterfactual_stress.json").write_text(json.dumps(artifact, indent=2) + "\n")
    Path("reports/phase5_counterfactual_stress.md").write_text("# Phase 5 counterfactual stress\n\n" + json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
