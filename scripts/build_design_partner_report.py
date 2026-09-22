from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.commercial_workflow import build_opportunity_report, discover_package_moments, generate_ad_experiment
from buyermoment.dogfood import load_package


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a customer-facing, evidence-first opportunity report from an authorized package.")
    parser.add_argument("input", type=Path, help="Private/local BusinessEvidencePackage JSON")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = load_package(args.input)
    report = build_opportunity_report(package, top_n=5)
    experiments = [generate_ad_experiment(moment, package.business.id) for moment in discover_package_moments(package)[:5]]
    payload = {"report": report.model_dump(mode="json"), "experiment_summaries": [{"experiment_id": item.experiment_id, "buyer_moment_id": item.buyer_moment_id, "spend_decision": item.spend_decision, "human_approval_required": item.approval.required} for item in experiments], "private_input": True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"business_id": package.business.id, "candidates": report.raw_candidate_count, "top_candidates": len(report.top_buyer_moments), "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
