from confidence_layer import ConfidenceAssessment
from decision_case import DecisionCase
from decision_quality_evaluator import evaluate_decision_quality, render_decision_quality_review
from evidence_ledger import EvidenceItem, EvidenceLedger


def test_decision_quality_evaluator_returns_all_dimensions() -> None:
    decision_case = DecisionCase(
        decision_question="What should management do?",
        source_summary="Export controls affect chip supply chains.",
        situation="Management needs to assess supply and customer exposure.",
        stakeholders=["management", "suppliers"],
        decision_criteria=["Evidence quality", "Exposure", "Reversibility"],
        decision_options=[
            "Option A: wait for more information.",
            "Option B: map exposure and prepare staged response.",
            "Option C: move immediately to a defensive posture.",
        ],
        evidence_items=["E1", "E2"],
        historical_analogues=["Prior export control case (2022)"],
        assumptions=["Human review will verify source details."],
        risks=["Historical similarity may not transfer cleanly.", "New evidence may change the preferred path."],
        recommended_path="Option B: map exposure and prepare staged response.",
        confidence_level="Moderate",
        change_triggers=["New evidence changes the factual basis.", "Implementation details change constraints."],
        monitoring_signals=["Source updates", "Stakeholder responses"],
        limitations=["Available evidence is limited to supplied material."],
    )
    ledger = EvidenceLedger(
        items=[
            EvidenceItem(
                evidence_id="E1",
                source_type="User-provided input material",
                evidence_text="Export controls affect chip supply chains.",
                observation="Controls affect supply chains.",
                inference="The issue is relevant for exposure mapping.",
                claim_supported="Situation understanding.",
                relevance="High",
                confidence="Moderate",
                limitations="Source detail is limited.",
                used_in_section="Decision Snapshot",
            ),
            EvidenceItem(
                evidence_id="E2",
                source_type="Local historical analogue record",
                evidence_text="Prior export control case.",
                observation="A similar case was retrieved.",
                inference="Historical comparison does not determine the current outcome.",
                claim_supported="Historical comparison.",
                relevance="Moderate",
                confidence="Moderate",
                limitations="Historical similarity supports comparison, not prediction.",
                used_in_section="Historical Evidence",
            ),
        ]
    )
    confidence = ConfidenceAssessment(
        confidence_level="Moderate",
        key_assumptions=decision_case.assumptions,
        what_would_change_this_view=decision_case.change_triggers,
        unknown_or_uncertain=["Organization-specific exposure requires review."],
        limitations=decision_case.limitations,
        rationale="Moderate confidence because reviewable evidence exists.",
    )

    result = evaluate_decision_quality(
        decision_case=decision_case,
        evidence_ledger=ledger,
        confidence_assessment=confidence,
        brief_markdown="## Evidence and Confidence\nDecision-support only. No forecasts.",
        language="en",
    )

    dimensions = [
        result.direct_answer_quality,
        result.historical_analogue_relevance,
        result.evidence_use,
        result.option_clarity,
        result.risk_identification,
        result.change_trigger_quality,
        result.localization_quality,
        result.overconfidence_control,
    ]
    assert all(0.0 <= dimension.score <= 1.0 for dimension in dimensions)
    assert result.overall_label in {"Strong", "Adequate", "Needs Review", "Weak"}
    assert result.evidence_use.label == "Strong"
    assert "not real-world accuracy claims" in result.notes[1]

    rendered = render_decision_quality_review(result)
    assert "**Overall score:** 10.0 / 10" in rendered
    assert "- **Score:** 10.0 / 10" in rendered
