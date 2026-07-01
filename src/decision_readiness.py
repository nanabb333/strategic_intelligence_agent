"""Deterministic decision readiness mapping for reviewer workflow support."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from decision_frameworks import DecisionFramework, classify_decision_question
from decision_support_utils import latest_or_first_project_question
from domain_evaluation import build_domain_evaluation
from evidence_intelligence import build_evidence_intelligence, evidence_reference, source_category


COVERED = "covered"
PARTIALLY_COVERED = "partially_covered"
MISSING = "missing"
OVER_CONCENTRATED = "over_concentrated"
UNKNOWN = "unknown"


@dataclass(frozen=True)
class MappedEvidenceItem:
    """Evidence mapped to a framework dimension."""

    dimension: str
    coverage_bucket: str
    evidence_refs: list[dict[str, str]] = field(default_factory=list)
    matched_terms: list[str] = field(default_factory=list)
    reviewer_note: str = ""


@dataclass(frozen=True)
class FrameworkDimensionCoverage:
    """Coverage for required evidence categories and pathway dimensions."""

    framework_id: str
    required_evidence_categories: list[MappedEvidenceItem] = field(default_factory=list)
    pathway_dimensions: list[MappedEvidenceItem] = field(default_factory=list)


@dataclass(frozen=True)
class FrameworkRiskCoverage:
    """Coverage for required risk categories."""

    framework_id: str
    risks: list[MappedEvidenceItem] = field(default_factory=list)


@dataclass(frozen=True)
class FrameworkConstraintCoverage:
    """Coverage for required regulatory or legal constraint categories."""

    framework_id: str
    constraints: list[MappedEvidenceItem] = field(default_factory=list)


@dataclass(frozen=True)
class HistoricalSupportMap:
    """Framework-aware historical support mapping."""

    framework_id: str
    historical_dimensions: list[MappedEvidenceItem] = field(default_factory=list)


@dataclass(frozen=True)
class AssumptionMap:
    """Assumption category surfaced before pathway generation."""

    category: str
    explanation: str
    evidence_refs: list[dict[str, str]] = field(default_factory=list)
    related_framework_dimensions: list[str] = field(default_factory=list)
    reviewer_question: str = ""


@dataclass(frozen=True)
class UnknownsMap:
    """Unknown or missing information category surfaced for reviewer review."""

    category: str
    explanation: str
    evidence_refs: list[dict[str, str]] = field(default_factory=list)
    related_framework_dimensions: list[str] = field(default_factory=list)
    reviewer_question: str = ""


@dataclass(frozen=True)
class DecisionReadinessIssue:
    """Reviewer-facing readiness issue."""

    issue_type: str
    severity: str
    explanation: str
    evidence_refs: list[dict[str, str]] = field(default_factory=list)
    reviewer_question: str = ""


@dataclass(frozen=True)
class ReviewerQuestion:
    """Question generated from framework requirements and readiness gaps."""

    question: str
    source: str
    related_framework_id: str = ""
    related_dimension: str = ""
    evidence_refs: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class DecisionReadinessSummary:
    """Categorical readiness summary without ranking or recommendations."""

    readiness_state: str
    reviewer_summary: str
    evidence_count: int
    framework_count: int
    issue_count: int
    limitation: str = "Readiness is a workflow status, not a recommendation, forecast, investment advice, or legal advice."


@dataclass(frozen=True)
class FrameworkEvidenceMap:
    """Framework-specific mapping of evidence, risks, constraints, and history."""

    framework_id: str
    framework_name: str
    evidence_coverage: FrameworkDimensionCoverage
    risk_coverage: FrameworkRiskCoverage
    constraint_coverage: FrameworkConstraintCoverage
    historical_support: HistoricalSupportMap
    reviewer_questions: list[ReviewerQuestion] = field(default_factory=list)


@dataclass(frozen=True)
class DecisionReadinessMap:
    """Complete read-only readiness map for a project decision question."""

    decision_question: str
    applicable_frameworks: list[dict[str, str]]
    primary_framework: dict[str, str]
    framework_evidence_maps: list[FrameworkEvidenceMap]
    risk_coverage: list[FrameworkRiskCoverage]
    constraint_coverage: list[FrameworkConstraintCoverage]
    historical_support: list[HistoricalSupportMap]
    assumption_map: list[AssumptionMap]
    unknowns_map: list[UnknownsMap]
    evidence_gaps: list[DecisionReadinessIssue]
    over_concentration_flags: list[DecisionReadinessIssue]
    conflict_flags: list[DecisionReadinessIssue]
    freshness_flags: list[DecisionReadinessIssue]
    source_diversity_flags: list[DecisionReadinessIssue]
    reviewer_questions: list[ReviewerQuestion]
    readiness_issues: list[DecisionReadinessIssue]
    readiness_summary: DecisionReadinessSummary
    domain_evaluation: dict[str, Any] = field(default_factory=dict)
    domain_evaluation_issues: list[DecisionReadinessIssue] = field(default_factory=list)


def build_decision_readiness_map(
    *,
    decision_question: str,
    decision_context: str = "",
    evidence_items: list[dict[str, Any]] | None = None,
    evidence_intelligence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic, serializable readiness map."""
    evidence = list(evidence_items or [])
    intelligence = evidence_intelligence or build_evidence_intelligence(evidence)
    metadata = _classification_metadata(evidence, intelligence)
    classification = classify_decision_question(decision_question, decision_context, metadata)
    frameworks = classification.applicable_frameworks

    framework_maps = [_map_framework(framework, evidence, intelligence) for framework in frameworks]
    risk_coverage = [item.risk_coverage for item in framework_maps]
    constraint_coverage = [item.constraint_coverage for item in framework_maps]
    historical_support = [item.historical_support for item in framework_maps]
    evidence_gaps = _evidence_gap_issues(framework_maps)
    conflict_flags = _conflict_issues(intelligence)
    freshness_flags = _freshness_issues(intelligence)
    source_diversity_flags = _source_diversity_issues(intelligence)
    over_concentration_flags = _over_concentration_issues(framework_maps, source_diversity_flags)
    assumption_map = _assumption_map(intelligence, framework_maps)
    unknowns_map = _unknowns_map(framework_maps, evidence_gaps, conflict_flags, source_diversity_flags)
    domain_evaluation = build_domain_evaluation(
        decision_question=decision_question,
        decision_context=decision_context,
        evidence_items=evidence,
    )
    domain_issues = _domain_evaluation_issues(domain_evaluation)
    readiness_issues = [
        *evidence_gaps,
        *over_concentration_flags,
        *conflict_flags,
        *freshness_flags,
        *source_diversity_flags,
        *_regulatory_uncertainty_issues(framework_maps, frameworks[0].framework_id if frameworks else ""),
        *domain_issues,
    ]
    reviewer_questions = _reviewer_questions(frameworks, framework_maps, readiness_issues, assumption_map, unknowns_map)
    summary = _readiness_summary(
        evidence_count=len(evidence),
        framework_count=len(frameworks),
        readiness_issues=readiness_issues,
        framework_maps=framework_maps,
        has_question=bool((decision_question or "").strip()),
    )
    readiness_map = DecisionReadinessMap(
        decision_question=(decision_question or "").strip(),
        applicable_frameworks=[_framework_summary(framework) for framework in frameworks],
        primary_framework=_framework_summary(frameworks[0]) if frameworks else {},
        framework_evidence_maps=framework_maps,
        risk_coverage=risk_coverage,
        constraint_coverage=constraint_coverage,
        historical_support=historical_support,
        assumption_map=assumption_map,
        unknowns_map=unknowns_map,
        evidence_gaps=evidence_gaps,
        over_concentration_flags=over_concentration_flags,
        conflict_flags=conflict_flags,
        freshness_flags=freshness_flags,
        source_diversity_flags=source_diversity_flags,
        reviewer_questions=reviewer_questions,
        readiness_issues=readiness_issues,
        readiness_summary=summary,
        domain_evaluation=domain_evaluation,
        domain_evaluation_issues=domain_issues,
    )
    return asdict(readiness_map)


