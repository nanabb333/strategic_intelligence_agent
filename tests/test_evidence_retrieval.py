from evidence_retrieval import (
    ExistingRetrievedEvidenceProvider,
    LocalDocumentEvidenceProvider,
    ManualEvidenceProvider,
    confidence_impact_metadata,
    evidence_rank_score,
    historical_live_evidence_guidance,
    missing_evidence_flags,
    normalize_evidence_item,
    normalize_evidence_items,
    rank_evidence_items,
    retrieve_evidence,
)


def test_evidence_item_normalization_preserves_traceable_schema() -> None:
    item = normalize_evidence_item(
        {
            "title": "Official release",
            "source_type": "Government / regulator",
            "source_name": "SEC",
            "source_url": "https://www.sec.gov/news",
            "published_at": "2026-06-30",
            "excerpt": "A current official release describes a new rule.",
            "status": "Retrieved",
        },
        query="official rule",
        retrieved_at="2026-06-30T10:00:00",
    )

    assert item.evidence_id.startswith("ev_")
    assert item.trace_id.startswith("trace_")
    assert item.credibility_tier == "Tier 1 Official"
    assert item.credibility_score == 1.0
    assert item.relevance_score > 0
    assert item.validation_status == "Valid"
    assert item.conflict_status == "No Conflict"


def test_validation_flags_missing_and_unsupported_metadata() -> None:
    item = normalize_evidence_item(
        {
            "source_type": "Unclassified memo",
            "summary": "",
        },
        query="market access",
        retrieved_at="2026-06-30T10:00:00",
    )

    assert item.validation_status == "Weak Metadata"
    assert "Missing source name or URL." in item.validation_notes
    assert "Missing published date." in item.validation_notes
    assert "Missing or empty excerpt." in item.validation_notes
    assert "Unsupported or unclassified source type." in item.validation_notes


def test_duplicate_title_and_url_are_marked_deterministically() -> None:
    items = normalize_evidence_items(
        [
            {
                "title": "Company update",
                "source_type": "Company press release",
                "source_name": "Investor Relations",
                "source_url": "https://example.com/update",
                "published_at": "2026-06-30",
                "excerpt": "First update.",
            },
            {
                "title": "Company update",
                "source_type": "Company press release",
                "source_name": "Investor Relations",
                "source_url": "https://example.com/update",
                "published_at": "2026-06-30",
                "excerpt": "Second update.",
            },
        ],
        query="company update",
        retrieved_at="2026-06-30T10:00:00",
    )

    assert items[0].validation_status == "Valid"
    assert items[1].validation_status == "Duplicate"
    assert "Duplicate source URL." in items[1].validation_notes
    assert "Duplicate title." in items[1].validation_notes


def test_ranking_is_deterministic_and_rewards_accepted_high_quality_evidence() -> None:
    weak = normalize_evidence_item(
        {
            "title": "Blog commentary",
            "source_type": "Blog",
            "source_name": "Independent Blog",
            "published_at": "2022-01-01",
            "excerpt": "Commentary about the topic.",
            "status": "Retrieved",
        },
        query="official topic",
        retrieved_at="2026-06-30T10:00:00",
    )
    strong = normalize_evidence_item(
        {
            "title": "Official topic release",
            "source_type": "Government / regulator",
            "source_name": "Official Government Release",
            "source_url": "https://agency.gov/release",
            "published_at": "2026-06-30",
            "excerpt": "Official topic release text.",
            "status": "Accepted",
        },
        query="official topic",
        retrieved_at="2026-06-30T10:00:00",
    )

    ranked = rank_evidence_items([weak, strong])

    assert ranked[0].title == "Official topic release"
    assert evidence_rank_score(ranked[0]) > evidence_rank_score(ranked[1])
    assert [item.title for item in rank_evidence_items([weak, strong])] == [item.title for item in ranked]


def test_missing_evidence_and_confidence_impact_metadata() -> None:
    weak = normalize_evidence_item(
        {"title": "Unverified note", "source_type": "Manual note", "excerpt": "A note."},
        query="note",
        retrieved_at="2026-06-30T10:00:00",
    )

    flags = missing_evidence_flags([weak])
    impact = confidence_impact_metadata([weak])

    assert "No Tier 1 official evidence is present." in flags
    assert "No reviewer-accepted evidence is present." in flags
    assert weak.evidence_id in impact["confidence_reducers"]
    assert impact["missing_evidence"]


def test_provider_boundary_requires_user_triggered_call_only() -> None:
    provider = ExistingRetrievedEvidenceProvider()
    response = retrieve_evidence(
        query="licensing update",
        provider=provider,
    )

    assert response["items"]
    assert provider.provider_name == "existing_local_candidates"
    assert all(item["status"] == "Retrieved" for item in response["items"])


def test_manual_and_local_document_providers_normalize_without_external_calls() -> None:
    manual = ManualEvidenceProvider(
        [
            {
                "title": "Reviewer note",
                "source_type": "Manual note",
                "excerpt": "Reviewer supplied evidence.",
                "status": "Accepted",
            }
        ]
    )
    document = LocalDocumentEvidenceProvider("Uploaded memo", "Memo text about a decision context.")

    manual_items = normalize_evidence_items(manual.retrieve("", retrieved_at="2026-06-30T10:00:00"))
    document_items = normalize_evidence_items(document.retrieve("", retrieved_at="2026-06-30T10:00:00"))

    assert manual_items[0].status == "Accepted"
    assert document_items[0].source_name == "Local document"


def test_historical_live_evidence_guidance_preserves_boundaries() -> None:
    guidance = historical_live_evidence_guidance()

    assert "Historical analogues remain structural context, not current factual proof." in guidance
    assert "Live evidence should not automatically override historical analogue patterns." in guidance
