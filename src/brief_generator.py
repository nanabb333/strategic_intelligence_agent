"""Executive brief generation for Strategic Intelligence Agent."""

from context_retriever import CurrentContext
from event_context import EventContext
from event_understanding import EventUnderstanding
from historical_retriever import HistoricalAnalogue
from implication_analyzer import ImplicationAnalysis
from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification


DISCLAIMER = (
    "This output is for decision-support and analyst productivity only. It does not provide "
    "forecasts, probabilities, trading advice, or investment recommendations."
)


def _bullet_list(items: list[str], empty_message: str) -> list[str]:
    if not items:
        return [f"- {empty_message}"]
    return [f"- {item}" for item in items]


def _article_for(value: str) -> str:
    return "an" if value[:1].lower() in {"a", "e", "i", "o", "u"} else "a"


def _format_distribution(distribution: dict[str, int]) -> str:
    if not distribution:
        return "None"
    return ", ".join(f"{key}: {value}" for key, value in sorted(distribution.items()))


def _format_event_context(event_context: EventContext | None) -> list[str]:
    if not event_context:
        return ["- No current-event context was extracted."]
    lines = [
        f"- **Event type:** {event_context.event_type}",
        f"- **Primary actor:** {event_context.primary_actor}",
        f"- **Secondary actor:** {event_context.secondary_actor}",
        f"- **Affected sectors:** {', '.join(event_context.affected_sectors) or 'Not specified'}",
        f"- **Affected regions:** {', '.join(event_context.affected_regions) or 'Not specified'}",
        f"- **Policy domain:** {event_context.policy_domain}",
        f"- **Strategic significance:** {event_context.strategic_significance}",
        f"- **Event summary:** {event_context.event_summary}",
        f"- **Confidence:** {event_context.confidence}",
        "- **Evidence trace:** Source Document + deterministic current-event rules",
    ]
    if event_context.context_limitations:
        lines.append("- **Limitations:** " + " ".join(event_context.context_limitations))
    return lines


def _filter_outcomes_for_event(outcomes, event_understanding: EventUnderstanding | None):
    if not event_understanding or not event_understanding.relevant_families:
        return outcomes
    relevant = {family.lower() for family in event_understanding.relevant_families}
    filtered = [outcome for outcome in outcomes if outcome.event_family.lower() in relevant]
    return filtered if filtered else outcomes[:2]


def _matching_analogue(outcome, analogues: list[HistoricalAnalogue]) -> HistoricalAnalogue | None:
    outcome_name = getattr(outcome, "case_name", "").lower()
    for analogue in analogues:
        analogue_name = analogue.case_title.lower()
        if outcome_name in analogue_name or analogue_name in outcome_name:
            return analogue
    return None


def _analogue_comparison(outcome, analogue: HistoricalAnalogue | None) -> str:
    if analogue:
        return analogue.similarity_reason or analogue.business_relevance or "Retrieved as a structurally similar historical analogue."
    return getattr(outcome, "retrieval_reason", "") or "Retrieved from the repository's historical outcome records as a comparable case."


def _historical_reference_status(outcome, analogue: HistoricalAnalogue | None) -> str:
    if analogue and _is_valid_url(analogue.source_url):
        source_type = analogue.source_type if analogue.source_type != "source pending" else "Primary source"
        return f"{source_type}; repository historical analogue record."
    if getattr(outcome, "source_status", ""):
        return "Curated repository historical knowledge record; primary source link pending."
    return "Curated repository historical knowledge record."


def _historical_reference(outcome, analogue: HistoricalAnalogue | None) -> str:
    if analogue and _is_valid_url(analogue.source_url):
        title = _historical_reference_label(outcome, analogue)
        source_type = analogue.source_type if analogue.source_type != "source pending" else "Primary source"
        return f"{title}. {source_type}. URL: {analogue.source_url.strip()}."
    return "No primary source link available."


def _historical_reference_label(outcome, analogue: HistoricalAnalogue) -> str:
    title = analogue.source_title if analogue.source_title != "source pending" else analogue.case_title
    year = analogue.year or getattr(outcome, "year", "")
    return f"{title}, {year}" if year and year not in title else title


def _source_reference(source_url: str) -> str:
    if _is_valid_url(source_url):
        return f"User-provided source. URL: {source_url.strip()}."
    return "No primary source link available."


def _is_valid_url(value: str) -> bool:
    clean = value.strip()
    return clean.startswith(("http://", "https://")) and " " not in clean


def _sentence(value: str) -> str:
    text = value.strip()
    if not text:
        return ""
    return text if text.endswith((".", "!", "?")) else f"{text}."


def _decision_confidence(similar_cases_count: int, has_event_family: bool) -> str:
    if similar_cases_count >= 3 and has_event_family:
        return "Medium"
    if similar_cases_count >= 1:
        return "Medium"
    return "Low"


def _decision_position(event_family: str) -> str:
    if event_family in {"Corporate Restructuring", "Earnings Shock", "Financial Product Risk"}:
        return "Gradual monitoring and staged adjustment"
    if event_family in {"Trade Restriction", "Economic Coercion", "State Support", "Supply Chain Disruption"}:
        return "Monitor closely and prepare staged response options"
    return "Maintain flexibility while gathering decision-relevant evidence"


def _issue_text(issue: ExtractedIssue) -> str:
    return " ".join(
        [
            issue.title,
            issue.summary,
            issue.core_issue,
            " ".join(issue.industries),
            " ".join(issue.policy_terms),
            issue.document_type_guess,
        ]
    ).lower()


