from buyermoment.scoring import build_context, score
from buyermoment.demo import demo_businesses


def test_purchase_stage_distinguishes_buying_from_research():
    buying = build_context("I need waterproof hiking boots under $150 for Yellowstone.")
    research = build_context("I'm researching the history of waterproof hiking boots.")
    support = build_context("How do I clean the waterproof boots I already own?")
    assert buying.purchase_stage == "consideration"
    assert research.purchase_stage == "informational"
    assert support.purchase_stage == "informational"
    assert buying.commerciality > research.commerciality


def test_constraints_and_score_are_explainable():
    business = demo_businesses()[0]
    context = build_context("I need waterproof hiking boots under $150 for Yellowstone.")
    result = score(context, business.products[0])
    assert result.constraint_match > 0.5
    assert "BUDGET_MATCH" in result.reason_codes
    assert result.evidence
    assert all(item.kind in {"observed", "inference", "hypothesis", "result"} for item in result.evidence)

