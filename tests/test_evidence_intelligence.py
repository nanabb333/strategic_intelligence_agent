import json

from fastapi.testclient import TestClient

from app import app
from evidence_intelligence import (
    analyze_coverage,
    analyze_evidence_relationships,
    analyze_freshness,
    analyze_novelty,
    build_evidence_intelligence,
    classify_decision_risk_evidence,
    detect_duplicate_groups,
    evidence_reference,
    flag_regulatory_constraints,
    generate_historical_pathway_signals,
    reviewer_attention_queue,
    summarize_evidence_set,
)
import project_workspace
from project_workspace import create_project


def _item(**overrides):
    base = {
        "evidence_id": "ev_base",
        "title": "Official export controls update",
        "source_type": "Government / regulator",
        "source_name": "Commerce Department",
        "source_url": "https://agency.gov/update",
        "published_at": "2026-06-30",
        "retrieved_at": "2026-06-30T10:00:00",
        "excerpt": "The United States approved a licensing process for advanced semiconductor exports.",
        "summary": "Official licensing update.",
        "credibility_tier": "Tier 1 Official",
        "validation_status": "Valid",
        "validation_notes": [],
        "conflict_status": "No Conflict",
        "status": "Retrieved",
        "reviewer_status": "retrieved",
    }
    base.update(overrides)
    return base


def test_evidence_set_summary_counts_attention_and_metadata() -> None:
    items = [
        _item(evidence_id="ev1"),
        _item(
            evidence_id="ev2",
            source_type="Blog",
            source_name="Independent Blog",
            source_url="",
            published_at="",
            credibility_tier="Tier 5 Other",
            validation_status="Weak Metadata",
        ),
    ]
    attention = reviewer_attention_queue(items)
    summary = summarize_evidence_set(items, attention)

    assert summary["total_evidence_count"] == 2
    assert summary["source_type_counts"]["Government / regulator"] == 1
    assert summary["credibility_tier_counts"]["Tier 5 Other"] == 1
    assert summary["validation_status_counts"]["Weak Metadata"] == 1
    assert summary["attention_items"]


def test_duplicate_url_and_title_detection() -> None:
    items = [
        _item(evidence_id="ev1", source_url="https://agency.gov/update", title="Policy Update"),
        _item(evidence_id="ev2", source_url="https://agency.gov/update/", title="Different Title"),
        _item(evidence_id="ev3", source_url="https://agency.gov/other", title="Policy Update"),
    ]

    groups = detect_duplicate_groups(items)

    reasons = {group["duplicate_reason"] for group in groups}
    assert "same URL" in reasons
    assert "same normalized title" in reasons


def test_similar_excerpt_detection() -> None:
    items = [
        _item(
            evidence_id="ev1",
            source_url="https://agency.gov/one",
            title="First",
            excerpt="Official agency announced advanced semiconductor export licensing requirements today.",
        ),
        _item(
            evidence_id="ev2",
            source_url="https://agency.gov/two",
            title="Second",
            excerpt="Agency announced advanced semiconductor export licensing requirements today for companies.",
        ),
    ]

    groups = detect_duplicate_groups(items)

    assert any("similar excerpt overlap" in group["duplicate_reason"] for group in groups)


def test_support_and_potential_conflict_heuristics() -> None:
    support_items = [
        _item(evidence_id="ev1", source_url="https://agency.gov/a", published_at="2026-06-30"),
        _item(
            evidence_id="ev2",
            source_url="https://agency.gov/b",
            published_at="2026-06-29",
            excerpt="Official regulator approved a licensing process for advanced semiconductor exports.",
        ),
    ]
    conflict_items = [
        _item(evidence_id="ev3", excerpt="The regulator approved the export license."),
        _item(evidence_id="ev4", source_url="https://news.example/conflict", excerpt="The license was blocked and not confirmed."),
    ]

    support = analyze_evidence_relationships(support_items)
    conflict = analyze_evidence_relationships(conflict_items)

    assert support[0]["relationship"] == "supports"
    assert conflict[0]["relationship"] == "potential_conflict"
    assert conflict[0]["rationale"]


