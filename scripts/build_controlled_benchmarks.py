from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.models import CommercialContextRecord, Evidence, LocationContext


FEATURES = ("waterproof", "slip-resistant", "fragrance-free", "sensitive skin", "12-hour", "SOC 2", "fast shipping")


def evidence(record_id: str, text: str) -> list[Evidence]:
    return [Evidence(id=f"{record_id}:text", kind="observed", text=text, source="ccb1-controlled-benchmark-v0.1", source_record_id=record_id, confidence=1.0)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create explicitly labeled, non-human CCB-1 constraint/location controls.")
    parser.add_argument("--output", type=Path, default=Path("data/ccb1/augmented/controlled_benchmark.jsonl"))
    args = parser.parse_args()
    records: list[CommercialContextRecord] = []
    for index in range(100):
        feature = FEATURES[index % len(FEATURES)]
        text = f"I need a {feature} solution under ${80 + index} for my team this week."
        record_id = f"controlled-constraint:{index:03d}"
        records.append(CommercialContextRecord(record_id=record_id, source_dataset="ccb1_controlled", source_record_id=record_id, source_license="Synthetic controlled benchmark; no external license", context_text=text, original_query=text, product_id=f"controlled-product:{index:03d}", product_title=f"{feature} solution", product_description=f"A controlled product with the {feature} requirement.", product_attributes={"features": feature}, problem="Explicitly stated constrained need.", desired_outcome="Find a matching product.", use_case="Controlled extraction evaluation.", constraints={"budget_max": 80 + index, "required_features": [feature], "timing": "this week"}, purchase_stage="consideration", commerciality="medium", evidence=evidence(record_id, text), provenance=["controlled benchmark template"], transformation_history=["generated as a labeled constraint control; not observed customer data"], confidence=1.0, split="unassigned", metadata={"label_origin": "controlled_constraint_target", "gold_required_features": [feature]}))
    for index in range(40):
        city, region, served = ("Austin", "Texas", index % 2 == 0)
        text = f"I need an on-site service in {city}, {region} this week."
        record_id = f"controlled-location:{index:03d}"
        service_regions = ["Austin, Texas"] if served else ["Dallas, Texas"]
        records.append(CommercialContextRecord(record_id=record_id, source_dataset="ccb1_controlled", source_record_id=record_id, source_license="Synthetic controlled benchmark; no external license", context_text=text, original_query=text, product_id=f"controlled-location-product:{index:03d}", product_title="On-site service", product_description="A service with explicitly listed service regions.", product_attributes={"service_regions": service_regions}, location=LocationContext(country="US", region=region, city=city, location_specificity="city"), purchase_stage="consideration", commerciality="medium", evidence=evidence(record_id, text), provenance=["controlled benchmark template"], transformation_history=["generated as a labeled location/serviceability control; not observed customer data"], confidence=1.0, split="unassigned", metadata={"label_origin": "controlled_location_target", "location_fit_gold": served}))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(record.model_dump_json() for record in records) + "\n")
    print(json.dumps({"records": len(records), "constraints": 100, "locations": 40, "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
