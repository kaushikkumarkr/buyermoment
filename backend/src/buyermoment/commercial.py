from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .models import BusinessProfile, Evidence


LifecycleStage = Literal["FORECAST", "SOLICITATION", "AWARD", "RECOMPETE_CANDIDATE"]
Platform = Literal["chatgpt_ads", "google_ai_max", "manual", "unknown"]
ExperimentStatus = Literal["DRAFT", "PENDING_APPROVAL", "APPROVED", "EXPORTED", "ACTIVE", "COMPLETED", "PAUSED"]
OutcomeQuality = Literal["unknown", "unqualified", "qualified", "revenue_attributed"]
DataOrigin = Literal["benchmark", "synthetic", "public_dataset", "human_review", "real_campaign"]
PartnerStatus = Literal["PROSPECT", "CONTACTED", "ANALYSIS_SENT", "REVIEWED", "DESIGN_PARTNER", "DECLINED", "EXPERIMENT_READY", "EXPERIMENT_ACTIVE", "COMPLETED"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AudienceOrContextStrategy(BaseModel):
    model_config = ConfigDict(extra="forbid")

    commercial_context: str = Field(min_length=1)
    context_hints: list[str] = Field(default_factory=list)
    search_terms: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ExperimentOffer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    offer_id: str | None = None
    description: str = Field(min_length=1)
    landing_page: str | None = None


class CreativeCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    headline: str = Field(min_length=1)
    body: str = Field(min_length=1)
    cta: str = Field(min_length=1)


class ExperimentBudget(BaseModel):
    model_config = ConfigDict(extra="forbid")

    planned_total: float | None = Field(default=None, ge=0)
    planned_daily: float | None = Field(default=None, ge=0)
    currency: str = "USD"


class MeasurementPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_conversion: str = Field(min_length=1)
    secondary_events: list[str] = Field(default_factory=list)
    tracking_parameters: dict[str, str] = Field(default_factory=dict)


class Approval(BaseModel):
    model_config = ConfigDict(extra="forbid")

    required: bool = True
    approved: bool = False
    approved_by: str | None = None
    approved_at: datetime | None = None


class AdExperiment(BaseModel):
    """Platform-neutral experiment plan; platform adapters own export details."""

    model_config = ConfigDict(extra="forbid")

    experiment_id: str
    business_id: str
    buyer_moment_id: str
    platform: Platform
    status: ExperimentStatus = "DRAFT"
    hypothesis: str = Field(min_length=1)
    audience_or_context_strategy: AudienceOrContextStrategy
    offer: ExperimentOffer
    creative: CreativeCandidate
    budget: ExperimentBudget = Field(default_factory=ExperimentBudget)
    measurement: MeasurementPlan
    contextfit_score: float = Field(ge=0, le=1)
    test_readiness: float = Field(ge=0, le=1)
    commercial_potential: float = Field(ge=0, le=1)
    spend_decision: Literal["TEST", "WATCH", "ABSTAIN", "BLOCK"]
    approval: Approval = Field(default_factory=Approval)
    contextfit_version: str = "phase6"
    policy_version: str = "phase5-v1"
    experiment_version: str = "1"
    provenance: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class CampaignOutcome(BaseModel):
    model_config = ConfigDict(extra="forbid")

    experiment_id: str
    buyer_moment_id: str
    platform: Platform
    date: str
    impressions: int = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)
    spend: float = Field(default=0, ge=0)
    conversions: int = Field(default=0, ge=0)
    qualified_conversions: int = Field(default=0, ge=0)
    conversion_value: float | None = Field(default=None, ge=0)
    revenue: float | None = Field(default=None, ge=0)
    campaign: str | None = None
    ad_group: str | None = None
    landing_page: str | None = None
    source: str
    import_method: Literal["manual_csv", "api", "manual_entry"]
    data_origin: DataOrigin = "real_campaign"
    provenance: dict[str, Any] = Field(default_factory=dict)


