"""Compatibility wrapper for the secured reviewer-triggered URL reader."""

import sys
from pathlib import Path


SRC = Path(__file__).resolve().parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from url_reader import fetch_url_text  # noqa: E402


if __name__ == "__main__":
    url = "https://example.com"

    text = fetch_url_text(url)

    print(text[:1000])
