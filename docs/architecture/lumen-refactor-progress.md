# Lumen Runtime Refactor Progress

This log tracks the architecture cleanup and project identity work. Update it after every completed phase.

## Current Status

| Item | Status |
| --- | --- |
| Repository | `moonBuff/lumen` |
| Local path | Current local checkout |
| Planning baseline | Completed |
| Code rename | Completed |
| Runtime concept documentation | Completed |
| Structured model context | Completed |
| Explicit context blocks | Completed |
| Transcript/session cleanup | Completed |
| Evaluation artifact terminology | Completed |
| Context architecture refactor | Completed |
| DeepSeek provider client | Completed |
| Focused test status | `78 passed`; `13 passed, 6 warnings`; smoke `6/6 checks` after Phase 13 |

## Phase Tracker

| Phase | Name | Status | Result |
| --- | --- | --- | --- |
| 0 | Planning Baseline | Completed | Plan and progress docs were added. |
| 1 | Project Identity Rename | Completed | Package, CLI, runtime paths, tests, docs, and benchmark terminology now use Lumen. |
| 2 | Runtime Concept Documentation | Completed | Runtime vocabulary, boundaries, and lightweight architecture rationale are documented. |
| 3 | Structured ModelContext | Completed | Context sections are now structured before prompt rendering. |
| 4 | Explicit Context Blocks | Completed | Stable prompt context is split into explicit blocks and checkpoint context is a separate section. |
| 5 | Transcript, Memory, and Session Cleanup | Completed | Session conversation state now uses `transcript`; memory remains a separate distilled store. |
| 6 | Evaluation and Artifact Terminology Cleanup | Completed | Reports and benchmark rows now expose model-context sections and context-block order. |
| 7 | Compatibility Cleanup | Completed | Runtime and memory code now use only the current session, memory, and provider configuration schema. |
| 8 | DeepSeek Provider Client | Completed | DeepSeek now uses a dedicated chat-completions client instead of the Anthropic-compatible adapter. |
| 9 | Durable Memory Promotion | Completed | Explicit user memory requests now create durable-memory candidates before final-answer label parsing. |
| 10 | Run Failure Finalization | Completed | Model errors now finalize failed task state, trace, checkpoint, and report artifacts. |
| 11 | Controlled File Deletion Tool | Completed | Added a risky `delete_file` tool with workspace boundary checks, approval, and trace metadata. |
| 12 | Tool Budget and Limit Strategy | Completed | Default model budgets and near-limit tool guidance were tuned. |
| 13 | Smoke Regression Harness | Completed | Added a deterministic local smoke regression for core runtime abilities. |

## Progress Entries

### 2026-05-21: Phase 0 Started

Scope:

- Create the architecture refactor plan.
- Create this progress log.
- No runtime code changes.
- No package rename yet.

Notes:

- The goal is a clean lightweight runtime architecture, not a feature expansion.
- The planned refactor will favor clear boundaries over compatibility shims where old concepts were ambiguous.
- Future phase updates should include changed files, validation commands, and remaining risks.

Validation:

- Document files were created under `docs/architecture/`.

### 2026-05-21: Phase 0 Completed

Scope:

- Added the architecture refactor plan.
- Added this progress log.
- Defined the phase sequence for naming, context, memory, state, prompt, evaluation, and portfolio polish.
- No runtime code changes.
- No package rename yet.

Changed files:

- `.gitignore`
- `docs/architecture/lumen-refactor-plan.md`
- `docs/architecture/lumen-refactor-progress.md`

Validation:

- Confirmed both documents exist under `docs/architecture/`.
- Updated `.gitignore` so project docs are trackable.

Risks / follow-ups:

- Phase 1 will touch many files. It should be done as a dedicated rename stage with full test validation.
- Avoid adding compatibility shims unless there is a clear pre-release migration reason.

### 2026-05-21: Phase 1 Completed

Scope:

- Switched the Python package, CLI entry point, module entry point, runtime class names, tests, scripts, benchmark text, docs, environment variable prefix, and runtime artifact path to Lumen terminology.
- Changed local runtime artifacts to `.lumen/`.
- Updated README examples and provider configuration names to `LUMEN_*`.
- Renamed screenshot assets referenced by README.
- Included `uv.lock` in version control scope for repeatable `uv` installs.
- Kept this stage focused on identity and runtime path cleanup, without starting the context architecture refactor.

Changed files:

- `.env.example`
- `.gitignore`
- `README.md`
- `assets/screenshots/*`
- `benchmarks/coding_tasks.json`
- `docs/architecture/*`
- `docs/review-pack/README.md`
- `lumen/*`
- `pyproject.toml`
- `scripts/*`
- `tests/*`
- `uv.lock`

