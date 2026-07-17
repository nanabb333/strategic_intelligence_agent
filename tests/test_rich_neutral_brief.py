from fastapi.testclient import TestClient

from app import app
from helpers import ANALYZE_PAYLOAD
from neutral_brief_renderer import render_rich_neutral_assessment


FORBIDDEN_CURRENT_CONTRACT_TEXT = [
    "Option B (Recommended)",
    "Preferred Path",
    "Recommended Path",
    "currently ranks first",
    "recommended_path",
    "automatic selection",
    "system final judgment",
]


def rich_analysis_fixture() -> dict:
    return {
        "issue": {
            "actors": ["Manufacturer", "Regulator"],
            "countries_or_regions": ["United States", "China"],
            "industries": ["Semiconductors"],
            "policy_terms": ["export controls"],
            "companies": ["Example Foundry"],
        },
        "event_context": {
            "event_type": "Export Controls",
            "event_summary": "Licensing rules may affect advanced-chip shipments.",
            "primary_actor": "Government regulators",
            "secondary_actor": "Manufacturers",
            "affected_sectors": ["Semiconductors"],
            "affected_regions": ["United States", "China"],
            "policy_domain": "Technology and national security",
            "strategic_significance": "Shipment eligibility and supplier exposure require review.",
            "context_limitations": ["The submitted source has not been independently verified."],
        },
        "scenario": {
            "primary_scenario": "Export Controls",
            "matched_keywords": ["export control", "license"],
            "confidence_label": "Medium",
        },
        "current_context": [
            {
                "industry": "Semiconductors",
                "scenario_type": "Export Controls",
                "context_summary": "Licensing can alter access to production inputs.",
                "why_it_matters": "Review timelines can affect customer commitments.",
                "stakeholders": "Compliance; operations; customers",
                "monitoring_considerations": "Monitor licensing guidance and end-user rules.",
                "similarity_reason": "Scenario and industry match.",
                "evidence_trace": "Curated semiconductor context record.",
            }
        ],
        "evidence_ledger": {
            "items": [
                {
                    "evidence_id": "E1",
                    "source_type": "User-provided source",
                    "observation": "The rule names advanced-chip shipment restrictions.",
                    "inference": "Shipment eligibility requires reviewer verification.",
                    "claim_supported": "A licensing review is relevant.",
                    "evidence_text": "Advanced-chip shipments require a license.",
                    "source_status": "User provided",
                    "source_identity": "https://example.com/rule",
                    "relevance": "High",
                    "limitations": "Only one source is available.",
                }
            ]
        },
        "evidence": [
            {
                "lens": "Economics",
                "supporting_evidence": ["The source identifies an input-access constraint."],
                "weakening_evidence": ["Cost effects are not quantified."],
                "missing_evidence": ["Supplier-level exposure data is missing."],
            }
        ],
        "tool_routing_trace": {
            "document_type": "Policy update",
            "scenario_type": "Export Controls",
            "selected_tools": ["IssueExtractor", "HistoricalRetriever"],
            "skipped_tools": [],
            "trace": [{"event": "Tool selected", "detail": "HistoricalRetriever matched the scenario."}],
            "reasoning_record": [
                {
                    "tool": "HistoricalRetriever",
                    "decision": "selected",
                    "why": "Historical comparison was requested.",
                    "expected_contribution": "Retrieve comparable local cases.",
                }
            ],
        },
        "evidence_credibility": {
            "evidence_summary": "One current source and one local analogue are recorded.",
            "source_status_distribution": {"source provided": 1, "source pending": 1},
            "reviewer_note": "Verify the primary rule before operational use.",
            "key_limitations": ["The historical record has no primary source link."],
        },
        "mechanisms": [
            {
                "mechanism_name": "Technology Access Restriction",
                "description": "Licensing limits access to sensitive technology.",
                "detection_reason": "Export-control terms matched.",
                "possible_observations": "License delays and restricted end users.",
                "evidence_references": ["Source Document"],
            }
        ],
        "analogues": [
            {
                "case_title": "Historical Chip-Control Case",
                "year": 2023,
                "scenario_type": "Export Controls",
                "similarity_reason": "Both cases involve equipment licensing.",
                "business_relevance": "Supplier access required review.",
                "geopolitical_relevance": "Cross-border rules affected operations.",
                "caution_note": "The actors and legal rules differ.",
                "source_title": "Historical record",
                "source_url": "source pending",
                "evidence_trace": "Local analogue record",
            }
        ],
        "historical_outcomes": [
            {
                "case_name": "Historical Chip-Control Case",
                "year": 2023,
                "event_family": "Trade Restriction",
                "observed_outcome": "Firms expanded license and customer screening.",
                "strategic_response": "Organizations mapped exposed products.",
                "time_horizon": "Medium term",
                "source_status": "source pending",
                "retrieval_reason": "Matched the export-control frame.",
                "evidence_references": ["Local historical record"],
            }
        ],
        "implications": [
            {
                "observed_similarities": ["Both cases involve licensing constraints."],
                "observed_differences": ["The current product scope is not established."],
                "business_considerations": ["Customer commitments may require review."],
                "operational_considerations": ["Operations may need product screening."],
                "geopolitical_considerations": ["Cross-border alignment remains uncertain."],
                "strategic_questions": ["Which products are exposed to the rule?"],
            }
        ],
        "lenses": [
            {
                "lens": "Economics",
                "hypothesis": "One interpretation is that access constraints affect capacity planning.",
                "supporting_observations": ["The source names restricted chip shipments."],
                "limitations": ["The source does not quantify capacity effects."],
                "evidence_references": ["Source Document"],
            }
        ],
        "strategic_lessons": [
            {
                "lesson": "Map exposure before relying on a historical comparison.",
                "rationale": "Historical cases differ in products and legal scope.",
                "supporting_cases": ["Historical Chip-Control Case"],
            }
        ],
        "response_playbooks": [
            {
                "pattern_name": "Exposure mapping",
                "observed_historical_choices": ["Organizations reviewed product eligibility."],
                "observed_outcomes": ["Review identified affected shipments."],
                "business_lessons": ["Product-level data matters."],
                "cross_domain_lessons": ["Preserve reversibility while rules remain unclear."],
                "evidence_references": ["Historical Chip-Control Case"],
            }
        ],
        "strategic_assessment": {
            "important_limitations": ["Historical patterns do not determine the current outcome."],
            "historical_patterns": [
                {
                    "pattern": "Expanded compliance review",
                    "frequency_percent": 50,
                    "supporting_cases": ["Historical Chip-Control Case"],
                    "interpretation": "One of two local cases recorded expanded screening.",
                }
            ],
            "outcome_distribution": [
                {
                    "outcome_type": "Operational adjustment",
                    "frequency_percent": 50,
                    "case_count": 1,
                    "interpretation": "A local case recorded a workflow adjustment.",
                }
            ],
            "strategic_watchlist": ["Monitor publication of implementation guidance."],
            "role_based_monitoring": {
                "corporate_strategy_view": ["Monitor customer and product exposure."],
                "supply_chain_view": ["Monitor supplier license status."],
            },
        },
        "decision_assessment": {
            "decision_question": "How should reviewers compare shipment-plan pathways?",
            "assessment_summary": "The rule may affect shipments, but product-level exposure remains unverified.",
            "comparison_criteria": ["Evidence strength", "Reversibility"],
            "pathways_for_review": [
                {
                    "pathway_id": "path-1",
                    "title": "Maintain current plan while verifying exposure",
                    "pathway_family": "monitor_and_verify",
                    "description": "Keep the current plan under review while collecting product-level evidence.",
                    "pathway_evidence": {
                        "supporting": [
                            {
                                "evidence_id": "E1",
                                "title": "Submitted export-control notice",
                                "source_url": "https://example.com/rule",
                            }
                        ],
                        "weakening": [],
                        "gaps": [],
                    },
                    "pathway_tradeoffs": ["Preserves flexibility but may delay preparation."],
                    "risks": ["Late operational response"],
                    "reversibility": "High",
                    "timing_implications": "Requires a near-term review window.",
                    "assumptions": ["Current shipments remain eligible during review."],
                    "unknowns": ["Product-level rule coverage is unknown."],
                    "constraints": ["Primary legal guidance is incomplete."],
                    "pathway_conditions": {
                        "more_supportable_when": ["Exposure remains limited."],
                        "less_supportable_when": ["A shipment is confirmed restricted."],
                    },
                    "change_triggers": ["Confirmed restriction of a planned shipment."],
                    "reviewer_questions": ["What is the cost of waiting for clarification?"],
                    "limitations": ["This pathway is a template-guided comparison aid."],
                },
                {
                    "pathway_id": "path-2",
                    "title": "Prepare a staged shipment adjustment",
                    "pathway_family": "staged_preparation",
                    "description": "Prepare reversible operational changes while evidence is reviewed.",
                    "pathway_evidence": {"supporting": [], "weakening": [], "gaps": []},
                    "pathway_tradeoffs": ["Adds preparation cost while preserving options."],
                    "risks": ["Unnecessary preparation"],
                    "reversibility": "Medium",
                    "timing_implications": "Preparation can begin before final clarification.",
                    "assumptions": [],
                    "unknowns": ["Implementation timing is unknown."],
                    "constraints": [],
                    "pathway_conditions": {"more_supportable_when": [], "less_supportable_when": []},
                    "change_triggers": ["Regulator publishes implementation guidance."],
                    "reviewer_questions": [],
                    "limitations": ["No pathway ranking is implied."],
                },
            ],
            "strategic_considerations": ["Separate confirmed restrictions from scenario assumptions."],
            "change_triggers": ["New licensing guidance becomes available."],
            "reviewer_questions": ["Which evidence gap most affects shipment eligibility?"],
            "assumptions": ["The submitted notice is current."],
            "unknowns": ["Customer-specific eligibility is unknown."],
            "constraints": ["No verified product classification is available."],
            "limitations": ["The system does not validate legal applicability."],
            "reviewer_selected_path": "",
            "selection_rationale": "",
            "selection_status": "No pathway selected",
            "judgment_boundary": {
                "owner": "reviewer",
                "statement": "The system does not rank or select a pathway. Final judgment remains with the reviewer.",
            },
        },
        "evidence_sufficiency": {
            "tier": "Reviewable",
            "rationale": "Four unique records and one detectable source identity are present.",
            "rule_explanation": "The structural review threshold is met.",
            "missing_evidence": ["Product-level exposure data."],
            "limitations": ["Source independence is not established."],
            "interpretation_boundary": "Structural assessment only; factual validity is not established.",
        },
        "artifact_completeness": {
            "status": "Incomplete",
            "passed_checks": 7,
            "total_checks": 8,
            "dimensions": [
                {"name": "decision_question", "complete": True, "explanation": "A question is present."},
                {"name": "limitations", "complete": False, "explanation": "More limitations are required."},
            ],
            "interpretation_boundary": "Completeness checks structure only, not factual or decision quality.",
        },
    }


