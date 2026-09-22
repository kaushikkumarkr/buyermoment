from __future__ import annotations

import re
from pathlib import Path


MAX_EVIDENCE_BYTES = 2_000_000
ALLOWED_UPLOAD_SUFFIXES = {".txt", ".md", ".csv", ".json", ".html", ".htm", ".pdf", ".docx"}

_INJECTION_PATTERNS = (
    r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions",
    r"reveal\s+(?:the\s+)?system\s+prompt",
    r"use\s+another\s+client",
    r"send\s+(?:the\s+)?(?:credentials|api\s+key|secret)",
    r"change\s+(?:the\s+)?(?:campaign|ad)\s+budget",
    r"disregard\s+(?:your|the)\s+instructions",
)


def detect_prompt_injection(text: str) -> list[str]:
    """Flag untrusted content; callers must still treat it as data, never instructions."""
    lowered = text.lower()
    return [pattern for pattern in _INJECTION_PATTERNS if re.search(pattern, lowered)]


def safe_filename(filename: str) -> str:
    candidate = Path(filename).name
    if candidate in {"", ".", ".."}:
        raise ValueError("filename is required")
    suffix = Path(candidate).suffix.lower()
    if suffix not in ALLOWED_UPLOAD_SUFFIXES:
        raise ValueError(f"unsupported file type: {suffix or 'none'}")
    if len(candidate) > 180:
        raise ValueError("filename is too long")
    return candidate


def validate_upload_size(content: bytes) -> None:
    if len(content) > MAX_EVIDENCE_BYTES:
        raise ValueError(f"file exceeds {MAX_EVIDENCE_BYTES} byte limit")


def redact_pii_hint(text: str) -> str:
    """Conservative log-safe preview; raw evidence is never placed in logs."""
    return re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[email-redacted]", text)[:240]