Validation:

- `uv sync` completed successfully.
- `uv run lumen --help` completed successfully.
- `uv run python -m lumen --help` completed successfully.
- `uv run python -c "import lumen; print(lumen.__name__); print(hasattr(lumen, 'LumenAgent'))"` completed successfully.
- `uv run python -m pytest tests/test_evaluator.py -q` -> `8 passed`.
- `uv run python -m ruff check lumen tests scripts pyproject.toml` -> all checks passed.
- `uv run python -m pytest -q` -> `104 passed, 1 skipped, 6 warnings`.
- Fresh benchmark artifact generation -> `12 passed`, `pass_rate: 1.0`.

Risks / follow-ups:

- Phase 2 should document the new runtime vocabulary before deeper context refactoring.
- Existing local pre-Phase-1 run/session artifacts are not migrated; new runs use `.lumen/`.
- The remaining warnings are existing `datetime.utcnow()` deprecation warnings in metrics code.

### 2026-05-21: Phase 2 Completed

Scope:

- Added a runtime concept document that defines session, run, task state, transcript, memory, model context, prompt, trace, report, checkpoint, workspace, tools, and evaluator.
- Documented the intended boundary between state, memory, transcript, context, prompt, trace, run, session, and workspace.
- Documented why Lumen should remain a compact single-agent runtime for the current project size.
- Linked the concept document from the refactor plan and README.
- No runtime behavior changes.

Changed files:

- `README.md`
- `docs/architecture/lumen-refactor-plan.md`
- `docs/architecture/lumen-refactor-progress.md`
- `docs/architecture/runtime-concepts.md`

Validation:

- Documentation reviewed against the Phase 1 code layout.
- `uv run lumen --help` completed successfully.
- `uv run python -m pytest tests/test_evaluator.py -q` -> `8 passed`.

Risks / follow-ups:

- Phase 3 should introduce the small `ModelContext` abstraction described in the concept document.
- Some implementation names still use existing internal terms such as session `history`; those are intentionally left for Phase 5.

### 2026-05-21: Phase 3 Completed

Scope:

- Added lightweight `ContextSection` and `ModelContext` dataclasses.
- Changed `ContextManager` to build structured model context before rendering the prompt.
- Kept the public `ContextManager.build()` return shape as `(prompt, metadata)` so runtime behavior stays stable.
- Added model-context metadata to prompt metadata for trace/report inspection.
- Added focused tests for structured context construction and rendering.
- Corrected the runtime concept document's evaluator mapping to the current code layout.

Changed files:

- `lumen/__init__.py`
- `lumen/context_manager.py`
- `lumen/model_context.py`
- `tests/test_context_manager.py`
- `docs/architecture/lumen-refactor-progress.md`
- `docs/architecture/runtime-concepts.md`

Validation:

- `uv run python -m pytest tests/test_context_manager.py -q` -> `8 passed`.
- `uv run python -m ruff check lumen tests scripts pyproject.toml` -> all checks passed.
- `uv run python -m pytest tests/test_evaluator.py tests/test_lumen.py -q` -> `66 passed`.
- `uv run python -m pytest -q` -> `105 passed, 1 skipped, 6 warnings`.
- Fresh benchmark artifact generation -> `12 passed`, `pass_rate: 1.0`.

Risks / follow-ups:

- Phase 4 should split the remaining overloaded `prefix` text into explicit context blocks.
- Session storage still uses `history`; that cleanup remains scoped to Phase 5.

### 2026-05-21: Phase 4 Completed

Scope:

- Split the stable runtime context into explicit renderers for system instructions, tool specs, tool examples, and workspace context.
- Added stable context block metadata, including block order, block hashes, and block character counts.
- Moved checkpoint text out of the stable prefix path and into a separate `checkpoint_context` model context section.
- Kept prompt ordering and cache behavior stable for existing runtime flows.
- Added focused assertions for explicit context block metadata.

Changed files:

- `lumen/context_manager.py`
- `lumen/model_context.py`
- `lumen/runtime.py`
- `tests/test_context_manager.py`
- `tests/test_lumen.py`
- `docs/architecture/lumen-refactor-progress.md`

Validation:

- `uv run python -m pytest tests/test_context_manager.py -q` -> `8 passed`.
- `uv run python -m pytest tests/test_lumen.py -q` -> `58 passed`.
- `uv run python -m ruff check lumen tests scripts pyproject.toml` -> all checks passed.
- `uv run python -m pytest tests/test_evaluator.py -q` -> `8 passed`.
- `uv run python -m pytest -q` -> `105 passed, 1 skipped, 6 warnings`.
- Fresh benchmark artifact generation -> `12 passed`, `pass_rate: 1.0`.

