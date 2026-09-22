# Phase 7 commercial-validation data

This directory contains portable schemas/templates and a local SQLite experiment ledger.

- `outcome_import_template.csv` is a header-only manual import template. It contains no campaign outcome data.
- `experiment_ledger.sqlite3` is runtime-local and is ignored by Git.
- Private business evidence, CRM exports, PII, ad credentials, and campaign exports must not be committed here.

Use `scripts/import_phase7_outcomes.py` only with authorized exports. The importer requires an existing immutable experiment and preserves the `experiment_id` → `buyer_moment_id` lineage.
