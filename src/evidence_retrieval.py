"""User-triggered evidence retrieval candidate for Version 4.5.

This module intentionally uses a deterministic local provider. It creates
reviewable evidence candidates only; it does not browse autonomously, monitor
sources, or influence decisions directly.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any
from uuid import uuid4


DEFAULT_ALLOWED_TIERS = {"Tier 1 Official", "Tier 2 Company", "Tier 3 Reputable News"}


@dataclass
class RetrievedEvidenceItem:
    title: str
    source_name: str
    source_url: str
    source_type: str
    published_at: str
    retrieved_at: str
    excerpt: str
    status: str
    credibility_tier: str
    freshness_note: str


def retrieve_evidence(
    *,
    query: str,
    project_id: str = "",
    allowed_sources: list[str] | None = None,
) -> dict[str, Any]:
    """Return deterministic review-queue evidence candidates for a user query."""
    clean_query = query.strip()
    if not clean_query:
        raise ValueError("Query is required.")

    retrieved_at = _now()
    allowed = _allowed_tiers(allowed_sources or [])
    items = [
        item
        for item in _local_provider_items(clean_query, retrieved_at)
        if item.credibility_tier in allowed
    ]
    return {
        "retrieval_id": f"retrieval_{uuid4().hex[:10]}",
        "query": clean_query,
        "project_id": project_id,
        "retrieved_at": retrieved_at,
        "items": [asdict(item) for item in items],
    }


def source_tier(source_name: str, source_url: str = "", source_type: str = "") -> str:
    """Classify source credibility with deterministic source-category rules."""
    value = " ".join([source_name, source_url, source_type]).lower()
    tokens = {token.strip(".,:/_-") for token in value.split()}
    if any(
        marker in value
        for marker in [
            ".gov",
            "government",
            "regulator",
            "court",
            "central bank",
            "sec.gov",
            "official statistics",
            "federal reserve",
            "commerce department",
        ]
    ):
        return "Tier 1 Official"
    if any(
        marker in value
        for marker in [
            "annual report",
            "10-k",
            "10-q",
            "investor relations",
            "press release",
            "company announcement",
        ]
    ):
        return "Tier 2 Company"
    if any(marker in value for marker in ["reuters", "associated press", "ft.com", "financial times", "wsj", "bloomberg"]) or tokens & {"ap", "ft"}:
        return "Tier 3 Reputable News"
    if any(marker in value for marker in ["academic", "imf", "world bank", "oecd", "nber", "journal"]):
        return "Tier 4 Research"
    return "Tier 5 Other"


def _allowed_tiers(allowed_sources: list[str]) -> set[str]:
    if not allowed_sources:
        return set(DEFAULT_ALLOWED_TIERS)
    normalized = {item.strip() for item in allowed_sources if item and item.strip()}
    if "Tier 5 Other" not in normalized and "Other" not in normalized:
        normalized.discard("Tier 5 Other")
    expanded = set()
    for item in normalized:
        if item.startswith("Tier "):
            expanded.add(item)
        elif item == "Official":
            expanded.add("Tier 1 Official")
        elif item == "Company":
            expanded.add("Tier 2 Company")
        elif item == "Reputable News":
            expanded.add("Tier 3 Reputable News")
        elif item == "Research":
            expanded.add("Tier 4 Research")
        elif item == "Other":
            expanded.add("Tier 5 Other")
    return expanded or set(DEFAULT_ALLOWED_TIERS)


def _local_provider_items(query: str, retrieved_at: str) -> list[RetrievedEvidenceItem]:
    clean = " ".join(query.split())
    candidates = [
        {
            "title": f"Official policy status relevant to {clean}",
            "source_name": "Official Government Release",
            "source_url": "https://www.commerce.gov/",
            "source_type": "Government / regulator",
            "published_at": retrieved_at[:10],
            "excerpt": f"Official-source candidate for reviewer validation of current policy status related to {clean}.",
        },
        {
            "title": f"Company disclosure signal for {clean}",
            "source_name": "Investor Relations Press Release",
            "source_url": "https://example.com/investor-relations",
            "source_type": "Company press release",
            "published_at": retrieved_at[:10],
            "excerpt": f"Company-source candidate describing management exposure, disclosure, or operating implications related to {clean}.",
        },
        {
            "title": f"Reuters-style news context for {clean}",
            "source_name": "Reuters",
            "source_url": "https://www.reuters.com/",
            "source_type": "Reputable news",
            "published_at": retrieved_at[:10],
            "excerpt": f"News-source candidate for corroborating market and stakeholder context related to {clean}.",
        },
        {
            "title": f"Research background for {clean}",
            "source_name": "OECD Research",
            "source_url": "https://www.oecd.org/",
            "source_type": "Research",
            "published_at": retrieved_at[:10],
            "excerpt": f"Research-source candidate for broader structural context related to {clean}.",
        },
        {
            "title": f"Open web commentary for {clean}",
            "source_name": "Independent Blog",
            "source_url": "https://example.com/blog",
            "source_type": "Blog",
            "published_at": retrieved_at[:10],
            "excerpt": f"Lower-tier open-web candidate related to {clean}; excluded by default unless explicitly allowed.",
        },
    ]
    items = []
    for candidate in candidates:
        tier = source_tier(
            candidate["source_name"],
            candidate["source_url"],
            candidate["source_type"],
        )
        items.append(
            RetrievedEvidenceItem(
                **candidate,
                retrieved_at=retrieved_at,
                status="Retrieved",
                credibility_tier=tier,
                freshness_note=_freshness_note(candidate["published_at"], retrieved_at),
            )
        )
    return items


def _freshness_note(published_at: str, retrieved_at: str) -> str:
    if published_at == retrieved_at[:10]:
        return "Retrieved candidate is dated today; reviewer should verify source details before acceptance."
    return "Retrieved candidate should be checked for current relevance before acceptance."


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")
