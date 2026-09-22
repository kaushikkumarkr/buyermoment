# Build status

## Phase 9 — service operating system (current branch)

- Branch: `phase9/service-readiness` (from `phase8/intelligence-v1`, parent `16fe45b`).
- Frozen pre-service baseline is recorded at `reports/final_build_baseline.md`; all prior benchmark artifacts remain preserved.
- Added client-scoped SQLite workspace tables for clients, evidence sources/chunks, portfolios, approvals, feedback, reports, and experiment lineage.
- Added deterministic local evidence ingestion for website/HTML/TXT/Markdown/CSV/JSON/DOCX and optional PDF parsing, with size/type validation and prompt-injection flags.
- Added client-filtered retrieval, preliminary evidence analysis, OfferFit, LandingPageFit, Experiment Portfolio, measurement audit, manual outcome CSV import, next-best-experiment structure, client reports, and platform-neutral plans.
- Added documented ChatGPT Ads manual/bulk workflow and Google AI Max planning contract using official first-party documentation; no undocumented API or private ChatGPT conversation access is claimed.
- Expanded CCB-B2B silver queue to 44 controlled scenarios across 11 categories; human-reviewed/gold records remain 0.
- Added three explicitly `DEMO_SYNTHETIC` B2B full-flow demos: CRM, Analytics/BI, Cybersecurity.
- Added minimal client workspace intake strip to the existing UI; no redesign or autonomous action.
- Local service validation: 22 backend tests passing; frontend typecheck/build passing; no Phase 9 Azure inference job or new Azure resource.
- Service gate: `SERVICE_READY_WITH_LIMITATIONS` for controlled internal/design-partner operation; live advertising and autonomous spend remain `NO-GO`.

### Phase 9 limitations

- No external client, live campaign, or real outcome is present in the repository.
- Azure AI Search, Container Apps app, Application Insights, and Azure ML were not provisioned; local SQLite/lexical retrieval is the tested default.
- Authentication/deployment hardening is still required before private client data is accepted in a deployed service.
- Evidence grounding is conservative local support logic, not a production semantic verifier.

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

## Phase 5 completed in this branch

- Added deterministic `TestReadiness` with separate commercial potential, evidence strength, ambiguity, purchase immediacy, and test-readiness components.
- Added stricter `phase5-v1` TEST eligibility policy. The selected validation-only policy requires readiness 0.75, evidence strength 0.65, ambiguity at most 0.05, explicit immediate signal, and human approval.
- Added false-TEST analysis, TEST-vs-WATCH, third-party, future-intent, harder multi-turn, counterfactual, routing, and shadow-pilot artifacts.
- Phase 5 gate: `SHADOW-GO` for offline human review only; live spend remains `NO-GO`. Human approval remains mandatory.

## Currently working

- No live advertising or Phase 5 Azure generation is authorized. The next safe step is an independent blinded human shadow review and a reviewed purchase-stage/adversarial gold tranche.

## Phase 8 — intelligence hardening

- Branch: `phase8/intelligence-v1`; audit checkpoint: `4fb6e4c`.
- Required pre-training gates completed: repository baseline recorded, Azure inventory recorded, dataset-rights registry added, and CCB-1 coverage audited.
- Azure Phase 8 inference calls: `0`; no new Azure resource/deployment/compute was created. Remaining startup credit and expiry are unverified; posted usage fields were null.
- CCB-1 coverage audit confirms `419,199` v0.1 normalized records: ESCI `10,000/2,621,288` example rows, WANDS `233,448/233,448` labels, ConvApparel V1 `175,751/175,751` turn-recommendation rows. ConvApparel V2 is separately archived/normalized as `141,168` evaluation-only rows and excluded from the v0.1 split pending rights review.
- Dataset rights registry is at `datasets/registry.yaml`; `REVIEW_REQUIRED` sources are not used to train model weights.
- Added candidate CPU ProductFit TF-IDF/logistic model and WANDS OOD benchmark. The candidate lost to the lexical baseline and remains `CANDIDATE`, not production.
- Added CCB-B2B schema and 22-record silver review queue across 11 categories; human-reviewed records and gold holdout remain `0`.
- Added deterministic evidence-grounding candidate and explicit hybrid router feature flag; no learned module is promoted by default.

