# Blinded shadow-pilot packet generation

{
  "businesses": 5,
  "candidates": 50,
  "candidates_per_business": {
    "northline-footwear": 10,
    "kindred-skin": 10,
    "signaldesk": 10,
    "lumen-local-services": 10,
    "trailwise-learning": 10
  },
  "review_split": {
    "shadow_dev": 30,
    "shadow_holdout": 20
  },
  "review_packets": "shadow_reviews/private/reviewer_packets.jsonl",
  "model_predictions": "shadow_reviews/private/model_predictions.jsonl",
  "blindness": "model decision and score are excluded from reviewer packets",
  "status": "packets prepared; no independent human submissions yet"
}

Reviewer packets contain business evidence and candidate context only. Predictions are stored separately and joined only after reviewer submission. Five packages are included, but the two added verticals are explicitly synthetic scenarios; no private customer data is committed.
