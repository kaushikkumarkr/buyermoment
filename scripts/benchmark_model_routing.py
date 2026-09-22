from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

from buyermoment.providers import AzureOpenAIChatProvider

def classify(provider: AzureOpenAIChatProvider, text: str) -> dict:
    prompt = (
        "Classify the current customer turn into exactly one purchase stage: "
        "informational, exploration, comparison, consideration, transactional. "
        "Use only the current turn; do not treat a product keyword as buying intent. "
        "Return JSON with stage and confidence between 0 and 1.\n\nTURN=" + text
    )
    raw = provider.generate(prompt, role="extractor")
    payload = json.loads(raw)
    return {"stage": str(payload["stage"]), "confidence": float(payload.get("confidence", 0.5))}

def ambiguous(text: str) -> bool:
    lowered = text.lower()
    cues = ("but", "not buying", "research", "already", "until next year", "moving", "for my", "compare", "vs", "which one")
    return sum(cue in lowered for cue in cues) >= 1 or text.count(" ") > 22

def main() -> None:
    parser = argparse.ArgumentParser(description="Bounded nano-to-mini routing comparison on reviewed stage cases.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--output", type=Path, default=Path("artifacts/model_routing_report.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/model_routing_report.md"))
    args = parser.parse_args()
    endpoint = os.environ["BUYERMOMENT_AZURE_OPENAI_ENDPOINT"]
    token = subprocess.check_output(["az", "account", "get-access-token", "--scope", "https://cognitiveservices.azure.com/.default", "--query", "accessToken", "-o", "tsv"], text=True).strip()
    rows = [json.loads(line) for line in Path("data/ccb1/adversarial/adversarial_v0_1.jsonl").read_text().splitlines() if line.strip()][:args.limit]
    providers = {"nano": AzureOpenAIChatProvider(endpoint=endpoint, deployment="buyermoment-bulk-generator", api_version="2025-04-01-preview", bearer_token=token), "mini": AzureOpenAIChatProvider(endpoint=endpoint, deployment="buyermoment-extractor", api_version="2025-04-01-preview", bearer_token=token)}
    results = {"all_mini": [], "routed": []}
    usage = {key: {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "calls": 0, "latency_ms": []} for key in ("nano", "mini")}
    def invoke(label: str, text: str) -> dict:
        started = time.perf_counter()
        try:
            answer = classify(providers[label], text)
            elapsed = (time.perf_counter() - started) * 1000
            usage[label]["latency_ms"].append(elapsed)
            usage[label]["calls"] += 1
            for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
                usage[label][key] += int(providers[label].last_usage.get(key, 0))
            return {"ok": True, **answer, "latency_ms": elapsed}
        except Exception as exc:
            return {"ok": False, "error": str(exc), "latency_ms": (time.perf_counter() - started) * 1000}
    for row in rows:
        expected = row["purchase_stage"]
        all_mini = invoke("mini", row["context_text"])
        results["all_mini"].append({"id": row["record_id"], "expected": expected, "prediction": all_mini})
        nano = invoke("nano", row["context_text"])
        escalate = ambiguous(row["context_text"]) or not nano.get("ok") or float(nano.get("confidence", 0.0)) < 0.72
        routed = invoke("mini", row["context_text"]) if escalate else nano
        results["routed"].append({"id": row["record_id"], "expected": expected, "nano": nano, "escalated": escalate, "prediction": routed})
    def quality(items: list[dict]) -> dict:
        valid = [item for item in items if item["prediction"].get("ok")]
        return {"count": len(items), "valid": len(valid), "accuracy": sum(item["prediction"].get("stage") == item["expected"] for item in valid) / len(valid) if valid else None, "errors": [item["prediction"].get("error") for item in items if not item["prediction"].get("ok")]}
    routed_count = sum(item["escalated"] for item in results["routed"])
    for key in usage.values():
        key["mean_latency_ms"] = sum(key["latency_ms"]) / len(key["latency_ms"]) if key["latency_ms"] else None
        del key["latency_ms"]
    summary = {"benchmark": "Phase 3 bounded model routing comparison", "sample": len(rows), "all_mini": quality(results["all_mini"]), "routed_nano_to_mini": {**quality(results["routed"]), "escalated": routed_count, "escalation_rate": routed_count / len(rows) if rows else None}, "usage": usage, "cost": "not posted; token usage retained and no dollar estimate fabricated", "models": {"nano": "buyermoment-bulk-generator / gpt-5.4-nano", "mini": "buyermoment-extractor / gpt-5.4-mini"}, "status": "bounded Azure-direct run on manually authored adversarial stage cases; not a production cost claim"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n")
    args.report_output.write_text("# Model routing report\n\n" + json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
