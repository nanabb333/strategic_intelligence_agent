"""Deterministic decision pathway draft generation for reviewer comparison."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from decision_support_utils import unique_refs, unique_strings
from decision_readiness import build_project_decision_readiness


PATHWAY_FAMILIES = {
    "maintain_current_course",
    "delay_or_wait",
    "accelerate_or_expand",
    "diversify_or_hedge",
    "reduce_exposure",
    "seek_regulatory_clarity",
    "staged_commitment",
    "contingency_preparation",
    "further_evidence_required",
}
INSUFFICIENT_STATES = {"not_ready_insufficient_evidence", "blocked_by_conflicts"}


@dataclass(frozen=True)
class DecisionPathwayDraft:
    """Reviewer-facing pathway scaffold without ranking, scores, or recommendations."""

    pathway_id: str
    title: str
    pathway_family: str
    description: str
    applicable_frameworks: list[dict[str, str]] = field(default_factory=list)
    supporting_evidence_refs: list[dict[str, str]] = field(default_factory=list)
    related_risk_categories: list[str] = field(default_factory=list)
    related_constraints: list[str] = field(default_factory=list)
    historical_support_refs: list[dict[str, str]] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    tradeoffs: list[str] = field(default_factory=list)
    decision_triggers: list[str] = field(default_factory=list)
    reviewer_questions: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DecisionPathwayDraftSet:
    """Complete pathway draft set generated from a readiness map."""

    decision_question: str
    readiness_state: str
    primary_framework: dict[str, str]
    pathway_drafts: list[DecisionPathwayDraft]
    limitation_notes: list[str] = field(default_factory=list)
    generation_note: str = (
        "Pathway drafts are deterministic scaffolds for reviewer comparison; they are not recommendations, "
        "rankings, forecasts, investment advice, or legal advice."
    )


def build_decision_pathway_drafts(
    *,
    decision_question: str = "",
    decision_context: str = "",
    readiness_map: dict[str, Any] | None = None,
    applicable_frameworks: list[dict[str, str]] | None = None,
    accepted_evidence_refs: list[dict[str, str]] | None = None,
    evidence_intelligence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate deterministic pathway drafts from a DecisionReadinessMap."""
    readiness = readiness_map or {}
    state = _readiness_state(readiness)
    frameworks = applicable_frameworks or readiness.get("applicable_frameworks", [])
    evidence_refs = unique_refs([*(accepted_evidence_refs or []), *_supporting_refs(readiness)])
    limitations = _limitation_notes(readiness)
    families = _pathway_families_for_state(state, readiness)
    drafts = [
        _draft_for_family(
            family=family,
            index=index,
            decision_question=decision_question or readiness.get("decision_question", ""),
            readiness=readiness,
            frameworks=frameworks,
            evidence_refs=evidence_refs,
            evidence_intelligence=evidence_intelligence or {},
            limitations=limitations,
        )
        for index, family in enumerate(families, start=1)
    ]
    draft_set = DecisionPathwayDraftSet(
        decision_question=(decision_question or readiness.get("decision_question", "")).strip(),
        readiness_state=state,
        primary_framework=readiness.get("primary_framework", {}),
        pathway_drafts=drafts,
        limitation_notes=limitations,
    )
    return asdict(draft_set)


def build_project_decision_pathway_drafts(project: dict[str, Any]) -> dict[str, Any]:
    """Build pathway drafts from project data without mutating the project."""
    readiness = build_project_decision_readiness(project)
    return build_decision_pathway_drafts(readiness_map=readiness)


