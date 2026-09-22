from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.commercial_workflow import build_opportunity_report, discover_package_moments, generate_ad_experiment
from buyermoment.dogfood import load_package


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the deterministic BuyerMoment-on-BuyerMoment dogfood workflow.")
    parser.add_argument("--input", default="businesses/buyermoment/business_evidence.json")
    parser.add_argument("--output", default="reports/buyermoment_dogfood.md")
    parser.add_argument("--artifact", default="artifacts/phase7_dogfood.json")
    args = parser.parse_args()
    package = load_package(Path(args.input))
    moments = discover_package_moments(package)
    report = build_opportunity_report(package, top_n=5)
    experiments = [generate_ad_experiment(moment, package.business.id, budget=None) for moment in moments[:5]]
    payload = {"report": report.model_dump(mode="json"), "experiments": [item.model_dump(mode="json") for item in experiments], "human_approval_required": True}
    artifact = Path(args.artifact)
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(payload, indent=2) + "\n")
    lines = ["# BuyerMoment dogfood report\n", f"Business: {package.business.name}", "", f"Evidence analyzed: {report.evidence_analyzed}", f"Raw Buyer Moments: {report.raw_candidate_count}", f"Supported candidates: {report.supported_candidate_count}", f"Top candidates: {len(report.top_buyer_moments)}", f"TEST candidates: {sum(item.spend_decision == 'TEST' for item in experiments)}", "", "## Top-ranked Buyer Moments\n"]
    for index, item in enumerate(report.top_buyer_moments, 1):
        lines.extend([f"### {index}. {item['title']}", f"- Buyer Moment ID: `{item['id']}`", f"- Situation: {item['situation']}", f"- Commerciality: {item['score']['commerciality']}", f"- Test readiness: {experiments[index - 1].test_readiness if index <= len(experiments) else 'not generated'}", f"- Proposed decision: {experiments[index - 1].spend_decision if index <= len(experiments) else 'not generated'}", "- Human approval required: true", "- Evidence: " + "; ".join(e["text"] for e in item["supporting_evidence"]), ""])
    lines.extend(["## Rejected or unsupported", "", "No candidate is treated as an observed customer fact when its evidence is inference-only.", "", "## Evidence gaps", "", *[f"- {item}" for item in report.evidence_gaps], "", "## Risks", "", *[f"- {item}" for item in report.risks], ""])
    Path(args.output).write_text("\n".join(lines))
    print(json.dumps({"raw_candidates": report.raw_candidate_count, "supported_candidates": report.supported_candidate_count, "top_candidates": len(report.top_buyer_moments), "experiments": len(experiments), "test_candidates": sum(item.spend_decision == "TEST" for item in experiments)}, indent=2))


if __name__ == "__main__":
    main()
