"""
Financial Rubric Agent V2.0

A beginner-friendly terminal application that:
1. asks the user for one or more public company tickers,
2. pulls basic financial data from yfinance,
3. prints key financial metrics,
4. creates simple rule-based rubric scores,
5. prints structured investment reports,
6. compares multiple companies when multiple tickers are provided.
7. exports batch comparison results to CSV.
8. optionally adds an AI-generated narrative to individual company reports.

Rule-based logic calculates scores. AI explains the results.
"""

import csv
from datetime import datetime
from pathlib import Path
import sys

import yfinance as yf

from ai_writer import generate_ai_narrative
from rubric import (
    calculate_total_score,
    score_competitive_moat,
    score_profitability,
    score_revenue_growth,
    score_risk,
    score_valuation,
)


def format_percentage(value):
    """Convert decimal values like 0.1234 into '12.34%'."""
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def format_large_number(value):
    """Format large dollar values for easier reading."""
    if value is None:
        return "N/A"
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    return f"${value:,.0f}"


def format_number(value):
    """Format regular numbers and handle missing values."""
    if value is None:
        return "N/A"
    return f"{value:,.2f}"


def get_info_value(info, key):
    """
    Safely read a field from yfinance's info dictionary.

    yfinance data availability varies by ticker, so missing values are normal.
    """
    value = info.get(key)
    if value in ("", "None", "N/A"):
        return None
    return value


def fetch_company_data(ticker_symbol):
    """Fetch basic company and financial data from yfinance."""
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    if not info or info.get("quoteType") is None:
        raise ValueError("No company data found. Please check the ticker symbol.")

    return {
        "company_name": get_info_value(info, "longName") or get_info_value(info, "shortName") or "N/A",
        "ticker": ticker_symbol.upper(),
        "sector": get_info_value(info, "sector"),
        "industry": get_info_value(info, "industry"),
        "market_cap": get_info_value(info, "marketCap"),
        "revenue_growth": get_info_value(info, "revenueGrowth"),
        "profit_margin": get_info_value(info, "profitMargins"),
        "operating_margin": get_info_value(info, "operatingMargins"),
        "return_on_equity": get_info_value(info, "returnOnEquity"),
        "trailing_pe": get_info_value(info, "trailingPE"),
        "forward_pe": get_info_value(info, "forwardPE"),
        "price_to_sales": get_info_value(info, "priceToSalesTrailing12Months"),
        "beta": get_info_value(info, "beta"),
        "debt_to_equity": get_info_value(info, "debtToEquity"),
        "current_ratio": get_info_value(info, "currentRatio"),
    }


def build_scores(data):
    """Create the five investment category scores."""
    scores = {
        "Revenue Growth": score_revenue_growth(data["revenue_growth"]),
        "Profitability": score_profitability(
            data["profit_margin"],
            data["operating_margin"],
        ),
        "Valuation": score_valuation(
            data["trailing_pe"],
            data["forward_pe"],
        ),
        "Competitive Moat": score_competitive_moat(
            data["market_cap"],
            data["profit_margin"],
            data["operating_margin"],
        ),
        "Risk Assessment": score_risk(
            data["beta"],
            data["debt_to_equity"],
        ),
    }
    return scores


def get_total_score_label(total_score):
    """Convert the total score into a simple investment interpretation."""
    if total_score >= 80:
        return "Strong overall investment profile"
    if total_score >= 65:
        return "Good company, but with some concerns"
    if total_score >= 50:
        return "Mixed investment profile"
    if total_score >= 35:
        return "Weak or high-risk profile"
    return "Very weak profile"