def build_project_decision_readiness(project: dict[str, Any]) -> dict[str, Any]:
    """Build readiness for the latest or first project question without mutating project state."""
    question = _project_question(project)
    context = " ".join([str(project.get("name", "")), str(project.get("description", ""))]).strip()
    return build_decision_readiness_map(
        decision_question=question.get("question", "") if question else "",
        decision_context=context,
        evidence_items=project.get("evidence_library", []),
    )


def _map_framework(
    framework: DecisionFramework,
    evidence: list[dict[str, Any]],
    intelligence: dict[str, Any],
) -> FrameworkEvidenceMap:
    evidence_coverage = FrameworkDimensionCoverage(
        framework_id=framework.framework_id,
        required_evidence_categories=[
            _map_evidence_category(category, evidence) for category in framework.required_evidence_categories
        ],
        pathway_dimensions=[
            _map_keyword_dimension(dimension, evidence, "pathway dimension") for dimension in framework.pathway_dimensions
        ],
    )
    risk_coverage = FrameworkRiskCoverage(
        framework_id=framework.framework_id,
        risks=[
            _map_signal_category(category, intelligence.get("decision_risk_evidence_map", []), "risk_category")
            for category in framework.required_risk_categories
        ],
    )
    constraint_coverage = FrameworkConstraintCoverage(
        framework_id=framework.framework_id,
        constraints=[
            _map_signal_category(category, intelligence.get("regulatory_constraint_flags", []), "constraint_category")
            for category in framework.required_constraints
        ],
    )
    historical_support = HistoricalSupportMap(
        framework_id=framework.framework_id,
        historical_dimensions=[
            _map_historical_dimension(dimension, intelligence.get("historical_pathway_signals", []))
            for dimension in framework.historical_dimensions
        ],
    )
    return FrameworkEvidenceMap(
        framework_id=framework.framework_id,
        framework_name=framework.name,
        evidence_coverage=evidence_coverage,
        risk_coverage=risk_coverage,
        constraint_coverage=constraint_coverage,
        historical_support=historical_support,
        reviewer_questions=[
            ReviewerQuestion(
                question=question,
                source="framework",
                related_framework_id=framework.framework_id,
            )
            for question in framework.reviewer_questions
        ],
    )