def test_rich_fixture_renders_substantive_neutral_sections() -> None:
    brief = render_rich_neutral_assessment(rich_analysis_fixture())

    expected_content = [
        "Licensing rules may affect advanced-chip shipments.",
        "The rule names advanced-chip shipment restrictions.",
        "HistoricalRetriever matched the scenario.",
        "Verify the primary rule before operational use.",
        "Technology Access Restriction",
        "Firms expanded license and customer screening.",
        "Frequencies below describe only the retrieved local case set. They are not real-world probabilities.",
        "Operational adjustment",
        "Both cases involve licensing constraints.",
        "access constraints affect capacity planning",
        "The source names restricted chip shipments.",
        "Maintain current plan while verifying exposure",
        "Preserves flexibility but may delay preparation.",
        "Customer commitments may require review.",
        "Monitor licensing guidance and end-user rules.",
        "Monitor publication of implementation guidance.",
        "New licensing guidance becomes available.",
        "Customer-specific eligibility is unknown.",
        "Which evidence gap most affects shipment eligibility?",
        "Reviewable — Structural assessment only",
        "7 of 8 passed",
        "Final judgment remains with the reviewer.",
    ]
    for text in expected_content:
        assert text in brief
    for text in FORBIDDEN_CURRENT_CONTRACT_TEXT:
        assert text not in brief


