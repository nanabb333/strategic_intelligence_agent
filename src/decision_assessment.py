"""Neutral Decision Assessment schema and deterministic builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


ASSESSMENT_CONTRACT = "neutral-decision-assessment-v1"


@dataclass(frozen=True)
class PathwayEvidence:
    """Evidence references grouped without implying pathway selection."""

    supporting: list[dict[str, Any]] = field(default_factory=list)
    weakening: list[dict[str, Any]] = field(default_factory=list)
    gaps: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class PathwayConditions:
    """Directional conditions supplied by an upstream neutral adapter."""

    more_supportable_when: list[str] = field(default_factory=list)
    less_supportable_when: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class JudgmentBoundary:
    """Explicitly reserve decision ownership for the human reviewer."""

    owner: str = "reviewer"
    statement: str = "The system does not rank or select a pathway. Final judgment remains with the reviewer."


@dataclass(frozen=True)
class PathwayForReview:
    """One evidence-aware pathway presented for non-evaluative review."""

    pathway_id: str
    title: str
    pathway_family: str
    description: str
    pathway_evidence: PathwayEvidence = field(default_factory=PathwayEvidence)
    pathway_tradeoffs: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    reversibility: str = "Not assessed"
    timing_implications: str = "Not assessed"
    assumptions: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    pathway_conditions: PathwayConditions = field(default_factory=PathwayConditions)
    change_triggers: list[str] = field(default_factory=list)
    reviewer_questions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class NeutralDecisionAssessment:
    """Dependency-light schema for a neutral, reviewer-owned assessment."""

    decision_question: str
    assessment_summary: str
    comparison_criteria: list[str]
    pathways_for_review: list[PathwayForReview]
    strategic_considerations: list[str] = field(default_factory=list)
    change_triggers: list[str] = field(default_factory=list)
    reviewer_questions: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    reviewer_selected_path: str = ""
    selection_rationale: str = ""
    selection_status: str = "No pathway selected"
    judgment_boundary: JudgmentBoundary = field(default_factory=JudgmentBoundary)
    assessment_contract: str = ASSESSMENT_CONTRACT


def build_neutral_decision_assessment(
    *,
    assessment_summary: str = "",
    pathway_draft_set: dict[str, Any] | None = None,
    comparison_matrix: dict[str, Any] | None = None,
    pathway_evidence: dict[str, dict[str, list[dict[str, Any]]]] | None = None,
    pathway_conditions: dict[str, dict[str, list[str]]] | None = None,
) -> NeutralDecisionAssessment:
    """Build a neutral assessment from normalized pathway and comparison outputs.

    Pathways use lexical pathway ID order solely for deterministic serialization;
    the order has no evaluative meaning. Directional conditions and weakening or
    gap evidence remain empty unless an upstream adapter supplies them explicitly.
    """
    draft_set = pathway_draft_set or {}
    matrix = comparison_matrix or {}
    evidence_by_pathway = pathway_evidence or {}
    conditions_by_pathway = pathway_conditions or {}
    comparison_rows = {
        str(row.get("pathway_id") or ""): row
        for row in matrix.get("pathway_comparisons", [])
        if row.get("pathway_id")
    }
    drafts = sorted(
        draft_set.get("pathway_drafts", []),
        key=lambda item: str(item.get("pathway_id") or ""),
    )
    pathways = [
        _pathway_for_review(
            draft,
            comparison_rows.get(str(draft.get("pathway_id") or ""), {}),
            evidence_by_pathway.get(str(draft.get("pathway_id") or ""), {}),
            conditions_by_pathway.get(str(draft.get("pathway_id") or ""), {}),
        )
        for draft in drafts
    ]
    return NeutralDecisionAssessment(
        decision_question=str(
            draft_set.get("decision_question") or matrix.get("decision_question") or ""
        ).strip(),
        assessment_summary=assessment_summary.strip(),
        comparison_criteria=_strings(matrix.get("comparison_dimensions", [])),
        pathways_for_review=pathways,
        strategic_considerations=_strategic_considerations(pathways),
        change_triggers=_collect(pathways, "change_triggers"),
        reviewer_questions=_collect(pathways, "reviewer_questions"),
        assumptions=_collect(pathways, "assumptions"),
        unknowns=_collect(pathways, "unknowns"),
        constraints=_collect(pathways, "constraints"),
        limitations=_strings(
            [
                *draft_set.get("limitation_notes", []),
                *matrix.get("limitation_notes", []),
            ]
        ),
    )


def _pathway_for_review(
    draft: dict[str, Any],
    comparison_row: dict[str, Any],
    evidence: dict[str, list[dict[str, Any]]],
    conditions: dict[str, list[str]],
) -> PathwayForReview:
    supporting = evidence.get("supporting")
    if supporting is None:
        supporting = draft.get("supporting_evidence_refs")
    if supporting is None:
        supporting = comparison_row.get("supporting_evidence_refs", [])
    return PathwayForReview(
        pathway_id=str(draft.get("pathway_id") or ""),
        title=str(draft.get("title") or ""),
        pathway_family=str(draft.get("pathway_family") or ""),
        description=str(draft.get("description") or ""),
        pathway_evidence=PathwayEvidence(
            supporting=_references(supporting),
            weakening=_references(evidence.get("weakening", [])),
            gaps=_references(evidence.get("gaps", [])),
        ),
        pathway_tradeoffs=_strings(draft.get("tradeoffs", [])),
        risks=_strings(draft.get("related_risk_categories", [])),
        reversibility=str(comparison_row.get("reversibility") or "Not assessed"),
        timing_implications=str(comparison_row.get("time_sensitivity") or "Not assessed"),
        assumptions=_strings(draft.get("assumptions", [])),
        unknowns=_strings(draft.get("unknowns", [])),
        constraints=_strings(draft.get("related_constraints", [])),
        pathway_conditions=PathwayConditions(
            more_supportable_when=_strings(conditions.get("more_supportable_when", [])),
            less_supportable_when=_strings(conditions.get("less_supportable_when", [])),
        ),
        change_triggers=_strings(draft.get("decision_triggers", [])),
        reviewer_questions=_strings(draft.get("reviewer_questions", [])),
        limitations=_strings(draft.get("limitation_notes", [])),
    )


def normalize_stored_decision_assessment(analysis: dict[str, Any]) -> dict[str, Any]:
    """Return a current neutral assessment or an isolated legacy view.

    Legacy ``recommended_path`` values are deliberately ignored. They are not
    migrated into reviewer selection because the historical value was produced
    by the system rather than explicitly selected by a reviewer.
    """
    current = analysis.get("decision_assessment")
    if isinstance(current, dict) and current:
        normalized = dict(current)
        legacy_boundary = normalized.pop("final_judgment", None)
        if "judgment_boundary" not in normalized:
            normalized["judgment_boundary"] = _normalized_judgment_boundary(legacy_boundary)
        normalized["reviewer_selected_path"] = str(normalized.get("reviewer_selected_path") or "")
        normalized["selection_rationale"] = str(normalized.get("selection_rationale") or "")
        return normalized

    legacy = analysis.get("decision_case")
    if not isinstance(legacy, dict) or not legacy:
        return {}
    return {
        "assessment_contract": "legacy-read-only-neutral-view-v1",
        "decision_question": str(legacy.get("decision_question") or ""),
        "assessment_summary": "Legacy assessment artifact normalized for current neutral review.",
        "comparison_criteria": _strings(legacy.get("decision_criteria", [])),
        "pathways_for_review": [],
        "strategic_considerations": [],
        "change_triggers": _strings(legacy.get("change_triggers", [])),
        "reviewer_questions": [],
        "assumptions": _strings(legacy.get("assumptions", [])),
        "unknowns": [],
        "constraints": [],
        "limitations": _strings(
            [
                *legacy.get("limitations", []),
                "Legacy system-generated recommendation was ignored; no reviewer pathway selection was inferred.",
            ]
        ),
        "reviewer_selected_path": "",
        "selection_rationale": "",
        "selection_status": "No pathway selected",
        "judgment_boundary": {
            "owner": "reviewer",
            "statement": "The system does not rank or select a pathway. Final judgment remains with the reviewer.",
        },
        "legacy_compatibility": {
            "read_only": True,
            "system_recommendation_ignored": bool(legacy.get("recommended_path")),
        },
    }


def render_neutral_decision_assessment(assessment: NeutralDecisionAssessment) -> str:
    """Render a reviewer-first assessment without ranking or selection."""
    lines = [
        "# Neutral Decision Assessment",
        "",
        "## Decision Question",
        "",
        assessment.decision_question or "The decision question was not specified.",
        "",
        "## Assessment Summary",
        "",
        assessment.assessment_summary or "The available evidence supports structured reviewer comparison.",
        "",
        f"**Selection status:** {assessment.selection_status}",
        "",
        assessment.judgment_boundary.statement,
        "",
        "## Comparison Criteria",
        "",
        *_bullets(assessment.comparison_criteria, "No comparison criteria were generated."),
        "",
        "## Pathways for Review",
        "",
    ]
    for pathway in assessment.pathways_for_review:
        lines.extend(
            [
                f"### {pathway.title}",
                "",
                pathway.description,
                "",
                f"- **Pathway ID:** {pathway.pathway_id}",
                f"- **Family:** {pathway.pathway_family}",
                f"- **Reversibility:** {pathway.reversibility}",
                f"- **Timing implications:** {pathway.timing_implications}",
                "",
                "**Supporting evidence**",
                "",
                *_reference_bullets(pathway.pathway_evidence.supporting),
                "",
                "**Risks and trade-offs**",
                "",
                *_bullets([*pathway.risks, *pathway.pathway_tradeoffs], "No pathway-specific risks were mapped."),
                "",
                "**Uncertainties and assumptions**",
                "",
                *_bullets([*pathway.unknowns, *pathway.assumptions], "No pathway-specific uncertainty was mapped."),
                "",
                "**Change triggers**",
                "",
                *_bullets(pathway.change_triggers, "No change triggers were generated."),
                "",
            ]
        )
    lines.extend(
        [
            "## Strategic Considerations",
            "",
            *_bullets(assessment.strategic_considerations, "No additional strategic considerations were generated."),
            "",
            "## Reviewer Questions",
            "",
            *_bullets(assessment.reviewer_questions, "No reviewer questions were generated."),
            "",
            "## Limitations",
            "",
            *_bullets(assessment.limitations, "No additional limitations were generated."),
        ]
    )
    return "\n".join(lines).strip() + "\n"


def render_normalized_stored_assessment(assessment: dict[str, Any]) -> str:
    """Render a neutral read-only view for a normalized legacy artifact."""
    lines = [
        "# Legacy Assessment - Neutral Read-Only View",
        "",
        "## Decision Question",
        "",
        str(assessment.get("decision_question") or "Decision question not available."),
        "",
        "## Assessment Summary",
        "",
        str(assessment.get("assessment_summary") or "Legacy assessment summary not available."),
        "",
        "**Selection status:** No pathway selected",
        "",
        "The former system-generated recommendation is not displayed and was not converted into reviewer selection.",
        "",
        "## Limitations",
        "",
        *_bullets(list(assessment.get("limitations") or []), "Legacy artifact limitations were not recorded."),
    ]
    return "\n".join(lines).strip() + "\n"


def _strategic_considerations(pathways: list[PathwayForReview]) -> list[str]:
    values: list[str] = []
    for pathway in pathways:
        values.extend(pathway.pathway_tradeoffs[:2])
    return _strings(values)


def _normalized_judgment_boundary(value: Any) -> dict[str, str]:
    """Convert a legacy boundary-shaped field without treating it as a judgment."""
    if isinstance(value, dict) and str(value.get("owner") or "").lower() == "reviewer":
        statement = str(value.get("statement") or "").strip()
        if statement:
            return {"owner": "reviewer", "statement": statement}
    return {
        "owner": "reviewer",
        "statement": "The system does not rank or select a pathway. Final judgment remains with the reviewer.",
    }


def _bullets(values: list[str], fallback: str) -> list[str]:
    return [f"- {value}" for value in values] or [f"- {fallback}"]


def _reference_bullets(values: list[dict[str, Any]]) -> list[str]:
    if not values:
        return ["- No pathway-specific supporting evidence was mapped."]
    output = []
    for value in values:
        label = value.get("title") or value.get("evidence_id") or value.get("source_url") or "Evidence reference"
        output.append(f"- {label}")
    return output


def _collect(pathways: list[PathwayForReview], attribute: str) -> list[str]:
    values: list[str] = []
    for pathway in pathways:
        values.extend(getattr(pathway, attribute))
    return _strings(values)


def _strings(values: list[Any]) -> list[str]:
    output: list[str] = []
    for value in values:
        text = str(value).strip()
        if text and text not in output:
            output.append(text)
    return output


def _references(values: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[tuple[tuple[str, str], ...]] = set()
    for value in values or []:
        reference = {str(key): item for key, item in value.items()}
        identity = tuple(sorted((key, str(item)) for key, item in reference.items()))
        if identity not in seen:
            seen.add(identity)
            output.append(reference)
    return output
