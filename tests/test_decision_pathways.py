import json

from fastapi.testclient import TestClient

from app import app
from decision_pathways import build_decision_pathway_drafts
from decision_readiness import build_decision_readiness_map
import project_workspace
from project_workspace import create_project


def _evidence(**overrides):
    base = {
        "evidence_id": "ev_base",
        "title": "Market and regulatory evidence",
        "source_type": "Major news",
        "source_name": "Reuters",
        "source_url": "https://news.example/evidence",
        "published_at": "2026-06-30",
        "retrieved_at": "2026-06-30T10:00:00",
        "excerpt": "Market volatility, regulatory approval, licensing, and demand shock remain relevant.",
        "summary": "Evidence summary.",
        "credibility_tier": "Tier 3 Reputable News",
        "validation_status": "Valid",
        "status": "Accepted",
    }
    base.update(overrides)
    return base


def _ready_readiness():
    return build_decision_readiness_map(
        decision_question="Should the investment portfolio adjust market exposure after earnings revision?",
        evidence_items=[
            _evidence(evidence_id="market", title="Market data", source_type="Financial market", source_name="Market Data", source_url="https://market.example/data", excerpt="Market volatility repricing demand shock earnings revision."),
            _evidence(evidence_id="company", title="Company earnings", source_type="Company investor relations", source_name="Investor Relations", source_url="https://company.example/ir", excerpt="Company earnings revenue margin liquidity and guidance update."),
            _evidence(evidence_id="sec", title="SEC filing 10-K", source_type="SEC filing 10-K", source_name="SEC", source_url="https://sec.gov/filing", excerpt="SEC disclosure reporting fiduciary governance 10-K filing."),
            _evidence(evidence_id="news", title="Reuters market report", source_type="Major news", source_name="Reuters", source_url="https://reuters.example/report", excerpt="Counterparty risk, uncertainty, and market repricing remain under review."),
        ],
    )


def test_sufficient_readiness_generates_two_to_four_unranked_drafts() -> None:
    draft_set = build_decision_pathway_drafts(readiness_map=_ready_readiness())

    assert 2 <= len(draft_set["pathway_drafts"]) <= 4
    assert draft_set["readiness_state"] == "ready_for_pathway_analysis"
    assert all("Possible pathway" in draft["title"] for draft in draft_set["pathway_drafts"])
    assert all("supporting_evidence_refs" in draft for draft in draft_set["pathway_drafts"])


def test_insufficient_readiness_generates_further_evidence_only() -> None:
    readiness = build_decision_readiness_map(decision_question="", evidence_items=[])

    draft_set = build_decision_pathway_drafts(readiness_map=readiness)

    assert [draft["pathway_family"] for draft in draft_set["pathway_drafts"]] == ["further_evidence_required"]
    assert "evidence gaps" in " ".join(draft_set["pathway_drafts"][0]["limitation_notes"]).lower()


def test_regulatory_uncertainty_generates_seek_regulatory_clarity() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we enter a new market with licensing approval requirements?",
        evidence_items=[
            _evidence(evidence_id="market", title="Market entry demand note", source_url="https://news.example/market", excerpt="Market entry launch demand shock and consumer demand remain strong."),
        ],
    )

    draft_set = build_decision_pathway_drafts(readiness_map=readiness)
    families = [draft["pathway_family"] for draft in draft_set["pathway_drafts"]]

    assert "seek_regulatory_clarity" in families
    assert any("not legal advice" in " ".join(draft["limitation_notes"]).lower() for draft in draft_set["pathway_drafts"])


def test_unresolved_conflicts_appear_as_limitations_and_questions() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we review export control licensing?",
        evidence_items=[
            _evidence(evidence_id="approved", excerpt="The regulator approved the export license."),
            _evidence(evidence_id="blocked", source_url="https://news.example/conflict", excerpt="The export license was blocked and not confirmed."),
        ],
    )

    draft = build_decision_pathway_drafts(readiness_map=readiness)["pathway_drafts"][0]

    assert draft["pathway_family"] == "further_evidence_required"
    assert any("conflict" in item.lower() for item in draft["limitation_notes"])
    assert any("conflict" in item.lower() for item in draft["reviewer_questions"])


def test_stale_or_source_concentrated_evidence_adds_limitation() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we review supply chain supplier plans?",
        evidence_items=[
            _evidence(evidence_id="old1", source_type="Major news", source_name="Reuters", published_at="2020-01-01", excerpt="Supply chain supplier logistics disruption."),
            _evidence(evidence_id="old2", source_type="Major news", source_name="Reuters", published_at="2020-01-02", source_url="https://news.example/two", excerpt="Supply chain inventory shortage and delayed resolution."),
        ],
    )

    draft_set = build_decision_pathway_drafts(readiness_map=readiness)
    text = " ".join(note for draft in draft_set["pathway_drafts"] for note in draft["limitation_notes"]).lower()

    assert "freshness" in text or "source diversity" in text or "source concentration" in text


def test_pathways_include_traceable_evidence_refs() -> None:
    draft_set = build_decision_pathway_drafts(readiness_map=_ready_readiness())

    refs = [ref for draft in draft_set["pathway_drafts"] for ref in draft["supporting_evidence_refs"]]

    assert refs
    assert all(ref.get("evidence_id") and ref.get("title") for ref in refs)


def test_pathway_payload_has_no_ranking_probability_or_recommendation_fields() -> None:
    draft_set = build_decision_pathway_drafts(readiness_map=_ready_readiness())

    keys = _all_keys(draft_set)

    assert "ranking" not in keys
    assert "probability" not in keys
    assert "recommendation_score" not in keys
    assert "best_pathway" not in keys
    assert "recommended" not in keys


def test_pathway_api_is_read_only(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    project = create_project("Pathway Workspace")
    project["questions"] = [{"question_id": "q1", "question": "Should we review export control licensing?"}]
    project["evidence_library"] = [_evidence(evidence_id="ev1")]
    project_workspace.save_project(project)
    path = project_workspace.PROJECTS_DIR / f"{project['project_id']}.json"
    before = json.loads(path.read_text(encoding="utf-8"))

    response = TestClient(app).get(f"/projects/{project['project_id']}/decision/pathways")
    after = json.loads(path.read_text(encoding="utf-8"))

    assert response.status_code == 200
    payload = response.json()
    assert payload["pathway_drafts"]
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
