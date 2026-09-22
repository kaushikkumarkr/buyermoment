# Shadow-pilot review guide

This workflow is offline decision-support validation. It must not launch an ad, set a budget, or call a platform API.

Review each BuyerMoment independently of the model's final decision where possible. Read the business evidence, context, product/serviceability facts, timing, and constraints first. Assign exactly one label:

- `TEST`: evidence is explicit and immediate enough to justify a human-approved experiment.
- `WATCH`: commercially plausible, but timing, evidence, identity, or constraints are not strong enough for spend.
- `ABSTAIN`: insufficient, research-only, hypothetical, mixed, or non-actionable evidence.
- `BLOCK`: a known policy/serviceability/ownership condition makes advertising inappropriate or impossible.

Record the evidence sentence(s), the deciding constraint, uncertainty, and whether a human would approve a capped experiment. Do not infer revenue, conversion rate, or profitability. The reviewer must mark `HUMAN_APPROVAL_REQUIRED=true` for every recommendation.

The existing demo-business review is a proxy and was not blinded to candidate generation. A real shadow pilot should use an independent reviewer, freeze the rubric before scoring, preserve disagreements, and report agreement separately from benchmark accuracy.
