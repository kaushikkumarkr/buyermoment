from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IsotonicCalibrator:
    """Small dependency-free isotonic calibrator for validation-only score fitting."""

    thresholds: tuple[float, ...]
    values: tuple[float, ...]
    default: float = 0.5

    @classmethod
    def fit(cls, scores: list[float], labels: list[bool]) -> "IsotonicCalibrator":
        if len(scores) != len(labels) or not scores:
            return cls((), (), 0.5)
        pairs = sorted((max(0.0, min(1.0, score)), float(label)) for score, label in zip(scores, labels, strict=True))
        blocks: list[list[float]] = []
        for score, label in pairs:
            blocks.append([score, score, 1.0, label])
            while len(blocks) > 1 and blocks[-2][3] > blocks[-1][3]:
                left, right = blocks[-2], blocks[-1]
                total = left[2] + right[2]
                merged = [left[0], right[1], total, (left[3] * left[2] + right[3] * right[2]) / total]
                blocks[-2:] = [merged]
        return cls(tuple(block[1] for block in blocks), tuple(block[3] for block in blocks), sum(labels) / len(labels))

    def predict(self, score: float) -> float:
        if not self.thresholds:
            return self.default
        bounded = max(0.0, min(1.0, score))
        for threshold, value in zip(self.thresholds, self.values, strict=True):
            if bounded <= threshold:
                return value
        return self.values[-1]


def brier(scores: list[float], labels: list[bool]) -> float | None:
    if not scores:
        return None
    return sum((score - float(label)) ** 2 for score, label in zip(scores, labels, strict=True)) / len(scores)


def expected_calibration_error(scores: list[float], labels: list[bool], bins: int = 10) -> float | None:
    if not scores:
        return None
    total = len(scores)
    error = 0.0
    for index in range(bins):
        lower, upper = index / bins, (index + 1) / bins
        selected = [(score, label) for score, label in zip(scores, labels, strict=True) if lower <= score < upper or (index == bins - 1 and score == upper)]
        if selected:
            error += len(selected) / total * abs(sum(item[0] for item in selected) / len(selected) - sum(float(item[1]) for item in selected) / len(selected))
    return error


def confidence_band(score: float | None) -> str | None:
    if score is None:
        return None
    return "LOW" if score < 0.6 else ("MEDIUM" if score < 0.8 else "HIGH")


def calibrated_fields(raw_score: float, calibrator: IsotonicCalibrator) -> dict[str, float | str]:
    calibrated = calibrator.predict(raw_score)
    return {"raw_confidence": raw_score, "calibrated_confidence": calibrated, "confidence_band": confidence_band(calibrated) or "LOW"}
