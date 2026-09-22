# ChatGPT Ads adapter

BuyerMoment currently produces a human-reviewable experiment package and context-hint export. It does not call an undocumented campaign API, access private ChatGPT conversations, or launch campaigns.

The current official Ads Manager Beta workflow supports campaigns, ad groups, ads, context hints, bulk upload, CSV reporting, and conversion measurement. Context hints describe useful situations and help relevance; they are not exact-match keywords, targeting rules, or delivery guarantees. Advertisers receive aggregated performance reporting rather than users' private chats.

Implemented:

- platform-neutral `AdExperiment` with immutable `experiment_id` → `buyer_moment_id` lineage;
- JSON hypothesis package;
- context-hint CSV for human review;
- manual outcome import for impressions, clicks, spend, and conversions;
- explicit `human_approval_required=true`.

The exporter labels the package `template_mapping_required=true` because Ads Manager bulk-upload templates and fields can evolve. A user must map the package to the current Ads Manager template and approve it in the official UI. No live launch is performed by BuyerMoment.

Official references reviewed on 2026-09-22:

- [Ads Manager Beta Overview](https://help.openai.com/en/articles/20001206-ads-manager-beta-overview)
- [Write Context Hints for ChatGPT Ads](https://help.openai.com/en/articles/20001521-write-context-hints-for-chatgpt-ads)
- [Bulk Upload Campaign Schema Checklist](https://help.openai.com/en/articles/20001218)
- [Measure Results](https://help.openai.com/en/articles/20001214-measure-results)
- [Conversion Measurement](https://help.openai.com/en/articles/20001409-conversion-measurement)
- [Ads in ChatGPT: The Basics](https://help.openai.com/en/articles/20001207)
