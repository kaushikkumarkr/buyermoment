from buyermoment.evidence_grounding import assess_claim
from buyermoment.intelligence import IntelligenceRouter
from buyermoment.models import Evidence, Product
from buyermoment.scoring import build_context


def product() -> Product:
    return Product(
        id="p1",
        name="Evidence product",
        category="software",
        description="A product with verified evidence.",
        evidence=[Evidence(id="p1:e", kind="observed", text="A product with verified evidence.", source="test")],
    )


def test_router_is_explicitly_legacy_by_default():
    context = build_context("I need a software product today.")
    decision = IntelligenceRouter().route(context, product())
    assert decision.mode == "legacy"
    assert decision.llm_escalated is False


def test_hybrid_router_marks_ambiguous_context_for_review():
    context = build_context("What should I learn about software products?").model_copy(update={"confidence": 0.4})
    decision = IntelligenceRouter("hybrid_v1").route(context, product())
    assert decision.llm_escalated is True
    assert "LOW_CONTEXT_CONFIDENCE" in decision.reasons


def test_grounding_returns_unsupported_without_evidence():
    assessment = assess_claim("This is proven.", [])
    assert assessment.label == "UNSUPPORTED"
