from __future__ import annotations

import json
from pathlib import Path

from .commercial import BusinessEvidencePackage
from .models import BusinessProfile, Evidence


def load_package(path: Path) -> BusinessEvidencePackage:
    raw = json.loads(path.read_text())
    business = BusinessProfile.model_validate(raw["business"])
    evidence = [
        Evidence.model_validate(item)
        for item in [
            *raw["business"].get("evidence", []),
            *[e for product in raw["business"]["products"] for e in product.get("evidence", [])],
            *[e for offer in raw["business"].get("offers", []) for e in offer.get("evidence", [])],
        ]
    ]
    raw["evidence_store"] = evidence
    raw["business"] = business
    return BusinessEvidencePackage.model_validate(raw)
