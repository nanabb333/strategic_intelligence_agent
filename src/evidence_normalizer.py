"""Normalize retrieved documents into the existing EvidenceItem schema."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from evidence_parser import ParsedDocument, parse_html_document, parse_text_document
from evidence_provider import RetrievedDocument
from evidence_retrieval import EvidenceItem, normalize_evidence_item


def normalize_retrieved_document(document: RetrievedDocument | ParsedDocument | dict[str, Any], *, query: str = "") -> EvidenceItem:
    """Convert a retrieved or parsed document into the shared EvidenceItem type."""
    parsed = _to_parsed_document(document)
    body = parsed.raw_body or parsed.description
    payload = {
        "title": parsed.title or "Untitled retrieved evidence",
        "source_type": parsed.source_type or "Retrieved evidence",
        "source_name": parsed.source_name,
        "source_url": parsed.canonical_url or parsed.source_url,
        "publisher": parsed.source_name,
        "author": parsed.author,
        "published_at": parsed.published_at,
        "retrieved_at": parsed.retrieved_at,
        "excerpt": body[:900],
        "summary": (parsed.description or body)[:900],
        "status": "Retrieved",
    }
    return normalize_evidence_item(payload, query=query, retrieved_at=parsed.retrieved_at)


def normalize_retrieved_documents(
    documents: list[RetrievedDocument | ParsedDocument | dict[str, Any]],
    *,
    query: str = "",
) -> list[EvidenceItem]:
    """Normalize multiple retrieved documents deterministically."""
    return [normalize_retrieved_document(document, query=query) for document in documents]


def _to_parsed_document(document: RetrievedDocument | ParsedDocument | dict[str, Any]) -> ParsedDocument:
    if isinstance(document, ParsedDocument):
        return document
    if isinstance(document, RetrievedDocument):
        if document.html:
            parsed = parse_html_document(
                document.html,
                source_url=document.source_url,
                source_name=document.source_name,
                source_type=document.source_type,
                retrieved_at=document.retrieved_at,
            )
            return _overlay_retrieved_metadata(parsed, document)
        return parse_text_document(
            document.text or document.description,
            title=document.title,
            description=document.description,
            published_at=document.published_at,
            author=document.author,
            canonical_url=document.canonical_url,
            source_url=document.source_url,
            source_name=document.source_name,
            source_type=document.source_type,
            retrieved_at=document.retrieved_at,
            metadata=document.metadata,
        )
    payload = _dict_payload(document)
    return _to_parsed_document(RetrievedDocument(**payload))


def _overlay_retrieved_metadata(parsed: ParsedDocument, document: RetrievedDocument) -> ParsedDocument:
    return ParsedDocument(
        title=parsed.title or document.title,
        description=parsed.description or document.description,
        published_at=parsed.published_at or document.published_at,
        author=parsed.author or document.author,
        canonical_url=parsed.canonical_url or document.canonical_url,
        raw_body=parsed.raw_body or document.text,
        source_url=document.source_url,
        source_name=document.source_name,
        source_type=document.source_type,
        retrieved_at=document.retrieved_at,
        metadata={**document.metadata, **parsed.metadata},
    )


def _dict_payload(document: dict[str, Any]) -> dict[str, Any]:
    payload = asdict(document) if is_dataclass(document) else dict(document)
    allowed = set(RetrievedDocument.__dataclass_fields__)
    return {key: payload.get(key, "") for key in allowed}
