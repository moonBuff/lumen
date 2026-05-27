from __future__ import annotations

import argparse
import json
from pathlib import Path

from lumen.smoke import run_smoke_regression


def main():
    parser = argparse.ArgumentParser(description="Run deterministic Lumen smoke regression.")
    parser.add_argument("--workspace-root", default=".lumen/smoke-regression", help="Directory for the smoke workspace.")
    parser.add_argument(
        "--artifact-path",
        default=".lumen/smoke-regression/artifact.json",
        help="Path to write the smoke regression artifact.",
    )
    args = parser.parse_args()

    artifact = run_smoke_regression(
        workspace_root=Path(args.workspace_root),
        artifact_path=Path(args.artifact_path),
    )
    print(json.dumps(artifact["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
