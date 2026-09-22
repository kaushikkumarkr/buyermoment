# Multi-turn state benchmark

{
  "journey_count": 96,
  "turn_count": 576,
  "baseline_stage_accuracy": 0.625,
  "stateful_stage_accuracy": 0.625,
  "baseline_transition_accuracy": 0.55,
  "stateful_transition_accuracy": 0.55,
  "constraint_and_identity_memory_accuracy": 1.0,
  "intent_reversal_actionability_accuracy": 1.0,
  "stale_context_error_rate": 0.0,
  "stale_context_by_type": {},
  "state_revision_reasons": {
    "current_turn_confirmed_prior_state": 420,
    "LATEST_BUDGET_OVERRIDES_PRIOR": 12,
    "RESEARCH_CONTEXT_REVISES_ACTIONABILITY": 48,
    "LATEST_LOCATION_OVERRIDES_PRIOR": 12,
    "LATEST_RECIPIENT_OVERRIDES_PRIOR": 24,
    "OWNERSHIP_OR_CANCELLATION_REVISES_ACTIONABILITY": 48,
    "LATEST_PRODUCT_OVERRIDES_PRIOR": 12,
    "LATEST_TIMING_OVERRIDES_PRIOR": 12
  },
  "decision_distribution": {
    "WATCH": 408,
    "ABSTAIN": 144,
    "BLOCK": 24
  },
  "status": "manually authored Phase 6 state-revision controls; no campaign outcome claim"
}

The stateful path stores current constraints, recipient, location, product interest, timing, commerciality, and revision reasons. Later explicit evidence is permitted to override earlier state.
