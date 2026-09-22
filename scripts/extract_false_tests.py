from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from buyermoment.models import CommercialContextRecord, SpendDecision
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import spend_safety
from evaluate_spend_safety import product_for


def classify_failure(row: CommercialContextRecord) -> tuple[str, str]:
    text = row.context_text.lower()
    kind = str(row.metadata.get("adversarial_type", "unknown"))
    if any(term in text for term in ("hypothetically", "if money were no object", "sarcasm", "useless")):
        return "ambiguous_intent", "The lexical scorer treats product/buying language as actionable despite hypothetical or negative framing."
    if any(term in text for term in ("research", "paper", "article", "market report", "not buying", "not for a purchase", "will not purchase")):
        return "research_mistaken_for_purchase", "Research framing was not converted into a sufficiently strong abstention signal."
    if any(term in text for term in ("might", "maybe", "if i", "next year", "later", "could buy")):
        return "future_intent", "A future or conditional purchase was treated as immediate test readiness."
    if any(term in text for term in ("already own", "already bought", "already purchased", "clean", "return")):
        return "existing_owner_support", "Ownership/support language was not fully recognized before the positive decision."
    if any(term in text for term in ("mother", "father", "sister", "brother", "child", "client", "not for me")):
        return "third_party_intent", "The beneficiary or buyer identity is not represented as an explicit readiness signal."
    if kind in {"mixed_commercial", "ambiguous_pronoun"}:
        return "mixed_or_ambiguous_intent", "Multiple plausible intents or unresolved references remain in the context."
    if kind in {"budget_mismatch", "budget_change"}:
        return "constraint_mismatch", "The product/constraint compatibility signal did not block the positive decision."
    if kind in {"location_mismatch", "location_change", "shipping_deadline"}:
        return "location_or_serviceability", "Location or fulfillment evidence was insufficiently decisive."
    return "policy_or_threshold_gap", "The current TEST thresholds accepted a case that the control label marks as not ready."


