from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.commercial import DesignPartnerFeedback


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate structured design-partner feedback without turning it into ML ground truth.")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    values = json.loads(args.input.read_text())
    records = values if isinstance(values, list) else [values]
    feedback = [DesignPartnerFeedback.model_validate(item) for item in records]
    print(json.dumps({"valid": len(feedback), "formal_ml_ground_truth": False}, indent=2))


if __name__ == "__main__":
    main()
