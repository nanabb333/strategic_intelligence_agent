"""Markdown utility helpers."""

from __future__ import annotations


def markdown_to_text(markdown: str) -> str:
    """Convert simple Markdown output to plain text using existing rules."""
    lines = []
    for line in markdown.splitlines():
        cleaned = line.replace("#", "").replace("**", "").replace("`", "").strip()
        if cleaned:
            lines.append(cleaned)
    return "\n".join(lines) + "\n"
