# Google AI Max future adapter

Google AI Max is intentionally not integrated in Phase 7. The product owns a provider-neutral `CampaignOutcome` shape and a dedicated `GoogleAiMaxOutcome` contract so a later importer can retain:

```text
search term
headline
landing page
campaign
ad group
date
impressions
clicks
cost
conversions
conversion value
```

The future adapter must map each row to an immutable `experiment_id` and `buyer_moment_id`. It must preserve the platform export filename, account/campaign identifiers, reporting window, currency, and import timestamp. OAuth, bid management, campaign creation, and Google-specific claims are out of scope until official documentation and an approved integration path are available.
