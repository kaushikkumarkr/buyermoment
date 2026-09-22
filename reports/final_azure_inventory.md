# Final Azure inventory

Captured: 2026-09-22. Inventory was read-only and limited to `rg-buyermoment-dev` in subscription `97be63b6-5dd8-45f4-87da-0bc4d87ac24a`.

## Existing resources

| Resource | Type | Region | State |
|---|---|---|---|
| `buyermoment-foundry-260921` | AI Services / Foundry | eastus2 | Succeeded |
| `buyermoment-bulk-generator` | gpt-5.4-nano, GlobalStandard, capacity 10 | eastus2 | Running |
| `buyermoment-extractor` | gpt-5.4-mini, GlobalStandard, capacity 10 | eastus2 | Running |
| `acrbuymoment260921` | Container Registry Basic | eastus2 | Existing |
| `stbuyermoment260921` | Storage Standard_LRS | eastus2 | Existing |
| `kv-buyermoment-260921` | Key Vault, RBAC, soft delete | eastus2 | Existing |
| `law-buyermoment-260921` | Log Analytics | eastus2 | Existing |
| `cae-buyermoment-dev` | Container Apps environment | eastus2 | Existing |

## Not provisioned in the isolated group

No Azure AI Search service, Azure ML workspace, Application Insights component, or Container App was found. No new Azure resource was created in Phase 9; the local evidence index and SQLite ledger are the reproducible default.

## Billing/credit status

Subscription usage queries returned records with null `pretaxCost`, quantity, currency, and usage dates in the available posting window. Remaining startup credit and expiry were not verifiable from the available CLI result. No dollar amount is claimed. Existing deployment metadata is recorded; no Phase 9 model inference job was submitted.

## Guardrails

- Existing unrelated resource groups were not inspected or modified.
- Existing Foundry deployments are used only through an opt-in provider interface; local tests do not call them.
- No GPU, Batch, Search, database, or always-on app was created.
