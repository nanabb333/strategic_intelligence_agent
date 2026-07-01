"""Shared deterministic helpers for decision support modules."""

from __future__ import annotations


def unique_refs(refs: list[dict[str, str]]) -> list[dict[str, str]]:
    """Return traceable evidence references de-duplicated by durable identity."""
    output: list[dict[str, str]] = []
    seen: set[str] = set()
    for ref in refs:
        key = str(ref.get("evidence_id") or ref.get("source_url") or ref.get("title") or "")
        if key and key not in seen:
            seen.add(key)
            output.append(ref)
    return output


def unique_strings(values: list[str]) -> list[str]:
    """Return non-empty strings in first-seen order."""
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        clean = str(value).strip()
        if clean and clean not in seen:
            seen.add(clean)
            output.append(clean)
    return output


def latest_or_first_project_question(project: dict) -> dict:
    """Return the last analyzed project question, then the most recent saved question."""
    questions = project.get("questions", []) or []
    if not questions:
        return {}
    state = project.get("workspace_state", {}) or {}
    last_id = state.get("last_analyzed_question_id") or state.get("last_question_id")
    if last_id:
        for question in questions:
            if question.get("question_id") == last_id:
                return question
    return questions[-1]
