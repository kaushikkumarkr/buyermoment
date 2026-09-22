# CCB-1 v0.1 Dataset Card

## Purpose

CCB-1 is a versioned benchmark for commercial context understanding: commercial intent, purchase stage, product relevance, constraints, and advertising appropriateness. It is an evaluation and research asset, not a claim that any context will convert or be profitable.

## Current composition

The v0.1 build uses real/open data first. The exact counts and checksums are in [`ccb1_manifest.json`](ccb1_manifest.json). The current local build contains 233,448 WANDS judgments, 175,751 ConvApparel recommendation contexts, and a reproducible 10,000-record ESCI slice from the official 2.6M-row release. It also contains 500 Azure-generated controlled conversational transformations, 500 local template controls, 500 controlled hard negatives, and 140 explicit constraint/location controls. No records have been promoted to human-reviewed gold.

The ESCI slice is an explicit cost/storage boundary for v0.1, not a claim to represent the full source. The normalization script can be rerun with a different cap or no cap when storage and review capacity justify it.

## Sources and attribution

- Google ConvApparel: CC BY 4.0, conversational shopping sessions with recommendation context. Source metadata and checksums are recorded in `data/ccb1/source_manifest.json`.
- Amazon ESCI: Apache-2.0 source release. Original Exact/Substitute/Complement/Irrelevant labels are preserved in `metadata.original_esci_label`; they are never replaced by generated judgments.
- Wayfair WANDS: MIT source release. Original Exact/Partial/Irrelevant labels are preserved in `metadata.original_label`; Partial remains `unknown` in the canonical relevance field because it is not equivalent to Exact.

## Construction and splits

Normalization uses source-provided joins only. Missing fields remain missing. Every generated row carries `metadata.parent_record_id`, evidence, provenance, and transformation history. All source records and their variants are assigned together using a stable source-aware group split. The hidden split is not included in Git; only its counts and checksum metadata are committed.

Phase 3 adds 120 separately held-out adversarial controls and 100 six-turn manually authored journeys. No records have been promoted to human-reviewed gold.

## Synthetic augmentation

Augmentation creates controlled conversational variants (high purchase intent, comparison, exploration, informational, and existing-owner support) from real parents. Hard negatives deliberately retain product keywords while changing the commercial meaning (buy, research, support, complaint, comparison). These labels are controlled targets for pipeline checks, not human ground truth. Azure generation is implemented behind a provider interface; Stage A produced 500 accepted Azure variants and is retained as controlled transformation data, never as observed customer behavior. A five-parent same-input comparison across two Azure-direct models is recorded in `artifacts/model_comparison_v0_1.json`; its token-overlap signal is only a guardrail proxy.

Phase 3 split audit: zero cross-split source-group leakage, zero cross-split exact normalized-context collisions, and zero hidden-example matches in tracked files. Exact normalized-context collisions are merged into one split group before assignment.

Phase 4 adds 300 separately held-out adversarial v2 controls across 30 categories: 150 validation records and 150 hidden records. They are manually authored controls with neutral paraphrase suffixes, not customer conversations or campaign outcomes. It also adds 50 six-turn difficult journeys (300 turns) and 150 one-feature counterfactual controls. These assets are evaluated separately from the CCB-1 real-data hidden split.

## Limitations and risks

- ConvApparel does not provide a universal product-relevance label for every recommendation row; relevance remains unknown unless the source explicitly provides it.
- The current real-data slice is shopping/search-centric and has limited location, language, currency, serviceability, and timing annotations.
- WANDS and ESCI labels measure product-search relevance, not advertising lift, conversion probability, or profitability.
- Dataset source populations and product categories can encode geographic, demographic, language, and marketplace bias.
- Controlled transformations may be stylistically narrow and require manual review before training or gold promotion.

## Appropriate and prohibited interpretations

Use CCB-1 to compare model/configuration behavior, find failure modes, and measure evidence-grounded context/product matching. Do not use it to claim a guaranteed buyer, infer a precise location without evidence, set ad budgets autonomously, or represent model-generated variants as observed customer behavior.

## Promotion policy

Human review is required before any synthetic row is promoted to `gold`. Benchmark results must report the source subset and whether labels are human/original or controlled targets. Unsupported-claim rate remains uncomputed until human evidence annotations exist.
