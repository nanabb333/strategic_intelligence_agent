from types import SimpleNamespace

from confidence_layer import assess_confidence, render_evidence_confidence_section
from decision_case import build_decision_case
from evidence_ledger import build_evidence_ledger
from serialization import serializable


def test_decision_case_schema_creation_uses_simple_fields() -> None:
    issue = SimpleNamespace(
        title="Export controls affect chips",
        summary="New controls affect advanced chip supply chains.",
        core_issue="Management needs to assess customer and supply exposure.",
        actors=["management", "suppliers"],
        companies=[],
        countries_or_regions=["United States"],
        industries=["semiconductors"],
    )
    classification = SimpleNamespace(primary_scenario="Export Controls")

    decision_case = build_decision_case(
        issue=issue,
        classification=classification,
        analogues=[],
        mechanisms=[],
        strategic_assessment=None,
        evidence_ids=["E1"],
        question_text="What should determine this decision?",
    )

    assert decision_case.decision_question == "What should determine this decision?"
    assert decision_case.evidence_items == ["E1"]
    assert "Evidence quality" in decision_case.decision_criteria
    assert decision_case.recommended_path.startswith("Option B")
    assert decision_case.limitations


def test_evidence_ledger_creation_and_serialization() -> None:
    issue = SimpleNamespace(
        summary="New controls affect advanced chip supply chains.",
        core_issue="Management needs to assess customer and supply exposure.",
    )
    analogue = SimpleNamespace(
        case_title="Prior export control case",
        year="2022",
        similarity_reason="Shares export-control pressure.",
        business_relevance="Exposure mapping was needed.",
        caution_note="Sector and rule details may differ.",
    )

    ledger = build_evidence_ledger(
        issue=issue,
        source_url="",
        analogues=[analogue],
        mechanisms=[],
        evidence_assessments=[],
        historical_outcomes=[],
        contexts=[],
    )
    payload = serializable(ledger)

    assert ledger.ids() == ["E1", "E2"]
    assert payload["items"][0]["observation"] == "Management needs to assess customer and supply exposure."
    assert payload["items"][1]["inference"].endswith("does not determine the current outcome.")


def test_confidence_layer_limits_high_confidence_when_evidence_is_limited() -> None:
    decision_case = build_decision_case(
        issue=None,
        classification=None,
        analogues=[],
        mechanisms=[],
        strategic_assessment=None,
        evidence_ids=["E1"],
        question_text="What should happen next?",
    )
    ledger = build_evidence_ledger(
        issue=None,
        source_url="",
        analogues=[],
        mechanisms=[],
        evidence_assessments=[],
        historical_outcomes=[],
        contexts=[],
    )

    assessment = assess_confidence(decision_case, ledger)
    section = render_evidence_confidence_section(evidence_ledger=ledger, confidence_assessment=assessment)

    assert assessment.confidence_level == "Low"
    assert "## Evidence and Confidence" in section
    assert "### What Is Unknown Or Uncertain" in section
