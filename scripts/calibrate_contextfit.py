from __future__ import annotations

import argparse
import json
from pathlib import Path

from buyermoment.calibration import IsotonicCalibrator, brier, confidence_band, expected_calibration_error
from buyermoment.models import CommercialContextRecord, Product
from buyermoment.scoring import build_context, score
from evaluate_contextfit import relevance_gain

def read_rows(path: Path):
    with path.open() as stream:
        for line in stream:
            if line.strip():
                yield CommercialContextRecord.model_validate_json(line)

def predictions(path: Path, kind: str) -> tuple[list[float], list[bool]]:
    scores: list[float] = []
    labels: list[bool] = []
    for row in read_rows(path):
        product = Product(id=row.product_id or row.record_id, name=row.product_title or "unknown", category="unknown", description=row.product_description or row.product_title or "unknown", features=[])
        result = score(build_context(row.context_text), product)
        if kind == "stage":
            if row.purchase_stage and row.metadata.get("label_origin") in {"controlled_variant_target", "controlled_hard_negative_target", "manual_phase3_control"}:
                scores.append(result.confidence)
                labels.append(result.purchase_stage == row.purchase_stage)
        elif kind == "relevance":
            gain = relevance_gain(row)
            if gain is not None:
                scores.append(result.product_fit)
                labels.append(gain > 0)
    return scores, labels

def reliability(scores: list[float], labels: list[bool], bins: int = 10) -> list[dict[str, float | int]]:
    result = []
    for index in range(bins):
        lower, upper = index / bins, (index + 1) / bins
        selected = [(score, label) for score, label in zip(scores, labels, strict=True) if lower <= score < upper or (index == bins - 1 and score == upper)]
        if selected:
            result.append({"bin": f"{lower:.2f}-{upper:.2f}", "count": len(selected), "mean_confidence": sum(item[0] for item in selected) / len(selected), "accuracy": sum(float(item[1]) for item in selected) / len(selected)})
    return result

def measure(scores: list[float], labels: list[bool], calibrator: IsotonicCalibrator | None = None) -> dict:
    calibrated = [calibrator.predict(score) for score in scores] if calibrator else scores
    return {"count": len(scores), "ece": expected_calibration_error(calibrated, labels), "brier": brier(calibrated, labels), "reliability": reliability(calibrated, labels), "calibrator": {"thresholds": calibrator.thresholds, "values": calibrator.values, "default": calibrator.default} if calibrator else None, "confidence_bands": {band: sum(1 for value in calibrated if confidence_band(value) == band) for band in ("LOW", "MEDIUM", "HIGH")}}

def main() -> None:
    parser = argparse.ArgumentParser(description="Fit validation-only calibration and evaluate on the corrected hidden split.")
    parser.add_argument("--validation", type=Path, default=Path("data/ccb1/validation/real.jsonl"))
    parser.add_argument("--hidden", type=Path, default=Path("data/ccb1/hidden_test/real.jsonl"))
    parser.add_argument("--json-output", type=Path, default=Path("artifacts/calibration_report.json"))
    parser.add_argument("--report-output", type=Path, default=Path("reports/calibration_report.md"))
    args = parser.parse_args()
    output = {}
    for kind in ("stage", "relevance"):
        validation_scores, validation_labels = predictions(args.validation, kind)
        hidden_scores, hidden_labels = predictions(args.hidden, kind)
        calibrator = IsotonicCalibrator.fit(validation_scores, validation_labels)
        output[kind] = {"validation_raw": measure(validation_scores, validation_labels), "hidden_raw": measure(hidden_scores, hidden_labels), "hidden_calibrated": measure(hidden_scores, hidden_labels, calibrator), "calibration_fit": "validation split only"}
    output["interpretation"] = "Raw confidence is not a probability. Calibrated values are empirical estimates fitted on validation and must be recalibrated when data, prompts, or scorer logic change."
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.report_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(output, indent=2) + "\n")
    args.report_output.write_text("# ContextFit calibration report\n\n" + json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
