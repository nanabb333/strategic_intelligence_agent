from urllib.error import URLError

from fastapi.testclient import TestClient

from app import app
import evidence_provider
from evidence_provider import URLEvidenceProvider, is_url
from evidence_retrieval import retrieve_evidence
from evidence_retriever import retrieve_with_provider


class FakeHeaders:
    def __init__(self, content_type: str) -> None:
        self.content_type = content_type

    def get(self, name: str, default: str = "") -> str:
        if name.lower() == "content-type":
            return self.content_type
        return default


class FakeResponse:
    def __init__(self, *, body: str, content_type: str, final_url: str) -> None:
        self.body = body.encode("utf-8")
        self.headers = FakeHeaders(content_type)
        self.final_url = final_url

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        if not self.body:
            return b""
        if size < 0:
            size = len(self.body)
        chunk, self.body = self.body[:size], self.body[size:]
        return chunk

    def geturl(self) -> str:
        return self.final_url


class FakeOpener:
    def __init__(self, response: FakeResponse | None = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.requests = []

    def open(self, request, timeout: float):
        self.requests.append((request, timeout))
        if self.error:
            raise self.error
        return self.response


def test_url_detection_requires_http_or_https() -> None:
    assert is_url("https://example.com/report")
    assert is_url("http://example.com/report")
    assert not is_url("example.com/report")
    assert not is_url("file:///tmp/report.html")


def test_url_provider_retrieves_html_and_normalizes_to_evidence_item() -> None:
    opener = FakeOpener(
        FakeResponse(
            body="""
              <html>
                <head>
                  <title>Official release</title>
                  <meta name="description" content="Official description">
                  <meta name="author" content="Agency Staff">
                  <meta property="article:published_time" content="2026-06-30">
                </head>
                <body><article>Official body text for reviewer validation.</article></body>
              </html>
            """,
            content_type="text/html; charset=utf-8",
            final_url="https://agency.gov/release",
        )
    )
    provider = URLEvidenceProvider(timeout_seconds=2.0, opener=opener)

    response = retrieve_with_provider(
        query="https://agency.gov/release",
        provider=provider,
        limit=1,
    )

    assert response["documents_retrieved"] == 1
    assert response["errors"] == []
    item = response["items"][0]
    assert item["title"] == "Official release"
    assert item["source_url"] == "https://agency.gov/release"
    assert item["author"] == "Agency Staff"
    assert item["credibility_tier"] == "Tier 1 Official"
    assert item["validation_status"] == "Valid"
    assert opener.requests[0][1] == 2.0


def test_url_provider_handles_text_pages() -> None:
    opener = FakeOpener(
        FakeResponse(
            body="Plain text evidence from an official source.",
            content_type="text/plain",
            final_url="https://agency.gov/evidence.txt",
        )
    )
    provider = URLEvidenceProvider(opener=opener)

    response = retrieve_with_provider(
        query="https://agency.gov/evidence.txt",
        provider=provider,
    )

    item = response["items"][0]
    assert item["source_url"] == "https://agency.gov/evidence.txt"
    assert "Plain text evidence" in item["excerpt"]
    assert item["validation_status"] == "Needs Review"


def test_url_provider_reports_timeout_or_fetch_failure() -> None:
    provider = URLEvidenceProvider(opener=FakeOpener(error=TimeoutError("timed out")))

    response = retrieve_with_provider(
        query="https://agency.gov/slow",
        provider=provider,
    )

    assert response["documents_retrieved"] == 0
    assert response["items"] == []
    assert "timed out" in response["errors"][0]["error"]


def test_url_provider_rejects_unsupported_content_type() -> None:
    provider = URLEvidenceProvider(
        opener=FakeOpener(
            FakeResponse(
                body="%PDF-1.7",
                content_type="application/pdf",
                final_url="https://agency.gov/report.pdf",
            )
        )
    )

    response = retrieve_with_provider(
        query="https://agency.gov/report.pdf",
        provider=provider,
    )

    assert response["documents_retrieved"] == 0
    assert "Unsupported content type" in response["errors"][0]["error"]


def test_url_provider_preserves_redirect_final_url() -> None:
    provider = URLEvidenceProvider(
        opener=FakeOpener(
            FakeResponse(
                body="<html><head><title>Redirected</title></head><body>Redirected body</body></html>",
                content_type="text/html",
                final_url="https://agency.gov/final",
            )
        )
    )

    response = retrieve_with_provider(
        query="https://agency.gov/start",
        provider=provider,
    )

    assert response["items"][0]["source_url"] == "https://agency.gov/final"


def test_retrieve_evidence_uses_url_provider_for_explicit_url(monkeypatch) -> None:
    monkeypatch.setattr(evidence_provider, "validate_public_http_url", lambda url, **kwargs: url)
    monkeypatch.setattr(
        evidence_provider,
        "build_opener",
        lambda *args, **kwargs: FakeOpener(
            FakeResponse(
                body="<html><head><title>URL Evidence</title><meta property='article:published_time' content='2026-06-30'></head><body>URL body text.</body></html>",
                content_type="text/html",
                final_url="https://agency.gov/url-evidence",
            )
        ),
    )

    response = retrieve_evidence(query="https://agency.gov/url-evidence")

    assert response["provider"]["provider_name"] == "url"
    assert len(response["items"]) == 1
    assert response["items"][0]["title"] == "URL Evidence"
    assert response["items"][0]["status"] == "Retrieved"


def test_retrieve_evidence_non_url_behavior_still_uses_local_candidates() -> None:
    response = retrieve_evidence(query="semiconductor export controls")

    assert "provider" not in response
    assert response["items"]
    assert all(item["status"] == "Retrieved" for item in response["items"])


def test_retrieve_evidence_url_failure_returns_clear_api_error(monkeypatch) -> None:
    monkeypatch.setattr(evidence_provider, "validate_public_http_url", lambda url, **kwargs: url)
    monkeypatch.setattr(
        evidence_provider,
        "build_opener",
        lambda *args, **kwargs: FakeOpener(error=URLError("connection refused")),
    )

    response = TestClient(app).post(
        "/retrieve-evidence",
        json={"query": "https://agency.gov/unavailable"},
    )

    assert response.status_code == 400
    assert "Could not retrieve URL evidence" in response.json()["detail"]
