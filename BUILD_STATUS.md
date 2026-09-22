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

## Phase 3 completed in this branch

- Corrected two split defects: ConvApparel parent/variant leakage and exact normalized-context collisions across groups. Corrected split: 348,914 train / 38,184 validation / 33,241 hidden test across 13,360 merged groups.
- Added integrity audit, purchase-stage guide, 100 six-turn journeys (600 turns), adversarial controls, calibration analysis, constraint-type breakdown, failure taxonomy, model routing benchmark, and structured review for all three demo businesses.
- Extended ContextFit output with semantic-product-fit, offer-fit, raw confidence, calibrated confidence fields, and explicit constraint-field extraction.
- Reused only the two existing Azure-direct deployments for a bounded 10-case nano/mini routing run. No new Azure resource, deployment, Batch job, or non-dedicated resource was created.

## Currently working

- Phase 4 findings are documented. The next safe step is human review of targeted adversarial/purchase-stage gold cases before any live pilot decision. No Phase 5 product expansion was started.

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
- Corrected hidden split: 348,914 train / 38,184 validation / 33,241 hidden test; 420,339 unique record IDs; 13,360 merged groups; integrity audit PASS.
- Corrected hidden baseline: commercial-intent F1 1.0 on 190 controlled targets; purchase-stage accuracy 0.872 on 250 controlled targets; relevance F1 0.7388, NDCG 0.8502, MRR 0.8244 on original ESCI/WANDS labels; schema validity 1.0. Synthetic constraint/location families are isolated from the hidden split to prevent template leakage; the dedicated 140-record control reports budget F1 1.0, required-feature F1 0.9247, timing F1 1.0, and location-serviceability F1 1.0.
- Adversarial benchmark: 120 manual controls; commercial-intent F1 0.6667; purchase-stage accuracy 0.5333; hard-negative FPR 0.2857; 8/16 explicit negative-serviceability cases failed.
- Multi-turn benchmark: 100 manually authored journeys / 600 turns; baseline and stateful rule-assisted stage accuracy 1.0, transition errors 0, constraint-memory accuracy 1.0. Template coverage only.
- Calibration: raw stage ECE 0.3083 / Brier 0.2032 and raw relevance ECE 0.2236 / Brier 0.2771. Validation-fitted isotonic calibration reduced relevance ECE to 0.1180 but worsened stage ECE to 0.7071, so calibrated values remain analysis-only.
- Bounded routing: all-mini valid accuracy 0.4444 with one 429; routed nano→mini valid accuracy 0.4000, 70% escalated, 10/10 routed calls valid. No routing quality improvement is claimed.
- Real-business review: 45 evidence-backed candidates, 15 per demo business; top-five usefulness 1.0 / 1.0 / 0.8 for footwear / skincare / B2B SaaS; `would_test_with_real_ad_budget=yes` rate 0.5333 for each. Internal engineering review only.

## Phase 4 completed in this branch

- Added first-class `SpendDecision`: `TEST`, `WATCH`, `ABSTAIN`, and `BLOCK`, with versioned deterministic policy rules, commercial actionability, evidence, reason codes, and `human_approval_required=true`.
- Added 300 adversarial v2 controls across 30 categories with source-aware validation/hidden separation, 50 six-turn difficult journeys (300 turns), and 150 one-feature counterfactual controls.
- Revalidated the clean hidden benchmark after implementation changes: purchase-stage accuracy 0.8720, relevance F1 0.7388, NDCG 0.8502, MRR 0.8244, hard-negative FPR 0.0, schema validity 1.0.
- Phase 4 adversarial v2: purchase-stage accuracy 0.5667, macro F1 0.6256, overall Waste-Risk Rate 0.0455, held-out Waste-Risk Rate 0.0833, held-out TEST precision 0.50, held-out hard-negative FPR 0.0833, block accuracy 1.0. These remain controlled benchmark results, not campaign outcomes.
- Multi-turn controls: stage accuracy 1.0, transition accuracy 1.0, intent-reversal detection 1.0, constraint-memory accuracy 1.0, stale-context error rate 0.0. Coverage is manually authored and not external validation.
- Counterfactual controls: direction consistency 1.0 and reason-code correctness 1.0 on 150 cases.
- Real-business safety replay: 45 candidates; 16 TEST, 14 WATCH, 9 ABSTAIN, 6 BLOCK; TEST precision against the subjective `would_test=yes` review 1.0; human approval required 1.0.
- Pilot gate: `NO-GO` for live advertiser spend. BuyerMoment remains human-approved decision support.
- No new Azure resources, deployments, Batch jobs, or Phase 4 Azure model calls were made. Existing resources outside `rg-buyermoment-dev` were not modified.

## Known limitations

- Demo UI currently uses local fixture data and does not persist uploads.
- The ESCI normalization is a reproducible 10,000-row slice of the official 2.6M-row release for v0.1; scaling requires storage/review justification.
- ConvApparel lacks universal human relevance labels; unsupported-inference rate needs human evidence annotations.
- Azure augmentation labels are controlled transformation targets, not human ground truth; no external campaign outcomes are present.
- The generated experiment export is a structured package, not a live platform integration.
- Purchase-stage and multi-turn labels are authored controls, not human conversation annotations.
- Exact-context grouping improves integrity but reduces independent ranking queries; revised ranking metrics are not directly comparable with pre-audit metrics.
- Location, currency, shipping, exclusion, compatibility, and language labels remain sparse; unsupported categories are marked not computed.
- Confidence calibration is dataset/configuration-specific and not suitable for customer-facing probability language.

## Next action

Add a small human-reviewed gold tranche for purchase stage and adversarial serviceability, then rerun the same Phase 4 gate. Use Azure billing export to populate actual dollar costs; Phase 4 produced no new Azure model usage and does not justify scale-up.
