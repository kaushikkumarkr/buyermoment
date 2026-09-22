# ProductFit out-of-domain evaluation

The ProductFit candidate is trained on Amazon ESCI and evaluated on both the held-out ESCI subset and independent Wayfair WANDS labels. WANDS `Partial` rows are excluded from binary metrics because the canonical pipeline keeps that original label as `unknown` rather than inventing a relevance class.

The machine-readable run is [`artifacts/product_fit_benchmark.json`](../artifacts/product_fit_benchmark.json). The report must be regenerated after any model/config change; no ESCI-only result should be treated as evidence of general product relevance.

## Interpretation rules

- ESCI hidden measures within-source generalization under the corrected source-aware split.
- WANDS OOD measures transfer to a different product catalog/search domain.
- NDCG/MRR are query-group ranking metrics; F1 is binary relevant-vs-irrelevant classification.
- Neither dataset measures B2B SaaS fit, ad appropriateness, conversion, or revenue.

## Current promotion status

`product_fit_tfidf_v1` remains `CANDIDATE`. It cannot override deterministic constraints or SpendDecision policy. Promotion requires the hybrid ablation to show no hard-negative, evidence-grounding, or SpendDecision regression.
