"""Historical analogue retrieval for Strategic Intelligence Agent."""

from dataclasses import dataclass
from pathlib import Path

from scenario_classifier import ScenarioClassification


@dataclass
class HistoricalAnalogue:
    """A historical event or case with structural similarity to a scenario."""

    title: str
    relevance: str
    source: str | None = None


def retrieve_historical_analogues(
    classifications: list[ScenarioClassification],
    knowledge_base_dir: str | Path = "knowledge_base",
) -> dict[str, list[HistoricalAnalogue]]:
    """Retrieve historical analogues for each classified issue.

    V0.1 returns a placeholder result. Later versions should search curated
    records in `knowledge_base/`.
    """
    _ = Path(knowledge_base_dir)
    return {
        classification.issue_title: [
            HistoricalAnalogue(
                title="Placeholder historical analogue",
                relevance="Add curated analogues in knowledge_base/ during V0.5.",
            )
        ]
        for classification in classifications
    }

