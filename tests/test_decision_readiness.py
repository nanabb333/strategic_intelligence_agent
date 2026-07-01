import json

from fastapi.testclient import TestClient

from app import app
from decision_readiness import build_decision_readiness_map
import project_workspace
from project_workspace import create_project


def _evidence(**overrides):
    base = {
        "evidence_id": "ev_base",
        "title": "Official export control licensing update",
        "source_type": "Government regulator",
        "source_name": "Commerce Department",
        "source_url": "https://agency.gov/update",
        "published_at": "2026-06-30",
        "retrieved_at": "2026-06-30T10:00:00",
        "excerpt": "Export control sanctions licensing approval and regulatory review affect suppliers.",
        "summary": "Official export-control update.",
        "credibility_tier": "Tier 1 Official",
        "validation_status": "Valid",
        "status": "Accepted",
    }
    base.update(overrides)
    return base


def test_export_control_framework_evidence_mapping_is_traceable() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we review export control sanctions and entity list exposure?",
        evidence_items=[
            _evidence(evidence_id="official", source_type="Government official", excerpt="Export controls sanctions entity list license approval geopolitical escalation."),
            _evidence(evidence_id="regulator", source_type="Regulator notice", source_name="Regulator", excerpt="Regulatory investigation enforcement export license review."),
            _evidence(evidence_id="legal", source_type="Legal regulatory note", source_name="Law Review", excerpt="Policy relief waiver exemption for export licensing may apply."),
        ],
    )

    export_map = next(item for item in readiness["framework_evidence_maps"] if item["framework_id"] == "export_control")

    assert readiness["primary_framework"]["framework_id"] == "export_control"
    assert export_map["risk_coverage"]["risks"][0]["evidence_refs"]
    assert export_map["constraint_coverage"]["constraints"][0]["evidence_refs"]
    assert export_map["historical_support"]["historical_dimensions"][0]["evidence_refs"]


def test_supply_chain_mapping_and_unknowns() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we adjust supply chain supplier logistics plans?",
        evidence_items=[
            _evidence(evidence_id="supply", source_type="Major news", source_name="Reuters", excerpt="Supply chain supplier logistics inventory disruption and demand shock."),
        ],
    )

    framework_ids = {item["framework_id"] for item in readiness["applicable_frameworks"]}
    unknown_categories = {item["category"] for item in readiness["unknowns_map"]}

    assert "supply_chain" in framework_ids
    assert "missing_supplier_data" in unknown_categories
    assert readiness["evidence_gaps"]


def test_investment_and_regulatory_mapping() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should the investment committee review market exposure and regulatory approval timing?",
        evidence_items=[
            _evidence(evidence_id="market", source_type="Financial market", source_name="Market Data", excerpt="Market volatility earnings revenue margin repricing and financial risk."),
            _evidence(evidence_id="filing", source_type="SEC filing 10-K", source_name="SEC", excerpt="SEC disclosure reporting and fiduciary governance considerations."),
            _evidence(evidence_id="reg", source_type="Regulator", source_name="Regulator", excerpt="Regulatory approval licensing and legal compliance review remain pending."),
        ],
    )
    framework_ids = {item["framework_id"] for item in readiness["applicable_frameworks"]}

    assert "investment_decision" in framework_ids
    assert "regulatory_compliance" in framework_ids
    assert readiness["risk_coverage"]
    assert readiness["constraint_coverage"]


def test_ready_for_pathway_analysis_state() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should the investment portfolio adjust market exposure after earnings revision?",
        evidence_items=[
            _evidence(evidence_id="market1", title="Market exposure note", source_type="Financial market", source_name="Market Data", source_url="https://market.example/data", excerpt="Market volatility repricing demand shock earnings revision."),
            _evidence(evidence_id="company1", title="Company earnings note", source_type="Company investor relations", source_name="Investor Relations", source_url="https://company.example/ir", excerpt="Company earnings revenue margin liquidity and guidance update."),
            _evidence(evidence_id="sec1", title="SEC filing 10-K", source_type="SEC filing 10-K", source_name="SEC", source_url="https://sec.gov/filing", excerpt="SEC disclosure reporting fiduciary governance 10-K filing."),
            _evidence(evidence_id="news1", title="Reuters market report", source_type="Major news", source_name="Reuters", source_url="https://reuters.example/report", excerpt="Counterparty risk, uncertainty, and market repricing remain under review."),
        ],
    )

    assert readiness["readiness_summary"]["readiness_state"] == "ready_for_pathway_analysis"


def test_partially_ready_state_for_missing_framework_dimensions() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we review corporate strategy?",
        evidence_items=[
            _evidence(evidence_id="strategy", source_type="Company investor relations", excerpt="Corporate strategy shift and execution capacity were discussed."),
        ],
    )

    assert readiness["readiness_summary"]["readiness_state"] in {"partially_ready", "not_ready_insufficient_evidence"}
    assert readiness["evidence_gaps"]


