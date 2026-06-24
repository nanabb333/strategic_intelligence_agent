# V9.5 Localization And Input Modes

## Purpose

V9.5 responds to user testing feedback that the app needed stronger multilingual output and clearer input choices. The upgrade keeps the project local, deterministic, and portfolio-focused.

## True Localization Goal

The app now centralizes localization in `src/localization.py`.

Supported languages:

- English
- Simplified Chinese
- Traditional Chinese

The localization layer translates app-generated analytical structure:

- section headings
- confidence labels
- question intent labels
- event-context labels
- strategic lesson template sentences
- evidence credibility notes
- limitations and decision-support notes

The app does not claim to translate arbitrary copyrighted user-uploaded articles. User source text is preserved where it appears as input-derived content.

## Free-Form Question Localization

`src/question_router.py` classifies free-form questions into deterministic intents such as Historical Comparison, Decision Support, Evidence Review, Mechanism Analysis, and Implication Analysis. V9.5 adds localized intent labels such as:

- Historical Comparison -> 历史比较 / 歷史比較
- Decision Support -> 决策支持 / 決策支持
- Evidence Review -> 证据审查 / 證據審查

## Supported Input Modes

The dashboard now presents three clear modes:

1. **Paste Text:** paste an article, policy excerpt, earnings note, or memo.
2. **Upload File:** upload `.txt`, `.md`, `.markdown`, or `.pdf`.
3. **Paste Link:** store a source URL as metadata.

## PDF Support

PDF upload uses local server-side text extraction with `pypdf`.

Limitations:

- Only text-based PDFs are supported.
- Scanned image PDFs are not supported.
- OCR is not included.

## Link Metadata Mode

Paste Link mode does not fetch web pages. If the user enters only a URL, the app stores the link and returns a clear message asking for pasted or uploaded document text.

If a link is provided with pasted or uploaded text, the app includes `source_url` in:

- `metadata.json`
- `analysis.json`
- `brief.md`
- `brief.txt`
- dashboard output

## Guardrails

V9.5 does not add live web search, RAG, vector databases, external news APIs, forecasting, legal advice, investment advice, cloud deployment, or authentication.
