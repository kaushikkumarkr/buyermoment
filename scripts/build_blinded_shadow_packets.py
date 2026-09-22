from __future__ import annotations

import json
import re
from pathlib import Path

from buyermoment.models import BusinessProfile, Product
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import spend_safety


def normalized(text: str) -> str:
    return re.sub(r"\W+", " ", text.lower()).strip()


def candidate_rows(package: dict, existing: dict[str, list[dict]]) -> list[dict]:
    business_id = package["business_id"]
    if business_id in existing:
        rows = []
        local_seen: set[str] = set()
        for candidate in existing[business_id]:
            key = normalized(candidate["context_text"])
            if key not in local_seen:
                local_seen.add(key)
                rows.append(candidate)
            if len(rows) == 10:
                break
        if len(rows) >= 8:
            return rows
        profile = BusinessProfile.model_validate(package["profile"])
        product = profile.products[0]
        for index, text in enumerate((f"I need {product.name} for a defined use case this month in review case {business_id}.", f"What constraint should I verify before choosing {product.name} in review case {business_id}?")):
            rows.append({"candidate_id": f"{business_id}:phase6:supplement:{index:02d}", "business_id": business_id, "business_name": profile.name, "context_text": text, "product": product.model_dump(mode="json"), "evidence": [item.model_dump(mode="json") for item in [*product.evidence, *profile.evidence]], "constraints": {}, "provenance": ["Phase 6 supplemental candidate", *package["package_provenance"]]})
        return rows
    profile = BusinessProfile.model_validate(package["profile"])
    product = profile.products[0]
    templates = [
        f"I need {product.category} and want {product.name} this month.",
        f"What should I look for in {product.category} before I subscribe?",
        f"Compare {product.name} with alternatives for my team.",
        f"I am researching {product.category} for a report, not buying.",
        f"Can {product.name} serve me in {profile.products[0].service_regions[0]}?",
        f"I might buy {product.name} next year if the budget is approved.",
        f"I need {product.name} under ${product.price} and can start today.",
        f"I already use a similar {product.category}; how do I switch?",
        "This is for my employer, and we are gathering options.",
        f"Please compare the constraints for {product.name}.",
    ]
    return [{"candidate_id": f"{business_id}:phase6:{index:02d}", "business_id": business_id, "business_name": profile.name, "context_text": text, "product": product.model_dump(mode="json"), "evidence": [item.model_dump(mode="json") for item in [*product.evidence, *profile.evidence]], "constraints": {}, "provenance": ["Phase 6 synthetic scenario candidate", *package["package_provenance"]]} for index, text in enumerate(templates)]


def main() -> None:
    packages = [json.loads(line) for line in Path("data/phase6/business_packages.jsonl").read_text().splitlines() if line.strip()]
    source = json.loads(Path("artifacts/real_business_validation.json").read_text())
    existing: dict[str, list[dict]] = {}
    for candidate in source["candidates"]:
        existing.setdefault(candidate["business_id"], []).append({"candidate_id": candidate["candidate_id"], "business_id": candidate["business_id"], "business_name": candidate["business"], "context_text": candidate["context_text"], "product": next(product for package in packages if package["business_id"] == candidate["business_id"] for product in package["profile"]["products"] if product["id"] == candidate["product_id"]), "evidence": candidate["score"]["evidence"], "constraints": candidate["constraints"], "provenance": ["existing demo-business candidate", "review labels kept separate"]})
    candidates = []
    seen: set[tuple[str, str]] = set()
    for package in packages:
        for candidate in candidate_rows(package, existing):
            key = (candidate["business_id"], normalized(candidate["context_text"]))
            if key not in seen:
                seen.add(key)
                candidates.append(candidate)
    private = Path("shadow_reviews/private")
    private.mkdir(parents=True, exist_ok=True)
    predictions = []
    packets = []
    for candidate in candidates:
        product = Product.model_validate(candidate["product"])
        context = build_context(candidate["context_text"], source="phase6_shadow", context_id=candidate["candidate_id"])
        result = score(context, product)
        decision = spend_safety(context, product, result)
        review_split = "shadow_holdout" if candidate["business_id"] in {"lumen-local-services", "trailwise-learning"} else "shadow_dev"
        predictions.append({"packet_id": candidate["candidate_id"], "review_split": review_split, "buyer_moment": candidate, "contextfit": result.model_dump(mode="json"), "spend_decision": decision.model_dump(mode="json")})
        packets.append({"packet_id": candidate["candidate_id"], "review_split": review_split, "business_name": candidate["business_name"], "business_id": candidate["business_id"], "context_text": candidate["context_text"], "product": candidate["product"], "evidence": candidate["evidence"], "constraints": candidate["constraints"], "provenance": candidate["provenance"], "review_fields": {"decision": None, "would_spend_real_money": None, "confidence": None, "reason": None, "reviewer_id": None}})
    (private / "model_predictions.jsonl").write_text("\n".join(json.dumps(row) for row in predictions) + "\n")
    (private / "reviewer_packets.jsonl").write_text("\n".join(json.dumps(row) for row in packets) + "\n")
    manifest = {"businesses": len(packages), "candidates": len(candidates), "candidates_per_business": {package["business_id"]: sum(row["business_id"] == package["business_id"] for row in candidates) for package in packages}, "review_split": {"shadow_dev": sum(candidate["business_id"] not in {"lumen-local-services", "trailwise-learning"} for candidate in candidates), "shadow_holdout": sum(candidate["business_id"] in {"lumen-local-services", "trailwise-learning"} for candidate in candidates)}, "review_packets": "shadow_reviews/private/reviewer_packets.jsonl", "model_predictions": "shadow_reviews/private/model_predictions.jsonl", "blindness": "model decision and score are excluded from reviewer packets", "status": "packets prepared; no independent human submissions yet"}
    Path("artifacts/phase6_shadow_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    Path("reports/blinded_shadow_pilot.md").write_text("# Blinded shadow-pilot packet generation\n\n" + json.dumps(manifest, indent=2) + "\n\nReviewer packets contain business evidence and candidate context only. Predictions are stored separately and joined only after reviewer submission. Five packages are included, but the two added verticals are explicitly synthetic scenarios; no private customer data is committed.\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
