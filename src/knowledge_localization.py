"""English-only knowledge text compatibility helpers."""

from __future__ import annotations

from typing import Any


def localize_knowledge_text(text: str, language: str) -> str:
    """Return curated knowledge text unchanged for the official English product."""
    if language != "en":
        raise ValueError(f"Unsupported language: {language}")
    return text


def localize_analysis_payload(payload: dict[str, Any], language: str) -> dict[str, Any]:
    """Return analysis artifacts unchanged for English output."""
    if language != "en":
        raise ValueError(f"Unsupported language: {language}")
    return payload
