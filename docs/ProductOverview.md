# Product Overview

Strategic Intelligence Agent is a local FastAPI intelligence app for turning messy source material into structured decision-support briefs. It is built for strategic analysis, not prediction.

## Product Purpose

The product helps a reviewer move from unstructured text to a clearer decision workspace:

```text
Source Material
  |
  v
Issue + Scenario
  |
  v
Decision Criteria
  |
  v
Options + Recommendation Logic
  |
  v
Historical Analogues + Outcomes
  |
  v
Strategic Lessons + Monitoring
  |
  v
Downloadable Artifacts
```

The goal is to make strategic review more consistent, explainable, and reusable.

## Target Users

- Analysts preparing executive or management briefings.
- Product managers and strategy teams reviewing policy, supply-chain, or market-access events.
- Business analytics stakeholders who need structured notes and JSON artifacts.
- Recruiters, admissions reviewers, and engineers evaluating the project as a portfolio artifact.

## Supported Input Modes

The current local app supports:

- Plain-language questions.
- Pasted article, policy, earnings, supply-chain, or memo text.
- Uploaded `.txt`, `.md`, `.markdown`, and text-based `.pdf` files.
- User-provided readable URLs when the backend can fetch and extract page text.

PDF extraction is text-based only. Scanned image PDFs are not supported.

## Supported Output Modes

The dashboard and pipeline support:

- Beginner, analyst, and executive output modes.
- English, Simplified Chinese, and Traditional Chinese output structure.
- Markdown, TXT, and JSON downloads.
- Run history and per-run artifacts under `outputs/runs/`.

## Strategic Intelligence Workflow

At a high level, the pipeline:

1. Prepares source text and metadata.
2. Extracts issue and entity information.
3. Classifies the scenario.
4. Identifies decision criteria and decision paths.
5. Retrieves historical analogues and outcomes from local curated records.
6. Generates strategic lessons and evidence notes.
7. Produces an executive brief and structured JSON artifact.
8. Stores run outputs for download and review.

## Product Value

The product is valuable because it does more than summarize. It gives the user a structured way to ask:

- What decision does this source material raise?
- What criteria should drive that decision?
- What options are available?
- Why is one option currently preferred?
- What historical cases resemble the situation?
- What evidence is strong, weak, or missing?
- What should be monitored next?

## Current Limitations

The current app is local and single-user. It does not provide:

- Live web monitoring.
- Autonomous internet research.
- Forecasts or probabilities.
- Investment, trading, legal, or compliance advice.
- Enterprise authentication or cloud deployment.
- OCR for scanned documents.
- Real-world accuracy guarantees.

All outputs require human review before any executive, legal, financial, operational, or geopolitical use.

## Related Documentation

- [README](../README.md)
- [Documentation Index](DocumentationIndex.md)
- [Repository Trust Audit](RepositoryTrustAudit.md)
- [Trust Model](TrustModel.md)
- [Demo Scenarios](DemoScenarios.md)
- [Engineering Architecture](EngineeringArchitecture.md)
- [Analysis Pipeline](Pipeline.md)
- [Testing](Testing.md)
