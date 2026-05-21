# Lumen Runtime Refactor Plan

## Purpose

This plan describes how to turn the current codebase into a clearer lightweight agent runtime under the Lumen name.

The current feature set is already sufficient. The work here is intentionally not a feature expansion. The goal is to improve naming, module boundaries, runtime concepts, and public presentation so the project reads as a coherent engineering artifact for a team project and for job-search review.

## Goals

- Rename the project identity from the current legacy name to `lumen` across code, package metadata, CLI, docs, comments, tests, benchmark artifacts, and runtime text.
- Clarify the boundaries between session, run, task state, transcript, memory, model context, prompt, trace, report, and checkpoint.
- Refactor the prompt/context/memory path around a structured `ModelContext` concept instead of treating the final prompt string as the primary abstraction.
- Keep the runtime lightweight and local-first.
- Preserve existing behavior, benchmark coverage, and test confidence.
- Prefer clean refactors over compatibility layers where old boundaries were unclear.

## Non-Goals

- Do not add a graph runtime.
- Do not add vector memory or RAG infrastructure.
- Do not introduce LangChain, LangGraph, AutoGen, or another framework dependency.
- Do not add new model providers.
- Do not change the core user workflow unless required by the rename.
- Do not keep legacy naming shims in runtime code after the rename unless a short-lived migration note is strictly necessary.

## Target Vocabulary

The project should use these terms consistently:

| Term | Meaning |
| --- | --- |
| `Session` | A recoverable multi-run conversation container. |
| `Run` | One `ask()` invocation from user request to final answer or stop condition. |
| `TaskState` | Runtime control state for one run: attempts, tool steps, stop reason, checkpoint id. |
| `Transcript` | User, assistant, and tool interaction history within a session. |
| `Memory` | Distilled reusable knowledge selected from prior activity or durable notes. |
| `ModelContext` | Structured set of sections prepared for the model this turn. |
| `Prompt` | Rendered model input derived from `ModelContext`. |
| `Trace` | Append-only event log for audit and evaluation. |
| `Report` | Final run summary artifact. |
| `Checkpoint` | Recoverable snapshot for resume and drift detection. |
| `Workspace` | The local repository and files the agent can inspect or modify. |
| `ToolRegistry` | Available tool schemas, risk levels, validation, and execution hooks. |

## Target Architecture

Lumen should remain a compact single-agent coding runtime:

```text
CLI
  -> Runtime
      -> ModelClient
      -> ToolRegistry
      -> WorkspaceContext
      -> SessionStore
      -> RunStore
      -> Memory
      -> ModelContextBuilder
      -> PromptRenderer
      -> Evaluator
```

The important change is conceptual:

```text
current runtime/session/workspace/memory
  -> ModelContext
  -> Prompt
  -> model.complete()
```

Instead of:

```text
runtime fields
  -> prefix string + memory string + history string
  -> prompt
```

## Design Principles

- `State` is for runtime control.
- `Memory` is for reusable knowledge.
- `Transcript` is for what happened in the conversation.
- `Trace` is for audit, not model context by default.
- `Context` is structured before it is rendered.
- `Prompt` is a serialization target, not the source of truth.
- Workspace files remain artifacts; memory should store summaries, references, or stable facts.
- The benchmark suite should verify behavior after each phase.
- Renaming should be decisive: code should end up saying `lumen`, not carrying legacy names as normal runtime concepts.

## Phase Plan

### Phase 0: Planning Baseline

Deliverables:

- Add this refactor plan.
- Add a progress log for phase updates.
- Establish that no code behavior changes are included in the planning commit.

Validation:

- Docs exist and are tracked.

### Phase 1: Project Identity Rename

Deliverables:

- Rename package directory to `lumen`.
- Update package metadata in `pyproject.toml`.
- Update CLI command from legacy command to `lumen`.
- Update imports in tests, scripts, benchmarks, docs, and package metadata.
- Update runtime strings, welcome text, comments, generated report names, and benchmark metadata.
- Rename local runtime artifact paths where appropriate, for example `.lumen/`.
- Update README and docs to present the project as Lumen from the start.

Important choice:

- Because this is still pre-public-release, prefer a clean rename over runtime compatibility shims.
- If a one-time migration note is useful, place it in docs, not runtime code.

Validation:

