"""Evidence ledger structures for reviewable decision support."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha256
from typing import Any
from uuid import uuid4


@dataclass
class EvidenceItem:
    """One reviewable evidence record."""

    evidence_id: str
    source_type: str
    evidence_text: str
    observation: str
    inference: str
    claim_supported: str
    relevance: str
    confidence: str
    limitations: str
    used_in_section: str
    source_identity: str = ""
    source_status: str = ""
    externally_sourced: bool = False


@dataclass
class EvidenceLedger:
    """Collection of evidence records used by a decision case."""

    items: list[EvidenceItem] = field(default_factory=list)

    def ids(self) -> list[str]:
        """Return stable evidence identifiers for downstream artifacts."""
        return [item.evidence_id for item in self.items]


@dataclass
class EvidenceWorkflowLedgerEntry:
    """Append-only audit entry for evidence lifecycle movement."""

    ledger_id: str
    project_id: str
    project_question_id: str
    decision_run_id: str
    evidence_id: str
    trace_id: str
    evidence_title: str
    lifecycle_state: str
    reviewer_action: str
    reviewer_status: str
    rationale: str
    supported_sections: list[str] = field(default_factory=list)
    confidence_effect: str = ""
    validation_status: str = ""
    ranking_score: float | None = None
    timestamp: str = ""


def build_evidence_workflow_entry(
    *,
    project_id: str,
    evidence: dict[str, Any],
    lifecycle_state: str,
    reviewer_action: str,
    reviewer_status: str = "",
    rationale: str = "",
    project_question_id: str = "",
    decision_run_id: str = "",
    supported_sections: list[str] | None = None,
    confidence_effect: str = "",
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic audit entry for project evidence workflow events."""
    entry = EvidenceWorkflowLedgerEntry(
        ledger_id=str(uuid4())[:8],
        project_id=project_id,
        project_question_id=project_question_id,
        decision_run_id=decision_run_id,
        evidence_id=str(evidence.get("evidence_id") or ""),
        trace_id=str(evidence.get("trace_id") or ""),
        evidence_title=str(evidence.get("title") or "Untitled evidence"),
        lifecycle_state=lifecycle_state,
        reviewer_action=reviewer_action,
        reviewer_status=reviewer_status or lifecycle_state,
        rationale=rationale,
        supported_sections=supported_sections or [],
        confidence_effect=confidence_effect,
        validation_status=str(evidence.get("validation_status") or ""),
        ranking_score=_ranking_score(evidence),
        timestamp=timestamp or datetime.now().isoformat(timespec="seconds"),
    )
    return {
        "ledger_id": entry.ledger_id,
        "project_id": entry.project_id,
        "project_question_id": entry.project_question_id,
        "decision_run_id": entry.decision_run_id,
        "evidence_id": entry.evidence_id,
        "trace_id": entry.trace_id,
        "evidence_title": entry.evidence_title,
        "lifecycle_state": entry.lifecycle_state,
        "reviewer_action": entry.reviewer_action,
        "reviewer_status": entry.reviewer_status,
        "rationale": entry.rationale,
        "supported_sections": entry.supported_sections,
        "confidence_effect": entry.confidence_effect,
        "validation_status": entry.validation_status,
        "ranking_score": entry.ranking_score,
        "timestamp": entry.timestamp,
    }


def confidence_effect_for_evidence(evidence: dict[str, Any]) -> str:
    """Return additive confidence-effect metadata without changing confidence behavior."""
    conflict = str(evidence.get("conflict_status") or "").strip().lower()
    validation = str(evidence.get("validation_status") or "").lower()
    tier = str(evidence.get("credibility_tier") or "")
    status = str(evidence.get("status") or "").lower()
    if conflict and conflict != "no conflict":
        return "requires_reviewer_attention"
    if validation and validation != "valid":
        return "weakens_confidence_metadata"
    if tier in {"Tier 1 Official", "Tier 2 Company", "Tier 3 Reputable News"} and status in {"accepted", "used", "verified", "corroborated"}:
        return "strengthens_confidence_metadata"
    return "neutral_confidence_metadata"


