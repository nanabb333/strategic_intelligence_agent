"""Validate Strategic Intelligence Agent V3 agent router."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agent_router import route_document  # noqa: E402
from document_loader import load_document  # noqa: E402
from tool_registry import build_default_registry  # noqa: E402
from run_agent import run_agent  # noqa: E402


ROUTING_CASES = {
    "examples/agent_export_controls.md": {
        "output": "outputs/agent_export_controls_brief.md",
        "scenario": "Export Controls",
        "selected": {"ContextRetriever", "HistoricalRetriever"},
        "skipped": set(),
    },
    "examples/agent_earnings.md": {
        "output": "outputs/agent_earnings_brief.md",
        "scenario": "Earnings / Corporate Disclosure",
        "selected": {"HistoricalRetriever"},
        "skipped": {"ContextRetriever"},
    },
    "examples/agent_supply_chain.md": {
        "output": "outputs/agent_supply_chain_brief.md",
        "scenario": "Supply Chain Disruption",
        "selected": {"ContextRetriever", "HistoricalRetriever"},
        "skipped": set(),
    },
    "examples/agent_industrial_policy.md": {
        "output": "outputs/agent_industrial_policy_brief.md",
        "scenario": "Industrial Policy",
        "selected": {"ContextRetriever", "HistoricalRetriever"},
        "skipped": set(),
    },
}


def validate_routing() -> None:
    registry = build_default_registry()
    for input_file, expected in ROUTING_CASES.items():
        text = load_document(ROOT / input_file)
        route = route_document(text, registry)
        if route.scenario_type != expected["scenario"]:
            raise AssertionError(f"{input_file} scenario {route.scenario_type} != {expected['scenario']}")
        if not expected["selected"].issubset(set(route.selected_tools)):
            raise AssertionError(f"{input_file} missing selected tools: {expected['selected']} from {route.selected_tools}")
        if not expected["skipped"].issubset(set(route.skipped_tools)):
            raise AssertionError(f"{input_file} missing skipped tools: {expected['skipped']} from {route.skipped_tools}")
        if not route.trace:
            raise AssertionError(f"{input_file} missing agent trace")
        if not route.reasoning_record:
            raise AssertionError(f"{input_file} missing reasoning record")


def validate_outputs() -> None:
    for input_file, expected in ROUTING_CASES.items():
        output_path = ROOT / expected["output"]
        run_agent(ROOT / input_file, output_path)
        text = output_path.read_text(encoding="utf-8")
        required_sections = [
            "## Agent Execution Trace",
            "## Tool Decisions",
            "## Evidence Sources",
            "## Analysis Path",
        ]
        for section in required_sections:
            if section not in text:
                raise AssertionError(f"{expected['output']} missing {section}")
        if "Agent Router" not in text or "Tool Registry" not in text:
            raise AssertionError(f"{expected['output']} missing router or registry evidence")


def main() -> None:
    validate_routing()
    validate_outputs()
    print("V3.0 validation passed.")


if __name__ == "__main__":
    main()

