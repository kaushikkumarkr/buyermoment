from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from buyermoment.models import CommercialContextRecord
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import load_policy, spend_safety
from evaluate_spend_safety import product_for

def f1(actual: list[str], predicted: list[str], label: str) -> float | None:
    tp = sum(a == p == label for a, p in zip(actual, predicted, strict=True))
    fp = sum(a != label and p == label for a, p in zip(actual, predicted, strict=True))
    fn = sum(a == label and p != label for a, p in zip(actual, predicted, strict=True))
    return 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None

def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Phase 4 adversarial stage and spend-safety robustness.")
    parser.add_argument("--input", type=Path, default=Path("data/ccb1/adversarial/adversarial_v2.jsonl"))
    parser.add_argument("--json-output", type=Path, default=Path("artifacts/adversarial_v2_benchmark.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/adversarial_v2_benchmark.md"))
    args = parser.parse_args()
    write_supporting_phase4_artifacts = args.json_output == Path("artifacts/adversarial_v2_benchmark.json")
    rows = [CommercialContextRecord.model_validate_json(line) for line in args.input.read_text().splitlines() if line.strip()]
    policy = load_policy()
    actual, predicted = [], []
    action_actual, action_predicted = [], []
    by_type: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"stage_actual": [], "stage_predicted": [], "action_actual": [], "action_predicted": []})
    failures = []
    for row in rows:
        product = product_for(row)
        context = build_context(row.context_text, source=row.source_dataset, context_id=row.record_id).model_copy(update={"location": row.location})
        result = score(context, product)
        decision = spend_safety(context, product, result, policy)
        actual.append(row.purchase_stage or "unknown")
        predicted.append(result.purchase_stage)
        action_actual.append(str(row.metadata["gold_spend_decision"]))
        action_predicted.append(decision.decision)
        bucket = by_type[str(row.metadata["adversarial_type"])]
        bucket["stage_actual"].append(row.purchase_stage or "unknown")
        bucket["stage_predicted"].append(result.purchase_stage)
        bucket["action_actual"].append(str(row.metadata["gold_spend_decision"]))
        bucket["action_predicted"].append(decision.decision)
        if row.purchase_stage != result.purchase_stage or str(row.metadata["gold_spend_decision"]) != decision.decision:
            failures.append({"record_id": row.record_id, "category": row.metadata["adversarial_type"], "expected_stage": row.purchase_stage, "predicted_stage": result.purchase_stage, "expected_decision": row.metadata["gold_spend_decision"], "predicted_decision": decision.decision, "reason_codes": decision.reason_codes})
    action_non_test = sum(actual != "TEST" for actual in action_actual)
    test_predictions = sum(predicted == "TEST" for predicted in action_predicted)
    commercial_actual = ["TEST" if row.metadata.get("gold_should_spend") else "NON_TEST" for row in rows]
    commercial_predicted = ["TEST" if prediction == "TEST" else "NON_TEST" for prediction in action_predicted]
    splits_by_category: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        splits_by_category[str(row.metadata["adversarial_type"])].add(row.split)
    duplicate_contexts = len(rows) - len({row.context_text for row in rows})
    summary = {"benchmark": "Phase 4 adversarial v2", "record_count": len(rows), "validation_count": sum(row.split == "validation" for row in rows), "hidden_count": sum(row.split == "hidden_test" for row in rows), "template_types": len(set(str(row.metadata["adversarial_type"]) for row in rows)), "integrity": {"duplicate_context_count": duplicate_contexts, "source_category_split_violations": sum(len(splits) > 1 for splits in splits_by_category.values())}, "purchase_stage": {"accuracy": sum(a == p for a, p in zip(actual, predicted, strict=True)) / len(actual), "macro_f1": sum(f1(actual, predicted, label) or 0 for label in sorted(set(actual))) / len(set(actual))}, "spend_safety": {"decision_accuracy": sum(a == p for a, p in zip(action_actual, action_predicted, strict=True)) / len(action_actual), "commercial_intent_f1": f1(commercial_actual, commercial_predicted, "TEST"), "test_precision": sum(a == "TEST" for a, p in zip(action_actual, action_predicted, strict=True) if p == "TEST") / test_predictions if test_predictions else None, "test_recall": sum(p == "TEST" for a, p in zip(action_actual, action_predicted, strict=True) if a == "TEST") / sum(a == "TEST" for a in action_actual), "waste_risk_rate": sum(p == "TEST" and a != "TEST" for a, p in zip(action_actual, action_predicted, strict=True)) / action_non_test if action_non_test else None, "hard_negative_fpr": sum(p == "TEST" and a != "TEST" for a, p in zip(action_actual, action_predicted, strict=True)) / action_non_test if action_non_test else None, "abstain_rate": sum(p == "ABSTAIN" for p in action_predicted) / len(action_predicted), "block_accuracy": sum(a == p == "BLOCK" for a, p in zip(action_actual, action_predicted, strict=True)) / sum(a == "BLOCK" for a in action_actual)}, "by_category": {key: {"stage_accuracy": sum(a == p for a, p in zip(value["stage_actual"], value["stage_predicted"], strict=True)) / len(value["stage_actual"]), "decision_accuracy": sum(a == p for a, p in zip(value["action_actual"], value["action_predicted"], strict=True)) / len(value["action_actual"]), "predicted_decisions": dict(Counter(value["action_predicted"]))} for key, value in by_type.items()}, "failure_count": len(failures), "status": "measured on manually authored Phase 4 adversarial controls; no customer outcome claim"}
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    artifact = {"summary": summary, "failure_cases": failures}
    args.json_output.write_text(json.dumps(artifact, indent=2) + "\n")
    args.report_output.write_text(
        "# Adversarial v2 benchmark\n\n"
        "This is a manually authored and provenance-preserving robustness set. "
        "It is not a customer or revenue outcome claim.\n\n"
        + "```json\n"
        + json.dumps(summary, indent=2)
        + "\n```\n"
    )
    if write_supporting_phase4_artifacts:
        Path("artifacts/purchase_stage_adversarial.json").write_text(
            json.dumps({"benchmark": "Phase 4 adversarial purchase-stage benchmark", "purchase_stage": summary["purchase_stage"], "by_category": summary["by_category"], "status": summary["status"]}, indent=2)
            + "\n"
        )
        Path("reports/purchase_stage_adversarial.md").write_text(
            "# Purchase-stage adversarial benchmark\n\n"
            f"The benchmark contains {len(rows)} controlled adversarial records across "
            f"{summary['template_types']} categories.\n\n"
            f"- Accuracy: **{summary['purchase_stage']['accuracy']:.4f}**\n"
            f"- Macro F1: **{summary['purchase_stage']['macro_f1']:.4f}**\n\n"
            "The result is intentionally reported separately from the clean hidden benchmark. "
            "Errors are retained in `artifacts/phase4_failure_cases.jsonl`; no synthetic label is treated as a human outcome.\n"
        )
        Path("artifacts/phase4_failure_cases.jsonl").write_text(
            "\n".join(
                json.dumps(
                    {
                        **failure,
                        "failure_categories": [
                            category
                            for category, condition in (
                                ("wrong_purchase_stage", failure["expected_stage"] != failure["predicted_stage"]),
                                ("spend_decision_mismatch", failure["expected_decision"] != failure["predicted_decision"]),
                            )
                            if condition
                        ],
                        "root_cause": failure["reason_codes"][0] if failure["reason_codes"] else "unexplained_policy_or_stage_error",
                        "fix_attempted": "Phase 4 deterministic SpendSafety policy and current ContextFit scorer",
                    }
                )
                for failure in failures
            )
            + ("\n" if failures else "")
        )
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
