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
    for candidate in source["candidates"]:
        product = products[(candidate["business_id"], candidate["product_id"])]
        context = build_context(candidate["context_text"], source="demo business evidence", context_id=candidate["candidate_id"])
        result = score(context, product)
        decision = spend_safety(context, product, result)
        review = candidate["review"]
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "business_id": candidate["business_id"],
                "product_id": candidate["product_id"],
                "context_text": candidate["context_text"],
                "contextfit": result.model_dump(mode="json"),
                "spend_decision": decision.model_dump(mode="json"),
                "review": review,
                "human_approval_required": decision.human_approval_required,
            }
        )
    test_rows = [row for row in rows if row["spend_decision"]["decision"] == "TEST"]
    yes_rows = [row for row in rows if row["review"]["would_test_with_real_ad_budget"] == "yes"]
    agreement = sum(
        (row["spend_decision"]["decision"] == "TEST") == (row["review"]["would_test_with_real_ad_budget"] == "yes")
        for row in rows
    ) / len(rows)
    summary = {
        "candidate_count": len(rows),
        "decision_distribution": dict(Counter(row["spend_decision"]["decision"] for row in rows)),
        "test_precision_against_yes_review": sum(row["review"]["would_test_with_real_ad_budget"] == "yes" for row in test_rows) / len(test_rows) if test_rows else None,
        "test_recall_against_yes_review": sum(row["spend_decision"]["decision"] == "TEST" for row in yes_rows) / len(yes_rows) if yes_rows else None,
        "unsupported_recommendation_rate": sum(row["review"]["label"] == "UNSUPPORTED" for row in test_rows) / len(test_rows) if test_rows else None,
        "would_test_agreement": agreement,
        "human_approval_required_rate": sum(row["human_approval_required"] for row in rows) / len(rows) if rows else None,
        "review_scope": "internal engineering review of demo catalog evidence; not customer, campaign, or revenue validation",
    }
    artifact = {"summary": summary, "candidates": rows}
    Path("artifacts/real_business_spend_review.json").write_text(json.dumps(artifact, indent=2) + "\n")
    Path("reports/real_business_spend_review.md").write_text(
        "# Real-business spend-safety review\n\n"
        + json.dumps(summary, indent=2)
        + "\n\nThis review replays the existing 45 candidates against the Phase 4 deterministic safety layer. It is an internal evidence review, not a customer or revenue claim. Every output requires human approval.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
