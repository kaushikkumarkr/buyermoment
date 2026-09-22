from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from buyermoment.demo import demo_businesses
from buyermoment.models import BusinessProfile, Evidence, Product


def synthetic_product(product_id: str, name: str, category: str, description: str, price: float, features: list[str], region: str = "US") -> Product:
    return Product(id=product_id, name=name, category=category, description=description, price=price, features=features, service_regions=[region], available=True, evidence=[Evidence(id=f"synthetic:{product_id}:catalog", kind="observed", text=f"Synthetic catalog record for {name}; this is not a live business fact.", source="phase6_synthetic_demo", source_record_id=product_id, provenance=["synthetic_demo_evidence"], confidence=1.0)])


def main() -> None:
    collected_at = datetime.now(timezone.utc).isoformat()
    packages = []
    for business in demo_businesses():
        packages.append({"business_id": business.id, "business_name": business.name, "evidence_status": "synthetic_demo", "collected_at": collected_at, "profile": business.model_dump(mode="json"), "target_markets": ["US"], "location_constraints": ["Use only product.service_regions; no additional geography inferred."], "unknowns": ["margin", "LTV", "CAC", "inventory", "conversion_rate"], "package_provenance": ["existing BuyerMoment demo fixture", "not customer or public-web validation"]})
    extras = [
        ("lumen-local-services", "Lumen Local Services", "local service", synthetic_product("lumen-clean", "Lumen Home Reset", "home organization service", "A synthetic local home-organization service scenario.", 180, ["in-home", "appointment"]), ["US"], "Synthetic local-service scenario; service radius is intentionally unknown."),
        ("trailwise-learning", "Trailwise Learning", "consumer subscription", synthetic_product("trailwise-monthly", "Trailwise Study Membership", "education subscription", "A synthetic education subscription scenario for benchmark coverage.", 49, ["monthly", "online", "tutoring"]), ["US", "Canada"], "Synthetic education/subscription scenario; age, outcomes, and availability are unknown."),
    ]
    for business_id, name, category, product, markets, note in extras:
        evidence = [Evidence(id=f"synthetic:{business_id}:profile", kind="observed", text=note, source="phase6_synthetic_demo", source_record_id=business_id, provenance=["synthetic_demo_evidence"], confidence=1.0)]
        profile = BusinessProfile(id=business_id, name=name, category=category, description=note, products=[product], evidence=evidence)
        packages.append({"business_id": business_id, "business_name": name, "evidence_status": "synthetic_demo", "collected_at": collected_at, "profile": profile.model_dump(mode="json"), "target_markets": markets, "location_constraints": [note], "unknowns": ["margin", "LTV", "CAC", "customer_demographics", "inventory", "conversion_rate"], "package_provenance": ["Phase 6 synthetic scenario", "not a real business or public-web validation"]})
    out = Path("data/phase6/business_packages.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(package) for package in packages) + "\n")
    print(json.dumps({"businesses": len(packages), "synthetic_demo_businesses": len(packages), "private_data": False, "path": str(out)}, indent=2))


if __name__ == "__main__":
    main()