Risks / follow-ups:

- Phase 5 should rename runtime/session `history` concepts toward `transcript`.
- Existing metadata still includes `prefix_*` cache keys for continuity with current reports; the underlying context is now block-based.

### 2026-05-21: Phase 5 Completed

Scope:

- Changed the session conversation schema from `history` to `transcript`.
- Updated transcript rendering, context section budgets, prompt metadata, evaluator setup, metrics helpers, and tests to use transcript terminology.
- Kept memory focused on distilled reusable state rather than duplicating the transcript.
- Added a focused test that verifies new sessions use `transcript` without a runtime `history` alias.
- Updated benchmark setup terms from `history_count` / `history` budget to `transcript_count` / `transcript`.

Changed files:

- `benchmarks/coding_tasks.json`
- `docs/architecture/lumen-refactor-plan.md`
- `docs/architecture/lumen-refactor-progress.md`
- `docs/architecture/runtime-concepts.md`
- `lumen/cli.py`
- `lumen/context_manager.py`
- `lumen/evaluator.py`
- `lumen/memory.py`
- `lumen/metrics.py`
- `lumen/models.py`
- `lumen/runtime.py`
- `lumen/tools.py`
- `tests/test_context_manager.py`
- `tests/test_evaluator.py`
- `tests/test_lumen.py`
- `tests/test_safety_invariants.py`

Validation:

- `uv run python -m pytest tests/test_context_manager.py -q` -> `8 passed`.
- `uv run python -m pytest tests/test_lumen.py -q` -> `59 passed`.
- `uv run python -m pytest tests/test_evaluator.py -q` -> `8 passed`.
- `uv run python -m ruff check lumen tests scripts pyproject.toml` -> all checks passed.
- `uv run python -m pytest tests/test_metrics.py tests/test_safety_invariants.py -q` -> `16 passed, 1 skipped, 6 warnings`.
- `uv run python -m pytest -q` -> `106 passed, 1 skipped, 6 warnings`.
- Fresh benchmark artifact generation -> `12 passed`, `pass_rate: 1.0`.

Risks / follow-ups:

- Existing local sessions that still contain `history` should be reset for this pre-release refactor; the runtime does not keep a normal alias.
- Phase 6 should finish terminology cleanup in reports and review-pack presentation where useful.

### 2026-05-21: Phase 6 Completed

Scope:

- Added a top-level `model_context` summary to run reports.
- Added model-context section order, section count, context-block order, transcript rendered chars, and memory rendered chars to benchmark rows.
- Updated evaluator tests to assert the benchmark artifact exposes the current context architecture.
- Updated review-pack docs to describe the final ModelContext, transcript, memory, trace, and report boundaries.
- Updated runtime concepts so ModelContext points to the current implementation.
- Kept deterministic fake-model benchmark behavior unchanged.

Changed files:

- `docs/architecture/lumen-refactor-progress.md`
- `docs/architecture/runtime-concepts.md`
- `docs/review-pack/README.md`
- `lumen/evaluator.py`
- `lumen/runtime.py`
- `tests/test_evaluator.py`
- `tests/test_lumen.py`

Validation:

- `uv run python -m pytest tests/test_evaluator.py -q` -> `8 passed`.
- `uv run python -m pytest tests/test_lumen.py -q` -> `59 passed`.
- `uv run python -m ruff check lumen tests scripts pyproject.toml` -> all checks passed.
- `uv run python -m pytest -q` -> `106 passed, 1 skipped, 6 warnings`.
- Fresh benchmark artifact generation -> `12 passed`, `pass_rate: 1.0`, model context sections exposed in rows.

Risks / follow-ups:

- Phase 7 should polish README and portfolio-facing documentation, then run a fresh clone style verification.
- `prefix_*` cache metadata remains in reports for continuity; context-block metadata is now also available for architecture review.

### 2026-05-23: Phase 7 Completed

Scope:

- Removed old memory alias fields from the runtime memory schema.
- Removed session `history` migration logic from runtime startup.
- Removed provider environment variable fallback paths; provider configuration now uses `LUMEN_*` names only.
- Updated delegate memory initialization to use the current `LayeredMemory` API.
- Updated tests and local architecture notes to match the current schema.

Changed files:

