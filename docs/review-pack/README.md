# Review Pack

## Project pitch

Lumen is a small local coding agent that runs inside a repository, uses a constrained tool set, and records enough local state to make runs inspectable.

## Architecture map

The core flow connects workspace discovery, prompt construction, tool execution, task state persistence, and run reports.

## Benchmark evidence

The fixed benchmark in `benchmarks/coding_tasks.json` exercises deterministic agent harness behavior, recovery paths, durable memory promotion, and verifier reporting.

## Sample run artifact list

- `.lumen/runs/<run_id>/trace.jsonl`
- `.lumen/runs/<run_id>/task_state.json`
- `.lumen/runs/<run_id>/report.json`