def test_not_ready_for_empty_project_data() -> None:
    readiness = build_decision_readiness_map(decision_question="", evidence_items=[])

    assert readiness["readiness_summary"]["readiness_state"] == "not_ready_insufficient_evidence"
    assert readiness["readiness_summary"]["evidence_count"] == 0


def test_blocked_by_conflicts_state() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we review export control licensing?",
        evidence_items=[
            _evidence(evidence_id="approved", excerpt="The regulator approved the export license."),
            _evidence(evidence_id="blocked", source_url="https://news.example/conflict", excerpt="The export license was blocked and not confirmed."),
        ],
    )

    assert readiness["readiness_summary"]["readiness_state"] == "blocked_by_conflicts"
    assert readiness["conflict_flags"][0]["evidence_refs"]


def test_blocked_by_regulatory_uncertainty_state() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we enter a new market with licensing approval requirements?",
        evidence_items=[
            _evidence(evidence_id="market", title="Market entry demand note", source_type="Major news", source_url="https://news.example/market", excerpt="Market entry launch demand shock and consumer demand remain strong."),
        ],
    )

    assert readiness["readiness_summary"]["readiness_state"] == "blocked_by_regulatory_uncertainty"
    assert any(issue["issue_type"] == "regulatory_uncertainty" for issue in readiness["readiness_issues"])


def test_stale_or_source_concentrated_state() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should we review supply chain supplier plans?",
        evidence_items=[
            _evidence(evidence_id="old1", source_type="Major news", source_name="Reuters", published_at="2020-01-01", excerpt="Supply chain supplier logistics disruption."),
            _evidence(evidence_id="old2", source_type="Major news", source_name="Reuters", published_at="2020-01-02", source_url="https://news.example/two", excerpt="Supply chain inventory shortage and delayed resolution."),
        ],
    )

    assert readiness["readiness_summary"]["readiness_state"] == "stale_or_low_diversity_evidence"
    assert readiness["freshness_flags"]
    assert readiness["source_diversity_flags"]


def test_assumptions_and_unknowns_include_required_categories() -> None:
    readiness = build_decision_readiness_map(
        decision_question="Should legal/compliance review regulatory approval?",
        evidence_items=[
            _evidence(evidence_id="legal", source_type="Regulator", excerpt="Regulatory approval licensing legal compliance and court review."),
        ],
    )
    assumptions = {item["category"] for item in readiness["assumption_map"]}
    unknowns = {item["category"] for item in readiness["unknowns_map"]}

    assert "legal_clearance" in assumptions
    assert "regulatory_stability" in assumptions
    assert "missing_regulatory_status" in unknowns or "missing_legal_review" in unknowns


def test_legacy_evidence_gets_deterministic_fallback_refs() -> None:
    legacy = {
        "title": "Legacy market note",
        "source_name": "Archive",
        "source_url": "https://archive.example/note",
        "retrieved_at": "2026-06-30T00:00:00",
        "summary": "Market volatility and repricing.",
    }

    first = build_decision_readiness_map(decision_question="Should we review investment market exposure?", evidence_items=[legacy])
    second = build_decision_readiness_map(decision_question="Should we review investment market exposure?", evidence_items=[dict(legacy)])
    first_ref = first["risk_coverage"][0]["risks"][0]["evidence_refs"][0]
    second_ref = second["risk_coverage"][0]["risks"][0]["evidence_refs"][0]

    assert first_ref["evidence_id"] == second_ref["evidence_id"]
    assert first_ref["evidence_id"].startswith("evref_")


def test_project_decision_readiness_api_is_read_only(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    project = create_project("Readiness Workspace")
    project["questions"] = [{"question_id": "q1", "question": "Should we review export control licensing?"}]
    project["evidence_library"] = [_evidence(evidence_id="ev1")]
    project_workspace.save_project(project)
    path = project_workspace.PROJECTS_DIR / f"{project['project_id']}.json"
    before = json.loads(path.read_text(encoding="utf-8"))

    response = TestClient(app).get(f"/projects/{project['project_id']}/decision/readiness")
    after = json.loads(path.read_text(encoding="utf-8"))

    assert response.status_code == 200
    payload = response.json()
    assert payload["decision_question"] == "Should we review export control licensing?"
    assert payload["readiness_summary"]["evidence_count"] == 1
    assert after == before


def test_empty_project_endpoint_returns_limited_state(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    project = create_project("Empty Readiness Workspace")

    response = TestClient(app).get(f"/projects/{project['project_id']}/decision/readiness")

    assert response.status_code == 200
    payload = response.json()
    assert payload["readiness_summary"]["readiness_state"] == "not_ready_insufficient_evidence"
    assert payload["decision_question"] == ""
