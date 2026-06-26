"""URL text extraction utilities for evidence retrieval."""

from __future__ import annotations

import requests
import trafilatura
from fastapi import HTTPException


def fetch_url_text(source_url: str) -> str:
    """Fetch readable webpage text for Paste Link mode."""
    if not source_url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=400,
            detail="Please paste a full http:// or https:// URL, or paste the article text directly.",
        )

    try:
        response = requests.get(
            source_url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 Chrome/137 Safari/537.36"
                )
            },
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not read webpage content from this link. Please paste the article text or upload a file. "
                "This local app only analyzes a link when readable page text can be fetched."
            ),
        ) from exc

    text = trafilatura.extract(response.text)

    if not text or len(text.strip()) < 300:
        raise HTTPException(
            status_code=400,
            detail="No readable article content was detected. Please paste article text or upload a file.",
        )

    return text.strip()