# Run Management Design

V6 stores each local analysis as a run folder under `outputs/runs/`.

## Run Folder Structure

Example:

```text
outputs/runs/run_20260623_001/
  input.txt
  analysis.json
  brief.md
  brief.txt
  agent_trace.json
  metadata.json
```

## Run ID Format

Run IDs use:

```text
run_YYYYMMDD_###
```

The numeric suffix increments for each local run on the same day.

## API Access

- `POST /analyze` creates a run.
- `GET /runs` lists saved runs.
- `GET /run/{run_id}` retrieves one run.
- `GET /run/{run_id}/download/markdown` downloads `brief.md`.
- `GET /run/{run_id}/download/txt` downloads `brief.txt`.
- `GET /run/{run_id}/download/json` downloads `analysis.json`.

## Git Policy

Dynamic run folders are ignored by git. The repository keeps `outputs/runs/.gitkeep` so the expected folder exists, but user-generated runs stay local.
