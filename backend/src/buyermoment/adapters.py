from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Protocol

from .commercial import AdExperiment
from .planners import chatgpt_ads_bulk_row


class PlatformAdapter(Protocol):
    platform: str

    def export(self, experiment: AdExperiment, output_dir: Path) -> dict[str, str]: ...


class ChatGPTAdsAdapter:
    """Manual/export adapter for the current Ads Manager Beta workflow.

    It intentionally does not call an undocumented API or claim that the generated
    files are upload-ready without mapping them to the current Ads Manager template.
    """

    platform = "chatgpt_ads"

    def export(self, experiment: AdExperiment, output_dir: Path) -> dict[str, str]:
        output_dir.mkdir(parents=True, exist_ok=True)
        payload_path = output_dir / f"{experiment.experiment_id}.json"
        payload_path.write_text(json.dumps({
            "format": "buyermoment_chatgpt_ads_hypothesis_package_v1",
            "manual_import_required": True,
            "template_mapping_required": True,
            "experiment": experiment.model_dump(mode="json"),
        }, indent=2) + "\n")
        context_path = output_dir / f"{experiment.experiment_id}_context_hints.csv"
        with context_path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["experiment_id", "buyer_moment_id", "ad_group_concept", "context_hint"])
            writer.writeheader()
            for hint in experiment.audience_or_context_strategy.context_hints:
                writer.writerow({"experiment_id": experiment.experiment_id, "buyer_moment_id": experiment.buyer_moment_id, "ad_group_concept": experiment.audience_or_context_strategy.commercial_context, "context_hint": hint})
        bulk_path = output_dir / f"{experiment.experiment_id}_bulk_upload.csv"
        row = chatgpt_ads_bulk_row(experiment)
        with bulk_path.open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(row))
            writer.writeheader()
            writer.writerow({**row, "context_hints": json.dumps(row["context_hints"]), "landing_page_url": row["landing_page_url"]})
        return {"package_json": str(payload_path), "context_hints_csv": str(context_path), "bulk_upload_csv": str(bulk_path)}
