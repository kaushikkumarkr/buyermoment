# Service full-flow validation

Local integration tests cover:

```text
client
→ evidence source/chunks
→ client-filtered retrieval
→ preliminary/business package
→ Buyer Moments
→ ContextFit/TestReadiness/SpendDecision
→ OfferFit/LandingPageFit
→ Experiment Portfolio
→ human-approval-gated AdExperiment
→ ChatGPT Ads plan
→ Google AI Max planning contract
→ manual outcome lineage contract
→ measurement audit
→ client report / next-best experiment
```

Automated result at capture: `22 backend tests passed`, including a FastAPI/ASGI service flow and three synthetic full-flow businesses. These are local fixtures, not external customer validation.
