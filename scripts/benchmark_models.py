from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from augment_ccb1 import parse_variants, prompt_for, source_records  # noqa: E402
from buyermoment.providers import AzureOpenAIChatProvider  # noqa: E402


def token_set(text: str) -> set[str]:
    return {token for token in text.lower().replace("-", " ").split() if len(token) > 2}


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare configured Azure model roles on the same small CCB-1 sample.")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--output", type=Path, default=Path("artifacts/model_comparison_v0_1.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/model_comparison_v0_1.md"))
    args = parser.parse_args()
    endpoint = os.environ["BUYERMOMENT_AZURE_OPENAI_ENDPOINT"]
    token = subprocess.check_output(["az", "account", "get-access-token", "--scope", "https://cognitiveservices.azure.com/.default", "--query", "accessToken", "-o", "tsv"], text=True).strip()
    parents = source_records(Path("data/ccb1/normalized"), args.limit)
    deployments = {
        "gpt-5.4-nano/bulk_generator": "buyermoment-bulk-generator",
        "gpt-5.4-mini/extractor": "buyermoment-extractor",
    }
    results: dict[str, dict] = {}
    for label, deployment in deployments.items():
        provider = AzureOpenAIChatProvider(endpoint=endpoint, deployment=deployment, api_version="2025-04-01-preview", bearer_token=token)
        valid = 0
        overlaps: list[float] = []
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        latencies: list[float] = []
        errors: list[str] = []
        for parent in parents:
            started = time.perf_counter()
            try:
                variants = parse_variants(provider.generate(prompt_for(parent), role="bulk_generator"))
                latencies.append((time.perf_counter() - started) * 1000)
                if len(variants) == 5:
                    valid += 1
                source_tokens = token_set(parent.original_query or parent.context_text)
                generated_tokens = token_set(" ".join(variants.values()))
                overlaps.append(len(source_tokens & generated_tokens) / max(1, len(source_tokens)))
                for key in total_usage:
                    total_usage[key] += int(provider.last_usage.get(key, 0))
            except Exception as exc:
                errors.append(f"{parent.record_id}: {exc}")
        results[label] = {
            "deployment": deployment,
            "sample_parents": len(parents),
            "schema_valid_parent_calls": valid,
            "schema_validity": valid / len(parents) if parents else None,
            "semantic_preservation_token_overlap_proxy": sum(overlaps) / len(overlaps) if overlaps else None,
            "mean_latency_ms": sum(latencies) / len(latencies) if latencies else None,
            "tokens": total_usage,
            "estimated_cost_per_1000_contexts": None,
            "cost_status": "not computed; current official price sheet is not embedded in source",
            "errors": errors,
        }
    summary = {
        "benchmark": "CCB-1 v0.1 bounded multi-model comparison",
        "sample_parent_ids": [parent.record_id for parent in parents],
        "comparison": results,
        "limitations": ["Token-overlap is a guardrail proxy, not human semantic quality.", "No LLM judge was used; original ESCI/WANDS labels remain ground truth.", "Dollar cost is null until a dated official Azure price is configured."],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    lines = ["# CCB-1 v0.1 bounded model comparison", "", "The sample is a same-input guardrail comparison, not a human quality verdict.", "", "| configuration | schema validity | token-overlap proxy | mean latency ms | total tokens | dollar cost / 1,000 |", "|---|---:|---:|---:|---:|---:|"]
    for label, result in results.items():
        lines.append(f"| {label} | {result['schema_validity']} | {result['semantic_preservation_token_overlap_proxy']} | {result['mean_latency_ms']} | {result['tokens']['total_tokens']} | not computed |")
    lines.extend(["", "- Original ESCI/WANDS labels remain ground truth; no LLM judge was used.", "- Token overlap is only a semantic-preservation guardrail proxy.", "- Dollar cost is intentionally null until a dated official Azure price configuration is added.", ""])
    args.report_output.write_text("\n".join(lines))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
