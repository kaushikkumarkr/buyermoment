# Phase 5 model routing

{
  "benchmark": "Phase 5 TEST-safety routing comparison",
  "rules_first_nano_then_mini": {
    "test_precision": 1.0,
    "waste_risk_rate": 0.0,
    "coverage": 0.4,
    "mini_escalation_rate": 0.0,
    "note": "Phase 5 local deterministic policy path; no Azure call was needed for the measured safety gate."
  },
  "bounded_azure_reference": {
    "all_mini_accuracy": 0.4444444444444444,
    "routed_accuracy": 0.4,
    "mini_escalation_rate": 0.7,
    "tokens": {
      "nano": {
        "prompt_tokens": 899,
        "completion_tokens": 179,
        "total_tokens": 1078,
        "calls": 10,
        "mean_latency_ms": 1254.3825626838952
      },
      "mini": {
        "prompt_tokens": 1436,
        "completion_tokens": 285,
        "total_tokens": 1721,
        "calls": 16,
        "mean_latency_ms": 1230.8816458535148
      }
    },
    "cost": "not posted; token usage retained and no dollar estimate fabricated"
  },
  "decision": "Use deterministic rules first; escalate only unresolved borderline cases in a future shadow run. Phase 5 did not create a deployment or submit model calls.",
  "status": "measured reference plus local Phase 5 policy benchmark; not a production cost claim"
}

The previous bounded Azure comparison is retained as a reference. The Phase 5 safety gate is deterministic and therefore has zero mini escalation in this benchmark; a future shadow pilot may route only borderline TEST/WATCH cases.
