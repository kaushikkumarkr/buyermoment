from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


EvidenceKind = Literal["observed", "inference", "hypothesis", "result"]
PurchaseStage = Literal["informational", "exploration", "comparison", "consideration", "transactional"]
CommercialityLevel = Literal["none", "low", "medium", "high"]
RelevanceLabel = Literal["exact", "substitute", "complement", "irrelevant", "unknown"]
SpendDecisionLabel = Literal["TEST", "WATCH", "ABSTAIN", "BLOCK"]


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    kind: EvidenceKind
    text: str = Field(min_length=1)
    source: str = Field(min_length=1)
    source_record_id: str | None = None
    provenance: list[str] = Field(default_factory=list)
    confidence: float = Field(default=1.0, ge=0, le=1)


class LocationContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    country: str | None = None
    region: str | None = None
    city: str | None = None
    language: str | None = None
    currency: str | None = None
    shipping: str | None = None
    location_specificity: Literal["unknown", "country", "region", "city"] = "unknown"


class Constraints(BaseModel):
    model_config = ConfigDict(extra="forbid")

    budget: float | None = Field(default=None, ge=0)
    currency: str | None = None
    required_features: list[str] = Field(default_factory=list)
    excluded_features: list[str] = Field(default_factory=list)
    compatibility: list[str] = Field(default_factory=list)
    timing: str | None = None
    geography: str | None = None
    shipping: str | None = None
    language: str | None = None


class CommercialContext(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    context_text: str = Field(min_length=1)
    problem: str
    desired_outcome: str
    use_case: str
    constraints: Constraints = Field(default_factory=Constraints)
    location: LocationContext = Field(default_factory=LocationContext)
    purchase_stage: PurchaseStage
    urgency: float = Field(default=0.5, ge=0, le=1)
    commerciality: float = Field(default=0.5, ge=0, le=1)
    product_category: str | None = None
    product_candidates: list[str] = Field(default_factory=list)
    product_fit: float = Field(default=0.5, ge=0, le=1)
    offer_fit: float = Field(default=0.5, ge=0, le=1)
    ad_relevance: float = Field(default=0.5, ge=0, le=1)
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0, le=1)
    source: str = "synthetic"
    provenance: list[str] = Field(default_factory=list)

    @field_validator("context_text")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return " ".join(value.split())


