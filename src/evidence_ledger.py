"""Evidence ledger structures for reviewable decision support."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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


@dataclass
class EvidenceLedger:
    """Collection of evidence records used by a decision case."""

    items: list[EvidenceItem] = field(default_factory=list)

    def ids(self) -> list[str]:
        """Return stable evidence identifiers for downstream artifacts."""
        return [item.evidence_id for item in self.items]


def build_evidence_ledger(
    *,
    issue: Any | None,
    source_url: str,
    analogues: list[Any],
    mechanisms: list[Any],
    evidence_assessments: list[Any],
    historical_outcomes: list[Any],
    contexts: list[Any],
) -> EvidenceLedger:
    """Build a deterministic evidence ledger from existing pipeline outputs."""
    items: list[EvidenceItem] = []

    if issue is not None:
        items.append(
            EvidenceItem(
                evidence_id=_next_id(items),
                source_type=_source_type(source_url),
                evidence_text=getattr(issue, "summary", "") or getattr(issue, "core_issue", "") or "Input material was processed.",
                observation=getattr(issue, "core_issue", "") or "A primary issue was extracted from the supplied material.",
                inference="The extracted issue defines the decision frame; the recommendation should not extend beyond the supplied source material without human review.",
                claim_supported="Situation understanding and decision framing.",
                relevance="High",
                confidence="Moderate",
                limitations="Source detail depends on the supplied material. No primary supporting source is currently available unless a readable URL was provided.",
                used_in_section="Decision Snapshot; Decision Question; Decision Criteria",
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
                inference="The recommendation should be constrained where weakening or missing evidence remains.",
                claim_supported="Evidence quality and uncertainty.",
                relevance="High",
                confidence=_normalize_confidence(getattr(assessment, "confidence_language", "")),
                limitations="; ".join((weakening + missing)[:2]) or "No specific weakening or missing evidence was listed.",
                used_in_section="Supporting Evidence; Weakening Evidence; Missing Evidence",
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
            )
        )

    return EvidenceLedger(items=items)


def _next_id(items: list[EvidenceItem]) -> str:
    return f"E{len(items) + 1}"


def _source_type(source_url: str) -> str:
    return "User-provided readable URL or extracted page text" if source_url else "User-provided input material"


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
