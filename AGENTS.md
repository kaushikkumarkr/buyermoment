# Agent operating notes

BuyerMoment follows the repository principle: evidence before inference, inference before experiment, real outcomes before claims.

- Preserve existing user changes.
- Use `apply_patch` for source edits.
- Run `pytest -q`, `make eval`, and frontend typecheck/build before handoff.
- Never fabricate benchmark results, campaign performance, dataset labels, or business facts.
- Azure changes must remain in the dedicated BuyerMoment resource group and must be cost-tagged.
- Keep raw external datasets out of Git and preserve license/NOTICE metadata.