- `docs/architecture/lumen-refactor-progress.md`
- `docs/architecture/lumen-architecture-interview-guide.zh.md`
- `docs/architecture/lumen-current-architecture-implementation.zh.md`
- `lumen/cli.py`
- `lumen/config.py`
- `lumen/memory.py`
- `lumen/metrics.py`
- `lumen/runtime.py`
- `lumen/tools.py`
- `tests/test_lumen.py`
- `tests/test_memory.py`
- `tests/test_metrics.py`

Validation:

- `uv run python -m pytest tests/test_memory.py tests/test_lumen.py tests/test_metrics.py tests/test_safety_invariants.py -q` -> `82 passed, 1 skipped, 6 warnings`.
- `uv run python -m ruff check lumen tests scripts pyproject.toml` -> all checks passed.

Risks / follow-ups:

- Existing local sessions that still contain removed fields should be discarded or reset.
- Users should configure providers through `LUMEN_*` environment variables or `.env` entries.

### 2026-05-27: Phase 8 Completed

Scope:

- Added a dedicated `DeepSeekModelClient` using the chat-completions endpoint.
- Routed CLI `--provider deepseek` and provider metrics experiments through the new DeepSeek client.
- Updated DeepSeek defaults to use the native API base URL.
- Added response-shape diagnostics for reasoning-only responses without message content.
- Updated provider tests so DeepSeek no longer depends on the Anthropic-compatible adapter.

Changed files:

- `.env.example`
- `docs/architecture/lumen-refactor-progress.md`
- `lumen/__init__.py`
- `lumen/cli.py`
- `lumen/metrics.py`
- `lumen/models.py`
- `tests/test_lumen.py`
- `tests/test_metrics.py`
- `tests/test_safety_invariants.py`

Validation:

- `uv run python -m pytest tests/test_lumen.py -q` -> `63 passed`.
- `uv run python -m pytest tests/test_safety_invariants.py -q` -> `11 passed, 1 skipped`.
- `uv run python -m pytest tests/test_metrics.py -q` -> `5 passed, 6 warnings`.

Risks / follow-ups:

- DeepSeek reasoning-only responses now fail with a clearer provider-specific error; Phase 10 should ensure such model errors always finalize the run artifact cleanly.
- Local `.env` files using the old DeepSeek Anthropic-compatible base URL should be updated to the native DeepSeek API base.

### 2026-05-27: Phase 9 Completed

Scope:

- Added a user-request extraction path for durable memory promotion.
- Natural requests such as `Remember: ...` and `请记住：...` now create durable-memory candidates even when the model final answer is unlabeled.
- Kept the existing labeled final-answer path for `Project convention:`, `Decision:`, `Dependency:`, and `Preference:` facts.
- Reused runtime审核 for secret-shaped text, transient task state, noisy output, dedupe, and supersede behavior.
- Added tests for English and Chinese preference capture plus secret-shaped request rejection.

Changed files:

- `docs/architecture/lumen-refactor-progress.md`
- `lumen/runtime.py`
- `tests/test_lumen.py`

Validation:

- `uv run python -m pytest tests/test_lumen.py -q` -> `66 passed`.
- `uv run python -m pytest tests/test_memory.py tests/test_safety_invariants.py -q` -> `16 passed, 1 skipped`.
- `uv run python -m pytest tests/test_metrics.py -q` -> `5 passed, 6 warnings`.
- `uv run python -m ruff check lumen tests` -> all checks passed.

Risks / follow-ups:

- Topic inference remains intentionally lightweight and rule-based; it is enough for explicit user preferences and stable facts, but not a full semantic memory classifier.
- Phase 10 should make model/runtime exceptions finalize run artifacts cleanly instead of leaving incomplete runs.

### 2026-05-27: Phase 10 Completed

Scope:

- Added failed-run finalization for model backend errors raised during `ask()`.
- Failed model calls now write `task_state.json`, `trace.jsonl`, `report.json`, and a checkpoint reference.
- Added a `run_failed` trace event with status, stop reason, error type, redacted error text, and run duration.
- Kept CLI-facing behavior unchanged by re-raising the model error after artifacts are finalized.
- Added regression coverage to ensure secret-shaped error text is redacted from report and trace artifacts.

Changed files:

- `docs/architecture/lumen-refactor-progress.md`
- `lumen/runtime.py`
- `tests/test_lumen.py`

Validation:

- `uv run python -m pytest tests/test_lumen.py -q` -> `67 passed`.
- `uv run python -m pytest tests/test_task_state.py tests/test_run_store.py tests/test_safety_invariants.py tests/test_evaluator.py -q` -> `29 passed, 1 skipped`.
- `uv run python -m pytest tests/test_metrics.py -q` -> `5 passed, 6 warnings`.
- `uv run python -m ruff check lumen tests` -> all checks passed.

Risks / follow-ups:

