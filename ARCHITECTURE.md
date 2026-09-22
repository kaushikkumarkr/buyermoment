# Architecture

```text
client-scoped evidence -> retrieval -> analyzer -> CommercialContext -> ContextFit scorer -> Buyer Moments -> portfolio -> experiment adapter
                                          |                  |                  |
                                      provenance         deterministic       ChatGPT Ads JSON
                                                         checks first
```

The Python core owns the provider-neutral models, deterministic scoring, analyzer, experiment package, and evaluation runner. `ModelProvider`, `StorageProvider`, and `EmbeddingProvider` are protocols; the default runtime is deterministic so the app remains portable after Azure credits expire.

The React client is a focused Signal Board: ranked moments, component scores, evidence tabs, and a hypothesis-only experiment lab. It ships with demo businesses for footwear ecommerce, skincare ecommerce, and B2B SaaS and can switch between them without inventing campaign results.

The service layer adds a portable client workspace, local evidence chunks/retrieval, OfferFit, LandingPageFit, MeasurementAudit, manual outcome import, and next-best-experiment records. Azure AI Search/Foundry are provider seams, not hidden requirements. All service objects are client-scoped; launch-time predictions remain immutable in the experiment ledger.

PostgreSQL/pgvector are intentionally deferred until the local workflow and retrieval evidence justify them. The MVP's interfaces are storage-neutral and can be backed by Postgres, Blob, or a local file store.
