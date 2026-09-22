from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .models import CommercialContext, Evidence, Product, ScoreResult, SpendDecision
from .readiness import score_test_readiness


@dataclass(frozen=True)
class SpendSafetyPolicy:
    version: str = "phase5-v1"
    min_test_overall: float = 0.70
    min_test_confidence: float = 0.68
    min_test_actionability: float = 0.20
    min_watch_overall: float = 0.50
    min_watch_confidence: float = 0.50
    min_test_readiness: float = 0.75
    min_test_evidence_strength: float = 0.65
    max_test_ambiguity: float = 0.05
    require_immediate_signal: bool = True
    human_approval_required: bool = True


def load_policy(path: Path = Path("policies/spend_safety.yaml")) -> SpendSafetyPolicy:
    if not path.is_absolute() and not path.exists():
        path = Path(__file__).resolve().parents[3] / path
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if line.strip() and not line.lstrip().startswith("#") and ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return SpendSafetyPolicy(
        version=values.get("version", "phase5-v1"),
        min_test_overall=float(values.get("min_test_overall", 0.70)),
        min_test_confidence=float(values.get("min_test_confidence", 0.68)),
        min_test_actionability=float(values.get("min_test_actionability", 0.20)),
        min_watch_overall=float(values.get("min_watch_overall", 0.50)),
        min_watch_confidence=float(values.get("min_watch_confidence", 0.50)),
        min_test_readiness=float(values.get("min_test_readiness", 0.75)),
        min_test_evidence_strength=float(values.get("min_test_evidence_strength", 0.65)),
        max_test_ambiguity=float(values.get("max_test_ambiguity", 0.05)),
        require_immediate_signal=values.get("require_immediate_signal", "true").lower() == "true",
        human_approval_required=values.get("human_approval_required", "true").lower() == "true",
    )


def _explicit_location(text: str, context: CommercialContext) -> bool:
    lowered = text.lower()
    return bool(context.location.country or context.location.region or context.location.city or context.constraints.geography or re.search(r"\b(canada|united states|u\.s\.|texas|california|boston|nevada|europe|uk)\b", lowered))


def _evidence(context: CommercialContext, code: str) -> list[Evidence]:
    return [Evidence(id=f"{context.id}:{code.lower()}", kind="inference", text=context.context_text, source="spend_safety_policy", source_record_id=context.id, provenance=[code], confidence=1.0)]


def spend_safety(context: CommercialContext, product: Product, score: ScoreResult, policy: SpendSafetyPolicy | None = None) -> SpendDecision:
    policy = policy or load_policy()
    lowered = context.context_text.lower()
    readiness = score_test_readiness(context, product, score)
    reasons: list[str] = []

    def decision(
        label: str,
        reason: str,
        actionability: float,
        evidence: list[Evidence] | None = None,
    ) -> SpendDecision:
        return SpendDecision(
            decision=label,
            commercial_potential=readiness.commercial_potential,
            test_readiness=readiness.test_readiness,
            evidence_strength=readiness.evidence_strength,
            ambiguity_score=readiness.ambiguity_score,
            commercial_actionability=actionability,
            reason_codes=[reason, *readiness.reason_codes],
            evidence=evidence or readiness.evidence,
            confidence=score.confidence,
            policy_version=policy.version,
            human_approval_required=policy.human_approval_required,
        )

    if any(term in lowered for term in ("how do i clean", "how do i use", "already own", "already purchased", "export contacts", "should i return", "return these")):
        reasons.append("EXISTING_OWNER_SUPPORT")
        return decision("BLOCK", reasons[0], 0.0, _evidence(context, reasons[0]))
    if any(term in lowered for term in ("researching", "researching competitors", "evaluating competitors", "for a paper", "market report", "academic", "professional article", "not buying", "not purchase", "not purchasing", "will not purchase", "not because i need to buy", "just gathering options", "only gathering options", "understand why")):
        reasons.append("RESEARCH_ONLY")
        return decision("ABSTAIN", reasons[0], 0.0, _evidence(context, reasons[0]))
    if any(term in lowered for term in ("might", "maybe", "if i", "until next year", "one day", "could buy later")):
        reasons.append("FUTURE_OR_CONDITIONAL_INTENT")
        return decision("ABSTAIN", reasons[0], 0.0, _evidence(context, reasons[0]))
    if any(term in lowered for term in ("hate this brand", "dislike this brand", "why is my current", "so slow", "frustrating")) and "buy" not in lowered and "order" not in lowered:
        reasons.append("NEGATIVE_SENTIMENT_OR_COMPLAINT")
        return decision("ABSTAIN", reasons[0], 0.0, _evidence(context, reasons[0]))
    if "us-only" in lowered and (context.location.country or context.constraints.geography or "").lower() not in {"", "us", "usa", "united states", "u.s."}:
        reasons.append("LOCATION_UNSERVICEABLE")
        return decision("BLOCK", reasons[0], 0.0, _evidence(context, reasons[0]))
    if product.service_regions and _explicit_location(context.context_text, context) and score.location_fit < 0.5:
        reasons.append("LOCATION_UNSERVICEABLE")
        return decision("BLOCK", reasons[0], 0.0, _evidence(context, reasons[0]))
    if context.constraints.budget is not None and product.price is not None and product.price > context.constraints.budget:
        reasons.append("BUDGET_INCOMPATIBLE")
        return decision("BLOCK", reasons[0], 0.0, _evidence(context, reasons[0]))
    if product.available is False:
        reasons.append("PRODUCT_UNAVAILABLE")
        return decision("BLOCK", reasons[0], 0.0, _evidence(context, reasons[0]))
    if product.shipping_deadline_met is False or "doesn't ship" in lowered or "does not ship" in lowered:
        reasons.append("SHIPPING_UNSERVICEABLE")
        return decision("BLOCK", reasons[0], 0.0, _evidence(context, reasons[0]))
    if "only supports english" in lowered or "english only" in lowered:
        reasons.append("LANGUAGE_UNSUPPORTED")
        return decision("BLOCK", reasons[0], 0.0, _evidence(context, reasons[0]))
    if product.price is None or not product.evidence:
        reasons.append("INSUFFICIENT_EVIDENCE")
        return decision("ABSTAIN", reasons[0], score.commercial_actionability, score.evidence)
    readiness_eligible = (
        readiness.test_readiness >= policy.min_test_readiness
        and readiness.evidence_strength >= policy.min_test_evidence_strength
        and readiness.ambiguity_score <= policy.max_test_ambiguity
        and (not policy.require_immediate_signal or "EXPLICIT_IMMEDIATE_SIGNAL" in readiness.reason_codes)
        and score.purchase_stage in {"consideration", "comparison", "transactional"}
    )
    if score.overall >= policy.min_test_overall and score.confidence >= policy.min_test_confidence and score.commercial_actionability >= policy.min_test_actionability and readiness_eligible:
        reasons.append("EVIDENCE_BACKED_COMMERCIAL_CONTEXT")
        return decision("TEST", reasons[0], score.commercial_actionability, score.evidence)
    if score.overall >= policy.min_watch_overall and score.confidence >= policy.min_watch_confidence:
        reasons.append("PLAUSIBLE_BUT_UNCERTAIN")
        return decision("WATCH", reasons[0], score.commercial_actionability, score.evidence)
    reasons.append("LOW_CONFIDENCE")
    return decision("ABSTAIN", reasons[0], score.commercial_actionability, score.evidence)
