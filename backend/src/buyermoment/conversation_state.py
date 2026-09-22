from __future__ import annotations

import re

from .models import CommercialContext, ConversationState, Evidence, LocationContext, Product, ScoreResult, SpendDecision
from .scoring import build_context, infer_stage_with_history, score
from .spend_safety import spend_safety


PRODUCT_TERMS = ("crm", "accounting software", "hiking shoes", "running shoes", "work shoes", "skincare", "backpack", "analytics", "support software")
LOCATION_TERMS = ("canada", "canadian", "united states", "u.s.", "us", "texas", "california", "boston", "nevada", "new york")
TIMING_TERMS = ("today", "now", "tomorrow", "this week", "this month", "by friday", "next month", "next quarter", "next year", "later", "someday")


def _match_budget(text: str) -> float | None:
    match = re.search(r"(?:under|below|less than|budget(?: is| of)?|at most)\s*\$?\s*(\d+(?:\.\d+)?)", text.lower())
    return float(match.group(1)) if match else None


def _latest_location(text: str) -> str | None:
    lowered = text.lower()
    for location in LOCATION_TERMS:
        if location in {"us", "u.s.", "united states"} and ("us-only" in lowered or "us only" in lowered):
            continue
        if re.search(rf"\b{re.escape(location)}\b", lowered):
            return "United States" if location in {"us", "u.s.", "united states"} else ("Canada" if location == "canadian" else location.title())
    return None


def _latest_recipient(text: str) -> str | None:
    lowered = text.lower()
    if "not for me" in lowered or "for my client" in lowered or "client report" in lowered or "market report" in lowered or "not procurement" in lowered:
        return "client"
    match = re.search(r"for my (mother|father|child|brother|sister|employer|team|company)", lowered)
    if match:
        return match.group(1)
    if re.search(r"\b(for myself|for me)\b", lowered):
        return "self"
    return None


def _latest_product(text: str) -> str | None:
    lowered = text.lower()
    if "accounting software" in lowered:
        return "accounting software"
    negative = re.search(r"(?:not|instead of)\s+(?:a\s+)?(crm|accounting software|hiking shoes|running shoes|skincare|backpack)", lowered)
    if negative:
        return f"NOT:{negative.group(1)}"
    for product in PRODUCT_TERMS:
        if product in lowered:
            return product
    return None


def _latest_timing(text: str) -> str | None:
    lowered = text.lower()
    for term in TIMING_TERMS:
        if term in lowered:
            return term
    return None


