# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: React + Vite TypeScript frontend, FastAPI Python backend, SQLite-friendly local development with Azure-ready service interfaces. Chosen for a fast evidence-first MVP with provider-neutral seams.

## Users

Growth, marketing, and commercial strategy teams who need to decide which customer contexts deserve an advertising experiment. Internal model/evaluation users need to inspect benchmark quality and provenance.

## Product Purpose

BuyerMoment turns business evidence and customer context into ranked, evidence-backed commercial opportunities and structured AI-ad experiments. Success means a user can trace every recommendation from source evidence through scoring to a clearly labeled experiment hypothesis.

## Positioning

The product's core asset is commercial-context intelligence, not ad copy or campaign operations: it measures whether a moment is commercially relevant, how close the person may be to buying, and whether a product/offer is appropriate to test.

## Operating Context

Users import a business URL, product catalog, reviews, search terms, and optional customer/support evidence; inspect ranked Buyer Moments; open supporting evidence and component scores; then create and export a platform-specific experiment package.

## Capabilities and Constraints

- CCB-1 is versioned, source-attributed, and separated into raw, normalized, augmented, gold, train, validation, and hidden-test data.
- CommercialContext and scoring outputs are strongly validated and preserve evidence/provenance.
- Observed evidence, model inference, hypotheses, and real campaign results must never be conflated in the UI or data model.
- The first adapter is a structured ChatGPT Ads experiment export; no fake live ad integration is claimed.
- Azure is offline computation and deployment fuel, not a business-logic dependency. No large batch or Azure resource should be created without a cost check.

## Brand Commitments

BuyerMoment. Voice is precise, evidence-first, commercially literate, and candid about uncertainty.

## Evidence on Hand

The launch repository begins with synthetic/demo business evidence for footwear ecommerce, skincare ecommerce, and B2B SaaS. No campaign performance results, customer testimonials, or benchmark claims are available yet and must not be fabricated.

## Product Principles

1. Evidence before inference.
2. Inference before experiment.
3. Real outcomes before claims.
4. Deterministic checks for deterministic facts.
5. Provider-neutral data and model seams.

## Accessibility & Inclusion

The web MVP should meet WCAG AA contrast, keyboard navigation, visible focus states, semantic labels, reduced-motion support, and responsive layouts at mobile and desktop widths.
