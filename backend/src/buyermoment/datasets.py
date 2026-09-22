from __future__ import annotations

import csv
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

from .models import CommercialContextRecord, Evidence


LICENSES = {
    "google_convapparel": "CC BY 4.0; Google ConvApparel dataset card and attribution must be preserved.",
    "google_convapparel_v2": "CC BY 4.0; Google ConvApparel V2 dataset card and attribution must be preserved.",
    "amazon_esci": "Apache-2.0; preserve LICENSE/NOTICE and original Exact/Substitute/Complement/Irrelevant labels.",
    "wayfair_wands": "MIT; preserve the upstream license and original product-relevance labels.",
}

SOURCE_VERSIONS = {
    "google_convapparel": "Hugging Face main release; version captured in source_manifest.json",
    "google_convapparel_v2": "Hugging Face ConvApparel_V2.zip; version captured in source_manifest.json",
    "amazon_esci": "amazon-research/esci-code main release; version captured in source_manifest.json",
    "wayfair_wands": "wayfair/WANDS main release; version captured in source_manifest.json",
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


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _write_records(records: list[CommercialContextRecord], destination: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(record.model_dump_json() for record in records) + ("\n" if records else ""))
    return {"records": len(records), "destination": str(destination), "sha256": sha256(destination)}


def normalize_wands(query_path: Path, product_path: Path, label_path: Path, destination: Path) -> dict[str, Any]:
    # WANDS names the files .csv but the official release is tab-delimited.
    products = {row["product_id"]: row for row in csv.DictReader(product_path.open(newline=""), delimiter="\t")}
    queries = {row["query_id"]: row for row in csv.DictReader(query_path.open(newline=""), delimiter="\t")}
    records: list[CommercialContextRecord] = []
    relevance = {"Exact": ("exact", 1.0), "Partial": ("unknown", 0.5), "Irrelevant": ("irrelevant", 0.0)}
    for row in csv.DictReader(label_path.open(newline=""), delimiter="\t"):
        query = queries.get(row["query_id"], {})
        product = products.get(row["product_id"], {})
        label = row.get("label", "")
        mapped, fit = relevance.get(label, ("unknown", None))
        feature_text = _text(product.get("product_features"))
        label_record_id = row.get("id") or f"{row['query_id']}:{row['product_id']}"
        records.append(CommercialContextRecord(
            record_id=f"wands:{label_record_id}", source_dataset="wayfair_wands", source_record_id=label_record_id, source_license=LICENSES["wayfair_wands"], source_version=SOURCE_VERSIONS["wayfair_wands"], context_text=query.get("query", ""), original_query=query.get("query"), product_id=row.get("product_id"), product_title=_text(product.get("product_name")), product_description=_text(product.get("product_description")), product_attributes={"product_class": product.get("product_class"), "category_hierarchy": product.get("category hierarchy"), "product_features": feature_text, "query_class": query.get("query_class")}, relevance=mapped, product_fit=fit, evidence=[Evidence(id=f"wands-query:{row['query_id']}", kind="observed", text=query.get("query", ""), source="wayfair_wands.query.csv", source_record_id=row["query_id"]), Evidence(id=f"wands-product:{row['product_id']}", kind="observed", text=_text(product.get("product_name")) or row["product_id"], source="wayfair_wands.product.csv", source_record_id=row["product_id"])], provenance=["wayfair/WANDS query.csv + product.csv + label.csv"], transformation_history=["joined query_id and product_id", "preserved original WANDS label", "mapped Exact/Partial/Irrelevant to canonical relevance; Partial remains unknown"], metadata={"original_label": label, "query_class": query.get("query_class"), "query_id": row["query_id"], "product_id": row["product_id"]}, split="unassigned"))
    return _write_records(records, destination) | {"dataset": "wayfair_wands"}


def normalize_esci(examples_path: Path, products_path: Path, destination: Path, *, max_rows: int | None = None) -> dict[str, Any]:
    import pandas as pd

    examples = pd.read_parquet(examples_path)
    products = pd.read_parquet(products_path)
    merged = examples.merge(products, how="left", on=["product_locale", "product_id"], suffixes=("", "_product"))
    if max_rows:
        merged = merged.head(max_rows)
    labels = {"E": ("exact", 1.0), "S": ("substitute", 0.75), "C": ("complement", 0.5), "I": ("irrelevant", 0.0)}
    records: list[CommercialContextRecord] = []
    for row in merged.to_dict(orient="records"):
        label = row.get("esci_label")
        mapped, fit = labels.get(label, ("unknown", None))
        product_id = str(row.get("product_id"))
        example_id = str(row.get("example_id"))
        query = _text(row.get("query")) or ""
        records.append(CommercialContextRecord(
            record_id=f"esci:{example_id}", source_dataset="amazon_esci", source_record_id=example_id, source_license=LICENSES["amazon_esci"], source_version=SOURCE_VERSIONS["amazon_esci"], context_text=query, original_query=query, product_id=product_id, product_title=_text(row.get("product_title")), product_description=_text(row.get("product_description")), product_attributes={key: row.get(key) for key in ("product_bullet_point", "product_brand", "product_color", "product_locale", "query_id", "product_id") if key in row and row.get(key) is not None}, relevance=mapped, product_fit=fit, evidence=[Evidence(id=f"esci-query:{row.get('query_id')}", kind="observed", text=query, source="amazon_esci.examples.parquet", source_record_id=str(row.get("query_id"))), Evidence(id=f"esci-product:{product_id}", kind="observed", text=_text(row.get("product_title")) or product_id, source="amazon_esci.products.parquet", source_record_id=product_id)], provenance=["amazon-science/esci-code shopping_queries_dataset examples + products"], transformation_history=["joined product_locale and product_id", "preserved original ESCI label", "mapped E/S/C/I to canonical relevance and product_fit"], metadata={"original_esci_label": label, "small_version": row.get("small_version"), "large_version": row.get("large_version"), "split": row.get("split"), "product_locale": row.get("product_locale")}, split="unassigned"))
    return _write_records(records, destination) | {"dataset": "amazon_esci", "source_rows": int(len(merged))}


def normalize_convapparel(zip_path: Path, destination: Path, *, max_records: int | None = None, dataset: str = "google_convapparel") -> dict[str, Any]:
    with zipfile.ZipFile(zip_path) as archive:
        json_names = [name for name in archive.namelist() if name.lower().endswith(".json") and not name.endswith("/")]
        if not json_names:
            raise ValueError(f"No JSON payload found in {zip_path}")
        payload = json.loads(archive.read(json_names[0]))
    conversations = payload.get("conversations", [])
    records: list[CommercialContextRecord] = []
    for conversation_index, conversation in enumerate(conversations):
        turns = conversation.get("turns", [])
        for turn_index, turn in enumerate(turns):
            context_text = _text(turn.get("user_utterance"))
            if not context_text:
                continue
            for recommendation in turn.get("recommendations", []) or [None]:
                item_id = _text((recommendation or {}).get("item_id"))
                record_id = f"{dataset}:{conversation.get('task_id', 'unknown')}:{conversation_index}:{turn_index}:{item_id or 'no-item'}"
                records.append(CommercialContextRecord(
                    record_id=record_id, source_dataset=dataset, source_record_id=record_id, source_license=LICENSES[dataset], source_version=SOURCE_VERSIONS[dataset], context_text=context_text, original_query=context_text, product_id=item_id, product_title=_text((recommendation or {}).get("title")), product_description=_text((recommendation or {}).get("description")), product_attributes={"features": (recommendation or {}).get("features"), "image_url": (recommendation or {}).get("image_url")}, evidence=[Evidence(id=f"{record_id}:utterance", kind="observed", text=context_text, source=f"{dataset}.conversation", source_record_id=record_id)], provenance=[f"google/ConvApparel {dataset} conversation turn and recommendation"], transformation_history=["one record per user turn and recommended item", "preserved turn/session ratings in metadata", "no product relevance label inferred"], metadata={"task_id": conversation.get("task_id"), "version": conversation.get("version"), "dataset_variant": dataset, "turn_ratings": turn.get("ratings"), "session_ratings": conversation.get("ratings")}, split="unassigned"))
                if max_records and len(records) >= max_records:
                    return _write_records(records[:max_records], destination) | {"dataset": dataset}
    return _write_records(records, destination) | {"dataset": dataset}
