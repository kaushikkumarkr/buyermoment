# Adversarial v2 benchmark

This is a manually authored and provenance-preserving robustness set. It is not a customer or revenue outcome claim.

```json
{
  "benchmark": "Phase 4 adversarial v2",
  "record_count": 300,
  "validation_count": 150,
  "hidden_count": 150,
  "template_types": 30,
  "integrity": {
    "duplicate_context_count": 0,
    "source_category_split_violations": 0
  },
  "purchase_stage": {
    "accuracy": 0.5666666666666667,
    "macro_f1": 0.6256410256410255
  },
  "spend_safety": {
    "decision_accuracy": 0.7666666666666667,
    "commercial_intent_f1": 0.47619047619047616,
    "test_precision": 0.8333333333333334,
    "test_recall": 0.625,
    "waste_risk_rate": 0.045454545454545456,
    "hard_negative_fpr": 0.045454545454545456,
    "abstain_rate": 0.26666666666666666,
    "block_accuracy": 1.0
  },
  "by_category": {
    "third_party_buying": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "TEST": 10
      }
    },
    "gift_buying": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "TEST": 10
      }
    },
    "research_only": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "ABSTAIN": 10
      }
    },
    "existing_support": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "negative_alternatives": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "TEST": 10
      }
    },
    "competitor_research": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "ABSTAIN": 10
      }
    },
    "future_intent": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "ABSTAIN": 10
      }
    },
    "conditional_intent": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "ABSTAIN": 10
      }
    },
    "company_gathering": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "ABSTAIN": 10
      }
    },
    "budget_mismatch": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "location_mismatch": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "mixed_commercial": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 0.0,
      "predicted_decisions": {
        "WATCH": 10
      }
    },
    "ambiguous_pronoun": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 0.0,
      "predicted_decisions": {
        "WATCH": 10
      }
    },
    "multiple_users": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "TEST": 10
      }
    },
    "location_change": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "budget_change": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "intent_reversal": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "sarcasm": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 0.0,
      "predicted_decisions": {
        "WATCH": 10
      }
    },
    "hypothetical": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 0.0,
      "predicted_decisions": {
        "TEST": 10
      }
    },
    "professional_research": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "ABSTAIN": 10
      }
    },
    "return_request": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "availability_buy": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "TEST": 10
      }
    },
    "unavailable_product": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "shipping_deadline": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "language_mismatch": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "BLOCK": 10
      }
    },
    "team_comparison": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 0.0,
      "predicted_decisions": {
        "WATCH": 10
      }
    },
    "popular_research": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "ABSTAIN": 10
      }
    },
    "complaint": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 1.0,
      "predicted_decisions": {
        "ABSTAIN": 10
      }
    },
    "direct_gift": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 0.0,
      "predicted_decisions": {
        "WATCH": 10
      }
    },
    "research_then_buy": {
      "stage_accuracy": 0.0,
      "decision_accuracy": 0.0,
      "predicted_decisions": {
        "WATCH": 10
      }
    }
  },
  "failure_count": 170,
  "status": "measured on manually authored Phase 4 adversarial controls; no customer outcome claim"
}
```
