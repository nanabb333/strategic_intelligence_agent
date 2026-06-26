"""Analysis workflow service for the local app."""

from __future__ import annotations

from typing import Any

from analysis_pipeline import execute_analysis_pipeline


def run_analysis(
    *,
    text: str,
    language: str,
    output_mode: str,
    question_id: str,
    question_text: str,
    source_url: str,
    input_mode: str,
    uploaded_filename: str,
    file_type: str,
) -> dict[str, Any]:
    """Run the intelligence pipeline and persist run artifacts."""
    return execute_analysis_pipeline(
        text=text,
        language=language,
        output_mode=output_mode,
        question_id=question_id,
        question_text=question_text,
        source_url=source_url,
        input_mode=input_mode,
        uploaded_filename=uploaded_filename,
        file_type=file_type,
    )
