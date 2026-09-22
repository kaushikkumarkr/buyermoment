from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .models import BuyerMoment, Evidence


def service_now() -> datetime:
    return datetime.now(timezone.utc)


class Client(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(min_length=1, max_length=200)
    website: str | None = None
    vertical: str = "B2B SaaS"
    status: Literal["PROSPECT", "ONBOARDING", "ACTIVE", "PAUSED", "ARCHIVED"] = "ONBOARDING"
    created_at: datetime = Field(default_factory=service_now)
    provenance: dict[str, Any] = Field(default_factory=dict)


class EvidenceSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    client_id: str
    source_type: Literal["website", "html", "txt", "markdown", "csv", "json", "pdf", "docx", "crm", "ads_export", "reviews", "provided", "synthetic"]
    title: str = Field(min_length=1)
    uri: str | None = None
    text: str = Field(min_length=1)
    retrieved_at: datetime = Field(default_factory=service_now)
    source_timestamp: datetime | None = None
    data_origin: Literal["provided", "public", "synthetic", "real_campaign", "human_review"] = "provided"
    private: bool = True
    prompt_injection_flags: list[str] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)


class EvidenceChunk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    client_id: str
    source_id: str
    ordinal: int = Field(ge=0)
    text: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class OfferFitAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_id: str
    buyer_moment_id: str
    offer_id: str | None = None
    fit: float = Field(ge=0, le=1)
    recommendation: str
    cta: str
    evidence: list[Evidence] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    observed_or_inferred: Literal["observed", "inferred", "hypothesis"] = "inferred"


class LandingPageAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_id: str
    buyer_moment_id: str
    page_id: str | None = None
    status: Literal["FIT", "PARTIAL", "NEW_LANDING_PAGE_RECOMMENDED", "UNKNOWN"]
    fit: float = Field(ge=0, le=1)
    message_match: float = Field(ge=0, le=1)
    offer_match: float = Field(ge=0, le=1)
    proof: float = Field(ge=0, le=1)
    cta: str
    missing_elements: list[str] = Field(default_factory=list)
    recommended_changes: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)


class MeasurementAudit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_id: str
    status: Literal["TRACKING_READY", "TRACKING_PARTIAL", "TRACKING_UNSAFE"]
    primary_conversion: str | None = None
    checks: dict[str, bool | None] = Field(default_factory=dict)
    blockers: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)


class PortfolioItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    buyer_moment: BuyerMoment
    offer_fit: OfferFitAssessment
    landing_page_fit: LandingPageAssessment
    commercial_potential: float = Field(ge=0, le=1)
    test_readiness: float = Field(ge=0, le=1)
    evidence_strength: float = Field(ge=0, le=1)
    ambiguity: float = Field(ge=0, le=1)
    spend_decision: Literal["TEST", "WATCH", "ABSTAIN", "BLOCK"]
    risks: list[str] = Field(default_factory=list)


class ExperimentPortfolio(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_id: str
    generated_at: datetime = Field(default_factory=service_now)
    test: list[PortfolioItem] = Field(default_factory=list)
    watch: list[PortfolioItem] = Field(default_factory=list)
    blocked_or_abstained: list[PortfolioItem] = Field(default_factory=list)
    human_approval_required: bool = True


class HumanApproval(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    client_id: str
    object_type: Literal["buyer_moment", "experiment", "campaign", "outcome_import"]
    object_id: str
    approved: bool = False
    approved_by: str | None = None
    approved_at: datetime | None = None
    notes: str = ""


class DesignPartnerFeedbackV2(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    client_id: str
    buyer_moment_id: str | None = None
    known_before: Literal["yes", "no", "unknown"] = "unknown"
    commercially_relevant: Literal["yes", "maybe", "no"]
    would_test: Literal["yes", "maybe", "no"]
    offer_appropriate: Literal["yes", "maybe", "no"]
    evidence_credible: Literal["yes", "maybe", "no"]
    would_use_again: Literal["yes", "maybe", "no"]
    would_pay: Literal["yes", "maybe", "no"]
    reviewer_confidence: Literal["low", "medium", "high"] = "medium"
    notes: str = ""
    submitted_at: datetime = Field(default_factory=service_now)


class NextBestExperiment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_id: str
    buyer_moment_id: str
    recommendation: Literal["SCALE", "RETEST", "MODIFY_OFFER", "MODIFY_LANDING_PAGE", "WATCH", "STOP", "NEW_TEST"]
    reason: str
    evidence: list[Evidence] = Field(default_factory=list)
    uncertainty: list[str] = Field(default_factory=list)
    human_approval_required: bool = True


class ClientReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    client_id: str
    generated_at: datetime = Field(default_factory=service_now)
    executive_summary: str
    what_changed: list[str] = Field(default_factory=list)
    top_buyer_moments: list[dict[str, Any]] = Field(default_factory=list)
    experiments: list[dict[str, Any]] = Field(default_factory=list)
    outcomes: list[dict[str, Any]] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    data_origin: Literal["synthetic", "provided", "real_campaign"] = "provided"


class AnalysisRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    client_id: str
    status: Literal["SUCCEEDED", "FAILED"]
    duration_ms: int = Field(ge=0)
    retrieval_calls: int = Field(default=0, ge=0)
    llm_calls: int = Field(default=0, ge=0)
    tokens: int | None = Field(default=None, ge=0)
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=service_now)


class ServiceAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client: Client
    evidence_sources: list[EvidenceSource] = Field(default_factory=list)
    buyer_moments: list[BuyerMoment] = Field(default_factory=list)
    portfolio: ExperimentPortfolio
    measurement_audit: MeasurementAudit | None = None
    generated_at: datetime = Field(default_factory=service_now)
    intelligence_mode: Literal["legacy", "hybrid_v1"] = "legacy"
    human_approval_required: bool = True
