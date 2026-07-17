from types import SimpleNamespace

from brief_generator import generate_brief


def test_registered_brief_generator_cannot_revive_ranked_option_output() -> None:
    issue = SimpleNamespace(title="Export-control review", core_issue="Which pathways should reviewers compare?")
    classification = SimpleNamespace(primary_scenario="Export Controls")

    brief = generate_brief(
        [issue],
        [classification],
        {},
        {},
        [],
    )

    assert "No pathway selected" in brief
    assert "Final judgment remains with the reviewer" in brief
    assert "Option B (Recommended)" not in brief
    assert "## Preferred Path" not in brief
    assert "## Option Ranking" not in brief
