# Model routing policy

The router is feature-flagged in `buyermoment.intelligence.IntelligenceRouter`:

- `legacy`: current ContextFit/scoring path; default and regression-safe.
- `hybrid_v1`: candidate local ProductFit/evidence modules first, deterministic policy next, LLM escalation only for low-confidence or ambiguous cases.

Routing principles:

1. Exact constraints and policy blockers are deterministic.
2. A candidate learned model cannot override serviceability, availability, support/ownership, or human approval policy.
3. Low confidence, missing evidence, exploration/information stages, and missing product evidence are escalation/review signals rather than permission to invent a result.
4. Azure inference is not invoked automatically by the router. Any future Azure call must verify Direct-from-Azure billing coverage and record role, deployment, tokens, latency, and result.
5. The candidate ProductFit model did not beat lexical ranking in the first ablation, so `legacy` remains the default.
