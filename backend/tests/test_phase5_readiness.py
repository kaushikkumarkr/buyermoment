from buyermoment.demo import demo_businesses
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import spend_safety


def test_test_readiness_requires_immediate_evidence():
    product = demo_businesses()[0].products[0]
    ready = build_context("I need waterproof hiking shoes under $150 and can order today.")
    future = build_context("I might buy waterproof hiking shoes next year.")
    ready_decision = spend_safety(ready, product, score(ready, product))
    future_decision = spend_safety(future, product, score(future, product))
    assert ready_decision.decision == "TEST"
    assert future_decision.decision != "TEST"
    assert ready_decision.test_readiness > future_decision.test_readiness


def test_readiness_exposes_evidence_and_ambiguity():
    product = demo_businesses()[0].products[0]
    context = build_context("I am researching waterproof hiking shoes for a market report.")
    decision = spend_safety(context, product, score(context, product))
    assert decision.decision == "ABSTAIN"
    assert decision.evidence_strength >= 0
    assert decision.ambiguity_score >= 0
    assert decision.human_approval_required is True
