# Phase 8 baseline

Generated from the verified Phase 7 state before intelligence changes.

## Repository

- Branch: `phase8/intelligence-v1`
- Parent commit: `8d8ad25`
- Working tree: clean before Phase 8 changes
- Backend tests: 15 passed
- Ruff: passed
- Existing evaluation CLI: passed on the 100-record smoke fixture; no new performance claim
- Frontend typecheck: passed
- Frontend production build: passed

## Preserved intelligence baseline

The existing Phase 2–6 benchmark artifacts remain the source of truth. The current reported baselines are:

- Clean hidden purchase-stage accuracy: `0.872`
- Clean hidden relevance F1: `0.7388`
- Clean hidden NDCG: `0.8502`
- Clean hidden MRR: `0.8244`
- Phase 5 hidden TEST precision: `100%`
- Phase 5 TEST coverage: `16.7%`
- Phase 6 stateful multi-turn stage accuracy: `62.5%`
- Phase 6 stale-context error: `0%` on authored controls
- Phase 6 constraint/identity memory: `100%` on authored controls
- Phase 6 intent-reversal actionability: `100%` on authored controls
- Phase 6 counterfactual direction/reason correctness: `60%` / `60%`
- Independent human reviews: `0`
- Live-advertising gate: `NO-GO`

These are controlled benchmark results, not campaign outcomes. Phase 8 must report regressions and must not silently replace these artifacts.

## Phase 7 commercial baseline

- Businesses analyzed: `1` internal BuyerMoment dogfood business
- Raw Buyer Moments: `30`
- Supported candidates: `30`
- Top report candidates: `5`
- Experiment packages: `5`
- External design partners: `0`
- Live campaigns: `0`
- Real campaign outcomes: `0`

Machine-readable copy: [`artifacts/phase8_baseline.json`](../artifacts/phase8_baseline.json).
