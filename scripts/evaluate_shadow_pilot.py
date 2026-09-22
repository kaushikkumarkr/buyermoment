from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from buyermoment.demo import demo_businesses
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import spend_safety


def main() -> None:
    source = json.loads(Path("artifacts/real_business_validation.json").read_text())
    businesses = {business.id: business for business in demo_businesses()}
    products = {(business.id, product.id): product for business in businesses.values() for product in business.products}
    rows = []
    mapping = {"yes": "TEST", "maybe": "WATCH", "no": "ABSTAIN"}
    for candidate in source["candidates"]:
        product = products[(candidate["business_id"], candidate["product_id"])]
        context = build_context(candidate["context_text"], source="shadow_pilot_demo", context_id=candidate["candidate_id"])
        result = score(context, product)
        decision = spend_safety(context, product, result)
        human = mapping[candidate["review"]["would_test_with_real_ad_budget"]]
        rows.append({"candidate_id": candidate["candidate_id"], "business_id": candidate["business_id"], "predicted": decision.decision, "human_review_proxy": human, "agreement": decision.decision == human, "test_readiness": decision.test_readiness, "evidence_strength": decision.evidence_strength, "ambiguity_score": decision.ambiguity_score, "reason_codes": decision.reason_codes, "review_notes": candidate["review"].get("reason")})
    test = [row for row in rows if row["predicted"] == "TEST"]
    human_tests = [row for row in rows if row["human_review_proxy"] == "TEST"]
    summary = {"businesses_reviewed": len({row["business_id"] for row in rows}), "recommendations_reviewed": len(rows), "decision_distribution": dict(Counter(row["predicted"] for row in rows)), "human_proxy_distribution": dict(Counter(row["human_review_proxy"] for row in rows)), "decision_agreement": sum(row["agreement"] for row in rows) / len(rows), "test_precision_vs_human_proxy": sum(row["human_review_proxy"] == "TEST" for row in test) / len(test) if test else None, "test_recall_vs_human_proxy": sum(row["predicted"] == "TEST" for row in human_tests) / len(human_tests) if human_tests else None, "unsupported_test_rate": sum(row["review_notes"] == "UNSUPPORTED" for row in test) / len(test) if test else None, "scope": "existing demo-business review reused as a non-blinded human proxy; not customer or campaign validation"}
    Path("artifacts/shadow_pilot_validation.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=2) + "\n")
    Path("reports/shadow_pilot_validation.md").write_text("# Shadow-pilot validation\n\n" + json.dumps(summary, indent=2) + "\n\nThis is an offline shadow workflow. The existing reviewer labels were not collected blind to the generated candidates, so agreement is a proxy rather than independent validation. No campaign was launched.\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
