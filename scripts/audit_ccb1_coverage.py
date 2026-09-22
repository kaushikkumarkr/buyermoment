from __future__ import annotations

import argparse
import csv
import hashlib
import json
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CCB1 = ROOT / "data" / "ccb1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def line_count(path: Path) -> int:
    with path.open("rb") as handle:
        return sum(1 for _ in handle)


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        return max(0, sum(1 for _ in csv.reader(handle)) - 1)


def parquet_row_count(path: Path) -> int | None:
    try:
        import pyarrow.parquet as parquet
    except ImportError:
        return None
    return parquet.ParquetFile(path).metadata.num_rows


def convapparel_stats(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        member = next(name for name in archive.namelist() if name.endswith("ConvApparel.json"))
        payload = json.loads(archive.read(member))
    conversations = payload.get("conversations", [])
    turns = sum(len(item.get("turns", [])) for item in conversations)
    recommendation_rows = sum(
        sum(len(turn.get("recommendations", []) or [None]) for turn in item.get("turns", []))
        for item in conversations
    )
    return {
        "archive_sha256": sha256(path),
        "conversations": len(conversations),
        "turns": turns,
        "recommendation_rows": recommendation_rows,
    }


def normalized_stats() -> dict[str, Any]:
    result: dict[str, Any] = {}
    for source in ("amazon_esci", "google_convapparel", "wayfair_wands"):
        path = CCB1 / "normalized" / f"{source}.jsonl"
        result[source] = {
            "path": str(path.relative_to(ROOT)),
            "records": line_count(path) if path.exists() else None,
            "sha256": sha256(path) if path.exists() else None,
        }
    return result


def split_stats() -> dict[str, Any]:
    result: dict[str, Any] = {}
    for split in ("train", "validation", "hidden_test"):
        path = CCB1 / split / "real.jsonl"
        counts = Counter()
        labels = Counter()
        if path.exists():
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    record = json.loads(line)
                    counts[record.get("source_dataset", "unknown")] += 1
                    labels[f"{record.get('source_dataset', 'unknown')}:{record.get('relevance', 'unknown')}"] += 1
        result[split] = {"records": sum(counts.values()), "by_source": dict(sorted(counts.items())), "labels": dict(sorted(labels.items()))}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit CCB-1 source coverage without model inference.")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts" / "ccb1_coverage_audit.json")
    args = parser.parse_args()

    esci_root = CCB1 / "raw" / "amazon_esci" / "esci-code" / "shopping_queries_dataset"
    wands_root = CCB1 / "raw" / "wayfair_wands"
    conv_path = CCB1 / "raw" / "google_convapparel" / "ConvApparel.zip"
    raw = {
        "amazon_esci": {
            "examples": parquet_row_count(esci_root / "shopping_queries_dataset_examples.parquet"),
            "products": parquet_row_count(esci_root / "shopping_queries_dataset_products.parquet"),
            "selected_normalization_cap": 10000,
        },
        "wayfair_wands": {
            "queries": csv_row_count(wands_root / "query.csv"),
            "products": csv_row_count(wands_root / "product.csv"),
            "labels": csv_row_count(wands_root / "label.csv"),
        },
        "google_convapparel": convapparel_stats(conv_path),
    }
    normalized = normalized_stats()
    counts = {source: item["records"] for source, item in normalized.items()}
    result = {
        "version": "phase8-ccb1-coverage-audit-v1",
        "generated_from_commit": "8d8ad25",
        "raw": raw,
        "normalized": normalized,
        "coverage": {
            "amazon_esci": {
                "record_basis": "examples parquet rows",
                "raw_rows": raw["amazon_esci"]["examples"],
                "used_rows": counts["amazon_esci"],
                "dropped_or_not_materialized": raw["amazon_esci"]["examples"] - counts["amazon_esci"],
                "coverage_fraction": counts["amazon_esci"] / raw["amazon_esci"]["examples"],
                "reason": "explicit 10,000-row v0.1 storage/review cap",
            },
            "wayfair_wands": {
                "record_basis": "label rows",
                "raw_rows": raw["wayfair_wands"]["labels"],
                "used_rows": counts["wayfair_wands"],
                "dropped_or_not_materialized": raw["wayfair_wands"]["labels"] - counts["wayfair_wands"],
                "coverage_fraction": counts["wayfair_wands"] / raw["wayfair_wands"]["labels"],
                "reason": "all downloaded label rows normalized",
            },
            "google_convapparel": {
                "record_basis": "turn-recommendation rows",
                "raw_rows": raw["google_convapparel"]["recommendation_rows"],
                "used_rows": counts["google_convapparel"],
                "dropped_or_not_materialized": raw["google_convapparel"]["recommendation_rows"] - counts["google_convapparel"],
                "coverage_fraction": counts["google_convapparel"] / raw["google_convapparel"]["recommendation_rows"],
                "reason": "all V1 recommendation rows normalized; relevance remains unknown where source is unlabeled",
            },
        },
        "normalized_total": sum(counts.values()),
        "splits": split_stats(),
        "augmentation_counts": {
            "azure_controlled": 500,
            "template_controls": 500,
            "hard_negatives": 500,
            "controlled_constraint_location": 140,
        },
        "unresolved": [
            "ConvApparel V2 is not present in the current raw archive.",
            "ESCI full-release training/evaluation is not materialized in CCB-1 v0.1.",
            "ConvApparel rows do not carry a universal human product-relevance label.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
