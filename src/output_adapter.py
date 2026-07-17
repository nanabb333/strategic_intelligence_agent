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
    """Preserve the complete assessment while applying an executive title."""
    return _replace_document_title(markdown_text, "Executive Decision Assessment")


def _render_beginner_output(markdown_text: str) -> str:
    """Preserve the complete assessment while applying a beginner-facing title."""
    return _replace_document_title(markdown_text, "Beginner Decision Assessment")


def _replace_document_title(markdown_text: str, title: str) -> str:
    lines = markdown_text.strip().splitlines()
    if lines and lines[0].startswith("# "):
        lines[0] = f"# {title}"
    else:
        lines = [f"# {title}", "", *lines]
    return "\n".join(lines).strip() + "\n"


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
