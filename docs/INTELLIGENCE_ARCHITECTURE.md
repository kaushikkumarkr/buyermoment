# BuyerMoment Intelligence architecture

Phase 8 keeps the existing legacy scorer available and adds candidate local modules behind an explicit hybrid mode.

```text
deterministic extraction
        ↓
candidate ProductFit / EvidenceGrounding modules
        ↓
confidence and disagreement
        ↓
LLM fallback only when ambiguity requires it
        ↓
ContextFit → TestReadiness → SpendDecision
```

Hard constraints and policy remain deterministic. Specialized models may provide candidate scores, but they cannot override unavailable products, unsupported serviceability, explicit support/ownership cases, or human-approval policy.

`product_fit_tfidf_v1` is the first candidate. It is trained on original ESCI labels and evaluated on WANDS OOD; its promotion status is recorded in `models/registry.yaml`. Commercial intent/stage training is deferred until rights-cleared, human-supported labels are available. The existing `ConversationState` remains the stateful baseline.
