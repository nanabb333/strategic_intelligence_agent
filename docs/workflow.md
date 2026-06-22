# Workflow

## Target Workflow

```text
Document
-> Issue Extraction
-> Scenario Classification
-> Historical Analogue Retrieval
-> Current Context Retrieval
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
- Decisions or events.
- Constraints.
- Unknowns.
- Evidence snippets.

### 3. Scenario Classification

The classifier assigns the issue to strategic categories such as:

- Geopolitical shock.
- Regulatory change.
- Market structure shift.
- Supply chain disruption.
- Competitive move.
- Technology transition.
- Reputational or trust event.

### 4. Historical Analogue Retrieval

The retriever searches curated examples for structurally similar events. The
goal is not prediction; the goal is to support better reasoning by comparison.

### 5. Current Context Retrieval

The context retriever gathers or accepts current information relevant to the
issue. In early versions this can be a local notes file. Later versions may add
web, database, or internal knowledge integrations.

### 6. Implication Analysis

The analyzer converts extracted issues, analogues, and context into strategic
implications. It should separate evidence, inference, uncertainty, and possible
decision relevance.

### 7. Executive Brief Generation

The generator writes a concise brief for a decision-maker. The output should be
readable, structured, and explicit about limitations.

