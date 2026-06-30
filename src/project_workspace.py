"""Project workspace utilities for Version 4."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "data" / "projects"
EVIDENCE_STATUSES = {
    "Retrieved",
    "Reviewed",
    "Accepted",
    "Used",
    "Archived",
    "Verified",
    "Corroborated",
    "User Provided",
    "Single Source",
    "Conflicting",
    "Historical Only",
    "Outdated",
    "Unavailable",
}


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def ensure_projects_dir() -> None:
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)


def create_project(name: str, description: str = "") -> dict[str, Any]:
    ensure_projects_dir()
    project_id = str(uuid4())[:8]
    project = {
        "project_id": project_id,
        "name": name.strip(),
        "description": description.strip(),
        "created_at": _now(),
        "updated_at": _now(),
        "questions": [],
        "evidence_library": [],
        "decision_history": [],
        "workspace_state": _workspace_state([], []),
    }
    path = PROJECTS_DIR / f"{project_id}.json"
    path.write_text(json.dumps(project, indent=2, ensure_ascii=False), encoding="utf-8")
    return project


def list_projects() -> list[dict[str, Any]]:
    ensure_projects_dir()
    projects = []
    for path in sorted(PROJECTS_DIR.glob("*.json")):
        try:
            projects.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return projects


def get_project(project_id: str) -> dict[str, Any]:
    path = PROJECTS_DIR / f"{project_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Project not found: {project_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_project(project: dict[str, Any]) -> dict[str, Any]:
    ensure_projects_dir()
    project["updated_at"] = _now()
    project["workspace_state"] = _workspace_state(
        project.get("evidence_library", []),
        project.get("decision_history", []),
    )
    path = PROJECTS_DIR / f"{project['project_id']}.json"
    path.write_text(json.dumps(project, indent=2, ensure_ascii=False), encoding="utf-8")
    return project


def _workspace_state(evidence_library: list[dict[str, Any]], history: list[dict[str, Any]]) -> dict[str, Any]:
    latest = history[-1] if history else {}
    return {
        "current_recommendation": latest.get("recommendation_summary", ""),
        "current_confidence": latest.get("confidence_label", ""),
        "last_analyzed_question_id": latest.get("question_id", ""),
        "last_updated_at": latest.get("created_at", ""),
        "evidence_count": len(evidence_library),
        "decision_count": len(history),
    }


def _summary_from_analysis(analysis: dict[str, Any]) -> str:
    decision_case = analysis.get("decision_case") or {}
    return (
        str(decision_case.get("recommended_path") or "").strip()
        or str(decision_case.get("decision_question") or "").strip()
        or "Review stored decision brief."
    )


def _confidence_from_analysis(analysis: dict[str, Any]) -> str:
    confidence = analysis.get("confidence_assessment") or {}
    return str(confidence.get("confidence_level") or "Not stated")


def _quality_from_analysis(analysis: dict[str, Any]) -> float | None:
    quality = analysis.get("decision_quality_evaluation") or {}
    score = quality.get("overall_score")
    if isinstance(score, (int, float)):
        return round(float(score), 3)
    return None


def _evidence_ids_from_analysis(analysis: dict[str, Any]) -> list[str]:
    ledger = analysis.get("evidence_ledger") or {}
    ids = []
    for item in ledger.get("items") or []:
        evidence_id = item.get("evidence_id")
        if evidence_id:
            ids.append(str(evidence_id))
    return ids


def _find_question(project: dict[str, Any], question_id: str) -> dict[str, Any] | None:
    for question in project.get("questions", []):
        if question.get("question_id") == question_id:
            return question
    return None


def _record_decision_history(
    project: dict[str, Any],
    *,
    question_id: str,
    run_id: str,
    analysis: dict[str, Any],
    evidence_ids: list[str] | None = None,
) -> None:
    history = project.setdefault("decision_history", [])
    existing = next(
        (
            item
            for item in history
            if item.get("question_id") == question_id and item.get("run_id") == run_id
        ),
        None,
    )
    record = existing if existing is not None else {"decision_id": str(uuid4())[:8], "created_at": _now()}
    record.update(
        {
            "question_id": question_id,
            "run_id": run_id,
            "recommendation_summary": _summary_from_analysis(analysis),
            "confidence_label": _confidence_from_analysis(analysis),
            "decision_quality_score": _quality_from_analysis(analysis),
            "evidence_ids": evidence_ids if evidence_ids is not None else _evidence_ids_from_analysis(analysis),
        }
    )
    if existing is None:
        history.append(record)


def add_question_to_project(
    project_id: str,
    question: str,
    run_id: str | None = None,
    brief_path: str | None = None,
    analysis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    project = get_project(project_id)
    question_record = {
        "question_id": str(uuid4())[:8],
        "question": question.strip(),
        "run_id": run_id,
        "brief_path": brief_path,
        "created_at": _now(),
    }
    project["questions"].append(question_record)
    if run_id and analysis:
        _record_decision_history(
            project,
            question_id=question_record["question_id"],
            run_id=run_id,
            analysis=analysis,
        )
    return save_project(project)


def attach_run_to_question(
    project_id: str,
    *,
    question_id: str,
    run_id: str,
    analysis: dict[str, Any],
    brief_path: str | None = None,
    evidence_ids: list[str] | None = None,
) -> dict[str, Any]:
    project = get_project(project_id)
    question = _find_question(project, question_id)
    if question is None:
        raise FileNotFoundError(f"Question not found: {question_id}")
    question["run_id"] = run_id
    if brief_path:
        question["brief_path"] = brief_path
    if evidence_ids:
        _mark_evidence_used(project, evidence_ids)
    _record_decision_history(
        project,
        question_id=question_id,
        run_id=run_id,
        analysis=analysis,
        evidence_ids=evidence_ids,
    )
    return save_project(project)


def evidence_bundle_for_project(project: dict[str, Any], evidence_ids: list[str]) -> list[dict[str, Any]]:
    """Return selected project evidence items in caller-provided order."""
    evidence_by_id = {
        str(item.get("evidence_id")): item
        for item in project.get("evidence_library", [])
        if item.get("evidence_id")
    }
    return [evidence_by_id[evidence_id] for evidence_id in evidence_ids if evidence_id in evidence_by_id]


def _mark_evidence_used(project: dict[str, Any], evidence_ids: list[str]) -> None:
    selected = set(evidence_ids)
    used_at = _now()
    for item in project.get("evidence_library", []):
        if item.get("evidence_id") in selected:
            item["status"] = "Used"
            item["used_at"] = used_at


def add_evidence_to_project(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    project = get_project(project_id)
    status = str(payload.get("status") or "User Provided").strip()
    if status not in EVIDENCE_STATUSES:
        status = "User Provided"
    evidence = {
        "evidence_id": str(uuid4())[:8],
        "title": str(payload.get("title") or "Untitled evidence").strip(),
        "source_type": str(payload.get("source_type") or "Manual note").strip(),
        "source_url": str(payload.get("source_url") or "").strip(),
        "uploaded_filename": str(payload.get("uploaded_filename") or "").strip(),
        "text_excerpt": str(payload.get("text_excerpt") or payload.get("summary") or "").strip(),
        "summary": str(payload.get("summary") or payload.get("text_excerpt") or "").strip(),
        "added_at": _now(),
        "status": status,
        "freshness_note": str(payload.get("freshness_note") or "").strip(),
    }
    project.setdefault("evidence_library", []).append(evidence)
    return save_project(project)


def accept_retrieved_evidence(project_id: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    """Accept user-reviewed retrieval candidates into the project evidence library."""
    project = get_project(project_id)
    accepted = []
    for item in items:
        title = str(item.get("title") or "").strip()
        excerpt = str(item.get("excerpt") or item.get("text_excerpt") or item.get("summary") or "").strip()
        if not title or not excerpt:
            continue
        evidence = {
            "evidence_id": str(uuid4())[:8],
            "title": title,
            "source_type": str(item.get("source_type") or "Retrieved evidence").strip(),
            "source_name": str(item.get("source_name") or "").strip(),
            "source_url": str(item.get("source_url") or "").strip(),
            "uploaded_filename": str(item.get("uploaded_filename") or "").strip(),
            "text_excerpt": excerpt,
            "summary": str(item.get("summary") or excerpt).strip(),
            "added_at": _now(),
            "retrieved_at": str(item.get("retrieved_at") or "").strip(),
            "published_at": str(item.get("published_at") or "").strip(),
            "status": "Accepted",
            "credibility_tier": str(item.get("credibility_tier") or "Tier 5 Other").strip(),
            "freshness_note": str(item.get("freshness_note") or "").strip(),
        }
        accepted.append(evidence)
    project.setdefault("evidence_library", []).extend(accepted)
    return save_project(project)


def list_project_evidence(project_id: str) -> list[dict[str, Any]]:
    return get_project(project_id).get("evidence_library", [])


def decision_delta(project_id: str) -> dict[str, Any]:
    project = get_project(project_id)
    history = project.get("decision_history", [])
    if len(history) < 2:
        return {"available": False, "message": "At least two completed analyses are required."}

    previous = history[-2]
    current = history[-1]
    previous_score = previous.get("decision_quality_score")
    current_score = current.get("decision_quality_score")
    previous_ids = set(previous.get("evidence_ids") or [])
    current_ids = set(current.get("evidence_ids") or [])
    recommendation_changed = (
        previous.get("recommendation_summary") != current.get("recommendation_summary")
    )

    quality_change = None
    if isinstance(previous_score, (int, float)) and isinstance(current_score, (int, float)):
        quality_change = round(float(current_score) - float(previous_score), 3)

    return {
        "available": True,
        "previous_decision_id": previous.get("decision_id"),
        "current_decision_id": current.get("decision_id"),
        "previous_recommendation": previous.get("recommendation_summary"),
        "current_recommendation": current.get("recommendation_summary"),
        "what_changed": "Recommendation changed." if recommendation_changed else "Recommendation remained stable.",
        "confidence_change": {
            "previous": previous.get("confidence_label"),
            "current": current.get("confidence_label"),
        },
        "decision_quality_change": {
            "previous": previous_score,
            "current": current_score,
            "delta": quality_change,
        },
        "evidence_added": sorted(current_ids - previous_ids),
        "evidence_missing_or_weakened": sorted(previous_ids - current_ids),
        "recommendation_changed": recommendation_changed,
    }
