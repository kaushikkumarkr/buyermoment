from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


LICENSES = {
    "google_convapparel": "License must be read from the downloaded upstream dataset card and attribution file; preserve it verbatim because public cards may change.",
    "amazon_esci": "Apache-2.0; preserve LICENSE/NOTICE and original Exact/Substitute/Complement/Irrelevant labels.",
    "wayfair_wands": "MIT; preserve the upstream license and original product-relevance labels.",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_record(dataset: str, record: dict[str, Any], *, source_record_id: str, split: str = "train") -> dict[str, Any]:
    """Normalize one source record without replacing its source label."""
    label = record.get("label") or record.get("relevance") or record.get("judgment")
    text = record.get("query") or record.get("context") or record.get("conversation") or ""
    product_text = record.get("product_title") or record.get("product") or record.get("item") or ""
    return {
        "source_dataset": dataset,
        "source_record_id": source_record_id,
        "source_license": LICENSES.get(dataset, "See source-specific attribution file."),
        "original_label": label,
        "transformation_history": ["field names normalized into shared schema; original payload retained separately"],
        "context_text": text,
        "product_text": product_text,
        "split": split,
        "source_fields": record,
    }


def normalize_file(dataset: str, source: Path, destination: Path, *, fmt: str = "jsonl") -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    if source.suffix.lower() == ".csv":
        with source.open(newline="") as stream:
            records = list(csv.DictReader(stream))
    else:
        payload = json.loads(source.read_text())
        records = payload if isinstance(payload, list) else payload.get("data", payload.get("records", []))
    normalized = [normalize_record(dataset, record, source_record_id=str(index + 1)) for index, record in enumerate(records)]
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(json.dumps(record, ensure_ascii=False) for record in normalized) + ("\n" if normalized else ""))
    return {"dataset": dataset, "records": len(normalized), "source": str(source), "sha256": sha256(source), "destination": str(destination)}