def _map_evidence_category(category: str, evidence: list[dict[str, Any]]) -> MappedEvidenceItem:
    refs = [evidence_reference(item) for item in evidence if source_category(item) == category]
    if len(refs) >= 2:
        bucket = COVERED
    elif len(refs) == 1:
        bucket = PARTIALLY_COVERED
    else:
        bucket = MISSING
    return MappedEvidenceItem(
        dimension=category,
        coverage_bucket=bucket,
        evidence_refs=refs,
        reviewer_note=f"Evidence category {category} is {bucket.replace('_', ' ')}.",
    )


def _map_keyword_dimension(dimension: str, evidence: list[dict[str, Any]], label: str) -> MappedEvidenceItem:
    terms = _dimension_terms(dimension)
    matched = [item for item in evidence if _matches_any(_combined_text(item), terms)]
    refs = [evidence_reference(item) for item in matched]
    return MappedEvidenceItem(
        dimension=dimension,
        coverage_bucket=COVERED if refs else MISSING,
        evidence_refs=refs,
        matched_terms=terms if refs else [],
        reviewer_note=f"{label.title()} '{dimension}' has {'evidence support' if refs else 'no direct evidence support'}.",
    )


def _map_signal_category(category: str, signals: list[dict[str, Any]], key: str) -> MappedEvidenceItem:
    matched = [signal for signal in signals if signal.get(key) == category]
    refs = _refs_from_signals(matched)
    return MappedEvidenceItem(
        dimension=category,
        coverage_bucket=COVERED if refs else MISSING,
        evidence_refs=refs,
        matched_terms=sorted({term for signal in matched for term in signal.get("matched_terms", []) + signal.get("triggering_terms", [])}),
        reviewer_note=f"{category.replace('_', ' ')} is {'mapped to evidence' if refs else 'not mapped to current evidence'}.",
    )


