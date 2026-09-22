from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path("data/ccb1/raw")
WANDS_URLS = {
    "query.csv": "https://raw.githubusercontent.com/wayfair/WANDS/main/dataset/query.csv",
    "product.csv": "https://raw.githubusercontent.com/wayfair/WANDS/main/dataset/product.csv",
    "label.csv": "https://raw.githubusercontent.com/wayfair/WANDS/main/dataset/label.csv",
}
CONV_URL = "https://huggingface.co/datasets/google/ConvApparel/resolve/main/ConvApparel.zip?download=true"
ESCI_REPO = "https://github.com/amazon-research/esci-code.git"
LICENSE_REFERENCES = {
    "google_convapparel": {"license": "CC BY 4.0", "reference": "https://huggingface.co/datasets/google/ConvApparel"},
    "amazon_esci": {"license": "Apache-2.0", "reference": "https://github.com/amazon-research/esci-code"},
    "wayfair_wands": {"license": "MIT", "reference": "https://github.com/wayfair/WANDS"},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        print(f"exists: {destination}")
        return
    print(f"download: {url} -> {destination}")
    urllib.request.urlretrieve(url, destination)


def fetch_wands(manifest: dict) -> None:
    base = ROOT / "wayfair_wands"
    for name, url in WANDS_URLS.items():
        target = base / name
        download(url, target)
        manifest["files"].append({"dataset": "wayfair_wands", "path": str(target), "url": url, "sha256": sha256(target)})


def fetch_convapparel(manifest: dict) -> None:
    target = ROOT / "google_convapparel" / "ConvApparel.zip"
    download(CONV_URL, target)
    manifest["files"].append({"dataset": "google_convapparel", "path": str(target), "url": CONV_URL, "sha256": sha256(target)})


def fetch_esci(manifest: dict) -> None:
    repo = ROOT / "amazon_esci" / "esci-code"
    if not repo.exists():
        repo.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", ESCI_REPO, str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "lfs", "pull", "--include", "shopping_queries_dataset/*"], check=True)
    revision = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    manifest["git_revisions"]["amazon_esci"] = {"repository": ESCI_REPO, "revision": revision}
    for name in ("shopping_queries_dataset_examples.parquet", "shopping_queries_dataset_products.parquet", "shopping_queries_dataset_sources.csv"):
        target = repo / "shopping_queries_dataset" / name
        manifest["files"].append({"dataset": "amazon_esci", "path": str(target), "repository": ESCI_REPO, "revision": revision, "sha256": sha256(target)})


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch official CCB-1 source artifacts into ignored raw storage.")
    parser.add_argument("--dataset", choices=["all", "google_convapparel", "amazon_esci", "wayfair_wands"], default="all")
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = Path("data/ccb1/source_manifest.json")
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {"created_at": datetime.now(timezone.utc).isoformat(), "files": [], "git_revisions": {}}
    manifest.setdefault("files", [])
    manifest.setdefault("git_revisions", {})
    manifest["license_references"] = LICENSE_REFERENCES
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    if args.dataset in ("all", "wayfair_wands"):
        fetch_wands(manifest)
    if args.dataset in ("all", "google_convapparel"):
        fetch_convapparel(manifest)
    if args.dataset in ("all", "amazon_esci"):
        fetch_esci(manifest)
    deduped: dict[tuple[str, str], dict] = {(item.get("dataset", ""), item.get("path", "")): item for item in manifest["files"]}
    manifest["files"] = list(deduped.values())
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote data/ccb1/source_manifest.json with {len(manifest['files'])} artifacts")


if __name__ == "__main__":
    main()
