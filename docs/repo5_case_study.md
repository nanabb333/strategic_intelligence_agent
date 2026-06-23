# Strategic Intelligence Agent - Portfolio Case Study

## 1. Problem

Analysts often receive messy source material such as policy excerpts, earnings notes, supply chain updates, and geopolitical summaries. Turning those documents into structured executive intelligence is slow, inconsistent, and difficult to review.

The project addresses that workflow gap by creating a local strategic intelligence decision-support application.

## 2. Target User

The target user is a non-technical analyst, business student, strategy associate, policy researcher, or product reviewer who wants structured analysis without writing prompts or running command-line tools.

## 3. Product Vision

The vision is a local application that converts a document into a structured intelligence brief with traceable reasoning artifacts. The product emphasizes usability, transparency, and analytical discipline over technical complexity.

## 4. System Workflow

```text
Document
-> Issue Extraction
-> Scenario Classification
-> Mechanism Detection
-> Historical Analogues
-> Historical Outcomes
-> Strategic Lessons
-> Evidence Credibility
-> Executive Brief
-> Downloadable Artifacts
```

## 5. What the Agent Does

- Extracts the core issue and entities from pasted or uploaded text.
- Classifies the scenario using deterministic rules.
- Retrieves historical analogues from local knowledge bases.
- Maps mechanisms such as export controls, sanctions, supply chain disruption, and industrial policy.
- Retrieves simplified historical outcomes and observed strategic responses.
- Generates rule-based strategic lessons.
- Produces Markdown, TXT, and JSON artifacts.
- Displays run history through a local FastAPI-backed dashboard.

## 6. What the Agent Does Not Do

- It does not forecast outcomes.
- It does not provide investment advice.
- It does not provide legal advice.
- It does not perform live web search.
- It does not claim production readiness.
- It does not replace human expert review.

## 7. V6 Productization Milestone

V6 moved the project from portfolio demonstration to usable local application. The dashboard calls a FastAPI backend, runs the actual Python pipeline, stores run folders, and supports downloads.

For a non-technical user, the workflow is simple: open the dashboard, paste text, choose a guided question, click Analyze, and download results.

## 8. V7 Historical Outcome Layer

V7 added `knowledge_base/historical_outcomes.csv`, a curated educational database of simplified historical outcomes. The system connects retrieved analogues to observed consequences, strategic responses, time horizons, confidence labels, and source status.

The purpose is not prediction. The purpose is to help analysts ask better questions by understanding what happened in structurally similar historical cases.

## 9. V7.5 Evidence Credibility Layer

V7.5 adds an explicit credibility layer for historical outcomes and strategic lessons. It reports confidence distribution, source status distribution, key limitations, and a reviewer note.

This makes the system more honest: source URLs are not fabricated, confidence is internal evidence coding, and simplified summaries remain subject to human review.

## 10. Example User Journey

1. A user opens the local dashboard.
2. The user pastes a policy or business document.
3. The user selects a guided question such as "What does this issue mean?"
4. The system runs the deterministic pipeline.
5. The dashboard displays scenario, mechanisms, analogues, outcomes, lessons, and evidence credibility.
6. The user downloads the executive brief or JSON artifact.

## 11. Business Analytics Relevance

The project demonstrates business analytics product thinking:

- Structured extraction from unstructured text.
- Deterministic retrieval and scoring.
- Artifact generation for review and reuse.
- Evaluation and validation scripts.
- Product workflows for non-technical users.

## 12. Strategic Intelligence Relevance

The project demonstrates strategic intelligence concepts:

- Historical analogue reasoning.
- Political economy mechanisms.
- Geopolitical and regulatory scenario framing.
- Evidence credibility and limitations.
- Decision-support briefs without forecasting claims.

## 13. Limitations

- Historical outcomes are simplified educational summaries.
- Some source status values remain `source pending`.
- The system uses deterministic rules and local CSV/Markdown knowledge bases.
- It does not evaluate live source truth.
- It does not use LLM reasoning quality benchmarks.
- It requires human review before executive use.

## 14. Portfolio Value

This project is strongest as a portfolio example of AI product architecture, analytics workflow design, agent-style orchestration, evidence traceability, and local application productization. It demonstrates judgment about what not to build: no unnecessary cloud deployment, no autonomous agents, no forecasting claims, and no advice framing.
