from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.models import DatasetRecord
from buyermoment.scoring import score


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reproducible local CCB-1 evaluation.")
    parser.add_argument("--input", default="data/gold/ccb_v0_1.jsonl")
    parser.add_argument("--output", default="artifacts/evaluation")
    args = parser.parse_args()
    records = [DatasetRecord.model_validate_json(line) for line in Path(args.input).read_text().splitlines() if line.strip()]
    stage_hits = 0
    valid = 0
    for record in records:
        if record.product:
            result = score(record.context, record.product)
            stage_hits += result.purchase_stage == record.context.purchase_stage
            valid += 1
    summary = {
        "benchmark": "CCB-1 v0.1",
        "records": len(records),
        "scored_records": valid,
        "purchase_stage_accuracy": round(stage_hits / valid, 4) if valid else None,
        "constraint_extraction_f1": "not_computed_without_gold_spans",
        "unsupported_claim_rate": "not_computed_without_human_review",
        "status": "baseline_only; no fabricated performance claim",
    }
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (output / "report.md").write_text("# BuyerMoment benchmark report\n\n```json\n" + json.dumps(summary, indent=2) + "\n```\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

