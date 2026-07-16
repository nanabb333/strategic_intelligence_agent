# System Architecture

Strategic Intelligence Agent V2 keeps the deterministic V1 pipeline and adds an
Analyst Workbench interface.

## Components

- `dashboard/`: static browser workbench for paste, upload, analysis display,
  evidence review, and brief export.
- `src/`: deterministic Python workflow for repository-grade brief generation.
- `knowledge_base/`: historical analogue records and current-context entries.
- `examples/`: input documents for repeatable demos.
- `outputs/` and `demo_outputs/`: generated Markdown briefs.
- `scripts/`: validation scripts for V0.5, V1.0, and V2.

## Product Boundary

The system supports strategic analysis. It does not forecast outcomes, estimate
probabilities, or produce investment recommendations.

