"""Deterministic routing for free-form user questions."""

from __future__ import annotations

from dataclasses import dataclass, field


QUESTION_INTENTS = {
    "Historical Comparison": ["history", "historical", "past", "resemble", "analogue", "analog", "similar"],
    "Mechanism Analysis": ["mechanism", "driver", "why", "cause", "operating", "forces"],
    "Decision Support": ["decision", "brief", "executive", "do with", "prepare", "action", "monitor next"],
    "Evidence Review": ["evidence", "confidence", "source", "missing", "limitations", "credible"],
    "Implication Analysis": ["mean", "matter", "implication", "impact", "risk", "so what", "affect"],
}


@dataclass
class QuestionRoute:
    """Intent classification for a user's free-form question."""

    question_text: str
    intent: str
    matched_keywords: list[str] = field(default_factory=list)
    response_focus: list[str] = field(default_factory=list)
    routing_note: str = ""


def route_question(question_text: str) -> QuestionRoute:
    """Classify a user question into a deterministic product intent."""
    text = (question_text or "").strip()
    lowered = text.lower()
    if not lowered:
        return QuestionRoute(
            question_text="What does this issue mean?",
            intent="Implication Analysis",
            matched_keywords=["default"],
            response_focus=["current event context", "scenario", "strategic lessons", "executive brief"],
            routing_note="Default question used because the user did not enter a question.",
        )

    best_intent = "Implication Analysis"
    best_matches: list[str] = []
    for intent, keywords in QUESTION_INTENTS.items():
        matches = [keyword for keyword in keywords if keyword in lowered]
        if len(matches) > len(best_matches):
            best_intent = intent
            best_matches = matches

    return QuestionRoute(
        question_text=text,
        intent=best_intent,
        matched_keywords=best_matches,
        response_focus=_focus_for_intent(best_intent),
        routing_note="Question intent is classified with deterministic keyword rules; no LLM routing is used.",
    )


def _focus_for_intent(intent: str) -> list[str]:
    focus = {
        "Historical Comparison": ["historical analogues", "historical outcomes", "strategic lessons"],
        "Mechanism Analysis": ["mechanisms", "scenario classification", "multi-lens analysis"],
        "Decision Support": ["executive brief", "decision considerations", "monitoring considerations"],
        "Evidence Review": ["evidence credibility", "source status", "limitations"],
        "Implication Analysis": ["current event context", "business considerations", "operational considerations"],
    }
    return focus.get(intent, focus["Implication Analysis"])
