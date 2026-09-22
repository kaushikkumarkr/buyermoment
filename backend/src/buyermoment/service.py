from __future__ import annotations

import re
from typing import Any

from .commercial import BusinessEvidencePackage, BusinessHypothesis, CampaignOutcome
from .commercial_workflow import discover_package_moments
from .models import BusinessProfile, CommercialContext, Evidence, Product
from .readiness import score_test_readiness
from .scoring import score
from .service_models import (
    Client,
    ClientReport,
    EvidenceSource,
    ExperimentPortfolio,
    LandingPageAssessment,
    MeasurementAudit,
    NextBestExperiment,
    OfferFitAssessment,
    PortfolioItem,
    ServiceAnalysis,
)
from .spend_safety import spend_safety


def _terms(text: str) -> set[str]:
    return {item for item in re.findall(r"[a-z0-9][a-z0-9-]+", text.lower()) if len(item) > 2}


def _moment_context(moment, product: Product) -> CommercialContext:
    return CommercialContext(
        id=f"{moment.id}-service-context",
        context_text=f"{moment.situation} {moment.desired_outcome}",
        problem=moment.problem,
        desired_outcome=moment.desired_outcome,
        use_case=moment.situation,
        constraints=moment.constraints,
        location=moment.location,
        purchase_stage=moment.purchase_stage,
        commerciality=moment.score.commerciality,
        product_category=product.category,
        product_candidates=[product.id],
        product_fit=moment.score.product_fit,
        offer_fit=moment.score.offer_fit,
        ad_relevance=moment.score.ad_relevance,
        confidence=moment.confidence,
        source="service_analysis",
        provenance=[moment.id],
        evidence=moment.supporting_evidence,
    )


def offer_fit(client_id: str, moment, business: BusinessProfile) -> OfferFitAssessment:
    if not business.offers:
        return OfferFitAssessment(
            client_id=client_id,
            buyer_moment_id=moment.id,
            fit=0.2,
            recommendation="No approved offer is present; define an offer hypothesis before spend.",
            cta="Review offer options",
            unknowns=["Offer, eligibility, and conversion path are not supplied."],
            risks=["A strong Buyer Moment without a relevant offer is not test-ready."],
        )
    context_terms = _terms(f"{moment.problem} {moment.desired_outcome} {moment.situation}")
    ranked = sorted(business.offers, key=lambda item: len(context_terms & _terms(f"{item.name} {item.description}")), reverse=True)
    chosen = ranked[0]
    overlap = len(context_terms & _terms(f"{chosen.name} {chosen.description}"))
    fit = min(1.0, 0.55 + min(overlap, 8) / 20)
    evidence = chosen.evidence or [Evidence(id=f"{chosen.id}-offer", kind="observed", text=chosen.description, source="offer_catalog", source_record_id=chosen.id, confidence=0.9)]
    return OfferFitAssessment(
        client_id=client_id,
        buyer_moment_id=moment.id,
        offer_id=chosen.id,
        fit=fit,
        recommendation=f"Test {chosen.name} as the offer hypothesis for this Buyer Moment.",
        cta=chosen.name,
        evidence=evidence,
        unknowns=["Offer conversion rate is unknown until a real experiment runs."],
        risks=["Offer fit is semantic/provisional; human approval is required."],
    )


def landing_page_fit(client_id: str, moment, business: BusinessProfile) -> LandingPageAssessment:
    product = moment.matching_products[0] if moment.matching_products else None
    if not product or not product.url:
        return LandingPageAssessment(
            client_id=client_id,
            buyer_moment_id=moment.id,
            status="NEW_LANDING_PAGE_RECOMMENDED",
            fit=0.25,
            message_match=0.25,
            offer_match=0.25,
            proof=0.0,
            cta="Create a focused landing page",
            missing_elements=["URL/content not supplied", "proof", "specific CTA", "constraint handling"],
            recommended_changes=["Create a page that mirrors the Buyer Moment language.", "Add verifiable proof and one conversion CTA."],
        )
    return LandingPageAssessment(
        client_id=client_id,
        buyer_moment_id=moment.id,
        page_id=product.id,
        status="PARTIAL",
        fit=0.55,
        message_match=0.6,
        offer_match=0.5,
        proof=0.4,
        cta="Review the relevant product page",
        missing_elements=["Dedicated message-match review", "conversion and proof data"],
        recommended_changes=["Confirm the page supports the stated constraints before launch."],
        evidence=product.evidence,
    )


