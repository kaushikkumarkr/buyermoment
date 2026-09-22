from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
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


class AzureOpenAIChatProvider:
    """Small stdlib-only Azure OpenAI adapter used by offline data jobs.

    Authentication is deliberately supplied at runtime through a bearer token or API
    key.  No credential is read from or written to the repository.
    """

    name = "azure_openai"

    def __init__(self, *, endpoint: str, deployment: str, api_version: str, bearer_token: str | None = None, api_key: str | None = None) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.deployment = deployment
        self.api_version = api_version
        self.bearer_token = bearer_token
        self.api_key = api_key
        self.last_usage: dict[str, int] = {}
        if not bearer_token and not api_key:
            raise ValueError("AzureOpenAIChatProvider requires a runtime bearer token or API key")

    @classmethod
    def from_environment(cls, *, role: str = "bulk_generator") -> "AzureOpenAIChatProvider":
        deployment = os.environ.get(
            f"BUYERMOMENT_AZURE_OPENAI_DEPLOYMENT_{role.upper()}",
            os.environ.get("BUYERMOMENT_AZURE_OPENAI_DEPLOYMENT", ""),
        )
        return cls(
            endpoint=os.environ["BUYERMOMENT_AZURE_OPENAI_ENDPOINT"],
            deployment=deployment,
            api_version=os.environ.get("BUYERMOMENT_AZURE_OPENAI_API_VERSION", "2025-04-01-preview"),
            bearer_token=os.environ.get("AZURE_OPENAI_BEARER_TOKEN"),
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        )

    def generate(self, prompt: str, *, role: str) -> str:
        if not self.deployment:
            raise ValueError(f"No Azure deployment configured for role {role}")
        # Current Azure OpenAI v1 routing uses the deployment name in `model`.
        # Keep api_version as configuration metadata for older compatible adapters,
        # but do not force the legacy deployment URL for new Foundry deployments.
        url = f"{self.endpoint}/openai/v1/chat/completions"
        body = json.dumps({
            "messages": [
                {"role": "system", "content": "Return only valid JSON. Follow the requested schema exactly."},
                {"role": "user", "content": prompt},
            ],
            "model": self.deployment,
            "temperature": 0.2,
            "max_completion_tokens": 1200,
            "response_format": {"type": "json_object"},
        }).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["api-key"] = self.api_key
        else:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:1000]
            raise RuntimeError(f"Azure OpenAI request failed ({exc.code}): {detail}") from exc
        self.last_usage = payload.get("usage", {})
        return payload["choices"][0]["message"]["content"]
