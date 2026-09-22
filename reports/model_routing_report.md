# Model routing report

{
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
}
