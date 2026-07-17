# Decision Intelligence Framework

This document defines the conceptual architecture for Strategic Intelligence Agent. It explains the decision reasoning framework that future product documentation, evaluation strategy, roadmap planning, and implementation choices should follow.

The framework is not an implementation document. It does not describe APIs, modules, storage, or deployment. It defines the reasoning layers that make the product a Decision Intelligence Platform rather than a generic chatbot, summarizer, or autonomous web agent.

The framework has exactly seven layers:

1. Situation Understanding
2. Decision Definition
3. Evidence Assessment
4. Historical Knowledge
5. Decision Reasoning
6. Monitoring
7. Learning

Each layer has a distinct responsibility. The layers should remain stable even as implementation details evolve.

## Layer 1: Situation Understanding

### Purpose

Understand what has happened before constructing pathway comparisons.

### Description

This layer establishes the basic decision environment. It identifies the context, stakeholders, event type, uncertainty, and operating conditions around the source material.

The goal is to avoid premature pathway preference. A system cannot support a decision well until it has first understood the situation that created the decision need.

This layer should clarify:

- Context: the business, policy, market, supply-chain, or geopolitical setting.
- Stakeholders: the actors affected by the situation or involved in the response.
- Event type: the kind of change or pressure being analyzed.
- Uncertainty: what is unknown, incomplete, contested, or still developing.
- Decision environment: the constraints and conditions that shape possible action.

## Layer 2: Decision Definition

### Purpose

Clarify the actual decision that must be made.

### Description

This layer translates situation understanding into a decision frame. It defines the decision question, decision objective, decision criteria, and constraints.

The goal is to make the user's real choice explicit. Many source materials describe events without stating the decision they create. This layer connects information to possible action without selecting a path.

This layer should clarify:

- Decision question: the question the user or organization needs to answer.
- Decision objective: what the decision is trying to achieve.
- Decision criteria: the factors that should guide comparison across options.
- Constraints: timing, resources, policy limits, operational limits, or evidence gaps.

## Layer 3: Evidence Assessment

### Purpose

Collect, organize, and evaluate available evidence.

### Description

This layer separates what is supported by available source material from what is inferred, assumed, or missing. It records structural evidence sufficiency, relevance signals, limitations, and uncertainty without claiming calibrated confidence.

The goal is to make the evidence base reviewable. Decision support becomes less trustworthy when evidence boundaries are hidden or when weak evidence is presented with excessive certainty.

This layer should clarify:

- Evidence quality: whether the available material is direct, indirect, complete, partial, or weak.
- Relevance: how closely the evidence supports the decision question.
- Limitations: what the evidence does not show.
- Uncertainty: what remains unresolved or dependent on future information.
- Evidence Sufficiency: a structural workflow tier whose explicit limits remain visible.

## Layer 4: Historical Knowledge

### Purpose

Use historical analogues and mechanisms to improve reasoning.

### Description

This layer compares the current situation with historical cases, recurring mechanisms, similarities, differences, and transferability limits.

Historical knowledge helps users reason from patterns. It can identify mechanisms such as market-access restriction, compliance burden, supply-chain disruption, industrial policy response, or stakeholder adaptation. It can also show where current conditions differ from earlier cases.

Historical analogues inform reasoning but never determine conclusions. They provide context, comparison, and caution. They do not predict outcomes, prove a pathway, or replace current evidence.

This layer should clarify:

- Historical cases: prior situations that may help frame the current issue.
- Mechanism matching: the recurring dynamics that connect past and present cases.
- Similarities: features that make comparison useful.
- Differences: features that limit comparison.
- Transferability: how much reasoning can responsibly carry from one case to another.

## Layer 5: Decision Reasoning

### Purpose

Organize evidence and constraints into neutral pathway comparisons.

### Description

This layer combines deterministic pathway archetypes with case-derived references, risks, constraints, assumptions, and unknowns. Archetype titles, trade-offs, and several comparison buckets are reusable templates rather than fully evidence-derived content.

The goal is not to make an unsupported prediction, issue domain-specific advice, or select a path. The goal is to help the reviewer inspect how available pathways differ under the recorded evidence and constraints.

This layer must clearly distinguish facts, system-generated pathway considerations, and any later reviewer-authored selection.

This layer should clarify:

- Decision options: plausible paths the user could consider.
- Trade-offs: benefits, costs, risks, and implementation consequences.
- Assumptions: conditions that must hold for the reasoning to remain valid.
- Reviewer selection: an optional human-owned field that remains empty until a reviewer records a choice.
- Selection rationale: an optional reviewer-authored explanation, never inferred from pathway order.

## Layer 6: Monitoring

### Purpose

Identify future signals that could change the assessment or a reviewer-owned selection.

### Description

This layer defines what should be watched after the brief is produced. It identifies monitoring signals, change triggers, review timing, and evidence updates.

Assessments should remain revisable. Strategic situations change, and a responsible decision-support system should show what would justify updating the analysis.

This layer should clarify:

- Monitoring signals: observable developments relevant to the decision.
- Change triggers: specific conditions that would alter the assessment or pathway comparison.
- Review timing: when the user should revisit the analysis.
- Evidence updates: new information that would strengthen, weaken, or change the reasoning.

## Layer 7: Learning

### Purpose

Improve future decision quality.

### Description

This layer uses outcome review, retrospective analysis, framework refinement, evaluation feedback, and continuous improvement to make future decision support better.

Learning should improve the framework rather than rewriting history. Prior outputs should remain inspectable as records of what was known and reasoned at the time. Retrospectives should identify what worked, what failed, and how future analysis can become clearer, more evidence-aware, and less overconfident.

This layer should clarify:

- Outcome review: what happened after a decision or review.
- Retrospective analysis: what the original reasoning handled well or missed.
- Framework refinement: how concepts, criteria, or rubrics should improve.
- Evaluation feedback: what benchmark results or human review show.
- Continuous improvement: how repeated review improves decision quality over time.

## Relationship To Existing Repository

Existing repository components align with the framework where the mapping is natural:

| Repository Component | Framework Alignment |
| --- | --- |
| Issue extraction and scenario classification | Layer 1: Situation Understanding |
| Decision criteria and decision paths | Layer 2: Decision Definition |
| Evidence notes and limitation language | Layer 3: Evidence Assessment |
| Historical analogue engine | Layer 4: Historical Knowledge |
| Historical outcomes and strategic lessons | Layer 4: Historical Knowledge |
| Decision brief | Layer 5: Decision Reasoning |
| Neutral pathway comparison and reviewer-owned selection fields | Layer 5: Decision Reasoning |
| Monitoring signals and review windows | Layer 6: Monitoring |
| Evaluation Strategy | Cross-cutting across Layers 2 through 7 |
| Testing and CI | Supporting reliability, not a substitute for decision-quality evaluation |
| Run artifacts and metadata | Supporting reviewability across layers |

This mapping should not be forced. Some implementation details support multiple layers, and some are engineering concerns rather than conceptual framework elements.

## Design Principles

- Separate facts from pathway considerations and reviewer decisions.
- Evidence should be reviewable.
- Pathway considerations must expose assumptions.
- Historical analogues support reasoning.
- Decision support is not prediction.
- Trust is earned through transparency.
- Assessments should be revisable.
- Frameworks remain stable while implementations evolve.

## Governance Role

This framework should guide future product decisions. New features, documentation, roadmap items, and evaluation rubrics should be explainable through one or more framework layers.

If a proposed change does not strengthen situation understanding, decision definition, evidence assessment, historical knowledge, decision reasoning, monitoring, or learning, it should be treated as optional and reviewed carefully before inclusion.
