"""Deterministic pathway comparison matrix for reviewer workflows."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from decision_support_utils import unique_refs, unique_strings
from decision_pathways import build_project_decision_pathway_drafts
from decision_readiness import build_project_decision_readiness
from domain_evaluation import build_project_domain_evaluation
from evidence_intelligence import build_evidence_intelligence


BUCKETS = {"low", "medium", "high", "mixed", "unknown", "not_applicable"}


@dataclass(frozen=True)
class PathwayComparisonRow:
    """One pathway row in the comparison matrix."""

    pathway_id: str
    pathway_title: str
    pathway_family: str
    evidence_support_summary: str
    supporting_evidence_refs: list[dict[str, str]]
    risk_exposure_summary: str
    regulatory_constraint_summary: str
    domain_evaluation_summary: str
    assumptions_summary: str
    unknowns_summary: str
    historical_support_summary: str
    execution_complexity: str
    reversibility: str
    time_sensitivity: str
    decision_triggers: list[str]
    reviewer_questions: list[str]
    limitation_notes: list[str]
    dimension_buckets: dict[str, str]


@dataclass(frozen=True)
class PathwayComparisonMatrix:
    """Side-by-side pathway comparison without ranking, scoring, or recommendations."""

    decision_question: str
    comparison_dimensions: list[str]
    pathway_comparisons: list[PathwayComparisonRow]
    limitation_notes: list[str] = field(default_factory=list)
    generation_note: str = (
        "Comparison matrix is deterministic and evidence-backed; it does not rank, score, recommend, "
        "forecast, provide investment advice, or provide legal advice."
    )


COMPARISON_DIMENSIONS = [
    "evidence_support",
    "risk_exposure",
    "regulatory_constraints",
    "domain_specific_risks",
    "historical_support",
    "assumptions_required",
    "unknowns_remaining",
    "execution_complexity",
    "reversibility",
    "timing_sensitivity",
    "evidence_quality_concerns",
]


def build_pathway_comparison_matrix(
    *,
    decision_question: str = "",
    pathway_draft_set: dict[str, Any] | None = None,
    readiness_map: dict[str, Any] | None = None,
    domain_evaluation: dict[str, Any] | None = None,
    evidence_intelligence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a categorical comparison matrix from pathway drafts."""
    draft_set = pathway_draft_set or {}
    readiness = readiness_map or {}
    domain = domain_evaluation or {}
    evidence = evidence_intelligence or {}
    rows = [
        _comparison_row(draft, readiness, domain, evidence)
        for draft in draft_set.get("pathway_drafts", [])
    ]
    matrix = PathwayComparisonMatrix(
        decision_question=(decision_question or draft_set.get("decision_question", "") or readiness.get("decision_question", "")).strip(),
        comparison_dimensions=COMPARISON_DIMENSIONS,
        pathway_comparisons=rows,
        limitation_notes=_matrix_limitations(readiness, domain, evidence),
    )
    return asdict(matrix)


def build_project_pathway_comparison(project: dict[str, Any]) -> dict[str, Any]:
    """Build a read-only pathway comparison matrix from project data."""
    readiness = build_project_decision_readiness(project)
    pathways = build_project_decision_pathway_drafts(project)
    domain = build_project_domain_evaluation(project)
    intelligence = build_evidence_intelligence(project.get("evidence_library", []))
    return build_pathway_comparison_matrix(
        pathway_draft_set=pathways,
        readiness_map=readiness,
        domain_evaluation=domain,
        evidence_intelligence=intelligence,
    )


