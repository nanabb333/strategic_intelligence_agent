from artifact_completeness import check_artifact_completeness, render_artifact_completeness
from decision_assessment import build_neutral_decision_assessment
from decision_pathways import build_decision_pathway_drafts
from decision_readiness import build_decision_readiness_map
from evidence_ledger import EvidenceItem, EvidenceLedger
from evidence_sufficiency import assess_evidence_sufficiency
from pathway_comparison import build_pathway_comparison_matrix


def _assessment_and_ledger():
    evidence = [
        {
            "evidence_id": f"E{index}",
            "title": f"Evidence {index}",
            "source_type": "User-provided input material",
            "summary": "Export controls affect licensing, customers, and supplier exposure.",
            "status": "Accepted",
        }
        for index in range(1, 5)
    ]
    readiness = build_decision_readiness_map(
        decision_question="Which pathways should reviewers compare?",
        evidence_items=evidence,
    )
    pathways = build_decision_pathway_drafts(readiness_map=readiness)
    matrix = build_pathway_comparison_matrix(pathway_draft_set=pathways, readiness_map=readiness)
    assessment = build_neutral_decision_assessment(
        assessment_summary="Reviewers should compare the evidence-aware pathways.",
        pathway_draft_set=pathways,
        comparison_matrix=matrix,
    )
    ledger = EvidenceLedger(
        items=[
            EvidenceItem(
                evidence_id=item["evidence_id"],
                source_type="User-provided input material",
                evidence_text=item["summary"],
                observation=item["title"],
                inference="This evidence informs reviewer comparison.",
                claim_supported="Pathway comparison.",
                relevance="High",
                confidence="Moderate",
                limitations="Source requires human verification.",
                used_in_section="Pathways for Review",
            )
            for item in evidence
        ]
    )
    return assessment, ledger


def test_artifact_completeness_is_not_decision_quality() -> None:
    assessment, ledger = _assessment_and_ledger()
    sufficiency = assess_evidence_sufficiency(assessment, ledger)
    result = check_artifact_completeness(
        assessment=assessment,
        evidence_ledger=ledger,
        evidence_sufficiency=sufficiency,
    )

    assert 0.0 <= result.completion_rate <= 1.0
    assert result.passed_checks <= result.total_checks
    assert result.dimensions
    assert "does not validate factual accuracy" in result.interpretation_boundary
    assert "decision quality" in result.interpretation_boundary
    rendered = render_artifact_completeness(result)
    assert "## Artifact Completeness Check" in rendered
    assert f"{result.passed_checks} of {result.total_checks} passed" in rendered
    assert "/ 10" not in rendered
    assert "Decision Quality Review" not in rendered


def test_reviewer_boundary_requires_no_automatic_selection() -> None:
    assessment, ledger = _assessment_and_ledger()
    sufficiency = assess_evidence_sufficiency(assessment, ledger)
    result = check_artifact_completeness(
        assessment=assessment,
        evidence_ledger=ledger,
        evidence_sufficiency=sufficiency,
    )

    boundary = next(item for item in result.dimensions if item.name == "reviewer_boundary")
    assert boundary.complete is True
    assert assessment.reviewer_selected_path == ""