def build_evidence_ledger(
    *,
    issue: Any | None,
    source_url: str,
    analogues: list[Any],
    mechanisms: list[Any],
    evidence_assessments: list[Any],
    historical_outcomes: list[Any],
    contexts: list[Any],
    project_evidence: list[dict[str, Any]] | None = None,
) -> EvidenceLedger:
    """Build a deterministic evidence ledger from existing pipeline outputs."""
    items: list[EvidenceItem] = []
    input_identity = _input_source_identity(source_url, issue)

    if issue is not None:
        items.append(
            EvidenceItem(
                evidence_id=_next_id(items),
                source_type=_source_type(source_url),
                evidence_text=getattr(issue, "summary", "") or getattr(issue, "core_issue", "") or "Input material was processed.",
                observation=getattr(issue, "core_issue", "") or "A primary issue was extracted from the supplied material.",
                inference="The extracted issue defines the decision frame; reviewer conclusions should not extend beyond the supplied source material without further verification.",
                claim_supported="Situation understanding and decision framing.",
                relevance="High",
                confidence="Moderate",
                limitations="Source detail depends on the supplied material. No primary supporting source is currently available unless a readable URL was provided.",
                used_in_section="Decision Snapshot; Decision Question; Decision Criteria",
                source_identity=input_identity,
                source_status="URL supplied" if source_url else "User-provided material",
                externally_sourced=bool(source_url and source_url != "source pending"),
            )
        )
    else:
        items.append(
            EvidenceItem(
                evidence_id=_next_id(items),
                source_type=_source_type(source_url),
                evidence_text="No primary issue was extracted.",
                observation="The input did not produce a structured issue.",
                inference="Decision support should remain limited until the input is clarified.",
                claim_supported="Limitations.",
                relevance="Moderate",
                confidence="Low",
                limitations="Issue extraction failed or returned no issue.",
                used_in_section="Evidence and Confidence",
                source_identity=input_identity,
                source_status="Source pending",
                externally_sourced=False,
            )
        )

    for evidence in (project_evidence or [])[:5]:
        evidence_id = str(evidence.get("evidence_id") or _next_id(items))
        summary = str(evidence.get("summary") or evidence.get("text_excerpt") or "").strip()
        source_type = str(evidence.get("source_type") or "Project evidence").strip()
        status = str(evidence.get("status") or "User Provided").strip()
        freshness = str(evidence.get("freshness_note") or "").strip()
        items.append(
            EvidenceItem(
                evidence_id=evidence_id,
                source_type=source_type,
                evidence_text=summary or str(evidence.get("title") or "Project evidence item").strip(),
                observation=str(evidence.get("title") or "Selected project evidence was included in the run.").strip(),
                inference="This evidence was selected from the project evidence library and should inform reviewer comparison only through the deterministic evidence ledger.",
                claim_supported="Project evidence bundle and reviewer-selected context.",
                relevance="High",
                confidence=_confidence_from_status(status),
                limitations=f"Evidence status: {status}. {freshness}".strip(),
                used_in_section="Project Evidence Bundle; Evidence and Confidence",
                source_identity=_project_source_identity(evidence),
                source_status=status,
                externally_sourced=_is_traceable_project_source(evidence),
            )
        )

    for analogue in analogues[:3]:
        items.append(
            EvidenceItem(
                evidence_id=_next_id(items),
                source_type="Local historical analogue record",
                evidence_text=_analogue_text(analogue),
                observation=getattr(analogue, "similarity_reason", "") or "A historical analogue was retrieved.",
                inference="The analogue supports comparison of mechanisms and response patterns; it does not determine the current outcome.",
                claim_supported="Historical comparison and analogue reasoning.",
                relevance="Moderate",
                confidence="Moderate",
                limitations=_analogue_limitations(analogue),
                used_in_section="Historical Evidence; Evidence and Confidence",
                source_identity=_analogue_identity(analogue),
                source_status="Unverified local analogue",
                externally_sourced=False,
            )
        )

    for mechanism in mechanisms[:2]:
        items.append(
            EvidenceItem(
                evidence_id=_next_id(items),
                source_type="Deterministic mechanism detection",
                evidence_text=getattr(mechanism, "description", "") or getattr(mechanism, "mechanism_name", "Mechanism detected."),
                observation=getattr(mechanism, "possible_observations", "") or "A mechanism was detected from issue and scenario cues.",
                inference=getattr(mechanism, "detection_reason", "") or "The mechanism explains how pressure could move from source material into operations, customers, suppliers, or compliance work.",
                claim_supported="Mechanism reasoning and risk identification.",
                relevance="Moderate",
                confidence=_confidence_from_note(getattr(mechanism, "confidence_note", "")),
                limitations="Mechanism detection is deterministic and should be reviewed against source details.",
                used_in_section="Mechanisms Detected; Evidence and Confidence",
                source_identity=input_identity,
                source_status="Derived deterministic record",
                externally_sourced=False,
            )
        )

    for assessment in evidence_assessments[:2]:
        supporting = getattr(assessment, "supporting_evidence", []) or []
        weakening = getattr(assessment, "weakening_evidence", []) or []
        missing = getattr(assessment, "missing_evidence", []) or []
        items.append(
            EvidenceItem(
                evidence_id=_next_id(items),
                source_type="Evidence assessment",
                evidence_text="; ".join(supporting[:2]) or "Evidence assessment generated from multi-lens interpretation.",
                observation=f"{getattr(assessment, 'lens', 'Interpretation')} has supporting and weakening evidence.",
                inference="Reviewer conclusions should remain constrained where weakening or missing evidence remains.",
                claim_supported="Evidence quality and uncertainty.",
                relevance="High",
                confidence=_normalize_confidence(getattr(assessment, "confidence_language", "")),
                limitations="; ".join((weakening + missing)[:2]) or "No specific weakening or missing evidence was listed.",
                used_in_section="Supporting Evidence; Weakening Evidence; Missing Evidence",
                source_identity=input_identity,
                source_status="Derived deterministic record",
                externally_sourced=False,
            )
        )

    for outcome in historical_outcomes[:2]:
        items.append(
            EvidenceItem(
                evidence_id=_next_id(items),
                source_type="Local historical outcome record",
                evidence_text=getattr(outcome, "observed_outcome", "") or "Historical outcome record retrieved.",
                observation=getattr(outcome, "strategic_response", "") or "Historical response pattern was retrieved.",
                inference="The outcome informs possible response patterns and monitoring priorities; it is not a forecast.",
                claim_supported="Historical outcomes and strategic lessons.",
                relevance="Moderate",
                confidence=_normalize_confidence(getattr(outcome, "confidence", "")),
                limitations=getattr(outcome, "source_status", "") or "Outcome record should be reviewed before executive use.",
                used_in_section="Historical Outcomes; Historical Evidence",
                source_identity=_outcome_identity(outcome),
                source_status="Unverified local historical outcome",
                externally_sourced=False,
            )
        )

    for context in contexts[:2]:
        items.append(
            EvidenceItem(
                evidence_id=_next_id(items),
                source_type="Local current-context record",
                evidence_text=getattr(context, "context_summary", "") or "Current-context record retrieved.",
                observation=getattr(context, "why_it_matters", "") or "Context may affect decision interpretation.",
                inference=getattr(context, "monitoring_considerations", "") or "Context should inform monitoring.",
                claim_supported="Monitoring and current context.",
                relevance="Moderate",
                confidence="Moderate",
                limitations="Current-context records are local references and may not reflect live updates.",
                used_in_section="Current Context; Monitoring Considerations",
                source_identity=_context_identity(context),
                source_status="Unverified local context",
                externally_sourced=False,
            )
        )

    return EvidenceLedger(items=items)


