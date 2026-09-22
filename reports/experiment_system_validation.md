# Experiment system validation

- `AdExperiment` validates a platform-neutral hypothesis, context strategy, offer, creative, budget, measurement plan, approval, and immutable version metadata.
- `ChatGPTAdsAdapter` exports a JSON package and context-hint CSV for human review. It does not call an undocumented API or launch a campaign.
- A generated package preserves `business_id`, `buyer_moment_id`, `experiment_id`, evidence IDs, ContextFit version, policy version, and `human_approval_required=true`.
- The current dogfood run produced five packages and saved no live spend or credentials.
