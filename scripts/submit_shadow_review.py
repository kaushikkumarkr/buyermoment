from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Append one blinded shadow review without exposing the model prediction.")
    parser.add_argument("--packet-id", required=True)
    parser.add_argument("--decision", choices=("TEST", "WATCH", "ABSTAIN", "BLOCK"), required=True)
    parser.add_argument("--would-spend-real-money", choices=("yes", "maybe", "no"), required=True)
    parser.add_argument("--confidence", choices=("low", "medium", "high"), required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--category", default="unclassified")
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--output", type=Path, default=Path("shadow_reviews/private/reviewer_submissions.jsonl"))
    args = parser.parse_args()
    row = {"packet_id": args.packet_id, "decision": args.decision, "would_spend_real_money": args.would_spend_real_money, "confidence": args.confidence, "reason": args.reason, "category": args.category, "reviewer_id": args.reviewer_id}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a") as handle:
        handle.write(json.dumps(row) + "\n")
    print(json.dumps({"submitted": args.packet_id, "output": str(args.output), "model_prediction_read": False}, indent=2))


if __name__ == "__main__":
    main()
