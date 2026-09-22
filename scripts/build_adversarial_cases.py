from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.models import CommercialContextRecord, Evidence, LocationContext

CASES = [
    ("mixed_locations", "I'm in Texas now but moving to Boston next month. Can I buy waterproof boots that ship there?", "consideration", True, None),
    ("future_location", "I will be in Boston next month; I need a local service there by then.", "consideration", True, False),
    ("third_party", "My mother lives in Nevada. Can I buy this skincare set for her?", "transactional", True, None),
    ("existing_owner", "I already purchased these shoes. Should I return them because they hurt?", "informational", False, None),
    ("negative_sentiment", "I'm researching alternatives because I dislike this brand, not buying today.", "informational", False, None),
    ("unavailable_geography", "The product fits everything I want, but it doesn't ship to my country.", "consideration", True, False),
    ("currency_mismatch", "I need a CRM under 300 CAD per month, but this plan is priced in USD.", "consideration", True, None),
    ("shipping_constraint", "I need something under $100 total including shipping and it must arrive by Friday.", "transactional", True, None),
    ("research_keywords", "I'm researching the history of waterproof hiking boots for a paper.", "informational", False, None),
    ("comparison_no_purchase", "For a class assignment, compare HubSpot and Pipedrive without recommending one to buy.", "informational", False, None),
    ("delayed_purchase", "I can't buy this until next year; what should I learn about the category now?", "exploration", False, None),
    ("beneficiary_location", "I'm comparing options for my brother who lives in Canada, not for myself.", "comparison", True, None),
    ("service_travel", "This service is available only in California, but I travel there often. Can I use it?", "consideration", True, None),
    ("support_keyword", "How do I export contacts from my CRM?", "informational", False, None),
    ("complaint_keyword", "Why is my current CRM so slow?", "informational", False, None),
]

def main() -> None:
    parser = argparse.ArgumentParser(description="Build a separate adversarial benchmark without touching hidden splits.")
    parser.add_argument("--repeat", type=int, default=8)
    parser.add_argument("--output", type=Path, default=Path("data/ccb1/adversarial/adversarial_v0_1.jsonl"))
    args = parser.parse_args()
    rows: list[CommercialContextRecord] = []
    for repeat in range(args.repeat):
        for index, (kind, text, stage, commercial, location_fit) in enumerate(CASES):
            record_id = f"adversarial:{kind}:{repeat:02d}:{index:02d}"
            rows.append(CommercialContextRecord(
                record_id=record_id, source_dataset="ccb1_adversarial", source_record_id=record_id,
                source_license="Synthetic reviewed adversarial benchmark; no external license",
                context_text=text, original_query=text, product_id=f"adversarial-product:{kind}",
                product_title="Referenced product or service",
                product_description="A deliberately generic product context; no unsupported product facts are supplied.",
                product_attributes={"service_regions": ["Texas"] if kind in {"future_location", "service_travel"} else (["Canada"] if kind == "unavailable_geography" else ["US", "Canada"])},
                location=LocationContext(country="US", region="Texas" if "Texas" in text else None, city="Boston" if "Boston" in text else None, location_specificity="region" if "Texas" in text else "unknown"),
                purchase_stage=stage, commerciality="high" if commercial else "none",
                evidence=[Evidence(id=f"{record_id}:text", kind="observed", text=text, source="phase3-adversarial-review", source_record_id=record_id, confidence=1.0)],
                provenance=["phase3 manually authored adversarial template", "not part of CCB-1 hidden split"],
                transformation_history=["created to challenge location, ownership, research, sentiment, currency, shipping, and timing behavior"],
                confidence=1.0,
                metadata={"adversarial_type": kind, "gold_commerciality_positive": commercial, "location_fit_gold": location_fit, "label_origin": "manual_phase3_control"},
            ))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(row.model_dump_json() for row in rows) + "\n")
    print(json.dumps({"records": len(rows), "template_types": len(CASES), "output": str(args.output)}, indent=2))

if __name__ == "__main__":
    main()
