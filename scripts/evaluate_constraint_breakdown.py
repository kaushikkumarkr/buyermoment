from __future__ import annotations

import json
from pathlib import Path

from buyermoment.models import CommercialContextRecord, Product
from buyermoment.scoring import build_context, score

def f1(tp: int, fp: int, fn: int) -> dict[str, int | float | None]:
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": 2 * precision * recall / (precision + recall) if precision is not None and recall is not None and precision + recall else None}

def main() -> None:
    rows = [CommercialContextRecord.model_validate_json(line) for line in Path("data/ccb1/augmented/controlled_benchmark.jsonl").read_text().splitlines() if line.strip()]
    counts = {key: [0, 0, 0, 0] for key in ("numeric_budget", "required_feature", "excluded_feature", "compatibility", "timing", "geography", "language", "currency", "shipping")}
    location_pairs: list[tuple[bool, bool]] = []
    for row in rows:
        if row.source_dataset != "ccb1_controlled":
            continue
        result = score(build_context(row.context_text).model_copy(update={"location": row.location}), Product(id=row.product_id or row.record_id, name=row.product_title or "product", category="controlled", description=row.product_description or "product", features=[row.product_attributes.get("features", "")], service_regions=row.product_attributes.get("service_regions", [])))
        if row.metadata.get("location_fit_gold") is not None:
            location_pairs.append((bool(row.metadata["location_fit_gold"]), result.location_fit >= 0.5))
        if not row.constraints.required_features:
            continue
        fields = result.extracted_constraint_fields
        expected = {"required_feature": bool(row.constraints.required_features), "numeric_budget": row.constraints.budget_max is not None, "timing": row.constraints.timing is not None}
        predicted = {"required_feature": bool(fields.get("required_features")), "numeric_budget": fields.get("budget") is not None, "timing": fields.get("timing") is not None}
        for key in expected:
            counts[key][0] += int(expected[key] and predicted[key])
            counts[key][1] += int(not expected[key] and predicted[key])
            counts[key][2] += int(expected[key] and not predicted[key])
            counts[key][3] += 1
    metrics = {key: {**f1(values[0], values[1], values[2]), "count": values[3], "status": "measured" if values[3] else "not_computed"} for key, values in counts.items()}
    tp = sum(actual and predicted for actual, predicted in location_pairs)
    fp = sum(not actual and predicted for actual, predicted in location_pairs)
    fn = sum(actual and not predicted for actual, predicted in location_pairs)
    metrics["location_serviceability"] = {**f1(tp, fp, fn), "count": len(location_pairs), "status": "measured on controlled explicit serviceability controls"}
    summary = {"benchmark": "Phase 3 constraint extraction breakdown", "metrics": metrics, "status": "measured only for constraint types with explicit canonical labels; missing types are not fabricated"}
    Path("artifacts/constraint_breakdown.json").write_text(json.dumps(summary, indent=2) + "\n")
    Path("reports/constraint_breakdown.md").write_text("# Constraint breakdown\n\n" + json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
