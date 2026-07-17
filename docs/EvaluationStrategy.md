# Evaluation Strategy

This document is a compatibility overview. The canonical planned research protocol is [Research Evaluation Plan](research/EvaluationPlan.md). The current repository implements artifact completeness checks and a deterministic regression and contract validation suite; it does not implement external decision-quality evaluation.

The goal is to evaluate decision-support quality, not to claim real-world accuracy or prediction capability.

The current foundation exposes a Neutral Decision Assessment, Evidence Ledger, Evidence Sufficiency Assessment, and Artifact Completeness Check. Future research should use these structures as study materials, not as self-validating quality evidence.

The Artifact Completeness Check measures field presence and review structure only. It does not validate pathway correctness, evidence validity, decision correctness, human decision quality, or real-world usefulness.

## Why Evaluation Matters

Decision-support systems can produce structured and plausible outputs even when the reasoning is incomplete. Evaluation is necessary because the product is intended to help users reason under uncertainty.

Evaluation should answer:

- Does the output help a human make sense of the decision?
- Are historical analogues relevant?
- Is evidence used responsibly?
- Are risks and limitations visible?
- Does the output avoid unsupported confidence?
- Does the product perform better than a generic summary or generic LLM answer?

Without evaluation, the product could look polished while failing at its core purpose.

## Software Correctness Vs. Decision Quality

Software correctness asks whether the application behaves as implemented:

- Routes respond.
- Files upload.
- Artifacts are written.
- JSON is valid.
- Tests pass.
- The pipeline does not crash.

Future human evaluation of decision quality would ask whether the product output is useful, grounded, and appropriately cautious; the current automated checks do not answer these questions:

- The decision question is framed correctly.
- Options are clear.
- Historical analogues are relevant.
- Evidence limits are visible.
- Risks are not ignored.
- Monitoring triggers are practical.
- The output does not overstate certainty.

Both forms of evaluation matter. Software correctness protects reliability. Decision-quality evaluation protects product credibility.

## Proposed Evaluation Dimensions

### Direct Answer Quality

Assess whether the output directly addresses the user's decision question instead of drifting into a generic summary. A strong answer should make the decision context clear and identify the main judgment required.

### Historical Analogue Relevance

Assess whether selected analogues share meaningful mechanisms with the current case. Similarity should be based on strategic pattern, constraints, actors, and response dynamics, not superficial keyword overlap.

### Evidence Use

Assess whether the output distinguishes source-supported claims from inferred analysis. Strong outputs should cite or describe the evidence basis at the right level and identify missing information.

### Option Clarity

Assess whether the decision paths are concrete, distinguishable, and tied to decision criteria. Options should not be vague restatements of the same action.

### Risk Identification

Assess whether the output identifies material downside risks, implementation risks, timing risks, stakeholder risks, and evidence risks relevant to the scenario.

### Change Trigger Quality

Assess whether the output explains what new information would change the analysis. Good triggers are observable, specific, and connected to the decision.

### Product Language Consistency

Assess whether English output preserves the official terminology, decision-support boundaries, and reviewer-first workflow. Localization is not active in the consolidated release.

### Overconfidence Control

Assess whether the output avoids unsupported certainty, prediction language, advice claims, and false precision. Strong outputs should be clear without pretending to know more than the evidence supports.

## Future Benchmark Direction

Future benchmarks should move beyond simple label coverage. A stronger benchmark program should include:

- Curated strategic cases with expected decision questions.
- Human-reviewed analogue relevance labels.
- Evidence quality annotations.
- Golden output fixtures for selected cases.
- Scenario-specific risk expectations.
- Product language consistency samples.
- Regression tests for overconfidence language.
- Side-by-side comparison against generic LLM-style outputs.

Benchmarks should remain transparent about what they measure and what they do not measure. Scores should be interpreted as internal product signals, not proof of real-world correctness.

## Human Review Expectations

Human review should be part of the evaluation process because strategic decision quality cannot be fully reduced to automated checks.

Reviewers should assess:

- Whether the brief is useful for a real decision conversation.
- Whether the evidence and limitations are understandable.
- Whether analogues add insight or distract.
- Whether neutral pathway comparisons help reviewers form and explain their own judgment.
- Whether risks and change triggers are practical.
- Whether the output remains within product boundaries.

Reviewer disagreement should be tracked rather than hidden. Disagreement is useful evidence about ambiguity, weak rubrics, or unclear product behavior.

## Failure Mode Tracking

Future versions should track recurring failure modes such as:

- Generic summary instead of decision support.
- Weak or irrelevant analogues.
- Missing evidence limitations.
- Overconfident pathway or conclusion language.
- Vague options.
- Missing downside risks.
- Product terminology drift.
- Unsupported causal claims.
- Confusion between monitoring signals and predictions.
- Output that implies investment, trading, legal, or compliance advice.

Failure modes should be linked to benchmark cases, reviewer notes, and future remediation work.

## Comparison Against Generic LLM Output

The product should be compared against generic LLM responses because its strategic value depends on doing more than open-ended generation.

Comparison should assess:

- Decision structure.
- Evidence visibility.
- Historical analogue usefulness.
- Risk coverage.
- Option clarity.
- Limitation disclosure.
- Monitoring discipline.
- Artifact usefulness.

The product does not need to be broader than a generic LLM. It needs to be more structured, more reviewable, and more accountable for the decision-support workflow it claims to provide.

## Implementation Guidance

Do not implement a larger evaluation harness until the evaluation dimensions, rubrics, and benchmark cases are clear. The next step should be rubric design and selected benchmark expansion, followed by lightweight automation where it supports reviewer judgment.