def update_conversation_state(previous: ConversationState | None, text: str, *, conversation_id: str, turn_id: int) -> ConversationState:
    previous_stage = previous.current_purchase_stage if previous else None
    stage = infer_stage_with_history(text, previous_stage)
    lowered = text.lower()
    active = dict(previous.active_constraints) if previous else {}
    resolved = list(previous.resolved_constraints) if previous else []
    reasons: list[str] = []
    budget = _match_budget(text)
    if budget is not None:
        if "budget" in active and active["budget"] != budget:
            resolved.append(f"budget:{active['budget']}")
            reasons.append("LATEST_BUDGET_OVERRIDES_PRIOR")
        active["budget"] = budget
    location = _latest_location(text)
    prior_location = previous.location.country if previous else None
    if location:
        if prior_location and prior_location.lower() != location.lower():
            resolved.append(f"location:{prior_location}")
            reasons.append("LATEST_LOCATION_OVERRIDES_PRIOR")
        active["location"] = location
    recipient = _latest_recipient(text) or (previous.recipient if previous else None)
    prior_recipient = previous.recipient if previous else None
    if recipient and prior_recipient and recipient != prior_recipient:
        resolved.append(f"recipient:{prior_recipient}")
        reasons.append("LATEST_RECIPIENT_OVERRIDES_PRIOR")
    product = _latest_product(text)
    products = list(previous.current_product_interest) if previous else []
    if product and product.startswith("NOT:"):
        removed = product[4:]
        if removed in products:
            products.remove(removed)
            resolved.append(f"product:{removed}")
        reasons.append("LATEST_PRODUCT_NEGATION")
    elif product:
        if products and product not in products:
            resolved.extend(f"product:{item}" for item in products)
            reasons.append("LATEST_PRODUCT_OVERRIDES_PRIOR")
        products = [product]
    timing = _latest_timing(text) or (previous.purchase_timing if previous else None)
    if previous and timing and previous.purchase_timing and timing != previous.purchase_timing:
        reasons.append("LATEST_TIMING_OVERRIDES_PRIOR")
    if any(term in lowered for term in ("research", "market report", "for a paper", "not buying", "not purchasing")):
        reasons.append("RESEARCH_CONTEXT_REVISES_ACTIONABILITY")
    if any(term in lowered for term in ("already bought", "already purchased", "cancelled", "canceled", "return")):
        reasons.append("OWNERSHIP_OR_CANCELLATION_REVISES_ACTIONABILITY")
    negative_actionability = ("might", "maybe", "if ", "not buying", "not buy", "will not buy", "cancelled", "canceled", "return", "already bought", "already purchased", "do not recommend", "do not treat", "no new purchase", "no purchase", "only comparing", "gathering options")
    if any(term in lowered for term in ("buy", "order", "purchase", "checkout", "ready to")) and not any(term in lowered for term in negative_actionability):
        commerciality = max(previous.commerciality if previous else 0.5, 0.85)
    elif reasons and any("ACTIONABILITY" in reason for reason in reasons):
        commerciality = min(previous.commerciality if previous else 0.5, 0.2)
    else:
        commerciality = previous.commerciality if previous else 0.5
    if any(term in lowered for term in ("might", "maybe", "if ", "next quarter", "next year", "later", "someday", "no purchase date", "not buying", "not buy", "will not buy")):
        commerciality = min(commerciality, 0.2)
    if any(term in lowered for term in ("not buying", "not purchasing", "not buy", "will not buy", "only researching", "market report", "for a paper", "already bought", "already purchased", "cancelled", "canceled")):
        commerciality = min(commerciality, 0.15)
    country = active.get("location") or (previous.location.country if previous else None)
    evidence = [Evidence(id=f"{conversation_id}:{turn_id}:state", kind="inference", text=text, source="conversation_state", source_record_id=conversation_id, provenance=reasons or ["current_turn_evidence"], confidence=0.9)]
    return ConversationState(
        conversation_id=conversation_id,
        turn_id=turn_id,
        current_purchase_stage=stage,
        active_constraints=active,
        resolved_constraints=resolved,
        buyer_identity="self" if recipient == "self" else (previous.buyer_identity if previous else None),
        recipient=recipient,
        location=LocationContext(country=country, location_specificity="country" if country else "unknown"),
        purchase_timing=timing,
        current_product_interest=products,
        commerciality=commerciality,
        state_revision_reason=";".join(reasons) if reasons else "current_turn_confirmed_prior_state",
        evidence=evidence,
        provenance=["Phase 6 deterministic state revision", "latest explicit turn takes precedence"],
    )


def score_with_state(state: ConversationState, text: str, product: Product) -> tuple[CommercialContext, ScoreResult, SpendDecision]:
    summary = [text]
    if state.current_product_interest:
        summary.append("Current product: " + ", ".join(state.current_product_interest))
    if state.recipient:
        summary.append(f"Recipient: {state.recipient}")
    if state.location.country:
        summary.append(f"Current location: {state.location.country}")
    if "budget" in state.active_constraints:
        summary.append(f"Latest budget: ${state.active_constraints['budget']}")
    if state.purchase_timing:
        summary.append(f"Latest timing: {state.purchase_timing}")
    if state.commerciality <= 0.2:
        summary.append("Current state is non-actionable research, ownership, or cancellation context.")
    context = build_context(" ".join(summary), source="phase6_stateful", context_id=state.conversation_id).model_copy(update={"location": state.location})
    base_result = score(context, product)
    result = base_result.model_copy(update={"purchase_stage": state.current_purchase_stage, "commerciality": min(base_result.commerciality, state.commerciality)})
    decision = spend_safety(context, product, result)
    return context, result, decision
