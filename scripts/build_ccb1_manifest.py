from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def jsonl_stats(path: Path) -> dict[str, Any]:
    records = 0
    with path.open() as stream:
        for line in stream:
            if line.strip():
                records += 1
    return {"path": str(path), "records": records, "sha256": sha256(path)}


def unique_records(paths: list[Path]) -> int:
    record_ids: set[str] = set()
    for path in paths:
        with path.open() as stream:
            for line in stream:
                if line.strip():
                    record_ids.add(json.loads(line)["record_id"])
    return len(record_ids)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a portable CCB-1 manifest from local pipeline artifacts.")
    parser.add_argument("--output", type=Path, default=Path("ccb1_manifest.json"))
    args = parser.parse_args()
    normalized = [jsonl_stats(path) for path in sorted(Path("data/ccb1/normalized").glob("*.jsonl"))]
    augmented = [jsonl_stats(path) for path in sorted(Path("data/ccb1/augmented").glob("*.jsonl")) if "smoke" not in path.name]
    azure_paths = [path for path in Path("data/ccb1/augmented").glob("stage_a_azure*.jsonl") if "smoke" not in path.name]
    splits = {split: [jsonl_stats(path) for path in sorted((Path("data/ccb1") / split).glob("*.jsonl"))] for split in ("train", "validation", "hidden_test")}
    source_manifest = json.loads(Path("data/ccb1/source_manifest.json").read_text())
    normalization_manifest = json.loads(Path("data/ccb1/normalized/normalization_manifest.json").read_text())
    split_manifest = json.loads(Path("data/ccb1/split_manifest.json").read_text())
    model_config_path = Path("configs/model_roles.json")
    manifest = {
        "version": "CCB-1 v0.1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_datasets": ["Google ConvApparel", "Amazon ESCI", "Wayfair WANDS"],
        "source_artifacts": source_manifest,
        "source_license_references": {
            "google_convapparel": "CC BY 4.0; https://huggingface.co/datasets/google/ConvApparel",
            "amazon_esci": "Apache-2.0 with upstream LICENSE/NOTICE; https://github.com/amazon-research/esci-code",
            "wayfair_wands": "MIT; https://github.com/wayfair/WANDS",
        },
        "normalized_files": normalized,
        "normalization_runs": normalization_manifest,
        "augmentation_files": augmented,
        "record_counts": {
            "real_normalized": sum(item["records"] for item in normalized),
            "conversational_augmentations": unique_records(azure_paths),
            "template_control_records": sum(item["records"] for item in augmented if "template" in item["path"]),
            "hard_negatives": sum(item["records"] for item in augmented if "hard_negatives" in item["path"]),
            "controlled_constraint_location_records": sum(item["records"] for item in augmented if "controlled_benchmark" in item["path"]),
            "gold_records": 0,
            "train": sum(item["records"] for item in splits["train"]),
            "validation": sum(item["records"] for item in splits["validation"]),
            "hidden_test": sum(item["records"] for item in splits["hidden_test"]),
        },
        "split_manifest": split_manifest,
        "model_configurations": json.loads(model_config_path.read_text()),
        "transformation_pipeline_version": "ccb1-normalize-split-augment-v0.1",
        "hidden_test_policy": "source/group aware; labels and examples are local ignored artifacts and are not committed",
    }
    args.output.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest["record_counts"], indent=2))


if __name__ == "__main__":
    main()
