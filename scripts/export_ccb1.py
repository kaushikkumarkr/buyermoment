from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Export portable CCB-1 data, metadata, reports, and model configs.")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    args.destination.mkdir(parents=True, exist_ok=True)
    sources = [Path("data/ccb1"), Path("reports"), Path("artifacts"), Path("configs"), Path("ccb1_manifest.json"), Path("CCB1_CARD.md"), Path("AZURE_SPEND.md")]
    copied: list[Path] = []
    for source in sources:
        if not source.exists():
            continue
        target = args.destination / source
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=True)
            copied.extend(path for path in target.rglob("*") if path.is_file())
        else:
            shutil.copy2(source, target)
            copied.append(target)
    checksums = {str(path.relative_to(args.destination)): sha256(path) for path in copied if path.is_file()}
    (args.destination / "export_checksums.json").write_text(json.dumps(checksums, indent=2) + "\n")
    print(json.dumps({"destination": str(args.destination), "files": len(checksums)}, indent=2))


if __name__ == "__main__":
    main()
