"""Deterministic smoke regression for core Lumen runtime abilities."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from .models import FakeModelClient
from .runtime import Lumen, SessionStore
from .run_store import RunStore
from .workspace import WorkspaceContext


SMOKE_SCRIPTED_OUTPUTS = [
    '<tool>{"name":"read_file","args":{"path":"README.md"}}</tool>',
    "<final>Repository name is lumen-smoke.</final>",
    '<tool>{"name":"delete_file","args":{"path":"scratch.txt"}}</tool>',
    "<final>Deleted scratch.txt.</final>",
    "<final>已记住你的中文回答偏好。</final>",
]


def _prepare_workspace(root):
    workspace = Path(root) / "workspace"
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    (workspace / "README.md").write_text("# lumen-smoke\n\nSmoke workspace for Lumen.\n", encoding="utf-8")
    (workspace / "scratch.txt").write_text("temporary scratch\n", encoding="utf-8")
    return workspace


def _report_paths(run_root):
    return sorted(Path(run_root).glob("*/report.json"))


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_smoke_regression(workspace_root=None, artifact_path=None):
    """Run a small deterministic end-to-end regression without a real provider.

    The smoke checks cover the practical abilities users tend to test manually:
    reading a file, deleting a file through the controlled tool, persisting an
    explicit memory request, and writing run artifacts for each request.
    """

    temp_dir = None
    if workspace_root is None:
        temp_dir = tempfile.TemporaryDirectory(prefix="lumen-smoke-")
        workspace_root = Path(temp_dir.name)
    else:
        workspace_root = Path(workspace_root)
        workspace_root.mkdir(parents=True, exist_ok=True)

    try:
        workspace_path = _prepare_workspace(workspace_root)
        workspace = WorkspaceContext.build(workspace_path, repo_root_override=workspace_path)
        session_store = SessionStore(workspace_path / ".lumen" / "sessions")
        run_store = RunStore(workspace_path / ".lumen" / "runs")
        agent = Lumen(
            model_client=FakeModelClient(SMOKE_SCRIPTED_OUTPUTS),
            workspace=workspace,
            session_store=session_store,
            run_store=run_store,
            approval_policy="auto",
            max_steps=4,
            max_new_tokens=256,
        )

        answers = [
            agent.ask("Read README.md and tell me the repository name."),
            agent.ask("Delete scratch.txt."),
            agent.ask("请记住：我偏好中文回答。"),
        ]

        reports = [_read_json(path) for path in _report_paths(run_store.root)]
        preference_path = workspace_path / ".lumen" / "memory" / "topics" / "user-preferences.md"
        checks = {
            "read_file_answer": answers[0] == "Repository name is lumen-smoke.",
            "delete_file_removed_scratch": not (workspace_path / "scratch.txt").exists(),
            "durable_memory_saved_preference": preference_path.exists()
            and "我偏好中文回答" in preference_path.read_text(encoding="utf-8"),
            "run_reports_written": len(reports) == 3,
            "all_runs_completed": all(report.get("status") == "completed" for report in reports),
            "all_runs_final_answer": all(report.get("stop_reason") == "final_answer_returned" for report in reports),
        }
        artifact = {
            "schema_version": 1,
            "kind": "lumen-smoke-regression",
            "workspace_relpath": "workspace",
            "summary": {
                "total_checks": len(checks),
                "passed": sum(1 for value in checks.values() if value),
                "failed": sum(1 for value in checks.values() if not value),
                "pass_rate": sum(1 for value in checks.values() if value) / len(checks),
            },
            "checks": checks,
            "answers": answers,
            "run_count": len(reports),
            "tool_steps": [int(report.get("tool_steps", 0) or 0) for report in reports],
            "durable_promotions": [promotion for report in reports for promotion in report.get("durable_promotions", [])],
        }
        if artifact_path is not None:
            artifact_path = Path(artifact_path)
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return artifact
    finally:
        if temp_dir is not None:
            temp_dir.cleanup()
