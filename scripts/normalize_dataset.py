from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.datasets import normalize_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize a downloaded commercial dataset while preserving source labels.")
    parser.add_argument("dataset", choices=["google_convapparel", "amazon_esci", "wayfair_wands"])
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(json.dumps(normalize_file(args.dataset, args.source, args.destination), indent=2))


if __name__ == "__main__":
    main()