def _map_historical_dimension(dimension: str, pathway_signals: list[dict[str, Any]]) -> MappedEvidenceItem:
    terms = _dimension_terms(dimension)
    matched = [
        signal
        for signal in pathway_signals
        if _matches_any(signal.get("pathway_family", "").replace("_", " "), terms)
        or _matches_any(" ".join(signal.get("triggering_terms", [])), terms)
    ]
    refs = _refs_from_signals(matched)
    return MappedEvidenceItem(
        dimension=dimension,
        coverage_bucket=COVERED if refs else MISSING,
        evidence_refs=refs,
        matched_terms=sorted({term for signal in matched for term in signal.get("triggering_terms", [])}),
        reviewer_note=f"Historical dimension '{dimension}' has {'supporting evidence signals' if refs else 'a support gap'}.",
    )


def _classification_metadata(evidence: list[dict[str, Any]], intelligence: dict[str, Any]) -> list[dict[str, Any]]:
    metadata = []
    for item in evidence:
        metadata.append(
            {
                "title": item.get("title", ""),
                "source_type": source_category(item),
                "source_name": item.get("source_name", ""),
                "source_url": item.get("source_url", ""),
                "evidence_categories": [source_category(item)],
            }
        )
    for signal in intelligence.get("decision_risk_evidence_map", []):
        metadata.append({"risk_category": signal.get("risk_category"), "risk_categories": [signal.get("risk_category")]})
    for flag in intelligence.get("regulatory_constraint_flags", []):
        metadata.append({"constraint_category": flag.get("constraint_category"), "regulatory_constraints": [flag.get("constraint_category")]})
    return metadata


def _evidence_gap_issues(framework_maps: list[FrameworkEvidenceMap]) -> list[DecisionReadinessIssue]:
    issues = []
    for framework_map in framework_maps:
        missing = [
            item
            for item in framework_map.evidence_coverage.required_evidence_categories
            if item.coverage_bucket == MISSING
        ]
        for item in missing:
            issues.append(
                DecisionReadinessIssue(
                    issue_type="evidence_gap",
                    severity="medium",
                    explanation=f"Evidence gap: {framework_map.framework_name} lacks {item.dimension} evidence.",
                    reviewer_question=f"Which evidence supports the {item.dimension.replace('_', ' ')} requirement?",
                )
            )
    return issues


def _regulatory_uncertainty_issues(
    framework_maps: list[FrameworkEvidenceMap], primary_framework_id: str
) -> list[DecisionReadinessIssue]:
    issues = []
    for framework_map in framework_maps:
        if framework_map.framework_id != primary_framework_id:
            continue
        missing_constraints = [
            item for item in framework_map.constraint_coverage.constraints if item.coverage_bucket == MISSING
        ]
        if missing_constraints and any(
            marker in framework_map.framework_id for marker in ["regulatory", "export_control", "market_entry", "technology"]
        ):
            issues.append(
                DecisionReadinessIssue(
                    issue_type="regulatory_uncertainty",
                    severity="high",
                    explanation=f"Potential constraint exposure: {framework_map.framework_name} has unmapped regulatory or legal constraints.",
                    reviewer_question="Has legal/compliance reviewed the relevant constraint exposure?",
                )
            )
    return issues


def _conflict_issues(intelligence: dict[str, Any]) -> list[DecisionReadinessIssue]:
    conflicts = [item for item in intelligence.get("relationships", []) if item.get("relationship") == "potential_conflict"]
    return [
        DecisionReadinessIssue(
            issue_type="unresolved_conflict",
            severity="high",
            explanation="Potential conflicts should be reviewed before generating pathways.",
            evidence_refs=item.get("evidence_refs", []),
            reviewer_question="Which conflicting evidence should be verified or reconciled?",
        )
        for item in conflicts
    ]


