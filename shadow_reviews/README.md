# Shadow review storage

`schema.json` is source-controlled. Reviewer packets, model predictions, and submissions belong under `shadow_reviews/private/` and are ignored by Git because they may contain private business evidence.

Generate blinded packets with:

```bash
PYTHONPATH=backend/src python scripts/build_phase6_business_packages.py
PYTHONPATH=backend/src python scripts/build_blinded_shadow_packets.py
```

Reviewers must receive `reviewer_packets.jsonl` without the model-prediction file. Save one JSON object per submission using `schema.json`, then run `scripts/score_blinded_shadow.py` locally. Never commit the private files.
