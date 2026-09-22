from __future__ import annotations

import argparse
import hashlib
import json
import re
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
    if record.source_dataset == "google_convapparel":
        # ConvApparel rows are turn/item records and augmentations point at the
        # full parent id. Exact normalized utterance collisions must also stay
        # together or they can leak lexical answers across splits.
        normalized = re.sub(r"[^a-z0-9]+", " ", record.context_text.lower()).strip()
        return f"{record.source_dataset}:context:{normalized}"
    if record.source_dataset == "ccb1_controlled":
        family = "location" if record.record_id.startswith("controlled-location:") else "constraint"
        return f"{record.source_dataset}:{family}"
    return record.source_record_id


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
    # Merge source/query groups that share an exact normalized context. This
    # prevents repeated queries from becoming lexical duplicates across splits
    # while preserving parent->augmentation grouping.
    parent: dict[str, str] = {key: key for key in groups}
    def find(key: str) -> str:
        while parent[key] != key:
            parent[key] = parent[parent[key]]
            key = parent[key]
        return key
    def union(left: str, right: str) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root
    context_groups: dict[str, list[str]] = defaultdict(list)
    for key, grouped in groups.items():
        for record in grouped:
            normalized = re.sub(r"[^a-z0-9]+", " ", record.context_text.lower()).strip()
            context_groups[normalized].append(key)
    for keys in context_groups.values():
        for key in keys[1:]:
            union(keys[0], key)
    components: dict[str, list[CommercialContextRecord]] = defaultdict(list)
    for key, grouped in groups.items():
        components[find(key)].extend(grouped)
    assignments: dict[str, str] = {}
    for key in components:
        bucket = stable_bucket(key, args.seed)
        assignments[key] = "hidden_test" if bucket >= 0.9 else ("validation" if bucket >= 0.8 else "train")
    by_split: dict[str, list[CommercialContextRecord]] = defaultdict(list)
    for key, grouped in components.items():
        by_split[assignments[key]].extend(record.model_copy(update={"split": assignments[key]}) for record in grouped)
    for split, split_records in by_split.items():
        destination = Path("data/ccb1") / split / "real.jsonl"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(record.model_dump_json() for record in split_records) + "\n")
    summary = {"seed": args.seed, "input_records_after_dedupe": len(records), "duplicate_records_dropped": duplicate_records, "groups_before_context_merge": len(groups), "groups": len(components), "record_counts": {key: len(value) for key, value in by_split.items()}, "group_counts": Counter(assignments.values()), "group_leakage_check": len(components) == sum(len({find(group_key(record)) for record in value}) for value in by_split.values())}
    Path("data/ccb1/split_manifest.json").write_text(json.dumps(summary, indent=2, default=dict) + "\n")
    print(json.dumps(summary, indent=2, default=dict))


if __name__ == "__main__":
    main()
