"""URL text extraction utilities for evidence retrieval."""

from __future__ import annotations

import trafilatura
from fastapi import HTTPException

from evidence_provider import EvidenceFetchError, SearchResult, URLEvidenceProvider


def fetch_url_text(source_url: str) -> str:
    """Fetch readable webpage text for Paste Link mode."""
    if not source_url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=400,
            detail="Please paste a full http:// or https:// URL, or paste the article text directly.",
        )

    try:
        document = URLEvidenceProvider(timeout_seconds=15.0).retrieve(
            SearchResult(title=source_url, source_url=source_url)
        )
    except EvidenceFetchError as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not read webpage content from this link. Please paste the article text or upload a file. "
                "This local app only analyzes a link when readable page text can be fetched."
            ),
        ) from exc

    text = document.text or trafilatura.extract(document.html)

    if not text or len(text.strip()) < 300:
        raise HTTPException(
            status_code=400,
            detail="No readable article content was detected. Please paste article text or upload a file.",
        )

    return text.strip()