- This phase handles model-client `RuntimeError` paths. Broader runtime exception classification can be expanded later if needed.
- Phase 11 should add a controlled file deletion tool so the model does not need to use shell commands for simple file removal.

### 2026-05-27: Phase 11 Completed

Scope:

- Added a first-class `delete_file(path)` tool.
- Kept deletion inside the normal risky-tool pipeline, including approval, workspace snapshots, trace metadata, and diff summaries.
- Rejected workspace escape, directory deletion, and deletion under `.git` or `.lumen`.
- Updated prompt tool instructions and examples so the model can prefer `delete_file` over shell commands for simple file removal.
- Added trace-contract and safety regression tests for controlled deletion.

Changed files:

- `docs/architecture/lumen-refactor-progress.md`
- `lumen/runtime.py`
- `lumen/tools.py`
- `tests/test_lumen.py`
- `tests/test_safety_invariants.py`

Validation:

- `uv run python -m pytest tests/test_lumen.py tests/test_safety_invariants.py -q` -> `82 passed, 1 skipped`.
- `uv run python -m pytest tests/test_context_manager.py tests/test_evaluator.py tests/test_run_store.py tests/test_task_state.py -q` -> `26 passed`.
- `uv run python -m pytest tests/test_metrics.py -q` -> `5 passed, 6 warnings`.
- `uv run python -m ruff check lumen tests` -> all checks passed.

Risks / follow-ups:

- `delete_file` intentionally deletes only regular files, not directories.
- Phase 12 should tune tool budget and prompt strategy to reduce avoidable step-limit stops on larger code-reading tasks.

### 2026-05-27: Phase 12 Completed

Scope:

- Raised the default interactive step budget from 6 to 8.
- Raised the default per-step model output budget from 512 to 1024 tokens.
- Added `tool_budget` prompt metadata so traces/reports can explain how many tool calls were used and how many remain.
- Added near-limit current-request guidance when only one or zero tool calls remain, nudging the model to finalize from known evidence unless one more tool call is essential.
- Updated the memory metrics experiment fact that refers to the default step budget.
- Added regression coverage for CLI defaults and near-limit prompt guidance.

Changed files:

- `docs/architecture/lumen-refactor-progress.md`
- `lumen/cli.py`
- `lumen/context_manager.py`
- `lumen/metrics.py`
- `lumen/runtime.py`
- `tests/test_context_manager.py`
- `tests/test_lumen.py`

Validation:

- `uv run python -m pytest tests/test_context_manager.py tests/test_lumen.py -q` -> `78 passed`.
- `uv run python -m pytest tests/test_evaluator.py tests/test_metrics.py -q` -> `13 passed, 6 warnings`.
- `uv run python -m ruff check lumen tests` -> all checks passed.

Risks / follow-ups:

- The larger default budget may slightly increase token usage on real providers, but should reduce premature stop-limit failures.
- The existing metrics warning still comes from `datetime.utcnow()` and can be cleaned in a future maintenance pass.

### 2026-05-27: Phase 13 Completed

Scope:

- Added a deterministic smoke regression module for core local runtime abilities.
- Covered read-file, controlled delete, explicit durable-memory persistence, run report creation, and final-answer stop reasons without calling a real provider.
- Added a script entry point for local smoke checks under `.lumen/smoke-regression/`.
- Added pytest coverage for the smoke artifact and expected checks.

Changed files:

- `docs/architecture/lumen-refactor-progress.md`
- `lumen/smoke.py`
- `scripts/run_smoke_regression.py`
- `tests/test_smoke.py`

Validation:

- `uv run python -m pytest tests/test_smoke.py -q` -> `1 passed`.
- `uv run python scripts/run_smoke_regression.py --workspace-root .lumen/smoke-regression --artifact-path .lumen/smoke-regression/artifact.json` -> `6/6 checks passed`.
- `uv run python -m pytest tests/test_smoke.py tests/test_lumen.py -q` -> `70 passed`.
- `uv run python -m pytest tests/test_evaluator.py tests/test_metrics.py -q` -> `13 passed, 6 warnings`.
- `uv run python -m ruff check lumen tests scripts` -> all checks passed.

Risks / follow-ups:

- This smoke harness validates runtime wiring with scripted model outputs. Real provider behavior should still be checked manually after larger prompt or client changes.
- The smoke artifact is written under ignored `.lumen/` local state by default and is not committed.

## Update Template

Use this template after each phase:

```markdown
### YYYY-MM-DD: Phase N Completed

Scope:

- ...

Changed files:

- ...

Validation:

- `command`
- result

Risks / follow-ups:

- ...
```
