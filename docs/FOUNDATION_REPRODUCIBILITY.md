# Foundation reproducibility

The Phase 8 local, no-inference checkpoints are:

```bash
PYTHONPATH=backend/src python scripts/audit_ccb1_coverage.py
python scripts/benchmark_product_fit.py
PYTHONPATH=backend/src python scripts/build_ccb_b2b_seed.py
PYTHONPATH=backend/src python scripts/benchmark_evidence_grounding.py
```

The first command requires the existing raw CCB-1 cache. Large raw payloads and generated benchmark artifacts remain outside the normal Git path unless intentionally force-added as small, durable metadata. Source checksums and license references are recorded in `data/ccb1/source_manifest.json`, `ccb1_manifest.json`, and `datasets/registry.yaml`.

No Azure inference is required for these commands. Dataset downloads for new sources are deliberately separate and blocked by the rights registry until their terms and checksums are reviewed.
