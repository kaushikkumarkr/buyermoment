from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from buyermoment.models import CommercialContextRecord, Product
from buyermoment.scoring import build_context, score
from evaluate_contextfit import binary_metrics, macro_f1

def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the Phase 3 adversarial benchmark.")
    parser.add_argument("--input", type=Path, default=Path("data/ccb1/adversarial/adversarial_v0_1.jsonl"))
    parser.add_argument("--json-output", type=Path, default=Path("artifacts/adversarial_benchmark.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/adversarial_benchmark.md"))
    args = parser.parse_args()
    rows = [CommercialContextRecord.model_validate_json(line) for line in args.input.read_text().splitlines() if line.strip()]
    stages: list[tuple[str, str]] = []
    intent: list[tuple[bool, bool]] = []
    location: list[tuple[bool, bool]] = []
    by_type: dict[str, list[tuple[bool, bool]]] = defaultdict(list)
    for row in rows:
        context = build_context(row.context_text, source=row.source_dataset, context_id=row.record_id).model_copy(update={"location": row.location})
        product = Product(id=row.product_id or row.record_id, name=row.product_title or "product", category="product", description=row.product_description or "product", service_regions=row.product_attributes.get("service_regions", []))
        result = score(context, product)
        expected = bool(row.metadata["gold_commerciality_positive"])
        predicted = result.commerciality >= 0.5
        intent.append((expected, predicted))
        by_type[str(row.metadata["adversarial_type"])].append((expected, predicted))
        stages.append((row.purchase_stage or "unknown", result.purchase_stage))
        if row.metadata.get("location_fit_gold") is not None:
            location.append((bool(row.metadata["location_fit_gold"]), result.location_fit >= 0.5))
    summary = {
        "benchmark": "Phase 3 adversarial CCB-1 benchmark", "record_count": len(rows),
        "template_types": dict(Counter(str(row.metadata["adversarial_type"]) for row in rows)),
        "metrics": {
            "commercial_intent": binary_metrics(intent),
            "purchase_stage": {"accuracy": sum(a == p for a, p in stages) / len(stages) if stages else None, "macro_f1": macro_f1([a for a, _ in stages], [p for _, p in stages]), "count": len(stages)},
            "location_fit": binary_metrics(location),
            "hard_negative_false_positive_rate": sum(predicted for actual, predicted in intent if not actual) / sum(not actual for actual, _ in intent) if any(not actual for actual, _ in intent) else None,
            "by_adversarial_type": {key: binary_metrics(value) for key, value in by_type.items()},
        },
        "status": "measured_on_manual_phase3_controls; separate from hidden CCB-1 split",
    }
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(summary, indent=2) + "\n")
    args.report_output.write_text("# Adversarial benchmark\n\n" + json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
