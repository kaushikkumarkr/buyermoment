# ProductFit compact model training

The first Phase 8 learned module is a CPU-only TF-IDF + balanced logistic-regression baseline. It trains only on original Amazon ESCI labels from the CCB-1 train split. No Azure inference or external model call was used.

Run:

```bash
python scripts/benchmark_product_fit.py
```

The model is intentionally a candidate, not a silent replacement for ContextFit. The run records both the transparent lexical-overlap baseline and the learned model, plus a held-out ESCI and WANDS OOD evaluation. The exact records, metrics, and artifact hash are in [`artifacts/product_fit_benchmark.json`](../artifacts/product_fit_benchmark.json).

Acceptance is deferred until the model is compared against the legacy scorer on ranking, safety, latency, and cost. An improvement on ESCI alone is insufficient.
