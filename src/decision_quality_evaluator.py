"""Deterministic decision quality evaluation for generated briefs."""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean

from confidence_layer import ConfidenceAssessment
from decision_case import DecisionCase
from evidence_ledger import EvidenceLedger


@dataclass
class DimensionEvaluation:
    """Evaluation result for one decision-quality dimension."""

    score: float
    label: str
    rationale: str


@dataclass
class DecisionQualityEvaluation:
    """Deterministic product-quality evaluation for one generated analysis."""

    direct_answer_quality: DimensionEvaluation
    historical_analogue_relevance: DimensionEvaluation
    evidence_use: DimensionEvaluation
    option_clarity: DimensionEvaluation
    risk_identification: DimensionEvaluation
    change_trigger_quality: DimensionEvaluation
    localization_quality: DimensionEvaluation
    overconfidence_control: DimensionEvaluation
    overall_score: float
    overall_label: str
    notes: list[str] = field(default_factory=list)


DIMENSION_LABELS = {
    "direct_answer_quality": "Direct answer quality",
    "historical_analogue_relevance": "Historical analogue relevance",
    "evidence_use": "Evidence use",
    "option_clarity": "Option clarity",
    "risk_identification": "Risk identification",
    "change_trigger_quality": "Change trigger quality",
    "localization_quality": "Localization quality",
    "overconfidence_control": "Overconfidence control",
}


def evaluate_decision_quality(
    *,
    decision_case: DecisionCase,
    evidence_ledger: EvidenceLedger,
    confidence_assessment: ConfidenceAssessment,
    brief_markdown: str,
    language: str,
) -> DecisionQualityEvaluation:
    """Evaluate decision-support output quality with deterministic rubric checks."""
    dimensions = {
        "direct_answer_quality": _direct_answer_quality(decision_case),
        "historical_analogue_relevance": _historical_analogue_relevance(decision_case, evidence_ledger),
        "evidence_use": _evidence_use(evidence_ledger, confidence_assessment),
        "option_clarity": _option_clarity(decision_case),
        "risk_identification": _risk_identification(decision_case, confidence_assessment),
        "change_trigger_quality": _change_trigger_quality(decision_case, confidence_assessment),
        "localization_quality": _localization_quality(brief_markdown, language),
        "overconfidence_control": _overconfidence_control(brief_markdown, decision_case, confidence_assessment),
    }
    overall_score = round(mean(item.score for item in dimensions.values()), 3)
    return DecisionQualityEvaluation(
        **dimensions,
        overall_score=overall_score,
        overall_label=_label(overall_score),
        notes=[
            "Deterministic product-quality evaluation only.",
            "Scores are internal review aids, not real-world accuracy claims.",
            "No LLM evaluator, network access, or external benchmark is used.",
        ],
    )


def render_decision_quality_review(evaluation: DecisionQualityEvaluation) -> str:
    """Render existing decision-quality evaluation as a concise brief section."""
    dimensions = [
        ("direct_answer_quality", evaluation.direct_answer_quality),
        ("historical_analogue_relevance", evaluation.historical_analogue_relevance),
        ("evidence_use", evaluation.evidence_use),
        ("option_clarity", evaluation.option_clarity),
        ("risk_identification", evaluation.risk_identification),
        ("change_trigger_quality", evaluation.change_trigger_quality),
        ("localization_quality", evaluation.localization_quality),
        ("overconfidence_control", evaluation.overconfidence_control),
    ]
    lines = [
        "## Decision Quality Review",
        "",
        f"**Overall label:** {evaluation.overall_label}",
        f"**Overall score:** {_display_score(evaluation.overall_score)}",
        "",
        "This is a deterministic product-quality check. It is not a benchmark result, factual verification, or claim of real-world accuracy.",
        "",
    ]
    for key, dimension in dimensions:
        label = DIMENSION_LABELS[key]
        lines.extend(
            [
        f"### {label}",
        "",
        f"- **Score:** {_display_score(dimension.score)}",
        f"- **Assessment:** {dimension.label}",
        f"- **Rationale:** {dimension.rationale}",
        "",
            ]
        )
    if evaluation.notes:
        lines.extend(["### Notes", ""])
        lines.extend(f"- {note}" for note in evaluation.notes)
        lines.append("")
    return "\n".join(lines).strip()


def _direct_answer_quality(decision_case: DecisionCase) -> DimensionEvaluation:
    checks = [
        bool(decision_case.decision_question.strip()),
        bool(decision_case.situation.strip()),
        bool(decision_case.recommended_path.strip()),
        len(decision_case.decision_criteria) >= 3,
    ]
    score = _score(checks)
    return _result(
        score,
        "Checks whether the output frames a decision question, situation, recommendation, and criteria.",
    )