def test_pipeline_and_exports_remain_detailed_structured_and_neutral() -> None:
    client = TestClient(app)
    response = client.post("/analyze", json=ANALYZE_PAYLOAD)

    assert response.status_code == 200
    payload = response.json()
    markdown = payload["brief_markdown"]
    plain_text = payload["brief_text"]
    analysis = payload["analysis"]
    required_sections = [
        "Current Event Context",
        "Evidence Overview",
        "Mechanisms Detected",
        "Historical Analogues and Outcomes",
        "Competing Interpretations",
        "Multi-Lens Analysis",
        "Pathways for Review",
        "Evidence Sufficiency",
        "Artifact Completeness",
        "Judgment Boundary",
    ]
    for section in required_sections:
        assert f"## {section}" in markdown
        assert section in plain_text
    assert len(markdown) > 10_000
    assert "The document does not quantify cost, demand, or capacity effects." in markdown
    assert "The document does not quantify cost, demand, or capacity effects." in plain_text
    assert analysis["mechanisms"]
    assert analysis["analogues"]
    assert analysis["historical_outcomes"]
    assert analysis["lenses"]
    assert analysis["evidence_ledger"]["items"]
    assert analysis["decision_assessment"]["reviewer_selected_path"] == ""

    run_id = payload["run_id"]
    markdown_export = client.get(f"/run/{run_id}/download/markdown").text
    text_export = client.get(f"/run/{run_id}/download/txt").text
    json_export = client.get(f"/run/{run_id}/download/json").json()
    assert "Historical Analogues and Outcomes" in markdown_export
    assert "Historical Analogues and Outcomes" in text_export
    assert json_export["historical_outcomes"]
    assert json_export["evidence_credibility"]
    for output in (markdown, plain_text, markdown_export, text_export):
        for text in FORBIDDEN_CURRENT_CONTRACT_TEXT:
            assert text not in output
