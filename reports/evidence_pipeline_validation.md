# Evidence pipeline validation

Status: local validation PASS; managed Azure AI Search not provisioned.

Validated locally:

- text, Markdown, HTML, CSV, JSON, DOCX extraction paths;
- PDF path is optional and fails clearly when `pypdf` is unavailable;
- source metadata includes client ID, URI/title, retrieval time, data origin, privacy, and provenance;
- paragraph/sentence chunking is deterministic;
- lexical retrieval enforces `client_id` before scoring;
- prompt-injection phrases are flagged as untrusted data and are not executed;
- client A evidence is not returned to client B in tests.

Known limitation: local retrieval is lexical, not a production-scale semantic index. Azure AI Search is documented as an optional provider; no new Search resource was created.
