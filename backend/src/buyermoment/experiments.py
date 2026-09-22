from __future__ import annotations

import json

from .models import BuyerMoment, Experiment, Offer


def generate_experiment(moment: BuyerMoment, offer: Offer | None = None) -> Experiment:
    product = moment.matching_products[0]
    compact = moment.title.lower().replace(" ", "-")[:36]
    return Experiment(
        id=f"exp-{moment.id}", buyer_moment_id=moment.id,
        hypothesis=f"People in the {moment.situation.lower()} will find {product.name} relevant when the ad reflects {', '.join(moment.score.extracted_constraints) or 'their stated job to be done'}.",
        buyer_moment=moment, target_product=product, offer=offer,
        success_metric="Qualified landing-page sessions that reach the primary product CTA; campaign conversion economics remain unmeasured until live data exists.",
        stop_rule="Pause after 500 qualified sessions or 14 days if the primary CTA rate is below the pre-registered baseline; review evidence before changing the hypothesis.",
        creative_strategy="Lead with the customer situation and the verified constraint. Avoid unsupported superiority or outcome claims.",
        landing_page_strategy="Send to a focused product page that repeats the verified constraints, serviceability, price, and evidence links above the fold.",
        measurement_plan=["Attach experiment and buyer-moment IDs to every tracking event.", "Record location, product, offer, and landing-page variant.", "Separate observed campaign results from model predictions.", "Review false-positive examples before scaling."],
        context_hints=[moment.situation, *moment.score.extracted_constraints, moment.location.country or "location not specified"],
        title_candidates=[f"{product.name} for {moment.title}", f"Meet the {moment.title}", f"A fit for {moment.constraints.geography or 'your next plan'}"],
        copy_candidates=[f"{moment.desired_outcome} Explore {product.name}, with the details in view.", f"Built around {', '.join(moment.score.extracted_constraints) or 'your stated needs'}—see if {product.name} fits.", "Evidence-backed relevance is the test. Review the product details before you commit."],
        tracking_parameters={"utm_source": "chatgpt_ads", "utm_medium": "conversation", "utm_campaign": compact, "bm_buyer_moment": moment.id, "bm_experiment": f"exp-{moment.id}"},
        qa_checklist=["Verify product price and availability from current source evidence.", "Verify the offer's eligibility and geography.", "Confirm no copy implies guaranteed performance.", "Confirm tracking parameters persist through the landing page.", "Log reviewer and approval timestamp."],
    )


def export_experiment(experiment: Experiment) -> str:
    return json.dumps(experiment.model_dump(mode="json"), indent=2)

