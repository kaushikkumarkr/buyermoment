# TestReadiness benchmark

{
  "benchmark": "Phase 5 TEST-vs-WATCH and TestReadiness",
  "policy": {
    "version": "phase5-v1",
    "min_test_overall": 0.7,
    "min_test_confidence": 0.68,
    "min_test_actionability": 0.2,
    "min_watch_overall": 0.5,
    "min_watch_confidence": 0.5,
    "min_test_readiness": 0.75,
    "min_test_evidence_strength": 0.65,
    "max_test_ambiguity": 0.05,
    "require_immediate_signal": true,
    "human_approval_required": true
  },
  "validation": {
    "count": 12,
    "test_precision": 1.0,
    "test_recall": 0.5,
    "test_coverage": 0.25,
    "watch_precision": 0.5714285714285714,
    "watch_recall": 0.6666666666666666,
    "waste_risk_rate": 0.0,
    "false_abstention_rate": 0.0,
    "decision_distribution": {
      "TEST": 3,
      "WATCH": 7,
      "ABSTAIN": 2,
      "BLOCK": 0
    },
    "mean_evidence_strength_test": 0.7388888888888889,
    "mean_evidence_strength_watch": 0.7250000000000001,
    "mean_ambiguity_test": 0.008333333333333333,
    "mean_ambiguity_watch": 0.26666666666666666
  },
  "hidden": {
    "count": 12,
    "test_precision": 1.0,
    "test_recall": 0.3333333333333333,
    "test_coverage": 0.16666666666666666,
    "watch_precision": 0.5555555555555556,
    "watch_recall": 0.8333333333333334,
    "waste_risk_rate": 0.0,
    "false_abstention_rate": 0.0,
    "decision_distribution": {
      "TEST": 2,
      "WATCH": 9,
      "ABSTAIN": 1,
      "BLOCK": 0
    },
    "mean_evidence_strength_test": 0.7805555555555556,
    "mean_evidence_strength_watch": 0.7388888888888889,
    "mean_ambiguity_test": 0.008333333333333333,
    "mean_ambiguity_watch": 0.11666666666666665
  },
  "top_validation_candidates": [
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.2,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.05,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.3,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.05,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.35,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.05,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.2,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.1,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.3,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.1,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.35,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.1,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.2,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.15,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.3,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.15,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.35,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.15,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.2,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.2,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.3,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.2,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.35,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.2,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.2,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.3,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.3,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.3,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.35,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.3,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.2,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.45,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.3,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.45,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.35,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.55,
        "max_test_ambiguity": 0.45,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.2,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.6,
        "max_test_ambiguity": 0.05,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    },
    {
      "policy": {
        "version": "phase5-v1",
        "min_test_overall": 0.7,
        "min_test_confidence": 0.68,
        "min_test_actionability": 0.3,
        "min_watch_overall": 0.5,
        "min_watch_confidence": 0.5,
        "min_test_readiness": 0.55,
        "min_test_evidence_strength": 0.6,
        "max_test_ambiguity": 0.05,
        "require_immediate_signal": true,
        "human_approval_required": true
      },
      "metrics": {
        "count": 12,
        "test_precision": 1.0,
        "test_recall": 0.5,
        "test_coverage": 0.25,
        "watch_precision": 0.5714285714285714,
        "watch_recall": 0.6666666666666666,
        "waste_risk_rate": 0.0,
        "false_abstention_rate": 0.0,
        "decision_distribution": {
          "TEST": 3,
          "WATCH": 7,
          "ABSTAIN": 2,
          "BLOCK": 0
        },
        "mean_evidence_strength_test": 0.7388888888888889,
        "mean_evidence_strength_watch": 0.7250000000000001,
        "mean_ambiguity_test": 0.008333333333333333,
        "mean_ambiguity_watch": 0.26666666666666666
      }
    }
  ],
  "status": "manually authored readiness controls; no campaign outcome claim"
}

Threshold selection maximized validation TEST coverage among candidates with validation TEST precision at least 0.90 while retaining the empirically conservative confidence floor of 0.68. The hidden result is reported without retuning.
