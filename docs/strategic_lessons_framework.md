# Strategic Lessons Framework

The Strategic Lessons Engine converts retrieved historical outcomes into recurring, explainable lessons.

## Inputs

- Retrieved historical outcomes.
- Observed outcomes.
- Strategic responses.
- Event families and sectors.

## Method

`src/strategic_lessons.py` applies rule-based keyword groups to retrieved outcomes. Each lesson includes:

- Lesson statement.
- Supporting cases.
- Confidence: High, Medium, or Low.
- Rationale.
- Evidence references.

Confidence is based on the number of supporting retrieved cases:

- High: three or more supporting cases.
- Medium: two supporting cases.
- Low: one supporting case.

## Example

```text
Lesson:
Supply chain diversification frequently appears after export-control or disruption shocks.

Supporting cases:
ASML Export Controls
COVID Supply Chain Disruption
Red Sea Shipping Disruption

Confidence:
High
```

## Guardrails

The lesson engine is not predictive. It does not recommend investments, provide legal advice, or claim that a historical pattern will repeat. It supports structured executive discussion by surfacing recurring behaviors observed in retrieved examples.
