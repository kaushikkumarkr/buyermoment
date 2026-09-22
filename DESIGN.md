# BuyerMoment design system

BuyerMoment is a signal board for commercial-context intelligence. The interface should feel like a calm research console: a paper-colored workspace for evidence, ink typography for clarity, violet for model-derived signal, coral for hypotheses, and green only for verified/nominal states.

## World

- Surface: `#fbfafc` paper with white evidence panels and a charcoal experiment lab.
- Ink: `#17131f`; muted copy is violet-gray rather than neutral gray to preserve contrast.
- Signal: violet `#7653d6` for product-fit and inference; coral `#e87961` for hypotheses.
- Typography: Calistoga for editorial headings, IBM Plex Sans for operations copy, JetBrains Mono for scores/IDs.
- Depth: quiet 1px borders plus soft shadows; no hard offset shadows or decorative glass.

## Signal Board composition

The first viewport is an investigation surface: ranked Buyer Moment list at left, selected detail/evidence trail in the center, and experiment intent on the right. Business selection is a compact popover. Evidence tabs use type labels, confidence, source, and kind rather than color alone.

## Interaction

- Selected moment cards keep context visible while the detail pane changes.
- The experiment panel only generates a hypothesis package; the UI explicitly says it does not launch a campaign.
- Reduced motion is respected. Hover states use short color/shadow transitions without layout shifts.
- Mobile collapses the board into ranked moments, detail, and experiment sections without horizontal scrolling.

## Content rules

Observed evidence, model inference, hypothesis, and campaign result are different labels and types. Never state a Buyer Moment is profitable; call it a candidate or evidence-backed opportunity until real campaign outcomes exist.

