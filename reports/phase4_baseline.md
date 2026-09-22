# Phase 4 baseline

This report records the Phase 3 state before the Phase 4 safety changes. Existing Phase 3 reports are preserved.

## Revalidated build

- Branch at start: `phase3/benchmark-trust`, commit `1479b27`.
- Backend tests: 4 passed.
- Ruff and frontend typecheck/build: passed.
- Corrected split: 348,974 train / 38,175 validation / 33,190 hidden test.
- Cross-split leakage: zero, per the Phase 3 integrity audit.

## Revalidated benchmark values

| Measure | Phase 3 baseline |
|---|---:|
| Hidden purchase-stage accuracy | 0.8720 |
| Hidden relevance F1 | 0.7388 |
| Hidden relevance NDCG | 0.8502 |
| Hidden relevance MRR | 0.8244 |
| Hidden hard-negative FPR | 0.0000 |
| Adversarial purchase-stage accuracy | 0.5333 |
| Adversarial commercial-intent F1 | 0.6667 |
| Adversarial hard-negative FPR | 0.2857 |
| Relevance calibration ECE | 0.1180 |

The Phase 3 hidden set does not contain spend-action labels, so it cannot produce a valid Waste-Risk Rate. Phase 4 uses a separately held-out adversarial control set with explicit spend-safety labels for that metric.

## Interpretation

The baseline is strong on clean controlled stage and ranking slices but materially weaker on ambiguous/adversarial contexts. Phase 4 therefore evaluates abstention, deterministic serviceability/budget policy, current-turn intent handling, and counterfactual behavior. No Azure resource or model deployment was added for this baseline rerun.