def _pathway_families_for_state(state: str, readiness: dict[str, Any]) -> list[str]:
    if state == "not_ready_insufficient_evidence":
        return ["further_evidence_required"]
    if state == "blocked_by_regulatory_uncertainty":
        return ["seek_regulatory_clarity"]
    if state == "blocked_by_conflicts":
        return ["further_evidence_required"]

    families = ["staged_commitment", "delay_or_wait", "contingency_preparation"]
    risks = set(_risk_categories(readiness))
    constraints = set(_constraints(readiness))
    if risks & {"market_risk", "financial_risk", "supply_chain_risk", "geopolitical_risk"}:
        families.append("diversify_or_hedge")
    elif state == "ready_for_pathway_analysis":
        families.append("maintain_current_course")
    if risks & {"financial_risk", "counterparty_risk", "sanctions_export_control_risk"}:
        families[-1] = "reduce_exposure"
    if constraints and state != "blocked_by_regulatory_uncertainty":
        families[-1] = "seek_regulatory_clarity"
    return unique_strings(families)[:4]


def _draft_for_family(
    *,
    family: str,
    index: int,
    decision_question: str,
    readiness: dict[str, Any],
    frameworks: list[dict[str, str]],
    evidence_refs: list[dict[str, str]],
    evidence_intelligence: dict[str, Any],
    limitations: list[str],
) -> DecisionPathwayDraft:
    title = _title_for_family(family)
    related_risks = _risk_categories(readiness)
    related_constraints = _constraints(readiness)
    historical_refs = _historical_refs(readiness)
    assumptions = [item.get("explanation", "") for item in readiness.get("assumption_map", []) if item.get("explanation")]
    unknowns = [item.get("explanation", "") for item in readiness.get("unknowns_map", []) if item.get("explanation")]
    for result in (readiness.get("domain_evaluation") or {}).get("results", []):
        assumptions.extend(result.get("assumptions", []))
        unknowns.extend(result.get("unknowns", []))
    questions = _questions_for_family(family, readiness)
    return DecisionPathwayDraft(
        pathway_id=f"pathway_draft_{index}_{family}",
        title=title,
        pathway_family=family,
        description=_description_for_family(family, decision_question),
        applicable_frameworks=frameworks,
        supporting_evidence_refs=_refs_for_family(family, evidence_refs, readiness, evidence_intelligence),
        related_risk_categories=related_risks,
        related_constraints=related_constraints,
        historical_support_refs=historical_refs,
        assumptions=assumptions[:5],
        unknowns=unknowns[:6],
        tradeoffs=_tradeoffs_for_family(family),
        decision_triggers=_triggers_for_family(family, readiness),
        reviewer_questions=questions,
        limitation_notes=_family_limitations(family, readiness, limitations),
    )


def _title_for_family(family: str) -> str:
    titles = {
        "maintain_current_course": "Possible pathway: Maintain current course",
        "delay_or_wait": "Possible pathway: Delay or wait",
        "accelerate_or_expand": "Possible pathway: Accelerate or expand",
        "diversify_or_hedge": "Possible pathway: Diversify or hedge",
        "reduce_exposure": "Possible pathway: Reduce exposure",
        "seek_regulatory_clarity": "Possible pathway: Seek regulatory clarity",
        "staged_commitment": "Possible pathway: Staged commitment",
        "contingency_preparation": "Possible pathway: Contingency preparation",
        "further_evidence_required": "Possible pathway: Further evidence required",
    }
    return titles.get(family, "Possible pathway: Reviewer-defined pathway")


def _description_for_family(family: str, decision_question: str) -> str:
    context = decision_question or "the current decision question"
    descriptions = {
        "maintain_current_course": f"This pathway preserves the current posture while reviewers validate evidence for {context}.",
        "delay_or_wait": f"This pathway delays commitment while reviewers resolve evidence gaps and timing questions for {context}.",
        "accelerate_or_expand": f"This pathway frames an expanded posture that would require reviewer validation of evidence, constraints, and execution capacity for {context}.",
        "diversify_or_hedge": f"This pathway compares diversified exposure or hedging structures against current risks and unknowns for {context}.",
        "reduce_exposure": f"This pathway frames lower exposure while reviewers test risk, constraint, and evidence assumptions for {context}.",
        "seek_regulatory_clarity": f"This pathway centers legal or compliance review before pathway comparison advances for {context}.",
        "staged_commitment": f"This pathway uses staged commitment points so reviewers can compare evidence, triggers, and unknowns for {context}.",
        "contingency_preparation": f"This pathway prepares fallback actions tied to specific decision triggers and evidence changes for {context}.",
        "further_evidence_required": f"This pathway keeps pathway generation limited until reviewers add or verify evidence for {context}.",
    }
    return descriptions.get(family, f"This pathway would require reviewer validation for {context}.")


