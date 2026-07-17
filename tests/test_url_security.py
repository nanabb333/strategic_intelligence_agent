import socket

import pytest

from evidence_provider import (
    EvidenceFetchError,
    SearchResult,
    URLEvidenceProvider,
    _LimitedRedirectHandler,
    _read_bounded,
)
from url_security import UnsafeURLError, validate_public_http_url


def _resolver(address: str):
    def resolve(host, port, type=socket.SOCK_STREAM):
        return [(socket.AF_INET, type, 6, "", (address, port))]

    return resolve


def _multi_resolver(*addresses: str):
    def resolve(host, port, type=socket.SOCK_STREAM):
        return [(socket.AF_INET6 if ":" in address else socket.AF_INET, type, 6, "", (address, port)) for address in addresses]

    return resolve


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost/private",
        "http://127.0.0.1/private",
        "http://10.0.0.1/private",
        "http://169.254.169.254/latest/meta-data",
        "http://[::1]/private",
        "http://[fe80::1]/private",
        "http://[fc00::1]/private",
        "http://[::ffff:127.0.0.1]/private",
        "http://224.0.0.1/multicast",
    ],
)
def test_non_public_literal_and_metadata_targets_are_blocked(url: str) -> None:
    with pytest.raises(UnsafeURLError):
        validate_public_http_url(url)


def test_hostname_resolving_to_private_address_is_blocked() -> None:
    with pytest.raises(UnsafeURLError):
        validate_public_http_url("https://public-looking.example/report", resolver=_resolver("192.168.1.10"))


def test_public_hostname_resolution_is_allowed() -> None:
    assert validate_public_http_url(
        "https://public.example/report",
        resolver=_resolver("93.184.216.34"),
    ) == "https://public.example/report"


def test_any_non_public_dns_answer_blocks_the_hostname() -> None:
    with pytest.raises(UnsafeURLError):
        validate_public_http_url(
            "https://mixed.example/report",
            resolver=_multi_resolver("93.184.216.34", "10.0.0.5"),
        )


@pytest.mark.parametrize(
    "url",
    [
        "https://user@public.example/report",
        "https://user:secret@public.example/report",
    ],
)
def test_userinfo_urls_are_rejected(url: str) -> None:
    with pytest.raises(UnsafeURLError):
        validate_public_http_url(url, resolver=_resolver("93.184.216.34"))


@pytest.mark.parametrize(
    "target",
    [
        "http://127.0.0.1/private",
        "http://169.254.169.254/latest/meta-data",
        "http://[::1]/private",
    ],
)
def test_redirect_handler_blocks_non_public_targets(target: str) -> None:
    handler = _LimitedRedirectHandler(3, lambda url: validate_public_http_url(url))
    with pytest.raises(UnsafeURLError):
        handler.redirect_request(None, None, 302, "Found", {}, target)


class LargeHeaders:
    def get(self, name: str, default: str = "") -> str:
        return "text/plain" if name.lower() == "content-type" else default


class LargeResponse:
    headers = LargeHeaders()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return None

    def geturl(self):
        return "https://public.example/large"

    def read(self, size: int = -1):
        return b"x" * 101


class LargeOpener:
    def open(self, request, timeout: float):
        return LargeResponse()


def test_url_provider_enforces_response_size_boundary() -> None:
    provider = URLEvidenceProvider(
        opener=LargeOpener(),
        resolver=_resolver("93.184.216.34"),
        max_response_bytes=100,
    )

    with pytest.raises(EvidenceFetchError, match="safety limit"):
        provider.retrieve(
            SearchResult(title="Large", source_url="https://public.example/large")
        )


class StreamingResponse:
    def __init__(self, chunks: list[bytes], content_length: str | None = None) -> None:
        self.chunks = list(chunks)
        self.headers = {"Content-Length": content_length} if content_length is not None else {}
        self.read_sizes: list[int] = []

    def read(self, size: int) -> bytes:
        self.read_sizes.append(size)
        return self.chunks.pop(0) if self.chunks else b""


def test_bounded_streaming_stops_after_limit_without_content_length() -> None:
    response = StreamingResponse([b"a" * 60, b"b" * 41])
    with pytest.raises(EvidenceFetchError, match="safety limit"):
        _read_bounded(response, 100)
    assert all(size <= 101 for size in response.read_sizes)


def test_false_content_length_does_not_bypass_actual_byte_limit() -> None:
    response = StreamingResponse([b"a" * 70, b"b" * 31], content_length="1")
    with pytest.raises(EvidenceFetchError, match="safety limit"):
        _read_bounded(response, 100)


class Read1OnlyResponse:
    def __init__(self) -> None:
        self.done = False

    def read(self, size: int) -> bytes:
        raise TypeError("read requires compatibility path")

    def read1(self, size: int) -> bytes:
        if self.done:
            return b""
        self.done = True
        return b"bounded"


def test_bounded_read1_compatibility_never_calls_unbounded_read() -> None:
    assert _read_bounded(Read1OnlyResponse(), 100) == b"bounded"
