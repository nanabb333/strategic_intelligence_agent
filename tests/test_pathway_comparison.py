import json

from fastapi.testclient import TestClient

from app import app
from decision_pathways import build_decision_pathway_drafts
from decision_readiness import build_decision_readiness_map
from domain_evaluation import build_domain_evaluation
from evidence_intelligence import build_evidence_intelligence
from pathway_comparison import build_pathway_comparison_matrix
import project_workspace
from project_workspace import create_project


def _evidence(**overrides):
    base = {
        "evidence_id": "ev_compare",
        "title": "Comparison evidence",
        "source_type": "Major news",
        "source_name": "Reuters",
        "source_url": "https://news.example/compare",
        "published_at": "2026-06-30",
        "retrieved_at": "2026-06-30T10:00:00",
        "excerpt": "Market volatility, regulatory approval, debt leverage, and liquidity risk remain relevant.",
        "summary": "Comparison evidence.",
        "status": "Accepted",
    }
    base.update(overrides)
    return base


def _ready_inputs():
    question = "Should the investment portfolio adjust market exposure after earnings revision?"
    evidence = [
        _evidence(evidence_id="market", title="Market data", source_type="Financial market", source_name="Market Data", source_url="https://market.example/data", excerpt="Market volatility repricing demand shock earnings revision duration risk equity valuation risk."),
        _evidence(evidence_id="company", title="Company earnings", source_type="Company investor relations", source_name="Investor Relations", source_url="https://company.example/ir", excerpt="Company earnings revenue margin liquidity and guidance update."),
        _evidence(evidence_id="sec", title="SEC filing 10-K", source_type="SEC filing 10-K", source_name="SEC", source_url="https://sec.gov/filing", excerpt="SEC disclosure reporting fiduciary governance 10-K filing."),
        _evidence(evidence_id="news", title="Reuters market report", source_type="Major news", source_name="Reuters", source_url="https://reuters.example/report", excerpt="Counterparty risk, credit spread, uncertainty, and market repricing remain under review."),
    ]
    readiness = build_decision_readiness_map(decision_question=question, evidence_items=evidence)
    pathways = build_decision_pathway_drafts(readiness_map=readiness)
    domain = build_domain_evaluation(decision_question=question, evidence_items=evidence)
    intelligence = build_evidence_intelligence(evidence)
    return question, readiness, pathways, domain, intelligence


def test_comparison_matrix_generated_from_multiple_pathway_drafts() -> None:
    question, readiness, pathways, domain, intelligence = _ready_inputs()

    matrix = build_pathway_comparison_matrix(
        decision_question=question,
        pathway_draft_set=pathways,
        readiness_map=readiness,
        domain_evaluation=domain,
        evidence_intelligence=intelligence,
    )

    assert len(matrix["pathway_comparisons"]) >= 2
    assert "evidence_support" in matrix["comparison_dimensions"]
    assert all(row["dimension_buckets"] for row in matrix["pathway_comparisons"])


def test_comparison_matrix_has_no_ranking_probability_or_recommendation_fields() -> None:
    _, readiness, pathways, domain, intelligence = _ready_inputs()

    matrix = build_pathway_comparison_matrix(
        pathway_draft_set=pathways,
        readiness_map=readiness,
        domain_evaluation=domain,
        evidence_intelligence=intelligence,
    )
    keys = _all_keys(matrix)

    assert "ranking" not in keys
    assert "score" not in keys
    assert "probability" not in keys
    assert "recommendation" not in keys
    assert "best_option" not in keys


def test_unresolved_unknowns_create_high_unknown_bucket() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we review export control licensing?",
        evidence_items=[
            _evidence(evidence_id="approved", excerpt="The regulator approved the export license."),
            _evidence(evidence_id="blocked", source_url="https://news.example/conflict", excerpt="The export license was blocked and not confirmed."),
        ],
    )
    pathways = build_decision_pathway_drafts(readiness_map=readiness)
    matrix = build_pathway_comparison_matrix(pathway_draft_set=pathways, readiness_map=readiness)

    assert matrix["pathway_comparisons"][0]["dimension_buckets"]["unknowns_remaining"] == "high"