def _decision_profile(issue: ExtractedIssue, event_family: str) -> dict[str, object]:
    text = _issue_text(issue)
    if any(term in text for term in ["insurance savings product", "surrender", "treasur", "bond etf", "fx exposure", "usd-denominated"]):
        return {
            "position": "Do not commit until product costs, liquidity limits, FX exposure, and alternatives are compared",
            "why": "The decision depends less on the headline yield and more on surrender costs, liquidity constraints, issuer exposure, tax treatment, FX risk, and whether simpler USD alternatives meet the same need.",
            "next": "Compare the product with USD deposits, Treasuries, and bond ETFs; request surrender-cost schedules; review FX exposure; and document suitability questions before any commitment.",
            "question": "The key question is not whether the product offers an attractive headline yield, but whether it improves the family's liquidity and risk position after fees, surrender terms, FX exposure, and alternatives are compared.",
            "option_a": "Do not buy now / keep existing cash alternatives",
            "option_b": "Run a structured comparison before deciding",
            "option_c": "Commit immediately to the product",
            "preferred": "Option B currently ranks first because it preserves choice while forcing the product to compete against simpler USD deposits, Treasuries, and bond ETFs on cost, liquidity, risk, and reversibility.",
            "why_holds": [
                "Why this is true: yield products can look attractive before surrender terms, FX exposure, fees, and liquidity constraints are included.",
                "Compared with what: Option A may miss a suitable product, while Option C can lock the user into terms that are hard to reverse.",
                "Under what assumptions: the user has not yet compared net yield, liquidity, surrender costs, and issuer/product risk against simpler USD alternatives.",
                "What would make it wrong: a documented comparison shows the product has clear net advantages, acceptable liquidity, transparent costs, and suitability review support.",
            ],
            "monitoring": [
                ("Net yield after fees and surrender costs", "Shows whether the product remains attractive after real exit and holding costs are included."),
                ("Liquidity and lock-up terms", "Determines whether the product can support expected cash needs without forced penalties."),
                ("FX exposure between TWD and USD", "Clarifies whether currency movement could offset the stated USD yield benefit."),
                ("Comparison with USD deposits, Treasuries, and bond ETFs", "Tests whether a simpler, more liquid alternative solves the same problem."),
                ("Suitability documentation and risk disclosure", "Creates evidence that the decision was reviewed against the user's needs rather than sold on headline yield."),
            ],
            "actions": [
                "Request a one-page comparison against USD deposits, Treasuries, and bond ETFs using net yield, liquidity, costs, and risk.",
                "Ask for the surrender-cost schedule and identify the break-even holding period.",
                "Map expected USD cash needs before accepting any lock-up period.",
                "Document the FX exposure and whether the product creates concentration in one issuer, currency, or structure.",
            ],
        }
    if any(term in text for term in ["taiwan", "asset allocation", "real estate", "singapore", "future cash flow", "usd liquidity"]):
        return {
            "position": "Use staged diversification planning through future cash flow before selling existing assets",
            "why": "The decision is mainly about concentration, liquidity timing, and sequencing; forced sales can create tax, transaction-cost, and family-governance problems before the target allocation is clear.",
            "next": "Estimate current Taiwan / US / Singapore exposure, map future USD cash needs, define a review schedule, and use new cash flow first before selling existing assets.",
            "question": "The key question is not whether diversification is good in general, but how to reduce concentration while preserving liquidity, family flexibility, and decision discipline.",
            "option_a": "Keep the current allocation unchanged",
            "option_b": "Use future cash flow for staged diversification",
            "option_c": "Sell existing assets immediately to rebalance",
            "preferred": "Option B currently ranks first because it reduces concentration over time while avoiding premature sales, transaction costs, and family-governance friction.",
            "why_holds": [
                "Why this is true: concentration risk can be reduced through sequencing, not only immediate asset sales.",
                "Compared with what: Option A leaves concentration unchanged, while Option C may create tax, timing, liquidity, or family-consensus issues.",
                "Under what assumptions: there is enough future cash flow or investable liquidity to begin diversification without forced liquidation.",
                "What would make it wrong: near-term USD liabilities, liquidity stress, or unacceptable Taiwan concentration may require faster action with professional review.",
            ],
            "monitoring": [
                ("Current Taiwan / US / Singapore exposure", "Shows whether concentration risk is actually material and where diversification would matter."),
                ("Future USD cash needs", "Determines whether liquidity should be built before higher-return or less-liquid assets are considered."),
                ("New cash flow available for diversification", "Allows staged adjustment without selling existing assets immediately."),
                ("Review schedule and decision owner", "Prevents the plan from becoming vague intent without follow-through."),
                ("Tax, transaction-cost, and estate-planning constraints", "Identifies issues that can make immediate sales inefficient or risky."),
            ],
            "actions": [
                "Create a current allocation map across Taiwan, US, Singapore, currency, liquidity, and asset type.",
                "Estimate 12-24 month USD cash needs before deciding what to buy or sell.",
                "Use future cash flow first for any staged diversification plan.",
                "Set a quarterly review schedule with trigger points for faster action if liquidity needs change.",
            ],
        }
    if any(term in text for term in ["export control", "licensing", "customer eligibility", "advanced chip", "semiconductor"]):
        return {
            "position": "Monitor closely and prepare staged response options",
            "why": "The decision turns on licensing approval delays, customer eligibility, supplier concentration, compliance cost, and whether management guidance treats the issue as temporary or structural.",
            "next": "Review supplier exposure, licensing requirements, customer eligibility, compliance costs, and margin commentary over the next 30-90 days.",
            "question": "The key question is not only what the export control says, but whether it creates a temporary compliance adjustment or a structural market-access constraint.",
            "option_a": "Wait for final rule detail before changing operations",
            "option_b": "Map exposure and prepare staged adjustments",
            "option_c": "Immediately reduce exposed customers, suppliers, or product lines",
            "preferred": "Option B currently ranks first because it ranks above Option A by reducing blind exposure, and above Option C by avoiding premature disruption before licensing details and customer eligibility are clear.",
            "why_holds": [
                "Why this is true: export-control cases often move from announcement risk into licensing, screening, and supplier/customer review work.",
                "Compared with what: Option A leaves the team exposed to rule-detail surprises, while Option C may cut relationships before the actual restricted scope is known.",
                "Under what assumptions: the rule details, customer eligibility, and license timing remain uncertain enough to make staged preparation more robust than immediate withdrawal.",
                "What would make it wrong: binding restrictions, license denials, severe customer loss, or management guidance showing structural revenue or margin damage.",
            ],
            "monitoring": [
                ("Customer eligibility and restricted end-user exposure", "Shows whether market access is actually constrained or only administratively delayed."),
                ("Licensing approval timing and denial patterns", "Indicates whether the issue is becoming an operating bottleneck."),
                ("Supplier concentration in controlled tools or inputs", "Identifies where disruption could spread through the supply chain."),
                ("Compliance staffing, documentation, and legal cost", "Shows whether the control is becoming a durable operating burden."),
                ("Management guidance on revenue, margins, and product segmentation", "Connects policy exposure to business impact."),
            ],
            "actions": [
                "Review supplier exposure to controlled equipment, inputs, and restricted jurisdictions.",
                "List products and customers requiring license or eligibility review.",
                "Track compliance cost and staffing needs as a separate operating signal.",
                "Prepare an executive update separating confirmed restrictions from unresolved rule details.",
            ],
        }
    if any(term in text for term in ["earnings", "sanctions", "compliance costs", "regional demand", "shipping expenses", "margins"]):
        return {
            "position": "Monitor closely and test whether pressure is temporary or structural",
            "why": "The decision depends on whether margin pressure comes from temporary costs or durable exposure to sanctions compliance, demand weakness, shipping costs, and customer concentration.",
            "next": "Track guidance revisions, compliance staffing, regional revenue exposure, shipping cost absorption, and margin commentary.",
            "question": "The key question is not only why earnings weakened, but whether the drivers are temporary cost items or a structural exposure problem.",
            "option_a": "Treat the weakness as temporary and wait for another reporting cycle",
            "option_b": "Monitor drivers and prepare a staged response",
            "option_c": "Immediately assume structural deterioration",
            "preferred": "Option B currently ranks first because it ranks above Option A by isolating the drivers now, and above Option C by waiting for evidence that pressure is durable rather than temporary.",
            "why_holds": [
                "Why this is true: earnings pressure can reflect temporary cost timing, but geopolitical exposure can also become recurring compliance and revenue friction.",
                "Compared with what: Option A risks ignoring early structural signals, while Option C may overstate durability before management guidance confirms it.",
                "Under what assumptions: the company has not yet shown whether sanctions cost, shipping expense, and demand weakness are recurring.",
                "What would make it wrong: repeated guidance cuts, persistent regional revenue weakness, customer loss, or rising compliance cost without offset.",
            ],
            "monitoring": [
                ("Guidance revisions and margin bridge", "Shows whether management sees the pressure as temporary or recurring."),
                ("Sanctions compliance staffing and cost", "Indicates whether control burden is becoming structural."),
                ("Regional demand and customer concentration", "Connects geopolitical exposure to revenue risk."),
                ("Shipping expense and cost pass-through", "Shows whether logistics pressure is hitting margins or customers."),
                ("Management language on visibility", "Helps distinguish one-quarter noise from durable uncertainty."),
            ],
            "actions": [
                "Separate margin pressure into compliance, shipping, demand, and pricing components.",
                "Track whether management guidance changes before the next reporting cycle.",
                "Prepare a short risk note on regional and customer concentration.",
                "Compare current language with prior earnings disclosures for signs of deterioration.",
            ],
        }
    if any(term in text for term in ["red sea", "shipping", "transit", "insurance costs", "supplier delivery", "logistics"]):
        return {
            "position": "Prepare continuity options while monitoring whether disruption persists",
            "why": "The decision depends on route duration, insurance cost, delivery commitments, supplier concentration, and whether customers need revised timing communication.",
            "next": "Track transit times, freight and insurance costs, supplier delivery variance, inventory coverage, and customer communication needs over the next quarter.",
            "question": "The key question is not whether shipping is disrupted, but whether the disruption is manageable through routing and inventory or requires broader operating-model changes.",
            "option_a": "Absorb delays and wait for route normalization",
            "option_b": "Prepare alternate routing, inventory, and customer communication plans",
            "option_c": "Shift suppliers or logistics model immediately",
            "preferred": "Option B currently ranks first because it ranks above Option A by reducing delivery blind spots, and above Option C by avoiding costly network changes before disruption persistence is clear.",
            "why_holds": [
                "Why this is true: supply-chain disruptions often start as delay problems but become customer, inventory, and cost-management problems if they persist.",
                "Compared with what: Option A may underprepare customer commitments, while Option C may overreact to a disruption that remains temporary.",
                "Under what assumptions: alternate routing and inventory buffers are available but the duration of disruption remains uncertain.",
                "What would make it wrong: sustained route closure, severe insurance cost increases, inventory stockouts, or customer penalties.",
            ],
            "monitoring": [
                ("Transit-time variance by route", "Shows whether delay is stabilizing or spreading."),
                ("Freight and insurance cost changes", "Indicates whether the disruption is becoming margin pressure."),
                ("Inventory coverage for affected SKUs or inputs", "Reveals how long operations can continue before delivery risk becomes customer risk."),
                ("Supplier delivery reliability", "Identifies whether disruption is concentrated or systemic."),
                ("Customer communication and penalty exposure", "Shows whether the issue is becoming a commercial commitment problem."),
            ],
            "actions": [
                "Map affected lanes, suppliers, customers, and delivery commitments.",
                "Prepare alternate-route and inventory-buffer options with cost estimates.",
                "Define which customers need proactive delivery communication.",
                "Review whether contract penalties or service-level commitments are exposed.",
            ],
        }
    return {
        "position": _decision_position(event_family),
        "why": "Historical cases suggest the first headline is rarely the full impact; the real risk usually appears through implementation details, exposure mapping, compliance burden, customer eligibility, margins, or management reaction.",
        "next": "Track management guidance, supplier/customer exposure, implementation details, margin pressure, and whether the issue remains temporary or becomes structural.",
        "question": "",
        "option_a": "Maintain current position / wait for more evidence",
        "option_b": "Gradual adjustment / monitor and prepare",
        "option_c": "Immediate defensive action",
        "preferred": "Option B currently ranks first because it preserves flexibility while reducing the risk of being forced to react later under worse conditions.",
        "why_holds": _assumption_text(event_family),
        "monitoring": _monitoring_signals("", issue),
            "actions": [
                "Build a short exposure map covering affected suppliers, customers, products, regions, and workflows.",
                "Define trigger points that would move the decision from Option B to Option A or Option C.",
                "Prepare a one-page decision update using named exposure, cost, customer, supplier, and reversibility indicators.",
                "Keep historical cases as comparison evidence, not as proof that the same outcome will occur.",
            ],
    }


