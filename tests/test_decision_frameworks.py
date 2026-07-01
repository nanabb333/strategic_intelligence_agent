from dataclasses import asdict

from decision_frameworks import (
    CONFIDENCE_BUCKETS,
    DecisionComparison,
    DecisionPathway,
    classify_decision_question,
    framework_registry,
    get_decision_framework,
    load_decision_frameworks,
    validate_framework,
)


def test_framework_loading_includes_initial_library() -> None:
    frameworks = load_decision_frameworks()
    framework_ids = {framework.framework_id for framework in frameworks}

    assert len(frameworks) == 10
    assert framework_ids == {
        "investment_decision",
        "corporate_strategy",
        "supply_chain",
        "regulatory_compliance",
        "export_control",
        "market_entry",
        "strategic_partnership",
        "capital_allocation",
        "technology_strategy",
        "board_executive_decision",
    }


def test_framework_validation_has_no_warnings_for_library() -> None:
    for framework in load_decision_frameworks():
        assert validate_framework(framework) == []
        assert framework.reviewer_questions
        assert framework.pathway_dimensions


def test_framework_registry_lookup_is_stable() -> None:
    registry = framework_registry()

    assert registry["export_control"].name == "Export Control"
    assert get_decision_framework("market_entry") is registry["market_entry"]
    assert get_decision_framework("missing") is None


def test_decision_classification_uses_question_context_and_metadata() -> None:
    classification = classify_decision_question(
        "Should we adjust the supplier plan after export control licensing changes?",
        decision_context="The issue affects logistics, inventory, and restricted-party review.",
        evidence_metadata=[
            {
                "risk_categories": ["supply_chain_risk", "sanctions_export_control_risk"],
                "regulatory_constraints": ["sanctions_export_controls", "licensing_approval"],
                "evidence_categories": ["official_government"],
            }
        ],
    )

    framework_ids = {framework.framework_id for framework in classification.applicable_frameworks}

    assert classification.confidence_bucket in CONFIDENCE_BUCKETS
    assert classification.confidence_bucket == "High"
    assert "export_control" in framework_ids
    assert "supply_chain" in framework_ids
    assert "export control" in classification.matched_keywords
    assert "sanctions_export_controls" in classification.matched_metadata


def test_decision_classification_supports_multi_framework_matching() -> None:
    classification = classify_decision_question(
        "Should the board approve a strategic partnership and capital allocation for the new technology platform?",
        evidence_metadata=[
            {
                "risk_categories": ["data_privacy_security_risk", "counterparty_risk", "financial_risk"],
                "regulatory_constraints": ["fiduciary_governance", "data_privacy"],
            }
        ],
    )

    framework_ids = {framework.framework_id for framework in classification.applicable_frameworks}

    assert "board_executive_decision" in framework_ids
    assert "strategic_partnership" in framework_ids
    assert "technology_strategy" in framework_ids
    assert "capital_allocation" in framework_ids
    assert classification.rationale.startswith("Decision question classified")


def test_decision_classification_fallback_is_low_confidence_governance_review() -> None:
    classification = classify_decision_question("What should we do next?")

    assert classification.decision_type == "Unclassified Decision"
    assert classification.confidence_bucket == "Low"
    assert [framework.framework_id for framework in classification.applicable_frameworks] == ["board_executive_decision"]
    assert classification.matched_keywords == []


def test_decision_pathway_model_has_no_ranking_or_probability_fields() -> None:
    pathway = DecisionPathway(
        pathway_id="pathway_1",
        title="Staged Review",
        description="A reviewer-defined pathway for comparing evidence and unknowns.",
        supporting_evidence_refs=[{"evidence_id": "ev1", "title": "Evidence"}],
        risk_categories=["regulatory_risk"],
        regulatory_constraints=["licensing_approval"],
        assumptions=["Reviewer validates source context."],
        unknowns=["Jurisdiction applicability."],
        decision_triggers=["New regulator notice."],
        tradeoffs=["Speed versus review completeness."],
        reviewer_notes=["No recommendation is implied."],
    )
    payload = asdict(pathway)

    assert payload["pathway_id"] == "pathway_1"
    assert "recommendation_score" not in payload
    assert "probability" not in payload
    assert "ranking" not in payload
    assert "best_pathway" not in payload


def test_decision_comparison_model_is_structural_only() -> None:
    left = DecisionPathway(pathway_id="path_a", title="A", description="A")
    right = DecisionPathway(pathway_id="path_b", title="B", description="B")
    comparison = DecisionComparison(
        pathways=[left, right],
        comparison_dimensions=["evidence", "risk", "constraints", "unknowns"],
        evidence_matrix={"path_a": ["ev1"]},
        risk_matrix={"path_b": ["market_risk"]},
        constraint_matrix={"path_a": ["licensing_approval"]},
        historical_matrix={"path_b": ["delayed_resolution"]},
        unknown_matrix={"path_a": ["missing jurisdiction detail"]},
    )
    payload = asdict(comparison)

    assert len(comparison.pathways) == 2
    assert payload["comparison_dimensions"] == ["evidence", "risk", "constraints", "unknowns"]
    assert "recommendation" not in payload
    assert "ranking" not in payload


def test_decision_framework_module_does_not_change_existing_analysis_contract() -> None:
    classification = classify_decision_question("Should we review regulatory approval timing?")

    assert classification.decision_type
    assert classification.applicable_frameworks
    assert all(hasattr(framework, "framework_id") for framework in classification.applicable_frameworks)
