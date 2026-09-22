# BuyerMoment dogfood report

Business: BuyerMoment

Evidence analyzed: 10
Raw Buyer Moments: 30
Supported candidates: 30
Top candidates: 5
TEST candidates: 0

## Top-ranked Buyer Moments

### 1. SaaS marketer translating customer situations into AI-ad context — Buyer Moment Discovery
- Buyer Moment ID: `buyermoment-moment-saas-marketer-context-bm-buyer-moments`
- Situation: A B2B SaaS marketer is deciding which customer situations are specific enough to test in an AI advertising channel.
- Commerciality: 0.75
- Test readiness: 0.6076452702702703
- Proposed decision: ABSTAIN
- Human approval required: true
- Evidence: BuyerMoment is positioned as commercial-context intelligence for AI advertising, not a generic copywriter, ad network, or autonomous media buyer.; The repository implements a deterministic ContextFit scorer with budget, feature, location, stage, and ad-relevance reasoning codes.; SpendDecision supports TEST, WATCH, ABSTAIN, and BLOCK, with human approval required.; Candidate commercial situation: SaaS marketer translating customer situations into AI-ad context

### 2. Marketer converting customer research into a test — TestReadiness and SpendDecision
- Buyer Moment ID: `buyermoment-moment-evidence-to-experiment-bm-test-readiness`
- Situation: A marketer has website, product, and customer evidence and wants to know which situation is actionable now.
- Commerciality: 0.75
- Test readiness: 0.692875
- Proposed decision: ABSTAIN
- Human approval required: true
- Evidence: Human approval remains mandatory and live advertising is not launched by the current product.; SpendDecision supports TEST, WATCH, ABSTAIN, and BLOCK, with human approval required.; The product architecture includes a Business Analyzer to produce commercial contexts from business evidence.; Candidate commercial situation: Marketer converting customer research into a test

### 3. SaaS marketer translating customer situations into AI-ad context — TestReadiness and SpendDecision
- Buyer Moment ID: `buyermoment-moment-saas-marketer-context-bm-test-readiness`
- Situation: A B2B SaaS marketer is deciding which customer situations are specific enough to test in an AI advertising channel.
- Commerciality: 0.75
- Test readiness: 0.6000777027027027
- Proposed decision: ABSTAIN
- Human approval required: true
- Evidence: BuyerMoment is positioned as commercial-context intelligence for AI advertising, not a generic copywriter, ad network, or autonomous media buyer.; The repository implements a deterministic ContextFit scorer with budget, feature, location, stage, and ad-relevance reasoning codes.; SpendDecision supports TEST, WATCH, ABSTAIN, and BLOCK, with human approval required.; Candidate commercial situation: SaaS marketer translating customer situations into AI-ad context

### 4. Advertiser linking context hypotheses to outcomes — Buyer Moment Discovery
- Buyer Moment ID: `buyermoment-moment-measurement-learning-bm-buyer-moments`
- Situation: An advertiser wants to learn whether commercial-context quality predicts useful experiment outcomes.
- Commerciality: 0.75
- Test readiness: 0.5867500000000001
- Proposed decision: ABSTAIN
- Human approval required: true
- Evidence: The repository has no real advertiser interviews, accepted external experiments, live campaigns, or campaign outcomes recorded yet.; The MVP includes a ChatGPT Ads hypothesis package generator and JSON export; it does not claim a live platform integration.; The repository contains CCB-1 real-data normalization, hidden splits, calibration reports, and failure taxonomy artifacts.; Candidate commercial situation: Advertiser linking context hypotheses to outcomes

### 5. SaaS marketer translating customer situations into AI-ad context — Business Analyzer
- Buyer Moment ID: `buyermoment-moment-saas-marketer-context-bm-business-analyzer`
- Situation: A B2B SaaS marketer is deciding which customer situations are specific enough to test in an AI advertising channel.
- Commerciality: 0.75
- Test readiness: 0.5962939189189189
- Proposed decision: ABSTAIN
- Human approval required: true
- Evidence: BuyerMoment is positioned as commercial-context intelligence for AI advertising, not a generic copywriter, ad network, or autonomous media buyer.; The repository implements a deterministic ContextFit scorer with budget, feature, location, stage, and ad-relevance reasoning codes.; SpendDecision supports TEST, WATCH, ABSTAIN, and BLOCK, with human approval required.; Candidate commercial situation: SaaS marketer translating customer situations into AI-ad context

## Rejected or unsupported

No candidate is treated as an observed customer fact when its evidence is inference-only.

## Evidence gaps

- number of paying customers
- revenue
- conversion rate
- ROI
- campaign performance
- willingness to pay
- whether advertisers can control context-hint experiments sufficiently

## Risks

- No campaign outcome evidence exists yet.
- Commercial situations are hypotheses until validated with an advertiser or campaign.
