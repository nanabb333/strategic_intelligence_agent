# Portfolio Review Guide

This guide helps technical and product reviewers evaluate Strategic Intelligence Decision Companion as a local, reviewer-first Enterprise Decision Intelligence Platform.

## Suggested Review Order

1. [README](../README.md): product, workflow, boundaries, and version status.
2. [Product Overview](ProductOverview.md): current product contract.
3. [Demo Walkthrough](DemoWalkthrough.md): three-minute artifact review.
4. [Architecture](architecture.md): canonical architecture overview.
5. [Engineering Architecture](EngineeringArchitecture.md): implementation details.
6. [Documentation Index](DocumentationIndex.md): current and historical navigation.
7. [Release Notes](releases/README.md): verified version story.

## Product Review

Confirm that the primary flow is clear:

```text
Decision Question
  -> Decision Context
  -> Supporting Evidence
  -> Decision Assessment
  -> Human Review
  -> Export
```

Project should appear only as a secondary persistent container. The product should not be presented as a chatbot, AI assistant, autonomous agent or researcher, monitoring or forecasting system, generic RAG demo, compliance automation system, advisor, preferred-option selector, or autonomous decision maker.

## Engineering Review

Inspect:

- FastAPI routes and service boundaries
- deterministic Python pipeline and modules
- local JSON project and run storage
- vanilla browser interface
- reviewable Markdown, TXT, JSON, trace, and metadata artifacts
- Ruff, compile, pytest, and JavaScript syntax checks in CI

The architecture is intentionally local and single-user. It does not include production authentication, multi-user access control, managed storage, cloud deployment, or a signed installer.

## Decision Intelligence Review

Evaluate whether the product:

- makes the Decision Question and reviewer-authored Decision Context explicit
- distinguishes Supporting Evidence from context and inference
- exposes assumptions, unknowns, gaps, and limitations
- supports pathway comparison without ranking or recommendation
- preserves reviewer notes, unresolved questions, timeline, and delta
- keeps outputs inspectable rather than requiring trust in an opaque answer

## Claims Review

Passing repository tests supports maintainability claims within their test scope. It does not prove production readiness, security, scalability, compliance, benchmark leadership, factual correctness, or future accuracy. Historical documents and demo artifacts may retain earlier terminology and should not override the current documents listed above.
