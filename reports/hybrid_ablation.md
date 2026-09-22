# Hybrid intelligence ablation

The first local ProductFit candidate was evaluated against its transparent lexical-overlap baseline. This is an ablation of the product-fit component only; the legacy ContextFit, deterministic policy, ConversationState, TestReadiness, and SpendDecision remain available.

| Dataset | Learned TF-IDF F1 | Lexical F1 | Learned NDCG | Lexical NDCG |
|---|---:|---:|---:|---:|
| ESCI hidden | 0.6614 | 0.7670 | 0.8140 | 0.8607 |
| WANDS OOD | 0.3799 | 0.4418 | 0.7683 | 0.9436 |

The compact learned model does not beat the simple lexical baseline on this run and is rejected for `hybrid_v1` promotion. This is a useful negative result: the current 10,000-row ESCI slice does not justify adding model complexity, and ranking quality must be protected. No LLM fallback was invoked and no Azure inference was used.

Machine-readable metrics: [`artifacts/product_fit_benchmark.json`](../artifacts/product_fit_benchmark.json).
