# Phase 8 model routing

No Azure model calls were made in Phase 8. The explicit router feature flag and local candidate path were implemented, but no production routing claim is made.

| Route | Behavior | Status |
|---|---|---|
| `legacy` | Existing deterministic ContextFit and policy path | default |
| `hybrid_v1` clear case | Candidate local module + deterministic policy | experimental |
| `hybrid_v1` ambiguous case | Review/escalation signal; no automatic model invocation | experimental |
| Azure fallback | Existing Foundry deployment only after billing eligibility check | not invoked |

The first learned ProductFit module was rejected by the ablation. A useful escalation-rate/quality/cost comparison requires a rights-cleared candidate that first beats the simple lexical baseline; Phase 8 does not claim that result.
