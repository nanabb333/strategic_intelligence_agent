"""English-only text helpers.

The product language is English. This module keeps the former localization
boundary in place so a future localization layer can return without changing
pipeline call sites.
"""

from __future__ import annotations


SUPPORTED_LANGUAGES = {"en"}


TEXT = {
    "en": {
        "medium": "Medium",
        "high": "High",
        "low": "Low",
        "source_document": "Source Document",
        "not_available": "Not available",
    },
}


QUESTION_INTENT_LABELS = {
    "Historical Comparison": "Historical Comparison",
    "Decision Support": "Decision Support",
    "Evidence Review": "Evidence Review",
    "Mechanism Analysis": "Mechanism Analysis",
    "Implication Analysis": "Implication Analysis",
    "Source Link Only": "Source Link Only",
}


def translate_text(text: str, language: str) -> str:
    """Return English text unchanged."""
    if language != "en":
        raise ValueError(f"Unsupported language: {language}")
    return text


def label(key: str, language: str) -> str:
    """Return an English UI or artifact label."""
    if language != "en":
        raise ValueError(f"Unsupported language: {language}")
    return TEXT["en"].get(key, key)


def localized_question_intent(intent: str, language: str) -> str:
    """Return an English question intent label."""
    if language != "en":
        raise ValueError(f"Unsupported language: {language}")
    return QUESTION_INTENT_LABELS.get(intent, intent)


def localized_question_route(route, language: str) -> dict[str, object]:
    """Serialize a question route with English labels."""
    if language != "en":
        raise ValueError(f"Unsupported language: {language}")
    intent = getattr(route, "intent", "")
    return {
        "intent": intent,
        "intent_label": localized_question_intent(intent, language),
        "confidence": getattr(route, "confidence", ""),
        "notes": list(getattr(route, "notes", []) or []),
    }
