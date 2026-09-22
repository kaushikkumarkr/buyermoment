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
    "decision_accuracy": 0.7266666666666667,
    "commercial_intent_f1": 0.40425531914893614,
    "test_precision": 1.0,
    "test_recall": 0.475,
    "waste_risk_rate": 0.0,
    "hard_negative_fpr": 0.0,
    "abstain_rate": 0.26666666666666666,
    "block_accuracy": 1.0
  },
  "by_category": {
    "third_party_buying": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 0.9,
      "predicted_decisions": {
        "TEST": 9,
        "WATCH": 1
      }
    },
    "gift_buying": {
      "stage_accuracy": 1.0,
      "decision_accuracy": 0.9,
      "predicted_decisions": {
        "TEST": 9,
        "WATCH": 1
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
      "decision_accuracy": 0.2,
      "predicted_decisions": {
        "WATCH": 8,
        "TEST": 2
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
      "decision_accuracy": 0.9,
      "predicted_decisions": {
        "TEST": 9,
        "WATCH": 1
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
        "WATCH": 10
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
      "decision_accuracy": 0.0,
      "predicted_decisions": {
        "WATCH": 10
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
      "decision_accuracy": 0.9,
      "predicted_decisions": {
        "TEST": 9,
        "WATCH": 1
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
  "failure_count": 182,
  "status": "measured on manually authored Phase 4 adversarial controls; no customer outcome claim"
}
```
