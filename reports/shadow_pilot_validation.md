# Shadow-pilot validation

{
  "businesses_reviewed": 3,
  "recommendations_reviewed": 45,
  "decision_distribution": {
    "WATCH": 20,
    "ABSTAIN": 9,
    "BLOCK": 6,
    "TEST": 10
  },
  "human_proxy_distribution": {
    "TEST": 24,
    "WATCH": 21
  },
  "decision_agreement": 0.08888888888888889,
  "test_precision_vs_human_proxy": 0.4,
  "test_recall_vs_human_proxy": 0.16666666666666666,
  "unsupported_test_rate": 0.0,
  "scope": "existing demo-business review reused as a non-blinded human proxy; not customer or campaign validation"
}

This is an offline shadow workflow. The existing reviewer labels were not collected blind to the generated candidates, so agreement is a proxy rather than independent validation. No campaign was launched.
