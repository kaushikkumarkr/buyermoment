from __future__ import annotations

import json
from pathlib import Path

from buyermoment.b2b import B2BCommercialContextRecord


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "ccb_b2b"


SCENARIOS = [
    ("CRM", "We are a 60-person construction company using spreadsheets and need a CRM with email integration this quarter.", "consideration", "high", "actionable", "operations manager", "small business", ["email"], "this quarter"),
    ("CRM", "I am preparing an academic report comparing CRM vendors; our team is not buying software.", "informational", "low", "not_actionable", "researcher", "unknown", [], "none"),
    ("Sales", "Our sales team needs lead routing and a Salesforce integration before the next hiring cycle; procurement has started.", "consideration", "high", "actionable", "sales operations", "mid-market", ["Salesforce"], "before next hiring cycle"),
    ("Sales", "How do I export contacts from our current sales platform? We already own it.", "informational", "low", "not_actionable", "sales administrator", "unknown", [], "none"),
    ("Marketing Automation", "We need lifecycle email automation for a 70-person SaaS company and want to select a vendor by Q4.", "comparison", "high", "actionable", "marketing director", "B2B SaaS", ["email"], "by Q4"),
    ("Marketing Automation", "I am researching marketing automation vendors for a client market report, not a purchase.", "informational", "low", "not_actionable", "consultant", "unknown", [], "none"),
    ("Analytics / BI", "Our finance team needs a BI tool that connects to Snowflake and can be implemented this year.", "consideration", "high", "actionable", "finance leader", "mid-market", ["Snowflake"], "this year"),
    ("Analytics / BI", "What is the history of business intelligence software? This is for a class assignment.", "informational", "none", "not_actionable", "student", "unknown", [], "none"),
    ("Accounting / Finance", "We are replacing accounting software after an audit issue and need a compliant migration plan next month.", "consideration", "high", "actionable", "controller", "mid-market", [], "next month"),
    ("Accounting / Finance", "If our board approves next year, we might replace our accounting system.", "exploration", "medium", "uncertain", "founder", "small business", [], "next year if approved"),
    ("Procurement", "Our procurement team is evaluating intake software with SSO and approval workflows for a rollout in 90 days.", "comparison", "high", "actionable", "procurement lead", "enterprise", ["SSO"], "90 days"),
    ("Procurement", "I am learning procurement software categories for a consulting presentation.", "informational", "low", "not_actionable", "consultant", "unknown", [], "none"),
    ("Project Management", "We need project tracking for 25 engineers and must migrate from Trello before the next planning cycle.", "consideration", "high", "actionable", "engineering manager", "small business", ["Trello migration"], "next planning cycle"),
    ("Project Management", "How can I recover a deleted task in the project tool we already use?", "informational", "low", "not_actionable", "project administrator", "unknown", [], "none"),
    ("DevOps", "Our team needs CI/CD governance with GitHub integration and a security review before adoption.", "exploration", "medium", "uncertain", "platform engineer", "mid-market", ["GitHub"], "security review first"),
    ("DevOps", "Compare CI/CD tools for a research article; there is no approved project or buying timeline.", "comparison", "low", "not_actionable", "analyst", "unknown", [], "none"),
    ("Cybersecurity", "We need endpoint monitoring that supports our compliance program and can be deployed in the US this quarter.", "consideration", "high", "actionable", "security lead", "enterprise", [], "this quarter"),
    ("Cybersecurity", "Our current security product is slow; how do I open a support ticket?", "informational", "low", "not_actionable", "IT administrator", "unknown", [], "none"),
    ("HR / Payroll", "We are selecting payroll software for a 40-person company with a go-live target in six months.", "comparison", "high", "actionable", "people operations", "small business", [], "six months"),
    ("HR / Payroll", "I am studying how payroll systems evolved and do not have authority to buy one.", "informational", "low", "not_actionable", "student", "unknown", [], "none"),
    ("Customer Support", "Our support team is outgrowing email and needs a ticketing system with Slack integration this quarter.", "consideration", "high", "actionable", "support leader", "mid-market", ["Slack"], "this quarter"),
    ("Customer Support", "We already use a help desk and want to understand why ticket routing failed yesterday.", "informational", "low", "not_actionable", "support administrator", "unknown", [], "none"),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for index, (category, context, stage, commerciality, actionability, role, company_size, integrations, timing) in enumerate(SCENARIOS, start=1):
        record = {
            "record_id": f"ccb-b2b:silver:{index:03d}",
            "category": category,
            "context_text": context,
            "company_size": company_size,
            "industry": "B2B SaaS or professional services (controlled scenario)",
            "buyer_role": role,
            "recipient": "company team",
            "current_stack": [],
            "current_vendor": None,
            "pain_point": "controlled scenario pain point; requires review",
            "desired_outcome": "select or understand a suitable business software option",
            "required_integrations": integrations,
            "required_features": [],
            "excluded_features": [],
            "budget": None,
            "contract_preference": None,
            "security_requirement": [],
            "compliance_requirement": [],
            "migration_need": None,
            "implementation_timeline": timing,
            "purchase_timing": timing,
            "procurement_status": "controlled scenario",
            "decision_authority": "unknown",
            "geography": "US" if "US" in context else None,
            "purchase_stage": stage,
            "commerciality": commerciality,
            "commercial_actionability": actionability,
            "candidate_product": None,
            "product_fit": None,
            "offer_fit": None,
            "evidence": [{"id": f"ccb-b2b:evidence:{index:03d}", "kind": "hypothesis", "text": "Controlled B2B benchmark scenario; not a customer statement or product fact.", "source": "ccb_b2b_seed", "source_record_id": f"ccb-b2b:silver:{index:03d}", "provenance": ["scripts/build_ccb_b2b_seed.py"], "confidence": 0.5}],
            "provenance": ["controlled scenario authored for CCB-B2B silver review queue"],
            "label_quality": "SILVER",
            "review_status": "pending",
            "confidence": 0.5,
            "metadata": {"data_origin": "synthetic", "human_review_required": True, "source_scenario": "phase8_manual_seed"},
        }
        records.append(B2BCommercialContextRecord.model_validate(record).model_dump(mode="json"))
    path = OUT / "silver_review_queue.jsonl"
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")
    manifest = {"version": "CCB-B2B silver v0.1", "records": len(records), "human_reviewed_records": 0, "gold_holdout": 0, "review_queue": len(records), "categories": sorted({record["category"] for record in records}), "status": "SILVER_REVIEW_QUEUE_ONLY; no human-reviewed gold benchmark"}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
