from __future__ import annotations

import re
from dataclasses import dataclass

from .models import CommercialContext, Constraints, Evidence, Product, ScoreResult


STAGE_TERMS: dict[str, tuple[str, ...]] = {
    "transactional": ("buy", "order", "purchase", "checkout", "ship", "today", "need by"),
    "consideration": ("best", "recommend", "under $", "worth", "looking for", "need"),
    "comparison": ("compare", "versus", "vs", "difference", "alternative"),
    "exploration": ("options", "ideas", "what should", "explore", "looking into"),
    "informational": ("history", "how does", "research", "academic", "learn", "clean"),
}


@dataclass(frozen=True)
class ParsedConstraints:
    budget: float | None
    required: list[str]
    geography: str | None
    timing: str | None


def _parse_constraints(text: str) -> ParsedConstraints:
    lowered = text.lower()
    match = re.search(r"(?:under|below|less than|budget of)\s*\$?\s*(\d+(?:\.\d+)?)", lowered)
    budget = float(match.group(1)) if match else None
    geo_match = re.search(r"\b(?:in|near|around|for)\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*)", text)
    geography = geo_match.group(1) if geo_match else None
    timing = next((term for term in ("today", "this week", "tomorrow", "before Friday") if term in lowered), None)
    required = []
    for feature in ("waterproof", "slip-resistant", "fragrance-free", "sensitive skin", "12-hour", "SOC 2", "fast shipping"):
        if feature in lowered:
            required.append(feature)
    return ParsedConstraints(budget, required, geography, timing)


def infer_stage(text: str) -> str:
    lowered = text.lower()
    for stage in ("transactional", "consideration", "comparison", "exploration", "informational"):
        if any(term in lowered for term in STAGE_TERMS[stage]):
            return stage
    return "exploration"


def build_context(context_text: str, *, source: str = "user_input", context_id: str = "ctx-generated") -> CommercialContext:
    parsed = _parse_constraints(context_text)
    stage = infer_stage(context_text)
    commerciality = {"transactional": 0.96, "consideration": 0.84, "comparison": 0.76, "exploration": 0.49, "informational": 0.18}[stage]
    urgency = 0.88 if parsed.timing else (0.65 if stage in ("transactional", "consideration") else 0.3)
    evidence = [Evidence(id=f"{context_id}-text", kind="observed", text=context_text, source=source, confidence=1.0)]
    return CommercialContext(
        id=context_id,
        context_text=context_text,
        problem="Need inferred from customer language; verify against source evidence.",
        desired_outcome="Find a suitable solution with the stated constraints.",
        use_case="Customer context supplied for scoring.",
        constraints=Constraints(budget=parsed.budget, required_features=parsed.required, geography=parsed.geography, timing=parsed.timing),
        purchase_stage=stage,
        urgency=urgency,
        commerciality=commerciality,
        evidence=evidence,
        confidence=0.65 if parsed.required or parsed.budget or parsed.geography else 0.48,
        source=source,
        provenance=["deterministic lexical stage and constraint extraction"],
    )


def _token_set(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9-]+", text.lower()) if len(token) > 2}


def _location_fit(context: CommercialContext, product: Product) -> float:
    if not context.location.country and not context.constraints.geography:
        return 0.72
    query_location = (context.location.country or context.constraints.geography or "").lower()
    if not product.service_regions:
        return 0.5
    return 1.0 if any(region.lower() in query_location or query_location in region.lower() for region in product.service_regions) else 0.2


def score(context: CommercialContext, product: Product, offer_fit: float = 0.7) -> ScoreResult:
    context_tokens = _token_set(" ".join([context.context_text, context.problem, context.desired_outcome, *context.constraints.required_features]))
    product_tokens = _token_set(" ".join([product.name, product.category, product.description, *product.features]))
    overlap = len(context_tokens & product_tokens) / max(1, len(context_tokens))
    feature_hits = sum(1 for feature in context.constraints.required_features if feature.lower() in " ".join(product.features).lower())
    feature_score = feature_hits / len(context.constraints.required_features) if context.constraints.required_features else 0.65
    budget_score = 1.0 if context.constraints.budget is None or product.price is None else max(0.0, min(1.0, context.constraints.budget / product.price))
    constraint_match = (feature_score * 0.6) + (budget_score * 0.4)
    product_fit = min(1.0, 0.3 + (overlap * 0.7))
    location_fit = _location_fit(context, product)
    ad_relevance = max(0.0, min(1.0, context.commerciality * 0.6 + context.urgency * 0.25 + offer_fit * 0.15))
    confidence = min(1.0, 0.35 + context.confidence * 0.4 + min(overlap, 0.4) + (0.1 if context.constraints.required_features else 0))
    reasons = []
    if context.constraints.budget is not None:
        reasons.append("BUDGET_MATCH" if budget_score >= 0.95 else "BUDGET_TENSION")
    if context.constraints.required_features:
        reasons.append("FEATURE_MATCH" if feature_score >= 0.75 else "FEATURE_GAP")
    if location_fit < 0.5:
        reasons.append("SERVICEABILITY_UNCONFIRMED")
    if context.purchase_stage in ("transactional", "consideration"):
        reasons.append("BUYING_LANGUAGE")
    if context.purchase_stage == "informational":
        reasons.append("NON_COMMERCIAL_INTENT")
    evidence = [*context.evidence, *product.evidence]
    overall = min(1.0, commerciality_weight(context) * 0.3 + product_fit * 0.25 + constraint_match * 0.2 + location_fit * 0.1 + ad_relevance * 0.15)
    return ScoreResult(
        commerciality=context.commerciality,
        product_fit=product_fit,
        constraint_match=constraint_match,
        location_fit=location_fit,
        purchase_stage=context.purchase_stage,
        ad_relevance=ad_relevance,
        confidence=confidence,
        extracted_constraints=[feature for feature in context.constraints.required_features if feature],
        evidence=evidence,
        reason_codes=reasons,
        overall=overall,
    )


def commerciality_weight(context: CommercialContext) -> float:
    return context.commerciality
