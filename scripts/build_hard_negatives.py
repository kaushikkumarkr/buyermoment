from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.models import CommercialContextRecord, Evidence


TEMPLATES: tuple[tuple[str, str, str, str], ...] = (
    ("buy", "transactional", "high", "I need to buy {subject} soon and want the best option for my situation."),
    ("research", "informational", "none", "How did {subject} evolve, and what is its history?"),
    ("support", "informational", "none", "How do I use, clean, export from, or troubleshoot the {subject} I already own?"),
    ("complaint", "informational", "none", "Why is my current {subject} so frustrating or slow?"),
    ("comparison", "comparison", "medium", "Should I choose {subject} or an alternative for my situation?"),
)


def subject(record: CommercialContextRecord) -> str:
    return record.original_query or record.product_title or record.context_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Create explicit keyword-overlap hard negatives from real CCB-1 records.")
    parser.add_argument("--input", type=Path, default=Path("data/ccb1/normalized"))
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path("data/ccb1/augmented/hard_negatives.jsonl"))
    args = parser.parse_args()
    parents = []
    for path in sorted(args.input.glob("*.jsonl")):
        with path.open() as stream:
            for line in stream:
                if line.strip():
                    parents.append(CommercialContextRecord.model_validate_json(line))
                    if len(parents) >= args.limit:
                        break
        if len(parents) >= args.limit:
            break
    records: list[CommercialContextRecord] = []
    for parent in parents:
        for kind, stage, commerciality, template in TEMPLATES:
            record_id = f"hardneg:{parent.record_id}:{kind}"
            text = template.format(subject=subject(parent))
            records.append(CommercialContextRecord(
                record_id=record_id,
                source_dataset=parent.source_dataset,
                source_record_id=record_id,
                source_license=parent.source_license,
                source_version=parent.source_version,
                context_text=text,
                original_query=parent.original_query,
                product_id=parent.product_id,
                product_title=parent.product_title,
                product_description=parent.product_description,
                product_attributes=parent.product_attributes,
                purchase_stage=stage,
                commerciality=commerciality,
                location=parent.location,
                evidence=[*parent.evidence, Evidence(id=f"{record_id}:template", kind="hypothesis", text=text, source="ccb1-hard-negative-template-v0.1", source_record_id=parent.record_id, provenance=[parent.record_id], confidence=0.5)],
                provenance=[*parent.provenance, f"controlled hard-negative transformation from {parent.record_id}"],
                transformation_history=[*parent.transformation_history, f"generated {kind} hard negative with lexical product overlap", "labels are controlled targets, not source ground truth"],
                confidence=0.5,
                split="unassigned",
                metadata={"parent_record_id": parent.record_id, "hard_negative_type": kind, "label_origin": "controlled_hard_negative_target", "gold_commerciality_positive": commerciality in {"medium", "high"}},
            ))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(record.model_dump_json() for record in records) + ("\n" if records else ""))
    print(json.dumps({"parents": len(parents), "records": len(records), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
