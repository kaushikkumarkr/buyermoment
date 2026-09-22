from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.models import CommercialContextRecord, Evidence, LocationContext

CASES = [
    ("third_party_buying", "I'm comparing these for my mother, not for myself, and I'm ready to order today.", "transactional", "TEST", True, 120, ["US", "Canada"], True, None, "US"),
    ("gift_buying", "I want to buy this skincare set as a gift for my sister in Canada.", "transactional", "TEST", True, 72, ["US", "Canada"], True, None, "Canada"),
    ("research_only", "I'm researching CRM software for a market report, not buying one.", "informational", "ABSTAIN", False, 299, ["US"], True, None, "US"),
    ("existing_support", "I already bought these shoes. Should I return them because they hurt?", "informational", "BLOCK", False, 120, ["US"], True, None, "US"),
    ("negative_alternatives", "I hate this brand. What alternatives can I buy today?", "transactional", "TEST", True, 120, ["US"], True, None, "US"),
    ("competitor_research", "I'm evaluating competitors for work and will not purchase this quarter.", "informational", "ABSTAIN", False, 299, ["US"], True, None, "US"),
    ("future_intent", "I might move to Boston next year. What would I need then?", "exploration", "ABSTAIN", False, 120, ["US"], True, None, "US"),
    ("conditional_intent", "If I get promoted, I may buy one later.", "exploration", "ABSTAIN", False, 120, ["US"], True, None, "US"),
    ("company_gathering", "My company pays for this, but I'm only gathering options.", "exploration", "ABSTAIN", False, 299, ["US"], True, None, "US"),
    ("budget_mismatch", "I need something under $100 total including shipping.", "consideration", "BLOCK", True, 120, ["US"], True, None, "US"),
    ("location_mismatch", "I live in Canada, but this offer is US-only.", "consideration", "BLOCK", True, 120, ["US"], True, None, "Canada"),
    ("mixed_commercial", "What should I look for in hiking shoes? I need waterproof ones under $150.", "consideration", "TEST", True, 120, ["US"], True, None, "US"),
    ("ambiguous_pronoun", "Would that work for me?", "exploration", "ABSTAIN", False, 120, ["US"], True, None, "US"),
    ("multiple_users", "I need shoes for me, and my sister wants a pair too. Can I order both today?", "transactional", "TEST", True, 120, ["US"], True, None, "US"),
    ("location_change", "I moved to Canada and need the same service there this month.", "consideration", "BLOCK", True, 299, ["US"], True, None, "Canada"),
    ("budget_change", "I need the plan under $50 per month for 20 users.", "consideration", "BLOCK", True, 299, ["US"], True, None, "US"),
    ("intent_reversal", "I need waterproof boots, but I already bought them. How do I clean them?", "informational", "BLOCK", False, 120, ["US"], True, None, "US"),
    ("sarcasm", "Sure, I definitely want to spend money on another useless CRM.", "informational", "ABSTAIN", False, 299, ["US"], True, None, "US"),
    ("hypothetical", "Hypothetically, if money were no object, which shoes would I buy?", "exploration", "ABSTAIN", False, 120, ["US"], True, None, "US"),
    ("professional_research", "I'm writing a professional article explaining why these products are popular.", "informational", "ABSTAIN", False, 120, ["US"], True, None, "US"),
    ("return_request", "Can I exchange the moisturizer I already purchased for another one?", "informational", "BLOCK", False, 72, ["US"], True, None, "US"),
    ("availability_buy", "Is the PeakShield in stock in the US, and can I buy it today?", "transactional", "TEST", True, 120, ["US"], True, None, "US"),
    ("unavailable_product", "I need this exact product today, but the catalog says it is unavailable.", "transactional", "BLOCK", True, 120, ["US"], False, None, "US"),
    ("shipping_deadline", "I need these shoes to arrive by Friday for my trip.", "transactional", "BLOCK", True, 120, ["US"], True, False, "US"),
    ("language_mismatch", "I need this service in Spanish, but the offer only supports English.", "consideration", "BLOCK", True, 299, ["US"], True, None, "US"),
    ("team_comparison", "Compare the team and core plans for our support team this quarter.", "comparison", "TEST", True, 299, ["US", "Canada"], True, None, "US"),
    ("popular_research", "I want to understand why these products are popular, not buy one.", "informational", "ABSTAIN", False, 120, ["US"], True, None, "US"),
    ("complaint", "Why is my current CRM so slow?", "informational", "ABSTAIN", False, 299, ["US"], True, None, "US"),
    ("direct_gift", "My mother lives in Nevada; please order her the fragrance-free set today.", "transactional", "TEST", True, 72, ["US"], True, None, "US"),
    ("research_then_buy", "I'm comparing waterproof boots for an article, not for a purchase.", "informational", "ABSTAIN", False, 120, ["US"], True, None, "US"),
]

VARIANT_SUFFIXES = (
    "For reference.",
    "This is the current context.",
    "Please take these details into account.",
    "This is a specific case.",
    "The question is about this situation.",
    "Please consider the full context.",
    "This is not a general example.",
    "Answer with this context in mind.",
    "That is the situation.",
    "Use the details provided here.",
)

def main() -> None:
    parser = argparse.ArgumentParser(description="Build the Phase 4 adversarial v2 benchmark.")
    parser.add_argument("--repeat", type=int, default=10)
    parser.add_argument("--output", type=Path, default=Path("data/ccb1/adversarial/adversarial_v2.jsonl"))
    args = parser.parse_args()
    rows = []
    for index, (kind, text, stage, action, should_spend, price, regions, available, shipping_met, country) in enumerate(CASES):
        for repeat in range(args.repeat):
            variant_text = f"{text} {VARIANT_SUFFIXES[repeat % len(VARIANT_SUFFIXES)]}"
            record_id = f"adversarial-v2:{kind}:{repeat:02d}:{index:02d}"
            split = "validation" if index < len(CASES) // 2 else "hidden_test"
            rows.append(CommercialContextRecord(record_id=record_id, source_dataset="ccb1_adversarial_v2", source_record_id=record_id, source_license="Synthetic reviewed Phase 4 adversarial benchmark; no external license", context_text=variant_text, original_query=text, product_id=f"phase4-product:{kind}", product_title="Phase 4 referenced product", product_description="Controlled product evidence for safety evaluation.", product_attributes={"price": price, "currency": "USD", "service_regions": regions, "available": available, "shipping_deadline_met": shipping_met}, location=LocationContext(country=country, location_specificity="country"), purchase_stage=stage, commerciality="high" if should_spend else "none", evidence=[Evidence(id=f"{record_id}:text", kind="observed", text=variant_text, source="phase4-adversarial-review", source_record_id=record_id, confidence=1.0)], provenance=["phase4 manually authored adversarial template", "separate from Phase 3 hidden split"], transformation_history=["designed for spend-safety and abstention evaluation", f"controlled paraphrase suffix variant {repeat}"], confidence=1.0, split=split, metadata={"adversarial_type": kind, "gold_spend_decision": action, "gold_should_spend": should_spend, "gold_location_country": country, "label_origin": "manual_phase4_control"}))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(row.model_dump_json() for row in rows) + "\n")
    print(json.dumps({"records": len(rows), "template_types": len(CASES), "output": str(args.output)}, indent=2))

if __name__ == "__main__":
    main()
