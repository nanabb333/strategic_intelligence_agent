"""Issue extraction stage for Strategic Intelligence Agent."""

from dataclasses import dataclass, field


@dataclass
class ExtractedIssue:
    """Structured representation of an issue found in a document."""

    title: str
    summary: str
    actors: list[str] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)


def extract_issues(document_text: str) -> list[ExtractedIssue]:
    """Extract strategic issues from document text.

    This placeholder keeps the interface stable while the project migrates from
    rubric scoring to strategic issue extraction.
    """
    text = document_text.strip()
    if not text:
        return []

    lines = text.splitlines()
    first_line = lines[0].strip().lstrip("#").strip()
    title = first_line[:80] or "Untitled issue"
    body = "\n".join(lines[1:]).strip() or text
    summary = body[:500].strip()
    if len(body) > 500:
        summary = f"{summary}..."
    return [ExtractedIssue(title=title, summary=summary, evidence=[summary])]
