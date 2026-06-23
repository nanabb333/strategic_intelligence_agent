"""Tool registry for Strategic Intelligence Agent."""

from dataclasses import dataclass
from typing import Callable

from brief_generator import generate_brief
from context_retriever import retrieve_current_context
from historical_retriever import retrieve_historical_analogues
from implication_analyzer import analyze_implications
from issue_extractor import extract_issues
from scenario_classifier import classify_scenarios


@dataclass(frozen=True)
class ToolSpec:
    """Registered tool metadata."""

    name: str
    callable: Callable
    description: str


def build_default_registry() -> dict[str, ToolSpec]:
    """Build the default deterministic tool registry.

    Future tools can be added here without changing router decision logic.
    """
    return {
        "IssueExtractor": ToolSpec(
            name="IssueExtractor",
            callable=extract_issues,
            description="Extract structured issue fields from input documents.",
        ),
        "ScenarioClassifier": ToolSpec(
            name="ScenarioClassifier",
            callable=classify_scenarios,
            description="Assign deterministic scenario classifications.",
        ),
        "HistoricalRetriever": ToolSpec(
            name="HistoricalRetriever",
            callable=retrieve_historical_analogues,
            description="Retrieve historical analogues from the local historical database.",
        ),
        "ContextRetriever": ToolSpec(
            name="ContextRetriever",
            callable=retrieve_current_context,
            description="Retrieve current context from local domain knowledge-base files.",
        ),
        "ImplicationAnalyzer": ToolSpec(
            name="ImplicationAnalyzer",
            callable=analyze_implications,
            description="Synthesize implications from extracted issues, analogues, and context.",
        ),
        "BriefGenerator": ToolSpec(
            name="BriefGenerator",
            callable=generate_brief,
            description="Generate an executive intelligence brief.",
        ),
    }

