"""Deterministic scenario classification for Strategic Intelligence Agent."""

from dataclasses import dataclass

from issue_extractor import ExtractedIssue


SCENARIO_KEYWORDS = {
    "Export Controls": ["export control", "export controls", "entity list", "license", "licensing", "restricted access"],
    "Industrial Policy": ["chips act", "industrial policy", "subsidy", "subsidies", "domestic manufacturing"],
    "Sanctions": ["sanctions", "asset freeze", "restricted party", "embargo"],
    "Supply Chain Disruption": ["supply chain", "supplier", "shipping", "logistics", "shortage", "disruption", "rerouting"],
    "Regulatory Action": ["regulation", "regulatory", "compliance", "rule", "enforcement"],
    "Military / Security Shock": ["military", "security", "strait", "missile", "exercise", "conflict"],
    "Earnings / Corporate Disclosure": ["earnings", "guidance", "quarter", "margin", "revenue", "disclosure"],
    "Strategic Investment": ["investment", "capex", "facility", "plant", "joint venture", "partnership"],
    "Trade Policy": ["tariff", "tariffs", "trade", "customs", "import", "export ban"],
}


@dataclass
class ScenarioClassification:
    """Scenario type assigned to an extracted issue."""

    issue_title: str
    primary_scenario: str
    matched_keywords: list[str]
    confidence_label: str

    @property
    def scenario_type(self) -> str:
        """Backward-compatible alias for earlier V0.1 code."""
        return self.primary_scenario

    @property
    def rationale(self) -> str:
        """Explain classification without implying forecast probability."""
        if not self.matched_keywords:
            return "No strong keyword pattern matched; classified as Other."
        keywords = ", ".join(self.matched_keywords)
        return f"Matched deterministic keywords: {keywords}."


def _score_issue_text(text: str) -> tuple[str, list[str]]:
    lowered = text.lower()
    best_scenario = "Other"
    best_matches: list[str] = []
    for scenario, keywords in SCENARIO_KEYWORDS.items():
        matches = [keyword for keyword in keywords if keyword in lowered]
        if len(matches) > len(best_matches):
            best_scenario = scenario
            best_matches = matches
    return best_scenario, best_matches


def _confidence_label(match_count: int) -> str:
    if match_count >= 3:
        return "High"
    if match_count >= 1:
        return "Medium"
    return "Low"


def classify_scenarios(issues: list[ExtractedIssue]) -> list[ScenarioClassification]:
    """Classify extracted issues using deterministic keyword matching."""
    classifications: list[ScenarioClassification] = []
    for issue in issues:
        searchable_text = " ".join(
            [
                issue.title,
                issue.summary,
                issue.core_issue,
                " ".join(issue.policy_terms),
                " ".join(issue.industries),
                issue.document_type_guess,
            ]
        )
        scenario, matches = _score_issue_text(searchable_text)
        classifications.append(
            ScenarioClassification(
                issue_title=issue.title,
                primary_scenario=scenario,
                matched_keywords=matches,
                confidence_label=_confidence_label(len(matches)),
            )
        )
    return classifications
