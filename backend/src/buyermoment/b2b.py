from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .models import Evidence, PurchaseStage


B2BCategory = Literal[
    "CRM", "Sales", "Marketing Automation", "Analytics / BI", "Accounting / Finance",
    "Procurement", "Project Management", "DevOps", "Cybersecurity", "HR / Payroll",
    "Customer Support",
]
LabelQuality = Literal["GOLD", "HUMAN_REVIEWED", "SILVER", "SYNTHETIC", "PUBLIC_LABEL"]
ReviewStatus = Literal["pending", "reviewed", "rejected"]


class B2BCommercialContextRecord(BaseModel):
    """CCB-B2B record. Unknown business facts remain nullable and provenance is mandatory."""

    model_config = ConfigDict(extra="forbid")

    record_id: str
    category: B2BCategory
    context_text: str = Field(min_length=1)
    company_size: str | None = None
    industry: str | None = None
    buyer_role: str | None = None
    recipient: str | None = None
    current_stack: list[str] = Field(default_factory=list)
    current_vendor: str | None = None
    pain_point: str | None = None
    desired_outcome: str | None = None
    required_integrations: list[str] = Field(default_factory=list)
    required_features: list[str] = Field(default_factory=list)
    excluded_features: list[str] = Field(default_factory=list)
    budget: str | None = None
    contract_preference: str | None = None
    security_requirement: list[str] = Field(default_factory=list)
    compliance_requirement: list[str] = Field(default_factory=list)
    migration_need: str | None = None
    implementation_timeline: str | None = None
    purchase_timing: str | None = None
    procurement_status: str | None = None
    decision_authority: str | None = None
    geography: str | None = None
    purchase_stage: PurchaseStage
    commerciality: Literal["none", "low", "medium", "high"]
    commercial_actionability: Literal["not_actionable", "uncertain", "actionable"]
    candidate_product: str | None = None
    product_fit: float | None = Field(default=None, ge=0, le=1)
    offer_fit: float | None = Field(default=None, ge=0, le=1)
    evidence: list[Evidence] = Field(min_length=1)
    provenance: list[str] = Field(min_length=1)
    label_quality: LabelQuality
    review_status: ReviewStatus = "pending"
    confidence: float | None = Field(default=None, ge=0, le=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class B2BReviewDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str
    reviewer_id: str
    commerciality: str
    purchase_stage: PurchaseStage
    commercial_actionability: str
    product_fit: float | None = Field(default=None, ge=0, le=1)
    label_confidence: Literal["low", "medium", "high"]
    notes: str = ""
    submitted_at: str
