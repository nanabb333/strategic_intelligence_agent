# V7 Historical Outcomes Engine

V7 adds a historical outcome and strategic lesson layer to the existing Strategic Intelligence Agent workflow. It does not add live web search, RAG infrastructure, LLM APIs, new agents, or forecasting.

## Workflow Upgrade

```text
Issue
-> Scenario
-> Mechanism
-> Historical Analogues
-> Historical Outcomes
-> Strategic Lessons
-> Playbooks
-> Executive Brief
```

## Historical Outcome Database

The database lives at `knowledge_base/historical_outcomes.csv`. It contains compact educational summaries of observed outcomes and strategic responses across export controls, sanctions, industrial policy, supply chain disruption, technology competition, and geopolitical escalation.

Fields include:

- `case_id`
- `case_name`
- `event_family`
- `year`
- `actor`
- `sector`
- `observed_outcome`
- `strategic_response`
- `time_horizon`
- `confidence`
- `source_status`

Source status is explicit. When evidence is incomplete or not linked to a primary source, the record says so rather than fabricating precision.

## Retrieval Design

`src/outcome_retriever.py` deterministically retrieves outcomes by comparing retrieved historical analogue case names and event families against the outcome database. The retriever returns observed consequences, strategic responses, time horizon, confidence, source status, and evidence references.

## Product Value

Historical analogues show what a current issue may resemble. Historical outcomes add what happened in those cases and what strategic responses appeared. This gives analysts a clearer bridge from comparison to decision-support discussion without making predictions.

## Limitations

- Outcome records are simplified educational summaries.
- Source URLs are not fabricated.
- Outcome retrieval is deterministic and keyword/family based.
- Historical outcomes do not imply that similar outcomes will occur again.
- Human expert review remains necessary for executive use.
