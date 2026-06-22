"""
Scoring rubric for Financial Rubric Agent V2.0.

This file keeps the investment scoring rules separate from the terminal app.
Each scoring function returns:
1. a score from 0 to 20
2. a plain-English explanation

The rules are intentionally simple so a beginner can read and improve them.
"""


def make_result(score, explanation):
    """Create one consistent result format for every rubric category."""
    return {
        "score": score,
        "explanation": explanation,
    }


def score_revenue_growth(revenue_growth):
    """
    Score revenue growth from 0 to 20.

    revenue_growth is expected as a decimal:
    0.10 means 10% revenue growth.
    """
    if revenue_growth is None:
        return make_result(10, "Revenue growth was unavailable, so a neutral score was used.")
    if revenue_growth < 0:
        return make_result(4, "Revenue is shrinking, which is a weak growth signal.")
    if revenue_growth < 0.03:
        return make_result(8, "Revenue growth is positive but very low, between 0% and 3%.")
    if revenue_growth < 0.08:
        return make_result(12, "Revenue growth is modest, between 3% and 8%.")
    if revenue_growth < 0.15:
        return make_result(16, "Revenue growth is solid, between 8% and 15%.")
    return make_result(19, "Revenue growth is strong at 15% or higher.")


def score_profitability(profit_margin, operating_margin):
    """
    Score profitability from 0 to 20.

    V2.0 uses net profit margin first. In yfinance, profitMargins is the
    closest simple field for net margin. If it is unavailable, the app falls
    back to operating margin.
    """
    if profit_margin is not None:
        margin = profit_margin
        margin_name = "net profit margin"
    elif operating_margin is not None:
        margin = operating_margin
        margin_name = "operating margin"
    else:
        return make_result(10, "Profitability margin data was unavailable, so a neutral score was used.")

    if margin < 0:
        return make_result(4, f"The company has a negative {margin_name}, which is a weak profitability signal.")
    if margin < 0.05:
        return make_result(8, f"The company's {margin_name} is positive but low, between 0% and 5%.")
    if margin < 0.10:
        return make_result(12, f"The company's {margin_name} is acceptable, between 5% and 10%.")
    if margin < 0.20:
        return make_result(16, f"The company's {margin_name} is solid, between 10% and 20%.")
    return make_result(19, f"The company's {margin_name} is strong at 20% or higher.")


def score_valuation(trailing_pe, forward_pe):
    """
    Score valuation from 0 to 20.

    V2.0 uses trailing P/E first. If trailing P/E is unavailable, it uses
    forward P/E. Lower P/E usually means a better valuation score.
    """
    if trailing_pe is not None and trailing_pe > 0:
        pe_ratio = trailing_pe
        pe_name = "trailing P/E"
    elif forward_pe is not None and forward_pe > 0:
        pe_ratio = forward_pe
        pe_name = "forward P/E"
    else:
        return make_result(2, "P/E data was unavailable or not meaningful, so valuation received a low score.")

    if pe_ratio < 15:
        return make_result(18, f"The {pe_name} is below 15, which suggests a relatively attractive valuation.")
    if pe_ratio <= 25:
        return make_result(14, f"The {pe_name} is between 15 and 25, which looks reasonable.")
    if pe_ratio <= 40:
        return make_result(10, f"The {pe_name} is between 25 and 40, which suggests a more expensive valuation.")
    if pe_ratio <= 60:
        return make_result(6, f"The {pe_name} is between 40 and 60, which is expensive.")
    return make_result(2, f"The {pe_name} is above 60, which is very expensive.")


def score_competitive_moat(market_cap, profit_margin, operating_margin):
    """
    Placeholder moat score from 0 to 20.

    Moat score is placeholder in V2.0.

    A real moat score needs qualitative data like brand strength, switching
    costs, network effects, and market share. For now, this function defaults
    to 12/20 and makes small adjustments for size and strong margins.
    """
    score = 12
    reasons = ["Moat score is placeholder in V2.0."]

    if market_cap is not None:
        if market_cap >= 200_000_000_000:
            score += 3
            reasons.append("Large market cap may suggest scale advantages.")
        elif market_cap >= 50_000_000_000:
            score += 1
            reasons.append("Meaningful market cap may suggest some scale.")
        elif market_cap < 2_000_000_000:
            score -= 2
            reasons.append("Smaller company size may mean a less proven moat.")

    if profit_margin is not None:
        if profit_margin >= 0.20:
            score += 2
            reasons.append("Strong profit margin may suggest pricing power.")
        elif profit_margin < 0:
            score -= 3
            reasons.append("Negative profit margin weakens the moat signal.")

    if operating_margin is not None:
        if operating_margin >= 0.25:
            score += 2
            reasons.append("Strong operating margin may suggest business quality.")
        elif operating_margin < 0:
            score -= 3
            reasons.append("Negative operating margin weakens the moat signal.")

    final_score = max(0, min(20, score))
    return make_result(final_score, " ".join(reasons))


def score_risk(beta, debt_to_equity):
    """
    Score risk from 0 to 20.

    Higher score means lower risk / better risk profile.
    Uses debt-to-equity and beta because they are easy to understand:
    - lower debt is usually safer
    - lower beta usually means less stock price volatility
    """
    if beta is None and debt_to_equity is None:
        return make_result(10, "Debt-to-equity and beta were unavailable, so a neutral risk score was used.")

    very_high_risk = False
    high_risk = False
    moderate_risk = False
    low_risk = False

    if beta is not None:
        if beta > 1.7:
            very_high_risk = True
        elif beta > 1.3:
            high_risk = True
        elif beta >= 1.0:
            moderate_risk = True
        else:
            low_risk = True

    if debt_to_equity is not None:
        if debt_to_equity > 200:
            very_high_risk = True
        elif debt_to_equity > 100:
            high_risk = True
        elif debt_to_equity >= 50:
            moderate_risk = True
        else:
            low_risk = True

    if very_high_risk:
        return make_result(4, "Risk is high because beta is above 1.7 or debt-to-equity is very high.")
    if high_risk:
        return make_result(8, "Risk is elevated because beta is above 1.3 or debt-to-equity is high.")
    if moderate_risk:
        return make_result(13, "Risk is moderate based on debt-to-equity or beta.")
    if low_risk:
        return make_result(18, "Risk appears lower because debt is low and/or beta is below 1.")
    return make_result(10, "Risk data was limited, so a neutral score was used.")


def calculate_total_score(scores):
    """Add the five category scores into a total score from 0 to 100."""
    return sum(category["score"] for category in scores.values())
