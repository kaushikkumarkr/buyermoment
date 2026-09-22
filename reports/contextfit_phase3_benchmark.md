# ContextFit v0.1 benchmark

This report contains measured baseline outputs only. Null means the current data does not support a defensible metric.

| metric | value |
|---|---:|
| Commercial intent F1 | 1.0 |
| Purchase-stage accuracy | 0.872 |
| Constraint F1 | not computed |
| Product relevance NDCG | 0.8501995942843315 |
| Product relevance MRR | 0.8244140625 |
| Hard-negative FPR | 0.0 |
| Structured-output validity | 1.0 |
| Mean latency (ms) | 0.0672732249565106 |
| Estimated cost / 1,000 | 0.0 |

## Scope and limitations

- Inputs: data/ccb1/hidden_test/real.jsonl
- ESCI/WANDS relevance metrics use original human labels; no LLM judge was used.
- Controlled augmentation and hard-negative labels are targets for pipeline evaluation, not claims of human truth.
- Unsupported-inference rate requires human evidence annotations and is intentionally not fabricated.
- Azure-generated Stage A contexts are evaluated only as controlled transformations; the local deterministic scorer remains the measured scoring baseline.

```json
{
  "benchmark": "CCB-1 v0.1 ContextFit hidden evaluation",
  "inputs": [
    "data/ccb1/hidden_test/real.jsonl"
  ],
  "source_counts": {
    "amazon_esci": 1044,
    "google_convapparel": 15656,
    "wayfair_wands": 16490
  },
  "subset_counts": {
    "real": 32940,
    "hard_negative": 190,
    "conversational_augmentation": 60
  },
  "model_configuration": {
    "scorer": "deterministic-contextfit-v0.1",
    "provider": "local",
    "azure_roles": {
      "bulk_generator": "buyermoment-bulk-generator (Stage A generated inputs)",
      "extractor": "buyermoment-extractor (comparison only; not used for score labels)",
      "judge": "not_deployed; original human labels take precedence"
    }
  },
  "metrics": {
    "commercial_intent": {
      "count": 190,
      "tp": 76,
      "fp": 0,
      "fn": 0,
      "tn": 114,
      "precision": 1.0,
      "recall": 1.0,
      "f1": 1.0,
      "scope": "controlled hard-negative targets only"
    },
    "purchase_stage": {
      "count": 250,
      "accuracy": 0.872,
      "macro_f1": 0.8337932080048513,
      "scope": "controlled augmentation/hard-negative targets only"
    },
    "constraint_extraction": {
      "count": 0,
      "precision": null,
      "recall": null,
      "f1": null,
      "scope": "records with explicit canonical required_features only"
    },
    "location_fit": {
      "count": 0,
      "tp": 0,
      "fp": 0,
      "fn": 0,
      "tn": 0,
      "precision": null,
      "recall": null,
      "f1": null,
      "scope": "controlled explicit city/serviceability targets only"
    },
    "product_relevance": {
      "count": 17314,
      "tp": 8665,
      "fp": 3835,
      "fn": 2291,
      "tn": 2523,
      "precision": 0.6932,
      "recall": 0.790890836071559,
      "f1": 0.7388301500682128,
      "ndcg": 0.8501995942843315,
      "mrr": 0.8244140625,
      "queries_with_labels": 64,
      "scope": "original ESCI/WANDS labels; no LLM judge"
    },
    "hard_negative": {
      "false_positive_rate": 0.0,
      "count": 190
    },
    "evidence_grounding": {
      "evidence_coverage": 1.0,
      "unsupported_inference_rate": null,
      "unsupported_inference_status": "not_computed_without_human_annotations"
    },
    "structured_output": {
      "schema_validity": 1.0,
      "valid_records": 33190
    },
    "economics": {
      "scored_records": 33190,
      "mean_latency_ms": 0.0672732249565106,
      "tokens": 0,
      "estimated_cost_per_1000": 0.0,
      "cost_basis": "deterministic local scorer; Azure generation is tracked separately"
    }
  },
  "status": "measured_baseline; controlled labels are not human ground truth; Azure generation completed Stage A but is not used as a scorer label"
}
```
