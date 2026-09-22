from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.models import Evidence, LocationContext, Product
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import spend_safety

CASES = (
    ("base", "I need waterproof hiking shoes under $150.", "WATCH", "PLAUSIBLE_BUT_UNCERTAIN"),
    ("budget_lowered", "I need waterproof hiking shoes under $50.", "BLOCK", "BUDGET_INCOMPATIBLE"),
    ("existing_owner", "I already own waterproof hiking shoes. How do I clean them?", "BLOCK", "EXISTING_OWNER_SUPPORT"),
    ("research_only", "I'm researching waterproof hiking shoes for an article.", "ABSTAIN", "RESEARCH_ONLY"),
    ("location_unserviceable", "I need waterproof hiking shoes under $150, but they must ship to Canada.", "BLOCK", "LOCATION_UNSERVICEABLE"),
    ("future_intent", "I might buy waterproof hiking shoes next year.", "ABSTAIN", "FUTURE_OR_CONDITIONAL_INTENT"),
)

def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate one-feature counterfactual spend-safety changes.")
    parser.add_argument("--repeat", type=int, default=25)
    parser.add_argument("--json-output", type=Path, default=Path("artifacts/counterfactual_robustness.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/counterfactual_robustness.md"))
    args = parser.parse_args()
    rows = []
    for repeat in range(args.repeat):
        for kind, text, expected, reason in CASES:
            product = Product(id="counterfactual-product", name="Waterproof hiking shoes", category="hiking boots", description="Waterproof hiking shoes with traction.", price=120, service_regions=["US"], available=True, evidence=[Evidence(id="counterfactual-product:evidence", kind="observed", text="Catalog lists waterproof hiking shoes at $120 for US service.", source="counterfactual_catalog")])
            if kind == "location_unserviceable":
                product = product.model_copy(update={"service_regions": ["US"]})
            context = build_context(text, context_id=f"counterfactual:{kind}:{repeat}")
            context = context.model_copy(update={"location": LocationContext(country="Canada") if kind == "location_unserviceable" else context.location})
            result = score(context, product)
            decision = spend_safety(context, product, result)
            rows.append({"kind": kind, "text": text, "expected_decision": expected, "predicted_decision": decision.decision, "expected_reason": reason, "predicted_reasons": decision.reason_codes, "reason_correct": reason in decision.reason_codes, "direction_correct": decision.decision == expected, "contextfit": result.model_dump(mode="json")})
    summary = {"benchmark": "Phase 4 counterfactual robustness", "cases": len(rows), "consistency": sum(row["direction_correct"] for row in rows) / len(rows), "reason_code_correctness": sum(row["reason_correct"] for row in rows) / len(rows), "by_kind": {kind: {"count": sum(row["kind"] == kind for row in rows), "direction_correct": sum(row["kind"] == kind and row["direction_correct"] for row in rows) / sum(row["kind"] == kind for row in rows), "reason_correct": sum(row["kind"] == kind and row["reason_correct"] for row in rows) / sum(row["kind"] == kind for row in rows)} for kind, _, _, _ in CASES}, "status": "measured on manually authored one-feature counterfactual controls"}
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps({"summary": summary, "cases": rows}, indent=2) + "\n")
    args.report_output.write_text("# Counterfactual robustness\n\n" + json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
