"""Deterministic current context retrieval for Strategic Intelligence Agent."""

from dataclasses import dataclass
from pathlib import Path
import re

from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification


@dataclass
class CurrentContext:
    """Current context finding retrieved from the local context knowledge base."""

    issue_title: str
    industry: str
    scenario_type: str
    context_summary: str
    why_it_matters: str
    stakeholders: str
    monitoring_considerations: str
    similarity_reason: str
    source_file: str
    evidence_trace: str

    @property
    def summary(self) -> str:
        """Backward-compatible summary alias."""
        return self.context_summary

    @property
    def sources(self) -> list[str]:
        """Backward-compatible sources alias."""
        return [self.evidence_trace]


def _tokenize(value: str) -> set[str]:
    stop_words = {"and", "the", "for", "with", "from", "that", "this", "into", "can", "may"}
    tokens: set[str] = set()
    for token in re.findall(r"[a-zA-Z][a-zA-Z0-9-]+", value.lower()):
        if len(token) < 3 or token in stop_words:
            continue
        tokens.add(token)
        if len(token) > 4 and token.endswith("s"):
            tokens.add(token[:-1])
    return tokens


def _parse_context_file(path: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("## Entry"):
            if current:
                entries.append(current)
            current = {"entry_id": line.replace("## Entry", "").strip(), "source_file": path.name}
            continue
        if ":" in line and current:
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip()

    if current:
        entries.append(current)
    return entries


def load_context_entries(
    context_dir: str | Path = "knowledge_base/current_context",
) -> list[dict[str, str]]:
    """Load current-context entries from Markdown KB files."""
    directory = Path(context_dir)
    if not directory.exists():
        raise FileNotFoundError(f"Current context directory not found: {directory}")

    entries: list[dict[str, str]] = []
    for path in sorted(directory.glob("*.md")):
        entries.extend(_parse_context_file(path))
    return entries


def _score_context_entry(
    issue: ExtractedIssue,
    classification: ScenarioClassification,
    entry: dict[str, str],
) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    entry_industry_tokens = _tokenize(entry.get("industry", ""))
    issue_industry_tokens = _tokenize(" ".join(issue.industries))
    industry_overlap = sorted(issue_industry_tokens & entry_industry_tokens)
    if industry_overlap:
        score += 6
        reasons.append(f"industry match: {', '.join(industry_overlap)}")

    if entry.get("scenario_type") == classification.primary_scenario:
        score += 8
        reasons.append(f"scenario match: {classification.primary_scenario}")

    issue_terms = _tokenize(
        " ".join(
            [
                issue.title,
                issue.summary,
                issue.core_issue,
                " ".join(issue.policy_terms),
                " ".join(issue.actors),
                " ".join(issue.companies),
                " ".join(classification.matched_keywords),
            ]
        )
    )
    entry_terms = _tokenize(
        " ".join(
            [
                entry.get("context_summary", ""),
                entry.get("why_it_matters", ""),
                entry.get("stakeholders", ""),
                entry.get("monitoring_considerations", ""),
            ]
        )
    )
    keyword_overlap = sorted(issue_terms & entry_terms)
    if keyword_overlap:
        score += min(6, len(keyword_overlap) * 2)
        reasons.append(f"keyword overlap: {', '.join(keyword_overlap[:4])}")

    return score, reasons


def retrieve_current_context(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    context_dir: str | Path = "knowledge_base/current_context",
    limit: int = 3,
) -> dict[str, list[CurrentContext]]:
    """Retrieve top current-context findings using deterministic scoring."""
    entries = load_context_entries(context_dir)
    issue_by_title = {issue.title: issue for issue in issues}
    results: dict[str, list[CurrentContext]] = {}

    for classification in classifications:
        issue = issue_by_title[classification.issue_title]
        scored_entries = []
        for entry in entries:
            score, reasons = _score_context_entry(issue, classification, entry)
            scored_entries.append((score, reasons, entry))

        top_entries = sorted(scored_entries, key=lambda item: item[0], reverse=True)[:limit]
        findings: list[CurrentContext] = []
        for _, reasons, entry in top_entries:
            source_file = entry.get("source_file", "current_context")
            entry_id = entry.get("entry_id", "unknown")
            evidence_trace = f"{entry.get('industry', 'Context')} Context KB: {entry_id} ({source_file})"
            findings.append(
                CurrentContext(
                    issue_title=issue.title,
                    industry=entry.get("industry", "Unknown"),
                    scenario_type=entry.get("scenario_type", "Other"),
                    context_summary=entry.get("context_summary", ""),
                    why_it_matters=entry.get("why_it_matters", ""),
                    stakeholders=entry.get("stakeholders", ""),
                    monitoring_considerations=entry.get("monitoring_considerations", ""),
                    similarity_reason="; ".join(reasons) if reasons else "general context relevance",
                    source_file=source_file,
                    evidence_trace=evidence_trace,
                )
            )
        results[issue.title] = findings

    return results
