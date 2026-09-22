# Shadow-data privacy

- Source-controlled files contain schemas, synthetic scenarios, aggregate metrics, and provenance—not private customer evidence.
- Private packets and reviewer submissions live under `shadow_reviews/private/`, which is Git-ignored.
- Only authorized business evidence may enter a packet. Redact secrets, credentials, personal contact details, payment data, and unnecessary personal information before review.
- Model prompts should contain only the selected evidence needed for the candidate. Raw uploads and reviewer identifiers must not be logged in application logs.
- Keep model predictions and reviewer submissions separate until the comparison step.
- Do not use shadow data to train an external model without explicit authorization and compatible provider terms.
- Delete private packets according to the business retention agreement; repository artifacts must contain only de-identified aggregates.