def test_regulatory_constraints_reflected_in_matrix() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we enter a new market with licensing approval requirements?",
        evidence_items=[_evidence(evidence_id="market", excerpt="Market entry launch demand shock and consumer demand remain strong.")],
    )
    pathways = build_decision_pathway_drafts(readiness_map=readiness)
    matrix = build_pathway_comparison_matrix(pathway_draft_set=pathways, readiness_map=readiness)

    assert matrix["pathway_comparisons"][0]["dimension_buckets"]["regulatory_constraints"] == "high"


def test_domain_evaluation_risks_reflected_in_matrix() -> None:
    question, readiness, pathways, domain, intelligence = _ready_inputs()
    matrix = build_pathway_comparison_matrix(
        decision_question=question,
        pathway_draft_set=pathways,
        readiness_map=readiness,
        domain_evaluation=domain,
        evidence_intelligence=intelligence,
    )

    assert any(row["dimension_buckets"]["domain_specific_risks"] in {"medium", "high"} for row in matrix["pathway_comparisons"])


def test_stale_source_concentrated_evidence_reflected_as_quality_concern() -> None:
    evidence = [
        _evidence(evidence_id="old1", source_type="Major news", source_name="Reuters", published_at="2020-01-01", excerpt="Supply chain supplier logistics disruption."),
        _evidence(evidence_id="old2", source_type="Major news", source_name="Reuters", published_at="2020-01-02", source_url="https://news.example/two", excerpt="Supply chain inventory shortage and delayed resolution."),
    ]
    readiness = build_decision_readiness_map(decision_question="Should we review supply chain supplier plans?", evidence_items=evidence)
    pathways = build_decision_pathway_drafts(readiness_map=readiness)
    intelligence = build_evidence_intelligence(evidence)
    matrix = build_pathway_comparison_matrix(pathway_draft_set=pathways, readiness_map=readiness, evidence_intelligence=intelligence)

    assert matrix["pathway_comparisons"][0]["dimension_buckets"]["evidence_quality_concerns"] == "high"


def test_execution_complexity_and_reversibility_buckets() -> None:
    _, readiness, pathways, domain, intelligence = _ready_inputs()
    matrix = build_pathway_comparison_matrix(
        pathway_draft_set=pathways,
        readiness_map=readiness,
        domain_evaluation=domain,
        evidence_intelligence=intelligence,
    )
    buckets = {row["pathway_family"]: row["dimension_buckets"] for row in matrix["pathway_comparisons"]}

    assert buckets["staged_commitment"]["execution_complexity"] == "medium"
    assert buckets["staged_commitment"]["reversibility"] == "high"


def test_traceable_evidence_refs_preserved() -> None:
    _, readiness, pathways, domain, intelligence = _ready_inputs()
    matrix = build_pathway_comparison_matrix(
        pathway_draft_set=pathways,
        readiness_map=readiness,
        domain_evaluation=domain,
        evidence_intelligence=intelligence,
    )
    refs = [ref for row in matrix["pathway_comparisons"] for ref in row["supporting_evidence_refs"]]

    assert refs
    assert all(ref.get("evidence_id") and ref.get("title") for ref in refs)


def test_pathway_comparison_api_is_read_only(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    project = create_project("Comparison Workspace")
    project["questions"] = [{"question_id": "q1", "question": "Should we review credit and market exposure?"}]
    project["evidence_library"] = [_evidence(evidence_id="ev1")]
    project_workspace.save_project(project)
    path = project_workspace.PROJECTS_DIR / f"{project['project_id']}.json"
    before = json.loads(path.read_text(encoding="utf-8"))

    response = TestClient(app).get(f"/projects/{project['project_id']}/decision/pathway-comparison")
    after = json.loads(path.read_text(encoding="utf-8"))

    assert response.status_code == 200
    assert response.json()["pathway_comparisons"]
    assert after == before


def _all_keys(value):
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(_all_keys(item))
        return keys
    if isinstance(value, list):
        keys = set()
        for item in value:
            keys.update(_all_keys(item))
        return keys
    return set()
