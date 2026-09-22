# Phase 8 cost report

## Azure

- Phase 8 Azure model inference calls: `0`.
- New Azure deployments: `0`.
- New GPU/VM/Batch/Databricks/AKS resources: `0`.
- Temporary resources deleted: `Yes` (none created in Phase 8).
- Posted Phase 8 dollar cost: unavailable; the read-only consumption response returned null quantity/currency/pretax cost fields.
- Remaining startup credit and expiry: unverified by the available subscription queries.

The existing `rg-buyermoment-dev` resources and deployments were inspected only. No model is being treated as sponsorship-covered without a future Direct-from-Azure/billing verification.

## Local computation

The ProductFit candidate ran locally on CPU using scikit-learn. It used 8,096 labeled ESCI training rows and produced a 2.5 MB checkpoint. The CCB-B2B seed and evidence-grounding controls used local deterministic Python. No paid inference was required.

## Decision

The learned ProductFit candidate did not beat the lexical baseline, so no larger run or Azure augmentation was justified. Remaining credits are preserved for a future rights-cleared, targeted experiment.
