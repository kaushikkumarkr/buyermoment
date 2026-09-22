# Phase 7 baseline

Baseline frozen from commit `f394400` on branch `phase6/blinded-shadow-state` before commercial-validation changes.

## Regression checks

- Backend tests: `11 passed`.
- Ruff lint: passed.
- Frontend typecheck: passed.
- Frontend production build: passed.
- Evaluation CLI: passed; 100 records scored; purchase-stage accuracy `1.0` on the existing smoke set.

## Intelligence baseline

| Metric | Frozen value |
|---|---:|
| Clean hidden purchase-stage accuracy | 0.8720 |
| Clean hidden relevance F1 | 0.7388 |
| Clean hidden NDCG | 0.8502 |
| Clean hidden MRR | 0.8244 |
| Phase 5 adversarial TEST precision | 1.0000 |
| Phase 5 adversarial TEST coverage | 0.3000 |
| Phase 5 adversarial Waste-Risk Rate | 0.0000 |
| Phase 5 adversarial hard-negative FPR | 0.0000 |
| Phase 6 stateful stage accuracy | 0.6250 |
| Phase 6 transition accuracy | 0.5500 |
| Phase 6 stale assertion error | 0.0000 |
| Phase 6 constraint/identity memory | 1.0000 |
| Phase 6 intent-reversal actionability | 1.0000 |
| Phase 6 counterfactual direction correctness | 0.6000 |
| Phase 6 counterfactual reason correctness | 0.6000 |
| Independent human reviews | 0 |
| Live advertising gate | NO-GO |

These values are regression baselines, not commercial outcome claims. Phase 7 focuses on dogfood, experiment lineage, manual outcome import, and real advertiser validation rather than synthetic benchmark expansion.
