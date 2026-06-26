# Demo Scenarios

These scenarios are designed for portfolio review and local product demonstration. They use capabilities the current repository supports: pasted text, uploaded text/Markdown/PDF files, user-provided readable URLs, local retrieval, structured briefs, and downloadable artifacts.

## 1. Semiconductor Export Controls

**User question:** What decision should a semiconductor supplier consider after new export controls affect advanced equipment and customer eligibility?

**Input type:** Pasted policy excerpt or uploaded Markdown file.

**Expected output:** Scenario classification, affected actors, decision criteria, mechanisms such as technology containment and market access restriction, historical analogues, historical outcomes, strategic lessons, decision paths, and monitoring points.

**Capability demonstrated:** Export-control reasoning, historical analogue retrieval, outcome retrieval, and criteria-driven recommendation structure.

**Why it is useful:** Reviewers can see how the app turns a policy headline into operational decision-support material.

## 2. Semiconductor Supply Chain Exposure

**User question:** How should a company evaluate supply chain exposure after a constraint on advanced chip components?

**Input type:** Pasted internal memo, supplier note, or uploaded `.txt` file.

**Expected output:** Issue extraction, supplier/customer exposure framing, supply chain mechanisms, historical cases, action timeline, monitoring triggers, and limitations.

**Capability demonstrated:** Supply-chain event classification and separation of actions from monitoring.

**Why it is useful:** The output helps structure discussion around exposure mapping, resilience, margin impact, and execution complexity.

## 3. Industrial Policy Incentives

**User question:** What should management consider when evaluating a new subsidy or domestic production incentive?

**Input type:** Pasted policy summary or readable URL.

**Expected output:** Industrial policy scenario, decision criteria such as eligibility, execution complexity, capital requirements, compliance burden, and strategic flexibility, plus historical analogues and lessons.

**Capability demonstrated:** Business strategy analysis with policy and regulatory context.

**Why it is useful:** The brief can help teams compare participation, monitoring, and staged-response options without treating the incentive as automatically favorable.

## 4. Banking Earnings And Geopolitical Exposure

**User question:** What risks should analysts monitor after a bank reports earnings pressure tied to geopolitical exposure?

**Input type:** Pasted earnings excerpt or uploaded Markdown file.

**Expected output:** Earnings/geopolitical exposure framing, extracted actors, relevant mechanisms, historical response patterns, evidence assessment, decision paths, and monitoring points.

**Capability demonstrated:** Cross-domain reasoning across earnings, geopolitical exposure, and business risk communication.

**Why it is useful:** The app helps turn a dense earnings note into an executive-ready discussion of exposure, uncertainty, and follow-up evidence.

## 5. Corporate Strategic Response

**User question:** Should a company maintain its current posture, prepare staged adjustments, or change operations immediately?

**Input type:** Pasted management memo or uploaded text file.

**Expected output:** Decision criteria, option cards, option ranking, preferred path, trade-offs, assumptions, historical evidence, and action timeline.

**Capability demonstrated:** Decision-first output architecture and recommendation transparency.

**Why it is useful:** This demonstrates the app as a decision workspace rather than a long-form summary generator.

## 6. Shipping And Supply Chain Disruption

**User question:** What should a supply-chain team monitor after a disruption affects a key shipping route?

**Input type:** Pasted logistics update, article excerpt, or readable URL.

**Expected output:** Supply chain disruption scenario, mechanisms such as rerouting and cost pressure, historical analogues, observed outcomes, strategic lessons, action timeline, and monitoring considerations.

**Capability demonstrated:** Operational risk analysis using local historical patterns and decision-support formatting.

**Why it is useful:** The output helps separate immediate operational actions from the evidence that would change the current recommendation.

## Demo Guidance

For a clean demo:

1. Start the local server with `python3 -m uvicorn app:app --reload`.
2. Open `http://127.0.0.1:8000/dashboard/`.
3. Paste one scenario input or upload a local text/Markdown file.
4. Run the analysis.
5. Download Markdown, TXT, and JSON artifacts.
6. Inspect the run folder under `outputs/runs/`.

The demo should not be presented as real-time monitoring, forecasting, investment advice, legal advice, or geopolitical prediction.

## Related Documentation

- [README](../README.md)
- [Documentation Index](DocumentationIndex.md)
- [Product Overview](ProductOverview.md)
- [Portfolio Narrative](PortfolioNarrative.md)
- [Engineering Architecture](EngineeringArchitecture.md)
