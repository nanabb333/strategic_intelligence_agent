from dataclasses import dataclass
from types import SimpleNamespace

from analysis_artifact import build_analysis_artifact


@dataclass
class Issue:
    title: str
    summary: str


@dataclass
class Classification:
    issue_title: str
    primary_scenario: str


def test_build_analysis_artifact_preserves_top_level_shape() -> None:
    issue = Issue("Test issue", "Summary")
    classification = Classification("Test issue", "Export Controls")
    route = SimpleNamespace(
        document_type="Policy",
        scenario_type="Export Controls",
        selected_tools=["IssueExtractor"],
        skipped_tools=[],
        trace=[],
        reasoning_record=[],
    )

    artifact = build_analysis_artifact(
        issues=[issue],
        classifications=[classification],
        analogues={"Test issue": []},
        contexts={"Test issue": []},
        analyses=[],
        mechanisms={"Test issue": []},
        interpretations={"Test issue": []},
        evidence_assessments={"Test issue": []},
        historical_outcomes={"Test issue": []},
        strategic_lessons={"Test issue": []},
        strategic_assessments={"Test issue": {}},
        evidence_credibility={"Test issue": {}},
        response_patterns={"Test issue": []},
        event_context=None,
        event_understanding=None,
        question_route=None,
        localized_question_route={"intent": "Decision Support"},
        source_url="",
        input_mode="paste_text",
        uploaded_filename="",
        file_type="text",
        route=route,
        metadata={"run_id": "run_1"},
    )

    assert artifact["issue"] == {"title": "Test issue", "summary": "Summary"}
    assert artifact["scenario"] == {"issue_title": "Test issue", "primary_scenario": "Export Controls"}
    assert artifact["agent_trace"]["document_type"] == "Policy"
    assert artifact["evaluation_metadata"]["framework"] == "V5 deterministic benchmark framework"
    assert artifact["metadata"] == {"run_id": "run_1"}
