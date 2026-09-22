# Phase 8 OOD matrix

The matrix is intentionally partial. It reports measured runs only where labels and rights are currently available, and marks deferred datasets rather than manufacturing comparable scores.

| Train | Test | Module | Result |
|---|---|---|---|
| ESCI | ESCI hidden | TF-IDF ProductFit | F1 `0.6614`, NDCG `0.8140`, MRR `0.7409` |
| ESCI | WANDS hidden OOD | TF-IDF ProductFit | F1 `0.3799`, NDCG `0.7683`, MRR `0.6555` |
| ESCI | WANDS hidden OOD | lexical baseline | F1 `0.4418`, NDCG `0.9436`, MRR `0.9232` |
| Phase 6 state controls | Phase 6 state journeys | ConversationState | stage `0.625`, stale-context `0.0` |
| B2B silver | B2B human-reviewed holdout | CommercialIntent | unavailable; `0` reviewed records |
| SGD/SGD-X, Taskmaster | dialogue OOD | dialogue state | deferred pending rights review |

The learned ProductFit model is rejected for default promotion because it loses to the lexical baseline both within ESCI and on WANDS OOD. The clean ContextFit benchmark remains the preserved legacy baseline, not a directly comparable model run.
