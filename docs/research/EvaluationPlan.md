# Evaluation Plan

## Status

This is a planned evaluation protocol. No research comparison, participant result, or statistical conclusion has been completed.

## Regression Evaluation Versus Research Evaluation

The existing deterministic regression and contract validation suite checks whether known rules still produce predetermined labels and structures. Its synthetic cases are useful for software stability. Fixed lens and response checks measure contract presence, not external accuracy.

Research evaluation will use independently sourced cases, frozen conditions, external annotations, and human review outcomes. Artifact completeness is not decision quality, and evidence sufficiency is not a probability of correctness.

## Planned Baselines

- Unstructured strategic summary with the same source boundary.
- A simple deterministic summary/template baseline.
- If approved and reproducibly configured, a generic LLM summary may be included as a separate baseline; the product itself will not require an LLM.

Baseline content, model/version if applicable, parameters, and source access must be frozen and reported before the main study.

## Planned Outcome Measures

- Unsupported-claim detection rate.
- Source-attribution accuracy.
- Missed-critical-limitation rate.
- Review completion time.
- Decision-rationale completeness using a pre-defined rubric.
- Trust and reliance measures that distinguish appropriate from excessive trust.
- Cognitive load using a defined instrument selected before the main study.

## Gold Annotation and Agreement

Independent annotators will label claims, source relationships, and critical limitations. The protocol will report raw agreement and an agreement statistic suitable for each scale, plus adjudication rules. System developers should not be the sole final annotators.

## Pilot and Sample Planning

A pilot will test instructions, task duration, instrumentation, rubric ambiguity, and expected variance. A power analysis based on the primary outcome and planned design will be completed before fixing the final participant count. Pilot cases and participants will not silently become the confirmatory sample.

## Randomization and Counterbalancing

Case order, condition order, and condition-to-case assignment will be randomized or counterbalanced. The analysis will check period, carryover, learning, and fatigue effects. Training examples will be held separate.

## Planned Statistical Reporting

Report effect estimates, confidence intervals, effect sizes, sample exclusions, missing data, and robustness checks. Avoid substituting statistical significance for practical usefulness. Analysis code and de-identified aggregate outputs should be reproducible where ethics and licenses permit.

## Ablation Plan

Planned ablations include removal of the evidence ledger, removal of explicit limitations/change triggers, removal of pathway comparison, and a structure-only condition. Each ablation must preserve the same source material so that evidence access is not confounded with presentation structure.

## Research Gaps Before Execution

- Freeze the primary outcome and analysis design.
- Assemble and audit the independent dataset.
- Complete the annotation guide and annotator training.
- Select and freeze baselines.
- Run the pilot and power analysis.
- Resolve ethics, consent, privacy, and retention requirements.
