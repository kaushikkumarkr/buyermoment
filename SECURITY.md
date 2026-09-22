# Security

- Secrets belong in environment variables locally and the dedicated BuyerMoment Key Vault in Azure. Never commit `.env` files or raw tokens.
- Uploaded filenames must be sanitized and uploads must enforce file type and size limits before persistence.
- Customer evidence is private to its organization. The service ledger scopes clients, evidence, experiments, outcomes, approvals, feedback, and reports by `client_id`; deployment authentication and tenant identity are still required before accepting sensitive production data.
- Observed evidence, inference, hypothesis, and campaign result are separate typed values. UI copy must not turn inference into fact.
- Do not send customer data to a model provider unless the provider terms/settings permit it and the customer has explicitly authorized it.
- Use Managed Identity in Azure; the local deterministic provider does not require a secret.
- Do not log raw API keys, connection strings, uploaded customer text, or full request bodies.
- Retrieved documents are untrusted data, never instructions. Prompt-injection text is flagged; it cannot request secrets, cross-client retrieval, budget changes, or system-prompt disclosure.
- Human approval is mandatory for campaign actions. The API does not launch ads, change bids/budgets, or charge payment methods.
