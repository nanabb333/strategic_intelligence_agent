# Local App Setup

Strategic Intelligence Decision Companion runs as a local usable application. The browser dashboard calls a FastAPI backend, and the backend runs the existing Python pipeline.

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Start The Local Server

From the repository root:

```bash
python3 -m uvicorn app:app --reload
```

The local API runs at:

```text
http://127.0.0.1:8000
```

## Open The Dashboard

Open:

```text
http://127.0.0.1:8000/dashboard/
```

## Basic User Workflow

1. Create or open a project.
2. Add a decision question.
3. Paste text, upload a supported file, or provide a readable URL.
4. Choose beginner, analyst, or executive output mode.
5. Click Analyze.
6. Review the workspace panels and download Markdown, TXT, or JSON results.

## Local-Only Scope

The server is intended for local execution. It can attempt to fetch readable text from a user-provided URL, but it does not add live web search, external monitoring, LLM APIs, forecasting, investment advice, or trading recommendations.