class Product(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    category: str
    description: str
    price: float | None = Field(default=None, ge=0)
    currency: str = "USD"
    url: str | None = None
    features: list[str] = Field(default_factory=list)
    service_regions: list[str] = Field(default_factory=list)
    available: bool | None = None
    shipping_deadline_met: bool | None = None
    evidence: list[Evidence] = Field(default_factory=list)


class Offer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    description: str
    discount_percent: float | None = Field(default=None, ge=0, le=100)
    eligibility: str | None = None
    evidence: list[Evidence] = Field(default_factory=list)


class BusinessProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    category: str
    website: str | None = None
    description: str
    products: list[Product]
    offers: list[Offer] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    model_config = ConfigDict(extra="forbid")

    commerciality: float = Field(ge=0, le=1)
    product_fit: float = Field(ge=0, le=1)
    constraint_match: float = Field(ge=0, le=1)
    location_fit: float = Field(ge=0, le=1)
    ad_relevance: float = Field(ge=0, le=1)


class ScoreResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    commerciality: float = Field(ge=0, le=1)
    product_fit: float = Field(ge=0, le=1)
    semantic_product_fit: float = Field(default=0.5, ge=0, le=1)
    constraint_match: float = Field(ge=0, le=1)
    location_fit: float = Field(ge=0, le=1)
    purchase_stage: PurchaseStage
    ad_relevance: float = Field(ge=0, le=1)
    commercial_actionability: float = Field(default=0.5, ge=0, le=1)
    offer_fit: float = Field(default=0.7, ge=0, le=1)
    confidence: float = Field(ge=0, le=1)
    raw_confidence: float | None = Field(default=None, ge=0, le=1)
    calibrated_confidence: float | None = Field(default=None, ge=0, le=1)
    confidence_band: Literal["LOW", "MEDIUM", "HIGH"] | None = None
    extracted_constraints: list[str] = Field(default_factory=list)
    extracted_constraint_fields: dict[str, Any] = Field(default_factory=dict)
    evidence: list[Evidence] = Field(default_factory=list)
    reason_codes: list[str] = Field(default_factory=list)
    overall: float = Field(ge=0, le=1)


class SpendDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: SpendDecisionLabel
    commercial_actionability: float = Field(ge=0, le=1)
    reason_codes: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    human_approval_required: bool = True
    policy_version: str


class BuyerMoment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    business_id: str
    title: str
    problem: str
    situation: str
    desired_outcome: str
    constraints: Constraints
    purchase_stage: PurchaseStage
    location: LocationContext
    matching_products: list[Product]
    supporting_evidence: list[Evidence]
    confidence: float = Field(ge=0, le=1)
    score: ScoreResult
    why_experiment: str


class Experiment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    buyer_moment_id: str
    hypothesis: str
    buyer_moment: BuyerMoment
    target_product: Product
    offer: Offer | None = None
    channel: str = "chatgpt_ads"
    test_budget: float = Field(default=500, ge=0)
    success_metric: str
    stop_rule: str
    creative_strategy: str
    landing_page_strategy: str
    measurement_plan: list[str]
    context_hints: list[str]
    title_candidates: list[str]
    copy_candidates: list[str]
    tracking_parameters: dict[str, str]
    qa_checklist: list[str]
    disclaimer: str = "Hypothesis only. No performance claim has been made."


class DatasetRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_dataset: str
    source_record_id: str
    source_license: str
    original_label: str | None = None
    transformation_history: list[str] = Field(default_factory=list)
    context: CommercialContext
    product: Product | None = None
    split: Literal["train", "validation", "hidden_test"]
    metadata: dict[str, Any] = Field(default_factory=dict)


class CanonicalConstraints(BaseModel):
    """Nullable canonical fields: missing source evidence stays missing."""

    model_config = ConfigDict(extra="forbid")

    budget_min: float | None = Field(default=None, ge=0)
    budget_max: float | None = Field(default=None, ge=0)
    currency: str | None = None
    required_features: list[str] = Field(default_factory=list)
    excluded_features: list[str] = Field(default_factory=list)
    compatibility: list[str] = Field(default_factory=list)
    timing: str | None = None
    geography: str | None = None
    language: str | None = None
    shipping: str | None = None


class CommercialContextRecord(BaseModel):
    """CCB-1 v0.1 canonical record for real and augmented examples."""

    model_config = ConfigDict(extra="forbid")

    record_id: str
    source_dataset: str
    source_record_id: str
    source_license: str
    source_version: str | None = None
    context_text: str = Field(min_length=1)
    original_query: str | None = None
    product_id: str | None = None
    product_title: str | None = None
    product_description: str | None = None
    product_attributes: dict[str, Any] = Field(default_factory=dict)
    problem: str | None = None
    desired_outcome: str | None = None
    use_case: str | None = None
    constraints: CanonicalConstraints = Field(default_factory=CanonicalConstraints)
    purchase_stage: PurchaseStage | None = None
    commerciality: CommercialityLevel | None = None
    relevance: RelevanceLabel | None = None
    product_fit: float | None = Field(default=None, ge=0, le=1)
    constraint_match: float | None = Field(default=None, ge=0, le=1)
    ad_relevance: float | None = Field(default=None, ge=0, le=1)
    location: LocationContext = Field(default_factory=LocationContext)
    evidence: list[Evidence] = Field(default_factory=list)
    provenance: list[str] = Field(default_factory=list)
    transformation_history: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0, le=1)
    split: Literal["train", "validation", "hidden_test", "unassigned"] = "unassigned"
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("context_text")
    @classmethod
    def normalize_context_text(cls, value: str) -> str:
        return " ".join(value.split())
