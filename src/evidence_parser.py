"""HTML and text parsing utilities for evidence retrieval."""

from __future__ import annotations

from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
import re
from typing import Any


@dataclass(frozen=True)
class ParsedDocument:
    """Parsed document metadata before EvidenceItem normalization."""

    title: str
    description: str
    published_at: str
    author: str
    canonical_url: str
    raw_body: str
    source_url: str
    source_name: str
    source_type: str
    retrieved_at: str
    metadata: dict[str, Any]


class _EvidenceHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.body_parts: list[str] = []
        self.meta: dict[str, str] = {}
        self.canonical_url = ""
        self._capture_title = False
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "title":
            self._capture_title = True
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
        if tag == "meta":
            key = (
                attrs_dict.get("name")
                or attrs_dict.get("property")
                or attrs_dict.get("itemprop")
                or ""
            ).lower()
            content = attrs_dict.get("content", "").strip()
            if key and content:
                self.meta[key] = content
        if tag == "link" and attrs_dict.get("rel", "").lower() == "canonical":
            self.canonical_url = attrs_dict.get("href", "").strip()
        if tag == "time" and attrs_dict.get("datetime"):
            self.meta.setdefault("time:datetime", attrs_dict["datetime"].strip())

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._capture_title = False
        if tag in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        text = " ".join(unescape(data).split())
        if not text:
            return
        if self._capture_title:
            self.title_parts.append(text)
            return
        if not self._skip_depth:
            self.body_parts.append(text)


def parse_html_document(
    html: str,
    *,
    source_url: str = "",
    source_name: str = "",
    source_type: str = "Retrieved evidence",
    retrieved_at: str = "",
) -> ParsedDocument:
    """Parse HTML into metadata and text, tolerating malformed markup."""
    parser = _EvidenceHTMLParser()
    try:
        parser.feed(html or "")
        parser.close()
    except Exception:
        pass

    title = _first_value(
        " ".join(parser.title_parts),
        parser.meta.get("og:title", ""),
        parser.meta.get("twitter:title", ""),
    )
    description = _first_value(
        parser.meta.get("description", ""),
        parser.meta.get("og:description", ""),
        parser.meta.get("twitter:description", ""),
    )
    published_at = _first_value(
        parser.meta.get("article:published_time", ""),
        parser.meta.get("date", ""),
        parser.meta.get("pubdate", ""),
        parser.meta.get("publishdate", ""),
        parser.meta.get("dc.date", ""),
        parser.meta.get("time:datetime", ""),
    )
    author = _first_value(
        parser.meta.get("author", ""),
        parser.meta.get("article:author", ""),
        parser.meta.get("dc.creator", ""),
    )
    title = _clean_title(title)
    body = " ".join(parser.body_parts) or _fallback_body_text(html or "", title)
    return ParsedDocument(
        title=title,
        description=description,
        published_at=published_at,
        author=author,
        canonical_url=parser.canonical_url,
        raw_body=body,
        source_url=source_url,
        source_name=source_name,
        source_type=source_type,
        retrieved_at=retrieved_at,
        metadata={"malformed_html_tolerated": True},
    )


def parse_text_document(
    text: str,
    *,
    title: str = "",
    description: str = "",
    published_at: str = "",
    author: str = "",
    canonical_url: str = "",
    source_url: str = "",
    source_name: str = "",
    source_type: str = "Retrieved evidence",
    retrieved_at: str = "",
    metadata: dict[str, Any] | None = None,
) -> ParsedDocument:
    """Wrap plain text in the parsed document shape."""
    return ParsedDocument(
        title=title,
        description=description,
        published_at=published_at,
        author=author,
        canonical_url=canonical_url,
        raw_body=" ".join((text or "").split()),
        source_url=source_url,
        source_name=source_name,
        source_type=source_type,
        retrieved_at=retrieved_at,
        metadata=metadata or {},
    )


def _first_value(*values: str) -> str:
    for value in values:
        clean = " ".join(str(value or "").split())
        if clean:
            return clean
    return ""


def _clean_title(value: str) -> str:
    clean = str(value or "").strip()
    if "<" in clean:
        clean = clean.split("<", 1)[0]
    return " ".join(clean.split())


def _fallback_body_text(html: str, title: str) -> str:
    without_scripts = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", without_scripts)
    text = " ".join(unescape(text).split())
    if title and text.startswith(title):
        text = text[len(title):].strip()
    return text
