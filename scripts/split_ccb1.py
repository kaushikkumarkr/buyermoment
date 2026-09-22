from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from buyermoment.models import CommercialContextRecord


def group_key(record: CommercialContextRecord) -> str:
    parent = record.metadata.get("parent_record_id")
    if parent:
        return str(parent)
    if record.source_dataset == "amazon_esci":
        return f"{record.source_dataset}:{record.metadata.get('query_id', record.source_record_id)}"
    if record.source_dataset == "wayfair_wands":
        return f"{record.source_dataset}:{record.metadata.get('query_id', record.source_record_id)}"
    parts = record.source_record_id.split(":")
    return ":".join(parts[:4]) if len(parts) >= 4 else record.source_record_id


def stable_bucket(key: str, seed: int) -> float:
    digest = hashlib.sha256(f"{seed}:{key}".encode()).hexdigest()
    return int(digest[:12], 16) / 16**12


def main() -> None:
    parser = argparse.ArgumentParser(description="Create source-aware CCB-1 train/validation/hidden-test JSONL splits.")
    parser.add_argument("--input", action="append", default=None, help="Input directory; repeat to include augmented/hard-negative directories")
    parser.add_argument("--seed", type=int, default=20260921)
    args = parser.parse_args()
    inputs = [Path(value) for value in (args.input or ["data/ccb1/normalized"])]
    records: list[CommercialContextRecord] = []
    seen_record_ids: set[str] = set()
    duplicate_records = 0
    for directory in inputs:
        for path in sorted(directory.glob("*.jsonl")):
            if any(marker in path.name for marker in ("smoke", "template")):
                continue
            with path.open() as stream:
                for line in stream:
                    if not line.strip():
                        continue
                    record = CommercialContextRecord.model_validate_json(line)
                    if record.record_id in seen_record_ids:
                        duplicate_records += 1
                        continue
                    seen_record_ids.add(record.record_id)
                    records.append(record)
    groups: dict[str, list[CommercialContextRecord]] = defaultdict(list)
    for record in records:
        groups[group_key(record)].append(record)
    assignments: dict[str, str] = {}
    for key in groups:
        bucket = stable_bucket(key, args.seed)
        assignments[key] = "hidden_test" if bucket >= 0.9 else ("validation" if bucket >= 0.8 else "train")
    by_split: dict[str, list[CommercialContextRecord]] = defaultdict(list)
    for key, grouped in groups.items():
        by_split[assignments[key]].extend(record.model_copy(update={"split": assignments[key]}) for record in grouped)
    for split, split_records in by_split.items():
        destination = Path("data/ccb1") / split / "real.jsonl"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(record.model_dump_json() for record in split_records) + "\n")
    summary = {"seed": args.seed, "input_records_after_dedupe": len(records), "duplicate_records_dropped": duplicate_records, "groups": len(groups), "record_counts": {key: len(value) for key, value in by_split.items()}, "group_counts": Counter(assignments.values()), "group_leakage_check": len(groups) == sum(len({group_key(record) for record in value}) for value in by_split.values())}
    Path("data/ccb1/split_manifest.json").write_text(json.dumps(summary, indent=2, default=dict) + "\n")
    print(json.dumps(summary, indent=2, default=dict))


if __name__ == "__main__":
    main()
