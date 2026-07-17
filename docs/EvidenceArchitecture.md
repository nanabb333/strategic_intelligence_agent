# Evidence Architecture

> Historical V2 design note: recommendation and qualitative-confidence language below documents the earlier artifact contract. Current runs use neutral pathways, reviewer-owned selection, and Evidence Sufficiency. See `docs/Pipeline.md` and `docs/research/EvaluationPlan.md` for the current contract.

This document defines how evidence should move through Strategic Intelligence Agent. It is a conceptual architecture document, not an implementation plan.

The Evidence Architecture supports future work on an Evidence Ledger, Confidence Layer, Evaluation Harness, and Decision Brief generation. Its purpose is to preserve trust, explainability, and consistency as the platform evolves.

The first V2 foundation implements lightweight versions of the Decision Case Schema, Evidence Ledger, and qualitative Confidence Assessment. These implementations are intentionally simple and additive; they do not introduce scoring formulas, external sources, databases, or autonomous research.

## Evidence Definition

Evidence is any material or structured signal that can support, qualify, challenge, or revise decision reasoning.

Evidence may include:

- Source material provided by the user.
- Extracted observations from that source material.
- Historical analogues retrieved from curated records.
- Inferred assumptions needed to connect evidence to a decision.
- Identified mechanisms that explain how a situation may operate.

The platform must distinguish four concepts:

### Evidence

Evidence is the material basis for analysis. It can be direct source text, extracted data, historical context, or structured records used to support reasoning.

### Observation

An observation is a statement drawn from evidence. It should describe what the available material indicates without turning that statement into a recommendation.

### Inference

An inference is a reasoned interpretation based on evidence and observations. It may connect patterns, mechanisms, or implications, but it depends on assumptions that should remain visible.

### Recommendation

A recommendation is a proposed action or preferred path based on decision criteria, evidence, observations, inferences, and assumptions.

Evidence, observations, inferences, and recommendations must never be conflated. A mature decision-support system should let reviewers see which category each claim belongs to.

## Evidence Lifecycle

Evidence should move through the platform in a clear lifecycle:

```text
Input
  |
  v
Extraction
  |
  v
Assessment
  |
  v
Reasoning
  |
  v
Decision Brief
  |
  v
Monitoring
  |
  v
Learning
```

### Input

Input is the user's supplied material: pasted text, supported files, readable URL text, or a decision question. Input establishes the initial evidence boundary. The platform should not imply that it has reviewed sources outside that boundary unless future functionality explicitly supports and discloses that behavior.

### Extraction

Extraction converts input into structured observations: issue signals, stakeholders, event types, mechanisms, constraints, and decision-relevant details. Extraction should preserve the distinction between what the source states and what the system interprets.

### Assessment

Assessment evaluates evidence quality, relevance, completeness, recency, and uncertainty. This stage should identify limitations, missing context, weak support, and conflicting signals where they are present.

### Reasoning

Reasoning connects assessed evidence to decision criteria, historical analogues, mechanisms, options, assumptions, and trade-offs. This stage should make clear when it is using evidence directly and when it is relying on inference.

### Decision Brief

The Decision Brief presents evidence-backed reasoning to the user. It should expose the basis for recommendations, show assumptions, preserve uncertainty, and avoid hiding weak or conflicting evidence.

### Monitoring

Monitoring identifies future evidence that could strengthen, weaken, or invalidate the current recommendation. Monitoring signals and change triggers should be tied to the evidence gaps and assumptions in the brief.

### Learning

Learning uses outcome review, evaluation feedback, reviewer notes, and failure-mode tracking to improve future evidence handling. Learning should improve the framework and future practice without rewriting what was known at the time of an earlier decision.

## Evidence Quality

Evidence quality should be described through conceptual dimensions. The platform should not introduce scoring formulas until the dimensions and review expectations are stable.

### Relevance

Relevance asks whether evidence directly supports the decision question, decision criteria, historical comparison, or monitoring need.

### Credibility

Credibility asks whether the source or record is trustworthy enough for the role it plays in the analysis. Credibility should reflect source type, proximity to the event, internal consistency, and known limitations.

### Completeness

Completeness asks whether the available evidence covers the major facts, stakeholders, constraints, risks, and alternatives needed for useful decision support.

### Recency

Recency asks whether the evidence is current enough for the decision context. Some historical evidence remains useful for mechanism comparison, while current event evidence may age quickly.

### Uncertainty

Uncertainty asks what remains unknown, unresolved, contested, inferred, or dependent on future developments. Uncertainty should not be hidden behind confident language.

## Evidence Transparency

Evidence transparency is a platform requirement, not a presentation preference.

The platform should follow these principles:

- Recommendations should expose supporting evidence.
- Uncertainty should remain visible.
- Assumptions should be explicit.
- Conflicting evidence should not be hidden.
- Evidence gaps should be named where they affect decision quality.
- Historical analogues should disclose similarities and differences.
- Inferred claims should be distinguishable from source-grounded observations.
- Confidence language should reflect evidence quality, not output fluency.

Evidence that materially affects a recommendation should never be hidden. This includes weak evidence, missing evidence, conflicting evidence, assumptions, and change triggers.

## Relationship To The Decision Intelligence Framework

Evidence supports every layer of the Decision Intelligence Framework, but it plays a different role in each layer:

- Situation Understanding: evidence establishes context, stakeholders, event type, uncertainty, and decision environment.
- Decision Definition: evidence helps identify the decision question, objective, criteria, and constraints.
- Evidence Assessment: evidence is evaluated for quality, relevance, completeness, recency, and uncertainty.
- Historical Knowledge: evidence supports analogue selection, mechanism matching, similarity analysis, difference analysis, and transferability limits.
- Decision Reasoning: evidence supports options, trade-offs, assumptions, preferred path, and rationale.
- Monitoring: evidence gaps and assumptions become monitoring signals, change triggers, review timing, and update needs.
- Learning: evidence from outcomes, retrospectives, evaluation, and reviewer feedback improves future decision quality.

The Evidence Architecture does not replace the Framework. It defines how evidence should move through and support the Framework.

## Future Implementation

Future implementation should begin only after the conceptual evidence model is stable. Candidate implementation layers include:

### Evidence Ledger

An Evidence Ledger would record source material, extracted observations, assumptions, historical analogues, mechanisms, evidence quality notes, and links between evidence and brief claims.

The ledger should make the evidence trail inspectable without requiring the user to infer how a recommendation was produced.

### Confidence Layer

A Confidence Layer would express confidence based on evidence quality, uncertainty, completeness, and limitations. It should avoid false precision and should not convert weak evidence into numerical certainty without a validated reason.

The layer should help users understand how much weight to place on a recommendation and what would change that confidence.

### Evaluation Harness

An Evaluation Harness would test whether evidence is used responsibly across benchmark cases. It should evaluate evidence relevance, analogue fit, limitation disclosure, uncertainty handling, and separation between observations, inferences, and recommendations.

The harness should support human review rather than replace it.

## Design Boundary

This document does not implement evidence storage, confidence scoring, or evaluation automation. It defines the architecture those future systems should respect.

Evidence architecture should make the platform more trustworthy, not more complicated for its own sake.
