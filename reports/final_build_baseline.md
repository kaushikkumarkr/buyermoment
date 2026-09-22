# Final service-build baseline

Date: 2026-09-22
Branch at capture: `phase9/service-readiness` (created from `phase8/intelligence-v1`)
Parent commit: `16fe45b39892771bf6f2a1ecc40674e026854fd0`

## Verification

| Check | Result |
|---|---|
| Backend tests | PASS — 18 passed |
| Ruff | PASS |
| Evaluation CLI | PASS — 100-record smoke run; baseline-only output |
| Frontend typecheck | PASS |
| Frontend production build | PASS |
| Working tree before Phase 9 edits | CLEAN |

## Preserved intelligence baseline

- Clean hidden purchase-stage accuracy: `0.872`.
- Clean hidden relevance F1: `0.7388`.
- Clean hidden NDCG: `0.8502`.
- Clean hidden MRR: `0.8244`.
- Phase 6 multi-turn stage accuracy: `0.625`.
- Phase 6 stale-context error: `0%`.
- Phase 8 CCB-B2B silver records: `22`; human-reviewed/gold records: `0`.
- Phase 8 candidate TF-IDF ProductFit model: rejected; legacy ContextFit remains default.
- Phase 8 evidence-grounding authored-control accuracy: `50%`; not production-ready as a standalone semantic verifier.

This report is a frozen pre-service baseline. Later reports must distinguish local/demo validation from real client or campaign evidence.
