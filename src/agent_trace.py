"""Agent trace artifact construction."""

from __future__ import annotations

from typing import Any

from serialization import serializable


def build_agent_trace(route: Any) -> dict[str, Any]:
    return {
        "selected_tools": route.selected_tools,
        "skipped_tools": route.skipped_tools,
        "trace": serializable(route.trace),
        "reasoning_record": serializable(route.reasoning_record),
        "reasoning_stages": [
            "Current event context extraction",
            "Event-family understanding",
            "Historical analogue retrieval",
            "Historical outcome retrieval",
            "Strategic assessment generation",
            "Strategic lesson generation",
            "Evidence credibility assessment",
            "Response playbook retrieval",
            "Executive brief generation",
        ],
    }
