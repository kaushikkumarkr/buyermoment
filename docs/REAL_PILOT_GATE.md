# Real pilot gate

BuyerMoment remains decision support. `HUMAN_APPROVAL_REQUIRED = true` for every `SpendDecision`; the system must not autonomously create campaigns, set budgets, or spend media.

## Gate inputs

The gate is based on actual Phase 4 artifacts, not a target invented after seeing a result:

- corrected CCB-1 integrity audit;
- adversarial v2 Waste-Risk Rate and TEST precision;
- explicit BLOCK-policy checks for serviceability, availability, shipping, budget, and support contexts;
- counterfactual consistency;
- multi-turn intent reversal and stale-context checks;
- evidence coverage and reviewer agreement on the three demo businesses.

## Decision policy

- `GO` requires a reviewed gold tranche for the relevant industry and location, no critical BLOCK-policy failures, and adversarial TEST precision/Waste-Risk distributions accepted by the pilot owner before any budget is committed.
- `LIMITED GO` may support a manually approved, capped observation-only experiment when policy failures are absent but coverage or calibration remains limited. BuyerMoment may recommend a hypothesis, but a human selects the audience, budget, creative, and stop rule.
- `NO-GO` applies when adversarial waste risk is not yet acceptable, stage/reversal errors remain material, evidence coverage is weak, or the review set is still only synthetic/demo evidence.

## Phase 4 decision

Phase 4 is `NO-GO` for real advertiser spend. The expanded adversarial v2 set contains material stage errors and a measured 8.33% held-out Waste-Risk Rate (4.55% across all 300 controls); held-out TEST precision is 50%. The 45-business review is an internal engineering review rather than customer validation, and no human-reviewed gold tranche or campaign outcomes exists. The next safe prerequisite is human review of targeted adversarial and purchase-stage cases followed by a repeated gate evaluation.
