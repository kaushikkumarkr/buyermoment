from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from buyermoment.models import CommercialContextRecord, Product
from buyermoment.scoring import build_context, score

def main() -> None:
    counts = Counter()
    examples: dict[str, list[str]] = {}
    rows = [CommercialContextRecord.model_validate_json(line) for line in Path("data/ccb1/adversarial/adversarial_v0_1.jsonl").read_text().splitlines() if line.strip()]
    for row in rows:
        product = Product(id=row.product_id or row.record_id, name=row.product_title or "product", category="product", description=row.product_description or "product", service_regions=row.product_attributes.get("service_regions", []))
        result = score(build_context(row.context_text), product)
        expected_commercial = bool(row.metadata["gold_commerciality_positive"])
        if expected_commercial is False and result.commerciality >= 0.5:
            counts["false_commercial_intent"] += 1
            examples.setdefault("false_commercial_intent", []).append(row.record_id)
        if row.purchase_stage and result.purchase_stage != row.purchase_stage:
            counts["wrong_purchase_stage"] += 1
            examples.setdefault("wrong_purchase_stage", []).append(row.record_id)
        if row.metadata.get("location_fit_gold") is not None and (result.location_fit >= 0.5) != bool(row.metadata["location_fit_gold"]):
            counts["location_failure"] += 1
            examples.setdefault("location_failure", []).append(row.record_id)
        if result.confidence >= 0.8 and row.purchase_stage and result.purchase_stage != row.purchase_stage:
            counts["overconfident_prediction"] += 1
            examples.setdefault("overconfident_prediction", []).append(row.record_id)
    constraint = json.loads(Path("artifacts/constraint_breakdown.json").read_text())["metrics"]
    if constraint["required_feature"]["fn"]:
        counts["missed_hard_constraint"] += int(constraint["required_feature"]["fn"])
    summary = {"failure_counts": dict(counts), "examples": {key: value[:10] for key, value in examples.items()}, "source": ["adversarial_benchmark.json", "constraint_breakdown.json"], "status": "measured taxonomy counts; categories are assigned by deterministic benchmark mismatch rules"}
    Path("artifacts/failure_taxonomy.json").write_text(json.dumps(summary, indent=2) + "\n")
    Path("reports/failure_taxonomy.md").write_text("# Failure taxonomy counts\n\n" + json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
