from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


def main() -> None:
    path = Path("shadow_reviews/private/model_predictions.jsonl")
    predictions = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    by_business: dict[str, list[dict]] = defaultdict(list)
    for row in predictions:
        by_business[row["buyer_moment"]["business_id"]].append(row)
    scorecards = []
    for business_id, rows in sorted(by_business.items()):
        scorecards.append({"business_id": business_id, "candidates_reviewed": len(rows), "model_decision_distribution": dict(Counter(row["spend_decision"]["decision"] for row in rows)), "human_decision": None, "exact_agreement": None, "test_precision_vs_human": None, "severe_disagreement_rate": None, "would_spend_agreement": None, "review_status": "pending_independent_human_submissions"})
    artifact = {"businesses": len(scorecards), "scorecards": scorecards, "status": "model-side scorecards prepared; human fields intentionally unavailable until blinded review"}
    Path("artifacts/phase6_business_scorecards.json").write_text(json.dumps(artifact, indent=2) + "\n")
    Path("reports/phase6_business_scorecards.md").write_text("# Phase 6 business scorecards\n\n" + json.dumps(artifact, indent=2) + "\n")
    print(json.dumps(artifact, indent=2))


if __name__ == "__main__":
    main()
