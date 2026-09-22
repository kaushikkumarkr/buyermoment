export type EvidenceKind = 'observed' | 'inference' | 'hypothesis' | 'result'
export type BusinessId = 'northline-footwear' | 'kindred-skin' | 'signaldesk'

export type Evidence = { id: string; kind: EvidenceKind; text: string; source: string; confidence: number }
export type Product = { id: string; name: string; category: string; description: string; price: number; currency: string; features: string[]; serviceRegions: string[]; evidence: Evidence[] }
export type Moment = {
  id: string; title: string; problem: string; situation: string; desiredOutcome: string; stage: string; score: number; confidence: number; productFit: number; constraintMatch: number; locationFit: number; commerciality: number; adRelevance: number; whyExperiment: string; constraints: string[]; location: string; product: Product; evidence: Evidence[]; reasonCodes: string[]
}
export type Business = { id: BusinessId; name: string; category: string; website: string; description: string; products: Product[]; moments: Moment[] }

const evidence = (id: string, kind: EvidenceKind, text: string, source: string, confidence = 0.98): Evidence => ({ id, kind, text, source, confidence })
const product = (id: string, name: string, category: string, description: string, price: number, features: string[], regions: string[], source: string): Product => ({ id, name, category, description, price, currency: 'USD', features, serviceRegions: regions, evidence: [evidence(`${id}-evidence`, 'observed', source, 'product_catalog')] })

const northlineBoot = product('northline-peakshield', 'PeakShield GTX', 'Hiking boots', 'Waterproof hiking boots with slip-resistant outsole and cushioned ankle support for wet trails.', 139, ['waterproof', 'slip-resistant', 'cushioned support'], ['US', 'Canada'], 'Product catalog lists waterproof construction, slip-resistant outsole, and $139 price.')
const northlineLite = product('northline-ridgeline', 'Ridgeline Hiker', 'Hiking boots', 'Lightweight day-hike boot with durable traction for maintained trails.', 119, ['slip-resistant', 'lightweight'], ['US'], 'Product catalog lists lightweight build, traction, and $119 price.')
const calmSet = product('kindred-calm-set', 'Calm Start Set', 'Skincare', 'A fragrance-free cleanser, barrier serum, and moisturizer for sensitive skin.', 72, ['fragrance-free', 'sensitive skin', 'barrier support'], ['US', 'Canada'], 'Product catalog lists fragrance-free formulas and a $72 set price.')
const barrier = product('kindred-barrier-cream', 'Barrier Cloud Cream', 'Moisturizer', 'Fragrance-free daily moisturizer for dry and reactive skin.', 34, ['fragrance-free', 'sensitive skin'], ['US'], 'Product catalog lists fragrance-free ingredients and a $34 price.')
const signalCore = product('signaldesk-core', 'SignalDesk Core', 'Support analytics', 'Customer support analytics with conversation tagging, trend alerts, and SOC 2 controls.', 599, ['SOC 2', 'conversation tagging', 'trend alerts'], ['US', 'Canada', 'UK'], 'Product brief lists SOC 2 controls, conversation tagging, and $599 monthly plan.')
const signalTeam = product('signaldesk-team', 'SignalDesk Team', 'Support analytics', 'A smaller support analytics workspace for growing teams with secure shared views.', 299, ['SOC 2', 'shared views'], ['US', 'Canada'], 'Product brief lists SOC 2 controls and shared views on the $299 plan.')

const moment = (id: string, title: string, problem: string, situation: string, desiredOutcome: string, stage: string, score: number, productFit: number, constraintMatch: number, locationFit: number, commerciality: number, adRelevance: number, constraints: string[], location: string, product: Product, whyExperiment: string): Moment => ({
  id, title, problem, situation, desiredOutcome, stage, score, confidence: 0.86, productFit, constraintMatch, locationFit, commerciality, adRelevance, whyExperiment, constraints, location, product,
  evidence: [product.evidence[0], evidence(`${id}-inference`, 'inference', `Candidate situation: ${situation}`, 'buyer_moment_discovery', 0.73)],
  reasonCodes: ['BUYING_LANGUAGE', 'FEATURE_MATCH', constraints.some((c) => c.includes('$')) ? 'BUDGET_MATCH' : 'TIMING_SIGNAL'],
})

