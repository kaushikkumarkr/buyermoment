# Azure spend and sponsorship guardrails

## Scope

This phase uses only the dedicated `rg-buyermoment-dev` resource group. Existing Azure resources outside that group are out of scope and were not modified.

## Model eligibility decision

Microsoft’s Foundry sponsorship guidance says startup credits apply when Microsoft bills the AI model usage to the Azure subscription. The Microsoft Foundry documentation classifies Azure OpenAI models as models sold directly by Azure and billed through the Azure subscription. BuyerMoment therefore selected the Azure-direct `gpt-5.4-nano` deployment, not a partner/community model. This decision must be rechecked before adding another model because catalog and billing characteristics can change.

## Recorded activity

| date | job/resource | model/deployment | scope | result | cost status |
|---|---|---|---:|---|---|
| 2026-09-22 | model deployment | `gpt-5.4-nano` / `buyermoment-bulk-generator` | capacity 10, GlobalStandard | Running in dedicated account | Azure-direct; exact credit charge not available from the deployment response |
| 2026-09-22 | Stage A smoke request | same deployment | 1 parent requested | 5 accepted variants after switching to the current v1 endpoint | Per-request usage was not retained by the augmentation runner; verify billing export before reporting dollars |
| 2026-09-22 | Stage A augmentation | `gpt-5.4-nano` / `buyermoment-bulk-generator` | 100 parents, 500 variants | 500 accepted variants; 49 parents required a paced retry after rate limiting | Exact dollar cost not available from the job metadata |
| 2026-09-22 | bounded model comparison | `gpt-5.4-nano` and `gpt-5.4-mini` | 5 parents per model | Both models returned 5/5 schema-valid parent calls | Token counts in `artifacts/model_comparison_v0_1.json`; dollar cost intentionally not computed |
| 2026-09-22 | Phase 3 bounded routing comparison | `gpt-5.4-nano` and `gpt-5.4-mini` | 10 adversarial stage cases; 26 total calls including escalation | 10 nano calls, 16 mini calls; one all-mini request hit 429, routed run completed | Token usage in `artifacts/model_routing_report.json`; posted dollar cost unavailable and not fabricated |

No 100-record Azure run or Batch workload has been submitted. The deterministic 500-row Stage A control and 500 hard negatives were generated locally at no model-token cost.

The read-only Azure Consumption query for `rg-buyermoment-dev` over 2026-09-21 through 2026-09-23 returned no usage rows, so this repository does not claim a dollar amount. Billing export/Cost Management remains the authoritative source when the sponsorship ledger posts.

## Rules before scaling

1. Check the model is still listed as sold directly by Azure and sponsorship-covered.
2. Estimate tokens and cost for the requested sample.
3. Run a single request and validate schema/evidence safety.
4. Inspect failures before scaling from 100 to 500 or larger.
5. Record actual usage/cost from Azure billing/usage data; do not substitute a fabricated estimate.

The legacy deployment URL initially returned a data-plane authorization error even though the least-privilege `Cognitive Services OpenAI User` role was present. The current Azure OpenAI v1 endpoint succeeded; no account key was retrieved as a workaround.
