from __future__ import annotations

import argparse
import hashlib
import urllib.request
from pathlib import Path


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Download one dataset artifact and verify an expected checksum.")
    parser.add_argument("url")
    parser.add_argument("output", type=Path)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(args.url, args.output)
    actual = digest(args.output)
    if actual != args.sha256:
        raise SystemExit(f"checksum mismatch for {args.output}: expected {args.sha256}, got {actual}")
    print(f"verified {args.output} sha256={actual}")


if __name__ == "__main__":
    main()