def build_report(data, scores, ai_narrative=None):
    """Create a structured text report for the terminal and output file."""
    total_score = calculate_total_score(scores)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ai_section = ""

    if ai_narrative:
        ai_section = f"""

AI Investment Narrative
-----------------------
{ai_narrative}
"""

    report = f"""
Financial Rubric Agent V2.0
Generated At: {generated_at}

Company: {data["company_name"]}
Ticker: {data["ticker"]}
Sector: {data["sector"] or "N/A"}
Industry: {data["industry"] or "N/A"}

Raw Financial Metrics Used
--------------------------
Market Cap: {format_large_number(data["market_cap"])}
Revenue Growth: {format_percentage(data["revenue_growth"])}
Net Profit Margin: {format_percentage(data["profit_margin"])}
Operating Margin: {format_percentage(data["operating_margin"])}
Return on Equity: {format_percentage(data["return_on_equity"])}
Trailing P/E: {format_number(data["trailing_pe"])}
Forward P/E: {format_number(data["forward_pe"])}
Price to Sales: {format_number(data["price_to_sales"])}
Beta: {format_number(data["beta"])}
Debt to Equity: {format_number(data["debt_to_equity"])}
Current Ratio: {format_number(data["current_ratio"])}

Investment Scores and Explanations
----------------------------------
Revenue Growth Score: {scores["Revenue Growth"]["score"]}/20
Metrics Used: Revenue Growth = {format_percentage(data["revenue_growth"])}
Explanation: {scores["Revenue Growth"]["explanation"]}

Profitability Score: {scores["Profitability"]["score"]}/20
Metrics Used: Net Profit Margin = {format_percentage(data["profit_margin"])}, Operating Margin = {format_percentage(data["operating_margin"])}
Explanation: {scores["Profitability"]["explanation"]}

Valuation Score: {scores["Valuation"]["score"]}/20
Metrics Used: Trailing P/E = {format_number(data["trailing_pe"])}, Forward P/E = {format_number(data["forward_pe"])}
Explanation: {scores["Valuation"]["explanation"]}

Competitive Moat Score: {scores["Competitive Moat"]["score"]}/20
Metrics Used: Market Cap = {format_large_number(data["market_cap"])}, Net Profit Margin = {format_percentage(data["profit_margin"])}, Operating Margin = {format_percentage(data["operating_margin"])}
Explanation: {scores["Competitive Moat"]["explanation"]}

Risk Score: {scores["Risk Assessment"]["score"]}/20
Metrics Used: Debt to Equity = {format_number(data["debt_to_equity"])}, Beta = {format_number(data["beta"])}
Explanation: {scores["Risk Assessment"]["explanation"]}

Total Score: {total_score}/100
Interpretation: {get_total_score_label(total_score)}
{ai_section}
Note: Rule-based logic calculates the scores. AI explains the results when enabled.
This report is educational analysis, not investment advice.
"""
    return report.strip()


def save_report(ticker_symbol, report):
    """Save the report to the outputs folder."""
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = outputs_dir / f"{ticker_symbol.upper()}_report_{timestamp}.txt"
    file_path.write_text(report, encoding="utf-8")
    return file_path


def analyze_ticker(ticker_symbol):
    """
    Fetch data, score the company, build the report, and save the report.

    This helper is used by both single-ticker mode and batch comparison mode.
    """
    data = fetch_company_data(ticker_symbol)
    scores = build_scores(data)
    total_score = calculate_total_score(scores)
    interpretation = get_total_score_label(total_score)
    ai_narrative = generate_ai_narrative(data, scores, total_score, interpretation)
    report = build_report(data, scores, ai_narrative)
    output_file = save_report(ticker_symbol, report)

    return {
        "data": data,
        "scores": scores,
        "report": report,
        "output_file": output_file,
        "total_score": total_score,
        "interpretation": interpretation,
    }


def build_comparison_rows(results):
    """Create sorted comparison rows from successful ticker analyses."""
    rows = []

    for result in results:
        data = result["data"]
        scores = result["scores"]
        total_score = result["total_score"]

        rows.append({
            "Ticker": data["ticker"],
            "Company": data["company_name"],
            "Revenue Growth Score": f'{scores["Revenue Growth"]["score"]}/20',
            "Profitability Score": f'{scores["Profitability"]["score"]}/20',
            "Valuation Score": f'{scores["Valuation"]["score"]}/20',
            "Competitive Moat Score": f'{scores["Competitive Moat"]["score"]}/20',
            "Risk Assessment Score": f'{scores["Risk Assessment"]["score"]}/20',
            "Total Score": f"{total_score}/100",
            "Interpretation": result["interpretation"],
            "sort_score": total_score,
        })

    return sorted(rows, key=lambda row: row["sort_score"], reverse=True)


def format_comparison_table(rows):
    """
    Format comparison rows as a simple terminal table.

    The table uses only standard Python string formatting, so no extra package
    is needed. Long company names and interpretations are shortened to keep the
    terminal output readable.
    """
    if not rows:
        return "No successful ticker results to compare."

    columns = [
        ("Ticker", 8),
        ("Company", 28),
        ("Revenue Growth Score", 22),
        ("Profitability Score", 21),
        ("Valuation Score", 17),
        ("Competitive Moat Score", 24),
        ("Risk Assessment Score", 22),
        ("Total Score", 12),
        ("Interpretation", 38),
    ]

    def shorten(value, width):
        text = str(value)
        if len(text) <= width:
            return text
        return text[: width - 3] + "..."

    header = " | ".join(column_name.ljust(width) for column_name, width in columns)
    divider = "-+-".join("-" * width for _, width in columns)
    lines = [header, divider]

    for row in rows:
        line = " | ".join(
            shorten(row[column_name], width).ljust(width)
            for column_name, width in columns
        )
        lines.append(line)

    return "\n".join(lines)


