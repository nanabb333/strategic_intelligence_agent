"""Provider-independent evidence retrieval pipeline."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from typing import Any

from evidence_normalizer import normalize_retrieved_document
from evidence_provider import BaseEvidenceProvider, RetrievedDocument, provider_registry
from evidence_retrieval import EvidenceItem


class EvidenceRetrievalError(RuntimeError):
    """Raised when the retrieval pipeline cannot complete."""


def retrieve_from_provider(
    *,
    query: str,
    provider_name: str,
    limit: int = 5,
    retry_count: int = 0,
) -> dict[str, Any]:
    """Run search, retrieval, parsing, and normalization for one provider.

    This function does not rank, reason, accept evidence, or update projects.
    """
    provider = provider_registry.get(provider_name)
    return retrieve_with_provider(
        query=query,
        provider=provider,
        limit=limit,
        retry_count=retry_count,
    )


def retrieve_with_provider(
    *,
    query: str,
    provider: BaseEvidenceProvider,
    limit: int = 5,
    retry_count: int = 0,
) -> dict[str, Any]:
    """Run the provider-independent retrieval foundation."""
    clean_query = " ".join(query.split())
    if not clean_query:
        raise ValueError("Query is required.")

    retrieved_at = _now()
    errors: list[dict[str, str]] = []
    results = _retry(lambda: provider.search(clean_query, limit=limit), retry_count=retry_count)
    documents: list[RetrievedDocument] = []
    items: list[EvidenceItem] = []

    for result in results[:limit]:
        try:
            document = _retry(lambda result=result: provider.retrieve(result), retry_count=retry_count)
            document = _with_retrieved_at(document, retrieved_at)
            documents.append(document)
            items.append(normalize_retrieved_document(document, query=clean_query))
        except Exception as exc:
            errors.append(
                {
                    "provider": provider.provider_name,
                    "source_url": result.source_url,
                    "error": str(exc),
                }
            )

    return {
        "query": clean_query,
        "provider": provider.metadata(),
        "retrieved_at": retrieved_at,
        "results": [asdict(result) for result in results[:limit]],
        "documents_retrieved": len(documents),
        "items": [asdict(item) for item in items],
        "errors": errors,
    }


def _retry(operation: Any, *, retry_count: int) -> Any:
    attempts = max(0, retry_count) + 1
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            return operation()
        except Exception as exc:
            last_error = exc
    raise EvidenceRetrievalError(str(last_error)) from last_error


def _with_retrieved_at(document: RetrievedDocument, retrieved_at: str) -> RetrievedDocument:
    if document.retrieved_at:
        return document
    return RetrievedDocument(
        title=document.title,
        source_url=document.source_url,
        source_name=document.source_name,
        source_type=document.source_type,
        html=document.html,
        text=document.text,
        description=document.description,
        published_at=document.published_at,
        author=document.author,
        canonical_url=document.canonical_url,
        retrieved_at=retrieved_at,
        metadata=document.metadata,
    )


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")
