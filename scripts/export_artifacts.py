from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Export portable BuyerMoment datasets and benchmark artifacts.")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    args.destination.mkdir(parents=True, exist_ok=True)
    for source in [Path("data/gold"), Path("data/normalized"), Path("artifacts")]:
        if source.exists():
            target = args.destination / source
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target, dirs_exist_ok=True)
            else:
                shutil.copy2(source, target)
    print(f"exported portable artifacts to {args.destination}")


if __name__ == "__main__":
    main()