def _freshness_issues(intelligence: dict[str, Any]) -> list[DecisionReadinessIssue]:
    freshness = intelligence.get("freshness", {})
    if freshness.get("freshness_risk") not in {"High", "Moderate"}:
        return []
    refs = freshness.get("stale_evidence_refs", []) + freshness.get("missing_date_evidence_refs", [])
    return [
        DecisionReadinessIssue(
            issue_type="stale_or_undated_evidence",
            severity="medium",
            explanation="Evidence is stale or missing dates; reviewer should verify timing before pathway analysis.",
            evidence_refs=refs,
            reviewer_question="Which evidence needs updated source timing or date verification?",
        )
    ]


def _source_diversity_issues(intelligence: dict[str, Any]) -> list[DecisionReadinessIssue]:
    counts = intelligence.get("summary", {}).get("source_type_counts", {})
    total = sum(int(value) for value in counts.values()) if counts else 0
    if total < 2:
        return []
    top_name, top_count = max(counts.items(), key=lambda item: int(item[1]))
    if top_count / total < 0.75:
        return []
    return [
        DecisionReadinessIssue(
            issue_type="source_concentration",
            severity="medium",
            explanation=f"Source concentration risk: {top_name} accounts for most current evidence.",
            reviewer_question="Is there evidence from more than one source type?",
        )
    ]


def _domain_evaluation_issues(domain_evaluation: dict[str, Any]) -> list[DecisionReadinessIssue]:
    issues = []
    for result in domain_evaluation.get("results", []):
        for issue in result.get("issues", [])[:4]:
            if issue.get("issue_type") == "missing_evidence":
                issues.append(
                    DecisionReadinessIssue(
                        issue_type="domain_evaluation_gap",
                        severity="medium",
                        explanation=issue.get("explanation", "Domain evaluation evidence gap."),
                        evidence_refs=issue.get("evidence_refs", []),
                        reviewer_question=issue.get("reviewer_question", "Which domain evidence is needed?"),
                    )
                )
    return issues


def _over_concentration_issues(
    framework_maps: list[FrameworkEvidenceMap], source_diversity_flags: list[DecisionReadinessIssue]
) -> list[DecisionReadinessIssue]:
    issues = list(source_diversity_flags)
    for framework_map in framework_maps:
        for item in framework_map.evidence_coverage.required_evidence_categories:
            if len(item.evidence_refs) >= 3:
                issues.append(
                    DecisionReadinessIssue(
                        issue_type="over_concentrated",
                        severity="low",
                        explanation=f"{framework_map.framework_name} evidence is concentrated in {item.dimension}.",
                        evidence_refs=item.evidence_refs,
                        reviewer_question="Would another source category strengthen readiness?",
                    )
                )
    return issues


def _assumption_map(intelligence: dict[str, Any], framework_maps: list[FrameworkEvidenceMap]) -> list[AssumptionMap]:
    risks = {signal.get("risk_category"): signal for signal in intelligence.get("decision_risk_evidence_map", [])}
    constraints = {flag.get("constraint_category"): flag for flag in intelligence.get("regulatory_constraint_flags", [])}
    assumptions: list[AssumptionMap] = []
    if "market_risk" in risks:
        assumptions.append(_assumption("market_continuity", "Market conditions remain relevant to the decision context.", risks["market_risk"]))
    if "regulatory_risk" in risks or constraints:
        assumptions.append(_assumption("regulatory_stability", "Regulatory posture does not materially change before review.", risks.get("regulatory_risk") or next(iter(constraints.values()))))
    if "supply_chain_risk" in risks:
        assumptions.append(_assumption("supply_availability", "Supply availability remains sufficient for compared options.", risks["supply_chain_risk"]))
    if "financial_risk" in risks:
        assumptions.append(_assumption("financing_availability", "Financing and liquidity assumptions remain valid.", risks["financial_risk"]))
    if constraints:
        assumptions.append(_assumption("legal_clearance", "Legal or compliance review can verify constraint applicability.", next(iter(constraints.values()))))
    if "data_privacy_security_risk" in risks:
        assumptions.append(_assumption("data_security", "Data security controls are adequate for the reviewed pathway.", risks["data_privacy_security_risk"]))
    if "geopolitical_risk" in risks:
        assumptions.append(_assumption("geopolitical_stability", "Geopolitical conditions do not sharply deteriorate before action.", risks["geopolitical_risk"]))
    if not assumptions and framework_maps:
        assumptions.append(
            AssumptionMap(
                category="stakeholder_alignment",
                explanation="Reviewer assumes stakeholders can align around a pathway comparison process.",
                related_framework_dimensions=[framework_maps[0].framework_id],
                reviewer_question="Which stakeholder assumptions need validation before pathway comparison?",
            )
        )
    return assumptions


