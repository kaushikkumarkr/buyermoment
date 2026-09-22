# Service readiness gate

## Current result

`SERVICE_READY_WITH_LIMITATIONS` is the target outcome of the local service validation in this phase. It must not be read as live-client or live-ROI proof.

## Required checks

- client isolation and evidence provenance pass;
- website/file ingestion and prompt-injection defense pass;
- Buyer Moment, OfferFit, LandingPageFit, Experiment Portfolio, and measurement audit pass;
- ChatGPT Ads and Google AI Max plans are documented/manual or planning-only, with no fabricated APIs;
- manual outcome import preserves immutable launch predictions;
- reports and next-best decisions preserve evidence and uncertainty;
- human approval is enforced;
- red-team tests pass;
- backend/lint/evaluation/frontend checks pass.

## Limitations that prevent `SERVICE_READY`

No external client has yet supplied real data in this repository, no live campaign has been launched, no real campaign outcome exists, evidence grounding still uses a conservative local baseline, and Azure AI Search/Container Apps deployment has not been provisioned in this phase. The service is therefore ready for controlled internal/design-partner operation, not autonomous or proven advertising performance.
