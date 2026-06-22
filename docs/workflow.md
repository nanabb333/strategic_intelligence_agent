# Workflow

## Target Workflow

```text
Document
-> Issue Extraction
-> Scenario Classification
-> Historical Analogue Retrieval
-> Current Context Retrieval
-> Intelligence Synthesis
-> Executive Intelligence Brief
```

## Stage Details

### 1. Document Loading

The agent accepts source material such as reports, policy documents, news
briefs, transcripts, filings, memos, or pasted text. The loader normalizes the
content into a consistent text representation.

### 2. Issue Extraction

The extractor identifies:

- Core issue.
- Relevant actors.
- Countries or regions.
- Industries.
- Policy terms.
- Companies.
- Document type guess.
- Uncertainties.
- Evidence snippets.

### 3. Scenario Classification

The classifier assigns the issue to strategic categories such as:

- Export Controls.
- Industrial Policy.
- Sanctions.
- Supply Chain Disruption.
- Regulatory Action.
- Military / Security Shock.
- Earnings / Corporate Disclosure.
- Strategic Investment.
- Trade Policy.
- Other.

Classification uses deterministic keyword matching. The confidence label
describes classification quality only; it is not a forecast probability.

### 4. Historical Analogue Retrieval

The retriever searches curated examples for structurally similar events. The
goal is not prediction; the goal is to support better reasoning by comparison.

The retriever loads `knowledge_base/historical_analogues.csv` and scores cases
using:

- Scenario type match.
- Keyword overlap.
- Industry overlap.
- Actor overlap.

### 5. Current Context Retrieval

The context retriever loads local Markdown files from
`knowledge_base/current_context/` and scores entries using:

- Industry match.
- Scenario match.
- Keyword overlap.

Historical analogues alone are insufficient because they show what an issue may
resemble, but not which current stakeholders, constraints, and monitoring
considerations are relevant. The context layer improves decision support by
adding present-domain framing without making forecasts.

### 6. Intelligence Synthesis

The analyzer combines historical analogues and current context into:

- Observed similarities.
- Observed differences.
- Business considerations.
- Operational considerations.
- Geopolitical considerations.
- Strategic questions.

The language avoids forecasts, probabilities, and investment recommendations.
It uses phrasing such as "may resemble", "shares characteristics with",
"differs from", and "requires monitoring".

### 7. Executive Brief Generation

The generator writes a concise brief with these sections:

- Executive Summary.
- Key Issue.
- Scenario Classification.
- Extracted Entities.
- Historical Analogues.
- Current Context.
- Similarities and Differences.
- Business Considerations.
- Operational Considerations.
- Geopolitical Considerations.
- Strategic Questions.
- Analyst Notes.
- Limitations.

Each brief includes an evidence trace section showing source origins.

