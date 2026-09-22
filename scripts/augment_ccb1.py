from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any

from buyermoment.models import CommercialContextRecord, Evidence
from buyermoment.providers import AzureOpenAIChatProvider


VARIANTS: tuple[dict[str, str], ...] = (
    {"name": "high_purchase_intent", "stage": "transactional", "commerciality": "high"},
    {"name": "comparison", "stage": "comparison", "commerciality": "medium"},
    {"name": "exploration", "stage": "exploration", "commerciality": "low"},
    {"name": "informational", "stage": "informational", "commerciality": "low"},
    {"name": "existing_owner_support", "stage": "informational", "commerciality": "none"},
)


def source_records(input_dir: Path, limit: int, offset: int = 0) -> list[CommercialContextRecord]:
    by_source: dict[str, list[CommercialContextRecord]] = {}
    for path in sorted(input_dir.glob("*.jsonl")):
        with path.open() as stream:
            by_source[path.stem] = [CommercialContextRecord.model_validate_json(line) for line in stream if line.strip()]
    result: list[CommercialContextRecord] = []
    index = 0
    sources = sorted(by_source)
    target = limit + offset
    while len(result) < target and sources:
        source = sources[index % len(sources)]
        if by_source[source]:
            result.append(by_source[source].pop(0))
        sources = [name for name in sources if by_source[name]]
        index += 1
    return result[offset:]


def selected_records(input_dir: Path, record_ids: list[str]) -> list[CommercialContextRecord]:
    wanted = set(record_ids)
    found: dict[str, CommercialContextRecord] = {}
    for path in sorted(input_dir.glob("*.jsonl")):
        with path.open() as stream:
            for line in stream:
                if line.strip():
                    record = CommercialContextRecord.model_validate_json(line)
                    if record.record_id in wanted:
                        found[record.record_id] = record
    return [found[record_id] for record_id in record_ids if record_id in found]


def template_variants(record: CommercialContextRecord) -> dict[str, str]:
    base = record.original_query or record.context_text
    product = record.product_title or "this product"
    return {
        "high_purchase_intent": f"I need {base} soon and want to choose a suitable option like {product}.",
        "comparison": f"Which option is better for {base}: {product} or a comparable alternative?",
        "exploration": f"What should I look for when exploring options for {base}?",
        "informational": f"What are the main considerations and background behind {base}?",
        "existing_owner_support": f"How do I use, maintain, or troubleshoot the {product} I already own?",
    }


def prompt_for(record: CommercialContextRecord) -> str:
    source = {
        "original_query": record.original_query,
        "context_text": record.context_text,
        "product_title": record.product_title,
        "product_description": record.product_description,
        "product_attributes": record.product_attributes,
    }
    requested = [item["name"] for item in VARIANTS]
    return (
        "Transform this real shopping example into five conversational contexts. "
        "Preserve the product/category semantics and any explicit constraints. "
        "Do not invent prices, features, availability, locations, or product claims. "
        "The variant types are fixed by the caller; do not add or remove types. "
        f"Return JSON {{\"variants\": [{{\"variant_type\": ..., \"context_text\": ...}}]}} for exactly {requested}.\n\n"
        f"SOURCE={json.dumps(source, ensure_ascii=False)}"
    )


def parse_variants(text: str) -> dict[str, str]:
    payload = json.loads(text)
    variants = payload.get("variants", [])
    result = {str(item.get("variant_type")): " ".join(str(item.get("context_text", "")).split()) for item in variants}
    return {item["name"]: result[item["name"]] for item in VARIANTS if item["name"] in result and result[item["name"]]}


