# Client data policy

Client data is private by default and is never committed to Git. Local development uses a private SQLite path or private files excluded by `.gitignore`; deployment uses client-scoped database records and private Blob Storage with managed identity/Key Vault.

## Allowed handling

- collect only evidence needed for the requested analysis;
- preserve source, retrieval time, client ID, and data origin;
- redact unnecessary personal data before upload;
- separate provided, public, synthetic, human-review, and real-campaign data;
- support export and deletion by client;
- log metadata and IDs, not raw CRM or support text.

## Model boundary

Retrieved documents are untrusted data. They are not instructions. Do not send secrets, credentials, or unrelated client data to any model. Azure/LLM use must respect the configured provider terms and client authorization; no external training use is implied.

## Retention

The service operator records the retention period in the engagement record. Temporary source files are deleted after normalization when permitted. Outcome records retain lineage and source metadata; raw exports are retained only when the client authorizes it.
