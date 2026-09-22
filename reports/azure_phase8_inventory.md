# Azure Phase 8 inventory

Read-only inventory captured on 2026-09-22. Scope was the existing subscription for account metadata and `rg-buyermoment-dev` for BuyerMoment resources. No deployment, inference, scaling, deletion, or other write operation was performed.

## Dedicated footprint

`rg-buyermoment-dev` is in `eastus2`, is `Succeeded`, and is tagged `product=BuyerMoment` and `creditGuardrail=startup-credit`. It contains only the previously established BuyerMoment development footprint:

- `buyermoment-foundry-260921` — Cognitive Services/AIServices S0
- `acrbuymoment260921` — Container Registry Basic
- `stbuyermoment260921` — Storage Standard_LRS
- `kv-buyermoment-260921` — Key Vault
- `law-buyermoment-260921` — Log Analytics
- `cae-buyermoment-dev` — Container Apps managed environment

The Foundry account has two succeeded existing deployments: `gpt-5.4-nano` (`buyermoment-bulk-generator`) and `gpt-5.4-mini` (`buyermoment-extractor`), both GlobalStandard capacity 10.

## Spend and credit visibility

The read-only Azure consumption query for 2026-09-01 through 2026-09-22 returned five filtered BuyerMoment records, but the preview CLI response exposed null quantity, currency, dates, and `pretaxCost`. The posted dollar amount is therefore unavailable and is not fabricated here. The subscription query also did not expose remaining Microsoft for Startups balance or expiry. Remaining credit and expiry are recorded as `UNVERIFIED`, not assumed from prior context.

Before any paid inference or deployment, the model must be re-checked as `Direct from Azure` and covered by the sponsorship. Phase 8 has started no Azure inference and has created no new resources.

Machine-readable inventory: [`artifacts/azure_phase8_inventory.json`](../artifacts/azure_phase8_inventory.json).
