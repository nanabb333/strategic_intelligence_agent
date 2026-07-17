"""Conservative public-URL validation for reviewer-triggered retrieval."""

from __future__ import annotations

import ipaddress
import socket
from collections.abc import Callable
from typing import Any
from urllib.parse import urlparse


Resolver = Callable[..., list[tuple[Any, ...]]]
BLOCKED_HOSTNAMES = {
    "localhost",
    "localhost.localdomain",
    "metadata.google.internal",
    "metadata.google",
}


class UnsafeURLError(ValueError):
    """Raised when a URL can target a non-public network resource."""


def validate_public_http_url(
    url: str,
    *,
    resolver: Resolver | None = None,
    resolve_host: bool = True,
) -> str:
    """Validate scheme, host, and every resolved address as globally routable."""
    value = str(url or "").strip()
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise UnsafeURLError("Only explicit public http or https URLs are supported.")
    if parsed.username or parsed.password:
        raise UnsafeURLError("URLs containing user information are not supported.")

    hostname = parsed.hostname.rstrip(".").lower()
    if hostname in BLOCKED_HOSTNAMES or hostname.endswith(".localhost"):
        raise UnsafeURLError("Localhost and metadata service targets are blocked.")

    literal = _ip_address(hostname)
    if literal is not None:
        _require_global(literal)
        return value

    if resolve_host:
        lookup = resolver or socket.getaddrinfo
        try:
            records = lookup(hostname, parsed.port or _default_port(parsed.scheme), type=socket.SOCK_STREAM)
        except OSError as exc:
            raise UnsafeURLError("The URL hostname could not be resolved safely.") from exc
        addresses = {_record_address(record) for record in records}
        if not addresses:
            raise UnsafeURLError("The URL hostname did not resolve to a public address.")
        for address in addresses:
            _require_global(ipaddress.ip_address(address))
    return value


def _record_address(record: tuple[Any, ...]) -> str:
    sockaddr = record[4]
    return str(sockaddr[0])


def _ip_address(hostname: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    try:
        return ipaddress.ip_address(hostname)
    except ValueError:
        return None


def _require_global(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> None:
    if (
        not address.is_global
        or address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    ):
        raise UnsafeURLError(
            "Private, loopback, link-local, multicast, reserved, and unspecified network targets are blocked."
        )


def _default_port(scheme: str) -> int:
    return 443 if scheme == "https" else 80
