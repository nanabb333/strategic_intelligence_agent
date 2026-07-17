from serialization import serializable
from decision_assessment import (
    ASSESSMENT_CONTRACT,
    build_neutral_decision_assessment,
    normalize_stored_decision_assessment,
)
from decision_pathways import build_decision_pathway_drafts
from decision_readiness import build_decision_readiness_map
from pathway_comparison import build_pathway_comparison_matrix


PROHIBITED_KEYS = {
    "recommended_path",
    "recommendation",
    "ranking",
    "rank",
    "score",
    "best_pathway",
    "preferred_option",
    "selected_pathway",
    "winner",
}


def _evidence(evidence_id: str, source_name: str, excerpt: str) -> dict[str, str]:
    return {
        "evidence_id": evidence_id,
        "title": f"{source_name} evidence",
        "source_type": source_name,
        "source_name": source_name,
        "source_url": f"https://example.com/{evidence_id}",
        "published_at": "2026-06-30",
        "retrieved_at": "2026-06-30T10:00:00",
        "excerpt": excerpt,
        "summary": excerpt,
        "status": "Accepted",
    }


def _neutral_inputs() -> tuple[dict, dict]:
    readiness = build_decision_readiness_map(
        decision_question="Should reviewers reassess market exposure after an earnings revision?",
        evidence_items=[
            _evidence("market", "Financial market", "Market volatility repricing demand shock earnings revision."),
            _evidence("company", "Company investor relations", "Company earnings revenue margin liquidity guidance update."),
            _evidence("filing", "SEC filing 10-K", "SEC disclosure reporting fiduciary governance filing."),
            _evidence("news", "Major news", "Counterparty risk uncertainty and market repricing remain under review."),
        ],
    )
    draft_set = build_decision_pathway_drafts(readiness_map=readiness)
    matrix = build_pathway_comparison_matrix(pathway_draft_set=draft_set, readiness_map=readiness)
    return draft_set, matrix


def _assessment(**overrides):
    draft_set, matrix = _neutral_inputs()
    return build_neutral_decision_assessment(
        assessment_summary="Evidence supports comparison across distinct pathways while final judgment remains with the reviewer.",
        pathway_draft_set=draft_set,
        comparison_matrix=matrix,
        **overrides,
    )


def test_contract_and_reviewer_boundary_are_explicit() -> None:
    payload = serializable(_assessment())

    assert payload["assessment_contract"] == ASSESSMENT_CONTRACT == "neutral-decision-assessment-v1"
    assert "final_judgment" not in payload
    assert payload["judgment_boundary"]["owner"] == "reviewer"
    assert "Final judgment remains with the reviewer" in payload["judgment_boundary"]["statement"]
    assert payload["reviewer_selected_path"] == ""
    assert payload["selection_rationale"] == ""
    assert payload["selection_status"] == "No pathway selected"


def test_serialization_is_deterministic_and_pathway_order_is_non_evaluative() -> None:
    first = serializable(_assessment())
    second = serializable(_assessment())
    pathway_ids = [item["pathway_id"] for item in first["pathways_for_review"]]

    assert first == second
    assert len(pathway_ids) >= 2
    assert pathway_ids == sorted(pathway_ids)
    assert all(PROHIBITED_KEYS.isdisjoint(item) for item in first["pathways_for_review"])


def test_pathways_preserve_neutral_review_structures() -> None:
    pathways = serializable(_assessment())["pathways_for_review"]

    assert len({item["pathway_id"] for item in pathways}) == len(pathways)
    for pathway in pathways:
        assert pathway["pathway_id"]
        assert set(pathway["pathway_evidence"]) == {"supporting", "weakening", "gaps"}
        assert pathway["pathway_evidence"]["supporting"]
        assert pathway["pathway_tradeoffs"]
        assert isinstance(pathway["risks"], list)
        assert pathway["reversibility"]
        assert pathway["timing_implications"]
        assert set(pathway["pathway_conditions"]) == {"more_supportable_when", "less_supportable_when"}
        assert pathway["reviewer_questions"]
        assert isinstance(pathway["limitations"], list)


def test_normalized_evidence_and_conditions_are_preserved_by_pathway_id() -> None:
    draft_set, _ = _neutral_inputs()
    pathway_id = draft_set["pathway_drafts"][0]["pathway_id"]
    weakening = {"evidence_id": "weak_1", "title": "Weakening evidence"}
    gap = {"evidence_id": "gap_1", "title": "Evidence gap"}
    assessment = _assessment(
        pathway_evidence={pathway_id: {"weakening": [weakening], "gaps": [gap]}},
        pathway_conditions={
            pathway_id: {
                "more_supportable_when": ["Accepted evidence resolves the timing uncertainty."],
                "less_supportable_when": ["A binding constraint removes reversibility."],
            }
        },
    )
    pathway = next(item for item in serializable(assessment)["pathways_for_review"] if item["pathway_id"] == pathway_id)

    assert pathway["pathway_evidence"]["weakening"] == [weakening]
    assert pathway["pathway_evidence"]["gaps"] == [gap]
    assert pathway["pathway_conditions"]["more_supportable_when"]
    assert pathway["pathway_conditions"]["less_supportable_when"]


def test_missing_normalized_inputs_remain_honest_empty_collections() -> None:
    draft_set, matrix = _neutral_inputs()
    assessment = build_neutral_decision_assessment(pathway_draft_set=draft_set, comparison_matrix=matrix)
    payload = serializable(assessment)

    assert payload["assessment_summary"] == ""
    for pathway in payload["pathways_for_review"]:
        assert pathway["pathway_evidence"]["weakening"] == []
        assert pathway["pathway_evidence"]["gaps"] == []
        assert pathway["pathway_conditions"]["more_supportable_when"] == []
        assert pathway["pathway_conditions"]["less_supportable_when"] == []


def test_serialized_neutral_contract_has_no_selection_or_evaluation_keys() -> None:
    keys = _all_keys(serializable(_assessment()))

    assert PROHIBITED_KEYS.isdisjoint(keys)


def test_legacy_recommendation_is_ignored_and_not_converted_to_reviewer_selection() -> None:
    normalized = normalize_stored_decision_assessment(
        {
            "decision_case": {
                "decision_question": "What should reviewers compare?",
                "situation": "Legacy situation",
                "recommended_path": "Option B: system-selected legacy path",
                "limitations": ["Legacy limitation"],
            }
        }
    )

    assert normalized["reviewer_selected_path"] == ""
    assert normalized["selection_status"] == "No pathway selected"
    assert normalized["legacy_compatibility"]["system_recommendation_ignored"] is True
    assert "recommended_path" not in normalized


def test_legacy_final_judgment_is_normalized_as_ownership_boundary() -> None:
    normalized = normalize_stored_decision_assessment(
        {
            "decision_assessment": {
                "decision_question": "What should reviewers compare?",
                "final_judgment": {
                    "owner": "reviewer",
                    "statement": "Final judgment remains with the reviewer.",
                },
            }
        }
    )

    assert "final_judgment" not in normalized
    assert normalized["judgment_boundary"]["owner"] == "reviewer"
    assert normalized["reviewer_selected_path"] == ""
    assert normalized["selection_rationale"] == ""


def _all_keys(value) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_all_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_all_keys(item))
        return keys
    return set()