class GoogleAiMaxOutcome(BaseModel):
    """Future-ready Google AI Max/search outcome shape; no Google API client yet."""

    model_config = ConfigDict(extra="forbid")

    experiment_id: str
    buyer_moment_id: str
    date: str
    search_term: str | None = None
    headline: str | None = None
    landing_page: str | None = None
    campaign: str | None = None
    ad_group: str | None = None
    impressions: int = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)
    cost: float = Field(default=0, ge=0)
    conversions: int = Field(default=0, ge=0)
    conversion_value: float | None = Field(default=None, ge=0)
    source: str = "google_ads_export"
    data_origin: DataOrigin = "real_campaign"
    provenance: dict[str, Any] = Field(default_factory=dict)


class CommercialContextOutcome(BaseModel):
    model_config = ConfigDict(extra="forbid")

    buyer_moment_id: str
    experiment_id: str
    contextfit_prediction: float = Field(ge=0, le=1)
    test_readiness_prediction: float = Field(ge=0, le=1)
    platform: Platform
    product_id: str | None = None
    offer_id: str | None = None
    spend: float = Field(default=0, ge=0)
    clicks: int = Field(default=0, ge=0)
    conversions: int = Field(default=0, ge=0)
    qualified_conversions: int = Field(default=0, ge=0)
    revenue: float | None = Field(default=None, ge=0)
    outcome_quality: OutcomeQuality = "unknown"
    observed_at: datetime = Field(default_factory=utc_now)
    data_origin: DataOrigin = "real_campaign"
    provenance: dict[str, Any] = Field(default_factory=dict)


class DesignPartner(BaseModel):
    model_config = ConfigDict(extra="forbid")

    partner_id: str
    company: str
    website: str
    contact: str | None = None
    vertical: str = "B2B SaaS"
    status: PartnerStatus = "PROSPECT"
    analysis_created: bool = False
    meeting: bool = False
    interested: bool = False
    experiment_accepted: bool = False
    feedback: list[str] = Field(default_factory=list)
    provenance: list[str] = Field(default_factory=list)


class DesignPartnerFeedback(BaseModel):
    model_config = ConfigDict(extra="forbid")

    partner_id: str
    buyer_moment_id: str | None = None
    known_before: Literal["yes", "no", "unknown"] = "unknown"
    commercially_relevant: Literal["yes", "maybe", "no"]
    would_test: Literal["yes", "maybe", "no"]
    offer_appropriate: Literal["yes", "maybe", "no"]
    evidence_credible: Literal["yes", "maybe", "no"]
    missing: str = ""
    use_again: Literal["yes", "maybe", "no"]
    would_pay: Literal["yes", "maybe", "no"]
    acceptable_pricing: str | None = None
    notes: str = ""
    submitted_at: datetime = Field(default_factory=utc_now)


class PilotRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    source: str = "buyermoment_landing_page"
    platform: Platform = "manual"
    campaign: str | None = None
    experiment_id: str | None = None
    buyer_moment_id: str | None = None
    landing_page: str = "buyer_moment_pilot"
    conversion_type: Literal["pilot_request"] = "pilot_request"
    name: str = Field(min_length=1, max_length=200)
    work_email: str = Field(min_length=3, max_length=320)
    company: str = Field(min_length=1, max_length=200)
    website: str = Field(min_length=1, max_length=500)
    role: str = Field(min_length=1, max_length=200)
    message: str = Field(default="", max_length=2000)


class BusinessHypothesis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    label: str
    situation: str
    problem: str
    desired_outcome: str
    evidence_ids: list[str] = Field(default_factory=list)
    origin: Literal["provided_strategy", "observed_evidence", "inference"] = "provided_strategy"


class BusinessEvidencePackage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    business: BusinessProfile
    target_customer_hypotheses: list[BusinessHypothesis]
    unknowns: list[str] = Field(default_factory=list)
    evidence_store: list[Evidence] = Field(default_factory=list)
    data_origin: DataOrigin = "human_review"


class OpportunityReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    business_id: str
    business_name: str
    generated_at: datetime = Field(default_factory=utc_now)
    evidence_analyzed: int
    raw_candidate_count: int
    supported_candidate_count: int
    top_buyer_moments: list[dict[str, Any]]
    rejected_moments: list[dict[str, Any]] = Field(default_factory=list)
    evidence_gaps: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
