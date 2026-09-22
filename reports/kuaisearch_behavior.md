# KuaiSearch behavioral benchmark status

KuaiSearch-Lite is a promising behavioral architecture source because it separates relevance, clicks, and purchases. The official public repository documents the Lite subset and ranking schema, but the current repository does not have a verified dataset license/checksum recorded in the rights registry.

Therefore this phase does not download, train, or report KuaiSearch metrics. It remains `REVIEW_REQUIRED`. The intended future benchmark is isolated from BuyerMoment B2B semantics:

```text
query/context + item/features → click likelihood → purchase likelihood
```

It must not be used to claim that Chinese ecommerce behavior predicts B2B SaaS ad actionability. No production use: `NO`.

Source: <https://github.com/benchen4395/KuaiSearch>.
