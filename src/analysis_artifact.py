"""Analysis artifact construction for persisted run outputs."""

from __future__ import annotations

from typing import Any

from serialization import serializable


def build_analysis_artifact(**items: Any) -> dict[str, Any]:
    """Build the JSON analysis artifact persisted for each run."""
    issues = items["issues"]
    classifications = items["classifications"]
    route = items["route"]
    issue_title = issues[0].title if issues else "Untitled issue"
    return {
        "issue": serializable(issues[0]) if issues else {},
        "source_url": items["source_url"],
        "input_mode": items["input_mode"],
        "uploaded_filename": items["uploaded_filename"],
        "file_type": items["file_type"],
        "event_context": serializable(items["event_context"]),
        "event_understanding": serializable(items["event_understanding"]),
        "question_route": serializable(items["localized_question_route"]),
        "scenario": serializable(classifications[0]) if classifications else {},
        "mechanisms": serializable(items["mechanisms"].get(issue_title, [])),
        "analogues": serializable(items["analogues"].get(issue_title, [])),
        "historical_outcomes": serializable(items["historical_outcomes"].get(issue_title, [])),
        "strategic_lessons": serializable(items["strategic_lessons"].get(issue_title, [])),
        "strategic_assessment": serializable(items["strategic_assessments"].get(issue_title, {})),
        "evidence_credibility": serializable(items["evidence_credibility"].get(issue_title, {})),
        "current_context": serializable(items["contexts"].get(issue_title, [])),
        "implications": serializable(items["analyses"]),
        "response_playbooks": serializable(items["response_patterns"].get(issue_title, [])),
        "lenses": serializable(items["interpretations"].get(issue_title, [])),
        "evidence": serializable(items["evidence_assessments"].get(issue_title, [])),
        "decision_assessment": serializable(items.get("decision_assessment", {})),
        "decision_readiness": serializable(items.get("decision_readiness", {})),
        "decision_pathways": serializable(items.get("decision_pathways", {})),
        "pathway_comparison": serializable(items.get("pathway_comparison", {})),
        "evidence_ledger": serializable(items.get("evidence_ledger", {})),
        "evidence_bundle": serializable(items.get("evidence_bundle", [])),
        "evidence_sufficiency": serializable(items.get("evidence_sufficiency", {})),
        "artifact_completeness": serializable(items.get("artifact_completeness", {})),
        "tool_routing_trace": {
            "document_type": route.document_type,
            "scenario_type": route.scenario_type,
            "selected_tools": route.selected_tools,
            "skipped_tools": route.skipped_tools,
            "trace": serializable(route.trace),
            "reasoning_record": serializable(route.reasoning_record),
            "reasoning_stages": [
                "Current event context extraction",
                "Event-family understanding",
                "Historical analogue retrieval",
                "Historical outcome retrieval",
                "Strategic assessment generation",
                "Strategic lesson generation",
                "Evidence credibility assessment",
                "Response playbook retrieval",
                "Executive brief generation",
            ],
        },
        "evaluation_metadata": {
            "framework": "V5 deterministic regression and contract validation framework",
            "note": "Completeness is internal contract validation, not decision quality or real-world accuracy.",
        },
        "metadata": items["metadata"],
    }
