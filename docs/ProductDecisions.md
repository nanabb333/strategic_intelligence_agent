# Product Decisions

This document records key product and architecture decisions that shape Strategic Intelligence Agent as a mature AI Decision Intelligence product.

## Decision 1: Position Repo 5 As A Decision Intelligence Platform, Not An AI Agent

### Decision

The project is positioned as a Decision Intelligence Platform rather than an autonomous AI agent.

### Rationale

The core value is structured decision support: issue framing, criteria selection, option comparison, historical analogues, evidence notes, limitations, and monitoring considerations. The product should help users reason more clearly under uncertainty, not imply autonomous research or action.

### Alternatives Considered

- Position the project as an AI agent.
- Add autonomous planning and browsing behavior.
- Present the system as a general research assistant.

### Why Rejected

Agent framing would overstate the current behavior and shift attention away from the mature product strengths: bounded workflow, reviewable artifacts, transparent limitations, and local execution.

### Long-Term Implication

Future work should deepen decision quality, evidence discipline, and evaluation before adding autonomy. If agentic capabilities are ever considered, they should be narrow, auditable, and explicitly evaluated.

## Decision 2: Keep `app.py` Thin

### Decision

`app.py` should remain a thin FastAPI entrypoint focused on HTTP concerns.

### Rationale

The app entrypoint owns routing, request and response models, static file serving, upload handling, run lookup, and downloads. Product logic belongs in the service, pipeline, and intelligence modules. This keeps the system easier to inspect, test, and maintain.

### Alternatives Considered

- Put analysis workflow logic directly inside route handlers.
- Collapse the service and pipeline layers into the FastAPI file.

### Why Rejected

Large route handlers would make behavior harder to test and review. They would also weaken the architecture story for a mature portfolio product.

### Long-Term Implication

The API surface can stay stable while the decision-support pipeline improves behind it.

## Decision 3: Make Historical Analogues Central

### Decision

Historical analogue retrieval and historical outcome context are central to the product workflow.

### Rationale

Strategic decisions often depend on mechanisms that have appeared before: market-access restrictions, compliance burdens, industrial policy responses, supply-chain shocks, regulatory pressure, and organizational adaptation. Historical analogues help users compare patterns without claiming that history determines the future.

### Alternatives Considered

- Produce only a source summary.
- Generate advice without historical comparison.
- Use generic model knowledge without curated local analogue records.

### Why Rejected

Without analogues, the product would be closer to a summarizer. Without curated records, the historical layer would be harder to inspect and explain.

### Long-Term Implication

Future development should improve analogue quality, relevance scoring, evidence labels, and evaluation around whether selected analogues are actually useful.

## Decision 4: Show Evidence And Limitations Explicitly

### Decision

Outputs should disclose evidence notes, assumptions, uncertainty, and limitations.

### Rationale

Decision-support systems can create false confidence if they present conclusions without evidence boundaries. Explicit limitations make the output safer to review and more credible as a portfolio artifact.

### Alternatives Considered

- Provide cleaner executive briefs without caveats.
- Hide evidence quality details to make the output feel more decisive.

### Why Rejected

That would weaken trust and increase the risk that users misread the output as authoritative advice.

### Long-Term Implication

Evidence and limitation handling should become more structured in future versions, especially as evaluation becomes more rigorous.

## Decision 5: Separate Beginner And Analyst Modes

### Decision

The product separates beginner, analyst, and executive output modes.

### Rationale

Different users need different levels of detail and terminology. Beginner mode supports accessibility. Analyst mode supports deeper review. Executive mode supports concise decision framing. Separating modes lets the product serve multiple review contexts without forcing one output style on all users.

### Alternatives Considered

- Use a single universal output format.
- Let users rely on free-form prompting to change the tone.

### Why Rejected

A single format would either be too shallow for analysts or too dense for non-specialists. Free-form prompting would reduce repeatability.

### Long-Term Implication

Future output improvements should preserve mode separation and evaluate whether each mode serves its intended user.

## Decision 6: Exclude Autonomous Web Monitoring From Version 1.0 And Version 2

### Decision

Autonomous web monitoring is not included in Version 1.0 and should not be part of Version 2.

### Rationale

The current product is a local decision-support workspace. Adding autonomous monitoring would introduce source selection, reliability, scheduling, alerting, and trust problems before the evidence and evaluation foundations are mature.

### Alternatives Considered

- Add background source monitoring.
- Add autonomous web search or crawling.
- Add automatic alerts based on external sources.

### Why Rejected

These capabilities would increase complexity and could imply completeness or authority that the product does not yet support.

### Long-Term Implication

Monitoring should begin as structured review triggers and human-controlled signals. Automated monitoring should only be considered after evaluation and evidence practices are stronger.

## Decision 7: Reject Multi-Agent Orchestration For Now

### Decision

The project avoids multi-agent orchestration for the current roadmap.

### Rationale

The product does not need multiple autonomous agents to deliver its current value. The existing deterministic workflow is easier to test, explain, and review.

### Alternatives Considered

- Add multiple agents for research, critique, synthesis, and review.
- Add agent debate or planner-executor loops.

### Why Rejected

Multi-agent orchestration would add complexity without a clear evaluation benefit. It could also make outputs harder to reproduce and explain.

### Long-Term Implication

Any future orchestration should be justified by a measurable decision-quality improvement, not by architecture novelty.

## Decision 8: Avoid Unnecessary Infrastructure

### Decision

The project avoids login systems, databases, multi-user infrastructure, and cloud deployment unless explicitly required by a future product need.

### Rationale

The current product is local, single-user, and portfolio-oriented. Adding infrastructure would increase maintenance burden and distract from the core product question: whether the system improves decision-support quality.

### Alternatives Considered

- Add authentication.
- Add persistent database storage.
- Add hosted SaaS deployment architecture.
- Add account management.

### Why Rejected

These features do not improve the current decision-support workflow. They would expand the operational surface without making the product more mature.

### Long-Term Implication

Infrastructure should remain proportional. If a future version needs persistence or collaboration, those requirements should be documented before implementation.

## Decision 9: Preserve Local, Reviewable Artifacts

### Decision

Each analysis run should continue producing local artifacts that can be inspected outside the browser.

### Rationale

Artifacts support review, reproducibility, debugging, and portfolio evaluation. They make the workflow visible rather than ephemeral.

### Alternatives Considered

- Show only browser output.
- Store only minimal response data.
- Prioritize conversational interaction over artifact generation.

### Why Rejected

Browser-only output would make the system harder to audit. Minimal artifacts would weaken traceability and long-term evaluation.

### Long-Term Implication

Future versions should preserve and improve artifact quality, especially for evaluation, evidence review, and failure-mode tracking.
