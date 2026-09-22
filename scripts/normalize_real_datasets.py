from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.datasets import normalize_convapparel, normalize_esci, normalize_wands


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize downloaded source datasets into CCB-1 canonical JSONL.")
    parser.add_argument("--dataset", choices=["all", "google_convapparel", "amazon_esci", "wayfair_wands"], default="all")
    parser.add_argument("--esci-max-rows", type=int, default=None, help="Optional small validation cap; omit for the full real dataset.")
    args = parser.parse_args()
    output = Path("data/ccb1/normalized")
    results: list[dict] = []
    if args.dataset in ("all", "wayfair_wands"):
        root = Path("data/ccb1/raw/wayfair_wands")
        results.append(normalize_wands(root / "query.csv", root / "product.csv", root / "label.csv", output / "wayfair_wands.jsonl"))
    if args.dataset in ("all", "google_convapparel"):
        results.append(normalize_convapparel(Path("data/ccb1/raw/google_convapparel/ConvApparel.zip"), output / "google_convapparel.jsonl"))
    if args.dataset in ("all", "amazon_esci"):
        root = Path("data/ccb1/raw/amazon_esci/esci-code/shopping_queries_dataset")
        results.append(normalize_esci(root / "shopping_queries_dataset_examples.parquet", root / "shopping_queries_dataset_products.parquet", output / "amazon_esci.jsonl", max_rows=args.esci_max_rows))
    manifest_path = Path("data/ccb1/normalized/normalization_manifest.json")
    existing = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    merged = {(item.get("dataset"), item.get("destination")): item for item in existing}
    merged.update({(item.get("dataset"), item.get("destination")): item for item in results})
    manifest = list(merged.values())
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