def test_novelty_scoring_detects_new_source_date_category_keywords_geography_actor() -> None:
    items = [
        _item(evidence_id="ev1"),
        _item(
            evidence_id="ev2",
            source_url="https://company.example/ir",
            source_name="Acme Investor Relations",
            source_type="Company press release",
            published_at="2026-07-01",
            excerpt="Acme described China revenue exposure and new compliance controls.",
        ),
    ]

    novelty = analyze_novelty(items)

    assert novelty[1]["novelty_score"] > 0
    assert "new source" in novelty[1]["novelty_reasons"]
    assert "new source type" in novelty[1]["novelty_reasons"]
    assert "new geography" in novelty[1]["novelty_reasons"]


def test_source_coverage_and_missing_categories() -> None:
    coverage = analyze_coverage(
        [
            _item(evidence_id="ev1"),
            _item(evidence_id="ev2", source_type="Company press release", source_name="Investor Relations"),
        ]
    )

    assert "official_government" in coverage["covered_categories"]
    assert "company_ir" in coverage["covered_categories"]
    assert "academic" in coverage["missing_categories"]
    assert coverage["coverage_score"] > 0
    assert coverage["reviewer_recommendation"]


def test_freshness_and_attention_queue() -> None:
    items = [
        _item(evidence_id="current", published_at="2026-06-30", retrieved_at="2026-06-30T10:00:00"),
        _item(evidence_id="stale", published_at="2020-01-01", retrieved_at="2026-06-30T10:00:00"),
        _item(evidence_id="missing", published_at="", source_url="", excerpt="", validation_status="Weak Metadata"),
    ]

    freshness = analyze_freshness(items)
    attention = reviewer_attention_queue(items, freshness=freshness)

    assert freshness["current_items"] == ["current"]
    assert freshness["stale_items"] == ["stale"]
    assert freshness["missing_date_items"] == ["missing"]
    assert any(entry["evidence_id"] == "stale" and "stale evidence" in entry["reasons"] for entry in attention)
    assert any(entry["evidence_id"] == "missing" and "empty excerpt" in entry["reasons"] for entry in attention)


def test_build_evidence_intelligence_handles_old_evidence_records() -> None:
    intelligence = build_evidence_intelligence(
        [
            {
                "evidence_id": "old1",
                "title": "Legacy note",
                "source_type": "Manual note",
                "summary": "Legacy evidence summary.",
            }
        ]
    )

    assert intelligence["summary"]["total_evidence_count"] == 1
    assert intelligence["coverage"]["covered_categories"] == ["unknown"]
    assert intelligence["attention_items"][0]["evidence_id"] == "old1"


def test_stable_evidence_reference_generation_for_legacy_records() -> None:
    item = {
        "title": "Legacy regulatory note",
        "source_name": "Agency Archive",
        "source_url": "https://agency.gov/archive",
        "retrieved_at": "2026-06-30T10:00:00",
    }

    first = evidence_reference(item)
    second = evidence_reference(dict(item))

    assert first == second
    assert first["evidence_id"].startswith("evref_")
    assert first["title"] == "Legacy regulatory note"
    assert first["source"] == "Agency Archive"


def test_duplicate_and_relationship_signals_include_evidence_refs() -> None:
    items = [
        _item(evidence_id="ev1", source_url="https://agency.gov/a", title="Policy Update"),
        _item(evidence_id="ev2", source_url="https://agency.gov/a/", title="Different Policy Update"),
        _item(evidence_id="ev3", source_url="https://news.example/conflict", excerpt="The license was blocked and not confirmed."),
    ]

    intelligence = build_evidence_intelligence(items)

    assert intelligence["duplicate_groups"][0]["evidence_refs"][0]["evidence_id"] == "ev1"
    conflict = [item for item in intelligence["relationships"] if item["relationship"] == "potential_conflict"]
    assert conflict
    assert conflict[0]["evidence_refs"][0]["title"]
    assert any(signal["evidence_refs"] for signal in intelligence["traceable_signals"])


