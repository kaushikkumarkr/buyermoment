# Multi-turn robustness

{
  "journey_count": 50,
  "turn_count": 300,
  "stage_accuracy": 1.0,
  "stage_transition_accuracy": 1.0,
  "intent_reversal_detection": 1.0,
  "constraint_memory_accuracy": 1.0,
  "third_party_intent_detection": 1.0,
  "stale_context_error_rate": 0.0,
  "spend_decision_distribution": {
    "WATCH": 240,
    "BLOCK": 40,
    "ABSTAIN": 20
  },
  "by_journey_type": {
    "reversal": {
      "count": 60,
      "stage_accuracy": 1.0,
      "block_accuracy": 1.0
    },
    "location_change": {
      "count": 60,
      "stage_accuracy": 1.0,
      "block_accuracy": 1.0
    },
    "third_party": {
      "count": 60,
      "stage_accuracy": 1.0,
      "block_accuracy": null
    },
    "budget_change": {
      "count": 60,
      "stage_accuracy": 1.0,
      "block_accuracy": 1.0
    },
    "research_to_buy": {
      "count": 60,
      "stage_accuracy": 1.0,
      "block_accuracy": null
    }
  },
  "status": "manually authored multi-turn controls; current-turn safety evaluation, not customer outcome validation"
}

The current-turn classifier is evaluated against explicit journey labels. `stale_context_error_rate` counts a positive eligible decision on a turn explicitly labeled as a support, reversal, or serviceability block.
