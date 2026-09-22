# Build status

## Completed

- Product context and evidence-first principles recorded in `PRODUCT.md`.
- Design system persisted under `design-system/buyermoment/`.
- Provider-neutral Pydantic models for CommercialContext, evidence, products, Buyer Moments, scores, datasets, and experiments.
- Deterministic ContextFit scorer with budget, feature, location, stage, and ad-relevance reasoning codes.
- Three demo businesses and Business Analyzer -> Buyer Moment discovery path.
- ChatGPT Ads experiment package generator with JSON export and explicit hypothesis disclaimer.
- 100-record synthetic CCB-1 seed builder and reproducible evaluation CLI.
- Real dataset fetch/normalization adapters for ConvApparel, Amazon ESCI, and Wayfair WANDS with source checksums and license metadata.
- Canonical `CommercialContextRecord`, source-aware grouping, hidden-test split generation, 100-record manual inspection report, CCB-1 card, manifest, and portable export script.
- Azure-direct Stage A conversational augmentation: 100 real parents, 500 accepted variants, with rate-limited retry metadata retained.
- Controlled hard negatives and explicit constraint/location controls.
- ContextFit hidden benchmark and bounded two-model Azure comparison report.
- Initial React Signal Board UI with evidence/inference separation and responsive states.
- Dedicated BuyerMoment Azure development footprint provisioned and verified in eastus2.

## Currently working

- Finalize Phase 2 documentation/tests, review benchmark artifacts, and push the phase branch.

## Blocked

- Azure model dollar cost is not reported because the run metadata captured tokens only for the bounded comparison sample and no dated price sheet is embedded.
- Live ChatGPT Ads integration is intentionally not implemented without an official stable import/API contract.

## Azure resources created

- Resource group: `rg-buyermoment-dev` (eastus2), tagged `product=BuyerMoment`, `creditGuardrail=startup-credit`.
- Foundry/AIServices account: `buyermoment-foundry-260921` — `https://buyermoment-foundry-260921.cognitiveservices.azure.com/`.
- Blob Storage: `stbuyermoment260921` — `https://stbuyermoment260921.blob.core.windows.net/`.
- ACR Basic: `acrbuymoment260921` — `acrbuymoment260921.azurecr.io`.
- Key Vault: `kv-buyermoment-260921`.
- Log Analytics: `law-buyermoment-260921`.
- Container Apps Environment: `cae-buyermoment-dev`.
- `buyermoment-bulk-generator`: gpt-5.4-nano, GlobalStandard capacity 10, used for Stage A.
- `buyermoment-extractor`: gpt-5.4-mini, GlobalStandard capacity 10, used only for a five-parent comparison.
- Least-privilege `Cognitive Services OpenAI User` role assigned at the dedicated account scope.

## Approximate credit consumed

- Infrastructure existed before this phase. Two Azure-direct deployments were added in the dedicated resource group. Stage A used 100 parent requests, produced 500 accepted variants, and encountered then cleared 49 request-rate-limit retries. No Batch job, GPU, VM, AKS, or partner-billed model was used.
- Exact dollar consumption is intentionally unclaimed; see `AZURE_SPEND.md`.

## Benchmark status

- CCB-1 manifest: 419,199 real normalized records; 500 Azure conversational augmentations; 500 template controls; 500 hard negatives; 140 controlled constraint/location records; 0 human-reviewed gold records.
- Hidden source-aware split: 345,460 train / 39,785 validation / 35,094 hidden test; 420,339 unique record IDs and group leakage check passed.
- ContextFit hidden baseline: intent F1 1.0 on 40 controlled hard-negative cases; purchase-stage accuracy 0.5619 on 105 controlled cases; constraint F1 0.7778 on 11 hidden controls; location-fit F1 1.0 on 7 hidden controls; relevance F1 0.7357, NDCG 0.9155, MRR 0.9078 on original ESCI/WANDS labels; schema validity 1.0.
- Bounded model comparison: both Azure-direct configurations returned 5/5 schema-valid parent calls; token counts and latency are in `artifacts/model_comparison_v0_1.json`. Dollar cost remains null.

## Known limitations

- Demo UI currently uses local fixture data and does not persist uploads.
- The ESCI normalization is a reproducible 10,000-row slice of the official 2.6M-row release for v0.1; scaling requires storage/review justification.
- ConvApparel lacks universal human relevance labels; unsupported-inference rate needs human evidence annotations.
- Azure augmentation labels are controlled transformation targets, not human ground truth; no external campaign outcomes are present.
- The generated experiment export is a structured package, not a live platform integration.

## Next action

Review the benchmark artifacts, add human evidence annotations for the next gold tranche, and use Azure billing export to populate actual dollar costs before any Stage B scale-up.