def _comparison_row(
    draft: dict[str, Any],
    readiness: dict[str, Any],
    domain: dict[str, Any],
    evidence_intelligence: dict[str, Any],
) -> PathwayComparisonRow:
    refs = unique_refs(draft.get("supporting_evidence_refs", []))
    risks = draft.get("related_risk_categories", [])
    constraints = draft.get("related_constraints", [])
    unknowns = draft.get("unknowns", [])
    assumptions = draft.get("assumptions", [])
    historical_refs = unique_refs(draft.get("historical_support_refs", []))
    buckets = {
        "evidence_support": _evidence_support_bucket(refs),
        "risk_exposure": _risk_bucket(risks),
        "regulatory_constraints": _constraint_bucket(constraints, readiness),
        "domain_specific_risks": _domain_bucket(domain),
        "historical_support": _historical_bucket(historical_refs),
        "assumptions_required": _assumption_bucket(assumptions),
        "unknowns_remaining": _unknown_bucket(unknowns, readiness),
        "execution_complexity": _execution_bucket(draft, constraints, risks),
        "reversibility": _reversibility_bucket(draft),
        "timing_sensitivity": _timing_bucket(draft),
        "evidence_quality_concerns": _evidence_quality_bucket(readiness, evidence_intelligence),
    }
    return PathwayComparisonRow(
        pathway_id=draft.get("pathway_id", ""),
        pathway_title=draft.get("title", "Possible pathway"),
        pathway_family=draft.get("pathway_family", "unknown"),
        evidence_support_summary=_support_summary(refs, buckets["evidence_support"]),
        supporting_evidence_refs=refs,
        risk_exposure_summary=_list_summary("Risk exposure", risks, buckets["risk_exposure"]),
        regulatory_constraint_summary=_list_summary("Regulatory constraints", constraints, buckets["regulatory_constraints"]),
        domain_evaluation_summary=_domain_summary(domain, buckets["domain_specific_risks"]),
        assumptions_summary=_count_summary("Assumptions", assumptions, buckets["assumptions_required"]),
        unknowns_summary=_count_summary("Unknowns", unknowns, buckets["unknowns_remaining"]),
        historical_support_summary=_support_summary(historical_refs, buckets["historical_support"]),
        execution_complexity=buckets["execution_complexity"],
        reversibility=buckets["reversibility"],
        time_sensitivity=buckets["timing_sensitivity"],
        decision_triggers=draft.get("decision_triggers", []),
        reviewer_questions=draft.get("reviewer_questions", []),
        limitation_notes=_row_limitations(draft, readiness, buckets),
        dimension_buckets=buckets,
    )


def _evidence_support_bucket(refs: list[dict[str, str]]) -> str:
    if len(refs) >= 4:
        return "high"
    if len(refs) >= 2:
        return "medium"
    if len(refs) == 1:
        return "low"
    return "unknown"


def _risk_bucket(risks: list[str]) -> str:
    if len(risks) >= 5:
        return "high"
    if len(risks) >= 2:
        return "medium"
    if risks:
        return "low"
    return "unknown"


def _constraint_bucket(constraints: list[str], readiness: dict[str, Any]) -> str:
    severe = any(issue.get("issue_type") == "regulatory_uncertainty" for issue in readiness.get("readiness_issues", []))
    if severe:
        return "high"
    if len(constraints) >= 2:
        return "high"
    if constraints:
        return "medium"
    return "not_applicable"


def _domain_bucket(domain: dict[str, Any]) -> str:
    risks = [risk for result in domain.get("results", []) for risk in result.get("risk_categories", [])]
    if len(risks) >= 6:
        return "high"
    if len(risks) >= 2:
        return "medium"
    if risks:
        return "low"
    return "not_applicable"


def _historical_bucket(refs: list[dict[str, str]]) -> str:
    if len(refs) >= 2:
        return "medium"
    if len(refs) == 1:
        return "low"
    return "unknown"


def _assumption_bucket(assumptions: list[str]) -> str:
    if len(assumptions) >= 5:
        return "high"
    if len(assumptions) >= 2:
        return "medium"
    if assumptions:
        return "low"
    return "unknown"


def _unknown_bucket(unknowns: list[str], readiness: dict[str, Any]) -> str:
    unresolved = any(issue.get("issue_type") == "unresolved_conflict" for issue in readiness.get("readiness_issues", []))
    if unresolved or len(unknowns) >= 5:
        return "high"
    if len(unknowns) >= 2:
        return "medium"
    if unknowns:
        return "low"
    return "unknown"


