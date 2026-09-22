from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.adapters import ChatGPTAdsAdapter
from buyermoment.commercial_workflow import discover_package_moments, generate_ad_experiment
from buyermoment.dogfood import load_package


def main() -> None:
    parser = argparse.ArgumentParser(description="Export a human-reviewable ChatGPT Ads experiment package.")
    parser.add_argument("--business", default="businesses/buyermoment/business_evidence.json")
    parser.add_argument("--output", default="artifacts/phase7_chatgpt_ads")
    args = parser.parse_args()
    package = load_package(Path(args.business))
    moment = discover_package_moments(package)[0]
    experiment = generate_ad_experiment(moment, package.business.id, budget=None)
    paths = ChatGPTAdsAdapter().export(experiment, Path(args.output))
    print(json.dumps({"experiment_id": experiment.experiment_id, "paths": paths, "human_approval_required": True}, indent=2))


if __name__ == "__main__":
    main()
