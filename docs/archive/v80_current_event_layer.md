# V8 Current Event Intelligence Layer

## Why Current Event Context Matters

Historical analogues are more useful when the system first understands what kind of current event the user submitted. A policy update, earnings disclosure, regulatory action, or supply chain note can contain similar words but require different strategic framing.

The current event layer adds a structured context step before issue extraction, scenario classification, historical retrieval, and brief generation.

## What The Layer Extracts

`src/event_context.py` uses deterministic rules to extract:

- event type
- primary actor
- secondary actor
- affected sectors
- affected regions
- policy domain
- strategic significance
- event summary
- confidence label
- context limitations

## How Event Type Classification Works

The layer matches input text against transparent keyword groups for supported event types such as Export Controls, Sanctions, Industrial Policy, Regulatory Action, Geopolitical Escalation, Supply Chain Disruption, Corporate Strategic Shift, Technology Competition, Legislative Action, Trade Restriction, Financial / Earnings Risk, and Market Access Restriction.

The confidence label is based on detected event keywords, sectors, regions, and actor cues. It is a workflow confidence label, not a probability and not a forecast.

## What It Adds Before Historical Retrieval

The layer gives the rest of the workflow a reviewer-friendly framing:

- What kind of event is this?
- Who appears to be involved?
- Which sectors and regions are named?
- Which policy or strategic domain is implicated?
- Why might this matter for decision support?

This makes historical analogue retrieval easier to interpret because reviewers can see the current-event context before comparing past cases.

## Why Deterministic Rules Were Used

The project is a local portfolio application focused on explainable workflow design. Deterministic rules make the behavior auditable, easy to validate, and safe from hidden live-data or LLM dependencies.

## Limitations

- No live web retrieval is performed.
- No external news APIs are used.
- No source verification is performed.
- Keyword rules can miss nuance, sarcasm, implicit references, or multilingual wording.
- Confidence labels do not measure real-world factual accuracy.
- The layer supports decision review; it does not predict outcomes.