def _decision_question(event_type: str, profile: dict[str, object] | None = None) -> str:
    if profile and profile.get("question"):
        return str(profile["question"])
    return (
        f"The key question is not only what happened in this {event_type.lower()}, "
        "but whether it creates a temporary adjustment problem or a deeper structural risk."
    )


DecisionCriterion = tuple[str, str, str]


def _decision_criteria(issue: ExtractedIssue, profile: dict[str, object]) -> list[DecisionCriterion]:
    text = _issue_text(issue)
    if any(term in text for term in ["insurance savings product", "surrender", "treasur", "bond etf", "fx exposure", "usd-denominated"]):
        return [
            ("Net return after costs", "High", "Headline yield is insufficient unless fees and surrender charges are included."),
            ("Liquidity", "High", "The product must match expected USD cash needs without forced penalties."),
            ("FX exposure", "Medium", "Currency movement can offset the apparent USD yield benefit."),
            ("Alternative simplicity", "High", "USD deposits, Treasuries, and bond ETFs may solve the same need with fewer constraints."),
            ("Product suitability evidence", "High", "The decision should be documented against user needs, not sales language."),
        ]
    if any(term in text for term in ["taiwan", "asset allocation", "real estate", "singapore", "future cash flow", "usd liquidity"]):
        return [
            ("Jurisdiction concentration", "High", "The starting risk is overexposure to one geography or legal environment."),
            ("Liquidity", "High", "Future USD obligations require cash-flow timing before return-seeking decisions."),
            ("Opportunity cost", "Medium", "The plan should not sacrifice useful upside before the target allocation is clear."),
            ("Execution complexity", "Medium", "Immediate sales can create tax, transaction, and family-governance friction."),
            ("Flexibility", "High", "Using future cash flow preserves optionality while reducing concentration over time."),
            ("Review discipline", "Medium", "A schedule prevents diversification from remaining an abstract goal."),
        ]
    if any(term in text for term in ["export control", "licensing", "customer eligibility", "advanced chip", "semiconductor"]):
        return [
            ("Customer exposure", "High", "Restricted end-user exposure determines whether market access is actually constrained."),
            ("Licensing uncertainty", "High", "Approval timing and denial patterns determine operating bottlenecks."),
            ("Compliance burden", "Medium", "Documentation, staffing, and review costs can become durable operating work."),
            ("Margin impact", "High", "Costs matter if they flow through to revenue, pricing, or profitability."),
            ("Supply chain resilience", "Medium", "Supplier concentration determines whether disruption spreads beyond legal review."),
        ]
    if any(term in text for term in ["earnings", "sanctions", "compliance costs", "regional demand", "shipping expenses", "margins"]):
        return [
            ("Margin durability", "High", "The key distinction is temporary cost pressure versus recurring margin damage."),
            ("Guidance credibility", "High", "Management commentary shows whether visibility is improving or deteriorating."),
            ("Compliance burden", "Medium", "Staffing and control costs indicate whether geopolitical exposure is becoming structural."),
            ("Regional demand exposure", "High", "Customer and geography concentration determine revenue sensitivity."),
            ("Cost pass-through", "Medium", "Pricing power affects whether shipping or compliance costs hit margins."),
        ]
    if any(term in text for term in ["red sea", "shipping", "transit", "insurance costs", "supplier delivery", "logistics"]):
        return [
            ("Delivery reliability", "High", "Transit-time variance determines whether the issue is manageable or customer-facing."),
            ("Cost impact", "High", "Freight and insurance costs determine whether disruption becomes margin pressure."),
            ("Inventory coverage", "High", "Buffer depth determines how long operations can absorb delay."),
            ("Supplier concentration", "Medium", "Single-route or single-supplier exposure determines resilience."),
            ("Customer communication", "Medium", "Service commitments determine whether operational disruption becomes commercial risk."),
        ]
    return [
        ("Exposure severity", "High", "The decision depends on whether exposure is limited or material."),
        ("Reversibility", "High", "Lower-reversibility actions require stronger evidence."),
        ("Execution burden", "Medium", "Operational difficulty affects whether preparation is realistic."),
        ("Information value", "Medium", "The preferred path should create useful evidence for the next review."),
    ]


def _top_criteria(criteria: list[DecisionCriterion], limit: int = 3) -> list[str]:
    high = [name for name, importance, _ in criteria if importance == "High"]
    selected = high if high else [name for name, _, _ in criteria]
    return selected[:limit]


def _decision_options(profile: dict[str, object] | None = None) -> list[tuple[str, str, str]]:
    if profile:
        return [
            ("Option A", str(profile.get("option_a", "Maintain current position / wait for more evidence")), "Lowest immediate effort, but can leave blind spots if exposure grows."),
            ("Option B", str(profile.get("option_b", "Gradual adjustment / monitor and prepare")), "Balanced path when evidence is meaningful but still incomplete."),
            ("Option C", str(profile.get("option_c", "Immediate defensive action")), "Highest risk reduction, but hardest to reverse and easiest to overuse."),
        ]
    return [
        ("Option A", "Maintain current position / wait for more evidence", "Best when the event is likely temporary and exposure is limited."),
        ("Option B", "Gradual adjustment / monitor and prepare", "Best when uncertainty is material but immediate defensive action would be premature."),
        ("Option C", "Immediate defensive action", "Best when exposure is already clear, costly, and difficult to reverse."),
    ]


def _option_comparison_rows() -> list[tuple[str, str, str, str, str, str, str]]:
    return [
        ("Option A", "Low", "Low", "Low", "High", "Medium", "High"),
        ("Option B", "Medium", "Medium", "Medium", "Medium", "High", "High"),
        ("Option C", "High", "High", "High", "Low", "Medium", "Low"),
    ]


def _option_cards(
    profile: dict[str, object] | None = None,
    criteria: list[DecisionCriterion] | None = None,
) -> list[dict[str, object]]:
    options = _decision_options(profile)
    criterion_names = [item[0] for item in (criteria or [])]
    high_criteria = _top_criteria(criteria or [])
    key_criteria = ", ".join(high_criteria) or "the highest-importance criteria"
    first_criterion = high_criteria[0] if high_criteria else (criterion_names[0] if criterion_names else "exposure")
    option_b = options[1][1]
    option_c = options[2][1]
    return [
        {
            "name": "Option A",
            "label": options[0][1],
            "meaning": "Hold the current posture until the evidence base is clearer.",
            "appropriate_when": (
                f"Available evidence shows limited exposure, high reversibility, and no deterioration in {key_criteria}."
            ),
            "immediate_actions": [
                f"Document why {options[0][1]} is acceptable.",
                f"Confirm whether {first_criterion.lower()} can be ruled out as a material constraint.",
            ],
            "near_term_actions": [
                "Schedule a dated review rather than leaving the decision open-ended.",
                f"Move to {option_b} if exposure cannot be ruled out with current evidence.",
            ],
            "main_benefit": "Avoids unnecessary disruption when the issue is likely manageable.",
            "main_risk": "May underprepare the organization if exposure is already material.",
            "evidence_preferable": (
                f"This becomes preferable if {key_criteria} remain limited and no monitoring signal shows material change."
            ),
            "recommended": False,
        },
        {
            "name": "Option B",
            "label": option_b,
            "meaning": "Proceed with reversible preparation while delaying irreversible commitments.",
            "appropriate_when": (
                f"Uncertainty is meaningful, especially around {key_criteria}, but evidence does not yet justify a full defensive move."
            ),
            "immediate_actions": [
                f"Build an exposure map covering {key_criteria}.",
                "Assign one decision owner and one review date.",
                "Separate confirmed facts from unresolved assumptions.",
            ],
            "near_term_actions": [
                "Review new evidence at the 30-day and 90-day checkpoints.",
                f"Prepare actions needed if the decision shifts to {options[0][1]} or {option_c}.",
            ],
            "main_benefit": "Preserves flexibility while converting uncertainty into decision-useful evidence.",
            "main_risk": "Can become process activity if the exposure map and review cadence are not owned.",
            "evidence_preferable": (
                f"This remains preferable when {key_criteria} are material enough to monitor but not yet binding."
            ),
            "recommended": True,
        },
        {
            "name": "Option C",
            "label": option_c,
            "meaning": "Take immediate defensive action before waiting for additional clarification.",
            "appropriate_when": (
                f"Evidence shows {first_criterion.lower()} is already binding, costly, customer-facing, or difficult to reverse."
            ),
            "immediate_actions": [
                "Identify the specific customers, suppliers, products, approvals, or workflows to reduce or pause.",
                "Escalate legal, compliance, finance, and operating-owner review before acting.",
            ],
            "near_term_actions": [
                "Confirm whether the defensive action reduced the specific exposure it targeted.",
                "Document the opportunity cost and reversibility of the action taken.",
            ],
            "main_benefit": "Reduces downside quickly when exposure is already severe.",
            "main_risk": "Can sacrifice opportunity or relationships before the evidence supports that cost.",
            "evidence_preferable": (
                f"This becomes preferable if evidence shows {first_criterion.lower()} is severe or worsening."
            ),
            "recommended": False,
        },
    ]


