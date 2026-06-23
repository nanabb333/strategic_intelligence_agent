# JSON Artifact Design

V6 creates `analysis.json` for each run so outputs are reviewable and reusable outside the dashboard.

## Top-Level Fields

```text
issue
scenario
mechanisms
analogues
historical_outcomes
strategic_lessons
evidence_credibility
current_context
implications
response_playbooks
lenses
evidence
agent_trace
evaluation_metadata
metadata
```

## Purpose

- `issue`: extracted document fields.
- `scenario`: deterministic scenario classification.
- `mechanisms`: detected strategic mechanisms.
- `analogues`: retrieved historical analogues.
- `historical_outcomes`: observed outcomes and responses tied to retrieved analogues.
- `strategic_lessons`: rule-based recurring lessons generated from retrieved outcomes.
- `evidence_credibility`: confidence distribution, source status distribution, limitations, and reviewer note.
- `current_context`: local context KB results.
- `implications`: synthesis from analogues and context.
- `response_playbooks`: observed historical response patterns.
- `lenses`: multi-lens interpretations.
- `evidence`: evidence assessment records.
- `agent_trace`: selected and skipped tools plus route trace.
- `evaluation_metadata`: reminder that run artifacts are local deterministic outputs, not real-world accuracy claims.
- `metadata`: run ID, language, output mode, question, timestamp, and artifact paths.

## Source Metadata

Historical analogues, mechanisms, and response playbooks include:

- `source_title`
- `source_type`
- `source_date`
- `source_url`
- `confidence_note`

When a source URL is unavailable, the value is `source pending`. URLs are not fabricated.
