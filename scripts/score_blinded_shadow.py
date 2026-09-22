from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


LABELS = ("TEST", "WATCH", "ABSTAIN", "BLOCK")


def kappa(actual: list[str], predicted: list[str]) -> float | None:
    if not actual:
        return None
    observed = sum(a == p for a, p in zip(actual, predicted, strict=True)) / len(actual)
    actual_counts = Counter(actual)
    predicted_counts = Counter(predicted)
    expected = sum(actual_counts[label] * predicted_counts[label] for label in LABELS) / (len(actual) * len(actual))
    return (observed - expected) / (1 - expected) if expected < 1 else 1.0


def main() -> None:
    private = Path("shadow_reviews/private")
    predictions_path = private / "model_predictions.jsonl"
    reviews_path = private / "reviewer_submissions.jsonl"
    predictions = {row["packet_id"]: row for row in (json.loads(line) for line in predictions_path.read_text().splitlines() if line.strip())} if predictions_path.exists() else {}
    reviews = [json.loads(line) for line in reviews_path.read_text().splitlines() if line.strip()] if reviews_path.exists() else []
    joined = []
    for review in reviews:
        prediction = predictions.get(review["packet_id"])
        if prediction:
            joined.append({"packet_id": review["packet_id"], "business_id": prediction["buyer_moment"]["business_id"], "model_decision": prediction["spend_decision"]["decision"], "human_decision": review["decision"], "human_confidence": review.get("confidence"), "would_spend_real_money": review.get("would_spend_real_money"), "reason": review.get("reason"), "category": review.get("category", "unclassified"), "agreement": prediction["spend_decision"]["decision"] == review["decision"]})
    actual = [row["human_decision"] for row in joined]
    predicted = [row["model_decision"] for row in joined]
    model_tests = [row for row in joined if row["model_decision"] == "TEST"]
    disagreements = [row for row in joined if not row["agreement"]]
    by_packet: dict[str, list[str]] = defaultdict(list)
    for review in reviews:
        by_packet[review["packet_id"]].append(review["decision"])
    human_pairs = [(labels[0], labels[1]) for labels in by_packet.values() if len(labels) >= 2]
    summary = {"review_status": "complete" if joined else "pending_independent_human_submissions", "candidates_reviewed": len(joined), "businesses_reviewed": len({row["business_id"] for row in joined}), "exact_decision_agreement": sum(row["agreement"] for row in joined) / len(joined) if joined else None, "cohen_kappa": kappa(actual, predicted), "test_precision_vs_blinded_human": sum(row["human_decision"] == "TEST" for row in model_tests) / len(model_tests) if model_tests else None, "test_watch_utility_agreement": sum((row["model_decision"] in {"TEST", "WATCH"}) == (row["human_decision"] in {"TEST", "WATCH"}) for row in joined) / len(joined) if joined else None, "severe_disagreement_rate": sum(row["model_decision"] == "TEST" and row["human_decision"] == "BLOCK" for row in joined) / len(joined) if joined else None, "would_spend_agreement_among_model_test": sum(row["would_spend_real_money"] == "yes" for row in model_tests) / len(model_tests) if model_tests else None, "human_human_kappa": kappa([pair[0] for pair in human_pairs], [pair[1] for pair in human_pairs]) if human_pairs else None, "human_human_pairs": len(human_pairs), "disagreement_categories": dict(Counter(row["category"] for row in disagreements)), "reviewer_confidence": dict(Counter(row["human_confidence"] for row in joined)), "scope": "independent human submissions only; proxy labels are excluded"}
    artifact = {"summary": summary, "joined": joined, "disagreements": disagreements}
    Path("artifacts/phase6_blinded_shadow.json").write_text(json.dumps(artifact, indent=2) + "\n")
    Path("artifacts/phase6_disagreements.jsonl").write_text("\n".join(json.dumps(row) for row in disagreements) + ("\n" if disagreements else ""))
    Path("reports/reviewer_agreement.md").write_text("# Reviewer agreement\n\n" + json.dumps(summary, indent=2) + "\n\nProxy/non-blinded Phase 5 labels are intentionally not mixed into this report. Metrics remain null until independent reviewer submissions are placed in `shadow_reviews/private/reviewer_submissions.jsonl`.\n")
    Path("reports/shadow_agreement_analysis.md").write_text("# Blinded shadow agreement analysis\n\n" + json.dumps(summary, indent=2) + "\n")
    Path("reports/phase6_disagreement_analysis.md").write_text("# Phase 6 disagreement analysis\n\n" + json.dumps({"summary": summary, "disagreements": disagreements}, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
