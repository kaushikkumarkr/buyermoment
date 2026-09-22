from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from buyermoment.models import CommercialContextRecord, Evidence, LocationContext, Product
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import SpendSafetyPolicy, spend_safety

def metrics(pairs: list[tuple[str, str, bool, bool]]) -> dict:
    total = len(pairs)
    test_pred = [item for item in pairs if item[1] == "TEST"]
    test_gold = [item for item in pairs if item[0] == "TEST"]
    waste_denominator = sum(item[0] != "TEST" for item in pairs)
    false_abstain_denominator = sum(item[0] == "TEST" for item in pairs)
    eligible_gold = [item for item in pairs if item[0] in {"TEST", "WATCH"}]
    eligible_pred = [item for item in pairs if item[1] in {"TEST", "WATCH"}]
    eligible_gold_count = len(eligible_gold)
    return {
        "count": total,
        "decision_accuracy": sum(actual == predicted for actual, predicted, _, _ in pairs) / total if total else None,
        "test_precision": sum(actual == "TEST" for actual, _, _, _ in test_pred) / len(test_pred) if test_pred else None,
        "test_recall": sum(predicted == "TEST" for _, predicted, _, _ in test_gold) / len(test_gold) if test_gold else None,
        "waste_risk_rate": sum(predicted == "TEST" and actual != "TEST" for actual, predicted, _, _ in pairs) / waste_denominator if waste_denominator else None,
        "hard_negative_fpr": sum(predicted == "TEST" and actual != "TEST" for actual, predicted, _, _ in pairs) / waste_denominator if waste_denominator else None,
        "abstain_rate": sum(predicted == "ABSTAIN" for _, predicted, _, _ in pairs) / total if total else None,
        "false_abstention_rate": sum(predicted in {"ABSTAIN", "BLOCK"} for actual, predicted, _, _ in pairs if actual == "TEST") / false_abstain_denominator if false_abstain_denominator else None,
        "block_accuracy": sum(actual == predicted == "BLOCK" for actual, predicted, _, _ in pairs) / sum(actual == "BLOCK" for actual, _, _, _ in pairs) if any(actual == "BLOCK" for actual, _, _, _ in pairs) else None,
        "eligible_precision": sum(actual in {"TEST", "WATCH"} for actual, predicted, _, _ in eligible_pred) / len(eligible_pred) if eligible_pred else None,
        "eligible_recall": sum(predicted in {"TEST", "WATCH"} for _, predicted, _, _ in eligible_gold) / eligible_gold_count if eligible_gold_count else None,
        "eligible_coverage": len(eligible_pred) / total if total else None,
    }

def product_for(row: CommercialContextRecord) -> Product:
    attributes = row.product_attributes
    return Product(id=row.product_id or row.record_id, name=row.product_title or "product", category="controlled", description=f"{row.product_description or 'controlled product'} {row.context_text}", price=attributes.get("price"), currency=str(attributes.get("currency", "USD")), service_regions=list(attributes.get("service_regions", [])), available=attributes.get("available"), shipping_deadline_met=attributes.get("shipping_deadline_met"), evidence=row.evidence or [Evidence(id=f"{row.record_id}:product", kind="observed", text="Controlled product evidence supplied for this test.", source="phase4_control")])

def evaluate_rows(rows: list[CommercialContextRecord], policy: SpendSafetyPolicy) -> tuple[list[tuple[str, str, bool, bool]], list[dict]]:
    pairs = []
    failures = []
    for row in rows:
        context = build_context(row.context_text, source=row.source_dataset, context_id=row.record_id).model_copy(update={"location": row.location})
        result = score(context, product_for(row))
        decision = spend_safety(context, product_for(row), result, policy)
        actual = str(row.metadata.get("gold_spend_decision", "ABSTAIN"))
        should_spend = bool(row.metadata.get("gold_should_spend", actual == "TEST"))
        pairs.append((actual, decision.decision, should_spend, decision.decision == "TEST"))
        if actual != decision.decision:
            failures.append({"record_id": row.record_id, "category": row.metadata.get("adversarial_type"), "context": row.context_text, "expected": actual, "predicted": decision.decision, "reason_codes": decision.reason_codes, "contextfit": result.model_dump(mode="json"), "spend_decision": decision.model_dump(mode="json"), "root_cause": decision.reason_codes[0] if decision.reason_codes else "policy_threshold", "fix_attempted": "Phase 4 deterministic policy layer"})
    return pairs, failures

def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate deterministic SpendDecision and Waste-Risk metrics.")
    parser.add_argument("--input", type=Path, default=Path("data/ccb1/adversarial/adversarial_v2.jsonl"))
    parser.add_argument("--json-output", type=Path, default=Path("artifacts/spend_safety_benchmark.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/spend_safety_benchmark.md"))
    args = parser.parse_args()
    rows = [CommercialContextRecord.model_validate_json(line) for line in args.input.read_text().splitlines() if line.strip()]
    policy = SpendSafetyPolicy()
    validation, hidden = [row for row in rows if row.split == "validation"], [row for row in rows if row.split == "hidden_test"]
    hidden_pairs, failures = evaluate_rows(hidden, policy)
    by_category: dict[str, list[tuple[str, str, bool, bool]]] = defaultdict(list)
    for row in hidden:
        pair, _ = evaluate_rows([row], policy)
        by_category[str(row.metadata.get("adversarial_type"))].extend(pair)
    journey_path = Path("data/ccb1/multiturn/phase4_journeys.jsonl")
    journey_pairs: list[tuple[str, str, bool, bool]] = []
    if journey_path.exists():
        for line in journey_path.read_text().splitlines():
            row = json.loads(line)
            product = Product(id="journey-product", name="journey product", category="controlled", description=f"controlled product for {row['context_text']}", price=120, service_regions=["US", "Canada"], available=True, evidence=[Evidence(id="journey-product:evidence", kind="observed", text="Controlled product evidence supplied for the journey.", source="phase4_control")])
            context = build_context(row["context_text"], context_id=str(row["turn_id"])).model_copy(update={"location": LocationContext(country=row.get("country", "US"))})
            result = score(context, product)
            decision = spend_safety(context, product, result, policy)
            expected = "TEST" if row["purchase_stage"] in {"consideration", "comparison", "transactional"} else ("BLOCK" if row.get("expected_block") else "ABSTAIN")
            journey_pairs.append((expected, decision.decision, expected == "TEST", decision.decision == "TEST"))
    clean = {"count": 33190, "ground_truth": "not available for SpendDecision; Phase 3 hidden records do not have spend-action labels", "decision_distribution": {}}
    summary = {"benchmark": "Phase 4 SpendDecision benchmark", "policy": policy.__dict__, "validation": metrics(evaluate_rows(validation, policy)[0]), "adversarial_hidden": metrics(hidden_pairs), "adversarial_by_category": {key: metrics(value) for key, value in by_category.items()}, "multi_turn": metrics(journey_pairs), "clean_hidden": clean, "abstention_semantics": {"TEST": "eligible for a human-approved experiment", "WATCH": "plausible but not spend-ready", "ABSTAIN": "insufficient or non-actionable evidence", "BLOCK": "known policy or serviceability failure"}, "status": "measured; human approval remains mandatory"}
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(summary, indent=2) + "\n")
    args.report_output.write_text("# Spend-safety benchmark\n\n" + json.dumps(summary, indent=2) + "\n")
    Path("artifacts/phase4_spend_failure_cases.jsonl").write_text("\n".join(json.dumps(item) for item in failures) + ("\n" if failures else ""))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
