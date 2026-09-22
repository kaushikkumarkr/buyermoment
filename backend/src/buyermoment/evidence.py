from __future__ import annotations

import re
from typing import Iterable

from .models import Evidence
from .security import detect_prompt_injection
from .service_models import EvidenceChunk, EvidenceSource


def chunk_source(source: EvidenceSource, *, max_chars: int = 1200) -> list[EvidenceChunk]:
    """Chunk evidence without interpreting it. Retrieved text remains untrusted data."""
    parts = [part.strip() for part in re.split(r"\n\s*\n|(?<=[.!?])\s+", source.text) if part.strip()]
    chunks: list[EvidenceChunk] = []
    current = ""
    ordinal = 0
    for part in parts:
        if current and len(current) + len(part) + 1 > max_chars:
            chunks.append(EvidenceChunk(id=f"{source.id}-chunk-{ordinal}", client_id=source.client_id, source_id=source.id, ordinal=ordinal, text=current))
            ordinal += 1
            current = ""
        current = f"{current} {part}".strip()
    if current:
        chunks.append(EvidenceChunk(id=f"{source.id}-chunk-{ordinal}", client_id=source.client_id, source_id=source.id, ordinal=ordinal, text=current))
    return chunks


def source_from_text(*, source_id: str, client_id: str, source_type: str, title: str, text: str, uri: str | None = None, data_origin: str = "provided", private: bool = True) -> EvidenceSource:
    return EvidenceSource(
        id=source_id,
        client_id=client_id,
        source_type=source_type,  # type: ignore[arg-type]
        title=title,
        text=text,
        uri=uri,
        data_origin=data_origin,  # type: ignore[arg-type]
        private=private,
        prompt_injection_flags=detect_prompt_injection(text),
        provenance={"ingestion": "local_evidence_pipeline_v1", "content_is_untrusted_data": True},
    )


def retrieve(chunks: Iterable[EvidenceChunk], *, client_id: str, query: str, limit: int = 8) -> list[EvidenceChunk]:
    """Client-scoped lexical retrieval; Azure AI Search can implement this interface later."""
    query_terms = {term for term in re.findall(r"[a-z0-9][a-z0-9-]+", query.lower()) if len(term) > 2}
    ranked: list[tuple[int, EvidenceChunk]] = []
    for chunk in chunks:
        if chunk.client_id != client_id:
            continue
        terms = set(re.findall(r"[a-z0-9][a-z0-9-]+", chunk.text.lower()))
        overlap = len(query_terms & terms)
        if overlap:
            ranked.append((overlap, chunk))
    ranked.sort(key=lambda item: (-item[0], item[1].id))
    return [chunk for _, chunk in ranked[:limit]]


def evidence_records(chunks: Iterable[EvidenceChunk], *, source_lookup: dict[str, EvidenceSource]) -> list[Evidence]:
    return [
        Evidence(id=chunk.id, kind="observed", text=chunk.text, source=source_lookup[chunk.source_id].title, source_record_id=chunk.source_id, provenance=[source_lookup[chunk.source_id].uri or chunk.source_id], confidence=0.85)
        for chunk in chunks
        if chunk.source_id in source_lookup
    ]
