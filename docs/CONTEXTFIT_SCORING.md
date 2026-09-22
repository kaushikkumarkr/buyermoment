# ContextFit score decomposition

ContextFit keeps semantic fit, exact constraint matching, serviceability, offer fit, and ad appropriateness separate. The deterministic v0.1 aggregate is:

`overall = 0.30*commerciality + 0.25*semantic_product_fit + 0.20*constraint_match + 0.10*location_fit + 0.15*ad_relevance`

`semantic_product_fit` is the lexical candidate-fit component currently exposed as `product_fit` for backwards compatibility. `ad_relevance` is intentionally not a copy of product fit: it combines commerciality, urgency, and offer fit. `offer_fit` is passed independently and defaults to a neutral 0.7 when no offer evidence is supplied.

`raw_confidence` is the scorer's internal certainty heuristic. It is not a probability. `calibrated_confidence` and `confidence_band` are populated only after fitting the validation-only calibration layer in `scripts/calibrate_contextfit.py`; customer-facing code must not treat the raw value as a probability.

Every reason code and recommendation must retain the observed or inferred evidence that supports it. Missing serviceability, currency, or offer evidence lowers certainty or remains explicitly unconfirmed; it must not be silently converted into a fact.
