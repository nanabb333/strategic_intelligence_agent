"""User-triggered evidence foundations for Sprint 2.

This module provides deterministic evidence normalization, validation, ranking,
and provider boundaries. It creates reviewable evidence items only; it does not
browse autonomously, monitor sources, or influence decisions directly.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha1
from typing import Any, Protocol
from uuid import uuid4

from evidence_lifecycle import RETRIEVED, lifecycle_metadata
from evidence_provider import URLEvidenceProvider, is_url


DEFAULT_ALLOWED_TIERS = {"Tier 1 Official", "Tier 2 Company", "Tier 3 Reputable News"}
SUPPORTED_SOURCE_TYPES = {
    "blog",
    "company press release",
    "government / regulator",
    "manual note",
    "reputable news",
    "research",
    "retrieved evidence",
}
VALIDATION_VALID = "Valid"
VALIDATION_NEEDS_REVIEW = "Needs Review"
VALIDATION_DUPLICATE = "Duplicate"
VALIDATION_WEAK = "Weak Metadata"


@dataclass
class EvidenceItem:
    """Normalized evidence record used at provider and project boundaries."""

    evidence_id: str
    title: str
    source_type: str
    source_name: str
    source_url: str
    publisher: str
    author: str
    published_at: str
    retrieved_at: str
    excerpt: str
    summary: str
    credibility_tier: str
    credibility_score: float
    freshness_note: str
    relevance_score: float
    validation_status: str
    validation_notes: list[str]
    conflict_status: str
    trace_id: str
    status: str
    lifecycle_state: str
    reviewer_status: str
    reviewer_note: str
    reviewed_at: str
    review_reason: str
    evidence_action: str


class EvidenceProvider(Protocol):
    """Minimal provider boundary for user-triggered evidence collection."""

    provider_name: str

    def retrieve(self, query: str, *, retrieved_at: str) -> list[dict[str, Any]]:
        """Return raw evidence-like records for normalization."""


class ExistingRetrievedEvidenceProvider:
    """Deterministic local provider used by the current review queue."""

    provider_name = "existing_local_candidates"

    def retrieve(self, query: str, *, retrieved_at: str) -> list[dict[str, Any]]:
        return _local_provider_candidates(query, retrieved_at)


class ManualEvidenceProvider:
    """Provider adapter for reviewer-entered evidence records."""

    provider_name = "manual_project_evidence"

    def __init__(self, items: list[dict[str, Any]]) -> None:
        self.items = items

    def retrieve(self, query: str, *, retrieved_at: str) -> list[dict[str, Any]]:
        return [{**item, "retrieved_at": item.get("retrieved_at") or retrieved_at} for item in self.items]


class LocalDocumentEvidenceProvider:
    """Provider adapter for local document excerpts supplied by the user."""

    provider_name = "local_document_evidence"

    def __init__(self, title: str, text: str, source_name: str = "Local document") -> None:
        self.title = title
        self.text = text
        self.source_name = source_name

    def retrieve(self, query: str, *, retrieved_at: str) -> list[dict[str, Any]]:
        excerpt = " ".join(self.text.split())[:600]
        return [
            {
                "title": self.title,
                "source_type": "Manual note",
                "source_name": self.source_name,
                "retrieved_at": retrieved_at,
                "excerpt": excerpt,
                "summary": excerpt,
                "status": "Reviewed",
            }
        ]


def retrieve_evidence(
    *,
    query: str,
    project_id: str = "",
    allowed_sources: list[str] | None = None,
    provider: EvidenceProvider | None = None,
) -> dict[str, Any]:
    """Return deterministic review-queue evidence candidates for a user query."""
    clean_query = query.strip()
    if not clean_query:
        raise ValueError("Query is required.")

    retrieved_at = _now()
    allowed = _allowed_tiers(allowed_sources or [])

    if provider is None and is_url(clean_query):
        return _retrieve_url_evidence(
            query=clean_query,
            project_id=project_id,
            allowed=allowed,
        )

    provider = provider or ExistingRetrievedEvidenceProvider()
    normalized_items = normalize_evidence_items(
        provider.retrieve(clean_query, retrieved_at=retrieved_at),
        query=clean_query,
        retrieved_at=retrieved_at,
    )
    items = [
        item
        for item in rank_evidence_items(normalized_items)
        if item.credibility_tier in allowed
    ]
    return {
        "retrieval_id": f"retrieval_{uuid4().hex[:10]}",
        "query": clean_query,
        "project_id": project_id,
        "retrieved_at": retrieved_at,
        "items": [asdict(item) for item in items],
    }


def _retrieve_url_evidence(*, query: str, project_id: str, allowed: set[str]) -> dict[str, Any]:
    """Retrieve one explicit URL through the provider-independent pipeline."""
    from evidence_retriever import retrieve_with_provider

    response = retrieve_with_provider(
        query=query,
        provider=URLEvidenceProvider(),
        limit=1,
        retry_count=0,
    )
    normalized = [EvidenceItem(**item) for item in response.get("items", [])]
    ranked = [
        item
        for item in rank_evidence_items(normalized)
        if item.credibility_tier in allowed
    ]
    if not ranked and response.get("errors"):
        first_error = response["errors"][0].get("error") or "URL could not be retrieved."
        raise ValueError(first_error)
    return {
        "retrieval_id": f"retrieval_{uuid4().hex[:10]}",
        "query": query,
        "project_id": project_id,
        "retrieved_at": response.get("retrieved_at") or _now(),
        "provider": response.get("provider", {}),
        "errors": response.get("errors", []),
        "items": [asdict(item) for item in ranked],
    }


def normalize_evidence_item(
    payload: dict[str, Any],
    *,
    query: str = "",
    retrieved_at: str = "",
) -> EvidenceItem:
    """Normalize one raw evidence-like record without calling external services."""
    clean = {key: _clean(value) for key, value in payload.items()}
    now = retrieved_at or clean.get("retrieved_at") or _now()
    title = clean.get("title") or "Untitled evidence"
    excerpt = clean.get("excerpt") or clean.get("text_excerpt") or clean.get("summary") or ""
    summary = clean.get("summary") or excerpt
    source_type = clean.get("source_type") or "Retrieved evidence"
    source_name = clean.get("source_name") or clean.get("publisher") or ""
    source_url = clean.get("source_url") or ""
    tier = clean.get("credibility_tier") or source_tier(source_name, source_url, source_type)
    basis = "|".join([title, source_name, source_url, excerpt])
    digest = sha1(basis.encode("utf-8")).hexdigest()[:12]
    relevance = _relevance_score(query, " ".join([title, excerpt, summary]))
    validation_notes = _validation_notes(
        title=title,
        source_type=source_type,
        source_name=source_name,
        source_url=source_url,
        published_at=clean.get("published_at") or "",
        excerpt=excerpt,
    )
    conflict_status = _conflict_status(clean)
    lifecycle = lifecycle_metadata(clean, default_state=RETRIEVED)
    return EvidenceItem(
        evidence_id=clean.get("evidence_id") or f"ev_{digest}",
        title=title,
        source_type=source_type,
        source_name=source_name,
        source_url=source_url,
        publisher=clean.get("publisher") or source_name,
        author=clean.get("author") or "",
        published_at=clean.get("published_at") or "",
        retrieved_at=now,
        excerpt=excerpt,
        summary=summary,
        credibility_tier=tier,
        credibility_score=_credibility_score(tier),
        freshness_note=clean.get("freshness_note") or _freshness_note(clean.get("published_at") or "", now),
        relevance_score=relevance,
        validation_status=_validation_status(validation_notes),
        validation_notes=validation_notes,
        conflict_status=conflict_status,
        trace_id=clean.get("trace_id") or f"trace_{digest}",
        status=clean.get("status") or "Retrieved",
        lifecycle_state=lifecycle["lifecycle_state"],
        reviewer_status=lifecycle["reviewer_status"],
        reviewer_note=lifecycle["reviewer_note"],
        reviewed_at=lifecycle["reviewed_at"],
        review_reason=lifecycle["review_reason"],
        evidence_action=lifecycle["evidence_action"],
    )


def normalize_evidence_items(
    items: list[dict[str, Any]],
    *,
    query: str = "",
    retrieved_at: str = "",
) -> list[EvidenceItem]:
    """Normalize a collection and mark deterministic duplicate title or URL matches."""
    normalized = [
        normalize_evidence_item(item, query=query, retrieved_at=retrieved_at)
        for item in items
    ]
    seen_urls: dict[str, int] = {}
    seen_titles: dict[str, int] = {}
    for index, item in enumerate(normalized):
        url_key = item.source_url.lower()
        title_key = item.title.lower()
        duplicate = False
        if url_key and url_key in seen_urls:
            duplicate = True
            item.validation_notes.append("Duplicate source URL.")
        if title_key and title_key in seen_titles:
            duplicate = True
            item.validation_notes.append("Duplicate title.")
        if duplicate:
            item.validation_status = VALIDATION_DUPLICATE
        seen_urls.setdefault(url_key, index)
        seen_titles.setdefault(title_key, index)
    return normalized


def rank_evidence_items(items: list[EvidenceItem]) -> list[EvidenceItem]:
    """Rank evidence deterministically using source, freshness, relevance, and validation."""
    return sorted(
        items,
        key=lambda item: (
            evidence_rank_score(item),
            item.credibility_score,
            item.relevance_score,
            item.published_at,
            item.title.lower(),
        ),
        reverse=True,
    )


def evidence_rank_score(item: EvidenceItem) -> float:
    """Return an internal deterministic ranking score."""
    score = 0.0
    score += item.credibility_score * 0.35
    score += _freshness_score(item.published_at, item.retrieved_at) * 0.20
    score += item.relevance_score * 0.20
    score += _completeness_score(item) * 0.15
    score += _validation_score(item.validation_status) * 0.05
    score += _reviewer_status_score(item.status) * 0.05
    return round(score, 3)


def missing_evidence_flags(items: list[EvidenceItem]) -> list[str]:
    """Return deterministic missing-evidence flags based only on available metadata."""
    flags = []
    if not items:
        return ["No accepted or retrieved evidence is available for this decision context."]
    if not any(item.credibility_tier == "Tier 1 Official" for item in items):
        flags.append("No Tier 1 official evidence is present.")
    if not any(item.status in {"Accepted", "Used", "Verified", "Corroborated"} for item in items):
        flags.append("No reviewer-accepted evidence is present.")
    if any(item.validation_status != VALIDATION_VALID for item in items):
        flags.append("At least one evidence item requires metadata review.")
    if any(item.conflict_status != "No Conflict" for item in items):
        flags.append("At least one evidence item is marked as conflicting or potentially conflicting.")
    if any("stale" in " ".join(item.validation_notes).lower() for item in items):
        flags.append("At least one evidence item may be stale.")
    return flags


def confidence_impact_metadata(items: list[EvidenceItem]) -> dict[str, list[str]]:
    """Prepare additive metadata for future confidence explanations."""
    improves = []
    weakens = []
    missing = missing_evidence_flags(items)
    for item in items:
        if item.validation_status == VALIDATION_VALID and item.credibility_tier in DEFAULT_ALLOWED_TIERS:
            improves.append(item.evidence_id)
        if item.validation_status != VALIDATION_VALID or item.conflict_status != "No Conflict":
            weakens.append(item.evidence_id)
    return {
        "confidence_improvers": improves,
        "confidence_reducers": weakens,
        "missing_evidence": missing,
    }


def historical_live_evidence_guidance() -> list[str]:
    """Describe the deterministic boundary between historical and live evidence."""
    return [
        "Historical analogues remain structural context, not current factual proof.",
        "Live evidence provides current factual grounding only after reviewer acceptance.",
        "Conflicts between live evidence and historical patterns should be surfaced, not hidden.",
        "Live evidence should not automatically override historical analogue patterns.",
    ]


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


def _validation_notes(
    *,
    title: str,
    source_type: str,
    source_name: str,
    source_url: str,
    published_at: str,
    excerpt: str,
) -> list[str]:
    notes = []
    if not title or title == "Untitled evidence":
        notes.append("Missing title.")
    if not source_name and not source_url:
        notes.append("Missing source name or URL.")
    if not published_at:
        notes.append("Missing published date.")
    elif _freshness_score(published_at, _now()) <= 0.35:
        notes.append("Evidence may be stale.")
    if not excerpt:
        notes.append("Missing or empty excerpt.")
    if not source_name and not source_url and not source_type:
        notes.append("Weak source metadata.")
    if source_type.lower() not in SUPPORTED_SOURCE_TYPES:
        notes.append("Unsupported or unclassified source type.")
    return notes


def _validation_status(notes: list[str]) -> str:
    if not notes:
        return VALIDATION_VALID
    if any("Unsupported" in note or "Weak source" in note for note in notes):
        return VALIDATION_WEAK
    return VALIDATION_NEEDS_REVIEW


def _conflict_status(payload: dict[str, str]) -> str:
    explicit = (payload.get("conflict_status") or "").strip()
    if explicit:
        return explicit
    status = " ".join([payload.get("status", ""), payload.get("validation_notes", "")]).lower()
    if "conflict" in status or "contradict" in status:
        return "Potential Conflict"
    return "No Conflict"


def _credibility_score(tier: str) -> float:
    return {
        "Tier 1 Official": 1.0,
        "Tier 2 Company": 0.85,
        "Tier 3 Reputable News": 0.75,
        "Tier 4 Research": 0.70,
        "Tier 5 Other": 0.35,
    }.get(tier, 0.35)


def _freshness_score(published_at: str, retrieved_at: str) -> float:
    if not published_at:
        return 0.45
    try:
        published = datetime.fromisoformat(published_at[:10])
        retrieved = datetime.fromisoformat((retrieved_at or _now())[:10])
    except ValueError:
        return 0.45
    age_days = max((retrieved - published).days, 0)
    if age_days <= 30:
        return 1.0
    if age_days <= 180:
        return 0.75
    if age_days <= 365:
        return 0.55
    return 0.25


def _relevance_score(query: str, text: str) -> float:
    query_tokens = _tokens(query)
    if not query_tokens:
        return 0.5
    text_tokens = _tokens(text)
    if not text_tokens:
        return 0.0
    overlap = len(query_tokens & text_tokens) / len(query_tokens)
    return round(min(1.0, overlap), 3)


def _completeness_score(item: EvidenceItem) -> float:
    fields = [
        item.title,
        item.source_type,
        item.source_name or item.source_url,
        item.published_at,
        item.retrieved_at,
        item.excerpt,
        item.summary,
        item.credibility_tier,
    ]
    return round(sum(bool(field) for field in fields) / len(fields), 3)


def _validation_score(status: str) -> float:
    return {
        VALIDATION_VALID: 1.0,
        VALIDATION_NEEDS_REVIEW: 0.65,
        VALIDATION_WEAK: 0.4,
        VALIDATION_DUPLICATE: 0.25,
    }.get(status, 0.4)


def _reviewer_status_score(status: str) -> float:
    return {
        "Used": 1.0,
        "Accepted": 0.9,
        "Verified": 0.9,
        "Corroborated": 0.85,
        "Reviewed": 0.75,
        "Retrieved": 0.55,
        "Archived": 0.2,
    }.get(status, 0.5)


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


def _local_provider_candidates(query: str, retrieved_at: str) -> list[dict[str, Any]]:
    clean = " ".join(query.split())
    return [
        {
            "title": f"Official policy status relevant to {clean}",
            "source_name": "Official Government Release",
            "source_url": "https://www.commerce.gov/",
            "source_type": "Government / regulator",
            "published_at": retrieved_at[:10],
            "retrieved_at": retrieved_at,
            "excerpt": f"Official-source candidate for reviewer validation of current policy status related to {clean}.",
            "status": "Retrieved",
        },
        {
            "title": f"Company disclosure signal for {clean}",
            "source_name": "Investor Relations Press Release",
            "source_url": "https://example.com/investor-relations",
            "source_type": "Company press release",
            "published_at": retrieved_at[:10],
            "retrieved_at": retrieved_at,
            "excerpt": f"Company-source candidate describing management exposure, disclosure, or operating implications related to {clean}.",
            "status": "Retrieved",
        },
        {
            "title": f"Reuters-style news context for {clean}",
            "source_name": "Reuters",
            "source_url": "https://www.reuters.com/",
            "source_type": "Reputable news",
            "published_at": retrieved_at[:10],
            "retrieved_at": retrieved_at,
            "excerpt": f"News-source candidate for corroborating market and stakeholder context related to {clean}.",
            "status": "Retrieved",
        },
        {
            "title": f"Research background for {clean}",
            "source_name": "OECD Research",
            "source_url": "https://www.oecd.org/",
            "source_type": "Research",
            "published_at": retrieved_at[:10],
            "retrieved_at": retrieved_at,
            "excerpt": f"Research-source candidate for broader structural context related to {clean}.",
            "status": "Retrieved",
        },
        {
            "title": f"Open web commentary for {clean}",
            "source_name": "Independent Blog",
            "source_url": "https://example.com/blog",
            "source_type": "Blog",
            "published_at": retrieved_at[:10],
            "retrieved_at": retrieved_at,
            "excerpt": f"Lower-tier open-web candidate related to {clean}; excluded by default unless explicitly allowed.",
            "status": "Retrieved",
        },
    ]


def _freshness_note(published_at: str, retrieved_at: str) -> str:
    if not published_at:
        return "Published date missing; reviewer should verify freshness before acceptance."
    if _freshness_score(published_at, retrieved_at) >= 0.75:
        return "Evidence appears current; reviewer should verify source details before acceptance."
    return "Evidence may be stale and should be checked for current relevance before acceptance."


def _tokens(value: str) -> set[str]:
    return {
        token.strip(".,:;!?()[]{}'\"").lower()
        for token in value.split()
        if len(token.strip(".,:;!?()[]{}'\"")) > 2
    }


def _clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(item).strip() for item in value if str(item).strip())
    return str(value).strip()


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")
