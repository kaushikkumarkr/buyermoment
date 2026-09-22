from buyermoment.conversation_state import update_conversation_state


def test_latest_explicit_constraints_override_prior_state():
    state = None
    state = update_conversation_state(state, "I need a CRM under $500 for my US team.", conversation_id="test", turn_id=1)
    state = update_conversation_state(state, "Actually, the budget is $1000 and we are moving to Canada.", conversation_id="test", turn_id=2)
    assert state.active_constraints["budget"] == 1000
    assert state.location.country == "Canada"
    assert "LATEST_BUDGET_OVERRIDES_PRIOR" in state.state_revision_reason
    assert "LATEST_LOCATION_OVERRIDES_PRIOR" in state.state_revision_reason


def test_research_and_ownership_revise_actionability():
    state = update_conversation_state(None, "I need running shoes for myself.", conversation_id="test", turn_id=1)
    state = update_conversation_state(state, "Actually, I am researching them for a client report, not buying.", conversation_id="test", turn_id=2)
    assert state.recipient == "client"
    assert state.commerciality <= 0.2
    assert "RESEARCH_CONTEXT_REVISES_ACTIONABILITY" in state.state_revision_reason
