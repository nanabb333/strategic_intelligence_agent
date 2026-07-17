# Research Protocol

## Status

This document is the current research protocol skeleton. No participant study, external validation, or statistical analysis has been completed. Planned work must not be described as a current product capability or result.

## Working Research Question

To what extent does a structured, evidence-ledger-based decision assessment improve reviewers' identification of unsupported claims, source-attribution accuracy, and review efficiency compared with unstructured strategic summaries?

This question is provisional, subject to feasibility review and supervisor review/approval, and has not been validated by a completed study.

## System Under Study

Strategic Intelligence Decision Companion is a deterministic, auditable, reviewer-first strategic decision-support system. It structures a decision question, evidence ledger, neutral pathways, risks, uncertainties, limitations, and change triggers. It does not rank or select a pathway, use an LLM, or make an autonomous decision.

## Contribution Boundary

The planned contribution concerns evidence representation, reviewability, and reviewer performance. It does not claim better real-world decisions, factual correctness across domains, forecasting ability, calibrated probability, or replacement of professional judgment.

## Hypotheses

- H1: Structured evidence-ledger assessments improve unsupported-claim identification relative to unstructured summaries.
- H2: Structured assessments improve source-attribution accuracy.
- H3: Structured assessments reduce missed critical limitations.
- H4: Structured assessments change review time; the direction and practical value must be measured rather than assumed.
- H5: Reviewer trust is better aligned with visible evidence sufficiency and limitations.

## Experimental Conditions

- Source material with an unstructured strategic summary.
- A defined baseline summary condition using the same source boundary.
- The repository's structured neutral decision assessment.

The exact baseline implementation will be frozen before the main study. Conditions must use the same underlying source material and temporal cutoff.

## Variables

The independent variable is assessment presentation condition. Planned dependent variables are unsupported-claim detection rate, source-attribution accuracy, missed-critical-limitation rate, review time, rationale completeness, trust ratings, and cognitive-load measures.

## Participant Profile

Participants should have relevant graduate-level, analyst, policy, risk, strategy, or decision-review experience. Final eligibility criteria and sample size will be defined after a pilot and power analysis; no participant count is currently claimed.

## Study Design

A randomized, counterbalanced within-subject or mixed design is planned. Case order and condition order will be randomized. Training cases will be separate from study cases. Reviewers and outcome annotators should be blinded to the system-development hypotheses where practicable.

## Planned Analysis

The final analysis plan will specify estimands before the main study. It will report confidence intervals, effect sizes, missing-data handling, order effects, and sensitivity analyses. Inter-annotator agreement will be reported for gold annotations and rationale scoring. Statistical tests will be selected after the outcome distributions and study design are frozen.

## Threats to Validity

- Synthetic or overly short cases may not represent real review work.
- Participants may learn the rubric across repeated conditions.
- Domain expertise and familiarity with the cases may confound outcomes.
- Interface differences may affect time independently of evidence structure.
- Researcher-authored annotations may encode system assumptions.
- Historical cases can introduce hindsight leakage.
- Results from one decision domain may not generalize to others.

## Ethics and Privacy

Use non-sensitive public source material unless an approved protocol permits otherwise. Do not collect unnecessary personal data. Participant consent, withdrawal, data retention, anonymization, compensation, and institutional review requirements must be resolved before recruitment. Local project artifacts can contain sensitive material and must not be committed unintentionally.

## Current Versus Planned

Currently implemented: deterministic orchestration, evidence ledger, neutral pathway assessment, reviewer boundary, artifact completeness checks, and a synthetic regression suite.

Planned but not completed: independent research dataset, gold annotations, pilot study, participant study, power analysis, inferential analysis, and external validation.
