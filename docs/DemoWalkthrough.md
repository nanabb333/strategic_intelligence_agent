# Demo Walkthrough

This three-minute walkthrough shows how Strategic Intelligence Decision Companion preserves a reviewer-controlled decision process without requiring the reviewer to run the product.

## What The Demo Shows

The bundled artifacts demonstrate an earlier V4 Project container with linked questions, accepted evidence, assessments, history, and delta. They predate the V5 Sprint 0 interface migration, so use them to inspect persistence and artifacts—not as a current UI or terminology reference.

Recommended question:

```text
Should we adjust investment and supply-chain plans in response to new export controls?
```

## Review Path

1. Open [`demo_case_outputs/v4_workspace/project.json`](../demo_case_outputs/v4_workspace/project.json) to see the persistent Project context.
2. Open the [Evidence Library](../demo_case_outputs/v4_workspace/evidence_library.json) to inspect evidence IDs, sources, types, and metadata.
3. Review the first [Decision Brief](../demo_case_outputs/v4_workspace/question_1_q_export_controls_immediate/brief.md) as a deterministic decision-support artifact.
4. Inspect the matching [analysis JSON](../demo_case_outputs/v4_workspace/question_1_q_export_controls_immediate/analysis.json) for structured fields.
5. Open the [second question artifacts](../demo_case_outputs/v4_workspace/question_2_q_export_controls_update/) to see related work persisted in one Project.
6. Compare [Decision History](../demo_case_outputs/v4_workspace/decision_history.json) with [Decision Delta](../demo_case_outputs/v4_workspace/decision_delta.json).

## Map The Artifacts To The Current Workflow

| Current step | Demo evidence |
| --- | --- |
| Decision Question | Questions stored in `project.json` and question-specific directories. |
| Decision Context | Project and run metadata surrounding each question. |
| Supporting Evidence | Accepted items in `evidence_library.json`. |
| Decision Assessment | Brief and analysis artifacts for each question. |
| Human Review | Inspectable history, delta, and review-oriented metadata. |
| Export | Markdown, TXT, JSON, trace, and metadata files. |

## Reviewer Checkpoints

The reviewer remains responsible for defining the question and context, accepting evidence, inspecting assumptions and unknowns, comparing any pathway drafts without ranking, recording unresolved questions, and making the final decision outside the system.

Do not present the demo as autonomous research, monitoring, forecasting, evidence truth verification, compliance automation, legal or investment advice, preferred-option selection, or final decision-making.