def build_portfolio(client_id: str, package: BusinessEvidencePackage) -> tuple[list[Any], ExperimentPortfolio]:
    moments = discover_package_moments(package)
    portfolio_items: list[PortfolioItem] = []
    for moment in moments:
        product = moment.matching_products[0]
        context = _moment_context(moment, product)
        context_score = score(context, product)
        readiness = score_test_readiness(context, product, context_score)
        decision = spend_safety(context, product, context_score)
        offer = offer_fit(client_id, moment, package.business)
        landing = landing_page_fit(client_id, moment, package.business)
        risks = list(decision.reason_codes)
        if offer.fit < 0.5:
            risks.append("OFFER_FIT_WEAK")
        if landing.fit < 0.5:
            risks.append("LANDING_PAGE_FIT_WEAK")
        portfolio_items.append(PortfolioItem(
            buyer_moment=moment,
            offer_fit=offer,
            landing_page_fit=landing,
            commercial_potential=readiness.commercial_potential,
            test_readiness=readiness.test_readiness,
            evidence_strength=readiness.evidence_strength,
            ambiguity=readiness.ambiguity_score,
            spend_decision=decision.decision,
            risks=risks,
        ))
    portfolio_items.sort(key=lambda item: (item.test_readiness, item.commercial_potential, item.evidence_strength), reverse=True)
    return moments, ExperimentPortfolio(
        client_id=client_id,
        test=[item for item in portfolio_items if item.spend_decision == "TEST"],
        watch=[item for item in portfolio_items if item.spend_decision == "WATCH"],
        blocked_or_abstained=[item for item in portfolio_items if item.spend_decision in {"ABSTAIN", "BLOCK"}],
    )


def analyze_package(client: Client, package: BusinessEvidencePackage, sources: list[EvidenceSource]) -> ServiceAnalysis:
    moments, portfolio = build_portfolio(client.id, package)
    return ServiceAnalysis(client=client, evidence_sources=sources, buyer_moments=moments, portfolio=portfolio, intelligence_mode="legacy")


def package_from_sources(client: Client, sources: list[EvidenceSource]) -> BusinessEvidencePackage:
    """Create a conservative preliminary package from supplied evidence, leaving unknowns explicit."""
    evidence = [
        Evidence(id=f"{source.id}-evidence", kind="observed", text=source.text[:1800], source=source.title, source_record_id=source.id, provenance=[source.uri or source.id], confidence=0.75)
        for source in sources
    ]
    product = Product(
        id=f"{client.id}-preliminary-product",
        name=f"{client.name} offering (preliminary)",
        category=client.vertical,
        description=sources[0].text[:500] if sources else "No product description supplied.",
        evidence=evidence,
    )
    business = BusinessProfile(
        id=client.id,
        name=client.name,
        category=client.vertical,
        website=client.website,
        description=sources[0].text[:800] if sources else "No business description supplied.",
        products=[product],
        offers=[],
        evidence=evidence,
    )
    hypothesis = BusinessHypothesis(
        id=f"{client.id}-preliminary-hypothesis",
        label="Preliminary evidence-backed commercial situation",
        situation="A prospective buyer is evaluating the supplied business offering for a business problem.",
        problem="The supplied evidence does not yet identify a fully validated buying problem.",
        desired_outcome="Collect enough first-party evidence to define and review a Buyer Moment.",
        evidence_ids=[item.id for item in evidence],
        origin="observed_evidence",
    )
    return BusinessEvidencePackage(
        business=business,
        target_customer_hypotheses=[hypothesis],
        evidence_store=evidence,
        unknowns=["Buyer role, timing, budget, product claims, pricing, and campaign outcomes require confirmation."],
        data_origin="provided",
    )


