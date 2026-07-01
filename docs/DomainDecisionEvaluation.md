# Domain Decision Evaluation

Version 4 Sprint 4 adds deterministic domain decision evaluation frameworks for professional reviewer workflows.

Domain evaluation expands Decision Intelligence beyond generic pathway drafting by mapping evidence into domain-specific exposure, risk, constraint, assumption, unknown, and reviewer-question structures.

It does not tell reviewers what to buy, sell, allocate, approve, reject, or do.

## Supported Domains

Initial domains:

- Investment / Asset Allocation Evaluation
- Credit Risk Evaluation
- Insurance Business Evaluation

Each domain result includes:

- applicable framework
- evaluation dimensions
- evidence references
- risk categories
- constraints
- assumptions
- unknowns
- reviewer questions
- limitation notes
- domain issues

No output includes recommendation scores, rankings, best options, transaction instructions, or market probabilities.

## Investment / Asset Allocation Evaluation

The investment framework evaluates macro-sensitive exposure dimensions such as:

- interest rate sensitivity
- inflation exposure
- duration risk
- equity valuation risk
- earnings sensitivity
- liquidity risk
- credit spread risk
- FX exposure
- commodity exposure
- policy risk
- recession sensitivity
- market sentiment
- portfolio concentration
- downside protection

It can identify dimensions relevant to scenarios such as Federal Reserve rate changes, inflation shock, recession risk, liquidity tightening, and policy uncertainty.

This is not investment advice. It does not recommend securities, asset classes, weights, or transactions.

## Credit Risk Evaluation

The credit framework maps evidence into dimensions such as:

- default risk
- leverage risk
- liquidity risk
- refinancing risk
- interest coverage
- cash flow stability
- covenant risk
- counterparty risk
- collateral quality
- credit spread signal
- rating action risk
- sector credit pressure

This is not a credit rating. The system does not invent ratings or imply issuer quality beyond evidence-backed reviewer aids.

## Insurance Business Evaluation

The insurance framework maps evidence into dimensions such as:

- underwriting risk
- claims risk
- loss ratio
- combined ratio
- reserve adequacy
- reinsurance exposure
- catastrophe exposure
- premium growth
- policy retention
- investment portfolio sensitivity
- solvency capital
- regulatory capital requirement
- pricing adequacy
- fraud risk
- mortality / morbidity risk

This helps reviewers evaluate insurance business evidence. It is not investment advice or legal advice.

## Regulatory / Suitability Overlay

The overlay flags cautious review considerations such as:

- investment suitability
- fiduciary duty
- securities disclosure
- capital requirement
- solvency requirement
- insurance regulation
- risk disclosure
- conflict of interest
- jurisdiction-specific review

Reviewer language remains cautious:

- “May require compliance review”
- “Reviewer should verify jurisdiction and applicability”
- “Potential suitability or disclosure consideration”

The system does not conclude legality, compliance, suitability, or regulatory sufficiency.

## API

The read-only endpoint is:

```text
GET /projects/{project_id}/decision/domain-evaluation
```

It reads the project question, project context, and accepted project evidence.

It does not mutate project state, retrieve evidence, generate a Decision Brief, rank options, or recommend investment actions.

## Dashboard Panel

The dashboard includes a compact read-only `Domain Decision Evaluation` panel.

It shows:

- applicable domain
- key evaluation dimensions
- risk exposure areas
- missing evidence
- regulatory / suitability flags
- reviewer questions

The panel is for reviewer analysis only.

## Integration

Decision Readiness consumes domain evaluation issues so domain-specific evidence gaps are visible before pathway drafting.

Decision Pathway Drafts can carry domain-specific risks, assumptions, unknowns, evidence refs, and limitation notes.

Decision Brief generation remains unchanged.

## Boundaries

Domain Decision Evaluation is not:

- investment advice
- personalized financial advice
- a credit rating
- legal advice
- a forecast
- autonomous research
- autonomous monitoring
- an allocation engine

The reviewer remains responsible for evidence verification, compliance review, domain judgment, and final decisions.
