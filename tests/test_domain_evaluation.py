import json

from fastapi.testclient import TestClient

from app import app
from domain_evaluation import build_domain_evaluation
import project_workspace
from project_workspace import create_project


def _evidence(**overrides):
    base = {
        "evidence_id": "ev_domain",
        "title": "Domain evidence",
        "source_type": "Major news",
        "source_name": "Reuters",
        "source_url": "https://news.example/domain",
        "published_at": "2026-06-30",
        "retrieved_at": "2026-06-30T10:00:00",
        "excerpt": "Domain evidence excerpt.",
        "summary": "Domain evidence summary.",
        "status": "Accepted",
    }
    base.update(overrides)
    return base


def _dimensions(result_set):
    return {
        dimension["dimension_id"]
        for result in result_set["results"]
        for dimension in result["evaluation_dimensions"]
        if dimension["status"] == "mapped"
    }


def test_fed_rate_hike_maps_macro_investment_and_refinancing_dimensions() -> None:
    result = build_domain_evaluation(
        decision_question="How should reviewers evaluate a Federal Reserve rate hike scenario for asset allocation?",
        evidence_items=[
            _evidence(
                evidence_id="macro",
                excerpt=(
                    "Federal Reserve rate hike and interest rate pressure create duration risk, "
                    "equity valuation risk, refinancing risk, credit spread widening, and liquidity tightening."
                ),
            )
        ],
    )
    dimensions = _dimensions(result)

    assert "interest_rate_sensitivity" in dimensions
    assert "duration_risk" in dimensions
    assert "equity_valuation_risk" in dimensions
    assert "refinancing_risk" in dimensions


def test_asset_allocation_evaluation_avoids_transaction_language() -> None:
    result = build_domain_evaluation(
        decision_question="Evaluate inflation shock and portfolio concentration exposure.",
        evidence_items=[_evidence(excerpt="Inflation shock, portfolio concentration, downside protection, and market sentiment matter.")],
    )
    payload = json.dumps(result).lower()

    assert "buy" not in payload
    assert "sell" not in payload
    assert "hold" not in payload
    assert "recommended allocation" not in payload


def test_credit_risk_evaluation_maps_core_credit_terms() -> None:
    result = build_domain_evaluation(
        decision_question="Evaluate credit risk for a leveraged borrower.",
        evidence_items=[
            _evidence(
                evidence_id="credit",
                excerpt="Debt leverage default downgrade liquidity refinancing covenant spread maturity wall and interest expense were cited.",
            )
        ],
    )
    dimensions = _dimensions(result)

    assert "leverage_risk" in dimensions
    assert "default_risk" in dimensions
    assert "liquidity_risk" in dimensions
    assert "refinancing_risk" in dimensions
    assert any(result_item["domain"] == "credit_risk" for result_item in result["results"])


def test_insurance_business_evaluation_maps_operating_and_capital_terms() -> None:
    result = build_domain_evaluation(
        decision_question="Evaluate insurance business performance and capital exposure.",
        evidence_items=[
            _evidence(
                evidence_id="insurance",
                excerpt="Claims premiums underwriting loss ratio combined ratio reserves reinsurance catastrophe solvency and capital requirement were disclosed.",
            )
        ],
    )
    dimensions = _dimensions(result)

    assert "loss_ratio" in dimensions
    assert "combined_ratio" in dimensions
    assert "reserve_adequacy" in dimensions
    assert "reinsurance_exposure" in dimensions
    assert "solvency_capital" in dimensions


def test_regulatory_suitability_flags_are_cautious_and_non_advisory() -> None:
    result = build_domain_evaluation(
        decision_question="Evaluate investment suitability and insurance regulation exposure.",
        evidence_items=[
            _evidence(
                evidence_id="regulatory",
                excerpt="Suitability, fiduciary duty, securities disclosure, insurance regulation, risk disclosure, and jurisdiction review were noted.",
            )
        ],
    )
    flags = [flag for item in result["results"] for flag in item["regulatory_suitability_flags"]]

    assert flags
    assert all("May require compliance review" in flag["explanation"] for flag in flags)
    assert all("verify jurisdiction and applicability" in flag["explanation"] for flag in flags)


def test_domain_evaluation_preserves_evidence_refs_and_missing_questions() -> None:
    result = build_domain_evaluation(
        decision_question="Evaluate credit risk.",
        evidence_items=[_evidence(evidence_id="ev_ref", excerpt="Debt and leverage were cited.")],
    )
    refs = [ref for item in result["results"] for ref in item["evidence_refs"]]
    questions = [question["question"] for question in result["reviewer_questions"]]

    assert refs
    assert refs[0]["evidence_id"] == "ev_ref"
    assert any("What evidence is needed" in question for question in questions)


def test_domain_evaluation_has_no_ranking_probability_or_recommendation_fields() -> None:
    result = build_domain_evaluation(
        decision_question="Evaluate insurance business.",
        evidence_items=[_evidence(excerpt="Claims and premiums were disclosed.")],
    )
    keys = _all_keys(result)

    assert "recommendation_score" not in keys
    assert "ranking" not in keys
    assert "best_option" not in keys
    assert "probability" not in keys


def test_domain_evaluation_endpoint_is_read_only(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    project = create_project("Domain Workspace")
    project["questions"] = [{"question_id": "q1", "question": "Evaluate credit risk."}]
    project["evidence_library"] = [_evidence(evidence_id="ev1", excerpt="Debt leverage default and liquidity were cited.")]
    project_workspace.save_project(project)
    path = project_workspace.PROJECTS_DIR / f"{project['project_id']}.json"
    before = json.loads(path.read_text(encoding="utf-8"))

    response = TestClient(app).get(f"/projects/{project['project_id']}/decision/domain-evaluation")
    after = json.loads(path.read_text(encoding="utf-8"))

    assert response.status_code == 200
    assert response.json()["results"]
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
