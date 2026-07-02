# Demo Walkthrough

This walkthrough helps reviewers understand Strategic Intelligence Decision Companion without running the product.

## Demo Objective

Show how Repo 5 structures a strategic decision into evidence, readiness, pathway comparison, review state, timeline, and delta artifacts.

The objective is not to show a chatbot answer. The objective is to show reviewer-first Decision Intelligence.

## Recommended Showcase Scenario

Use the V4 workspace demo:

```text
demo_case_outputs/v4_workspace/
```

Recommended question:

```text
Should we adjust investment and supply-chain plans in response to new export controls?
```

This scenario is useful because it contains:

- strategic uncertainty
- regulatory context
- operational implications
- evidence constraints
- multiple review questions
- decision history and delta artifacts

## Step-By-Step Walkthrough

1. Start with the project file:

   ```text
   demo_case_outputs/v4_workspace/project.json
   ```

   Observe how the workspace groups questions, evidence, decisions, and timestamps.

2. Open the evidence library:

   ```text
   demo_case_outputs/v4_workspace/evidence_library.json
   ```

   Observe evidence IDs, source names, source types, and reviewable metadata.

3. Open the first decision brief:

   ```text
   demo_case_outputs/v4_workspace/question_1_q_export_controls_immediate/brief.md
   ```

   Observe how the brief presents a structured decision-support artifact rather than an open-ended answer.

4. Open the first analysis JSON:

   ```text
   demo_case_outputs/v4_workspace/question_1_q_export_controls_immediate/analysis.json
   ```

   Observe machine-readable analysis sections and traceable structured fields.

5. Open the second question artifacts:

   ```text
   demo_case_outputs/v4_workspace/question_2_q_export_controls_update/
   ```

   Observe how a later question can build a project decision history.

6. Open the decision history:

   ```text
   demo_case_outputs/v4_workspace/decision_history.json
   ```

   Observe how the project keeps prior decision runs inspectable.

7. Open the decision delta:

   ```text
   demo_case_outputs/v4_workspace/decision_delta.json
   ```

   Observe how the product compares the latest decision context against prior project history.

## Expected Reviewer Observations

Reviewers should see that the product:

- organizes decisions into project workspaces
- separates evidence from analysis
- preserves local artifacts
- supports multiple linked decision questions
- makes decision history inspectable
- avoids autonomous decision-making
- keeps reviewer interpretation central

## Decision Intelligence Value

The demo illustrates the product category:

```text
Most AI systems optimize for generating answers.
Strategic Intelligence Decision Companion optimizes for improving decision quality.
```

Decision Intelligence value appears in:

- explicit decision questions
- evidence traceability
- readiness and review concepts
- pathway comparison without ranking
- decision history and delta
- human-controlled interpretation

## Human-In-The-Loop Checkpoints

The reviewer remains responsible for:

- choosing the project
- defining the decision question
- deciding which evidence is accepted
- deciding which evidence is selected for analysis
- reviewing assumptions and unknowns
- interpreting pathway drafts
- recording unresolved questions
- making any final decision outside the system

## What Not To Claim

Do not describe this demo as:

- autonomous research
- legal advice
- investment advice
- compliance automation
- forecasting
- final decision selection
- evidence truth verification

It is a local, deterministic, reviewer-first decision-support workflow.
