# BuyerMoment Intelligence architecture

Phase 9 keeps the existing legacy scorer available and adds a service operating layer behind client-scoped evidence and explicit approval gates. The default service path is local/portable; Azure Search and Azure-direct LLM calls are optional providers, not hidden dependencies.

```text
client evidence (untrusted data)
        ↓
normalize / chunk / client-filtered retrieval
        ↓
LLM business understanding when configured
        ↓
Buyer Moment discovery + provenance
        ↓
deterministic constraints / policy / measurement audit
        ↓
ContextFit → OfferFit → LandingPageFit → TestReadiness → SpendDecision
        ↓
human-approved Experiment Portfolio
        ↓
manual platform execution → outcome import → next-best experiment
```

Hard constraints and policy remain deterministic. Specialized models may provide candidate scores, but they cannot override unavailable products, unsupported serviceability, explicit support/ownership cases, or human-approval policy.

Retrieved evidence is always data, never instructions. Every material claim carries source IDs and a fact/inference/hypothesis distinction. `product_fit_tfidf_v1` remains rejected after OOD review; the legacy ContextFit scorer remains the production default. Specialized models are optional accelerators and cannot override hard policy. Commercial intent/stage training remains deferred until rights-cleared, human-supported labels are available. The existing `ConversationState` remains the stateful baseline.
