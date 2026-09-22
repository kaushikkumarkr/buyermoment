# Measurement playbook

Before spend, audit:

- one primary conversion with a written definition;
- deduplication and event ownership;
- UTMs and experiment/Buyer Moment identifiers;
- landing-page and form tracking;
- CRM linkage and consent;
- MQL/SQL/opportunity/pipeline/revenue fields;
- offline conversion path and conversion lag;
- timezone, currency, attribution window, and data freshness.

Statuses are `TRACKING_READY`, `TRACKING_PARTIAL`, and `TRACKING_UNSAFE`. Do not recommend scaling while tracking is unsafe. Missing revenue remains missing; it is never imputed as success.
