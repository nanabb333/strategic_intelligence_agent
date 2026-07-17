"""Project workspace utilities for Version 4."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from decision_assessment import normalize_stored_decision_assessment
from decision_lifecycle import decision_governance_metadata
from decision_review import default_decision_review_state, update_decision_review_state
from evidence_ledger import build_evidence_workflow_entry, confidence_effect_for_evidence
from evidence_lifecycle import (
    ACCEPTED,
    REFERENCED,
    apply_reviewer_action,
    lifecycle_metadata,
)


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
        "evidence_audit_log": [],
        "decision_history": [],
        "archived": False,
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


def inspect_project_files() -> dict[str, Any]:
    """Inspect local project JSON files without raising on malformed records."""
    ensure_projects_dir()
    readable = 0
    malformed = 0
    warnings: list[str] = []
    files = sorted(PROJECTS_DIR.glob("*.json"))
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            malformed += 1
            warnings.append(f"Project file {path.name} could not be loaded: {exc}")
            continue
        if not isinstance(payload, dict) or not payload.get("project_id"):
            malformed += 1
            warnings.append(f"Project file {path.name} is missing required project metadata.")
            continue
        readable += 1
    return {
        "projects_directory": str(PROJECTS_DIR),
        "file_count": len(files),
        "readable_count": readable,
        "malformed_count": malformed,
        "warnings": warnings,
    }


def delete_project(project_id: str) -> None:
    ensure_projects_dir()
    path = PROJECTS_DIR / f"{project_id}.json"

    if not path.exists():
        raise FileNotFoundError(f"Project not found: {project_id}")

    path.unlink()

def get_project(project_id: str) -> dict[str, Any]:
    path = PROJECTS_DIR / f"{project_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Project not found: {project_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_project(project: dict[str, Any]) -> dict[str, Any]:
    ensure_projects_dir()
    project.setdefault("evidence_audit_log", [])
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
        "current_assessment": _history_assessment_summary(latest),
        "current_evidence_sufficiency": latest.get("evidence_sufficiency_tier", ""),
        "last_analyzed_question_id": latest.get("question_id", ""),
        "last_updated_at": latest.get("created_at", ""),
        "evidence_count": len(evidence_library),
        "decision_count": len(history),
    }


def _summary_from_analysis(analysis: dict[str, Any]) -> str:
    assessment = normalize_stored_decision_assessment(analysis)
    return (
        str(assessment.get("assessment_summary") or "").strip()
        or str(assessment.get("decision_question") or "").strip()
        or "Review stored decision brief."
    )


def _sufficiency_from_analysis(analysis: dict[str, Any]) -> str:
    sufficiency = analysis.get("evidence_sufficiency") or {}
    return str(sufficiency.get("tier") or "Not assessed")


def _completeness_from_analysis(analysis: dict[str, Any]) -> float | None:
    completeness = analysis.get("artifact_completeness") or {}
    score = completeness.get("completion_rate")
    if isinstance(score, (int, float)):
        return round(float(score), 3)
    return None


def _completeness_counts_from_analysis(analysis: dict[str, Any]) -> tuple[int | None, int | None]:
    completeness = analysis.get("artifact_completeness") or {}
    passed = completeness.get("passed_checks")
    total = completeness.get("total_checks")
    return (
        int(passed) if isinstance(passed, (int, float)) else None,
        int(total) if isinstance(total, (int, float)) else None,
    )


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
    passed_checks, total_checks = _completeness_counts_from_analysis(analysis)
    record.update(
        {
            "question_id": question_id,
            "run_id": run_id,
            "assessment_summary": _summary_from_analysis(analysis),
            "reviewer_selected_path": "",
            "selection_rationale": "",
            "evidence_sufficiency_tier": _sufficiency_from_analysis(analysis),
            "artifact_completeness_rate": _completeness_from_analysis(analysis),
            "artifact_completeness_passed": passed_checks,
            "artifact_completeness_total": total_checks,
            "evidence_ids": evidence_ids if evidence_ids is not None else _evidence_ids_from_analysis(analysis),
        }
    )
    record.update(
        decision_governance_metadata(
            record,
            evidence_count=len(record.get("evidence_ids") or []),
            timestamp=record.get("created_at") or _now(),
        )
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


def archive_project(project_id: str) -> dict[str, Any]:
    """Mark a project archived without deleting user data."""
    project = get_project(project_id)
    project["archived"] = True
    project["archived_at"] = _now()
    return save_project(project)


def restore_project(project_id: str) -> dict[str, Any]:
    """Restore a project previously marked archived."""
    project = get_project(project_id)
    project["archived"] = False
    project["restored_at"] = _now()
    return save_project(project)


def project_metadata(project: dict[str, Any]) -> dict[str, Any]:
    """Return reviewer-friendly project metadata without mutating the project."""
    questions = project.get("questions") or []
    evidence = project.get("evidence_library") or []
    decisions = project.get("decision_history") or []
    return {
        "project_id": project.get("project_id", ""),
        "name": project.get("name", ""),
        "description": project.get("description", ""),
        "created_at": project.get("created_at", ""),
        "updated_at": project.get("updated_at", ""),
        "archived": bool(project.get("archived", False)),
        "status": "Archived" if project.get("archived") else "Active",
        "question_count": len(questions),
        "evidence_count": len(evidence),
        "decision_count": len(decisions),
        "last_updated_at": project.get("updated_at", ""),
    }


def workspace_summary() -> dict[str, Any]:
    """Summarize local workspace state for diagnostics and release validation."""
    projects = list_projects()
    return {
        "projects_directory": str(PROJECTS_DIR),
        "project_count": len(projects),
        "archived_count": sum(1 for project in projects if project.get("archived")),
        "question_count": sum(len(project.get("questions") or []) for project in projects),
        "evidence_count": sum(len(project.get("evidence_library") or []) for project in projects),
        "decision_count": sum(len(project.get("decision_history") or []) for project in projects),
        "files": inspect_project_files(),
    }


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
        _mark_evidence_used(project, evidence_ids, question_id=question_id, run_id=run_id)
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


def _append_evidence_ledger_entry(
    project: dict[str, Any],
    evidence: dict[str, Any],
    *,
    lifecycle_state: str,
    reviewer_action: str,
    rationale: str = "",
    project_question_id: str = "",
    decision_run_id: str = "",
) -> None:
    project.setdefault("evidence_audit_log", []).append(
        build_evidence_workflow_entry(
            project_id=str(project.get("project_id") or ""),
            evidence=evidence,
            lifecycle_state=lifecycle_state,
            reviewer_action=reviewer_action,
            reviewer_status=str(evidence.get("reviewer_status") or lifecycle_state),
            rationale=rationale,
            project_question_id=project_question_id,
            decision_run_id=decision_run_id,
            supported_sections=["Evidence and Confidence"] if decision_run_id else [],
            confidence_effect=confidence_effect_for_evidence(evidence),
        )
    )


def _mark_evidence_used(
    project: dict[str, Any],
    evidence_ids: list[str],
    *,
    question_id: str = "",
    run_id: str = "",
) -> None:
    selected = set(evidence_ids)
    used_at = _now()
    for item in project.get("evidence_library", []):
        if item.get("evidence_id") in selected:
            apply_reviewer_action(
                item,
                action="reference_in_decision",
                review_reason="Selected evidence was referenced in an analysis run.",
                timestamp=used_at,
            )
            item["used_at"] = used_at
            _append_evidence_ledger_entry(
                project,
                item,
                lifecycle_state=REFERENCED,
                reviewer_action="reference_in_decision",
                rationale="Selected evidence was referenced in an analysis run.",
                project_question_id=question_id,
                decision_run_id=run_id,
            )


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
    evidence.update(lifecycle_metadata(evidence))
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
            "publisher": str(item.get("publisher") or item.get("source_name") or "").strip(),
            "author": str(item.get("author") or "").strip(),
            "uploaded_filename": str(item.get("uploaded_filename") or "").strip(),
            "text_excerpt": excerpt,
            "summary": str(item.get("summary") or excerpt).strip(),
            "added_at": _now(),
            "retrieved_at": str(item.get("retrieved_at") or "").strip(),
            "published_at": str(item.get("published_at") or "").strip(),
            "status": "Accepted",
            "credibility_tier": str(item.get("credibility_tier") or "Tier 5 Other").strip(),
            "credibility_score": item.get("credibility_score"),
            "relevance_score": item.get("relevance_score"),
            "validation_status": str(item.get("validation_status") or "").strip(),
            "validation_notes": item.get("validation_notes") or [],
            "conflict_status": str(item.get("conflict_status") or "No Conflict").strip(),
            "trace_id": str(item.get("trace_id") or "").strip(),
            "freshness_note": str(item.get("freshness_note") or "").strip(),
        }
        evidence.update(
            lifecycle_metadata(
                {
                    **item,
                    **evidence,
                    "evidence_action": "accept",
                    "reviewer_status": ACCEPTED,
                    "reviewed_at": _now(),
                    "review_reason": "Reviewer accepted retrieved evidence into the project library.",
                },
                default_state=ACCEPTED,
            )
        )
        accepted.append(evidence)
        _append_evidence_ledger_entry(
            project,
            evidence,
            lifecycle_state=ACCEPTED,
            reviewer_action="accept",
            rationale="Reviewer accepted retrieved evidence into the project library.",
        )
    project.setdefault("evidence_library", []).extend(accepted)
    return save_project(project)


def review_project_evidence(
    project_id: str,
    evidence_id: str,
    *,
    action: str,
    reviewer_note: str = "",
    review_reason: str = "",
) -> dict[str, Any]:
    """Apply a local reviewer action and append an evidence audit ledger entry."""
    project = get_project(project_id)
    evidence = next(
        (
            item
            for item in project.get("evidence_library", [])
            if item.get("evidence_id") == evidence_id
        ),
        None,
    )
    if evidence is None:
        raise FileNotFoundError(f"Evidence not found: {evidence_id}")
    apply_reviewer_action(
        evidence,
        action=action,
        reviewer_note=reviewer_note,
        review_reason=review_reason,
    )
    state = str(evidence.get("lifecycle_state") or "")
    _append_evidence_ledger_entry(
        project,
        evidence,
        lifecycle_state=state,
        reviewer_action=action,
        rationale=review_reason or reviewer_note,
    )
    return save_project(project)


def list_project_evidence(project_id: str) -> list[dict[str, Any]]:
    return get_project(project_id).get("evidence_library", [])


def get_decision_review_state(project_id: str) -> dict[str, Any]:
    """Return project-level decision review state without mutating legacy projects."""
    return default_decision_review_state(get_project(project_id))


def update_project_decision_review(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Persist reviewer-controlled decision review state under the project JSON."""
    project = get_project(project_id)
    project["decision_review_state"] = update_decision_review_state(project, payload)
    saved = save_project(project)
    return default_decision_review_state(saved)