def _unknowns_map(
    framework_maps: list[FrameworkEvidenceMap],
    evidence_gaps: list[DecisionReadinessIssue],
    conflict_flags: list[DecisionReadinessIssue],
    source_diversity_flags: list[DecisionReadinessIssue],
) -> list[UnknownsMap]:
    unknowns = []
    dimensions = [issue.explanation for issue in evidence_gaps]
    if any("financial_market" in item or "company_ir" in item or "sec_filing" in item for item in dimensions):
        unknowns.append(_unknown("missing_financial_impact", "Financial impact evidence is incomplete.", "Which financial evidence is needed?"))
    if any("major_news" in item or "industry_analysis" in item for item in dimensions):
        unknowns.append(_unknown("missing_market_data", "Market or industry evidence is incomplete.", "Which evidence supports the market impact assumption?"))
    if any("regulator" in item or "legal_regulatory" in item or "official_government" in item for item in dimensions):
        unknowns.append(_unknown("missing_regulatory_status", "Regulatory status evidence is incomplete.", "Has legal/compliance reviewed the regulatory status?"))
    if any(_has_missing_constraints(framework_map) for framework_map in framework_maps):
        unknowns.append(_unknown("missing_legal_review", "Constraint mapping is incomplete.", "Which legal or compliance checks remain open?"))
    if any("supply" in framework_map.framework_id for framework_map in framework_maps):
        unknowns.append(_unknown("missing_supplier_data", "Supplier evidence may be incomplete.", "Which supplier evidence is required?"))
    if any(_has_missing_history(framework_map) for framework_map in framework_maps):
        unknowns.append(_unknown("missing_historical_outcome", "Historical support is incomplete.", "Which historical analogue best matches the current context?"))
    if source_diversity_flags:
        unknowns.append(_unknown("missing_source_diversity", "Source diversity is limited.", "Is there evidence from more than one source type?"))
    if conflict_flags:
        unknowns.append(_unknown("unresolved_conflict", "Potential conflicting evidence remains unresolved.", "What evidence would reconcile the conflict?"))
    if not unknowns:
        unknowns.append(_unknown("missing_timeline", "Decision timing may still require reviewer validation.", "What timeline would invalidate the base-case pathway?"))
    return unknowns


def _reviewer_questions(
    frameworks: list[DecisionFramework],
    framework_maps: list[FrameworkEvidenceMap],
    readiness_issues: list[DecisionReadinessIssue],
    assumptions: list[AssumptionMap],
    unknowns: list[UnknownsMap],
) -> list[ReviewerQuestion]:
    questions: list[ReviewerQuestion] = []
    for framework in frameworks:
        questions.extend(
            ReviewerQuestion(question=question, source="framework", related_framework_id=framework.framework_id)
            for question in framework.reviewer_questions
        )
    questions.extend(
        ReviewerQuestion(
            question=issue.reviewer_question,
            source=issue.issue_type,
            evidence_refs=issue.evidence_refs,
        )
        for issue in readiness_issues
        if issue.reviewer_question
    )
    questions.extend(
        ReviewerQuestion(question=item.reviewer_question, source="assumption", evidence_refs=item.evidence_refs)
        for item in assumptions
        if item.reviewer_question
    )
    questions.extend(
        ReviewerQuestion(question=item.reviewer_question, source="unknown", evidence_refs=item.evidence_refs)
        for item in unknowns
        if item.reviewer_question
    )
    return _dedupe_questions(questions)[:18]


