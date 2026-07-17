from decision_assessment import NeutralDecisionAssessment, PathwayForReview
from evidence_ledger import EvidenceItem, EvidenceLedger
from evidence_sufficiency import (
    TIERS,
    assess_evidence_sufficiency,
    normalize_stored_evidence_sufficiency,
    render_evidence_sufficiency_section,
)


def _assessment() -> NeutralDecisionAssessment:
    return NeutralDecisionAssessment(
        decision_question="What pathways should reviewers compare?",
        assessment_summary="Neutral review.",
        comparison_criteria=["evidence_support"],
        pathways_for_review=[
            PathwayForReview("p1", "Path 1", "staged_commitment", "First path"),
            PathwayForReview("p2", "Path 2", "delay_or_wait", "Second path"),
        ],
    )


def _item(
    evidence_id: str,
    *,
    source_identity: str = "",
    externally_sourced: bool = False,
    source_status: str = "",
    source_type: str = "User-provided input material",
    confidence: str = "Moderate",
) -> EvidenceItem:
    return EvidenceItem(
        evidence_id=evidence_id,
        source_type=source_type,
        evidence_text="Source evidence.",
        observation="Evidence observation.",
        inference="Evidence inference.",
        claim_supported="Assessment context.",
        relevance="High",
        confidence=confidence,
        limitations="Human verification required.",
        used_in_section="Evidence Sufficiency",
        source_identity=source_identity,
        source_status=source_status,
        externally_sourced=externally_sourced,
    )


def _ledger(items: list[EvidenceItem]) -> EvidenceLedger:
    return EvidenceLedger(items=items)


def test_all_structural_tiers_use_explicit_rules() -> None:
    insufficient = assess_evidence_sufficiency(_assessment(), _ledger([_item("E1")]))
    limited = assess_evidence_sufficiency(
        _assessment(),
        _ledger([_item(f"E{i}", source_identity="url:a", externally_sourced=True) for i in range(3)]),
    )
    reviewable = assess_evidence_sufficiency(
        _assessment(),
        _ledger([_item(f"E{i}", source_identity="url:a", externally_sourced=True) for i in range(4)]),
    )
    evidence_rich = assess_evidence_sufficiency(
        _assessment(),
        _ledger(
            [
                _item(
                    f"E{i}",
                    source_identity=f"url:{i % 3}",
                    externally_sourced=True,
                )
                for i in range(7)
            ]
        ),
    )

    assert TIERS == {"Insufficient", "Limited", "Reviewable", "Evidence-rich"}
    assert insufficient.tier == "Insufficient"
    assert limited.tier == "Limited"
    assert reviewable.tier == "Reviewable"
    assert evidence_rich.tier == "Evidence-rich"
    assert "Structural assessment only" in evidence_rich.interpretation_boundary


def test_duplicate_evidence_id_does_not_increase_unique_count() -> None:
    items = [_item("same", source_identity="url:a", externally_sourced=True) for _ in range(7)]
    result = assess_evidence_sufficiency(_assessment(), _ledger(items))

    assert result.tier == "Insufficient"
    assert result.evidence_item_count == 1
    assert result.duplicate_item_count == 6


def test_same_source_records_do_not_increase_detectable_source_diversity() -> None:
    items = [_item(f"E{i}", source_identity="url:same", externally_sourced=True) for i in range(7)]
    result = assess_evidence_sufficiency(_assessment(), _ledger(items))

    assert result.tier == "Reviewable"
    assert result.source_based_item_count == 1


def test_source_pending_does_not_count_as_detectable_source() -> None:
    items = [
        _item(
            f"E{i}",
            source_identity=f"url:{i}",
            externally_sourced=True,
            source_status="source pending",
        )
        for i in range(4)
    ]
    result = assess_evidence_sufficiency(_assessment(), _ledger(items))

    assert result.tier == "Limited"
    assert result.source_based_item_count == 0


def test_unverified_analogue_does_not_count_as_external_source() -> None:
    items = [
        _item(
            f"A{i}",
            source_identity=f"local-analogue:{i}",
            externally_sourced=False,
            source_status="Unverified analogue",
            source_type="Local historical analogue record",
        )
        for i in range(4)
    ]
    result = assess_evidence_sufficiency(_assessment(), _ledger(items))

    assert result.tier == "Limited"
    assert result.source_based_item_count == 0


def test_sufficiency_section_places_structural_boundary_next_to_tier() -> None:
    ledger = _ledger([_item("E1")])
    result = assess_evidence_sufficiency(_assessment(), ledger)
    rendered = render_evidence_sufficiency_section(result, ledger)

    assert "**Tier:** Insufficient — Structural assessment only" in rendered
    assert "claim-level support" in rendered
    assert "probability of correctness" in rendered


def test_legacy_confidence_is_read_only_and_not_treated_as_calibrated() -> None:
    normalized = normalize_stored_evidence_sufficiency(
        {"confidence_assessment": {"confidence_level": "High", "limitations": ["Legacy limit"]}}
    )

    assert normalized["tier"] == "Reviewable"
    assert normalized["legacy_compatibility"]["read_only"] is True
    assert "not treated as calibrated confidence" in normalized["interpretation_boundary"]
