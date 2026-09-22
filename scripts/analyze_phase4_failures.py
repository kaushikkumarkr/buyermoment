from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def main() -> None:
    source = Path("artifacts/adversarial_v2_benchmark.json")
    artifact = json.loads(source.read_text())
    failures = artifact.get("failure_cases", [])
    category_counts = Counter()
    root_causes = Counter()
    stage_errors = Counter()
    decision_errors = Counter()
    for failure in failures:
        category_counts[str(failure.get("category", "unknown"))] += 1
        root_causes[str(failure.get("reason_codes", ["unexplained"])[0] if failure.get("reason_codes") else "unexplained")] += 1
        if failure.get("expected_stage") != failure.get("predicted_stage"):
            stage_errors[f"{failure.get('expected_stage')} -> {failure.get('predicted_stage')}"] += 1
        if failure.get("expected_decision") != failure.get("predicted_decision"):
            decision_errors[f"{failure.get('expected_decision')} -> {failure.get('predicted_decision')}"] += 1
    summary = {
        "failure_count": len(failures),
        "by_category": dict(category_counts),
        "by_root_cause": dict(root_causes),
        "stage_confusions": dict(stage_errors),
        "decision_confusions": dict(decision_errors),
        "method": "Every row is retained with expected/predicted fields; category counts are diagnostic, not model-quality labels.",
    }
    Path("artifacts/phase4_failure_analysis.json").write_text(json.dumps(summary, indent=2) + "\n")
    lines = [
        "# Phase 4 failure analysis",
        "",
        f"The adversarial v2 run retained **{len(failures)}** rows with either a stage or SpendDecision mismatch.",
        "",
        "## Failure categories",
        "",
    ]
    lines.extend(f"- `{key}`: {value}" for key, value in category_counts.most_common())
    lines.extend(["", "## Root causes/reason codes", ""])
    lines.extend(f"- `{key}`: {value}" for key, value in root_causes.most_common())
    lines.extend(["", "## Stage confusions", ""])
    lines.extend(f"- `{key}`: {value}" for key, value in stage_errors.most_common())
    lines.extend(["", "## Spend-decision confusions", ""])
    lines.extend(f"- `{key}`: {value}" for key, value in decision_errors.most_common())
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The most important failure classes are retained rather than discarded: a `WATCH` output where a manually labeled `ABSTAIN` was expected is still an actionability error, while a clean hidden relevance score cannot answer that question. These controls are not external campaign outcomes.",
            "",
            "## Remediation status",
            "",
            "- Deterministic serviceability, availability, shipping, budget, support, research, and future-intent rules are versioned in `policies/spend_safety.yaml` and `backend/src/buyermoment/spend_safety.py`.",
            "- Remaining ambiguous-stage errors require human-reviewed labels and/or a semantic model; they are not silently converted into positive spend recommendations.",
            "- The full row-level evidence is in `artifacts/phase4_failure_cases.jsonl`.",
        ]
    )
    Path("reports/phase4_failure_analysis.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
