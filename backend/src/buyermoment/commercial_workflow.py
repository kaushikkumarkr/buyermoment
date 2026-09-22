from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .commercial import (
    AdExperiment,
    BusinessEvidencePackage,
    CampaignOutcome,
    CommercialContextOutcome,
    DesignPartnerFeedback,
    ExperimentBudget,
    ExperimentOffer,
    MeasurementPlan,
    OpportunityReport,
)
from .models import BuyerMoment, CommercialContext, Evidence
from .readiness import score_test_readiness
from .scoring import score
from .spend_safety import spend_safety


def _slug(value: str) -> str:
    return "-".join(value.lower().split())[:40]


def discover_package_moments(package: BusinessEvidencePackage) -> list[BuyerMoment]:
    """Derive candidates from supplied hypotheses and product evidence.

    Hypotheses are kept as inference evidence; the function never presents them as
    observed customer facts. Product × hypothesis combinations are deterministic and
    therefore reproducible without an inference call.
    """
    business = package.business
    moments: list[BuyerMoment] = []
    for hypothesis in package.target_customer_hypotheses:
        for product in business.products:
            evidence = [item for item in package.evidence_store if getattr(item, "id", None) in hypothesis.evidence_ids]
            context = CommercialContext(
                id=f"{business.id}-{hypothesis.id}-{product.id}",
                context_text=f"{hypothesis.situation} {hypothesis.desired_outcome}",
                problem=hypothesis.problem,
                desired_outcome=hypothesis.desired_outcome,
                use_case=hypothesis.situation,
                purchase_stage="consideration",
                urgency=0.70,
                commerciality=0.75,
                product_category=product.category,
                product_candidates=[product.id],
                confidence=0.65 if hypothesis.origin == "inference" else 0.78,
                source="business_evidence_package",
                provenance=[f"hypothesis:{hypothesis.id}", f"product:{product.id}"],
                evidence=[
                    *evidence,
                    Evidence(
                        id=f"{business.id}-{hypothesis.id}-inference",
                        kind="inference",
                        text=f"Candidate commercial situation: {hypothesis.label}",
                        source="commercial_workflow",
                        source_record_id=hypothesis.id,
                        provenance=hypothesis.evidence_ids,
                        confidence=0.65,
                    ),
                ],
            )
            result = score(context, product)
            moments.append(BuyerMoment(
                id=f"{business.id}-moment-{hypothesis.id}-{product.id}",
                business_id=business.id,
                title=f"{hypothesis.label} — {product.name}",
                problem=hypothesis.problem,
                situation=hypothesis.situation,
                desired_outcome=hypothesis.desired_outcome,
                constraints=context.constraints,
                purchase_stage=context.purchase_stage,
                location=context.location,
                matching_products=[product],
                supporting_evidence=context.evidence,
                confidence=result.confidence,
                score=result,
                why_experiment="Candidate hypothesis derived from supplied business evidence; human approval is required before any spend.",
            ))
    return sorted(moments, key=lambda item: item.score.overall, reverse=True)


def _supported(moment: BuyerMoment) -> bool:
    return any(item.kind == "observed" for item in moment.supporting_evidence) and bool(moment.matching_products)


def build_opportunity_report(package: BusinessEvidencePackage, *, top_n: int = 5) -> OpportunityReport:
    moments = discover_package_moments(package)
    supported = [item for item in moments if _supported(item)]
    rejected = [
        {"buyer_moment_id": item.id, "reason": "NO_DIRECT_OBSERVED_EVIDENCE"}
        for item in moments
        if not _supported(item)
    ]
    return OpportunityReport(
        business_id=package.business.id,
        business_name=package.business.name,
        evidence_analyzed=len(package.evidence_store),
        raw_candidate_count=len(moments),
        supported_candidate_count=len(supported),
        top_buyer_moments=[item.model_dump(mode="json") for item in supported[:top_n]],
        rejected_moments=rejected,
        evidence_gaps=package.unknowns,
        risks=["No campaign outcome evidence exists yet.", "Commercial situations are hypotheses until validated with an advertiser or campaign."],
    )


