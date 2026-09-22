from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    prior = json.loads(Path("artifacts/model_routing_report.json").read_text())
    safety = json.loads(Path("artifacts/phase5_spend_safety.json").read_text())
    report = {
        "benchmark": "Phase 5 TEST-safety routing comparison",
        "rules_first_nano_then_mini": {
            "test_precision": safety["adversarial_hidden"]["test_precision"],
            "waste_risk_rate": safety["adversarial_hidden"]["waste_risk_rate"],
            "coverage": safety["adversarial_hidden"]["eligible_coverage"],
            "mini_escalation_rate": 0.0,
            "note": "Phase 5 local deterministic policy path; no Azure call was needed for the measured safety gate.",
        },
        "bounded_azure_reference": {
            "all_mini_accuracy": prior["all_mini"]["accuracy"],
            "routed_accuracy": prior["routed_nano_to_mini"]["accuracy"],
            "mini_escalation_rate": prior["routed_nano_to_mini"]["escalation_rate"],
            "tokens": prior["usage"],
            "cost": prior["cost"],
        },
        "decision": "Use deterministic rules first; escalate only unresolved borderline cases in a future shadow run. Phase 5 did not create a deployment or submit model calls.",
        "status": "measured reference plus local Phase 5 policy benchmark; not a production cost claim",
    }
    Path("artifacts/phase5_model_routing.json").write_text(json.dumps(report, indent=2) + "\n")
    Path("reports/phase5_model_routing.md").write_text("# Phase 5 model routing\n\n" + json.dumps(report, indent=2) + "\n\nThe previous bounded Azure comparison is retained as a reference. The Phase 5 safety gate is deterministic and therefore has zero mini escalation in this benchmark; a future shadow pilot may route only borderline TEST/WATCH cases.\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