def build_record(parent: CommercialContextRecord, spec: dict[str, str], text: str, provider_name: str) -> CommercialContextRecord:
    record_id = f"aug:{parent.record_id}:{spec['name']}"
    return CommercialContextRecord(
        record_id=record_id,
        source_dataset=parent.source_dataset,
        source_record_id=record_id,
        source_license=parent.source_license,
        source_version=parent.source_version,
        context_text=text,
        original_query=parent.original_query,
        product_id=parent.product_id,
        product_title=parent.product_title,
        product_description=parent.product_description,
        product_attributes=parent.product_attributes,
        constraints=parent.constraints,
        purchase_stage=spec["stage"],
        commerciality=spec["commerciality"],
        location=parent.location,
        evidence=[*parent.evidence, Evidence(id=f"{record_id}:transformation", kind="inference", text=text, source=provider_name, source_record_id=parent.source_record_id, provenance=[parent.record_id], confidence=0.5)],
        provenance=[*parent.provenance, f"controlled conversational transformation from {parent.record_id}"],
        transformation_history=[*parent.transformation_history, f"generated {spec['name']} variant with {provider_name}", "labels are controlled variant targets, not source ground truth"],
        confidence=0.5,
        split="unassigned",
        metadata={
            "parent_record_id": parent.record_id,
            "augmentation_variant": spec["name"],
            "label_origin": "controlled_variant_target",
            "provider": provider_name,
            "source_original_label": parent.metadata.get("original_label") or parent.metadata.get("original_esci_label"),
        },
    )


def azure_provider() -> AzureOpenAIChatProvider:
    if not os.environ.get("AZURE_OPENAI_BEARER_TOKEN") and not os.environ.get("AZURE_OPENAI_API_KEY"):
        token = subprocess.check_output(["az", "account", "get-access-token", "--resource", "https://cognitiveservices.azure.com", "--query", "accessToken", "-o", "tsv"], text=True).strip()
        os.environ["AZURE_OPENAI_BEARER_TOKEN"] = token
    return AzureOpenAIChatProvider.from_environment(role="bulk_generator")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate controlled conversational CCB-1 variants from real records.")
    parser.add_argument("--input", type=Path, default=Path("data/ccb1/normalized"))
    parser.add_argument("--limit", type=int, default=100, help="Number of real parent records, not generated rows")
    parser.add_argument("--offset", type=int, default=0, help="Skip this many round-robin parents; useful for bounded retries")
    parser.add_argument("--parent-id", action="append", default=None, help="Retry an explicit parent record; repeat for multiple IDs")
    parser.add_argument("--provider", choices=("azure", "template"), default="azure")
    parser.add_argument("--workers", type=int, default=5, help="Concurrent requests for Azure; bounded to protect quota")
    parser.add_argument("--delay-seconds", type=float, default=0.0, help="Delay between sequential parent requests")
    parser.add_argument("--output", type=Path, default=Path("data/ccb1/augmented/stage_a.jsonl"))
    parser.add_argument("--run-metadata", type=Path, default=Path("data/ccb1/augmented/stage_a_run.json"))
    args = parser.parse_args()
    parents = selected_records(args.input, args.parent_id) if args.parent_id else source_records(args.input, args.limit, args.offset)
    provider = azure_provider() if args.provider == "azure" else None
    generated: list[CommercialContextRecord] = []
    rejected: list[dict[str, Any]] = []
    started = time.perf_counter()
    def process(parent: CommercialContextRecord) -> tuple[list[CommercialContextRecord], dict[str, Any] | None]:
        try:
            variants = template_variants(parent) if provider is None else parse_variants(provider.generate(prompt_for(parent), role="bulk_generator"))
            missing = [item["name"] for item in VARIANTS if item["name"] not in variants]
            if missing:
                raise ValueError(f"missing variants: {missing}")
            rows = [build_record(parent, spec, variants[spec["name"]], args.provider) for spec in VARIANTS]
            if args.delay_seconds and provider is not None:
                time.sleep(args.delay_seconds)
            return rows, None
        except Exception as exc:  # keep failed rows in a review queue; never silently drop them
            if args.delay_seconds and provider is not None:
                time.sleep(args.delay_seconds)
            return [], {"parent_record_id": parent.record_id, "error": str(exc)}
    if provider is not None and args.workers > 1:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            results = list(executor.map(process, parents))
    else:
        results = [process(parent) for parent in parents]
    for rows, error in results:
        generated.extend(rows)
        if error:
            rejected.append(error)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(record.model_dump_json() for record in generated) + ("\n" if generated else ""))
    metadata = {
        "stage": "A",
        "provider": args.provider,
        "role": "bulk_generator",
        "parent_records": len(parents),
        "generated_records": len(generated),
        "rejected_parent_records": len(rejected),
        "rejected": rejected,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "output_sha256": __import__("hashlib").sha256(args.output.read_bytes()).hexdigest(),
        "quality_gate": "review_required",
    }
    args.run_metadata.parent.mkdir(parents=True, exist_ok=True)
    args.run_metadata.write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
