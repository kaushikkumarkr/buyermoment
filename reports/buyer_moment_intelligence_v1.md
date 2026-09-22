# BuyerMoment Intelligence v1 gate

## Result: NOT FROZEN

The Phase 8 v1 bundle is not frozen because the first learned ProductFit candidate did not beat the lexical baseline on either ESCI hidden or WANDS OOD ranking, and the B2B layer has no human-reviewed records. The safe decision is to preserve the legacy system and candidate modules rather than claim a hybrid improvement.

### Accepted foundation

- deterministic constraint and policy engine;
- evidence/provenance-carrying canonical schemas;
- existing ConversationState as a regression baseline;
- platform-neutral experiment/outcome lineage from Phase 7;
- reproducible rights and coverage audits;
- candidate evidence-grounding gate with explicit unsupported status.

### Rejected or deferred

- `product_fit_tfidf_v1`: rejected for hybrid promotion in this run because lexical overlap performed better on both held-out metrics;
- CommercialIntentModel: deferred; no rights-cleared human-reviewed B2B labels;
- EvidenceGroundingModel: candidate only; external Contextual Product QA evaluation deferred pending rights review;
- ConvApparel V2, SGD/SGD-X, Taskmaster, and KuaiSearch-Lite: not downloaded/trained while registry review is unresolved;
- Azure inference: zero Phase 8 calls; no cost was incurred by Phase 8 model inference.

The next credible v1 candidate requires more rights-cleared labels, a human-reviewed B2B holdout, and an ablation that improves or preserves ranking and safety rather than merely adding model complexity.
