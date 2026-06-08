# Financial Rubric Agent

Financial Rubric Agent is a beginner-friendly Python finance analytics tool that pulls public company data from `yfinance`, applies a structured 100-point investment rubric, compares multiple stock tickers, exports CSV results, and optionally generates an AI investment narrative using OpenAI.

The project is designed for Business Analytics students who want to combine finance, data analysis, and practical AI in a portfolio-ready project without using complex software frameworks.

## Why I Built This

I built this project to practice applying business analytics skills to public company analysis. Instead of trying to predict stock prices, the goal is to create a clear, repeatable scoring framework that evaluates companies across growth, profitability, valuation, moat, and risk.

This project also shows how AI can support financial analysis responsibly: the rule-based model calculates the numeric scores, while the optional AI narrative explains the results in plain English. The AI does not overwrite the scores.

## Features

- Single ticker analysis
- Batch ticker comparison
- Public company data fetching with `yfinance`
- Rule-based 100-point investment scoring
- Revenue Growth score
- Profitability score
- Valuation score
- Competitive Moat score
- Risk Assessment score
- Individual text reports
- Batch comparison text reports
- CSV export for batch results
- Optional OpenAI-powered AI investment narrative
- Graceful fallback when `OPENAI_API_KEY` is missing

## Folder Structure

```text
financial-rubric-agent/
│
├── main.py
├── rubric.py
├── ai_writer.py
├── requirements.txt
├── README.md
└── outputs/
    ├── AAPL_report_TIMESTAMP.txt
    ├── comparison_report_TIMESTAMP.txt
    └── comparison_results_TIMESTAMP.csv
```

### File Guide

| File | Purpose |
|---|---|
| `main.py` | Runs the terminal application, fetches data, creates reports, and handles batch mode |
| `rubric.py` | Contains the rule-based scoring logic |
| `ai_writer.py` | Creates the optional OpenAI investment narrative |
| `requirements.txt` | Lists required Python packages |
| `outputs/` | Stores generated text reports and CSV files |

## Installation

### 1. Open the project folder

```bash
cd financial-rubric-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 4. Install packages

```bash
pip install -r requirements.txt
```

## Run Single Ticker Mode

Use this mode when you want a detailed report for one company.

```bash
python3 main.py AAPL
```

Example:

```bash
python3 main.py MSFT
```

The program will:

- fetch financial metrics from `yfinance`
- calculate the five category scores
- calculate the total score out of 100
- optionally add an AI narrative if an OpenAI API key is available
- save an individual text report in `outputs/`

## Run Batch Mode

Use this mode when you want to compare multiple companies.

```bash
python3 main.py AAPL MSFT TSLA KO
```

The program will:

- generate an individual text report for each ticker
- print a comparison table in the terminal
- sort companies by total score from highest to lowest
- save a batch comparison text report
- save a CSV file with the scoring results and raw metrics

## Set Up OpenAI API Key

The OpenAI narrative mode is optional. If no API key is found, the program still works and prints:

```text
AI narrative skipped: OPENAI_API_KEY not found.
```

To enable AI narratives, create a file named `.env` in the project folder:

```text
OPENAI_API_KEY=your_api_key_here
```

You can also choose a model:

```text
OPENAI_MODEL=gpt-5
```

Then run:

```bash
python3 main.py AAPL
```

The individual company report will include an `AI Investment Narrative` section.

## Example Output

```text
Financial Rubric Agent V2.0

Company: Apple Inc.
Ticker: AAPL
Sector: Technology
Industry: Consumer Electronics

Investment Scores and Explanations
----------------------------------
Revenue Growth Score: 19/20
Profitability Score: 19/20
Valuation Score: 10/20
Competitive Moat Score: 19/20
Risk Score: 13/20

Total Score: 80/100
Interpretation: Strong overall investment profile
```

Example batch comparison:

```text
Ticker   | Company                  | Total Score | Interpretation
---------+--------------------------+-------------+--------------------------------
MSFT     | Microsoft Corporation    | 84/100      | Strong overall investment profile
AAPL     | Apple Inc.               | 80/100      | Strong overall investment profile
KO       | The Coca-Cola Company    | 76/100      | Good company, but with some concerns
TSLA     | Tesla, Inc.              | 48/100      | Weak or high-risk profile
```

## Current Limitations

- This is an educational analytics project, not investment advice.
- The scoring rules are simple and not sector-specific.
- `yfinance` data availability may vary by ticker.
- Competitive Moat is still partly a placeholder because moat often requires qualitative research.
- The model does not perform peer benchmarking yet.
- The AI narrative depends on the quality of the provided metrics and should not be treated as a recommendation.
- The project does not include real-time news, analyst estimates, backtesting, or portfolio optimization.

## Future Improvements

- Add sector-specific scoring rules
- Add peer comparison by industry
- Improve Competitive Moat scoring with qualitative research inputs
- Add historical revenue and margin trends
- Add charts for financial metrics
- Add confidence scores for missing or incomplete data
- Export results to Excel
- Add a simple dashboard later, such as Streamlit
- Add source citations for AI narratives
- Add unit tests for the scoring rubric

## Portfolio Description

Financial Rubric Agent is a Python-based business analytics project that evaluates public companies using a structured 100-point investment rubric. The tool collects financial data from `yfinance`, scores companies across revenue growth, profitability, valuation, competitive moat, and risk, supports single-company and multi-company comparison modes, exports CSV results, and optionally uses OpenAI to generate an investment-style narrative. The project demonstrates applied finance analytics, rule-based modeling, data extraction, reporting automation, and responsible use of AI for explanation rather than score generation.

## Resume Bullet Points

- Built a Python-based financial analytics tool that scores public companies using a structured 100-point investment rubric.
- Integrated `yfinance` to collect public company metrics such as revenue growth, profit margin, P/E ratio, debt-to-equity, and beta.
- Designed rule-based scoring logic across revenue growth, profitability, valuation, competitive moat, and risk assessment.
- Developed batch comparison mode to evaluate multiple tickers, rank companies by total score, and export results to CSV.
- Added optional OpenAI narrative generation while preserving rule-based scores as the source of truth.
- Automated individual company reports and batch comparison reports using beginner-friendly Python.
- Demonstrated practical business analytics skills across finance, data processing, scoring models, and AI-assisted reporting.

## Disclaimer

This project is for learning and portfolio purposes only. It does not provide financial advice or investment recommendations.
