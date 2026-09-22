# Abstention threshold analysis

The policy uses validation-selected thresholds and keeps raw confidence separate from calibrated probability. The table below shows the safety/coverage tradeoff on controlled adversarial data.

| Threshold | Validation TEST precision | Validation waste risk | Hidden TEST precision | Hidden waste risk | Hidden coverage |
|---:|---:|---:|---:|---:|---:|
| 0.50 | 1.0 | 0.0 | 0.5 | 0.08333333333333333 | 0.4 |
| 0.60 | 1.0 | 0.0 | 0.5 | 0.08333333333333333 | 0.4 |
| 0.68 | 1.0 | 0.0 | 0.5 | 0.08333333333333333 | 0.4 |
| 0.75 | 1.0 | 0.0 | 0.5 | 0.08333333333333333 | 0.4 |
| 0.80 | 1.0 | 0.0 | 0.5 | 0.08333333333333333 | 0.4 |
| 0.90 | 1.0 | 0.0 | 0.5 | 0.08333333333333333 | 0.4 |
| 0.95 | 1.0 | 0.0 | None | 0.0 | 0.4 |

The selected policy keeps the existing `0.68` raw confidence threshold. This is a safety gate, not a calibrated probability; purchase-stage confidence remains analysis-only until a reliable reviewed calibration set exists.