def audit_measurement(client_id: str, config: dict[str, Any]) -> MeasurementAudit:
    checks = {
        "primary_conversion_defined": bool(config.get("primary_conversion")),
        "utm_parameters": bool(config.get("utm_parameters")),
        "deduplication": config.get("deduplication"),
        "crm_linkage": config.get("crm_linkage"),
        "offline_conversion_path": config.get("offline_conversion_path"),
        "revenue_or_pipeline_fields": config.get("revenue_or_pipeline_fields"),
        "conversion_lag_defined": bool(config.get("conversion_lag")),
    }
    blockers = []
    if not checks["primary_conversion_defined"]:
        blockers.append("PRIMARY_CONVERSION_MISSING")
    if checks["deduplication"] is False:
        blockers.append("DUPLICATE_EVENT_RISK")
    if checks["utm_parameters"] is False:
        blockers.append("UTM_MISSING")
    if blockers:
        status = "TRACKING_UNSAFE"
    elif all(value is True for value in checks.values()):
        status = "TRACKING_READY"
    else:
        status = "TRACKING_PARTIAL"
    return MeasurementAudit(
        client_id=client_id,
        status=status,
        primary_conversion=config.get("primary_conversion"),
        checks=checks,
        blockers=blockers,
        recommendations=["Connect CRM/pipeline outcomes before using revenue efficiency as a decision signal."] if status != "TRACKING_READY" else [],
    )


def next_best_experiment(client_id: str, item: PortfolioItem, outcomes: list[CampaignOutcome]) -> NextBestExperiment:
    matching = [outcome for outcome in outcomes if outcome.buyer_moment_id == item.buyer_moment.id]
    spend = sum(outcome.spend for outcome in matching)
    qualified = sum(outcome.qualified_conversions for outcome in matching)
    clicks = sum(outcome.clicks for outcome in matching)
    if not matching:
        recommendation = "NEW_TEST" if item.spend_decision == "TEST" else "WATCH"
        reason = "No campaign outcome exists; retain the launch-time prediction and obtain human approval before any test."
    elif qualified:
        recommendation = "SCALE"
        reason = "Qualified conversion evidence exists; scale only after human review of tracking and economics."
    elif clicks >= 20:
        recommendation = "MODIFY_OFFER" if item.offer_fit.fit < item.landing_page_fit.fit else "MODIFY_LANDING_PAGE"
        reason = "There is engagement without a qualified conversion; change one controlled variable and retest."
    else:
        recommendation = "WATCH"
        reason = "Outcome volume is too small to support a strong next action."
    return NextBestExperiment(
        client_id=client_id,
        buyer_moment_id=item.buyer_moment.id,
        recommendation=recommendation,
        reason=reason,
        evidence=item.buyer_moment.supporting_evidence,
        uncertainty=["Small samples do not establish incremental ROI.", f"Spend observed: {spend:.2f}; qualified conversions: {qualified}."],
    )


def build_client_report(client: Client, portfolio: ExperimentPortfolio, outcomes: list[CampaignOutcome], unknowns: list[str]) -> ClientReport:
    summary = f"{client.name}: {len(portfolio.test)} TEST, {len(portfolio.watch)} WATCH, and {len(portfolio.blocked_or_abstained)} blocked/abstained opportunities. Human approval is required."
    return ClientReport(
        id=f"report-{client.id}",
        client_id=client.id,
        executive_summary=summary,
        what_changed=["Initial evidence-backed commercial-context analysis created."],
        top_buyer_moments=[item.model_dump(mode="json") for item in (portfolio.test + portfolio.watch)[:5]],
        experiments=[],
        outcomes=[outcome.model_dump(mode="json") for outcome in outcomes],
        next_actions=["Review evidence and approve or reject candidates.", "Audit tracking before any paid test."],
        unknowns=unknowns,
        data_origin="synthetic" if client.id.startswith("demo-") else "provided",
    )
