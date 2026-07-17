"""Provider boundary for future live evidence retrieval integrations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from socket import timeout as SocketTimeout
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from url_security import UnsafeURLError, validate_public_http_url


@dataclass(frozen=True)
class SearchResult:
    """Provider-neutral search result metadata before document retrieval."""

    title: str
    source_url: str
    source_name: str = ""
    source_type: str = "Retrieved evidence"
    excerpt: str = ""
    published_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievedDocument:
    """Provider-neutral retrieved document before parser and normalizer stages."""

    title: str
    source_url: str
    source_name: str = ""
    source_type: str = "Retrieved evidence"
    html: str = ""
    text: str = ""
    description: str = ""
    published_at: str = ""
    author: str = ""
    canonical_url: str = ""
    retrieved_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseEvidenceProvider(ABC):
    """Provider interface for search and retrieval only.

    Providers should not rank, reason, accept evidence, or update projects.
    """

    provider_name = "base"
    provider_type = "generic"

    @abstractmethod
    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        """Return provider-specific search results in a neutral shape."""

    @abstractmethod
    def retrieve(self, result: SearchResult) -> RetrievedDocument:
        """Retrieve one search result into a neutral document shape."""

    def normalize(self, document: RetrievedDocument, *, query: str = "") -> Any:
        """Normalize a document using the shared EvidenceItem normalizer."""
        from evidence_normalizer import normalize_retrieved_document

        return normalize_retrieved_document(document, query=query)

    def metadata(self) -> dict[str, Any]:
        """Return static provider metadata for diagnostics and future UI surfaces."""
        return {
            "provider_name": self.provider_name,
            "provider_type": self.provider_type,
            "external_api": False,
        }


class ProviderRegistry:
    """Small deterministic provider registry."""

    def __init__(self) -> None:
        self._providers: dict[str, BaseEvidenceProvider] = {}

    def register(self, provider: BaseEvidenceProvider) -> None:
        name = str(provider.provider_name).strip()
        if not name:
            raise ValueError("Provider name is required.")
        self._providers[name] = provider

    def get(self, provider_name: str) -> BaseEvidenceProvider:
        try:
            return self._providers[provider_name]
        except KeyError as exc:
            raise KeyError(f"Evidence provider not registered: {provider_name}") from exc

    def names(self) -> list[str]:
        return sorted(self._providers)

    def metadata(self) -> list[dict[str, Any]]:
        return [self._providers[name].metadata() for name in self.names()]


provider_registry = ProviderRegistry()


def register_provider(provider: BaseEvidenceProvider) -> None:
    """Register a provider in the process-local evidence provider registry."""
    provider_registry.register(provider)


def get_provider(provider_name: str) -> BaseEvidenceProvider:
    """Return a registered provider by name."""
    return provider_registry.get(provider_name)


class EvidenceFetchError(RuntimeError):
    """User-facing URL retrieval error."""


class _LimitedRedirectHandler(HTTPRedirectHandler):
    def __init__(self, max_redirects: int, validator: Any) -> None:
        self.max_redirects = max_redirects
        self.redirect_count = 0
        self.validator = validator
        super().__init__()

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        self.redirect_count += 1
        if self.redirect_count > self.max_redirects:
            raise EvidenceFetchError(f"Too many redirects while retrieving URL: {newurl}")
        self.validator(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class URLEvidenceProvider(BaseEvidenceProvider):
    """Explicit single-URL evidence provider.

    This provider fetches only the reviewer-supplied URL. It does not search,
    discover links, crawl pages, monitor sources, or follow background tasks.
    """

    provider_name = "url"
    provider_type = "explicit_url"

    def __init__(
        self,
        *,
        timeout_seconds: float = 8.0,
        max_redirects: int = 3,
        max_response_bytes: int = 2_000_000,
        opener: Any = None,
        resolver: Any = None,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_redirects = max_redirects
        self.max_response_bytes = max_response_bytes
        self.opener = opener
        self.resolver = resolver
        self.resolve_hosts = opener is None or resolver is not None

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        url = normalize_url(query)
        if not is_url(url):
            raise EvidenceFetchError("URL evidence retrieval requires an explicit http or https URL.")
        return [
            SearchResult(
                title=url,
                source_url=url,
                source_name=_host_name(url),
                source_type="Retrieved evidence",
            )
        ]

    def retrieve(self, result: SearchResult) -> RetrievedDocument:
        url = normalize_url(result.source_url)
        if not is_url(url):
            raise EvidenceFetchError("Unsupported URL. Provide an explicit http or https URL.")
        self._validate_url(url)

        request = Request(
            url,
            headers={
                "User-Agent": "Repo5EvidenceRetriever/6.0 (+reviewer-triggered)",
                "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.1",
            },
        )
        opener = self.opener or build_opener(_LimitedRedirectHandler(self.max_redirects, self._validate_url))
        try:
            with opener.open(request, timeout=self.timeout_seconds) as response:
                final_url = response.geturl()
                self._validate_url(final_url)
                content_type = response.headers.get("Content-Type", "")
                media_type = _media_type(content_type)
                if not _supported_content_type(media_type):
                    raise EvidenceFetchError(
                        f"Unsupported content type for URL evidence retrieval: {media_type or 'unknown'}"
                    )
                raw = _read_bounded(response, self.max_response_bytes)
        except EvidenceFetchError:
            raise
        except HTTPError as exc:
            raise EvidenceFetchError(f"Could not retrieve URL evidence: HTTP {exc.code}.") from exc
        except (URLError, SocketTimeout, TimeoutError) as exc:
            raise EvidenceFetchError(f"Could not retrieve URL evidence: {exc}.") from exc
        except OSError as exc:
            raise EvidenceFetchError(f"Could not retrieve URL evidence: {exc}.") from exc

        charset = _charset(content_type)
        text = raw.decode(charset, errors="replace")
        common = {
            "title": result.title,
            "source_url": url,
            "source_name": result.source_name or _host_name(final_url),
            "source_type": result.source_type,
            "canonical_url": final_url,
            "metadata": {
                **result.metadata,
                "content_type": content_type,
                "final_url": final_url,
                "redirected": final_url != url,
            },
        }
        if media_type in {"text/html", "application/xhtml+xml"} or "<html" in text[:500].lower():
            return RetrievedDocument(html=text, **common)
        return RetrievedDocument(text=text, **common)

    def _validate_url(self, url: str) -> None:
        try:
            validate_public_http_url(
                url,
                resolver=self.resolver,
                resolve_host=self.resolve_hosts,
            )
        except UnsafeURLError as exc:
            raise EvidenceFetchError(f"Unsafe URL blocked: {exc}") from exc

    def metadata(self) -> dict[str, Any]:
        metadata = super().metadata()
        metadata.update(
            {
                "supports": ["single_explicit_url"],
                "timeout_seconds": self.timeout_seconds,
                "max_redirects": self.max_redirects,
                "max_response_bytes": self.max_response_bytes,
            }
        )
        return metadata


def is_url(value: str) -> bool:
    parsed = urlparse(str(value or "").strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def normalize_url(value: str) -> str:
    return str(value or "").strip()


def _host_name(url: str) -> str:
    return urlparse(url).netloc


def _media_type(content_type: str) -> str:
    return str(content_type or "").split(";", 1)[0].strip().lower()


def _charset(content_type: str) -> str:
    for part in str(content_type or "").split(";"):
        if "charset=" in part.lower():
            return part.split("=", 1)[1].strip() or "utf-8"
    return "utf-8"


def _supported_content_type(media_type: str) -> bool:
    return media_type in {"", "text/html", "application/xhtml+xml", "text/plain"}


def _read_bounded(response: Any, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while total <= max_bytes:
        request_size = min(65_536, max_bytes + 1 - total)
        try:
            chunk = response.read(request_size)
        except TypeError as exc:
            read1 = getattr(response, "read1", None)
            if not callable(read1):
                raise EvidenceFetchError("URL response does not support bounded reading.") from exc
            chunk = read1(request_size)
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > max_bytes:
            raise EvidenceFetchError(f"URL response exceeds the {max_bytes}-byte safety limit.")
    return b"".join(chunks)