def legacy_phase4_decision(context, product, contextfit) -> SpendDecision:
    """Replays the Phase 4 pre-TestReadiness policy for baseline error extraction."""
    lowered = context.context_text.lower()
    reason = None
    decision = "TEST"
    if any(term in lowered for term in ("how do i clean", "how do i use", "already own", "already purchased", "export contacts", "should i return", "return these")):
        decision, reason = "BLOCK", "EXISTING_OWNER_SUPPORT"
    elif any(term in lowered for term in ("researching", "researching competitors", "evaluating competitors", "for a paper", "market report", "academic", "professional article", "not buying", "not purchase", "not purchasing", "will not purchase", "just gathering options", "only gathering options", "understand why")):
        decision, reason = "ABSTAIN", "RESEARCH_ONLY"
    elif any(term in lowered for term in ("might", "maybe", "if i", "until next year", "one day", "could buy later")):
        decision, reason = "ABSTAIN", "FUTURE_OR_CONDITIONAL_INTENT"
    elif any(term in lowered for term in ("hate this brand", "dislike this brand", "why is my current", "so slow", "frustrating")) and "buy" not in lowered and "order" not in lowered:
        decision, reason = "ABSTAIN", "NEGATIVE_SENTIMENT_OR_COMPLAINT"
    elif "us-only" in lowered and (context.location.country or context.constraints.geography or "").lower() not in {"", "us", "usa", "united states", "u.s."}:
        decision, reason = "BLOCK", "LOCATION_UNSERVICEABLE"
    elif product.service_regions and context.location.country and contextfit.location_fit < 0.5:
        decision, reason = "BLOCK", "LOCATION_UNSERVICEABLE"
    elif context.constraints.budget is not None and product.price is not None and product.price > context.constraints.budget:
        decision, reason = "BLOCK", "BUDGET_INCOMPATIBLE"
    elif product.available is False:
        decision, reason = "BLOCK", "PRODUCT_UNAVAILABLE"
    elif product.shipping_deadline_met is False or "doesn't ship" in lowered or "does not ship" in lowered:
        decision, reason = "BLOCK", "SHIPPING_UNSERVICEABLE"
    elif "only supports english" in lowered or "english only" in lowered:
        decision, reason = "BLOCK", "LANGUAGE_UNSUPPORTED"
    elif product.price is None or not product.evidence:
        decision, reason = "ABSTAIN", "INSUFFICIENT_EVIDENCE"
    elif not (contextfit.overall >= 0.72 and contextfit.confidence >= 0.68 and contextfit.commercial_actionability >= 0.42):
        decision, reason = ("WATCH", "PLAUSIBLE_BUT_UNCERTAIN") if contextfit.overall >= 0.50 and contextfit.confidence >= 0.50 else ("ABSTAIN", "LOW_CONFIDENCE")
    else:
        reason = "EVIDENCE_BACKED_COMMERCIAL_CONTEXT"
    return SpendDecision(decision=decision, commercial_actionability=contextfit.commercial_actionability, reason_codes=[reason], evidence=contextfit.evidence, confidence=contextfit.confidence, policy_version="phase4-v1-baseline", human_approval_required=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract every false TEST from the Phase 4 adversarial controls.")
    parser.add_argument("--input", type=Path, default=Path("data/ccb1/adversarial/adversarial_v2.jsonl"))
    parser.add_argument("--jsonl-output", type=Path, default=Path("artifacts/false_test_cases.jsonl"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/false_test_analysis.md"))
    parser.add_argument("--mode", choices=("baseline", "current"), default="baseline")
    args = parser.parse_args()
    rows = [CommercialContextRecord.model_validate_json(line) for line in args.input.read_text().splitlines() if line.strip()]
    failures = []
    for row in rows:
        context = build_context(row.context_text, source=row.source_dataset, context_id=row.record_id).model_copy(update={"location": row.location})
        product = product_for(row)
        contextfit = score(context, product)
        decision = legacy_phase4_decision(context, product, contextfit) if args.mode == "baseline" else spend_safety(context, product, contextfit)
        expected = str(row.metadata.get("gold_spend_decision", "ABSTAIN"))
        if decision.decision != "TEST" or expected == "TEST":
            continue
        category, root_cause = classify_failure(row)
        failures.append(
            {
                "record_id": row.record_id,
                "split": row.split,
                "adversarial_type": row.metadata.get("adversarial_type"),
                "context": row.context_text,
                "product": product.model_dump(mode="json"),
                "offer": None,
                "location": row.location.model_dump(mode="json"),
                "evidence": [item.model_dump(mode="json") for item in row.evidence],
                "contextfit": contextfit.model_dump(mode="json"),
                "spend_decision": decision.model_dump(mode="json"),
                "expected_decision": expected,
                "reason_codes": decision.reason_codes,
                "failure_category": category,
                "root_cause_hypothesis": root_cause,
                "held_out": row.split == "hidden_test",
            }
        )
    counts = Counter(item["failure_category"] for item in failures)
    split_counts = Counter(item["split"] for item in failures)
    summary = {"false_test_count": len(failures), "by_category": dict(counts), "by_split": dict(split_counts), "source_records": len(rows), "mode": args.mode, "method": "Phase 4 deterministic SpendSafety replay; expected labels are manually authored adversarial controls, not campaign outcomes."}
    args.jsonl_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.jsonl_output.write_text("\n".join(json.dumps(item) for item in failures) + ("\n" if failures else ""))
    lines = [
        "# False TEST analysis",
        "",
        f"The replay found **{len(failures)}** false TEST decisions across {len(rows)} adversarial controls. "
        "The hidden subset is kept separate from validation in the artifact.",
        "",
        "## Counts",
        "",
        *[f"- `{key}`: {value}" for key, value in counts.most_common()],
        "",
        "## Split",
        "",
        *[f"- `{key}`: {value}" for key, value in split_counts.items()],
        "",
        "## Interpretation",
        "",
        "These are control-label mismatches used to improve safety. A false TEST is treated as a spend-safety failure even when the underlying context contains some commercial interest. The full product, location, evidence, ContextFit, SpendDecision, reason codes, and root-cause hypothesis are retained in `artifacts/false_test_cases.jsonl`.",
        "",
        "## Immediate remediation direction",
        "",
        "The next policy should require strong test-readiness evidence, penalize ambiguity and future/conditional language, and keep plausible but under-evidenced contexts in WATCH. Threshold selection will be performed on validation controls and checked on the hidden subset.",
    ]
    args.report_output.write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