def _ranking_score(evidence: dict[str, Any]) -> float | None:
    value = evidence.get("ranking_score")
    if value is None:
        value = evidence.get("relevance_score")
    if isinstance(value, (int, float)):
        return round(float(value), 3)
    return None


def _next_id(items: list[EvidenceItem]) -> str:
    return f"E{len(items) + 1}"


def _source_type(source_url: str) -> str:
    return "User-provided readable URL or extracted page text" if source_url else "User-provided input material"


def _input_source_identity(source_url: str, issue: Any | None) -> str:
    if source_url and source_url != "source pending":
        return f"url:{source_url.strip().lower()}"
    text = "|".join(
        [
            str(getattr(issue, "title", "") or ""),
            str(getattr(issue, "core_issue", "") or ""),
            str(getattr(issue, "summary", "") or ""),
        ]
    )
    return f"input:{sha256(text.encode('utf-8')).hexdigest()[:16]}"


def _project_source_identity(evidence: dict[str, Any]) -> str:
    for key in ("source_url", "source_name", "publisher", "trace_id", "evidence_id"):
        value = str(evidence.get(key) or "").strip().lower()
        if value and value != "source pending":
            return f"{key}:{value}"
    text = str(evidence.get("summary") or evidence.get("text_excerpt") or evidence.get("title") or "")
    return f"project:{sha256(text.encode('utf-8')).hexdigest()[:16]}"


