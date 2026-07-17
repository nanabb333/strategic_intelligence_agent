"""Validate repository-relative links in tracked Markdown documents."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    excluded = {".git", ".venv", ".venv-1", "outputs"}
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in excluded for part in path.relative_to(ROOT).parts)
    )


def broken_links() -> list[str]:
    broken: list[str] = []
    for document in markdown_files():
        text = document.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            raw = match.group(1).strip().strip("<>")
            target = raw.split(maxsplit=1)[0]
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(("#", "mailto:")):
                continue
            relative = unquote(parsed.path)
            if not relative:
                continue
            destination = (document.parent / relative).resolve()
            if not destination.exists():
                line = text.count("\n", 0, match.start()) + 1
                broken.append(f"{document.relative_to(ROOT)}:{line}: {target}")
    return broken


def main() -> None:
    failures = broken_links()
    if failures:
        raise SystemExit("Broken Markdown links:\n" + "\n".join(failures))
    print("Markdown internal link validation passed.")


if __name__ == "__main__":
    main()
