# Evaluation Strategy

This document defines the future evaluation strategy for Strategic Intelligence Agent. It does not implement a new evaluation harness.

The goal is to evaluate decision-support quality, not to claim real-world accuracy or prediction capability.

The V2 foundation now exposes a Decision Case Schema, Evidence Ledger, and qualitative Confidence Assessment. Future evaluation work should use these structures as reviewable inputs for evidence use, overconfidence control, limitation disclosure, and change-trigger quality.

The first Decision Quality Evaluation Harness is deterministic and product-focused. It evaluates generated artifacts across direct answer quality, historical analogue relevance, evidence use, option clarity, risk identification, change trigger quality, localization quality, and overconfidence control. Its scores are internal review aids only, not scientific or real-world accuracy claims.

## Why Evaluation Matters

AI decision-support systems can produce structured, fluent, and plausible outputs even when the reasoning is incomplete. Evaluation is necessary because the product is intended to help users reason under uncertainty.

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

Decision quality asks whether the product output is useful, grounded, and appropriately cautious:

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

### Localization Quality

Assess whether localized output preserves meaning, structure, and decision logic across English, Simplified Chinese, and Traditional Chinese modes. Localization should not merely translate labels while losing analytical clarity.

### Overconfidence Control

Assess whether the output avoids unsupported certainty, prediction language, advice claims, and false precision. Strong outputs should be clear without pretending to know more than the evidence supports.

## Future Benchmark Direction

Future benchmarks should move beyond simple label coverage. A stronger benchmark program should include:

- Curated strategic cases with expected decision questions.
- Human-reviewed analogue relevance labels.
- Evidence quality annotations.
- Golden output fixtures for selected cases.
- Scenario-specific risk expectations.
- Localization review samples.
- Regression tests for overconfidence language.
- Side-by-side comparison against generic LLM-style outputs.

Benchmarks should remain transparent about what they measure and what they do not measure. Scores should be interpreted as internal product signals, not proof of real-world correctness.

## Human Review Expectations

Human review should be part of the evaluation process because strategic decision quality cannot be fully reduced to automated checks.

Reviewers should assess:

- Whether the brief is useful for a real decision conversation.
- Whether the evidence and limitations are understandable.
- Whether analogues add insight or distract.
- Whether the preferred path is justified by the stated criteria.
- Whether risks and change triggers are practical.
- Whether the output remains within product boundaries.

Reviewer disagreement should be tracked rather than hidden. Disagreement is useful evidence about ambiguity, weak rubrics, or unclear product behavior.

## Failure Mode Tracking

Future versions should track recurring failure modes such as:

- Generic summary instead of decision support.
- Weak or irrelevant analogues.
- Missing evidence limitations.
- Overconfident recommendation language.
- Vague options.
- Missing downside risks.
- Localization drift.
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
