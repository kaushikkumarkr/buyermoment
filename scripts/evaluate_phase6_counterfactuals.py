from __future__ import annotations

import json
from pathlib import Path

from buyermoment.models import Evidence, LocationContext, Product
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import spend_safety


COUNTERFACTUALS = [
    ("budget", "I need waterproof hiking shoes under $50 and can order today.", "BLOCK", "BUDGET_INCOMPATIBLE"),
    ("location", "I need waterproof hiking shoes in Canada and can order today.", "BLOCK", "LOCATION_UNSERVICEABLE"),
    ("timing", "I might buy waterproof hiking shoes next year.", "ABSTAIN", "FUTURE_OR_CONDITIONAL_INTENT"),
    ("ownership", "I already bought waterproof hiking shoes. How do I clean them?", "BLOCK", "EXISTING_OWNER_SUPPORT"),
    ("research", "I am researching waterproof hiking shoes for a market report.", "ABSTAIN", "RESEARCH_ONLY"),
    ("shipping", "I need waterproof hiking shoes tomorrow, but they do not ship in time.", "BLOCK", "SHIPPING_UNSERVICEABLE"),
    ("recipient", "I need to buy waterproof hiking shoes for my mother and can order today.", "TEST", "EVIDENCE_BACKED_COMMERCIAL_CONTEXT"),
    ("conditional", "If finance approves, I may buy waterproof hiking shoes next quarter.", "ABSTAIN", "FUTURE_OR_CONDITIONAL_INTENT"),
    ("negative", "I dislike this brand and want to understand alternatives, not buy today.", "ABSTAIN", "NEGATIVE_SENTIMENT_OR_COMPLAINT"),
    ("product", "I need accounting software, not waterproof hiking shoes.", "ABSTAIN", "INSUFFICIENT_EVIDENCE"),
]


def main() -> None:
    product = Product(id="phase6-cf", name="TrailShield", category="hiking shoes", description="Waterproof hiking shoes", features=["waterproof", "hiking", "slip-resistant"], price=120, service_regions=["US"], available=True, shipping_deadline_met=True, evidence=[Evidence(id="phase6:cf:product", kind="observed", text="Controlled first-party product evidence.", source="phase6_control")])
    base_text = "I need waterproof hiking shoes under $150 and can order today."
    rows = []
    for repeat in range(10):
        base_context = build_context(base_text, source="phase6_counterfactual", context_id=f"base:{repeat}").model_copy(update={"location": LocationContext(country="US")})
        base_score = score(base_context, product)
        base_decision = spend_safety(base_context, product, base_score)
        rows.append({"pair_id": f"base:{repeat}", "variant": "base", "category": "base", "expected_decision": "TEST", "predicted_decision": base_decision.decision, "reason_codes": base_decision.reason_codes, "score": base_score.model_dump(mode="json")})
        for category, text, expected, reason in COUNTERFACTUALS:
            country = "Canada" if category == "location" else "US"
            context = build_context(text, source="phase6_counterfactual", context_id=f"{category}:{repeat}").model_copy(update={"location": LocationContext(country=country)})
            result = score(context, product)
            decision = spend_safety(context, product, result)
            reason_ok = reason in decision.reason_codes or (expected == "TEST" and decision.decision == "TEST")
            stable = all(abs(getattr(base_score, component) - getattr(result, component)) <= 0.15 for component in ("product_fit", "location_fit")) if category in {"recipient", "timing"} else None
            rows.append({"pair_id": f"{category}:{repeat}", "variant": "counterfactual", "category": category, "expected_decision": expected, "predicted_decision": decision.decision, "direction_correct": (decision.decision == expected), "reason_code_correct": reason_ok, "unaffected_score_stable": stable, "reason_codes": decision.reason_codes, "score": result.model_dump(mode="json")})
    counters = [row for row in rows if row["variant"] == "counterfactual"]
    summary = {"base_cases": 10, "counterfactual_cases": len(counters), "direction_correctness": sum(row["direction_correct"] for row in counters) / len(counters), "reason_code_correctness": sum(row["reason_code_correct"] for row in counters) / len(counters), "unaffected_score_stability": sum(row["unaffected_score_stable"] for row in counters if row["unaffected_score_stable"] is not None) / sum(row["unaffected_score_stable"] is not None for row in counters), "by_category": {category: {"count": 10, "direction_correctness": sum(row["direction_correct"] for row in counters if row["category"] == category) / 10, "reason_code_correctness": sum(row["reason_code_correct"] for row in counters if row["category"] == category) / 10} for category, *_ in COUNTERFACTUALS}, "status": "Phase 6 one-variable counterfactual controls; no campaign outcome claim"}
    Path("artifacts/phase6_counterfactual.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=2) + "\n")
    Path("reports/counterfactual_phase6.md").write_text("# Phase 6 counterfactual robustness\n\n" + json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
