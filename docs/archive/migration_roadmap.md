# Migration Roadmap

## Current State

The current checkout has no tracked application files. The conceptual starting
point is the prior `financial_rubric_agent` project:

```text
Document Input -> Rubric Scoring -> AI Writing
```

The target project is:

```text
Document -> Issue Extraction -> Scenario Classification
-> Historical Analogue Retrieval -> Current Context Retrieval
-> Implication Analysis -> Executive Intelligence Brief
```

## V0.1: Structural Migration

Goal: Establish the Strategic Intelligence Agent architecture without rewriting
the prior system wholesale.

Recommended changes:

- Create the target folder structure.
- Add module stubs for each workflow stage.
- Document the project brief, architecture, workflow, and positioning.
- Recover prior code if available and map reusable components to the new module
  boundaries.
- Add one local text input example and one generated brief example.

Success criteria:

- Repository clearly communicates the new project direction.
- A reader can understand the workflow from the docs alone.
- `src/run_agent.py` can execute a simple placeholder pipeline.

## V0.5: Functional Prototype

Goal: Build an end-to-end working analyst workflow.

Recommended changes:

- Implement document loading for `.txt` and Markdown.
- Add structured issue extraction output.
- Add rule-based or LLM-assisted scenario classification.
- Add a small curated historical analogue knowledge base.
- Generate a Markdown executive brief.
- Add basic tests for each module.

Success criteria:

- A sample input produces a complete brief in `outputs/`.
- Intermediate results are inspectable.
- The system remains clearly non-advisory and decision-support oriented.

## V1.0: Portfolio-Ready Agent

Goal: Deliver a polished, demonstrable AI portfolio project.

Recommended changes:

- Add retrieval over a richer historical analogue knowledge base.
- Add source citations or traceability for extracted claims.
- Add configurable LLM provider support.
- Add current context retrieval through approved sources.
- Add a CLI or lightweight UI.
- Add examples showing multiple scenario types.
- Add tests, linting, and a strong README.

Success criteria:

- The project can be cloned, configured, and run by a reviewer.
- The demo shows clear LLM application, agent design, tool use, orchestration,
  business analytics, and strategic intelligence.
- Outputs are useful to an analyst while avoiding trading or investment advice.

