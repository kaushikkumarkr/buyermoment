from __future__ import annotations

import json
from pathlib import Path

from buyermoment.models import LocationContext, Product
from buyermoment.readiness import score_test_readiness
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import load_policy, spend_safety


def run(path: Path) -> dict:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    results = []
    policy = load_policy()
    for row in rows:
        product = Product.model_validate(row["product"])
        context = build_context(row["context_text"], source="phase5_control", context_id=row["record_id"]).model_copy(update={"location": LocationContext(country=product.service_regions[0])})
        contextfit = score(context, product)
        readiness = score_test_readiness(context, product, contextfit)
        decision = spend_safety(context, product, contextfit, policy)
        results.append({"label": row["label"], "split": row["split"], "context": row["context_text"], "decision": decision.decision, "test_readiness": readiness.test_readiness, "ambiguity_score": readiness.ambiguity_score, "reason_codes": decision.reason_codes})
    hidden = [row for row in results if row["split"] == "hidden_test"]
    def metric(label: str, decision: str) -> float | None:
        predicted = [row for row in hidden if row["decision"] == decision]
        actual = [row for row in hidden if row["label"] == label]
        return sum(row["label"] == label for row in predicted) / len(predicted) if predicted else None, sum(row["decision"] == decision for row in actual) / len(actual) if actual else None
    return {"count": len(results), "hidden_count": len(hidden), "test_precision_recall": metric("TEST", "TEST"), "watch_precision_recall": metric("WATCH", "WATCH"), "false_test_count": sum(row["decision"] == "TEST" and row["label"] != "TEST" for row in hidden), "decision_distribution": {decision: sum(row["decision"] == decision for row in hidden) for decision in ("TEST", "WATCH", "ABSTAIN", "BLOCK")}, "results": results}


def main() -> None:
    third_party = run(Path("data/ccb1/phase5/third_party_intent.jsonl"))
    future = run(Path("data/ccb1/phase5/future_intent.jsonl"))
    artifact = {"third_party": third_party, "future_intent": future, "status": "manually authored controls; third-party purchase is distinct from third-party research; no campaign outcome claim"}
    Path("artifacts/phase5_intent_benchmarks.json").write_text(json.dumps(artifact, indent=2) + "\n")
    Path("reports/third_party_intent.md").write_text("# Third-party intent benchmark\n\n" + json.dumps({key: value for key, value in third_party.items() if key != "results"}, indent=2) + "\n")
    Path("reports/future_intent.md").write_text("# Future-intent benchmark\n\n" + json.dumps({key: value for key, value in future.items() if key != "results"}, indent=2) + "\n")
    print(json.dumps({"third_party": {key: value for key, value in third_party.items() if key != "results"}, "future_intent": {key: value for key, value in future.items() if key != "results"}}, indent=2))


if __name__ == "__main__":
    main()
