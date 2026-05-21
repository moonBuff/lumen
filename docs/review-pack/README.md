# Review Pack

## Project pitch

Lumen is a small local coding agent that runs inside a repository, uses a constrained tool set, and records enough local state to make runs inspectable.

## Architecture map

The core flow connects workspace discovery, structured `ModelContext` construction, prompt rendering, tool execution, task state persistence, and run reports.

Runtime boundaries:

- `Session` stores the recoverable conversation `transcript`.
- `Memory` stores distilled reusable facts and file summaries.
- `ModelContext` keeps prompt sections explicit before rendering.
- `Trace` records the event stream for audit.
- `Report` summarizes the run outcome and key context metadata.

## Benchmark evidence

The fixed benchmark in `benchmarks/coding_tasks.json` exercises deterministic agent harness behavior, context reduction, recovery paths, durable memory promotion, and verifier reporting. Benchmark rows expose model-context sections and context-block order so the artifact can be reviewed without reading the full prompt.

## Sample run artifact list

- `.lumen/runs/<run_id>/trace.jsonl`
- `.lumen/runs/<run_id>/task_state.json`
- `.lumen/runs/<run_id>/report.json`
