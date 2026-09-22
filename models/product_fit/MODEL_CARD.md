# ProductFit TF-IDF v1 model card

## Summary

`product_fit_tfidf_v1` is a compact CPU candidate for binary product relevance. It uses word TF-IDF unigrams/bigrams over the context/query and product title/description, followed by balanced logistic regression.

## Training and evaluation

- Training source: Amazon ESCI original relevance labels only.
- Training split: CCB-1 train split; no hidden labels or WANDS rows used.
- Evaluation: CCB-1 hidden ESCI and hidden WANDS OOD rows with known binary labels.
- Relevance mapping: Exact/Substitute/Complement = relevant; Irrelevant = not relevant. WANDS Partial remains excluded because CCB-1 intentionally represents it as unknown.
- Exact metrics and checkpoint hash: [`artifacts/product_fit_benchmark.json`](../../artifacts/product_fit_benchmark.json).

## Intended use

Candidate retrieval/ranking feature for product fit, with deterministic constraint/policy checks applied afterward.

## Prohibited interpretation

This model does not predict advertising lift, click probability, conversion probability, profitability, or B2B SaaS behavior. It is trained on ecommerce product-search relevance and must not override hard serviceability or safety policies.

## Limitations

ESCI is currently represented by a 10,000-row normalized slice. WANDS is a different product-search domain and is used as an out-of-domain check, not as a claim of universal generalization. The model is a candidate and is not promoted to the production default until the hybrid ablation and SpendDecision regression gates pass.
