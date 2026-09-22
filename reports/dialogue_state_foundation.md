# Dialogue-state foundation

BuyerMoment's existing `ConversationState` is the current deterministic/stateful baseline. The Phase 6 authored-control run remains the only local state benchmark currently available:

| Metric | Result |
|---|---:|
| Stateful stage accuracy | 0.625 |
| Stateful transition accuracy | 0.55 |
| Constraint/identity memory | 1.0 |
| Intent-reversal actionability | 1.0 |
| Stale-context error | 0.0 |

These are 96 authored journeys / 576 turns, not external human dialogue validation. SGD/SGD-X and Taskmaster are registered for future dialogue-mechanics evaluation, but are not downloaded or trained on while their rights status is `REVIEW_REQUIRED`. ConvApparel V2 is likewise deferred. No compact commercial-intent/stage model is accepted because the current labels are controlled or source-domain-specific rather than a rights-cleared B2B gold set.

The existing `ConversationState` remains production-compatible as a regression baseline; it is not promoted as evidence of B2B SaaS generalization.
