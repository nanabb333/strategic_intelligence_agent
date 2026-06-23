"""Generate multi-lens interpretations for strategic intelligence briefs."""

from dataclasses import dataclass, field

from context_retriever import CurrentContext
from historical_retriever import HistoricalAnalogue
from issue_extractor import ExtractedIssue
from mechanism_detector import Mechanism
from scenario_classifier import ScenarioClassification


SUPPORTED_LENSES = [
    "Economics",
    "Political Economy",
    "International Relations",
    "Legislative / Regulatory",
    "Business Strategy",
]


@dataclass
class LensInterpretation:
    """One interpretation of the same issue through one analytic lens."""

    issue_title: str
    lens: str
    hypothesis: str
    supporting_observations: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    evidence_references: list[str] = field(default_factory=list)


def analyze_lenses(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    mechanisms: dict[str, list[Mechanism]],
    analogues: dict[str, list[HistoricalAnalogue]],
    contexts: dict[str, list[CurrentContext]],
) -> dict[str, list[LensInterpretation]]:
    """Generate deterministic competing interpretations without claiming certainty."""
    classification_by_issue = {classification.issue_title: classification for classification in classifications}
    results: dict[str, list[LensInterpretation]] = {}

    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        scenario = classification.primary_scenario if classification else "Other"
        issue_mechanisms = mechanisms.get(issue.title, [])
        mechanism_names = ", ".join(item.mechanism_name for item in issue_mechanisms[:2]) or "the detected mechanisms"
        analogue_names = ", ".join(item.case_title for item in analogues.get(issue.title, [])[:2]) or "retrieved historical analogues"
        context_names = ", ".join(item.industry for item in contexts.get(issue.title, [])[:2]) or "retrieved context entries"

        base_evidence = ["Source Document"] + [item.evidence_trace for item in analogues.get(issue.title, [])[:2]]
        base_evidence += [item.evidence_trace for item in contexts.get(issue.title, [])[:2]]
        base_evidence += [f"{item.mechanism_name} (Mechanism Framework)" for item in issue_mechanisms[:2]]

        results[issue.title] = [
            LensInterpretation(
                issue_title=issue.title,
                lens="Economics",
                hypothesis=f"One possible interpretation is that the {scenario.lower()} event reflects resource allocation constraints linked to {mechanism_names}.",
                supporting_observations=[
                    f"The issue references {', '.join(issue.industries[:3]) or 'business operations'} and operating constraints.",
                    f"Historical analogues such as {analogue_names} show comparable economic adjustment patterns.",
                ],
                limitations=["The document does not quantify cost, demand, or capacity effects."],
                evidence_references=base_evidence,
            ),
            LensInterpretation(
                issue_title=issue.title,
                lens="Political Economy",
                hypothesis=f"One possible interpretation is that public authority and business incentives are interacting through {mechanism_names}.",
                supporting_observations=[
                    f"The scenario classification is {scenario}.",
                    f"Current context from {context_names} highlights stakeholders and monitoring considerations.",
                ],
                limitations=["The balance between public policy goals and firm-level incentives requires more source detail."],
                evidence_references=base_evidence,
            ),
            LensInterpretation(
                issue_title=issue.title,
                lens="International Relations",
                hypothesis=f"One possible interpretation is that the issue reflects cross-border strategic positioning rather than only firm-level operations.",
                supporting_observations=[
                    f"Detected regions include {', '.join(issue.countries_or_regions) or 'no explicit region in the source document'}.",
                    f"Mechanisms such as {mechanism_names} can appear in geopolitical or cross-border settings.",
                ],
                limitations=["The source does not establish intent by governments or counterparties."],
                evidence_references=base_evidence,
            ),
            LensInterpretation(
                issue_title=issue.title,
                lens="Legislative / Regulatory",
                hypothesis=f"One possible interpretation is that implementation rules and compliance obligations are central to the event.",
                supporting_observations=[
                    f"Detected policy terms include {', '.join(issue.policy_terms) or 'limited explicit policy terms'}.",
                    "The evidence trace includes source document signals and retrieved context records.",
                ],
                limitations=["Primary legal text or agency guidance would be needed for a complete regulatory reading."],
                evidence_references=base_evidence,
            ),
            LensInterpretation(
                issue_title=issue.title,
                lens="Business Strategy",
                hypothesis=f"One possible interpretation is that executives face a positioning and resilience question, not only a one-time event summary.",
                supporting_observations=[
                    f"The issue mentions actors such as {', '.join(issue.actors[:3]) or 'business stakeholders'}.",
                    "The brief combines analogue patterns with current context monitoring considerations.",
                ],
                limitations=["The source does not contain internal priorities, customer-level exposure, or implementation plans."],
                evidence_references=base_evidence,
            ),
        ]

    return results

