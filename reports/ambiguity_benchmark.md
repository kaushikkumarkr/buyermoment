# Ambiguity benchmark

{
  "benchmark": "Phase 5 ambiguity analysis",
  "validation": {
    "mean_test": 0.008333333333333333,
    "mean_watch": 0.26666666666666666
  },
  "hidden": {
    "mean_test": 0.008333333333333333,
    "mean_watch": 0.11666666666666665
  },
  "policy": {
    "version": "phase5-v1",
    "min_test_overall": 0.7,
    "min_test_confidence": 0.68,
    "min_test_actionability": 0.2,
    "min_watch_overall": 0.5,
    "min_watch_confidence": 0.5,
    "min_test_readiness": 0.75,
    "min_test_evidence_strength": 0.65,
    "max_test_ambiguity": 0.05,
    "require_immediate_signal": true,
    "human_approval_required": true
  }
}