def generate_ad_experiment(moment: BuyerMoment, business_id: str, *, platform: str = "chatgpt_ads", budget: float | None = None) -> AdExperiment:
    product = moment.matching_products[0]
    context = CommercialContext(
            id=f"{moment.id}-context",
            context_text=moment.situation,
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
            source="buyer_moment",
            provenance=[moment.id],
            evidence=moment.supporting_evidence,
        )
    readiness = score_test_readiness(context, product, moment.score)
    safety = spend_safety(context, product, moment.score)
    return AdExperiment(
        experiment_id=f"adexp-{moment.id}",
        business_id=business_id,
        buyer_moment_id=moment.id,
        platform=platform,
        status="PENDING_APPROVAL",
        hypothesis=f"The situation '{moment.situation}' will respond to a context-led explanation of {product.name}.",
        audience_or_context_strategy={
            "commercial_context": moment.situation,
            "context_hints": [moment.situation, *moment.score.extracted_constraints],
            "search_terms": [],
            "notes": ["Context hints are natural situations, not exact-match keywords.", "Hypothesis only; no performance claim."],
        },
        offer=ExperimentOffer(description=f"Evaluate {product.name} against the stated situation."),
        creative={
            "headline": f"{product.name} for {moment.title}",
            "body": f"See whether {product.name} fits the problem and constraints described in this Buyer Moment.",
            "cta": "Review the fit",
        },
        budget=ExperimentBudget(planned_total=budget),
        measurement=MeasurementPlan(
            primary_conversion="pilot_request",
            secondary_events=["landing_page_view", "qualified_cta_click"],
            tracking_parameters={"bm_buyer_moment": moment.id, "bm_experiment": f"adexp-{moment.id}"},
        ),
        contextfit_score=moment.score.overall,
        test_readiness=readiness.test_readiness,
        commercial_potential=readiness.commercial_potential,
        spend_decision=safety.decision,
        contextfit_version="phase6",
        policy_version="phase5-v1",
        provenance={"buyer_moment_id": moment.id, "product_id": product.id, "evidence_ids": [item.id for item in moment.supporting_evidence], "human_approval_required": True},
    )


def chatgpt_ads_package(experiment: AdExperiment) -> dict[str, Any]:
    """Produce a documented/manual package; this is not an undocumented API client."""
    return {
        "format": "buyermoment_chatgpt_ads_hypothesis_package_v1",
        "manual_import_required": True,
        "human_approval_required": experiment.approval.required,
        "experiment": experiment.model_dump(mode="json"),
        "qa": ["Verify official platform workflow before use.", "Verify tracking persists.", "Do not infer private conversation access.", "Do not launch without recorded human approval."],
    }


def import_outcomes_csv(path: Path) -> list[CampaignOutcome]:
    """Import a neutral CSV; platform-specific columns are retained in provenance."""
    outcomes: list[CampaignOutcome] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            outcomes.append(CampaignOutcome(
                experiment_id=row["experiment_id"], buyer_moment_id=row["buyer_moment_id"], platform=row.get("platform", "manual"), date=row["date"],
                impressions=int(row.get("impressions", 0) or 0), clicks=int(row.get("clicks", 0) or 0), spend=float(row.get("spend", 0) or 0),
                conversions=int(row.get("conversions", 0) or 0), qualified_conversions=int(row.get("qualified_conversions", 0) or 0),
                conversion_value=float(row["conversion_value"]) if row.get("conversion_value") else None,
                revenue=float(row["revenue"]) if row.get("revenue") else None, campaign=row.get("campaign") or None, ad_group=row.get("ad_group") or None,
                landing_page=row.get("landing_page") or None, source=row.get("source", "manual_csv"), import_method="manual_csv",
                provenance={"file": str(path), "columns": sorted(row.keys())},
            ))
    return outcomes


def outcome_lineage(experiment: AdExperiment, outcome: CampaignOutcome) -> CommercialContextOutcome:
    if experiment.experiment_id != outcome.experiment_id or experiment.buyer_moment_id != outcome.buyer_moment_id:
        raise ValueError("Outcome does not match immutable experiment lineage")
    quality = "revenue_attributed" if outcome.revenue is not None else "qualified" if outcome.qualified_conversions else "unknown"
    return CommercialContextOutcome(
        buyer_moment_id=experiment.buyer_moment_id,
        experiment_id=experiment.experiment_id,
        contextfit_prediction=experiment.contextfit_score,
        test_readiness_prediction=experiment.test_readiness,
        platform=experiment.platform,
        product_id=experiment.provenance.get("product_id"),
        spend=outcome.spend,
        clicks=outcome.clicks,
        conversions=outcome.conversions,
        qualified_conversions=outcome.qualified_conversions,
        revenue=outcome.revenue,
        outcome_quality=quality,
        provenance={"outcome_source": outcome.source, "import_method": outcome.import_method},
    )


def feedback_from_json(path: Path) -> list[DesignPartnerFeedback]:
    data = json.loads(path.read_text())
    return [DesignPartnerFeedback.model_validate(item) for item in data]
