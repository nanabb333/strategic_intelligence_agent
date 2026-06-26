"""Input preparation for analysis runs."""

from __future__ import annotations

from fastapi import HTTPException

from url_reader import fetch_url_text


def prepare_analysis_input(*, text: str, source_url: str, question_text: str) -> dict[str, str]:
    text = text.strip()
    source_url = source_url.strip()

    # If the user pasted a URL into the main text box,
    # treat it as a URL automatically.
    if text.startswith(("http://", "https://")) and not source_url:
        source_url = text
        text = fetch_url_text(source_url)

    elif not text:
        if source_url:
            text = fetch_url_text(source_url)
        else:
            raise HTTPException(
                status_code=400,
                detail="Text is required.",
            )

    stripped_question_text = question_text.strip()
    analysis_text = f"{stripped_question_text}\n\n{text}".strip() if stripped_question_text else text

    return {
        "text": text,
        "source_url": source_url,
        "analysis_text": analysis_text,
    }
