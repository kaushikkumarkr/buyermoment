# Dataset rights and provenance policy

This document records engineering handling decisions, not legal advice. A dataset marked `REVIEW_REQUIRED` is not used to train model weights. Each source must keep its original license/NOTICE/citation alongside any downloaded artifact and in the manifest.

## Current registry decisions

The authoritative machine-readable registry is [`datasets/registry.yaml`](../datasets/registry.yaml). The initial Phase 8 review used the official publisher repositories/cards:

- [Amazon ESCI](https://github.com/amazon-research/esci-code): Apache-2.0 source release with upstream `LICENSE` and `NOTICE`; original relevance labels remain authoritative.
- [Wayfair WANDS](https://github.com/wayfair/WANDS): MIT source repository; original labels remain authoritative.
- [Google ConvApparel](https://huggingface.co/datasets/google/ConvApparel): the current card declares CC BY 4.0 and exposes both V1 and V2 archives. Because this is human conversation data and publication materials/versions must be reconciled, both versions are `REVIEW_REQUIRED` for training.
- [Google SGD / SGD-X](https://github.com/google-research-datasets/dstc8-schema-guided-dialogue): CC BY-SA 4.0. These are dialogue-state evaluation sources, not B2B ground truth; training use remains `REVIEW_REQUIRED` pending commercial-use review.
- [Google Taskmaster](https://github.com/google-research-datasets/Taskmaster): the Taskmaster-1 notice declares CC BY 4.0. Exact subset/version terms must be recorded before training; it remains `REVIEW_REQUIRED`.
- [Amazon Contextual Product QA](https://github.com/amazon-science/contextual-product-qa): CDLA Permissive 1.0 Sharing. It remains `REVIEW_REQUIRED` for weights and `EVAL_ONLY` pending review of Sharing obligations.
- [KuaiSearch](https://github.com/benchen4395/KuaiSearch): the public repository documents the data and citation but does not expose a dataset license clearly enough for this project’s policy. It remains `REVIEW_REQUIRED` and is not downloaded in this phase gate.

## Rules

1. Dataset labels are never replaced with model judgments.
2. `SILVER`, `SYNTHETIC`, or model-proposed labels are not called `GOLD`.
3. Training status is independent from evaluation status; a source may be evaluation-only.
4. Public research data is not private advertising, Google Ads, Amazon Ads, or ChatGPT conversation data.
5. A license decision does not establish that a source is representative of BuyerMoment’s B2B SaaS market or advertising economics.
6. No model artifact may be accepted without recording dataset versions, license dependencies, checksums, and intended/prohibited use.
