# Local App Setup

Strategic Intelligence Decision Companion runs as a local product. You do not need to understand FastAPI, uvicorn, or local server ports to start using it.

## Quick Start

From the repository folder, run:

```bash
./run_app.sh
```

Or use the Python launcher:

```bash
python3 launch.py
```

Open:

```text
http://localhost
```

Select **Open Decision Workspace** to begin.

## First Workflow

1. Create a project.
2. Add a decision question.
3. Add evidence manually or accept retrieved evidence into the Evidence Library.
4. Select evidence for analysis.
5. Run the deterministic analysis.
6. Review the Decision Workspace panels.
7. Download Markdown, TXT, or JSON artifacts if needed.

## Developer Startup

Developers can still run the FastAPI app directly:

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn app:app --reload
```

Developer workspace route:

```text
http://127.0.0.1:8000/workspace
```

The backward-compatible route remains available at `/dashboard`.

## Local-Only Scope

The app is intended for local execution. It can retrieve evidence only through explicit user action. It does not add live web search, autonomous browsing, external monitoring, LLM APIs, forecasting, investment advice, legal advice, or trading recommendations.