def _option_ranking(
    profile: dict[str, object] | None = None,
    criteria: list[DecisionCriterion] | None = None,
) -> list[tuple[str, str, str]]:
    options = _decision_options(profile)
    top = _top_criteria(criteria or [])
    criterion_text = ", ".join(top) or "the highest-importance criteria"
    first = top[0] if top else "exposure severity"
    return [
        ("1. Option B", options[1][1], f"Ranks first because the highest-importance criteria are {criterion_text}. It improves readiness on those criteria without creating the execution burden of Option C or the underpreparedness of Option A."),
        ("2. Option A", options[0][1], f"Ranks second because it has lower cost and disruption than Option C, but it is weaker than Option B on {criterion_text} if exposure grows."),
        ("3. Option C", options[2][1], f"Ranks third because it offers more protection, but it is weaker on reversibility, opportunity cost, and execution burden unless {first.lower()} is already severe."),
    ]


def _profile_assumptions(profile: dict[str, object], event_family: str) -> list[str]:
    why_holds = [str(item) for item in profile.get("why_holds", [])]
    assumption_lines = [
        line.replace("Under what assumptions:", "").strip()
        for line in why_holds
        if line.lower().startswith("under what assumptions:")
    ]
    option_b = str(profile.get("option_b", "Gradual adjustment / monitor and prepare"))
    option_c = str(profile.get("option_c", "Immediate defensive action"))
    base = assumption_lines or [f"The event remains consistent with {event_family or 'the detected event family'} and no severe contradictory signal has appeared yet."]
    base = [line[:1].upper() + line[1:] if line else line for line in base]
    return [
        *base,
        "The supplied source material is directionally accurate enough to frame the decision, but still requires human fact review before operational use.",
        f"The organization has enough time and management capacity to execute {option_b} before the issue becomes binding.",
        f"No immediate evidence shows that {option_c} is already required.",
    ]


def _profile_tradeoffs(profile: dict[str, object], criteria: list[DecisionCriterion] | None = None) -> list[str]:
    option_b = str(profile.get("option_b", "Gradual adjustment / monitor and prepare"))
    option_a = str(profile.get("option_a", "Maintain current position / wait for more evidence"))
    option_c = str(profile.get("option_c", "Immediate defensive action"))
    top = _top_criteria(criteria or [])
    top_text = ", ".join(top) or "the highest-importance criteria"
    return [
        f"Benefits gained: {option_b} creates an exposure map, assigns ownership, and preserves reversibility while evidence on {top_text} is still developing.",
        "Costs accepted: the recommendation prioritizes execution flexibility and learning over immediate risk elimination, so the team must spend management attention now and tolerate partial exposure while evidence matures.",
        f"Opportunities sacrificed: the user gives up the lowest-effort posture of {option_a} and does not receive the full immediate protection of {option_c}.",
        f"Risks still unresolved: new evidence on {top_text}, implementation timing, cost, customer behavior, or operating constraints may still justify changing paths.",
    ]


def _change_triggers(profile: dict[str, object], criteria: list[DecisionCriterion] | None = None) -> list[str]:
    why_holds = [str(item) for item in profile.get("why_holds", [])]
    wrong_lines = [
        line.replace("What would make it wrong:", "").strip()
        for line in why_holds
        if line.lower().startswith("what would make it wrong:")
    ]
    triggers = wrong_lines or ["Clear evidence that exposure is either immaterial or already severe enough to require a different path."]
    triggers = [line[:1].upper() + line[1:] if line else line for line in triggers]
    top = _top_criteria(criteria or [])
    top_text = ", ".join(top) or "the highest-importance criteria"
    option_a = str(profile.get("option_a", "Maintain current position / wait for more evidence"))
    option_c = str(profile.get("option_c", "Immediate defensive action"))
    return [
        *triggers,
        f"Move toward Option A ({option_a}) if review shows limited exposure, low cost, high reversibility, and no deterioration in {top_text}.",
        f"Move toward Option C ({option_c}) if constraints become binding, costly, customer-facing, or difficult to reverse.",
    ]


def _failure_modes(profile: dict[str, object], criteria: list[DecisionCriterion] | None = None) -> list[str]:
    top = _top_criteria(criteria or [])
    top_text = ", ".join(top) or "the highest-importance criteria"
    option_b = str(profile.get("option_b", "Gradual adjustment / monitor and prepare"))
    return [
        f"The preferred path fails if the review cadence misses rapid deterioration in {top_text}.",
        f"The recommendation is weaker if {option_b} creates process activity without producing a usable exposure map or decision owner.",
        "Historical analogues may mislead if the current actor exposure, timing, or implementation details differ materially from retrieved cases.",
        "Evidence remains insufficient if the supplied material does not confirm organization-specific exposure, costs, customer impact, or operational constraints.",
    ]


def _source_evidence_limitations(source_url: str, has_historical_cases: bool) -> list[str]:
    limitations = [
        "Some evidence is derived from user-provided material rather than independently verified primary sources.",
        "Organization-specific exposure, timing, cost, and implementation data may be missing.",
    ]
    if not _is_valid_url(source_url):
        limitations.append("No primary source link is available for the supplied input material.")
    if has_historical_cases:
        limitations.append(
            "Some historical analogues are based on curated repository knowledge rather than linked source documents."
        )
        limitations.append(
            "Analogue transferability depends on whether the current case shares comparable mechanisms and constraints."
        )
    return limitations


def _role_implications(profile: dict[str, object], criteria: list[DecisionCriterion] | None = None) -> list[str]:
    option_b = str(profile.get("option_b", "Gradual adjustment / monitor and prepare"))
    option_c = str(profile.get("option_c", "Immediate defensive action"))
    top = _top_criteria(criteria or [])
    top_text = ", ".join(top) or "exposure, reversibility, and execution burden"
    return [
        f"CEO / Executive Sponsor: treat {option_b} as a decision-control posture, not a delay tactic; require a named owner and a date for reassessment.",
        f"Corporate Strategy: translate {top_text} into an exposure map that shows which business units, customers, products, or regions are actually affected.",
        "Finance / CFO: separate confirmed financial exposure from possible exposure so the team does not overstate cost, margin, or liquidity impact before evidence supports it.",
        f"Operations / Supply Chain: identify which workflows would need to change if the decision shifts from Option B to {option_c}.",
        "Legal / Compliance: distinguish confirmed obligations from unresolved interpretation questions and document what evidence would change the operating posture.",
    ]


def _decision_blind_spots(criteria: list[DecisionCriterion], monitor_signals: list[tuple[str, str]]) -> list[str]:
    top = _top_criteria(criteria)
    blind_spots = [
        f"Organization-specific data for {criterion.lower()} is still needed to move from a general recommendation to an operating decision."
        for criterion in top[:3]
    ]
    signal_names = [signal for signal, _ in monitor_signals[:2]]
    if signal_names:
        blind_spots.append(f"The current recommendation would improve with fresher evidence on {', '.join(signal_names).lower()}.")
    blind_spots.append("Contractual obligations, customer commitments, and internal execution capacity may change the preferred path even if the external situation is unchanged.")
    return blind_spots[:5]


def _preferred_explanation(profile: dict[str, object], criteria: list[DecisionCriterion] | None = None) -> list[str]:
    option_a = str(profile.get("option_a", "Maintain current position / wait for more evidence"))
    option_c = str(profile.get("option_c", "Immediate defensive action"))
    top = _top_criteria(criteria or [])
    top_text = ", ".join(top) or "the highest-importance criteria"
    return [
        f"Top criteria driving the recommendation: {top_text}.",
        f"Why Option B ranks first: it performs best on the criteria that matter most for this decision, especially {top_text}, while preserving flexibility.",
        "Costs accepted: Option B requires monitoring, ownership, and delayed full protection rather than a one-step defensive move.",
        f"Why Option A does not rank first: {option_a} keeps costs low, but it can leave the user underprepared on {top_text} if exposure grows.",
        f"Why Option C does not rank first: {option_c} offers more protection, but it can impose high opportunity cost before evidence on {top_text} is strong enough.",
        f"What would change the ranking: stronger evidence that {top_text} are either clearly immaterial or clearly severe.",
    ]


