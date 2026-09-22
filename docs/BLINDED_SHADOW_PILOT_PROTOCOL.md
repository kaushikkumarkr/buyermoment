# Blinded shadow-pilot protocol

This protocol measures whether independent humans would consider BuyerMoment recommendations worth testing. It does not launch advertising and does not authorize spend.

## Separation

1. BuyerMoment generates candidates and stores its ContextFit, TestReadiness, SpendDecision, evidence, and reason codes in a private model-prediction file.
2. The reviewer receives only the business evidence package, candidate context, product/offer facts, constraints, provenance, and unknowns. The reviewer packet excludes model scores and decisions.
3. The reviewer submits `TEST`, `WATCH`, `ABSTAIN`, or `BLOCK`, plus `would_spend_real_money`, confidence, reason, and optional disagreement category.
4. A separate join step compares the reviewer submission with the private model prediction.

The packet and prediction files use the same opaque `packet_id`, but the review interface must not display or expose the prediction file. Reviewers should not inspect generated reports before submitting.

## Review rubric

- `TEST`: explicit need, suitable product/offer evidence, compatible constraints/location, and sufficient immediacy for a human-approved experiment.
- `WATCH`: commercially plausible but timing, evidence, identity, or constraints are not ready for spend.
- `ABSTAIN`: research, hypothetical, ambiguous, unsupported, or non-actionable context.
- `BLOCK`: known ownership/support, serviceability, availability, budget, shipping, language, or policy failure.

Record the evidence sentence(s) that support the label. Do not invent margin, LTV, CAC, inventory, demographics, conversion rates, or serviceability. Unknowns remain unknown.

## Sampling and holdout

Use 5–10 businesses with 8–15 deduplicated candidates each. Freeze the rubric and split businesses/candidates into `shadow_dev` and `shadow_holdout` before policy changes. Use the development split for discussion only; report final agreement on the holdout. If the sample is too small, report metrics as unavailable rather than treating the proxy review as independent evidence.

Where feasible, have two reviewers independently label a subset. Report human-human agreement and confidence alongside BuyerMoment-human agreement. A low-confidence human disagreement is not equivalent to a high-confidence policy failure.
