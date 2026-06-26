from dataclasses import dataclass
from types import SimpleNamespace

from agent_trace import build_agent_trace


@dataclass
class TraceStep:
    step: int
    event: str


def test_build_agent_trace_preserves_trace_shape() -> None:
    route = SimpleNamespace(
        selected_tools=["IssueExtractor"],
        skipped_tools=["ContextRetriever"],
        trace=[TraceStep(1, "start")],
        reasoning_record=[{"tool": "IssueExtractor", "decision": "use"}],
    )

    trace = build_agent_trace(route)

    assert trace["selected_tools"] == ["IssueExtractor"]
    assert trace["skipped_tools"] == ["ContextRetriever"]
    assert trace["trace"] == [{"step": 1, "event": "start"}]
    assert trace["reasoning_record"] == [{"tool": "IssueExtractor", "decision": "use"}]
    assert trace["reasoning_stages"] == [
        "Current event context extraction",
        "Event-family understanding",
        "Historical analogue retrieval",
        "Historical outcome retrieval",
        "Strategic assessment generation",
        "Strategic lesson generation",
        "Evidence credibility assessment",
        "Response playbook retrieval",
        "Executive brief generation",
    ]
