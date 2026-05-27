import json

from lumen.smoke import run_smoke_regression


def test_run_smoke_regression_covers_core_runtime_abilities(tmp_path):
    artifact_path = tmp_path / "smoke-artifact.json"

    artifact = run_smoke_regression(workspace_root=tmp_path / "smoke", artifact_path=artifact_path)

    assert artifact_path.exists()
    assert json.loads(artifact_path.read_text(encoding="utf-8")) == artifact
    assert artifact["summary"] == {
        "total_checks": 6,
        "passed": 6,
        "failed": 0,
        "pass_rate": 1.0,
    }
    assert artifact["checks"] == {
        "read_file_answer": True,
        "delete_file_removed_scratch": True,
        "durable_memory_saved_preference": True,
        "run_reports_written": True,
        "all_runs_completed": True,
        "all_runs_final_answer": True,
    }
    assert artifact["run_count"] == 3
    assert artifact["tool_steps"] == [1, 1, 0]
    assert artifact["durable_promotions"] == ["user-preferences: 我偏好中文回答。"]
