from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol



class ModelProvider(Protocol):
    name: str

    def generate(self, prompt: str, *, role: str) -> str: ...


class StorageProvider(Protocol):
    def put_json(self, key: str, value: dict) -> str: ...

    def get_json(self, key: str) -> dict: ...


class EmbeddingProvider(Protocol):
    def embed(self, texts: Iterable[str]) -> list[list[float]]: ...


class DeterministicProvider:
    """Offline fallback used when no Azure deployment is configured."""

    name = "deterministic"

    def generate(self, prompt: str, *, role: str) -> str:
        return f"[{role}] No model configured; deterministic fallback retained the input for review."
