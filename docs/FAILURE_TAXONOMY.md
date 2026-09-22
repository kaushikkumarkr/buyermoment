# BuyerMoment failure taxonomy

Benchmark and engineering-review failures use one primary category. Secondary notes may record the affected dataset, stage, or constraint type.

- `false_commercial_intent`: research, support, complaint, or academic text scored as an ad-worthy buying context.
- `wrong_purchase_stage`: current action was classified one or more stages away from the guide.
- `wrong_product_match`: product relevance or ranking does not match the original human label or explicit control.
- `missed_hard_constraint`: budget, feature, compatibility, timing, geography, currency, or shipping constraint was missed.
- `location_failure`: serviceability, destination, future location, or beneficiary location was handled incorrectly.
- `unsupported_inference`: output states a fact not present in retained evidence.
- `duplicate_buyer_moment`: recommendation repeats an existing intent without new evidence or constraints.
- `generic_non_actionable_intent`: output lacks a testable situation, product, or constraint.
- `bad_experiment_hypothesis`: experiment cannot be tied to the evidence-backed buyer moment.
- `overconfident_prediction`: confidence exceeds empirical correctness for its calibration bin.
- `evidence_mismatch`: cited evidence does not support the component or reason code.

Formal benchmark counts and engineering-review counts are reported separately; subjective usefulness is not substituted for ground-truth accuracy.
