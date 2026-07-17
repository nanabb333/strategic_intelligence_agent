import importlib

import pytest


def test_decision_case_shim_normalizes_but_does_not_generate_preferred_path() -> None:
    with pytest.warns(DeprecationWarning):
        module = importlib.reload(importlib.import_module("decision_case"))

    normalized = module.normalize_legacy_decision_case(
        {"decision_question": "What should reviewers compare?", "recommended_path": "Option B"}
    )
    assert normalized["reviewer_selected_path"] == ""
    assert normalized["selection_rationale"] == ""
    assert "recommended_path" not in normalized
    with pytest.raises(module.DeprecatedDecisionContractError, match="decision_assessment"):
        module.build_decision_case()


def test_confidence_shim_maps_legacy_for_read_only_display_and_rejects_generation() -> None:
    with pytest.warns(DeprecationWarning):
        module = importlib.reload(importlib.import_module("confidence_layer"))

    normalized = module.normalize_legacy_confidence({"confidence_level": "High"})
    assert normalized["tier"] == "Reviewable"
    assert normalized["legacy_compatibility"]["read_only"] is True
    with pytest.raises(module.DeprecatedConfidenceContractError, match="evidence_sufficiency"):
        module.assess_confidence()


def test_decision_quality_shim_drops_legacy_scores_and_rejects_evaluation() -> None:
    with pytest.warns(DeprecationWarning):
        module = importlib.reload(importlib.import_module("decision_quality_evaluator"))

    normalized = module.normalize_legacy_decision_quality({"overall_score": 1.0})
    assert "overall_score" not in normalized
    assert normalized["legacy_compatibility"]["contract_status"] == "superseded"
    with pytest.raises(module.DeprecatedDecisionQualityContractError, match="artifact_completeness"):
        module.evaluate_decision_quality()
