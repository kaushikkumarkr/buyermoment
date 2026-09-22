# ContextFit v0.1 benchmark

This report contains measured baseline outputs only. Null means the current data does not support a defensible metric.

| metric | value |
|---|---:|
| Commercial intent F1 | 1.0 |
| Purchase-stage accuracy | 0.5619047619047619 |
| Constraint F1 | 0.7777777777777778 |
| Product relevance NDCG | 0.9155279354161243 |
| Product relevance MRR | 0.9078387290167865 |
| Hard-negative FPR | 0.0 |
| Structured-output validity | 1.0 |
| Mean latency (ms) | 0.058244936864655594 |
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
    "amazon_esci": 1024,
    "google_convapparel": 17562,
    "wayfair_wands": 16490,
    "ccb1_controlled": 18
  },
  "subset_counts": {
    "real": 34971,
    "controlled": 18,
    "hard_negative": 40,
    "conversational_augmentation": 65
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
      "count": 40,
      "tp": 16,
      "fp": 0,
      "fn": 0,
      "tn": 24,
      "precision": 1.0,
      "recall": 1.0,
      "f1": 1.0,
      "scope": "controlled hard-negative targets only"
    },
    "purchase_stage": {
      "count": 105,
      "accuracy": 0.5619047619047619,
      "macro_f1": 0.6451547185751942,
      "scope": "controlled augmentation/hard-negative targets only"
    },
    "constraint_extraction": {
      "count": 11,
      "precision": 1.0,
      "recall": 0.6363636363636364,
      "f1": 0.7777777777777778,
      "scope": "records with explicit canonical required_features only"
    },
    "location_fit": {
      "count": 7,
      "tp": 3,
      "fp": 0,
      "fn": 0,
      "tn": 4,
      "precision": 1.0,
      "recall": 1.0,
      "f1": 1.0,
      "scope": "controlled explicit city/serviceability targets only"
    },
    "product_relevance": {
      "count": 17439,
      "tp": 8687,
      "fp": 3825,
      "fn": 2415,
      "tn": 2512,
      "precision": 0.6942934782608695,
      "recall": 0.7824716267339218,
      "f1": 0.73574997882612,
      "ndcg": 0.9155279354161243,
      "mrr": 0.9078387290167865,
      "queries_with_labels": 343,
      "scope": "original ESCI/WANDS labels; no LLM judge"
    },
    "hard_negative": {
      "false_positive_rate": 0.0,
      "count": 40
    },
    "evidence_grounding": {
      "evidence_coverage": 1.0,
      "unsupported_inference_rate": null,
      "unsupported_inference_status": "not_computed_without_human_annotations"
    },
    "structured_output": {
      "schema_validity": 1.0,
      "valid_records": 35094
    },
    "economics": {
      "scored_records": 35094,
      "mean_latency_ms": 0.058244936864655594,
      "tokens": 0,
      "estimated_cost_per_1000": 0.0,
      "cost_basis": "deterministic local scorer; Azure generation is tracked separately"
    }
  },
  "status": "measured_baseline; controlled labels are not human ground truth; Azure generation completed Stage A but is not used as a scorer label"
}
```