def decision_delta(project_id: str) -> dict[str, Any]:
    project = get_project(project_id)
    history = project.get("decision_history", [])
    if len(history) < 2:
        return {"available": False, "message": "At least two completed analyses are required."}

    previous = history[-2]
    current = history[-1]
    previous_score = previous.get("artifact_completeness_rate")
    current_score = current.get("artifact_completeness_rate")
    previous_ids = set(previous.get("evidence_ids") or [])
    current_ids = set(current.get("evidence_ids") or [])
    previous_assessment = _history_assessment_summary(previous)
    current_assessment = _history_assessment_summary(current)
    assessment_changed = previous_assessment != current_assessment

    quality_change = None
    if isinstance(previous_score, (int, float)) and isinstance(current_score, (int, float)):
        quality_change = round(float(current_score) - float(previous_score), 3)

    return {
        "available": True,
        "previous_decision_id": previous.get("decision_id"),
        "current_decision_id": current.get("decision_id"),
        "previous_assessment": previous_assessment,
        "current_assessment": current_assessment,
        "what_changed": "Assessment summary changed." if assessment_changed else "Assessment summary remained stable.",
        "evidence_sufficiency_change": {
            "previous": previous.get("evidence_sufficiency_tier") or "Legacy status unavailable",
            "current": current.get("evidence_sufficiency_tier") or "Legacy status unavailable",
        },
        "artifact_completeness_change": {
            "previous": previous_score,
            "current": current_score,
            "delta": quality_change,
            "previous_passed": previous.get("artifact_completeness_passed"),
            "previous_total": previous.get("artifact_completeness_total"),
            "current_passed": current.get("artifact_completeness_passed"),
            "current_total": current.get("artifact_completeness_total"),
        },
        "evidence_added": sorted(current_ids - previous_ids),
        "evidence_missing_or_weakened": sorted(previous_ids - current_ids),
        "assessment_changed": assessment_changed,
    }


def _history_assessment_summary(record: dict[str, Any]) -> str:
    summary = str(record.get("assessment_summary") or "").strip()
    if summary:
        return summary
    if record.get("recommendation_summary"):
        return "Legacy decision record; the former system-generated recommendation is suppressed."
    return "Assessment summary not available."