def _tradeoffs_for_family(family: str) -> list[str]:
    tradeoffs = {
        "maintain_current_course": ["Continuity versus missed adaptation", "Lower disruption versus delayed response"],
        "delay_or_wait": ["More evidence versus slower action", "Reduced uncertainty versus timing risk"],
        "accelerate_or_expand": ["Speed versus execution burden", "Potential upside versus evidence sufficiency"],
        "diversify_or_hedge": ["Resilience versus added complexity", "Risk reduction versus resource cost"],
        "reduce_exposure": ["Risk containment versus opportunity loss", "Lower exposure versus reversibility"],
        "seek_regulatory_clarity": ["Review completeness versus timing", "Constraint clarity versus operational delay"],
        "staged_commitment": ["Flexibility versus coordination burden", "Incremental validation versus slower scale"],
        "contingency_preparation": ["Preparedness versus planning overhead", "Optionality versus resource commitment"],
        "further_evidence_required": ["Evidence quality versus pathway completeness", "Review rigor versus immediate comparison"],
    }
    return tradeoffs.get(family, ["Reviewer validation versus uncertainty"])


def _triggers_for_family(family: str, readiness: dict[str, Any]) -> list[str]:
    base = [
        "New accepted evidence changes the readiness map.",
        "A reviewer resolves a key unknown or evidence gap.",
    ]
    if family == "seek_regulatory_clarity":
        base.append("Legal or compliance review verifies jurisdiction and applicability.")
    if family == "further_evidence_required":
        base.append("Missing framework evidence is added to the project evidence library.")
    if readiness.get("conflict_flags"):
        base.append("Potentially conflicting evidence is reconciled or documented.")
    if readiness.get("freshness_flags"):
        base.append("Stale or undated evidence is refreshed or verified.")
    return base


def _questions_for_family(family: str, readiness: dict[str, Any]) -> list[str]:
    questions = [item.get("question", "") for item in readiness.get("reviewer_questions", []) if item.get("question")]
    if readiness.get("conflict_flags"):
        questions.insert(0, "Which conflicting evidence should be verified before pathway comparison?")
    family_questions = {
        "seek_regulatory_clarity": [
            "Has legal/compliance reviewed the relevant exposure?",
            "Which jurisdiction and applicability assumptions require verification?",
        ],
        "further_evidence_required": [
            "Which evidence gap prevents pathway comparison?",
            "What accepted evidence would make pathway drafting more defensible?",
        ],
        "staged_commitment": [
            "Which trigger would validate the next stage?",
            "What evidence would pause further commitment?",
        ],
        "contingency_preparation": [
            "Which event would activate a fallback path?",
            "Which unknowns matter most for contingency timing?",
        ],
    }
    return unique_strings([*family_questions.get(family, []), *questions])[:6]


def _family_limitations(family: str, readiness: dict[str, Any], limitations: list[str]) -> list[str]:
    output = list(limitations)
    if family == "seek_regulatory_clarity":
        output.append("This pathway is not legal advice; reviewer should verify jurisdiction and applicability.")
    if family == "further_evidence_required":
        output.append("Pathway comparison is limited until evidence gaps are addressed.")
    if readiness.get("conflict_flags"):
        output.append("Unresolved conflicts limit confidence in pathway comparison.")
    if readiness.get("freshness_flags") or readiness.get("source_diversity_flags"):
        output.append("Freshness or source diversity limitations require reviewer validation.")
    return unique_strings(output)