- `uv sync`
- `uv run lumen --help`
- `uv run python -m pytest tests/test_evaluator.py -q`
- `uv run python -m pytest -q`

### Phase 2: Runtime Concept Documentation

Deliverables:

- Add `docs/architecture/runtime-concepts.md`.
- Define session, run, task state, transcript, memory, model context, prompt, trace, report, checkpoint, workspace, and tools.
- Include a compact architecture diagram.
- Document why Lumen remains single-agent and lightweight.
- Concept reference: [Runtime Concepts](runtime-concepts.md).

Validation:

- Docs reviewed for consistency with code after Phase 1.
- README links to the concept document.

### Phase 3: Structured ModelContext

Deliverables:

- Introduce a small `ModelContext` and `ContextSection` abstraction.
- Split context building from prompt rendering.
- Keep the public call site simple: runtime asks for a prompt and metadata, but internally the context is structured.
- Preserve current section order unless a test-backed reason changes it.

Suggested shape:

```python
@dataclass
class ContextSection:
    name: str
    raw: str
    budget: int | None = None
    rendered: str = ""
    details: dict | None = None

@dataclass
class ModelContext:
    sections: dict[str, ContextSection]
    metadata: dict
```

Validation:

- Existing prompt metadata tests continue to pass.
- Add focused tests for section construction and rendering.
- Benchmark pass rate remains 1.0.

### Phase 4: Prefix Split Into Explicit Context Blocks

Deliverables:

- Replace the overloaded `prefix` concept with explicit renderers:
  - system instructions
  - tool specs
  - tool examples
  - workspace context
  - checkpoint context
- Rename metadata keys where needed so they describe context sections, not just prompt prefix internals.

Validation:

- Prompt still contains equivalent instructions and tool schemas.
- Prompt cache key is based on stable context blocks.
- Context reduction tests continue to pass.

### Phase 5: Transcript, Memory, and Session Boundary Cleanup

Deliverables:

- Rename runtime usage of `history` to `transcript` in code and tests.
- Update session schema to use `transcript` as the primary concept.
- Keep memory focused on working summary, recent files, file summaries, episodic notes, and durable notes.
- Ensure transcript rendering and memory rendering are separate code paths.
- Keep `TaskState` focused on execution control only.

Important choice:

- Since this is a clean architecture pass, avoid normal runtime aliases like `history = transcript`.
- If old local sessions become invalid, document that pre-refactor sessions should be reset.

Validation:

- Resume tests updated to the new schema.
- Memory tests verify memory does not become a transcript duplicate.
- Full test suite passes.

### Phase 6: Evaluation and Artifact Terminology Cleanup

Deliverables:

- Update benchmark artifacts, reports, and scripts to use Lumen terminology.
- Ensure evaluator uses `ModelContext` metadata where useful.
- Keep deterministic fake model benchmark behavior unchanged.
- Update review-pack docs to describe the final architecture.

Validation:

- `uv run python -m pytest tests/test_evaluator.py -q`
- Generate a fresh benchmark artifact with 12/12 passing tasks.
- `uv run python -m pytest -q`

### Phase 7: Final Polish for Portfolio Readiness

Deliverables:

- Refresh README.
- Add architecture links.
- Add a short design tradeoffs section.
- Ensure comments and docstrings are readable and consistently encoded.
- Remove stale local artifacts from tracked scope.

Validation:

- Fresh clone instructions work.
- Full tests pass.
- README accurately describes the project as Lumen.

## Risk Register

| Risk | Mitigation |
| --- | --- |
| Rename touches many files and breaks imports. | Do Phase 1 as a dedicated stage with full tests before architecture refactor. |
| Clean schema rename invalidates old sessions. | Accept for pre-public-release and document reset behavior. |
| Context refactor changes prompt text too much. | Add focused tests around section order and benchmark behavior. |
| Architecture becomes too heavy. | Keep dataclasses small and avoid new framework dependencies. |
| Benchmark becomes coupled to implementation details. | Preserve outcome-level assertions and stable artifacts. |

## Working Rules

- Update `docs/architecture/lumen-refactor-progress.md` after each completed phase.
- Keep each phase reviewable and test-backed.
- Commit phase work separately.
- Use authorized Git tooling for push operations.
- Avoid commit messages that mention legacy project naming or rename details.
