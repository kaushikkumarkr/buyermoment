# Phase 4 model routing

{
  "benchmark": "Phase 4 model-routing safety comparison",
  "phase4_sample": 300,
  "strategies": {
    "A_nano_only": {
      "quality": "not rerun in Phase 4; see prior Azure-direct bounded result",
      "model": "buyermoment-bulk-generator / gpt-5.4-nano"
    },
    "B_mini_only": {
      "quality": "not rerun in Phase 4; see prior Azure-direct bounded result",
      "model": "buyermoment-extractor / gpt-5.4-mini"
    },
    "C_nano_then_mini": {
      "quality": "not rerun in Phase 4; prior bounded result retained below",
      "model": "existing Azure-direct deployments"
    },
    "D_rules_then_model_on_ambiguity": {
      "policy_decision_distribution": {
        "TEST": 60,
        "ABSTAIN": 80,
        "BLOCK": 100,
        "WATCH": 60
      },
      "model_escalation_proxy_rate": 0.4666666666666667,
      "quality_metrics": {
        "validation_test_precision": 1.0,
        "validation_waste_risk_rate": 0.0,
        "validation_abstain_rate": 0.3333333333333333,
        "hidden_test_precision": 0.5,
        "hidden_waste_risk_rate": 0.08333333333333333,
        "hidden_abstain_rate": 0.2
      },
      "latency": "local deterministic scorer; Azure model latency not measured in Phase 4",
      "token_usage": 0,
      "quality": "model calls intentionally not added: Phase 4 policy failures are measurable locally and the prior mini run hit a 429; no new Azure spend was justified before human-reviewed labels."
    }
  },
  "prior_bounded_azure_evidence": {
    "benchmark": "Phase 3 bounded model routing comparison",
    "sample": 10,
    "all_mini": {
      "count": 10,
      "valid": 9,
      "accuracy": 0.4444444444444444,
      "errors": [
        "Azure OpenAI request failed (429): {\n  \"error\": {\n    \"message\": \"Your requests to gpt-5.4-mini for buyermoment-extractor in eastus2 have exceeded rate limit.\",\n    \"type\": \"too_many_requests\",\n    \"param\": null,\n    \"code\": \"rate_limit_exceeded\"\n  }\n}"
      ]
    },
    "routed_nano_to_mini": {
      "count": 10,
      "valid": 10,
      "accuracy": 0.4,
      "errors": [],
      "escalated": 7,
      "escalation_rate": 0.7
    },
    "usage": {
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
    "cost": "not posted; token usage retained and no dollar estimate fabricated",
    "models": {
      "nano": "buyermoment-bulk-generator / gpt-5.4-nano",
      "mini": "buyermoment-extractor / gpt-5.4-mini"
    },
    "status": "bounded Azure-direct run on manually authored adversarial stage cases; not a production cost claim"
  },
  "cost": "posted dollar cost unavailable; no Phase 4 Azure model call or new deployment was made",
  "recommendation": "Keep deterministic rules first; route only ambiguous WATCH/ABSTAIN cases after a reviewed gold tranche exists.",
  "status": "measured safety routing proxy; not a claim of Phase 4 model-quality improvement"
}

Phase 4 did not create a model deployment or invoke a new Azure workload. The prior bounded Azure-direct comparison is included for traceability; deterministic safety routing is evaluated on the new adversarial set.