def _is_traceable_project_source(evidence: dict[str, Any]) -> bool:
    values = [
        str(evidence.get(key) or "").strip().lower()
        for key in ("source_url", "source_name", "publisher", "trace_id")
    ]
    return any(value and value != "source pending" for value in values)


def _analogue_identity(analogue: Any) -> str:
    title = str(getattr(analogue, "case_title", "") or "historical analogue").strip().lower()
    year = str(getattr(analogue, "year", "") or "").strip()
    return f"local-analogue:{title}:{year}"


def _outcome_identity(outcome: Any) -> str:
    title = str(getattr(outcome, "case_title", "") or getattr(outcome, "case_name", "") or "historical outcome")
    return f"local-outcome:{title.strip().lower()}"


def _context_identity(context: Any) -> str:
    title = str(getattr(context, "context_title", "") or getattr(context, "title", "") or "current context")
    return f"local-context:{title.strip().lower()}"


def _analogue_text(analogue: Any) -> str:
    title = getattr(analogue, "case_title", "") or "Historical analogue"
    year = getattr(analogue, "year", "")
    reason = getattr(analogue, "business_relevance", "") or getattr(analogue, "geopolitical_relevance", "")
    label = f"{title} ({year})" if year else title
    return f"{label}: {reason}" if reason else label


def _analogue_limitations(analogue: Any) -> str:
    source_url = getattr(analogue, "source_url", "") or ""
    source_title = getattr(analogue, "source_title", "") or ""
    base = getattr(analogue, "caution_note", "") or "Historical similarity supports comparison, not prediction."
    if source_url and source_url != "source pending":
        return f"{base} Reference: {source_title or source_url} ({source_url})."
    return f"{base} Based on the repository's curated historical knowledge base; no primary supporting source is currently available."


def _confidence_from_note(note: str) -> str:
    if "high" in note.lower():
        return "High"
    if "moderate" in note.lower() or "medium" in note.lower():
        return "Moderate"
    return "Low" if "limited" in note.lower() or "pending" in note.lower() else "Moderate"


def _normalize_confidence(value: str) -> str:
    lowered = value.lower()
    if lowered in {"high", "substantial"}:
        return "High"
    if lowered in {"moderate", "medium"}:
        return "Moderate"
    return "Low" if lowered in {"low", "limited"} else "Moderate"


def _confidence_from_status(status: str) -> str:
    if status in {"Verified", "Corroborated", "Accepted", "Used"}:
        return "High"
    if status in {"Outdated", "Unavailable", "Conflicting"}:
        return "Low"
    return "Moderate"