def _preferred_path_playbook(
    profile: dict[str, object],
    criteria: list[DecisionCriterion],
    monitor_signals: list[tuple[str, str]],
) -> dict[str, list[str] | str]:
    option_b = str(profile.get("option_b", "Map exposure, preserve flexibility, and prepare staged response options"))
    option_a = str(profile.get("option_a", "Maintain current position / wait for more evidence"))
    option_c = str(profile.get("option_c", "Immediate defensive action"))
    top = _top_criteria(criteria)
    top_text = ", ".join(top) or "exposure, reversibility, and execution burden"
    primary_signal = monitor_signals[0][0] if monitor_signals else "primary exposure indicators"
    secondary_signal = monitor_signals[1][0] if len(monitor_signals) > 1 else "cost and reversibility"
    actions = [str(item) for item in profile.get("actions", [])]
    immediate = actions[:3] or [
        f"Build an exposure map for {top_text}.",
        "Assign one accountable decision owner.",
        "Separate confirmed facts from unresolved assumptions.",
    ]
    return {
        "path": option_b,
        "why_today": [
            f"{option_b} is preferred today because it produces decision evidence on {top_text} without forcing irreversible action.",
            f"{option_a} is too passive if {primary_signal.lower()} is already material.",
            f"{option_c} is premature unless {secondary_signal.lower()} shows binding or costly constraints.",
        ],
        "assumptions": [
            f"The highest-priority unknowns are {top_text}, and they can be clarified through near-term internal work.",
            "The organization can still preserve reversibility while the evidence base improves.",
            "No current evidence requires immediate defensive reduction before exposure is mapped.",
        ],
        "immediate": immediate,
        "stakeholders": [
            "Executive sponsor: owns the go / hold / escalate decision.",
            "Strategy: produces the exposure map and decision memo.",
            "Finance: quantifies revenue, margin, liquidity, or cost exposure where relevant.",
            "Legal / Compliance: separates confirmed obligations from interpretation questions.",
            "Operations / Commercial owner: identifies affected workflows, suppliers, customers, or product commitments.",
        ],
        "checkpoints": [
            "Now: complete the exposure map and list unresolved assumptions.",
            "30 days: decide whether evidence supports holding Option B, de-escalating to Option A, or preparing Option C.",
            "90 days: convert the review into a board or executive decision package if exposure remains material.",
        ],
        "escalation": [
            f"Escalate toward {option_c} if {primary_signal.lower()} becomes binding, customer-facing, costly, or hard to reverse.",
            f"Escalate executive review if {secondary_signal.lower()} moves against planning assumptions.",
        ],
        "exit": [
            f"Exit toward {option_a} if exposure is confirmed as limited, reversible, and not material to the top criteria: {top_text}.",
            f"Exit toward {option_c} if delay creates more downside than the opportunity cost of immediate defensive action.",
        ],
    }


def _action_timeline(profile: dict[str, object], monitor_signals: list[tuple[str, str]]) -> dict[str, list[str]]:
    actions = list(profile.get("actions", []))
    primary_signal = monitor_signals[0][0] if monitor_signals else "primary exposure indicators"
    secondary_signal = monitor_signals[1][0] if len(monitor_signals) > 1 else "cost and reversibility constraints"
    now_action = str(actions[0]) if actions else "Create an exposure map for the current issue."
    now_support = str(actions[1]) if len(actions) > 1 else f"Confirm whether {primary_signal.lower()} is material."
    next_30_action = str(actions[2]) if len(actions) > 2 else f"Review {primary_signal.lower()} and document whether it changes the recommended path."
    next_30_support = str(actions[3]) if len(actions) > 3 else f"Confirm whether {secondary_signal.lower()} has changed."
    next_90 = [
        (
            "- **Action:** Reassess whether the evidence still supports Option B or whether Option A or Option C "
            "has become more appropriate.\n"
            "- **Owner:** Executive sponsor + Strategy.\n"
            "- **Deliverable:** Decision update memo comparing current evidence against the original criteria.\n"
            "- **Decision Outcome:** Hold, de-escalate, or move to a more defensive path."
        ),
    ]
    return {
        "NOW": [
            (
                f"- **Action:** {now_action} {now_support}\n"
                "- **Owner:** Strategy + relevant operating owner.\n"
                "- **Deliverable:** Exposure map with affected customers, suppliers, products, regions, workflows, and open assumptions.\n"
                "- **Decision Purpose:** Confirms whether staged preparation is sufficient or immediate escalation is needed."
            )
        ],
        "NEXT 30 DAYS": [
            (
                f"- **Action:** {next_30_action} {next_30_support}\n"
                "- **Owner:** Strategy + Legal / Compliance + Finance.\n"
                "- **Deliverable:** Readiness checklist showing confirmed facts, unresolved assumptions, and required follow-up.\n"
                "- **Expected Decision:** Hold the staged path, narrow scope, or prepare defensive execution."
            )
        ],
        "NEXT 90 DAYS": next_90,
        "RE-EVALUATION TRIGGER": [
            (
                f"- **Action:** Revisit the recommendation if {primary_signal.lower()}, {secondary_signal.lower()}, "
                "customer impact, cost pressure, or reversibility changes materially.\n"
                "- **Owner:** Executive sponsor.\n"
                "- **Deliverable:** Go / hold / escalate decision record.\n"
                "- **Decision Purpose:** Prevents the recommendation from remaining in force after the evidence changes."
            ),
        ],
    }


def _risk_analysis(
    profile: dict[str, object],
    criteria: list[DecisionCriterion],
    monitor_signals: list[tuple[str, str]],
) -> list[dict[str, str]]:
    top = _top_criteria(criteria)
    option_b = str(profile.get("option_b", "staged response"))
    option_c = str(profile.get("option_c", "immediate defensive action"))
    primary = top[0] if top else "Exposure severity"
    secondary = top[1] if len(top) > 1 else "Reversibility"
    tertiary = top[2] if len(top) > 2 else "Execution burden"
    primary_signal = monitor_signals[0][0] if monitor_signals else primary
    secondary_signal = monitor_signals[1][0] if len(monitor_signals) > 1 else secondary
    return [
        {
            "risk": f"{primary} is higher than the current evidence suggests.",
            "why": f"{option_b} depends on the assumption that exposure can be mapped before it becomes binding.",
            "impact": f"The preferred path may be insufficient and {option_c} may become necessary.",
            "warning": f"{primary_signal} indicates exposure above the planning assumption or cannot be documented.",
            "mitigation": f"Prepare the {option_c} execution checklist before making irreversible commitments.",
        },
        {
            "risk": f"{secondary} deteriorates before the next checkpoint.",
            "why": "The recommendation relies on preserving choice while evidence improves.",
            "impact": "Decision-makers may lose the ability to shift paths without higher cost.",
            "warning": f"{secondary_signal} indicates delay, denial, cost increase, or customer-facing impact.",
            "mitigation": "Set a dated executive checkpoint and require a go / hold / escalate decision record.",
        },
        {
            "risk": f"{tertiary} is underestimated.",
            "why": "A staged path only works if operating teams can produce the required decision artifacts.",
            "impact": "The organization may create review activity without improving the actual decision.",
            "warning": "No accountable owner, incomplete exposure map, or unresolved assumptions at the 30-day checkpoint.",
            "mitigation": "Assign owners by function and make the exposure map, readiness checklist, and decision memo mandatory deliverables.",
        },
    ]


def _regulatory_considerations(issue: ExtractedIssue, scenario: str) -> list[dict[str, str]]:
    text = _issue_text(issue)
    considerations: list[dict[str, str]] = []
    if "export control" in text or "licensing" in text or "restricted" in text:
        considerations.append(
            {
                "area": "Export Controls",
                "why": "Licensing, product classification, end-use, or restricted-party obligations may determine whether execution is allowed.",
                "impact": "Customer, supplier, product, or shipment decisions may need to pause until obligations are confirmed.",
                "review": "Legal / Compliance should prepare a regulatory impact review separating confirmed requirements from open interpretation questions.",
            }
        )
    if "sanction" in text or "restricted party" in text or "payment" in text:
        considerations.append(
            {
                "area": "Sanctions",
                "why": "Counterparty, payment, contract, or regional exposure can restrict execution even when commercial demand exists.",
                "impact": "The organization may need additional screening, payment-channel review, or contract escalation before acting.",
                "review": "Compliance and Treasury should document restricted-party, payment, and contract exposure.",
            }
        )
    if "competition" in text or "self-preferencing" in text or "marketplace" in text or "app store" in text:
        considerations.append(
            {
                "area": "Competition Law",
                "why": "Platform access, ranking, pricing, or complaint-handling rules may affect product and commercial choices.",
                "impact": "Product or commercial teams may need to change operating processes before continuing the current path.",
                "review": "Legal and Product should prepare a competition-risk operating checklist.",
            }
        )
    if "data" in text or "privacy" in text or "governance" in text:
        considerations.append(
            {
                "area": "Data Privacy / Data Governance",
                "why": "Data handling, reporting, or governance obligations may affect product design and compliance evidence.",
                "impact": "Execution may require documentation, access controls, reporting workflows, or data-use review.",
                "review": "Privacy, Data Governance, and Engineering should confirm required controls and evidence artifacts.",
            }
        )
    if "procurement" in text or "subsid" in text or "industrial policy" in text or "domestic" in text:
        considerations.append(
            {
                "area": "Procurement Rules / Industrial Policy Conditions",
                "why": "Eligibility, domestic-content, reporting, or public-funding conditions may affect investment sequencing.",
                "impact": "The preferred path may require compliance readiness before capital commitments or supplier choices.",
                "review": "Strategy, Finance, and Compliance should prepare an eligibility and obligation checklist.",
            }
        )
    if "board" in text or "governance" in text or scenario in {"Earnings / Corporate Disclosure", "Regulatory Action"}:
        considerations.append(
            {
                "area": "Corporate Governance",
                "why": "Material exposure, disclosure language, or control gaps may require executive or board-level review.",
                "impact": "The decision may need a formal memo, risk committee discussion, or documented escalation path.",
                "review": "Executive sponsor should decide whether the next checkpoint requires a board or risk-committee package.",
            }
        )
    return considerations[:4]


