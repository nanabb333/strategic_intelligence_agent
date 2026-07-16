# Agent Router Design

## Workflow vs Agent

Earlier versions used a deterministic workflow: every document moved through
the same core stages. V3 keeps the deterministic tools but adds an Agent Router
that decides which tools should run.

This is the key shift:

```text
Workflow: Document -> Fixed Tool Sequence -> Brief
Agent: Document -> Router -> Tool Selection -> Tool Execution -> Brief
```

## Why V3 Is Different From V2

V2 added the Analyst Workbench UI. The underlying analysis path was still
largely fixed.

V3 adds:

- `src/agent_router.py`.
- `src/tool_registry.py`.
- Selected tools.
- Skipped tools.
- Agent execution trace.
- Tool reasoning record.
- Analysis path in the brief.

## Tool Selection Logic

The router analyzes:

- Document type.
- Scenario type.
- Industries.
- Actors.
- Keywords.

Then it selects tools:

- `IssueExtractor`: always selected.
- `ScenarioClassifier`: always selected.
- `HistoricalRetriever`: selected when scenario comparison is useful.
- `ContextRetriever`: selected for policy, sanctions, supply chain, trade,
  security, regulatory, and industry-context routes; skipped for narrow
  corporate earnings routes when context is not relevant.
- `ImplicationAnalyzer`: selected after retrieval.
- `BriefGenerator`: selected for final output.

## Future Tool Extensibility

New tools can be added in `tool_registry.py` without rewriting the router. A
future version could register tools such as:

- SourceCitationRetriever.
- RiskControlChecklistGenerator.
- StakeholderMapper.
- TimelineExtractor.
- JSONArtifactExporter.

The router can then select those tools using the same deterministic decision
record pattern.

## Non-Goals

The Agent Router does not introduce forecasting, probabilities, investment
advice, or trading recommendations. Its job is orchestration and tool
selection, not prediction.

