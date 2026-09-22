from __future__ import annotations

from typing import Any

from .commercial import AdExperiment
from .models import BuyerMoment, BusinessProfile
from .service_models import PortfolioItem


def chatgpt_ads_plan(experiment: AdExperiment) -> dict[str, Any]:
    """Official-workflow-compatible plan; campaign creation remains manual/approval-gated."""
    return {
        "platform": "chatgpt_ads",
        "workflow": "Ads Manager manual or documented bulk upload",
        "private_conversation_access": False,
        "human_approval_required": True,
        "campaign": {"name": f"BM · {experiment.business_id} · {experiment.experiment_id}"},
        "ad_group": {
            "name": experiment.audience_or_context_strategy.commercial_context,
            "context_hints": experiment.audience_or_context_strategy.context_hints,
        },
        "ads": [{
            "title": experiment.creative.headline,
            "copy": experiment.creative.body,
            "call_to_action": experiment.creative.cta,
            "landing_page_url": experiment.offer.landing_page,
        }],
        "measurement": experiment.measurement.model_dump(mode="json"),
        "qa": [
            "Confirm Ads Manager account, billing, audience and policy review manually.",
            "Context hints describe situations; they are not exact-match keywords.",
            "Confirm UTMs and conversion tracking before approval.",
        ],
    }


def chatgpt_ads_bulk_row(experiment: AdExperiment) -> dict[str, Any]:
    """Neutral row mapped to the current documented bulk-upload concepts."""
    return {
        "campaign_name": f"BM · {experiment.business_id}",
        "ad_group_name": experiment.audience_or_context_strategy.commercial_context,
        "context_hints": experiment.audience_or_context_strategy.context_hints,
        "title": experiment.creative.headline,
        "copy": experiment.creative.body,
        "landing_page_url": experiment.offer.landing_page or "",
        "experiment_id": experiment.experiment_id,
        "buyer_moment_id": experiment.buyer_moment_id,
    }


def google_ai_max_plan(moment: BuyerMoment, business: BusinessProfile) -> dict[str, Any]:
    product = moment.matching_products[0] if moment.matching_products else None
    return {
        "platform": "google_ai_max",
        "status": "PLANNING_ONLY",
        "human_approval_required": True,
        "business_id": business.id,
        "buyer_moment_id": moment.id,
        "campaign_hypothesis": f"Test whether {moment.situation} creates qualified demand for {product.name if product else 'the selected offer'}.",
        "ai_max_suitability": "Review after conversion tracking and landing-page message match are verified.",
        "search_intent_strategy": [moment.situation, moment.problem, moment.desired_outcome],
        "landing_page_url_strategy": product.url if product else None,
        "brand_controls": ["Confirm brand inclusions/exclusions with the account owner."],
        "url_controls": ["Limit expansion to approved product and conversion pages until evidence supports broader coverage."],
        "negative_or_exclusion_considerations": ["Exclude support, research-only, employment, and incompatible geography contexts where identifiable."],
        "conversion_goal": "qualified_lead_or_client-defined_primary_conversion",
        "value_signal": "pipeline_or_revenue_when_available; do not substitute vanity metrics",
        "experiment_recommendation": "Use a controlled campaign experiment or matched pre/post design with manual review.",
        "measurement_requirements": ["UTMs", "deduplicated conversion event", "CRM linkage", "offline conversion path where available"],
        "disclaimer": "Google controls auction delivery and optimization; BuyerMoment supplies the commercial hypothesis.",
    }


def portfolio_plan(item: PortfolioItem, business: BusinessProfile, experiment: AdExperiment) -> dict[str, Any]:
    return {
        "buyer_moment_id": item.buyer_moment.id,
        "chatgpt_ads": chatgpt_ads_plan(experiment),
        "google_ai_max": google_ai_max_plan(item.buyer_moment, business),
    }
