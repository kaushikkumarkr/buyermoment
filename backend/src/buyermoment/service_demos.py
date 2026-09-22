from __future__ import annotations

from .commercial import BusinessEvidencePackage, BusinessHypothesis
from .models import BusinessProfile, Evidence, Offer, Product


def _demo_package(client_id: str, name: str, category: str, product_name: str, description: str, problem: str, offer_name: str, situation: str) -> BusinessEvidencePackage:
    evidence = Evidence(
        id=f"{client_id}-evidence-1",
        kind="observed",
        text=f"DEMO_SYNTHETIC: {description}",
        source="service_demo_fixture",
        source_record_id=f"{client_id}-product",
        provenance=["synthetic fixture; not a real company claim"],
        confidence=1.0,
    )
    product = Product(id=f"{client_id}-product", name=product_name, category=category, description=description, url=f"https://demo.invalid/{client_id}", features=["role-based access", "exportable reporting"], evidence=[evidence])
    offer = Offer(id=f"{client_id}-offer", name=offer_name, description=f"DEMO_SYNTHETIC: {offer_name} for teams evaluating {product_name}.", evidence=[evidence])
    business = BusinessProfile(id=client_id, name=name, category=category, website=f"https://demo.invalid/{client_id}", description=f"DEMO_SYNTHETIC: {description}", products=[product], offers=[offer], evidence=[evidence])
    hypothesis = BusinessHypothesis(id=f"{client_id}-hypothesis-1", label=f"{category} teams with an active evaluation", situation=situation, problem=problem, desired_outcome=f"Shortlist {product_name} for a controlled evaluation.", evidence_ids=[evidence.id], origin="observed_evidence")
    return BusinessEvidencePackage(business=business, target_customer_hypotheses=[hypothesis], evidence_store=[evidence], unknowns=["DEMO_SYNTHETIC: no real customers, pricing, margins, or campaign outcomes supplied."])


def service_demo_packages() -> list[BusinessEvidencePackage]:
    return [
        _demo_package("demo-crm", "Demo CRM SaaS", "CRM", "Pipeline Desk", "DEMO_SYNTHETIC: CRM workspace with account views and role-based reporting.", "Revenue teams need a clearer handoff from inbound lead to sales owner.", "Book a workflow review", "A 60-person services company is replacing spreadsheets and wants a CRM shortlist this quarter."),
        _demo_package("demo-analytics", "Demo Analytics SaaS", "Analytics / BI", "Signal Board", "DEMO_SYNTHETIC: analytics workspace with exportable reporting and role-based access.", "Finance and operations teams need a shared view of weekly performance without a long implementation.", "Request an analytics assessment", "A mid-market operations team is evaluating BI tools with a defined implementation window."),
        _demo_package("demo-cyber", "Demo Cybersecurity SaaS", "Cybersecurity", "Cloud Guard", "DEMO_SYNTHETIC: cloud security workflow with role-based findings and exportable reports.", "Security teams need a practical shortlist that fits their review and data-residency requirements.", "Schedule a security review", "A security team is comparing cloud posture tools before a quarterly assessment."),
    ]
