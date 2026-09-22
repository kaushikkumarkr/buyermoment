# Outcome ingestion validation

The neutral manual CSV importer and SQLite ledger are implemented and covered by automated tests using a temporary test ledger. The repository contains only a header-only import template; no real campaign data exists yet.

Validated behavior:

- accepts daily rows for impressions, clicks, spend, conversions, qualified conversions, conversion value, and revenue;
- requires a pre-existing experiment;
- rejects an outcome whose `experiment_id` and `buyer_moment_id` do not match the immutable experiment lineage;
- writes a `CommercialContextOutcome` with predictions captured from the experiment at creation time;
- preserves source and import-method provenance.

Current real-world counts: experiments with campaign outcomes `0`; qualified conversions `0`; revenue `0` (no campaigns have been launched).
