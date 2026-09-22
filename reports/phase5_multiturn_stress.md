# Phase 5 multi-turn stress benchmark

{
  "journey_count": 60,
  "turn_count": 360,
  "stage_accuracy": 0.6944444444444444,
  "stage_transition_accuracy": 0.6666666666666666,
  "decision_accuracy": 0.5555555555555556,
  "intent_reversal_detection": 0.8333333333333334,
  "stale_context_error_rate": 0.10526315789473684,
  "decision_distribution": {
    "ABSTAIN": 60,
    "WATCH": 230,
    "TEST": 50,
    "BLOCK": 20
  },
  "status": "manually authored Phase 5 stress controls; no campaign outcome claim"
}

Later-turn contradictions and cancellations are treated as current-state evidence; prior buying intent is not allowed to force TEST.
