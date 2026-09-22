from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .models import Evidence


GroundingLabel = Literal["SUPPORTED", "PARTIAL", "UNSUPPORTED"]


class EvidenceGroundingAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: GroundingLabel
    raw_score: float = Field(ge=0, le=1)
    matched_terms: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    reason_codes: list[str] = Field(default_factory=list)
    method: str = "deterministic_token_support_v1"


def _tokens(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9][a-z0-9-]+", text.lower()) if len(token) > 2}


def assess_claim(claim: str, evidence: list[Evidence]) -> EvidenceGroundingAssessment:
    """Conservative lexical support check; semantic ambiguity must escalate to a model."""
    claim_tokens = _tokens(claim)
    if not claim_tokens or not evidence:
        return EvidenceGroundingAssessment(label="UNSUPPORTED", raw_score=0.0, reason_codes=["NO_EVIDENCE"])
    matched: set[str] = set()
    evidence_ids: list[str] = []
    for item in evidence:
        overlap = claim_tokens & _tokens(item.text)
        if overlap:
            matched.update(overlap)
            evidence_ids.append(item.id)
    score = len(matched) / len(claim_tokens)
    if score >= 0.8:
        label: GroundingLabel = "SUPPORTED"
        reason = "DIRECT_TERM_SUPPORT"
    elif score >= 0.35:
        label = "PARTIAL"
        reason = "PARTIAL_TERM_SUPPORT"
    else:
        label = "UNSUPPORTED"
        reason = "INSUFFICIENT_TERM_SUPPORT"
    return EvidenceGroundingAssessment(label=label, raw_score=score, matched_terms=sorted(matched), evidence_ids=evidence_ids, reason_codes=[reason])
