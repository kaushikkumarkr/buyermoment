from __future__ import annotations

from .models import BuyerMoment, BusinessProfile, CommercialContext, Constraints, Evidence, LocationContext
from .scoring import score


def discover_buyer_moments(business: BusinessProfile) -> list[BuyerMoment]:
    moments: list[BuyerMoment] = []
    for index, product in enumerate(business.products):
        if index == 0 and business.category == "footwear":
            context_text = "I need waterproof hiking boots under $150 for Yellowstone."
            title = "Waterproof trail confidence under $150"
            problem = "Hikers need dependable footwear for wet, variable terrain without crossing a clear budget ceiling."
            situation = "Planning a Yellowstone trip with a concrete destination, feature requirement, and price constraint."
            outcome = "Find a waterproof, slip-resistant boot that can ship in time for the trip."
            constraints = Constraints(budget=150, currency="USD", required_features=["waterproof", "slip-resistant"], geography="Yellowstone", timing="before the trip")
            location = LocationContext(country="US", region="Wyoming/Montana", language="en", currency="USD", shipping="US shipping", location_specificity="region")
            stage = "consideration"
        elif index == 0 and business.category == "skincare":
            context_text = "What is a fragrance-free routine for sensitive skin under $80?"
            title = "A low-friction sensitive-skin routine"
            problem = "People with sensitive skin need a simple routine that avoids fragrance and stays within a manageable spend."
            situation = "Actively evaluating a routine with a skin constraint and a budget."
            outcome = "Build a gentle, fragrance-free starter routine with clear product roles."
            constraints = Constraints(budget=80, currency="USD", required_features=["fragrance-free", "sensitive skin"])
            location = LocationContext(country="US", language="en", currency="USD", shipping="US shipping", location_specificity="country")
            stage = "consideration"
        else:
            context_text = "We need SOC 2-ready customer support analytics for a 30-person team this quarter."
            title = "Support analytics that clears security review"
            problem = "A small support team needs actionable analytics without creating a security or implementation project."
            situation = "A team is evaluating a B2B tool against a compliance and timing constraint."
            outcome = "Shortlist a tool the team can adopt this quarter and take through security review."
            constraints = Constraints(required_features=["SOC 2"], timing="this quarter", geography="North America")
            location = LocationContext(country="US", language="en", currency="USD", location_specificity="country")
            stage = "comparison"
        context = CommercialContext(
            id=f"{business.id}-ctx-{index + 1}",
            context_text=context_text,
            problem=problem,
            desired_outcome=outcome,
            use_case=situation,
            constraints=constraints,
            location=location,
            purchase_stage=stage,
            urgency=0.85 if constraints.timing else 0.68,
            commerciality=0.88,
            product_category=product.category,
            product_candidates=[product.id],
            confidence=0.86,
            source="demo business evidence",
            provenance=[f"candidate synthesized from {business.name} product evidence", "deterministic constraint matching"],
            evidence=[
                Evidence(id=f"{business.id}-evidence-{index + 1}", kind="observed", text=product.description, source="product_catalog", source_record_id=product.id, confidence=0.98),
                Evidence(id=f"{business.id}-evidence-context-{index + 1}", kind="inference", text=f"Candidate situation: {situation}", source="buyer_moment_discovery", provenance=["product catalog", "structured context template"], confidence=0.73),
            ],
        )
        result = score(context, product)
        moments.append(BuyerMoment(
            id=f"{business.id}-moment-{index + 1}",
            business_id=business.id,
            title=title,
            problem=problem,
            situation=situation,
            desired_outcome=outcome,
            constraints=constraints,
            purchase_stage=stage,
            location=location,
            matching_products=[product],
            supporting_evidence=context.evidence,
            confidence=result.confidence,
            score=result,
            why_experiment="Strong constraints plus a clear product match make this a useful testable hypothesis; it is not a profitability claim.",
        ))
    return sorted(moments, key=lambda item: item.score.overall, reverse=True)