def _limitation_notes(readiness: dict[str, Any]) -> list[str]:
    notes = [
        "Pathway drafts are scaffolds for reviewer comparison, not recommendations.",
        "No probabilities, rankings, investment advice, or legal advice are provided.",
    ]
    state = _readiness_state(readiness)
    if state == "blocked_by_regulatory_uncertainty":
        notes.append("Regulatory or legal constraint exposure requires reviewer verification.")
    if readiness.get("conflict_flags"):
        notes.append("Potential evidence conflicts require reviewer review.")
    if readiness.get("freshness_flags"):
        notes.append("Stale or undated evidence may limit pathway usefulness.")
    if readiness.get("source_diversity_flags"):
        notes.append("Source concentration may limit pathway comparison.")
    for result in (readiness.get("domain_evaluation") or {}).get("results", []):
        notes.extend(result.get("limitation_notes", []))
    return notes


def _refs_for_family(
    family: str,
    evidence_refs: list[dict[str, str]],
    readiness: dict[str, Any],
    evidence_intelligence: dict[str, Any],
) -> list[dict[str, str]]:
    if family == "seek_regulatory_clarity":
        refs = _refs_from_items(readiness.get("constraint_coverage", []), "constraints")
        return unique_refs(refs or evidence_refs)
    if family == "further_evidence_required":
        refs = _refs_from_issues(readiness.get("readiness_issues", []))
        return unique_refs(refs or evidence_refs)
    if family in {"diversify_or_hedge", "reduce_exposure"}:
        refs = _refs_from_items(readiness.get("risk_coverage", []), "risks")
        return unique_refs(refs or evidence_refs)[:8]
    if evidence_intelligence.get("traceable_signals"):
        refs = _refs_from_signals(evidence_intelligence.get("traceable_signals", []))
        return unique_refs(refs or evidence_refs)[:8]
    return evidence_refs[:8]


def _supporting_refs(readiness: dict[str, Any]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    refs.extend(_refs_from_items(readiness.get("risk_coverage", []), "risks"))
    refs.extend(_refs_from_items(readiness.get("constraint_coverage", []), "constraints"))
    refs.extend(_historical_refs(readiness))
    refs.extend(_refs_from_issues(readiness.get("readiness_issues", [])))
    for result in (readiness.get("domain_evaluation") or {}).get("results", []):
        refs.extend(result.get("evidence_refs", []))
    for framework_map in readiness.get("framework_evidence_maps", []):
        categories = framework_map.get("evidence_coverage", {}).get("required_evidence_categories", [])
        for category in categories:
            refs.extend(category.get("evidence_refs", []))
    return unique_refs(refs)


def _refs_from_items(groups: list[dict[str, Any]], child_key: str) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for group in groups:
        for item in group.get(child_key, []):
            refs.extend(item.get("evidence_refs", []))
    return refs


def _historical_refs(readiness: dict[str, Any]) -> list[dict[str, str]]:
    return _refs_from_items(readiness.get("historical_support", []), "historical_dimensions")


def _refs_from_issues(issues: list[dict[str, Any]]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for issue in issues:
        refs.extend(issue.get("evidence_refs", []))
    return refs


def _refs_from_signals(signals: list[dict[str, Any]]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for signal in signals:
        refs.extend(signal.get("evidence_refs", []))
    return refs


def _risk_categories(readiness: dict[str, Any]) -> list[str]:
    categories = []
    for group in readiness.get("risk_coverage", []):
        for item in group.get("risks", []):
            if item.get("coverage_bucket") == "covered":
                categories.append(item.get("dimension", ""))
    for result in (readiness.get("domain_evaluation") or {}).get("results", []):
        categories.extend(result.get("risk_categories", []))
    return unique_strings(categories)


def _constraints(readiness: dict[str, Any]) -> list[str]:
    constraints = []
    for group in readiness.get("constraint_coverage", []):
        for item in group.get("constraints", []):
            if item.get("coverage_bucket") == "covered":
                constraints.append(item.get("dimension", ""))
    for result in (readiness.get("domain_evaluation") or {}).get("results", []):
        constraints.extend(result.get("constraints", []))
    return unique_strings(constraints)


def _readiness_state(readiness: dict[str, Any]) -> str:
    return str((readiness.get("readiness_summary") or {}).get("readiness_state") or "unknown")