def _execution_bucket(draft: dict[str, Any], constraints: list[str], risks: list[str]) -> str:
    family = draft.get("pathway_family", "")
    if family in {"accelerate_or_expand", "reduce_exposure"} and (constraints or len(risks) >= 3):
        return "high"
    if family in {"accelerate_or_expand", "reduce_exposure", "diversify_or_hedge", "seek_regulatory_clarity"}:
        return "medium"
    if family in {"staged_commitment", "contingency_preparation"}:
        return "medium"
    if family == "further_evidence_required":
        return "not_applicable"
    return "low"


def _reversibility_bucket(draft: dict[str, Any]) -> str:
    family = draft.get("pathway_family", "")
    if family in {"staged_commitment", "contingency_preparation", "delay_or_wait", "further_evidence_required"}:
        return "high"
    if family in {"diversify_or_hedge", "seek_regulatory_clarity"}:
        return "medium"
    if family in {"accelerate_or_expand", "reduce_exposure"}:
        return "low"
    return "mixed"


def _timing_bucket(draft: dict[str, Any]) -> str:
    family = draft.get("pathway_family", "")
    if family in {"accelerate_or_expand", "reduce_exposure"}:
        return "high"
    if family in {"staged_commitment", "contingency_preparation", "seek_regulatory_clarity"}:
        return "medium"
    if family in {"delay_or_wait", "further_evidence_required"}:
        return "low"
    return "unknown"


def _evidence_quality_bucket(readiness: dict[str, Any], evidence_intelligence: dict[str, Any]) -> str:
    if readiness.get("freshness_flags") and readiness.get("source_diversity_flags"):
        return "high"
    if readiness.get("freshness_flags") or readiness.get("source_diversity_flags"):
        return "medium"
    attention = evidence_intelligence.get("attention_items", [])
    if len(attention) >= 3:
        return "medium"
    if attention:
        return "low"
    return "not_applicable"


def _support_summary(refs: list[dict[str, str]], bucket: str) -> str:
    if refs:
        return f"Evidence support is {bucket}; {len(refs)} supporting evidence reference(s) are linked."
    return "Evidence support is unknown; no direct evidence references are linked."


def _list_summary(label: str, values: list[str], bucket: str) -> str:
    if values:
        return f"{label} bucket is {bucket}: {', '.join(values[:6])}."
    return f"{label} bucket is {bucket}."


def _count_summary(label: str, values: list[str], bucket: str) -> str:
    return f"{label} bucket is {bucket}; {len(values)} item(s) currently mapped."


def _domain_summary(domain: dict[str, Any], bucket: str) -> str:
    domains = [result.get("domain", "") for result in domain.get("results", []) if result.get("domain")]
    if domains:
        return f"Domain-specific risk bucket is {bucket}: {', '.join(domains)}."
    return f"Domain-specific risk bucket is {bucket}."


def _row_limitations(draft: dict[str, Any], readiness: dict[str, Any], buckets: dict[str, str]) -> list[str]:
    notes = list(draft.get("limitation_notes", []))
    if buckets["unknowns_remaining"] == "high":
        notes.append("Many unknowns remain; reviewer should resolve material gaps before relying on this comparison.")
    if buckets["evidence_quality_concerns"] in {"medium", "high"}:
        notes.append("Evidence quality concerns may affect pathway comparison.")
    if readiness.get("conflict_flags"):
        notes.append("Unresolved evidence conflicts require reviewer review.")
    return unique_strings(notes)


def _matrix_limitations(readiness: dict[str, Any], domain: dict[str, Any], evidence_intelligence: dict[str, Any]) -> list[str]:
    notes = [
        "The comparison matrix is a reviewer aid, not a recommendation.",
        "No ranking, scoring, probabilities, investment advice, or legal advice are provided.",
    ]
    if readiness.get("readiness_issues"):
        notes.append("Readiness issues should be reviewed before using the matrix for decision discussion.")
    if domain.get("results"):
        notes.append("Domain-specific concerns are evidence-backed and require reviewer validation.")
    if evidence_intelligence.get("attention_items"):
        notes.append("Evidence attention items may affect comparison quality.")
    return notes

