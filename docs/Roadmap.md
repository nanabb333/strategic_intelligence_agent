# Roadmap

This roadmap defines a 12-month product evolution path for Strategic Intelligence Decision Companion. The priority is product maturity, not feature quantity.

The project should evolve as a Decision Intelligence Platform: more evidence-aware, more evaluable, more trustworthy, and more useful for human decision review. Future work should preserve the current repository stability and avoid broad infrastructure expansion unless a specific product need justifies it.

## Version 1.0 Status

### Objective

Version 1.0 is complete and portfolio-ready. It demonstrates a local FastAPI decision-support workspace with structured English outputs, historical analogues, evidence notes, run artifacts, and CI validation.

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

## Version 4: Decision Intelligence Workspace

### Objective

Version 4 should evolve the platform from a one-time analysis tool into a structured Decision Intelligence Workspace. The focus is project continuity, reusable evidence, traceability, and decision evolution while preserving deterministic reasoning.

### User Value

Users should be able to work on a decision over time. A Project should hold related Questions, evidence, generated briefs, decision history, and change records so the user can see how recommendations evolve as evidence changes.

### Engineering Scope

Potential Version 4 scope:

- Project Workspace model for long-running decision problems.
- Question records that generate independent, reproducible analyses.
- Evidence Bundle model that unifies uploaded documents, user notes, supplied URLs, project evidence, and optional retrieved evidence.
- Project Evidence Library for reusable source material.
- Stronger evidence traceability from recommendation to reasoning rule, analogue, evidence statement, and original source.
- Evidence status labels such as User Provided, Corroborated, Historical Only, Conflicting, Outdated, or Unavailable.
- Deterministic evidence ranking based on authority, freshness, specificity, corroboration, and question relevance.
- Conflict detection that lowers confidence and identifies what additional evidence is needed.
- Decision evolution records comparing previous recommendations, new evidence, what changed, and updated recommendations.
- Optional user-triggered live retrieval that supplements evidence bundles without autonomous browsing or monitoring.

### Portfolio Value

Version 4 would position the project as a long-term Decision Intelligence Platform rather than a single-run report generator. It would show mature product architecture for evidence reuse, traceability, human-in-the-loop workflows, and decision continuity.

### What Should Not Be Included

Version 4 should not introduce autonomous agents, autonomous web research, background monitoring, multi-agent orchestration, chat-first workflows, unbounded source crawling, or infrastructure that does not clearly improve decision quality, evidence quality, trust, traceability, or maintainability.

## Sequencing Principle

Each version should earn the next layer of complexity. Evidence quality should come before monitoring. Evaluation should come before broader claims. Continuous improvement should come before additional automation.

The roadmap should protect the product identity: a trusted decision-support platform for human reviewers, not an uncontrolled agentic system.