def test_decision_risk_evidence_classification_covers_required_categories() -> None:
    items = [
        _item(
            evidence_id="market",
            title="Market repricing and demand shock",
            excerpt="Market volatility and demand shock created financial margin pressure and earnings revision risk.",
        ),
        _item(
            evidence_id="regulatory",
            title="Regulatory approval and legal review",
            excerpt="Regulatory approval, licensing, legal compliance, SEC disclosure, and 10-K reporting were highlighted.",
        ),
        _item(
            evidence_id="controls",
            title="Sanctions and competition review",
            excerpt="Sanctions, export controls, entity list restrictions, antitrust competition review, and supply chain supplier shifts were cited.",
        ),
        _item(
            evidence_id="geo",
            title="Geopolitical and security exposure",
            excerpt="Geopolitical conflict involving China and data privacy cybersecurity exposure created uncertainty.",
        ),
    ]

    categories = {signal["risk_category"] for signal in classify_decision_risk_evidence(items)}

    assert "market_risk" in categories
    assert "financial_risk" in categories
    assert "regulatory_risk" in categories
    assert "legal_compliance_risk" in categories
    assert "sanctions_export_control_risk" in categories
    assert "antitrust_competition_risk" in categories
    assert "supply_chain_risk" in categories
    assert "geopolitical_risk" in categories


def test_regulatory_constraint_flagging_uses_cautious_review_language() -> None:
    flags = flag_regulatory_constraints(
        [
            _item(
                evidence_id="ev_reg",
                excerpt="The SEC disclosure, sanctions export control license, antitrust review, and data privacy issues remain pending.",
            )
        ]
    )

    categories = {flag["constraint_category"] for flag in flags}

    assert "securities_disclosure" in categories
    assert "sanctions_export_controls" in categories
    assert "antitrust_competition" in categories
    assert "data_privacy" in categories
    assert all("Not legal advice" in flag["reviewer_note"] for flag in flags)
    assert all("May require legal / compliance review" in flag["reviewer_note"] for flag in flags)


def test_historical_pathway_signal_generation_without_probabilities() -> None:
    items = [
        _item(
            evidence_id="ev_path",
            excerpt="Regulatory investigation escalation, market repricing, supplier shift, and delayed pending resolution were reported.",
        )
    ]
    risks = classify_decision_risk_evidence(items)

    pathways = generate_historical_pathway_signals(items, risks)
    families = {pathway["pathway_family"] for pathway in pathways}

    assert "regulatory_escalation" in families
    assert "market_repricing" in families
    assert "supply_chain_reconfiguration" in families
    assert "delayed_resolution" in families
    assert all("probability" in pathway["limitation_note"].lower() for pathway in pathways)


def test_sparse_evidence_risk_signal_has_limitation_note() -> None:
    signals = classify_decision_risk_evidence([_item(evidence_id="ev_sparse", excerpt="Unverified remains.")])

    uncertainty = next(signal for signal in signals if signal["risk_category"] == "uncertainty_unknowns")

    assert uncertainty["confidence_bucket"] == "low"
    assert "sparse evidence" in uncertainty["limitation_note"]


def test_read_only_project_evidence_intelligence_api_does_not_mutate_project(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    project = create_project("Evidence Intelligence Workspace")
    project["evidence_library"] = [
        _item(evidence_id="ev1"),
        _item(evidence_id="ev2", source_url="https://agency.gov/update/", title="Official export controls update"),
    ]
    project_workspace.save_project(project)
    project_path = project_workspace.PROJECTS_DIR / f"{project['project_id']}.json"
    before = json.loads(project_path.read_text(encoding="utf-8"))

    response = TestClient(app).get(f"/projects/{project['project_id']}/evidence/intelligence")
    after = json.loads(project_path.read_text(encoding="utf-8"))

    assert response.status_code == 200
    payload = response.json()
    assert payload["summary"]["total_evidence_count"] == 2
    assert payload["duplicate_groups"]
    assert after == before