def _monitoring_signals(scenario: str, issue: ExtractedIssue) -> list[tuple[str, str]]:
    signals = [
        (
            "Management guidance and operating commentary",
            "Shows whether leaders treat the issue as temporary noise or a structural planning constraint.",
        ),
        (
            "Supplier and customer exposure",
            "Identifies where operational or revenue impact may appear before it is visible in headline summaries.",
        ),
        (
            "Implementation details, licensing rules, exemptions, or timelines",
            "Clarifies whether the event changes actual workflows or remains a broad announcement.",
        ),
        (
            "Margin pressure, cost absorption, or working-capital strain",
            "Helps separate manageable adjustment from business-model stress.",
        ),
        (
            "Evidence of process changes such as compliance reviews, sourcing changes, or customer segmentation",
            "Shows whether organizations are moving from observation to action.",
        ),
    ]
    if "Earnings" in scenario or issue.document_type_guess.lower().startswith("earnings"):
        signals.insert(
            1,
            (
                "Revenue visibility and guidance revisions",
                "Indicates whether the issue is changing expectations around demand, margins, or execution.",
            ),
        )
    return signals[:6]


def _assumption_text(event_family: str) -> list[str]:
    return [
        "Why this is true: comparable cases often moved from headline shock into implementation, exposure mapping, and communication work.",
        "Compared with what: immediate defensive action would reduce some risk but can create high opportunity cost before exposure is clear.",
        f"Under what assumptions: the event is being interpreted as {event_family or 'a strategic event'} and the local cases are relevant enough for comparison.",
        "What would make it wrong: clear evidence of severe exposure, binding rules, customer loss, liquidity stress, or management guidance changing faster than expected.",
    ]