### Phase 8 gate status

- BuyerMoment Intelligence v1: `NOT FROZEN`.
- B2B intelligence gate: `MORE_B2B_REVIEW_REQUIRED`.
- Live advertising: `NO-GO`.
- Real campaign outcomes: `0`.

## Phase 7 in progress — commercial validation

- Branch: `phase7/commercial-validation`.
- Frozen Phase 6 baseline recorded in `reports/phase7_baseline.md`; existing benchmark artifacts were not deleted or rewritten.
- BuyerMoment dogfood evidence package created at `businesses/buyermoment/business_evidence.json` from repository/product evidence only. Unknowns remain explicit; no customers, revenue, ROI, or campaign results were invented.
- Deterministic evidence-to-candidate workflow generated 30 raw Buyer Moments and a five-candidate opportunity report. Every candidate retains observed repository evidence plus separate inference evidence.
- Added platform-neutral `AdExperiment`, `CampaignOutcome`, `CommercialContextOutcome`, `PilotRequest`, design-partner feedback, and a portable SQLite experiment ledger.
- Added immutable Buyer Moment → experiment → outcome lineage checks and manual CSV outcome import. The repository contains no real campaign outcomes yet.
- Added ChatGPT Ads manual/export adapter: JSON package plus context-hint CSV; no undocumented API, private ChatGPT conversation access, or autonomous launch.
- Added Google AI Max future outcome schema without OAuth or campaign-management code.
- Added B2B SaaS design-partner report/feedback workflow, privacy policy, playbook, pilot preparation, and thesis kill criteria.
- Added a minimal landing-page pilot-request CTA; requests are validated and stored in the local ignored ledger only after a user submits the form.

### Phase 7 measured status

- Internal businesses analyzed: `1` (BuyerMoment dogfood).
- Raw candidates: `30`; supported candidates: `30`; top report candidates: `5`.
- Experiment packages generated: `5`; current TEST candidates: `0` because the dogfood package has no verified price or immediate buyer evidence.
- External B2B SaaS businesses, interviews, accepted experiments, live campaigns, and real outcomes: `0`.
- Human approval required: `true` for every generated experiment.

### Phase 7 limitations

- No external design partner has yet submitted data or feedback.
- ChatGPT Ads export is explicitly a human-review package and requires mapping to the current Ads Manager template; no live integration is claimed.
- The pilot request endpoint is intentionally minimal and stores local runtime data in the ignored SQLite ledger; production deployment needs authenticated private storage, consent/retention controls, and abuse protection.
- No campaign result or revenue claims exist.

## Phase 6 in progress

- Created `phase6/blinded-shadow-state` from the clean Phase 5 commit.
- Added a blinded packet protocol, private review boundary, JSON review schema, CLI submission tool, post-submission join/scoring, Cohen's kappa, severe-disagreement, reviewer-confidence, and disagreement-category metrics.
- Prepared five evidence packages and 50 deduplicated review packets (10 per business, with 30 shadow-dev and 20 shadow-holdout). The three existing businesses and two additional verticals are explicitly synthetic/demo evidence; no private customer data is committed. Independent human submissions: 0, so agreement metrics remain unavailable.
- Added an explicit validated `ConversationState` with latest budget/location/recipient/product/timing revision handling, state revision reasons, and stateful scoring. On 96 manually authored journeys / 576 turns: stateful stage accuracy 0.625, transition accuracy 0.55, explicit constraint/identity memory 1.0, intent-reversal actionability 1.0, stale assertion error 0.0. These are authored controls, not external validation.
- Added 100 Phase 6 counterfactual controls: direction correctness 0.60, reason-code correctness 0.60, unaffected-score stability 1.0. Shipping, conditional, negative, and product variants remain weaknesses.
- Phase 6 gate: `NO-GO` for live spend and pending independent shadow review. Human approval remains mandatory.

## Blocked

- Azure model dollar cost is not reported because the run metadata captured tokens only for the bounded comparison sample and no dated price sheet is embedded.
- Live ChatGPT Ads integration is intentionally not implemented without an official stable import/API contract.
- Phase 5 multi-turn stress exposes stale-context and intent-cancellation errors; the small TEST-vs-WATCH controls do not establish production safety.

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
