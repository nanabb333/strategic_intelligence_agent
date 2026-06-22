"""
AI narrative writer for Financial Rubric Agent V2.0.

The rule-based scoring system calculates the numeric scores.
This file only asks the AI model to explain those scores in plain English.
The AI should never replace or change the rule-based scores.
"""

import json
import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def clean_value(value):
    """Convert missing values to N/A so the prompt is easy to read."""
    if value is None:
        return "N/A"
    return value


def build_ai_prompt(data, scores, total_score, interpretation):
    """
    Build the prompt sent to OpenAI.

    The prompt includes raw metrics, rule-based scores, and score explanations.
    It clearly tells the AI not to change the numeric scores.
    """
    prompt_data = {
        "ticker": data["ticker"],
        "company_name": data["company_name"],
        "sector": clean_value(data["sector"]),
        "industry": clean_value(data["industry"]),
        "raw_financial_metrics": {
            "market_cap": clean_value(data["market_cap"]),
            "revenue_growth": clean_value(data["revenue_growth"]),
            "profit_margin": clean_value(data["profit_margin"]),
            "operating_margin": clean_value(data["operating_margin"]),
            "return_on_equity": clean_value(data["return_on_equity"]),
            "trailing_pe": clean_value(data["trailing_pe"]),
            "forward_pe": clean_value(data["forward_pe"]),
            "price_to_sales": clean_value(data["price_to_sales"]),
            "beta": clean_value(data["beta"]),
            "debt_to_equity": clean_value(data["debt_to_equity"]),
            "current_ratio": clean_value(data["current_ratio"]),
        },
        "rule_based_scores": scores,
        "total_score": total_score,
        "interpretation": interpretation,
    }

    return f"""
You are a financial analyst writing a beginner-friendly investment narrative.

Important rules:
- Do not change, override, recalculate, or second-guess the numeric scores.
- Treat the rule-based scores as fixed facts.
- Explain what the scores suggest in simple finance language.
- This is educational analysis, not investment advice.
- Do not invent exact financial metrics beyond the data provided.

Use this data:
{json.dumps(prompt_data, indent=2)}

Write the narrative with exactly these sections:

Short Company Overview
Strengths
Weaknesses
Bull Case
Bear Case
Overall Investment-Style Summary
Confidence Level: High / Medium / Low
""".strip()


def generate_ai_narrative(data, scores, total_score, interpretation):
    """
    Generate an optional AI-written investment narrative.

    Returns narrative text when successful.
    Returns None when the API key is missing or the API call fails.
    """
    if load_dotenv is not None:
        load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("AI narrative skipped: OPENAI_API_KEY not found.")
        return None

    if OpenAI is None:
        print("AI narrative skipped: OpenAI package is not installed.")
        return None

    try:
        client = OpenAI(api_key=api_key)
        prompt = build_ai_prompt(data, scores, total_score, interpretation)

        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5"),
            input=prompt,
        )

        return response.output_text.strip()
    except Exception as error:
        print(f"AI narrative skipped: OpenAI API call failed. {error}")
        return None
