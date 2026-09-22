# Phase 5 pilot gate

## Decision: `SHADOW-GO`, live spend `NO-GO`

The deterministic Phase 5 gate is eligible for an offline shadow review only. It is not approved to influence live advertising spend.

Measured evidence:

- TEST-vs-WATCH hidden TEST precision: 1.0000; TEST coverage: 0.1667; Waste-Risk Rate: 0.0000.
- Adversarial v2 hidden TEST precision: 1.0000; TEST recall: 0.4750; Waste-Risk Rate and hard-negative FPR: 0.0000.
- The harder 360-turn multi-turn stress set has stage accuracy 0.6944 and stale-context error rate 0.1053.
- The 60-case counterfactual stress set has decision consistency 0.8000, with conditional and cancelled-intent groups still failing.
- The 45-candidate demo-business shadow proxy has only 0.0889 agreement with the existing non-blinded reviewer proxy and is not independent validation.

Therefore the result is not a live pilot approval. A future shadow run needs independent, blinded human labels, a reviewed gold tranche, and targeted fixes for multi-turn/current-state errors. Human approval remains mandatory.
