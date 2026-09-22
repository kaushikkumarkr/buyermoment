# Build status

## Completed

- Product context and evidence-first principles recorded in `PRODUCT.md`.
- Design system persisted under `design-system/buyermoment/`.
- Provider-neutral Pydantic models for CommercialContext, evidence, products, Buyer Moments, scores, datasets, and experiments.
- Deterministic ContextFit scorer with budget, feature, location, stage, and ad-relevance reasoning codes.
- Three demo businesses and Business Analyzer -> Buyer Moment discovery path.
- ChatGPT Ads experiment package generator with JSON export and explicit hypothesis disclaimer.
- 100-record synthetic CCB-1 seed builder and reproducible evaluation CLI.
- Initial React Signal Board UI with evidence/inference separation and responsive states.
- Dedicated BuyerMoment Azure development footprint provisioned and verified in eastus2.

## Currently working

- Source-specific external dataset download/normalization adapters.

## Blocked

- Live model augmentation is waiting on verification that a chosen Foundry model is Direct from Azure / covered by startup sponsorship.
- Live ChatGPT Ads integration is intentionally not implemented without an official stable import/API contract.

## Azure resources created

- Resource group: `rg-buyermoment-dev` (eastus2), tagged `product=BuyerMoment`, `creditGuardrail=startup-credit`.
- Foundry/AIServices account: `buyermoment-foundry-260921` — `https://buyermoment-foundry-260921.cognitiveservices.azure.com/`.
- Blob Storage: `stbuyermoment260921` — `https://stbuyermoment260921.blob.core.windows.net/`.
- ACR Basic: `acrbuymoment260921` — `acrbuymoment260921.azurecr.io`.
- Key Vault: `kv-buyermoment-260921`.
- Log Analytics: `law-buyermoment-260921`.
- Container Apps Environment: `cae-buyermoment-dev`.
- No model deployment yet; eligibility and billing coverage must be verified before adding one.

## Approximate credit consumed

- Infrastructure-only deployment completed; no large model run has been executed. Billing consumption should be reviewed in Azure Cost Management before adding compute.

## Benchmark status

- CCB-1 v0.1 synthetic seed: 100 records; baseline evaluation is available; no external benchmark claim is made.

## Known limitations

- Demo UI currently uses local fixture data and does not persist uploads.
- External dataset ingestion, authentication, tenant enforcement, and real campaign outcome ingestion are next milestones.
- The generated experiment export is a structured package, not a live platform integration.

## Next action

Wire container images to the dedicated Container Apps environment, then add reviewed external dataset adapters and verify a Direct-from-Azure model deployment before any augmentation run.
