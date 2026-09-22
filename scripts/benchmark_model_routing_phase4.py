from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from buyermoment.models import CommercialContextRecord
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import spend_safety
from evaluate_spend_safety import product_for


def main() -> None:
    rows = [CommercialContextRecord.model_validate_json(line) for line in Path("data/ccb1/adversarial/adversarial_v2.jsonl").read_text().splitlines() if line.strip()]
    decisions = []
    for row in rows:
        context = build_context(row.context_text, source=row.source_dataset, context_id=row.record_id).model_copy(update={"location": row.location})
        product = product_for(row)
        decisions.append(spend_safety(context, product, score(context, product)).decision)
    policy_first_escalations = sum(decision in {"WATCH", "ABSTAIN"} for decision in decisions)
    prior = json.loads(Path("artifacts/model_routing_report.json").read_text())
    spend = json.loads(Path("artifacts/spend_safety_benchmark.json").read_text())
    summary = {
        "benchmark": "Phase 4 model-routing safety comparison",
        "phase4_sample": len(rows),
        "strategies": {
            "A_nano_only": {"quality": "not rerun in Phase 4; see prior Azure-direct bounded result", "model": "buyermoment-bulk-generator / gpt-5.4-nano"},
            "B_mini_only": {"quality": "not rerun in Phase 4; see prior Azure-direct bounded result", "model": "buyermoment-extractor / gpt-5.4-mini"},
            "C_nano_then_mini": {"quality": "not rerun in Phase 4; prior bounded result retained below", "model": "existing Azure-direct deployments"},
            "D_rules_then_model_on_ambiguity": {
                "policy_decision_distribution": dict(Counter(decisions)),
                "model_escalation_proxy_rate": policy_first_escalations / len(decisions) if decisions else None,
                "quality_metrics": {
                    "validation_test_precision": spend["validation"]["test_precision"],
                    "validation_waste_risk_rate": spend["validation"]["waste_risk_rate"],
                    "validation_abstain_rate": spend["validation"]["abstain_rate"],
                    "hidden_test_precision": spend["adversarial_hidden"]["test_precision"],
                    "hidden_waste_risk_rate": spend["adversarial_hidden"]["waste_risk_rate"],
                    "hidden_abstain_rate": spend["adversarial_hidden"]["abstain_rate"],
                },
                "latency": "local deterministic scorer; Azure model latency not measured in Phase 4",
                "token_usage": 0,
                "quality": "model calls intentionally not added: Phase 4 policy failures are measurable locally and the prior mini run hit a 429; no new Azure spend was justified before human-reviewed labels.",
            },
        },
        "prior_bounded_azure_evidence": prior,
        "cost": "posted dollar cost unavailable; no Phase 4 Azure model call or new deployment was made",
        "recommendation": "Keep deterministic rules first; route only ambiguous WATCH/ABSTAIN cases after a reviewed gold tranche exists.",
        "status": "measured safety routing proxy; not a claim of Phase 4 model-quality improvement",
    }
    Path("artifacts/model_routing_phase4.json").write_text(json.dumps(summary, indent=2) + "\n")
    Path("reports/model_routing_phase4.md").write_text(
        "# Phase 4 model routing\n\n"
        + json.dumps(summary, indent=2)
        + "\n\nPhase 4 did not create a model deployment or invoke a new Azure workload. The prior bounded Azure-direct comparison is included for traceability; deterministic safety routing is evaluated on the new adversarial set.\n"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
