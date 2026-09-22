from __future__ import annotations

import json
from pathlib import Path

from buyermoment.models import CommercialContext, DatasetRecord, Evidence, Product
from buyermoment.scoring import build_context


def main() -> None:
    examples = [
        ("I need waterproof hiking boots under $150 for Yellowstone.", "consideration", "waterproof hiking boots"),
        ("Compare the best hiking boots for wet trails.", "comparison", "hiking boots"),
        ("I'm researching the history of waterproof hiking boots.", "informational", "hiking boots"),
        ("How do I clean the waterproof boots I already own?", "informational", "boot care"),
        ("What is a fragrance-free routine for sensitive skin under $80?", "consideration", "skincare routine"),
        ("We need SOC 2-ready customer support analytics this quarter.", "comparison", "support analytics"),
        ("Show me options for a lightweight trail shoe.", "exploration", "trail shoe"),
        ("Can I order a moisturizer to Toronto tomorrow?", "transactional", "moisturizer"),
        ("What is the academic history of customer support metrics?", "informational", "support analytics"),
        ("This product is disappointing and I want a refund.", "informational", "refund support"),
    ]
    records = []
    for index in range(100):
        text, stage, category = examples[index % len(examples)]
        context = build_context(text, source="CCB-1 seed template", context_id=f"ccb-{index + 1:04d}")
        context = context.model_copy(update={"purchase_stage": stage})
        product = Product(id=f"seed-product-{index + 1:04d}", name=f"Seed {category.title()}", category=category, description=f"Demo product relevant to {category}.", price=120 if index % 3 else 72, features=context.constraints.required_features, evidence=[Evidence(id=f"seed-evidence-{index + 1:04d}", kind="observed", text=f"Seed product description for {category}.", source="seed_fixture", source_record_id=f"seed-product-{index + 1:04d}")])
        records.append(DatasetRecord(source_dataset="CCB-1", source_record_id=f"seed-{index + 1:04d}", source_license="Synthetic fixture; no external dataset license", original_label=stage, transformation_history=["generated from deterministic seed templates", "stage label retained as gold label"], context=context, product=product, split="hidden_test" if index >= 90 else ("validation" if index >= 80 else "train"), metadata={"case_type": category, "synthetic": True}))
    destination = Path("data/gold/ccb_v0_1.jsonl")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(record.model_dump_json() for record in records) + "\n")
    print(f"wrote {len(records)} records to {destination}")


if __name__ == "__main__":
    main()

