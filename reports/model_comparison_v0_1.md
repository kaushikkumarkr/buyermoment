# CCB-1 v0.1 bounded model comparison

Same five real parents were sent to two Azure-direct deployments. This is a guardrail comparison, not a human quality verdict.

| configuration | schema validity | token-overlap proxy | mean latency (ms) | total tokens | dollar cost / 1,000 |
|---|---:|---:|---:|---:|---:|
| gpt-5.4-nano / bulk_generator | 1.0 | 0.784615 | 4663.63 | 4136 | not computed |
| gpt-5.4-mini / extractor | 1.0 | 0.900000 | 3582.26 | 3852 | not computed |

- Original ESCI/WANDS labels remain ground truth; no LLM judge was used.
- Token overlap is only a semantic-preservation guardrail proxy.
- Dollar cost is intentionally null until a dated official Azure price configuration is added.
