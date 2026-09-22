# Phase 4 failure analysis

The adversarial v2 run retained **170** rows with either a stage or SpendDecision mismatch.

## Failure categories

- `research_only`: 10
- `existing_support`: 10
- `competitor_research`: 10
- `future_intent`: 10
- `conditional_intent`: 10
- `location_mismatch`: 10
- `mixed_commercial`: 10
- `ambiguous_pronoun`: 10
- `location_change`: 10
- `sarcasm`: 10
- `hypothetical`: 10
- `professional_research`: 10
- `unavailable_product`: 10
- `team_comparison`: 10
- `popular_research`: 10
- `direct_gift`: 10
- `research_then_buy`: 10

## Root causes/reason codes

- `PLAUSIBLE_BUT_UNCERTAIN`: 60
- `RESEARCH_ONLY`: 40
- `FUTURE_OR_CONDITIONAL_INTENT`: 20
- `LOCATION_UNSERVICEABLE`: 20
- `EXISTING_OWNER_SUPPORT`: 10
- `EVIDENCE_BACKED_COMMERCIAL_CONTEXT`: 10
- `PRODUCT_UNAVAILABLE`: 10

## Stage confusions

- `informational -> transactional`: 40
- `informational -> exploration`: 30
- `exploration -> transactional`: 20
- `consideration -> exploration`: 20
- `exploration -> consideration`: 10
- `transactional -> consideration`: 10

## Spend-decision confusions

- `TEST -> WATCH`: 30
- `ABSTAIN -> WATCH`: 30
- `ABSTAIN -> TEST`: 10

## Interpretation

The most important failure classes are retained rather than discarded: a `WATCH` output where a manually labeled `ABSTAIN` was expected is still an actionability error, while a clean hidden relevance score cannot answer that question. These controls are not external campaign outcomes.

## Remediation status

- Deterministic serviceability, availability, shipping, budget, support, research, and future-intent rules are versioned in `policies/spend_safety.yaml` and `backend/src/buyermoment/spend_safety.py`.
- Remaining ambiguous-stage errors require human-reviewed labels and/or a semantic model; they are not silently converted into positive spend recommendations.
- The full row-level evidence is in `artifacts/phase4_failure_cases.jsonl`.
