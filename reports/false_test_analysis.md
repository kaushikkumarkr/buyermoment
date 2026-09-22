# False TEST analysis

The replay found **10** false TEST decisions across 300 adversarial controls. The hidden subset is kept separate from validation in the artifact.

## Counts

- `ambiguous_intent`: 10

## Split

- `hidden_test`: 10

## Interpretation

These are control-label mismatches used to improve safety. A false TEST is treated as a spend-safety failure even when the underlying context contains some commercial interest. The full product, location, evidence, ContextFit, SpendDecision, reason codes, and root-cause hypothesis are retained in `artifacts/false_test_cases.jsonl`.

## Immediate remediation direction

The next policy should require strong test-readiness evidence, penalize ambiguity and future/conditional language, and keep plausible but under-evidenced contexts in WATCH. Threshold selection will be performed on validation controls and checked on the hidden subset.
