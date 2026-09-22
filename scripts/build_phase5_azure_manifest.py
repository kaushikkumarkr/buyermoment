from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    source = [json.loads(line) for line in Path("artifacts/false_test_cases.jsonl").read_text().splitlines() if line.strip()]
    categories = ["ambiguous_intent", "future_intent", "third_party_research", "mixed_intent", "constraint_conflict", "location_conflict"]
    rows = []
    for index, case in enumerate(source):
        for category in categories:
            rows.append({"job_id": f"phase5-targeted-{index:03d}-{category}", "source_record_id": case["record_id"], "category": category, "input": case["context"], "instruction": "Generate one minimally changed adversarial variant that preserves product semantics and changes only the requested uncertainty or policy boundary. Return provenance and a proposed label; never replace the source label.", "model_role": "bulk_generator", "requires_human_review": True})
    out = Path("data/ccb1/phase5/azure_targeted_augmentation_manifest.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
    print(json.dumps({"records": len(rows), "source_false_tests": len(source), "status": "manifest only; no Azure call submitted"}, indent=2))


if __name__ == "__main__":
    main()
