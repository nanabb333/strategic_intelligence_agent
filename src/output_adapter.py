"""English output-mode adapter for decision briefs."""

from __future__ import annotations

from pathlib import Path


SUPPORTED_MODES = {"beginner", "analyst", "executive"}
SUPPORTED_LANGUAGES = {"en"}


def adapt_output(markdown_text: str, mode: str = "analyst", language: str = "en") -> str:
    """Adapt a Markdown brief for the selected English output mode."""
    if mode not in SUPPORTED_MODES:
        raise ValueError(f"Unsupported output mode: {mode}")
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    source_markdown = markdown_text.strip()
    if mode == "beginner":
        return _render_beginner_output(source_markdown)
    if mode == "executive":
        return _render_executive_output(source_markdown)
    return source_markdown + "\n"


def adapt_file(input_path: str | Path, output_path: str | Path, mode: str, language: str) -> Path:
    """Adapt a Markdown file into another local Markdown file."""
    source = Path(input_path)
    destination = Path(output_path)
    destination.write_text(adapt_output(source.read_text(encoding="utf-8"), mode, language), encoding="utf-8")
    return destination


def _section_map(markdown_text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_title = ""
    current_lines: list[str] = []
    for line in markdown_text.splitlines():
        if line.startswith("## "):
            if current_title:
                sections[current_title] = "\n".join(current_lines).strip()
            current_title = line.replace("## ", "", 1).strip()
            current_lines = []
        elif current_title:
            current_lines.append(line)
    if current_title:
        sections[current_title] = "\n".join(current_lines).strip()
    return sections


def _render_executive_output(markdown_text: str) -> str:
    sections = _section_map(markdown_text)
    preferred_order = [
        "Decision Snapshot",
        "Decision Criteria",
        "Preferred Path",
        "Role-Based Implications",
        "Assumptions",
        "Trade-offs",
        "Risk Analysis",
        "Failure Modes",
        "Decision Blind Spots",
        "What Could Change This Recommendation",
        "Regulatory Considerations",
        "What to Monitor",
        "Recommendation Action Plan",
        "Action Timeline",
        "Limitations",
    ]
    lines = ["# Executive Summary", ""]
    for section in preferred_order:
        body = sections.get(section)
        if body:
            lines.extend([f"## {section}", "", body, ""])
    if len(lines) <= 2:
        return markdown_text.strip() + "\n"
    return "\n".join(lines).strip() + "\n"


def _render_beginner_output(markdown_text: str) -> str:
    sections = _section_map(markdown_text)
    snapshot = sections.get("Decision Snapshot", "").strip()
    question = sections.get("Decision Question", "").strip()
    criteria = sections.get("Decision Criteria", "").strip()
    paths = sections.get("Decision Paths", "").strip()
    preferred = sections.get("Preferred Path", "").strip()
    role_implications = sections.get("Role-Based Implications", "").strip()
    monitor = sections.get("What to Monitor", "").strip()
    change_section = sections.get("What Could Change This Recommendation", "").strip()
    limitations = sections.get("Limitations", "").strip()

    return "\n".join(
        [
            "# Beginner Explanation",
            "",
            "## Decision Snapshot",
            "",
            snapshot or "**Current Position:** Review the decision brief before acting.",
            "",
            "## What this means",
            "",
            question or "- The issue should be treated as a decision question, not only a news summary.",
            "",
            "## What matters most",
            "",
            _beginner_criteria(criteria),
            "",
            "## Possible choices",
            "",
            paths or "- Compare waiting, staged preparation, and defensive action against evidence and reversibility.",
            "",
            "## Current decision-support view",
            "",
            preferred or "- Review the full brief for the current decision-support view.",
            "",
            "## Who needs to do what",
            "",
            role_implications
            or "- Assign a decision owner, clarify exposure, separate confirmed facts from assumptions, and define review triggers.",
            "",
            "## What to watch next",
            "",
            monitor or "- Watch for evidence that the issue is becoming more costly, less reversible, or more structural.",
            "",
            "## What could change this view",
            "",
            change_section or "- New evidence, stronger constraints, or unresolved contradictions could change the view.",
            "",
            "## Limitations",
            "",
            limitations
            or "- This is a deterministic decision-support draft for human review, not a forecast, legal advice, investment advice, or verified research.",
        ]
    ).strip() + "\n"


def _beginner_criteria(criteria_text: str) -> str:
    if not criteria_text:
        return "- The most important factors are exposure, reversibility, execution burden, and what new information would change the review."
    simplified: list[str] = []
    for line in criteria_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        stripped = stripped.replace("- **", "- ").replace("**", "")
        if " - " in stripped:
            name, rest = stripped.split(" - ", 1)
            reason = rest.split(". ", 1)[1] if ". " in rest else rest
            simplified.append(f"{name}: {reason}")
        elif " — " in stripped:
            name, rest = stripped.split(" — ", 1)
            reason = rest.split(". ", 1)[1] if ". " in rest else rest
            simplified.append(f"{name}: {reason}")
        else:
            simplified.append(stripped)
    return "\n".join(simplified[:6]) or criteria_text
