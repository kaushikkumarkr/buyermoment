# Service red-team validation

Automated local checks cover:

- prompt-injection text is flagged and retained as data;
- cross-client evidence retrieval returns no results;
- client-boundary feedback/outcome checks reject mismatched client IDs;
- approved live-ad actions through the service approval endpoint are rejected; approval remains an external authorized-human action;
- missing tracking and duplicate-event risk become `TRACKING_UNSAFE`;
- a blocked/abstained Buyer Moment cannot be treated as proof of spend readiness;
- no endpoint launches ads, changes bids, changes budgets, or charges a payment method.

Remaining red-team work before handling sensitive real-client data: authenticated deployment, storage-layer access tests, deletion verification, and an independent security review.
