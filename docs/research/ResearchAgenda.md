# Research Agenda

This document defines the long-term research direction for Strategic Intelligence Agent.

The current repository is a deterministic, auditable, reviewer-first strategic decision-support system with internal completeness and regression checks. The research agenda describes how future work could validate reviewer outcomes while preserving local execution, reviewable artifacts, transparent limitations, and human-controlled judgment.

This document does not claim scientific proof, benchmark superiority, or real-world decision accuracy.

## Motivation

Decision-support systems are useful only when their outputs can be inspected, challenged, revised, and improved. A polished artifact is not enough. Reviewers need to understand whether evidence is represented clearly, whether historical analogues are relevant, whether evidence-sufficiency language is appropriate, and whether pathway comparisons remain bounded by the available evidence.

Research validation matters because decision-support quality is broader than software correctness. A system can pass tests and still provide weak decision support if it hides uncertainty, overstates analogues, omits risks, or fails to expose assumptions.

## Research Philosophy

The research direction should follow these principles:

- Validate decision-support quality before expanding capability.
- Treat evidence visibility as a core research object.
- Keep historical analogues comparative, not predictive.
- Use human review where judgment cannot be reduced to deterministic checks.
- Separate product QA from research validation.
- Avoid metrics that imply more certainty than the evidence supports.
- Preserve inspectable artifacts so claims can be reviewed.

Research should make the platform more accountable, not more complex for its own sake.

## Why Decision Support Requires Validation

Decision-support systems operate under uncertainty. They combine source material, extracted observations, historical context, assumptions, risks, and pathway considerations. Each layer can fail in different ways.

Validation should ask whether the system:

- Frames the decision clearly.
- Uses evidence responsibly.
- Selects relevant historical analogues.
- Identifies risks and missing information.
- Keeps confidence language proportional to evidence quality.
- Explains what new evidence could change the assessment or a reviewer's selection.
- Supports human review rather than replacing it.

These questions are different from whether the application starts, routes requests, writes artifacts, or passes unit tests.

## Product Evaluation Vs. Academic Evaluation

Product evaluation checks whether the application is reliable, coherent, and useful for its intended workflow. It includes tests, deterministic quality checks, artifact review, and documentation audits.

Academic evaluation asks broader research questions that may require controlled studies, human labels, inter-reviewer agreement, baseline comparisons, or decision replay. It should be designed carefully before any claims are made.

This repository currently implements product QA and deterministic product-quality evaluation. It does not yet implement academic validation.

## Major Research Themes

### Evidence Representation

How should evidence, observations, inferences, assumptions, and pathway considerations be represented so reviewers can inspect the decision path?

### Historical Analogue Quality

How should analogue relevance be evaluated beyond keyword overlap or scenario similarity? What makes a historical case useful, misleading, or only partially transferable?

### Evidence Sufficiency and Appropriate Reliance

How can deterministic evidence sufficiency make missing information and limitations visible without implying calibrated probability or correctness?

### Decision Explainability

What explanations help reviewers understand how pathway considerations relate to criteria, evidence, assumptions, and trade-offs without selecting a preferred path?

### Human-AI Collaboration

How should analysts review, challenge, correct, and annotate decision-support outputs? Which parts of the workflow should remain human-led?

### Decision Auditability

How can generated briefs, JSON artifacts, evidence ledgers, evidence sufficiency assessments, and research outputs support retrospective review?

## Open Research Questions

- What evidence representation best helps reviewers distinguish observation, inference, assumption, and pathway consideration?
- How should historical analogue relevance be judged across different decision domains?
- What human-review rubric best identifies useful versus misleading analogues?
- How should evidence sufficiency tiers be evaluated against independent reviewer judgments without implying statistical probability?
- Which failure modes most often reduce decision-support quality?
- How should reviewer disagreement be captured and used?
- What baseline comparison is fair for a bounded Decision Intelligence platform?
- How can decision replay be designed without pretending to know what decision-makers should have done?
- What artifacts are most useful for auditing a past decision-support brief?
- How can localization quality be evaluated without reducing it to direct translation accuracy?
