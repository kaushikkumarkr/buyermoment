# Google AI Max planning adapter

Google AI Max is planning-only in the current service build. The product owns a provider-neutral `CampaignOutcome` shape and a dedicated `GoogleAiMaxOutcome` contract so a later importer can retain:

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

The planning module also emits AI Max suitability, search-intent themes, landing-page/URL controls, brand controls, exclusions, conversion/value requirements, and an experiment recommendation. It must map each imported row to an immutable `experiment_id` and `buyer_moment_id`, and preserve the platform export filename, account/campaign identifiers, reporting window, currency, and import timestamp. OAuth, bid management, campaign creation, and Google-specific claims are out of scope until an approved integration path is available.

Official references reviewed on 2026-09-22: [AI Max setup](https://support.google.com/google-ads/answer/15909989?hl=en), [AI Max reporting](https://developers.google.com/google-ads/api/docs/campaigns/ai-max-for-search-campaigns/ai-max-reporting), [AI Max experiments](https://support.google.com/google-ads/answer/16450159?hl=en), and [offline conversions](https://support.google.com/google-ads/answer/10029210?hl=en).
