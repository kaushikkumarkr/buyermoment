# Evaluation

Run the baseline with:

```bash
make eval
```

The runner writes machine-readable `artifacts/evaluation/summary.json` and a human-readable report. It reports only metrics that are actually computed. The seed evaluation intentionally marks constraint extraction F1 and unsupported-claim rate as not computed until gold spans and human review annotations exist.

The benchmark should grow to include commercial-intent and purchase-stage accuracy, constraint extraction precision/recall/F1, location extraction accuracy, product-fit ranking NDCG/MRR, ESCI relevance accuracy without overwriting original labels, hard-negative false-positive rate, unsupported-claim rate and evidence-grounding quality, structured-output validity, latency, tokens, and estimated cost.

The hidden split is generated separately and should not be placed in prompts or developer-visible fixtures.

## Phase 2 measured benchmark

Run the hidden benchmark after the local split exists:

```bash
PYTHONPATH=backend/src python3 scripts/evaluate_contextfit.py \
  --input data/ccb1/hidden_test/real.jsonl
```

This writes `artifacts/contextfit_v0_1_benchmark.json` and `reports/contextfit_v0_1_benchmark.md`. Original ESCI/WANDS labels are the relevance ground truth; controlled augmentation, hard negatives, and constraint/location controls are reported separately and are not human gold. Null metrics are intentional when the source has no defensible annotation. `scripts/benchmark_models.py` runs a bounded same-input comparison across configured Azure-direct roles and records tokens/latency without inventing dollar costs.
