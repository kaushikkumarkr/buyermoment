# Security

- Secrets belong in environment variables locally and the dedicated BuyerMoment Key Vault in Azure. Never commit `.env` files or raw tokens.
- Uploaded filenames must be sanitized and uploads must enforce file type and size limits before persistence.
- Customer evidence is private to its organization. The future Postgres schema must scope every business, evidence record, context, and experiment by `organization_id`.
- Observed evidence, inference, hypothesis, and campaign result are separate typed values. UI copy must not turn inference into fact.
- Do not send customer data to a model provider unless the provider terms/settings permit it and the customer has explicitly authorized it.
- Use Managed Identity in Azure; the local deterministic provider does not require a secret.
- Do not log raw API keys, connection strings, uploaded customer text, or full request bodies.

