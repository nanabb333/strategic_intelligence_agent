# Intelligence Dataset Audit

## Overview

The historical outcome database now contains 55 curated educational cases in `knowledge_base/historical_outcomes.csv`.

- **Previous case count:** 20
- **Current case count:** 55
- **Rows added in V9:** 35
- **Source status approach:** URLs are not fabricated; rows use `source pending; educational summary` until source-grounded citations are added.

## Family Distribution

| Event Family | Case Count |
| --- | ---: |
| Export Controls | 9 |
| Supply Chain Disruption | 9 |
| Industrial Policy | 8 |
| Sanctions | 7 |
| Regulatory Action | 6 |
| Geopolitical Escalation | 5 |
| Technology Competition | 5 |
| Trade Policy | 2 |
| Corporate Strategic Response | 2 |
| Earnings / Corporate Disclosure | 1 |
| Financial / Earnings Geopolitical Exposure | 1 |

## Mechanism Distribution

Mechanisms are inferred from case family and case descriptions for audit purposes. They are not separate factual claims.

| Mechanism Cluster | Approximate Coverage |
| --- | ---: |
| Compliance Burden | 19 |
| Market Access Restriction | 18 |
| Strategic Dependency | 17 |
| Supply Chain Reconfiguration | 16 |
| Technology Containment | 14 |
| Counterparty Risk | 12 |
| Industrial Subsidy / Public Capacity Support | 8 |
| Regulatory Shock | 6 |
| Security Escalation | 5 |
| Information Uncertainty | 5 |
| Corporate Exposure Mapping | 4 |

## Confidence Distribution

| Confidence | Case Count |
| --- | ---: |
| High | 12 |
| Medium | 39 |
| Low | 4 |

## Coverage Assessment

The expanded dataset now covers the core portfolio domains: export controls, sanctions, industrial policy, supply chain disruption, technology competition, regulatory action, geopolitical escalation, corporate strategic response, and financial / earnings geopolitical exposure.

## Remaining Gaps

- Source-grounded citations are still pending.
- Some domains have stronger coverage than others.
- Financial / earnings geopolitical exposure has only one dedicated row.
- Mechanism distribution is inferred for audit readability rather than stored as a normalized column.
- The dataset remains educational and should not be treated as a factual research database without expert review.