def generate_brief(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    analogues: dict[str, list[HistoricalAnalogue]],
    contexts: dict[str, list[CurrentContext]],
    analyses: list[ImplicationAnalysis],
    agent_route=None,
    mechanisms=None,
    interpretations=None,
    evidence_assessments=None,
    historical_outcomes=None,
    strategic_lessons=None,
    strategic_assessments=None,
    evidence_credibility=None,
    response_patterns=None,
    event_context: EventContext | None = None,
    event_understanding: EventUnderstanding | None = None,
    source_url: str = "",
) -> str:
    """Generate a Markdown executive intelligence brief."""
    classification_by_issue = {item.issue_title: item for item in classifications}
    analysis_by_issue = {item.issue_title: item for item in analyses}

    lines = ["# Executive Intelligence Brief", ""]

    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        scenario = classification.primary_scenario if classification else "Other"
        analysis = analysis_by_issue.get(issue.title)
        issue_analogues = analogues.get(issue.title, [])
        issue_contexts = contexts.get(issue.title, [])
        issue_mechanisms = (mechanisms or {}).get(issue.title, [])
        issue_interpretations = (interpretations or {}).get(issue.title, [])
        issue_assessments = (evidence_assessments or {}).get(issue.title, [])
        issue_historical_outcomes = (historical_outcomes or {}).get(issue.title, [])
        issue_strategic_lessons = (strategic_lessons or {}).get(issue.title, [])
        issue_strategic_assessment = (strategic_assessments or {}).get(issue.title)
        issue_evidence_credibility = (evidence_credibility or {}).get(issue.title)
        issue_response_patterns = (response_patterns or {}).get(issue.title, [])

        if issue_strategic_assessment:
            similar_cases = _filter_outcomes_for_event(issue_historical_outcomes, event_understanding)[:5]
            event_type = issue_strategic_assessment.event_type or "strategic event"
            event_family = issue_strategic_assessment.event_family or scenario
            profile = _decision_profile(issue, event_family)
            current_position = str(profile["position"])
            confidence = _decision_confidence(len(similar_cases), bool(issue_strategic_assessment.event_family))
            monitor_signals = _monitoring_signals(scenario, issue)
            if profile.get("monitoring"):
                monitor_signals = list(profile["monitoring"])  # type: ignore[arg-type]
            why_sentence = str(profile["why"])
            action_timeline = _action_timeline(profile, monitor_signals)
            criteria = _decision_criteria(issue, profile)
            preferred_playbook = _preferred_path_playbook(profile, criteria, monitor_signals)
            risk_analysis = _risk_analysis(profile, criteria, monitor_signals)
            regulatory_considerations = _regulatory_considerations(issue, scenario)
            lines.extend(
                [
                    "## Decision Snapshot",
                    "",
                    f"**Current Position:** {current_position}",
                    f"**Confidence:** {confidence}",
                    f"**Why:** {why_sentence}",
                    f"**Next 30-90 Days:** {profile['next']}",
                    "",
                    "## Decision Question",
                    "",
                    _decision_question(event_type, profile),
                    "",
                    "## Decision Criteria",
                    "",
                    "These are the dimensions driving today's decision:",
                ]
            )
            for name, importance, reason in criteria:
                lines.append(f"- **{name}** — **Importance: {importance}.** {reason}")
            lines.extend(
                [
                    "",
                    "## Decision Paths",
                    "",
                ]
            )
            for option in _option_cards(profile, criteria):
                option_name = str(option["name"])
                label = f"{option_name} (Recommended)" if option["recommended"] else option_name
                lines.extend(
                    [
                        f"### {label}",
                        "",
                        f"**Path:** {option['label']}",
                        "",
                        f"**Meaning:** {option['meaning']}",
                        "",
                        f"**Appropriate when:** {option['appropriate_when']}",
                        "",
                        "**Immediate actions**",
                    ]
                )
                lines.extend(f"- {item}" for item in option["immediate_actions"])
                lines.append("")
                lines.append("**Near-term actions**")
                lines.extend(f"- {item}" for item in option["near_term_actions"])
                lines.append("")
                lines.append(f"**Main benefit:** {option['main_benefit']}")
                lines.append("")
                lines.append(f"**Main risk:** {option['main_risk']}")
                lines.append("")
                lines.append(f"**Evidence that would make this preferable:** {option['evidence_preferable']}")
                lines.append("")

            lines.extend(["## Option Ranking", ""])
            for rank, option_label, reason in _option_ranking(profile, criteria):
                lines.append(f"- **{rank}: {option_label}.** {reason}")
            lines.extend(
                [
                    "",
                    "## Option Comparison",
                    "",
                    "| Option | Risk Reduction | Opportunity Cost | Execution Difficulty | Reversibility | Robustness | Information Value |",
                    "| --- | --- | --- | --- | --- | --- | --- |",
                ]
            )
            for row in _option_comparison_rows():
                lines.append("| " + " | ".join(row) + " |")
            lines.extend(
                [
                    "",
                    "## Preferred Path",
                    "",
                ]
            )
            lines.extend(
                [
                    f"**Recommended path:** {preferred_playbook['path']}",
                    "",
                    "### Why Today",
                    "",
                ]
            )
            lines.extend(_bullet_list(list(preferred_playbook["why_today"]), "No preferred-path rationale generated."))
            lines.extend(["", "### Assumptions That Make This Preferable", ""])
            lines.extend(_bullet_list(list(preferred_playbook["assumptions"]), "No preferred-path assumptions generated."))
            lines.extend(["", "### Immediate Execution Steps", ""])
            lines.extend(_bullet_list(list(preferred_playbook["immediate"]), "No immediate execution steps generated."))
            lines.extend(["", "### Required Stakeholders", ""])
            lines.extend(_bullet_list(list(preferred_playbook["stakeholders"]), "No stakeholder list generated."))
            lines.extend(["", "### Decision Checkpoints", ""])
            lines.extend(_bullet_list(list(preferred_playbook["checkpoints"]), "No decision checkpoints generated."))
            lines.extend(["", "### Escalation Conditions", ""])
            lines.extend(_bullet_list(list(preferred_playbook["escalation"]), "No escalation conditions generated."))
            lines.extend(["", "### Exit Criteria", ""])
            lines.extend(_bullet_list(list(preferred_playbook["exit"]), "No exit criteria generated."))

            lines.extend(["", "## Role-Based Implications", ""])
            lines.extend(_bullet_list(_role_implications(profile, criteria), "No role-based implications generated."))

            lines.extend(["", "## Why This Reasoning Holds", ""])
            lines.extend(_bullet_list(list(profile["why_holds"]), "No decision assumptions generated."))

            lines.extend(["", "## Assumptions", ""])
            lines.extend(_bullet_list(_profile_assumptions(profile, event_family), "No assumptions generated."))

            lines.extend(["", "## Trade-offs", ""])
            lines.extend(_bullet_list(_profile_tradeoffs(profile, criteria), "No trade-offs generated."))

            lines.extend(["", "## Risk Analysis", ""])
            for item in risk_analysis:
                lines.extend(
                    [
                        f"### {item['risk']}",
                        "",
                        f"- **Why it matters:** {item['why']}",
                        f"- **Potential impact:** {item['impact']}",
                        f"- **Early warning indicator:** {item['warning']}",
                        f"- **Suggested mitigation:** {item['mitigation']}",
                        "",
                    ]
                )

            lines.extend(["", "## Decision Blind Spots", ""])
            lines.extend(_bullet_list(_decision_blind_spots(criteria, monitor_signals), "No decision blind spots generated."))

            lines.extend(["", "## What Could Change This Recommendation", ""])
            lines.extend(_bullet_list(_change_triggers(profile, criteria), "No change triggers generated."))

            if regulatory_considerations:
                lines.extend(["", "## Regulatory Considerations", ""])
                lines.append("Decision-support reminder only; this is not legal advice.")
                for item in regulatory_considerations:
                    lines.extend(
                        [
                            "",
                            f"### {item['area']}",
                            "",
                            f"- **Why it may matter:** {item['why']}",
                            f"- **Possible decision impact:** {item['impact']}",
                            f"- **Suggested internal review:** {item['review']}",
                        ]
                    )

            lines.extend(["", "## Recommendation Action Plan", ""])
            for window, items in action_timeline.items():
                lines.extend([f"### {window}", ""])
                lines.extend(str(item) for item in items)
                lines.append("")

            lines.extend(["## What to Monitor", ""])
            lines.append("These signals answer: what could change today's recommendation?")
            for signal, reason in monitor_signals:
                lines.append(f"- **{signal}:** {reason}")
            monitoring = issue_strategic_assessment.role_based_monitoring
            for role, items in [
                ("Investor", monitoring.investor_view),
                ("Corporate Strategy", monitoring.corporate_strategy_view),
                ("Supply Chain", monitoring.supply_chain_view),
                ("Policy", monitoring.policy_view),
            ]:
                lines.extend(["", f"### {role}", ""])
                lines.extend(_bullet_list(items, f"No {role.lower()} monitoring notes generated."))

            lines.extend(["", "## Historical Evidence", ""])
            if similar_cases:
                for outcome in similar_cases[:3]:
                    analogue = _matching_analogue(outcome, issue_analogues)
                    lines.extend(
                        [
                            f"### {outcome.case_name} ({outcome.year})",
                            "",
                            f"- **Case and time period:** {outcome.case_name}, {outcome.year}; {outcome.event_family}; {outcome.sector}.",
                            f"- **Why it is comparable:** {_analogue_comparison(outcome, analogue)}",
                            f"- **What happened:** {outcome.observed_outcome}",
                            f"- **Why it matters today:** {outcome.strategic_response}",
                            "- **Relationship to recommendation:** Supports a staged decision path by showing what organizations had to map, review, or adjust before acting.",
                            f"- **Reference:** {_historical_reference(outcome, analogue)}",
                            f"- **Source note:** {_historical_reference_status(outcome, analogue)}",
                            "",
                        ]
                    )
            else:
                lines.append("- No close historical cases were retrieved from the local dataset.")

            lines.extend(["## Market Expectations vs Actual Outcomes", ""])
            if issue_strategic_assessment.expectation_vs_reality:
                for gap in issue_strategic_assessment.expectation_vs_reality:
                    lines.extend(
                        [
                            f"### {gap.event}",
                            "",
                            f"- **Initial / mainstream expectation:** {gap.consensus_expectation}",
                            f"- **Market or user behavior:** {gap.market_user_behavior}",
                            f"- **Actual observed outcome:** {gap.observed_outcome}",
                            f"- **Expectation gap:** {gap.expectation_gap}",
                            f"- **Lesson:** {gap.strategic_lesson}",
                            "",
                        ]
                    )
            else:
                lines.append("- Local dataset does not contain enough market-outcome evidence for this claim.")

            lines.extend(["", "## Evidence Used", ""])
            lines.append("- Input document or question text.")
            lines.append("- Local historical analogue records.")
            lines.append("- Local historical outcome records.")
            if event_understanding:
                lines.append("- Deterministic event-family understanding rules.")
            if source_url:
                lines.append(f"- Source URL: {_source_reference(source_url)}")
            lines.append("")
            lines.extend(["## Limitations", ""])
            lines.extend(_bullet_list(issue_strategic_assessment.important_limitations, "No limitations generated."))
            lines.extend(_bullet_list(_source_evidence_limitations(source_url, bool(similar_cases)), "No source limitations generated."))
            lines.append("")
            continue

        lines.extend(
            [
                "## Executive Summary",
                "",
                f"- The document describes {_article_for(scenario)} {scenario} issue involving {', '.join(issue.industries[:3]) or 'strategic operations'}.",
                "- Evidence traces identify whether each finding comes from the source document, the historical database, or the current context knowledge base.",
                "",
            ]
        )

        if agent_route:
            lines.extend(
                [
                    "## Agent Execution Trace",
                    "",
                    f"- **Document type detected:** {agent_route.document_type}",
                    f"- **Scenario detected:** {agent_route.scenario_type}",
                    f"- **Selected tools:** {', '.join(agent_route.selected_tools) or 'None'}",
                    f"- **Skipped tools:** {', '.join(agent_route.skipped_tools) or 'None'}",
                    "",
                ]
            )
            for step in agent_route.trace:
                lines.append(f"{step.step}. **{step.event}:** {step.detail}")
            lines.extend(["", "## Tool Decisions", ""])
            for decision in agent_route.reasoning_record:
                lines.extend(
                    [
                        f"### {decision.tool}",
                        "",
                        f"- **Decision:** {decision.decision}",
                        f"- **Why:** {decision.why}",
                        f"- **Expected contribution:** {decision.expected_contribution}",
                        "",
                    ]
                )
            lines.extend(
                [
                    "## Analysis Path",
                    "",
                    "- Agent Router reviewed document type, scenario, industries, actors, and keywords.",
                    "- Tool Registry provided available deterministic tools.",
                    "- Selected tools executed in route order.",
                    "- Result synthesis generated the executive brief with evidence sources.",
                    "",
                ]
            )

        lines.extend(
            [
                "## Key Issue",
                "",
                f"**Title:** {issue.title}",
                "",
                f"**Core issue:** {issue.core_issue}",
                "",
                f"**Summary:** {issue.summary}",
                "",
                "**Evidence trace:** Source Document",
                "",
                "## Current Event Context",
                "",
            ]
        )
        lines.extend(_format_event_context(event_context))
        if source_url:
            lines.extend(
                [
                    "",
                    f"- **Source Link:** {_source_reference(source_url)}",
                    "- **Source Link note:** Webpage text was fetched when readable content was available.",
                ]
            )
        lines.extend(
            [
                "",
                "## Scenario Classification",
                "",
            ]
        )
        if classification:
            lines.extend(
                [
                    f"- **Primary scenario:** {classification.primary_scenario}",
                    f"- **Matched keywords:** {', '.join(classification.matched_keywords) or 'None'}",
                    f"- **Classification confidence:** {classification.confidence_label}",
                    "- **Evidence trace:** Source Document + deterministic keyword classifier",
                    "- **Note:** Confidence describes classification quality only; it is not a forecast.",
                ]
            )
        else:
            lines.append("- **Primary scenario:** Unclassified")

        lines.extend(
            [
                "",
                "## Extracted Entities",
                "",
                f"- **Document type guess:** {issue.document_type_guess} (Evidence trace: Source Document)",
                f"- **Actors:** {', '.join(issue.actors) or 'None detected'} (Evidence trace: Source Document)",
                f"- **Countries / regions:** {', '.join(issue.countries_or_regions) or 'None detected'} (Evidence trace: Source Document)",
                f"- **Industries:** {', '.join(issue.industries) or 'None detected'} (Evidence trace: Source Document)",
                f"- **Policy terms:** {', '.join(issue.policy_terms) or 'None detected'} (Evidence trace: Source Document)",
                f"- **Companies:** {', '.join(issue.companies) or 'None detected'} (Evidence trace: Source Document)",
                "",
                "## Historical Analogues",
                "",
            ]
        )
        for analogue in issue_analogues:
            lines.extend(
                [
                    f"### {analogue.case_title} ({analogue.year})",
                    "",
                    f"- **Scenario type:** {analogue.scenario_type}",
                    f"- **Similarity reason:** {analogue.similarity_reason}",
                    f"- **Business relevance:** {analogue.business_relevance}",
                    f"- **Geopolitical relevance:** {analogue.geopolitical_relevance}",
                    f"- **Caution note:** {analogue.caution_note}",
                    f"- **Source origin:** {analogue.evidence_trace}",
                    "",
                ]
            )

        lines.extend(["## Historical Outcomes", ""])
        if issue_historical_outcomes:
            for outcome in issue_historical_outcomes:
                lines.extend(
                    [
                        f"### {outcome.case_name} ({outcome.year})",
                        "",
                        f"- **Event family:** {outcome.event_family}",
                        f"- **Observed outcome:** {outcome.observed_outcome}",
                        f"- **Strategic response:** {outcome.strategic_response}",
                        f"- **Time horizon:** {outcome.time_horizon}",
                        f"- **Confidence:** {outcome.confidence}",
                        f"- **Source status:** {outcome.source_status}",
                        f"- **Retrieval reason:** {outcome.retrieval_reason}",
                        "",
                    ]
                )
        else:
            lines.append("- No historical outcomes retrieved.")

        lines.extend(["## Strategic Lessons", ""])
        if issue_strategic_lessons:
            for lesson in issue_strategic_lessons:
                lines.extend(
                    [
                        f"### {lesson.lesson}",
                        "",
                        f"- **Supporting cases:** {', '.join(lesson.supporting_cases)}",
                        f"- **Confidence:** {lesson.confidence}",
                        f"- **Rationale:** {lesson.rationale}",
                        "",
                    ]
                )
        else:
            lines.append("- No recurring strategic lessons generated.")

        lines.extend(["## Evidence Credibility Note", ""])
        if issue_evidence_credibility:
            lines.extend(
                [
                    f"- **Evidence summary:** {issue_evidence_credibility.evidence_summary}",
                    f"- **Confidence distribution:** {_format_distribution(issue_evidence_credibility.confidence_distribution)}",
                    f"- **Source status distribution:** {_format_distribution(issue_evidence_credibility.source_status_distribution)}",
                    f"- **Reviewer note:** {issue_evidence_credibility.reviewer_note}",
                    "",
                    "**Key limitations:**",
                ]
            )
            lines.extend(_bullet_list(issue_evidence_credibility.key_limitations, "No credibility limitations listed."))
            lines.append("")
        else:
            lines.extend(["- No evidence credibility assessment generated.", ""])

        lines.extend(
            [
                "## Decision Considerations",
                "",
                "- Decision-makers may wish to compare current issue details against the retrieved outcomes before acting.",
                "- Decision-makers may wish to separate recurring historical lessons from case-specific facts.",
                "",
            ]
        )

        lines.extend(["## Current Context", ""])
        if not issue_contexts:
            lines.extend(
                [
                    "- ContextRetriever was skipped or no current-context findings were returned for this route.",
                    "- **Source origin:** Agent Router",
                    "",
                ]
            )
        for context in issue_contexts:
            lines.extend(
                [
                    f"### {context.industry} - {context.scenario_type}",
                    "",
                    f"- **Context summary:** {context.context_summary}",
                    f"- **Why it matters:** {context.why_it_matters}",
                    f"- **Stakeholders:** {context.stakeholders}",
                    f"- **Monitoring considerations:** {context.monitoring_considerations}",
                    f"- **Retrieval reason:** {context.similarity_reason}",
                    f"- **Source origin:** {context.evidence_trace}",
                    "",
                ]
            )

        lines.extend(["## Similarities and Differences", ""])
        if analysis:
            lines.append("### Observed Similarities")
            lines.extend(_bullet_list(analysis.observed_similarities, "No observed similarities generated."))
            lines.append("")
            lines.append("### Observed Differences")
            lines.extend(_bullet_list(analysis.observed_differences, "No observed differences generated."))
        else:
            lines.append("- No synthesis available.")

        lines.extend(["", "## Business Considerations", ""])
        if analysis:
            lines.extend(_bullet_list(analysis.business_considerations, "No business considerations generated."))
        else:
            lines.append("- No business considerations generated.")

        lines.extend(["", "## Operational Considerations", ""])
        if analysis:
            lines.extend(_bullet_list(analysis.operational_considerations, "No operational considerations generated."))
        else:
            lines.append("- No operational considerations generated.")

        lines.extend(["", "## Geopolitical Considerations", ""])
        if analysis:
            lines.extend(_bullet_list(analysis.geopolitical_considerations, "No geopolitical considerations generated."))
        else:
            lines.append("- No geopolitical considerations generated.")

        lines.extend(["", "## Mechanisms Detected", ""])
        if issue_mechanisms:
            for mechanism in issue_mechanisms:
                lines.extend(
                    [
                        f"### {mechanism.mechanism_name}",
                        "",
                        f"- **Description:** {mechanism.description}",
                        f"- **Detection reason:** {mechanism.detection_reason}",
                        f"- **Possible observations:** {mechanism.possible_observations}",
                        f"- **Evidence references:** {', '.join(mechanism.evidence_references)}",
                        "",
                    ]
                )
        else:
            lines.append("- No mechanisms detected.")

        lines.extend(["## Competing Interpretations", ""])
        if issue_interpretations:
            for interpretation in issue_interpretations:
                lines.extend(
                    [
                        f"### {interpretation.lens}",
                        "",
                        f"- **Hypothesis:** {interpretation.hypothesis}",
                        f"- **Evidence references:** {', '.join(sorted(set(interpretation.evidence_references)))}",
                        "",
                    ]
                )
        else:
            lines.append("- No competing interpretations generated.")

        lines.extend(["## Multi-Lens Analysis", ""])
        if issue_interpretations:
            for interpretation in issue_interpretations:
                lines.extend([f"### {interpretation.lens}", "", "**Supporting observations:**"])
                lines.extend(_bullet_list(interpretation.supporting_observations, "No supporting observations generated."))
                lines.append("")
                lines.append("**Limitations:**")
                lines.extend(_bullet_list(interpretation.limitations, "No limitations generated."))
                lines.append("")
        else:
            lines.append("- No lens analysis generated.")

        lines.extend(["## Supporting Evidence", ""])
        if issue_assessments:
            for assessment in issue_assessments:
                lines.append(f"### {assessment.lens} ({assessment.confidence_language})")
                lines.extend(_bullet_list(assessment.supporting_evidence, "No supporting evidence listed."))
                lines.append("")
        else:
            lines.append("- No evidence assessment generated.")

        lines.extend(["## Weakening Evidence", ""])
        if issue_assessments:
            for assessment in issue_assessments:
                lines.append(f"### {assessment.lens}")
                lines.extend(_bullet_list(assessment.weakening_evidence, "No weakening evidence listed."))
                lines.append("")
        else:
            lines.append("- No weakening evidence generated.")

        lines.extend(["## Missing Evidence", ""])
        if issue_assessments:
            for assessment in issue_assessments:
                lines.append(f"### {assessment.lens}")
                lines.extend(_bullet_list(assessment.missing_evidence, "No missing evidence listed."))
                lines.append("")
        else:
            lines.append("- No missing evidence generated.")

        lines.extend(["## Historical Response Patterns", ""])
        if issue_response_patterns:
            for pattern in issue_response_patterns:
                lines.extend([f"### {pattern.pattern_name}", "", "**Observed Historical Choices:**"])
                lines.extend(_bullet_list(pattern.observed_historical_choices, "No historical choices listed."))
                lines.append("")
                lines.append("**Observed Outcomes:**")
                lines.extend(_bullet_list(pattern.observed_outcomes, "No observed outcomes listed."))
                lines.append("")
                lines.append("**Business Lessons:**")
                lines.extend(_bullet_list(pattern.business_lessons, "No business lessons listed."))
                lines.append("")
            lines.extend(["## Cross-Domain Lessons", ""])
            for pattern in issue_response_patterns:
                lines.extend(_bullet_list(pattern.cross_domain_lessons, "No cross-domain lessons listed."))
        else:
            lines.append("- No response patterns generated.")

        lines.extend(["", "## Monitoring Considerations", ""])
        lines.append("- Decision-makers may wish to monitor source updates, implementation details, stakeholder responses, and evidence gaps.")
        lines.append("- Decision-makers may wish to monitor whether new evidence strengthens or weakens each interpretation.")

        lines.extend(["", "## Strategic Questions", ""])
        if analysis:
            lines.extend(_bullet_list(analysis.strategic_questions, "No strategic questions generated."))
        else:
            lines.append("- What additional source material is needed?")

        lines.extend(
            [
                "",
                "## Analyst Notes",
                "",
                "- V3 uses an Agent Router to select tools before execution.",
                "- Current context retrieval uses local Markdown knowledge-base entries.",
                "- The synthesis uses phrases such as may resemble, shares characteristics with, differs from, and requires monitoring by design.",
                "",
                "### Evidence Trace",
                "",
            ]
        )
        evidence_items = ["Source Document"] + [item.evidence_trace for item in issue_analogues]
        evidence_items += [item.evidence_trace for item in issue_contexts]
        for mechanism in issue_mechanisms:
            evidence_items += mechanism.evidence_references
        for interpretation in issue_interpretations:
            evidence_items += interpretation.evidence_references
        for pattern in issue_response_patterns:
            evidence_items += pattern.evidence_references
        for outcome in issue_historical_outcomes:
            evidence_items += outcome.evidence_references
        for lesson in issue_strategic_lessons:
            evidence_items += lesson.evidence_references
        if agent_route:
            evidence_items.append("Agent Router: deterministic tool selection trace")
            evidence_items.append("Tool Registry: registered deterministic analysis tools")
        if analysis:
            evidence_items += analysis.evidence_trace
        for evidence in sorted(set(evidence_items)):
            lines.append(f"- {evidence}")
        lines.append("")

        if agent_route:
            context_source_line = (
                "- **Context Knowledge Base:** selected current-context findings when the router selected ContextRetriever."
                if issue_contexts
                else "- **Context Knowledge Base:** not used for this route because ContextRetriever was skipped or returned no findings."
            )
            lines.extend(
                [
                    "## Evidence Sources",
                    "",
                    "- **Input Document:** issue fields, scenario keywords, and extracted entities.",
                    "- **Historical Database:** retrieved analogue cases and similarity reasons.",
                    context_source_line,
                    "- **Agent Router:** selected and skipped tool decisions.",
                    "",
                ]
            )
        if issue_strategic_assessment:
            lines.extend(["## Important Limitations", ""])
            lines.extend(_bullet_list(issue_strategic_assessment.important_limitations, "No limitations generated."))
            lines.append("")

    return "\n".join(lines).strip() + "\n"