def build_comparison_report(rows, failed_tickers):
    """Create the text report for batch comparison mode."""
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comparison_table = format_comparison_table(rows)

    if failed_tickers:
        failed_section = "\n\nFailed Tickers\n--------------\n"
        failed_section += "\n".join(f"{ticker}: {error}" for ticker, error in failed_tickers)
    else:
        failed_section = ""

    report = f"""
Financial Rubric Agent V2.0 - Batch Comparison Report
Generated At: {generated_at}

Companies are sorted by Total Score from highest to lowest.

{comparison_table}{failed_section}

Note: These are simple rule-based scores, not investment advice.
"""
    return report.strip()


def save_comparison_report(report):
    """Save the batch comparison report to the outputs folder."""
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = outputs_dir / f"comparison_report_{timestamp}.txt"
    file_path.write_text(report, encoding="utf-8")
    return file_path


def csv_value(value):
    """
    Prepare one value for CSV export.

    Missing financial metrics become blank CSV cells. Keeping them blank makes
    the file easier to filter later in Excel, Google Sheets, or pandas.
    """
    if value is None:
        return ""
    return value


def build_csv_rows(results, timestamp):
    """Create CSV-ready rows from successful ticker analyses."""
    rows = []

    for result in results:
        data = result["data"]
        scores = result["scores"]

        rows.append({
            "timestamp": timestamp,
            "ticker": data["ticker"],
            "company": data["company_name"],
            "revenue_growth_score": scores["Revenue Growth"]["score"],
            "profitability_score": scores["Profitability"]["score"],
            "valuation_score": scores["Valuation"]["score"],
            "competitive_moat_score": scores["Competitive Moat"]["score"],
            "risk_assessment_score": scores["Risk Assessment"]["score"],
            "total_score": result["total_score"],
            "interpretation": result["interpretation"],
            "revenue_growth": csv_value(data["revenue_growth"]),
            "profit_margin": csv_value(data["profit_margin"]),
            "operating_margin": csv_value(data["operating_margin"]),
            "trailing_pe": csv_value(data["trailing_pe"]),
            "forward_pe": csv_value(data["forward_pe"]),
            "debt_to_equity": csv_value(data["debt_to_equity"]),
            "beta": csv_value(data["beta"]),
        })

    return rows


def save_comparison_csv(results):
    """Save batch comparison results as a CSV file in the outputs folder."""
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = outputs_dir / f"comparison_results_{timestamp}.csv"

    fieldnames = [
        "timestamp",
        "ticker",
        "company",
        "revenue_growth_score",
        "profitability_score",
        "valuation_score",
        "competitive_moat_score",
        "risk_assessment_score",
        "total_score",
        "interpretation",
        "revenue_growth",
        "profit_margin",
        "operating_margin",
        "trailing_pe",
        "forward_pe",
        "debt_to_equity",
        "beta",
    ]

    rows = build_csv_rows(results, timestamp)

    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return file_path


def run_single_ticker_mode(ticker_symbol):
    """Analyze one ticker and print the individual report."""
    result = analyze_ticker(ticker_symbol)

    print()
    print(result["report"])
    print()
    print(f"Report saved to: {result['output_file']}")


def run_batch_mode(ticker_symbols):
    """
    Analyze several tickers and print a sorted comparison table.

    If one ticker fails, the program records the error and continues with the
    remaining tickers.
    """
    successful_results = []
    failed_tickers = []

    for ticker_symbol in ticker_symbols:
        print(f"Analyzing {ticker_symbol}...")
        try:
            result = analyze_ticker(ticker_symbol)
            successful_results.append(result)
            print(f"Saved individual report to: {result['output_file']}")
        except Exception as error:
            failed_tickers.append((ticker_symbol, str(error)))
            print(f"Could not analyze {ticker_symbol}: {error}")

    comparison_rows = build_comparison_rows(successful_results)
    comparison_report = build_comparison_report(comparison_rows, failed_tickers)
    comparison_file = save_comparison_report(comparison_report)
    csv_file = save_comparison_csv(successful_results)

    print()
    print(comparison_report)
    print()
    print(f"Comparison report saved to: {comparison_file}")
    print(f"CSV results saved to: {csv_file}")


def main():
    """Run the terminal application."""
    print("Financial Rubric Agent V2.0")
    print("-------------------------")

    if len(sys.argv) > 1:
        ticker_symbols = [ticker.strip().upper() for ticker in sys.argv[1:] if ticker.strip()]
        print(f"Ticker symbols: {', '.join(ticker_symbols)}")
    else:
        ticker_symbol = input("Enter a ticker symbol, for example AAPL: ").strip().upper()
        ticker_symbols = [ticker_symbol] if ticker_symbol else []

    if not ticker_symbols:
        print("No ticker entered. Please run the program again.")
        return

    if len(ticker_symbols) == 1:
        try:
            run_single_ticker_mode(ticker_symbols[0])
        except Exception as error:
            print()
            print("Something went wrong while creating the report.")
            print(f"Error: {error}")
    else:
        run_batch_mode(ticker_symbols)


if __name__ == "__main__":
    main()
