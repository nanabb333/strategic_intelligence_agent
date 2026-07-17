# Local App Setup

Strategic Intelligence Decision Companion runs as a local product. You do not need to understand FastAPI, uvicorn, or local server ports to start using it.

## Quick Start

For macOS, double-click:

```text
launch/Launch Strategic Intelligence Decision Companion.command
```

For Windows, double-click:

```text
launch/Launch Strategic Intelligence Decision Companion.bat
```

The launcher starts the local app and opens the Decision Workspace. If the browser does not open automatically, open:

```text
http://localhost:8000
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

Technical users can still launch from a terminal:

```bash
./run_app.sh
python3 launch.py
```

Developers can also run the FastAPI app directly:

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

The launcher binds to `127.0.0.1` by default. `SIDC_HOST` can explicitly override the bind address, but non-loopback use requires a separate security review. CORS defaults to the local `localhost:8000` and `127.0.0.1:8000` origins and can be explicitly configured with `SIDC_ALLOWED_ORIGINS`.
