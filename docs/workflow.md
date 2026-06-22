# Workflow

## Target Workflow

```text
Document
-> Issue Extraction
-> Scenario Classification
-> Historical Analogue Retrieval
-> Implication Analysis
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

V0.5 loads `knowledge_base/historical_analogues.csv` and scores cases using:

- Scenario type match.
- Keyword overlap.
- Industry overlap.
- Actor overlap.

### 5. Implication Analysis

The analyzer converts extracted issues, scenario classifications, and analogues
into structured implications:

- Business implications.
- Geopolitical implications.
- Market-context implications.
- Operational-risk implications.
- Strategic questions.

The language avoids forecasts, probabilities, and investment recommendations.

### 6. Executive Brief Generation

The generator writes a concise brief with these sections:

- Key Issue.
- Scenario Classification.
- Extracted Entities.
- Historical Analogues.
- Current Relevance.
- Business and Geopolitical Implications.
- Strategic Questions for Decision-Makers.
- Analyst Notes and Limitations.
