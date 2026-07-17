# Trust Model

This document explains when Strategic Intelligence Decision Companion should and should not be trusted.

## Trust Boundary

The project is a local decision-support app. It helps structure analysis, but it does not verify the real world.

Trust should be assigned to:

- The reproducibility of the local workflow.
- The visibility of generated artifacts.
- The deterministic nature of the current rules.
- The ability to inspect source files, regression fixtures, run metadata, and traces.

Trust should not be assigned to:

- Future outcomes.
- Legal, financial, investment, trading, or geopolitical correctness.
- Completeness of historical coverage.
- Live factual accuracy of user-provided URLs.
- Claims that are not traceable to input text, local knowledge files, or documented system behavior.

## What The System Can Explain

The repository exposes:

- Input text through `input.txt`.
- Run metadata through `metadata.json`.
- Structured analysis through `analysis.json`.
- Generated brief text through `brief.md` and `brief.txt`.
- Tool route information through `agent_trace.json`.
- Synthetic regression fixtures through `evaluation/benchmark_cases.csv`.
- Separate contract-validation component results through `evaluation/benchmark_results.csv`.

This makes the workflow inspectable, even though it is not a scientific proof of correctness.

## Evidence Categories

The system combines several evidence types:

- **Input document evidence:** source text supplied by the user.
- **Historical analogue evidence:** local curated cases in the knowledge base.
- **Historical outcome evidence:** simplified educational outcome records.
- **Context evidence:** local context notes, not live monitoring.
- **Heuristic evidence:** deterministic rules for routing, classification, and matching.
- **Generated interpretation:** decision-support synthesis built from the above.

## Human Review Requirement

Human review is required when outputs may affect:

- Business decisions.
- Legal or compliance interpretation.
- Financial analysis.
- Geopolitical analysis.
- Operational planning.
- Public communication.

The app can help organize review. It cannot replace expert judgment.

## Related Docs

- [Evidence Philosophy](EvidencePhilosophy.md)
- [Evaluation Methodology](EvaluationMethodology.md)
- [Evaluation Limitations](evaluation_limitations.md)
- [Engineering Architecture](EngineeringArchitecture.md)
