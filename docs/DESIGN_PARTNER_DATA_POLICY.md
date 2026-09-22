# Design-partner data policy

Private partner evidence is not source-controlled. Keep it in an access-controlled local or approved private storage location; never place it under tracked `businesses/` or `data/` paths.

- Collect only data needed for the analysis and requested feedback.
- Prefer company/product facts and aggregated customer evidence; redact names, emails, phone numbers, free-form PII, secrets, and credentials.
- Record source, retrieval/submission time, authorization, and whether a claim is observed or inferred.
- Do not put CRM/support/customer text into model prompts without explicit authorization and a provider-terms review.
- Do not log raw secrets or private evidence in application logs.
- Store deletion requests and remove private artifacts from local/private storage; source-controlled schemas and aggregate metrics may remain.
- Do not use partner evidence as benchmark ground truth or training data automatically.

The committed BuyerMoment dogfood package is repository evidence and contains no private customer records, contacts, campaign exports, or credentials.
