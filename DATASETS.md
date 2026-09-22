# Dataset lineage

The repository keeps dataset directories separate:

```text
data/raw/          external downloads, ignored by Git
data/normalized/   source-specific normalized records
data/augmented/    offline model proposals, ignored by Git
data/gold/         reviewed benchmark fixtures
data/train/        training exports, ignored by Git
data/validation/   validation exports, ignored by Git
data/hidden_test/  held-back evaluation inputs, ignored by Git
```

CCB-1 records preserve `source_dataset`, `source_record_id`, `source_license`, `original_label`, and `transformation_history`. The committed 100-record seed is synthetic and is labeled as such; it is not a claim about Google ConvApparel, Amazon ESCI, or Wayfair WANDS.

Verified source references: Google ConvApparel is published by Google on Hugging Face; its dataset card currently advertises CC BY 4.0, while the associated paper materials have referenced CC BY-SA 4.0, so the ingestion job must preserve the exact license/attribution artifact downloaded with the selected release instead of hard-coding a guess. Amazon ESCI is maintained by Amazon Science under Apache-2.0 and retains Exact/Substitute/Complement/Irrelevant labels. Wayfair WANDS is maintained in the official `wayfair/WANDS` repository under MIT.

External ingestion adapters should preserve the original labels. ESCI Exact/Substitute/Complement/Irrelevant labels must remain untouched. Dataset-specific Apache-2.0, MIT, or source license/NOTICE text must be kept next to the downloaded artifact and included in exports.

Future download scripts should verify checksums and write to `data/raw/<dataset>/` without committing the raw payload.

## Phase 2 CCB-1 pipeline

Use `scripts/fetch_datasets.py --dataset all` to download the official artifacts into ignored `data/ccb1/raw/`. `scripts/normalize_real_datasets.py --dataset all --esci-max-rows 10000` writes the canonical `CommercialContextRecord` JSONL and retains per-source labels in metadata. The ESCI cap is an explicit v0.1 storage/review boundary; omit it only when a larger run is justified.

`reports/ccb1_real_data_validation.md` records the 100-record round-robin inspection. `scripts/split_ccb1.py` keeps every parent and conversational variant in one source-aware group and writes ignored train/validation/hidden-test files. `ccb1_manifest.json` contains counts and checksums without committing the large data.
