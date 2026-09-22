from __future__ import annotations

import json
from pathlib import Path

from buyermoment.demo import demo_businesses
from buyermoment.scoring import build_context, score

def candidate_text(business_id: str, product_name: str, category: str, features: list[str], price: float | None, region: str) -> str:
    feature_text = " and ".join(features[:2]) if features else category
    budget = f" under ${price + 15:.0f}" if price is not None else ""
    return f"I am evaluating {product_name} for {category} and need {feature_text}{budget} with service in {region}."

def main() -> None:
    rows = []
    for business in demo_businesses():
        for product in business.products:
            for variant in range(8 if product is business.products[0] else 7):
                region = product.service_regions[variant % len(product.service_regions)] if product.service_regions else "the service area"
                text = candidate_text(business.id, product.name, product.category, product.features, product.price, region)
                if variant == 4:
                    text = f"I am researching the history of {product.category}, including {product.name}, for a paper."
                elif variant == 5:
                    text = f"How do I use or maintain the {product.name} I already own?"
                elif variant == 6:
                    text = f"What should a buyer look for when exploring {product.category} options like {product.name}?"
                elif variant == 7:
                    text = f"I cannot buy {product.name} until next year; what should I learn about {product.category} now?"
                result = score(build_context(text, source="demo business evidence", context_id=f"{business.id}:{product.id}:{variant}"), product)
                useful = bool(product.evidence and result.constraint_match >= 0.5 and result.product_fit >= 0.5 and result.purchase_stage in {"consideration", "comparison", "transactional"})
                review = "USEFUL" if useful else "PLAUSIBLE_BUT_WEAK"
                would_test = "yes" if useful and result.purchase_stage in {"consideration", "comparison", "transactional"} else "maybe"
                evidence_ids = [item.id for item in product.evidence]
                rows.append({"candidate_id": f"{business.id}:candidate:{len([row for row in rows if row['business_id'] == business.id]):02d}", "business_id": business.id, "business": business.name, "product_id": product.id, "title": f"{product.name} for {product.category} demand", "context_text": text, "purchase_stage": result.purchase_stage, "constraints": result.extracted_constraint_fields, "score": result.model_dump(mode="json"), "evidence_ids": evidence_ids, "review": {"label": review, "would_test_with_real_ad_budget": would_test, "reason": "Engineering review based only on catalog evidence; no campaign or revenue claim."}, "review_source": "internal_engineering_review_not_customer_validation"})
    by_business = {}
    for row in rows:
        by_business.setdefault(row["business_id"], []).append(row)
    summary = {"businesses": {}, "candidate_count": len(rows), "status": "pre-campaign internal engineering review; not customer or revenue validation"}
    for business_id, candidates in by_business.items():
        ranked = sorted(candidates, key=lambda row: row["score"]["overall"], reverse=True)
        summary["businesses"][business_id] = {"candidate_count": len(candidates), "top_5_usefulness": sum(row["review"]["label"] == "USEFUL" for row in ranked[:5]) / min(5, len(ranked)), "unsupported_rate": sum(row["review"]["label"] == "UNSUPPORTED" for row in candidates) / len(candidates), "would_test_yes_rate": sum(row["review"]["would_test_with_real_ad_budget"] == "yes" for row in candidates) / len(candidates), "would_test_counts": {key: sum(row["review"]["would_test_with_real_ad_budget"] == key for row in candidates) for key in ("yes", "maybe", "no")}}
    artifact = {"summary": summary, "candidates": rows}
    Path("artifacts/real_business_validation.json").write_text(json.dumps(artifact, indent=2) + "\n")
    Path("reports/real_business_validation.md").write_text("# Real-business validation\n\n" + json.dumps(summary, indent=2) + "\n\nThis is a structured internal engineering review of demo catalog evidence. It is not external validation and contains no performance claim.\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