export const businesses: Business[] = [
  { id: 'northline-footwear', name: 'Northline Footwear', category: 'Footwear / ecommerce', website: 'demo.northline.example', description: 'Technical trail footwear for day hikes and wet-weather travel.', products: [northlineBoot, northlineLite], moments: [
    moment('northline-moment-1', 'Waterproof trail confidence under $150', 'Hikers need dependable footwear for wet, variable terrain without crossing a clear budget ceiling.', 'Planning a Yellowstone trip with a concrete destination, feature requirement, and price constraint.', 'Find a waterproof, slip-resistant boot that can ship in time for the trip.', 'consideration', 0.87, 0.92, 0.96, 0.78, 0.88, 0.89, ['waterproof', 'slip-resistant', 'under $150'], 'Yellowstone · US', northlineBoot, 'Strong constraints plus a clear product match make this a useful testable hypothesis; it is not a profitability claim.'),
    moment('northline-moment-2', 'Lightweight traction for maintained trails', 'Day hikers want less bulk without giving up predictable traction.', 'Exploring an upcoming day hike and narrowing down lightweight options.', 'Choose a lightweight boot with enough grip for maintained trails.', 'exploration', 0.64, 0.74, 0.62, 0.78, 0.58, 0.61, ['lightweight', 'traction'], 'US', northlineLite, 'A lower-intent opportunity that could be useful as a contrast test against the higher-intent trip-planning moment.'),
  ] },
  { id: 'kindred-skin', name: 'Kindred Skin', category: 'Skincare / ecommerce', website: 'demo.kindred.example', description: 'Fragrance-free skincare designed for sensitive routines.', products: [calmSet, barrier], moments: [
    moment('kindred-moment-1', 'A low-friction sensitive-skin routine', 'People with sensitive skin need a simple routine that avoids fragrance and stays within a manageable spend.', 'Actively evaluating a routine with a skin constraint and a budget.', 'Build a gentle, fragrance-free starter routine with clear product roles.', 'consideration', 0.84, 0.91, 0.94, 0.8, 0.86, 0.86, ['fragrance-free', 'sensitive skin', 'under $80'], 'US', calmSet, 'The product evidence directly covers the constraint set; confirm current formula and availability before testing.'),
    moment('kindred-moment-2', 'Barrier support without the full routine', 'Dry and reactive skin can make a single-product trial more approachable than a bundle.', 'Looking for a simple moisturizer before committing to a full routine.', 'Try a fragrance-free daily moisturizer with a smaller first step.', 'comparison', 0.72, 0.84, 0.8, 0.8, 0.72, 0.75, ['fragrance-free', 'single product'], 'US', barrier, 'This creates a clear package-vs-entry-point experiment, while staying honest about no proven conversion lift.'),
  ] },
  { id: 'signaldesk', name: 'SignalDesk', category: 'B2B SaaS', website: 'demo.signaldesk.example', description: 'Support intelligence for teams that want customer evidence in the operating rhythm.', products: [signalCore, signalTeam], moments: [
    moment('signaldesk-moment-1', 'Support analytics that clears security review', 'A small support team needs actionable analytics without creating a security or implementation project.', 'A team is evaluating a B2B tool against a compliance and timing constraint.', 'Shortlist a tool the team can adopt this quarter and take through security review.', 'comparison', 0.81, 0.9, 0.78, 0.83, 0.79, 0.82, ['SOC 2', '30-person team', 'this quarter'], 'North America', signalTeam, 'A clear buying committee constraint and verified compliance evidence make this a credible experiment hypothesis.'),
    moment('signaldesk-moment-2', 'Turn support conversations into a weekly signal', 'Support leaders want a shared view of recurring customer friction before it becomes churn risk.', 'Exploring a shift from ad-hoc reporting to a repeatable customer-evidence rhythm.', 'Create a shared weekly view with trend alerts and conversation tags.', 'exploration', 0.69, 0.8, 0.62, 0.83, 0.61, 0.72, ['trend alerts', 'shared views'], 'US · Canada · UK', signalCore, 'A broader exploration context; use it to learn which job language creates qualified interest before narrowing the audience.'),
  ] },
]

export function buildExperiment(moment: Moment) {
  return {
    id: `exp-${moment.id}`,
    hypothesis: `People in the ${moment.situation.toLowerCase()} will find ${moment.product.name} relevant when the ad reflects ${moment.constraints.join(', ')}.`,
    channel: 'ChatGPT Ads',
    targetProduct: moment.product.name,
    offer: moment.product.category === 'Skincare' ? 'Routine bundle · 10% off' : moment.product.category === 'Support analytics' ? '30-day pilot' : 'Free US shipping',
    contextHints: [moment.situation, ...moment.constraints, moment.location],
    successMetric: 'Qualified landing-page sessions that reach the primary product CTA',
    stopRule: 'Pause after 500 qualified sessions or 14 days if CTA rate is below baseline',
    copy: [
      `${moment.desiredOutcome} Explore ${moment.product.name}, with the details in view.`,
      `Built around ${moment.constraints.join(', ')} — see if ${moment.product.name} fits.`,
      'Evidence-backed relevance is the test. Review the product details before you commit.',
    ],
    tracking: { utm_source: 'chatgpt_ads', utm_medium: 'conversation', bm_buyer_moment: moment.id, bm_experiment: `exp-${moment.id}` },
  }
}