def _readiness_summary(
    *,
    evidence_count: int,
    framework_count: int,
    readiness_issues: list[DecisionReadinessIssue],
    framework_maps: list[FrameworkEvidenceMap],
    has_question: bool,
) -> DecisionReadinessSummary:
    if not has_question or evidence_count == 0 or framework_count == 0:
        state = "not_ready_insufficient_evidence"
        text = "Decision is not ready for pathway analysis because the question or evidence set is incomplete."
    elif any(issue.issue_type == "unresolved_conflict" for issue in readiness_issues):
        state = "blocked_by_conflicts"
        text = "Potential conflicts should be reviewed before generating pathways."
    elif any(issue.issue_type == "regulatory_uncertainty" for issue in readiness_issues):
        state = "blocked_by_regulatory_uncertainty"
        text = "Evidence is partially mapped, but regulatory constraints require review."
    elif any(issue.issue_type in {"source_concentration", "stale_or_undated_evidence"} for issue in readiness_issues):
        state = "stale_or_low_diversity_evidence"
        text = "Evidence is stale or source-concentrated; reviewer should add or verify evidence."
    elif _has_required_gaps(framework_maps[:1]):
        state = "partially_ready"
        text = "Evidence is partially ready; key framework dimensions still lack support."
    else:
        state = "ready_for_pathway_analysis"
        text = "Evidence is sufficient to begin pathway comparison, subject to reviewer verification."
    return DecisionReadinessSummary(
        readiness_state=state,
        reviewer_summary=text,
        evidence_count=evidence_count,
        framework_count=framework_count,
        issue_count=len(readiness_issues),
    )


def _project_question(project: dict[str, Any]) -> dict[str, Any]:
    return latest_or_first_project_question(project)


def _framework_summary(framework: DecisionFramework) -> dict[str, str]:
    return {"framework_id": framework.framework_id, "name": framework.name, "description": framework.description}


def _assumption(category: str, explanation: str, signal: dict[str, Any]) -> AssumptionMap:
    return AssumptionMap(
        category=category,
        explanation=explanation,
        evidence_refs=signal.get("evidence_refs", []),
        related_framework_dimensions=[category],
        reviewer_question=f"Which evidence supports the {category.replace('_', ' ')} assumption?",
    )


def _unknown(category: str, explanation: str, question: str) -> UnknownsMap:
    return UnknownsMap(category=category, explanation=explanation, reviewer_question=question)


def _refs_from_signals(signals: list[dict[str, Any]]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    seen: set[str] = set()
    for signal in signals:
        for ref in signal.get("evidence_refs", []):
            evidence_id = str(ref.get("evidence_id", ""))
            if evidence_id and evidence_id not in seen:
                seen.add(evidence_id)
                refs.append(ref)
    return refs


def _dimension_terms(dimension: str) -> list[str]:
    return [term for term in dimension.replace("/", " ").replace("-", " ").split() if len(term) > 2]


def _matches_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def _combined_text(item: dict[str, Any]) -> str:
    return " ".join(str(item.get(key, "")) for key in ("title", "summary", "excerpt", "text_excerpt", "source_type"))


def _has_required_gaps(framework_maps: list[FrameworkEvidenceMap]) -> bool:
    for framework_map in framework_maps:
        if any(item.coverage_bucket == MISSING for item in framework_map.evidence_coverage.required_evidence_categories):
            return True
        if any(item.coverage_bucket == MISSING for item in framework_map.risk_coverage.risks):
            return True
    return False


def _has_missing_constraints(framework_map: FrameworkEvidenceMap) -> bool:
    return any(item.coverage_bucket == MISSING for item in framework_map.constraint_coverage.constraints)


def _has_missing_history(framework_map: FrameworkEvidenceMap) -> bool:
    return any(item.coverage_bucket == MISSING for item in framework_map.historical_support.historical_dimensions)


def _dedupe_questions(questions: list[ReviewerQuestion]) -> list[ReviewerQuestion]:
    seen: set[str] = set()
    output = []
    for question in questions:
        if question.question not in seen:
            seen.add(question.question)
            output.append(question)
    return output
