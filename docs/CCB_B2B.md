# CCB-B2B v0.1

CCB-B2B is a B2B SaaS commercial-context benchmark scaffold focused on CRM, Sales, Marketing Automation, Analytics / BI, Accounting / Finance, Procurement, Project Management, DevOps, Cybersecurity, HR / Payroll, and Customer Support.

## Quality boundary

The current queue contains controlled, evidence-tagged `SILVER` scenarios. They are useful for schema checks, deterministic rule tests, and review prioritization, but they are not observed customer conversations and none are `GOLD` or `HUMAN_REVIEWED`. A human review workflow must promote records only after inspecting the scenario, evidence, and proposed labels.

## Fields

Records cover company size, industry, buyer role, recipient, current stack/vendor, pain, outcome, integrations/features, budget/contract preference, security/compliance, migration, timing, procurement status, authority, geography, stage, commerciality, actionability, fit, evidence, provenance, quality tier, and review status. The Pydantic contract is `buyermoment.b2b.B2BCommercialContextRecord`.

## Prohibited use

Do not use the current silver queue as evidence of B2B advertising lift, willingness to pay, customer demand, or market prevalence. Do not call it gold because labels are internally consistent. Real client evidence and independent human review remain required.
