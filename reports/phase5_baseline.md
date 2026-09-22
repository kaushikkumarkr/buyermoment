# Phase 5 baseline

The baseline was frozen before the Phase 5 gate changes and is retained separately from Phase 4 reports.

| Measure | Frozen Phase 4 held-out baseline |
|---|---:|
| Clean hidden purchase-stage accuracy | 0.8720 |
| Clean hidden relevance F1 | 0.7388 |
| Clean hidden NDCG | 0.8502 |
| Clean hidden MRR | 0.8244 |
| Adversarial held-out TEST precision | 0.5000 |
| Adversarial held-out TEST recall | 0.3333 |
| Adversarial held-out Waste-Risk Rate | 0.0833 |
| Adversarial held-out hard-negative FPR | 0.0833 |
| Adversarial held-out abstention rate | 0.2000 |
| Multi-turn stage accuracy | 1.0000 |
| Counterfactual consistency | 1.0000 |

Phase 5 adds a stricter evidence/readiness gate; the figures above are not overwritten or retuned. The clean hidden set has no spend-action labels, so it is not used to claim TEST precision.
