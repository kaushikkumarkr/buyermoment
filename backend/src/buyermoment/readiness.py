from __future__ import annotations

import re

from .models import CommercialContext, Product, ScoreResult, TestReadiness


IMMEDIATE_TERMS = ("today", "now", "this week", "this month", "tomorrow", "by friday", "ready to order", "checkout", "buy", "order", "purchase", "start")
FUTURE_TERMS = ("might", "maybe", "if i", "if we", "next year", "next quarter", "later", "one day", "when we move", "until finance")
AMBIGUITY_TERMS = ("hypothetically", "if money were no object", "would that", "that work", "research", "paper", "article", "market report", "gathering options", "not buying", "not because i need to buy")
EXPLICIT_CONSTRAINT_TERMS = ("under ", "budget", "in ", "near ", "ships", "arrive", "size ", "compatible", "need ", "requires", "must ", "without ", "not ")


def _has_any(text: str, terms: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def _evidence_strength(context: CommercialContext, product: Product) -> float:
    evidence = [*context.evidence, *product.evidence]
    observed = [item for item in evidence if item.kind == "observed"]
    sources = {item.source for item in observed}
    direct_user = 1.0 if context.context_text.strip() else 0.0
    explicit_constraints = sum(term in context.context_text.lower() for term in EXPLICIT_CONSTRAINT_TERMS)
    constraint_signal = min(1.0, explicit_constraints / 3)
    source_diversity = min(1.0, len(sources) / 2)
    direct_observation = min(1.0, len(observed) / 3)
    first_party = 1.0 if any(item.source in {"demo_catalog", "demo business evidence", "business_evidence", "first_party_catalog"} for item in observed) else 0.35
    return min(1.0, 0.20 * direct_user + 0.25 * constraint_signal + 0.20 * source_diversity + 0.20 * direct_observation + 0.15 * first_party)


def _ambiguity(context: CommercialContext, product: Product, score: ScoreResult) -> float:
    text = context.context_text.lower()
    penalties = 0.0
    penalties += 0.45 if _has_any(text, AMBIGUITY_TERMS) else 0.0
    penalties += 0.25 if _has_any(text, FUTURE_TERMS) else 0.0
    mixed_intent = ("research" in text and any(term in text for term in ("buy", "order", "purchase"))) or ("compare" in text and "research" in text)
    penalties += 0.20 if mixed_intent else 0.0
    product_referred = product.name.lower() in text or product.category.lower() in text or any(feature.lower() in text for feature in product.features)
    penalties += 0.20 if re.search(r"\b(that|it|they|them)\b", text) and not product_referred else 0.0
    if any(term in text for term in ("for my mother", "for my father", "for my child", "for my sister", "for my brother", "not for me")):
        penalties += 0.05 if _has_any(text, ("buy", "order", "purchase", "gift", "ready to")) else 0.25
    penalties += 0.20 if score.location_fit < 0.5 else 0.0
    penalties += 0.15 if context.constraints.budget is None and product.price is None else 0.0
    return min(1.0, penalties)


def score_test_readiness(context: CommercialContext, product: Product, score: ScoreResult) -> TestReadiness:
    evidence_strength = _evidence_strength(context, product)
    ambiguity_score = _ambiguity(context, product, score)
    immediate_signal = 0.95 if _has_any(context.context_text, IMMEDIATE_TERMS) else 0.45
    stage_signal = {
        "transactional": 1.0,
        "consideration": 0.82,
        "comparison": 0.74,
        "exploration": 0.42,
        "informational": 0.08,
    }[score.purchase_stage]
    commercial_potential = min(1.0, 0.60 * score.commerciality + 0.25 * score.product_fit + 0.15 * score.constraint_match)
    readiness = (
        0.20 * immediate_signal
        + 0.20 * stage_signal
        + 0.20 * score.product_fit
        + 0.15 * score.constraint_match
        + 0.10 * score.location_fit
        + 0.15 * evidence_strength
        - 0.25 * ambiguity_score
    )
    return TestReadiness(
        commercial_potential=commercial_potential,
        test_readiness=max(0.0, min(1.0, readiness)),
        purchase_immediacy=immediate_signal,
        evidence_strength=evidence_strength,
        ambiguity_score=ambiguity_score,
        reason_codes=[
            "EXPLICIT_IMMEDIATE_SIGNAL" if immediate_signal >= 0.9 else "NO_EXPLICIT_IMMEDIATE_SIGNAL",
            "EVIDENCE_STRENGTH_HIGH" if evidence_strength >= 0.65 else "EVIDENCE_STRENGTH_LIMITED",
            "AMBIGUITY_HIGH" if ambiguity_score >= 0.4 else "AMBIGUITY_CONTROLLED",
        ],
        evidence=[*context.evidence, *product.evidence],
    )
