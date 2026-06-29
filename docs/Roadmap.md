# Roadmap

This roadmap defines a 12-month product evolution path for Strategic Intelligence Agent. The priority is product maturity, not feature quantity.

The project should evolve as a Decision Intelligence Platform: more evidence-aware, more evaluable, more trustworthy, and more useful for human decision review. Future work should preserve the current repository stability and avoid broad infrastructure expansion unless a specific product need justifies it.

## Version 1.0 Status

### Objective

Version 1.0 is complete and portfolio-ready. It demonstrates a local FastAPI decision-support workspace with structured outputs, historical analogues, evidence notes, localization support, run artifacts, and CI validation.

### User Value

Users can turn pasted text, supported files, or readable URLs into structured decision briefs. Reviewers can inspect the product, architecture, tests, artifacts, and documentation without relying on a deployed service.

### Engineering Scope

Version 1.0 includes:

- Thin FastAPI entrypoint.
- Separated service and pipeline layers.
- Deterministic intelligence modules.
- Local run storage.
- Markdown, TXT, JSON, trace, and metadata artifacts.
- Dashboard workflow.
- Ruff, compile, pytest, and GitHub Actions validation.

### Portfolio Value

Version 1.0 shows mature AI product thinking: bounded scope, clear limitations, reviewable artifacts, testable architecture, and a working local application.

### What Should Not Be Included

Version 1.0 should not expand into autonomous web research, production SaaS deployment, login systems, databases, multi-agent orchestration, or advice-oriented claims.

## Version 2: Evidence, Evaluation, And Decision Quality

### Objective

Version 2 should improve the quality and inspectability of decision-support outputs. The focus should be evidence handling, evaluation depth, and clearer decision-quality signals.

### User Value

Users should better understand why a brief says what it says, how strong the supporting evidence is, and where human review is required. Reviewers should see a stronger connection between product claims and measurable evaluation criteria.

### Engineering Scope

Potential Version 2 scope:

- Initial Decision Case Schema, Evidence Ledger, and qualitative Confidence Assessment.
- More explicit evidence quality labels.
- Better limitation and uncertainty language.
- Expanded benchmark cases for decision-support quality.
- Golden output review fixtures for selected scenarios.
- Comparison tests against generic LLM-style summaries.
- Clearer scoring dimensions for analogue relevance, risk identification, option clarity, and overconfidence control.
- Documentation that ties evaluation outputs to product principles.

### Portfolio Value

Version 2 would show that the project is not only functional, but also accountable. It would demonstrate a serious approach to evaluating AI decision-support behavior.

### What Should Not Be Included

Version 2 should not include autonomous web monitoring, broad source crawling, multi-user infrastructure, production authentication, or new features that dilute evaluation work. It should not imply real-world accuracy guarantees.

## Version 3: Monitoring And Continuous Improvement

### Objective

Version 3 should add disciplined monitoring concepts and feedback loops without turning the product into an autonomous web agent.

### User Value

Users should receive clearer review triggers, monitoring questions, and change conditions that explain when a prior brief should be revisited. Teams should be able to learn from repeated analysis runs and documented failure modes.

### Engineering Scope

Potential Version 3 scope:

- Structured change triggers in output artifacts.
- Review-window metadata.
- Failure-mode logging for human reviewers.
- Simple comparison of current runs against prior local runs.
- Curated monitoring templates by scenario type.
- Lightweight feedback fields for reviewer notes.
- Documentation for continuous improvement practices.

### Portfolio Value

Version 3 would demonstrate product maturity beyond one-time analysis. It would show how an AI decision-support product can support ongoing review while preserving user control.

### What Should Not Be Included

Version 3 should not add unsupervised web surveillance, automatic alerts from uncontrolled external sources, background agents, databases without a clear need, or operational claims that exceed the local product.

## Version 4: Research-Grade Decision Intelligence

### Objective

Version 4 should move the platform toward research-grade evaluation and evidence discipline. The goal is stronger validation of decision-support quality, not broader automation.

### User Value

Users and reviewers should be able to understand the system's strengths, weaknesses, benchmark behavior, and failure modes with more confidence. The product should make it easier to compare outputs, evaluate reasoning quality, and maintain trust over time.

### Engineering Scope

Potential Version 4 scope:

- Larger curated benchmark corpus.
- Human review rubrics and adjudication notes.
- Scenario-specific evaluation dashboards or reports.
- Structured failure taxonomy.
- Versioned evaluation results.
- Deeper comparison against generic LLM outputs.
- More rigorous documentation of evidence provenance and limitations.

### Portfolio Value

Version 4 would position the project as a serious AI Decision Intelligence Platform prototype with defensible evaluation practices and long-term product architecture.

### What Should Not Be Included

Version 4 should not pursue feature volume for its own sake. It should avoid enterprise infrastructure, autonomous multi-agent research, production compliance claims, or domain-specific advice unless those capabilities are explicitly evaluated and bounded.

## Sequencing Principle

Each version should earn the next layer of complexity. Evidence quality should come before monitoring. Evaluation should come before broader claims. Continuous improvement should come before additional automation.

The roadmap should protect the product identity: a trusted decision-support platform for human reviewers, not an uncontrolled agentic system.
