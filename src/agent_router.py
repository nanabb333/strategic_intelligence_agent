"""Deterministic agent router for Strategic Intelligence Agent V3."""

from dataclasses import dataclass, field

from issue_extractor import ExtractedIssue, extract_issues
from scenario_classifier import ScenarioClassification, classify_scenarios
from tool_registry import ToolSpec


TOOL_ORDER = [
    "IssueExtractor",
    "ScenarioClassifier",
    "HistoricalRetriever",
    "ContextRetriever",
    "ImplicationAnalyzer",
    "BriefGenerator",
]


@dataclass
class ToolDecision:
    """Decision record for one tool."""

    tool: str
    decision: str
    why: str
    expected_contribution: str


@dataclass
class AgentTraceStep:
    """Human-readable agent trace step."""

    step: int
    event: str
    detail: str


@dataclass
class AgentRoute:
    """Agent routing result."""

    document_type: str
    scenario_type: str
    industries: list[str]
    actors: list[str]
    keywords: list[str]
    selected_tools: list[str]
    skipped_tools: list[str]
    reasoning_record: list[ToolDecision]
    trace: list[AgentTraceStep] = field(default_factory=list)


def _detect_keywords(text: str) -> list[str]:
    keywords = [
        "export control",
        "entity list",
        "license",
        "earnings",
        "guidance",
        "deposit",
        "supply chain",
        "shipping",
        "logistics",
        "industrial policy",
        "chips act",
        "sanctions",
        "regulatory",
        "compliance",
    ]
    lowered = text.lower()
    return [keyword for keyword in keywords if keyword in lowered]


def _should_run_context(
    issue: ExtractedIssue,
    classification: ScenarioClassification,
    keywords: list[str],
) -> tuple[bool, str, str]:
    scenario = classification.primary_scenario
    document_type = issue.document_type_guess
    if scenario == "Earnings / Corporate Disclosure" and not any(
        keyword in keywords for keyword in ["regulatory", "compliance", "supply chain", "export control", "sanctions"]
    ):
        return (
            False,
            "Corporate disclosure detected without strong policy, supply chain, sanctions, or regulatory context terms.",
            "Context retrieval is skipped to keep the route focused on disclosure interpretation.",
        )
    if scenario in {
        "Export Controls",
        "Industrial Policy",
        "Sanctions",
        "Supply Chain Disruption",
        "Regulatory Action",
        "Military / Security Shock",
        "Trade Policy",
    }:
        return (
            True,
            f"{scenario} usually benefits from domain context and monitoring considerations.",
            "Adds current context from the local knowledge base.",
        )
    if issue.industries and document_type != "General Strategic Note":
        return (
            True,
            "Structured industry signals and document type suggest context may help interpretation.",
            "Adds industry-specific context if available.",
        )
    return (
        False,
        "No strong context retrieval trigger detected.",
        "Avoids adding weak context findings.",
    )


def route_document(
    document_text: str,
    registry: dict[str, ToolSpec],
) -> AgentRoute:
    """Route a document to selected tools using deterministic metadata."""
    provisional_issues = extract_issues(document_text)
    provisional_classifications = classify_scenarios(provisional_issues)

    issue = provisional_issues[0] if provisional_issues else None
    classification = provisional_classifications[0] if provisional_classifications else None
    document_type = issue.document_type_guess if issue else "Unknown"
    scenario = classification.primary_scenario if classification else "Other"
    industries = issue.industries if issue else []
    actors = issue.actors if issue else []
    keywords = _detect_keywords(document_text)

    selected_tools = ["IssueExtractor", "ScenarioClassifier", "HistoricalRetriever"]
    skipped_tools: list[str] = []
    reasoning: list[ToolDecision] = [
        ToolDecision(
            tool="IssueExtractor",
            decision="Selected",
            why="Every route starts by converting source text into structured issue fields.",
            expected_contribution="Core issue, actors, industries, policy terms, and document type.",
        ),
        ToolDecision(
            tool="ScenarioClassifier",
            decision="Selected",
            why="Scenario classification is required before retrieval decisions can be interpreted.",
            expected_contribution="Primary scenario and matched keyword evidence.",
        ),
        ToolDecision(
            tool="HistoricalRetriever",
            decision="Selected",
            why=f"{scenario} benefits from comparison against historical precedents.",
            expected_contribution="Top analogue cases and similarity reasons from the historical database.",
        ),
    ]

    if issue and classification:
        run_context, why_context, context_contribution = _should_run_context(issue, classification, keywords)
    else:
        run_context = False
        why_context = "No issue metadata available for context routing."
        context_contribution = "Context retrieval skipped."

    if run_context and "ContextRetriever" in registry:
        selected_tools.append("ContextRetriever")
        reasoning.append(
            ToolDecision(
                tool="ContextRetriever",
                decision="Selected",
                why=why_context,
                expected_contribution=context_contribution,
            )
        )
    else:
        skipped_tools.append("ContextRetriever")
        reasoning.append(
            ToolDecision(
                tool="ContextRetriever",
                decision="Skipped",
                why=why_context,
                expected_contribution=context_contribution,
            )
        )

    selected_tools.extend(["ImplicationAnalyzer", "BriefGenerator"])
    reasoning.extend(
        [
            ToolDecision(
                tool="ImplicationAnalyzer",
                decision="Selected",
                why="Selected retrieval outputs need to be synthesized into analyst-facing considerations.",
                expected_contribution="Similarities, differences, business considerations, operational considerations, geopolitical considerations, and questions.",
            ),
            ToolDecision(
                tool="BriefGenerator",
                decision="Selected",
                why="The final deliverable is an executive intelligence brief.",
                expected_contribution="Markdown brief with evidence sources, trace, and analysis path.",
            ),
        ]
    )

    trace = [
        AgentTraceStep(1, "Scenario detected", scenario),
        AgentTraceStep(2, "Document type detected", document_type),
    ]
    step = 3
    for tool in TOOL_ORDER:
        decision = next((item for item in reasoning if item.tool == tool), None)
        if not decision:
            continue
        trace.append(AgentTraceStep(step, f"Tool {decision.decision.lower()}", f"{tool}: {decision.why}"))
        step += 1

    missing_registered_tools = [tool for tool in TOOL_ORDER if tool not in registry]
    skipped_tools.extend(tool for tool in missing_registered_tools if tool not in skipped_tools)

    return AgentRoute(
        document_type=document_type,
        scenario_type=scenario,
        industries=industries,
        actors=actors,
        keywords=keywords,
        selected_tools=[tool for tool in TOOL_ORDER if tool in selected_tools and tool in registry],
        skipped_tools=skipped_tools,
        reasoning_record=reasoning,
        trace=trace,
    )

