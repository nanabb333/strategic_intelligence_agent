"""Current context retrieval for Strategic Intelligence Agent."""

from dataclasses import dataclass

from scenario_classifier import ScenarioClassification


@dataclass
class CurrentContext:
    """Current context relevant to a classified issue."""

    issue_title: str
    summary: str
    sources: list[str]


def retrieve_current_context(
    classifications: list[ScenarioClassification],
) -> list[CurrentContext]:
    """Retrieve current context for each classified issue.

    V0.1 accepts the document as the main source of context. Future versions can
    integrate approved search, database, or internal knowledge tools.
    """
    return [
        CurrentContext(
            issue_title=classification.issue_title,
            summary="Current context retrieval is not yet connected.",
            sources=[],
        )
        for classification in classifications
    ]

