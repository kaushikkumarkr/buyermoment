# Evaluation

Run the baseline with:

```bash
make eval
```

The runner writes machine-readable `artifacts/evaluation/summary.json` and a human-readable report. It reports only metrics that are actually computed. The seed evaluation intentionally marks constraint extraction F1 and unsupported-claim rate as not computed until gold spans and human review annotations exist.

The benchmark should grow to include commercial-intent and purchase-stage accuracy, constraint extraction precision/recall/F1, location extraction accuracy, product-fit ranking NDCG/MRR, ESCI relevance accuracy without overwriting original labels, hard-negative false-positive rate, unsupported-claim rate and evidence-grounding quality, structured-output validity, latency, tokens, and estimated cost.

The hidden split is generated separately and should not be placed in prompts or developer-visible fixtures.

