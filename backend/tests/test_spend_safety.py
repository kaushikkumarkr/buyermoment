from buyermoment.demo import demo_businesses
from buyermoment.models import Evidence, Product
from buyermoment.scoring import build_context, score
from buyermoment.spend_safety import spend_safety


def test_support_and_research_do_not_become_spend_recommendations():
    product = demo_businesses()[0].products[0]
    support_context = build_context("I already bought these shoes. How do I clean them?")
    research_context = build_context("I am researching waterproof hiking shoes for a paper, not buying.")
    assert spend_safety(support_context, product, score(support_context, product)).decision == "BLOCK"
    assert spend_safety(research_context, product, score(research_context, product)).decision == "ABSTAIN"


def test_policy_blocks_known_serviceability_and_budget_failures():
    product = Product(
        id="controlled",
        name="controlled product",
        category="shoes",
        description="waterproof hiking shoes",
        price=120,
        service_regions=["US"],
        evidence=[Evidence(id="catalog-1", kind="observed", text="Catalog evidence", source="test")],
    )
    budget = build_context("I need waterproof hiking shoes under $50 in the US.")
    location = build_context("I need waterproof hiking shoes in Canada.")
    assert spend_safety(budget, product, score(budget, product)).decision == "BLOCK"
    assert spend_safety(location, product, score(location, product)).decision == "BLOCK"


def test_every_spend_decision_requires_human_approval():
    product = demo_businesses()[0].products[0]
    context = build_context("I need waterproof hiking shoes under $150.")
    decision = spend_safety(context, product, score(context, product))
    assert decision.human_approval_required is True
