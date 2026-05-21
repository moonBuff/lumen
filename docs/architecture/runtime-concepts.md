# Lumen Runtime Concepts

This document defines the runtime vocabulary used by Lumen. It is intentionally lightweight: the project should be easy to understand as a compact single-agent runtime, while still using boundaries that are familiar in mainstream agent systems.

## Design Intent

Lumen is a local-first coding agent runtime. It should keep the current feature set, but make the path from user task to model input easier to reason about.

The main architecture rule is:

```text
Runtime data -> ModelContext -> Prompt -> ModelClient
```

`Prompt` is the rendered model input. It should not be the source of truth for runtime state, memory, transcript, or tool metadata.

## Compact Architecture

```text
CLI / REPL
  -> Runtime
      -> SessionStore
      -> RunStore
      -> TaskState
      -> Memory
      -> WorkspaceContext
      -> ToolRegistry
      -> ModelContextBuilder
      -> PromptRenderer
      -> ModelClient
      -> Evaluator
```

The runtime remains single-agent by design. Lumen does not need a graph scheduler, multi-agent coordinator, vector database, or framework dependency for its current scope. A smaller runtime is easier to inspect, evaluate, and present as an engineering project.

## Core Terms

| Term | Meaning | Current code mapping |
| --- | --- | --- |
| `Session` | A recoverable multi-run conversation container. It owns the conversation transcript and session-level metadata. | `lumen.session.SessionStore`, files under `.lumen/sessions/`. |
| `Run` | One user request from `ask()` start to final answer, error, or stop condition. | `lumen.run_store.RunStore`, files under `.lumen/runs/<run_id>/`. |
| `TaskState` | Execution control state for one run: attempts, tool calls, stop reason, checkpoint id, and pending resume information. | `lumen.task_state.TaskState`. |
| `Transcript` | User, assistant, and tool interaction history inside a session. It records conversation flow, not distilled knowledge. | Currently stored as session `history`; later phases should rename this concept in code. |
| `Memory` | Reusable knowledge distilled from prior activity or durable notes. Memory should summarize or reference useful facts instead of duplicating the transcript. | `lumen.memory.MemoryManager` and related memory records. |
| `ModelContext` | A structured set of sections prepared for the model on a turn: instructions, tools, workspace, transcript slice, memory, task state hints, and checkpoint context. | Target abstraction for Phase 3. Current behavior is assembled through context and prompt helpers. |
| `Prompt` | The final serialized text sent to the model. It is derived from `ModelContext`. | Current rendered model input produced before `ModelClient.complete()`. |
| `Trace` | Append-only audit log for what the runtime did. Trace is for debugging, evaluation, and review; it is not model context by default. | `.lumen/runs/<run_id>/trace.jsonl`. |
| `Report` | Final run summary artifact with outcome, metrics, and useful metadata. | `.lumen/runs/<run_id>/report.json`. |
| `Checkpoint` | Recoverable snapshot used for resume and drift detection. It should describe enough state to continue a run safely. | `checkpoint_id` and run/session artifacts. |
| `Workspace` | The local project files and shell context the agent can inspect or modify. | Workspace context and shell/file tools. |
| `ToolRegistry` | Tool definitions, risk levels, validation, and execution hooks available to the runtime. | `lumen.tools` and tool execution helpers. |
| `Evaluator` | Deterministic benchmark and scoring path used to verify runtime behavior. | `lumen.evaluator` and benchmark helpers. |

## Boundary Rules

### State vs Memory

`TaskState` answers "what is the runtime doing right now?" It changes during a run and controls execution.

`Memory` answers "what reusable knowledge should the model know?" It should be selected and rendered into context only when useful.

### Transcript vs Memory

`Transcript` is the factual conversation record. It can be long, repetitive, and turn-based.

`Memory` is distilled. It may contain summaries, preferences, stable project facts, or references to important files. It should not become a second copy of the full transcript.

### Context vs Prompt

`ModelContext` is structured. It should preserve section names, metadata, budgets, and source information.

`Prompt` is rendered. It exists because current model APIs need text input, but it should be treated as an output format.

### Trace vs Transcript

`Transcript` is conversational and may be selected for model input.

`Trace` is operational. It should include events that are useful for audit and evaluation, even when those events should not be shown to the model.

### Run vs Session

A `Session` can contain many turns across time.

A `Run` is one execution attempt for one user request. Run artifacts are useful for debugging and evaluation because they are bounded and reproducible.

### Workspace vs Memory

Workspace files are source artifacts. Memory can reference or summarize them, but should not silently replace file reads when exact code matters.

## Suggested ModelContext Sections

Phase 3 should keep this small:

```text
system_instructions
tool_specs
tool_examples
workspace_context
checkpoint_context
memory
transcript
task_request
```

Each section should be independently buildable, testable, and renderable. The renderer can preserve the current prompt order while making the underlying data model explicit.

## Why Not a Heavier Runtime

Mainstream agent frameworks often include graph execution, planner/executor splits, multi-agent coordination, vector memory, retrieval pipelines, and provider abstraction layers. Those are useful when the product needs them, but Lumen currently does not.

For this project, the stronger portfolio signal is a clear compact runtime:

- one runtime loop,
- explicit tool execution boundaries,
- structured model context,
- separated transcript and memory,
- deterministic evaluation,
- readable local artifacts.

This keeps the project aligned with common agent architecture concepts without making the implementation larger than the product.

## Phase Notes

Phase 2 documents the target vocabulary. Some current code may still use older internal names such as `history` or build prompt text directly in places. Later phases should refactor those names decisively instead of adding compatibility layers around ambiguous concepts.
