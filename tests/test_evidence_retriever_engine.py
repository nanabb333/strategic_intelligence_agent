import pytest

from evidence_normalizer import normalize_retrieved_document
from evidence_parser import parse_html_document
from evidence_provider import (
    BaseEvidenceProvider,
    ProviderRegistry,
    RetrievedDocument,
    SearchResult,
)
from evidence_retriever import EvidenceRetrievalError, retrieve_with_provider


class StaticProvider(BaseEvidenceProvider):
    provider_name = "static_test"
    provider_type = "local_test"

    def __init__(self) -> None:
        self.retrieve_calls = 0

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        return [
            SearchResult(
                title=f"Official update for {query}",
                source_url="https://agency.gov/policy",
                source_name="Official Agency",
                source_type="Government / regulator",
                excerpt="Official policy update.",
            )
        ][:limit]

    def retrieve(self, result: SearchResult) -> RetrievedDocument:
        self.retrieve_calls += 1
        return RetrievedDocument(
            title=result.title,
            source_url=result.source_url,
            source_name=result.source_name,
            source_type=result.source_type,
            html="""
              <html>
                <head>
                  <title>Official policy title</title>
                  <meta name="description" content="Official policy description">
                  <meta name="author" content="Policy Office">
                  <meta property="article:published_time" content="2026-06-30">
                  <link rel="canonical" href="https://agency.gov/policy/canonical">
                </head>
                <body><main>Official policy body about semiconductor export controls.</main></body>
              </html>
            """,
        )


class FailingSearchProvider(BaseEvidenceProvider):
    provider_name = "failing_search"

    def __init__(self) -> None:
        self.calls = 0

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        self.calls += 1
        raise RuntimeError("search unavailable")

    def retrieve(self, result: SearchResult) -> RetrievedDocument:
        raise AssertionError("retrieve should not run")


class PartialFailureProvider(BaseEvidenceProvider):
    provider_name = "partial_failure"

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        return [
            SearchResult(title="Good result", source_url="https://agency.gov/good", source_name="Agency"),
            SearchResult(title="Bad result", source_url="https://agency.gov/bad", source_name="Agency"),
        ]

    def retrieve(self, result: SearchResult) -> RetrievedDocument:
        if "bad" in result.source_url:
            raise RuntimeError("document unavailable")
        return RetrievedDocument(
            title=result.title,
            source_url=result.source_url,
            source_name=result.source_name,
            source_type="Government / regulator",
            text="Official body text for reviewer evidence.",
            published_at="2026-06-30",
        )


def test_provider_registration_and_metadata() -> None:
    registry = ProviderRegistry()
    provider = StaticProvider()

    registry.register(provider)

    assert registry.names() == ["static_test"]
    assert registry.get("static_test") is provider
    assert registry.metadata()[0]["provider_type"] == "local_test"
    assert registry.metadata()[0]["external_api"] is False


def test_parser_extracts_metadata_and_body() -> None:
    parsed = parse_html_document(
        """
        <html><head>
          <title>Market Update</title>
          <meta name="description" content="A concise description">
          <meta name="author" content="Analyst Team">
          <meta property="article:published_time" content="2026-06-29T10:00:00Z">
          <link rel="canonical" href="https://example.com/canonical">
        </head><body><script>ignore()</script><article>Body text here.</article></body></html>
        """,
        source_url="https://example.com/raw",
        source_name="Example Source",
    )

    assert parsed.title == "Market Update"
    assert parsed.description == "A concise description"
    assert parsed.author == "Analyst Team"
    assert parsed.published_at == "2026-06-29T10:00:00Z"
    assert parsed.canonical_url == "https://example.com/canonical"
    assert "Body text here." in parsed.raw_body
    assert "ignore" not in parsed.raw_body


def test_parser_handles_malformed_html_and_missing_metadata() -> None:
    parsed = parse_html_document(
        "<html><head><title>Broken<title><body><article>Readable body",
        source_url="https://example.com/broken",
    )

    assert "Broken" in parsed.title
    assert parsed.source_url == "https://example.com/broken"
    assert "Readable body" in parsed.raw_body
    assert parsed.description == ""
    assert parsed.published_at == ""


def test_normalizer_reuses_existing_evidence_item_schema() -> None:
    document = RetrievedDocument(
        title="Company disclosure",
        source_url="https://example.com/investor-relations",
        source_name="Investor Relations",
        source_type="Company press release",
        text="Company disclosed operational exposure and mitigation timing.",
        published_at="2026-06-30",
        retrieved_at="2026-06-30T10:00:00",
    )

    item = normalize_retrieved_document(document, query="operational exposure")

    assert item.title == "Company disclosure"
    assert item.source_url == "https://example.com/investor-relations"
    assert item.credibility_tier == "Tier 2 Company"
    assert item.status == "Retrieved"
    assert item.validation_status == "Valid"
    assert item.lifecycle_state == "retrieved"


def test_retriever_returns_deterministic_structure_without_ranking() -> None:
    response = retrieve_with_provider(
        query="semiconductor export controls",
        provider=StaticProvider(),
        limit=1,
    )

    assert set(response) == {
        "query",
        "provider",
        "retrieved_at",
        "results",
        "documents_retrieved",
        "items",
        "errors",
    }
    assert response["query"] == "semiconductor export controls"
    assert response["provider"]["provider_name"] == "static_test"
    assert response["documents_retrieved"] == 1
    assert len(response["results"]) == 1
    assert len(response["items"]) == 1
    assert response["errors"] == []
    assert response["items"][0]["source_url"] == "https://agency.gov/policy/canonical"


def test_retriever_records_document_failure_without_losing_successful_items() -> None:
    response = retrieve_with_provider(
        query="policy update",
        provider=PartialFailureProvider(),
        limit=2,
    )

    assert response["documents_retrieved"] == 1
    assert len(response["items"]) == 1
    assert len(response["errors"]) == 1
    assert response["errors"][0]["source_url"] == "https://agency.gov/bad"


def test_retriever_retries_provider_search_then_raises() -> None:
    provider = FailingSearchProvider()

    with pytest.raises(EvidenceRetrievalError):
        retrieve_with_provider(
            query="policy update",
            provider=provider,
            retry_count=2,
        )

    assert provider.calls == 3
