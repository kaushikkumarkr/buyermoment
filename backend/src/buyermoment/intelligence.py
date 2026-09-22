from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .models import CommercialContext, Product


IntelligenceMode = Literal["legacy", "hybrid_v1"]


@dataclass(frozen=True)
class RouteDecision:
    mode: IntelligenceMode
    product_fit_backend: str
    evidence_backend: str
    llm_escalated: bool
    reasons: tuple[str, ...]


class IntelligenceRouter:
    """Explicit feature-flagged router; candidate modules never override policy."""

    def __init__(self, mode: IntelligenceMode = "legacy") -> None:
        self.mode = mode

    def route(self, context: CommercialContext, product: Product) -> RouteDecision:
        reasons: list[str] = []
        if self.mode == "legacy":
            return RouteDecision("legacy", "legacy_contextfit", "legacy_evidence", False, ("LEGACY_MODE",))
        if context.confidence < 0.55:
            reasons.append("LOW_CONTEXT_CONFIDENCE")
        if not context.evidence or not product.evidence:
            reasons.append("MISSING_EVIDENCE")
        if context.purchase_stage in {"exploration", "informational"}:
            reasons.append("SEMANTIC_AMBIGUITY")
        escalate = bool(reasons)
        return RouteDecision(
            "hybrid_v1",
            "candidate_product_fit_then_legacy_fallback",
            "deterministic_grounding_then_review",
            escalate,
            tuple(reasons) or ("CLEAR_LOCAL_ROUTE",),
        )
