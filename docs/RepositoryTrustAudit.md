# Repository Trust Audit

This audit reviews Strategic Intelligence Agent from four credibility perspectives: scientific, engineering, product, and user experience.

## Scientific Credibility

### Strengths

- The repository states that evaluation scores are internal deterministic benchmark scores, not real-world accuracy.
- Benchmark cases and results are stored in `evaluation/`.
- Evidence limitations are documented.
- The product avoids forecasting, probabilities, investment advice, legal advice, and trading recommendations.
- Historical analogues are presented as support, not proof.

### Weaknesses

- Current benchmark cases are compact synthetic / curated cases.
- There is no independent human-labeled evaluation set.
- There is no source-grounded factuality benchmark.
- Golden output fixtures are not yet implemented.

## Engineering Credibility

### Strengths

- FastAPI entrypoint is separated from the service and pipeline layers.
- CI runs compile, Ruff, and pytest.
- API smoke tests cover health, analyze, run lookup, and downloads.
- Runtime artifacts are structured and inspectable.

### Weaknesses

- The repository does not yet use pinned dependency versions.
- `src/` is not currently packaged as a formal import package.
- Some older milestone scripts and docs increase navigation complexity.

## Product Credibility

### Strengths

- README clearly states what the product supports and does not support.
- The app is positioned as decision support, not prediction.
- Product docs explain target users, demo scenarios, and limitations.
- Downloadable artifacts make outputs reusable.

### Weaknesses

- The product is local-only and not packaged as a normal desktop app.
- Public reviewers may need guidance to distinguish current docs from older milestone docs.
- Demo screenshots are static SVG assets, not generated during validation.

## UX Credibility

### Strengths

- Dashboard supports a straightforward paste/upload/analyze/download flow.
- Results expose evidence sources and method details.
- Beginner, analyst, and executive modes support different reviewer needs.
- A trust note now appears in the input panel.

### Weaknesses

- The dashboard still contains many expandable sections, which can feel dense.
- Evaluation information is static in the dashboard and should be understood as a snapshot, not live scoring.
- The product does not yet include an in-app guided reviewer walkthrough.

## Overall Trust Assessment

The repository is credible as a local strategic-intelligence product and portfolio artifact. It is not yet credible as a scientifically validated AI system or production SaaS product. The strongest trust signals are transparency, reproducibility, artifact generation, CI, tests, and honest scope limits.

## Recommended Trust Roadmap

1. Add formal golden output fixtures for representative cases.
2. Add human-labeled benchmark cases.
3. Add source-grounded factuality checks.
4. Archive older milestone docs behind a clearer documentation history page.
5. Add a reviewer walkthrough that connects one input to `analysis.json`, `brief.md`, `agent_trace.json`, and benchmark limitations.
6. Choose a license before promoting the repository as open source.

## Related Docs

- [Trust Model](TrustModel.md)
- [Evidence Philosophy](EvidencePhilosophy.md)
- [Evaluation Methodology](EvaluationMethodology.md)
- [Golden Output Philosophy](GoldenOutputPhilosophy.md)
- [Documentation Index](DocumentationIndex.md)