def _historical_analogue_relevance(decision_case: DecisionCase, evidence_ledger: EvidenceLedger) -> DimensionEvaluation:
    historical_items = [
        item for item in evidence_ledger.items if "historical" in item.source_type.lower() or "analogue" in item.claim_supported.lower()
    ]
    has_transferability_limit = any(
        "not prediction" in item.limitations.lower()
        or "not determine" in item.inference.lower()
        or "similarity supports comparison" in item.limitations.lower()
        for item in historical_items
    )
    checks = [
        bool(decision_case.historical_analogues),
        bool(historical_items),
        has_transferability_limit,
    ]
    score = _score(checks)
    return _result(
        score,
        "Checks whether analogues exist, appear in the evidence ledger, and include transferability limits.",
    )


def _evidence_use(
    evidence_ledger: EvidenceLedger,
    confidence_assessment: ConfidenceAssessment,
) -> DimensionEvaluation:
    items = evidence_ledger.items
    reviewable_items = [
        item
        for item in items
        if item.observation.strip() and item.inference.strip() and item.claim_supported.strip() and item.limitations.strip()
    ]
    checks = [
        len(items) >= 2,
        len(reviewable_items) == len(items) and bool(items),
        bool(confidence_assessment.limitations),
        bool(confidence_assessment.unknown_or_uncertain),
    ]
    score = _score(checks)
    return _result(
        score,
        "Checks whether evidence items are reviewable and uncertainty remains visible.",
    )


def _option_clarity(decision_case: DecisionCase) -> DimensionEvaluation:
    unique_options = {item.strip() for item in decision_case.decision_options if item.strip()}
    checks = [
        len(unique_options) >= 2,
        any("Option A" in item for item in unique_options),
        any("Option B" in item for item in unique_options),
        bool(decision_case.recommended_path.strip()),
    ]
    score = _score(checks)
    return _result(
        score,
        "Checks whether options are distinct and a preferred path is identified.",
    )


def _risk_identification(
    decision_case: DecisionCase,
    confidence_assessment: ConfidenceAssessment,
) -> DimensionEvaluation:
    checks = [
        len(decision_case.risks) >= 2,
        bool(decision_case.limitations),
        bool(confidence_assessment.unknown_or_uncertain),
    ]
    score = _score(checks)
    return _result(
        score,
        "Checks whether risks, limitations, and unknowns are explicit.",
    )


def _change_trigger_quality(
    decision_case: DecisionCase,
    confidence_assessment: ConfidenceAssessment,
) -> DimensionEvaluation:
    triggers = decision_case.change_triggers or confidence_assessment.what_would_change_this_view
    checks = [
        len(triggers) >= 2,
        len(decision_case.monitoring_signals) >= 2,
        any("evidence" in item.lower() or "source" in item.lower() for item in triggers),
    ]
    score = _score(checks)
    return _result(
        score,
        "Checks whether the recommendation includes observable change triggers and monitoring signals.",
    )


def _localization_quality(brief_markdown: str, language: str) -> DimensionEvaluation:
    if language == "en":
        return _result(1.0, "English is the official product language; localization transformation is not active.")
    return _result(
        0.0,
        "Unsupported language requested for an English-only product release.",
    )


def _overconfidence_control(
    brief_markdown: str,
    decision_case: DecisionCase,
    confidence_assessment: ConfidenceAssessment,
) -> DimensionEvaluation:
    lowered = brief_markdown.lower()
    prohibited_phrases = [
        "guarantees",
        "guaranteed",
        "will definitely",
        "proves the future",
        "statistical probability",
        "investment advice",
        "trading recommendation",
    ]
    uses_qualitative_confidence = confidence_assessment.confidence_level in {"Low", "Moderate", "High"}
    high_confidence_with_limits = confidence_assessment.confidence_level == "High" and (
        decision_case.limitations or confidence_assessment.unknown_or_uncertain
    )
    checks = [
        not any(phrase in lowered for phrase in prohibited_phrases),
        uses_qualitative_confidence,
        not high_confidence_with_limits,
        bool(confidence_assessment.limitations),
    ]
    score = _score(checks)
    return _result(
        score,
        "Checks for qualitative confidence, visible limitations, and absence of overconfident phrases.",
    )


def _score(checks: list[bool]) -> float:
    if not checks:
        return 0.0
    return round(sum(1 for item in checks if item) / len(checks), 3)


def _result(score: float, rationale: str) -> DimensionEvaluation:
    return DimensionEvaluation(score=score, label=_label(score), rationale=rationale)


def _display_score(score: float) -> str:
    """Convert internal 0–1 score into a user-facing 10-point scale."""
    return f"{score * 10:.1f} / 10"


def _label(score: float) -> str:
    if score >= 0.85:
        return "Strong"
    if score >= 0.6:
        return "Adequate"
    if score >= 0.3:
        return "Needs Review"
    return "Weak"
