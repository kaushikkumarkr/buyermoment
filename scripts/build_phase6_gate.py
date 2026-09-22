from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    shadow = json.loads(Path("artifacts/phase6_blinded_shadow.json").read_text())
    state = json.loads(Path("artifacts/phase6_state_benchmark.json").read_text())["summary"]
    counterfactual = json.loads(Path("artifacts/phase6_counterfactual.json").read_text())["summary"]
    summary = {"decision": "NO-GO", "live_spend": "NO-GO", "shadow_status": shadow["summary"]["review_status"], "human_review_candidates": shadow["summary"]["candidates_reviewed"], "stateful_stage_accuracy": state["stateful_stage_accuracy"], "stale_context_error_rate": state["stale_context_error_rate"], "counterfactual_consistency": counterfactual["direction_correctness"], "rationale": ["No independent blinded human submissions have been completed; exact agreement and TEST precision are therefore unavailable.", "The state representation achieves explicit-memory accuracy 1.0 and zero stale assertion errors on the authored controls, but stage accuracy remains 0.625 and does not improve over the baseline on this set.", "Counterfactual direction correctness is 0.6, with shipping, conditional, negative, and product variants failing.", "No live advertising has been launched; human approval remains mandatory."], "next_prerequisites": ["complete independent blinded holdout review", "analyze disagreements and reviewer confidence", "improve stage and failing counterfactual categories"]}
    Path("artifacts/phase6_pilot_gate.json").write_text(json.dumps(summary, indent=2) + "\n")
    Path("reports/phase6_pilot_gate.md").write_text("# Phase 6 pilot gate\n\n## Decision: `NO-GO`\n\n" + json.dumps(summary, indent=2) + "\n\nThis is an evidence gate, not a product or campaign result. The reviewer packet system is ready, but no independent human labels have been submitted, so Phase 6 cannot promote the pilot beyond shadow preparation.\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
