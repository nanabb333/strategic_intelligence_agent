"""Metadata construction for analysis run artifacts."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from localization import localized_question_intent


def build_analysis_metadata(
    *,
    run_id: str,
    language: str,
    output_mode: str,
    question_id: str,
    question_route: Any,
    source_url: str,
    input_mode: str,
    uploaded_filename: str,
    file_type: str,
    project_id: str = "",
    project_question_id: str = "",
    evidence_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Build persisted metadata for one analysis run."""
    return {
        "run_id": run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "language": language,
        "output_mode": output_mode,
        "question_id": question_id,
        "question_text": question_route.question_text,
        "question_intent": question_route.intent,
        "question_intent_label": localized_question_intent(question_route.intent, language),
        "project_id": project_id,
        "project_question_id": project_question_id,
        "evidence_ids": evidence_ids or [],
        "source_url": source_url,
        "input_mode": input_mode,
        "uploaded_filename": uploaded_filename,
        "file_type": file_type,
        "status": "complete",
        "artifact_paths": {
            "input": f"outputs/runs/{run_id}/input.txt",
            "analysis": f"outputs/runs/{run_id}/analysis.json",
            "brief_markdown": f"outputs/runs/{run_id}/brief.md",
            "brief_text": f"outputs/runs/{run_id}/brief.txt",
            "agent_trace": f"outputs/runs/{run_id}/agent_trace.json",
            "metadata": f"outputs/runs/{run_id}/metadata.json",
        },
    }
