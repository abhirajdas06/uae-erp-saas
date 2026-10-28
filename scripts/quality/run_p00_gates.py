"""Run the initial P00 gates with the same command locally and in CI."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from common import file_sha256, repository_root, repository_state, utc_now, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def _run(root: Path, name: str, command: list[str]) -> dict[str, Any]:
    started = time.monotonic()
    environment = os.environ.copy()
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", "TZ": "UTC"})
    result = subprocess.run(
        command,
        cwd=root,
        capture_output=True,
        text=True,
        env=environment,
        timeout=120,
    )
    return {
        "name": name,
        "command": command,
        "exit_code": result.returncode,
        "duration_seconds": round(time.monotonic() - started, 3),
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-4000:],
        "result": "PASS" if result.returncode == 0 else "FAIL",
    }


def main() -> int:
    args = parse_args()
    root = repository_root()
    output_dir = (root / args.output_dir).resolve()
    required_output_dir = (root / "build/evidence").resolve()
    if output_dir != required_output_dir:
        print("Output directory must be build/evidence", file=sys.stderr)
        return 2
    output_dir.mkdir(parents=True, exist_ok=True)
    for prior_artifact in output_dir.iterdir():
        if prior_artifact.is_file():
            prior_artifact.unlink()
    python = sys.executable
    commands = [
        (
            "manifest-validation",
            [python, "scripts/quality/validate_manifests.py", "--phase", "orchestration/phase-manifest.yml", "--task", "orchestration/task-manifest.yml", "--format", "json", "--output", str(output_dir / "manifests.json")],
        ),
        (
            "documentation-validation",
            [python, "scripts/quality/validate_docs.py", "--root", "docs", "--format", "json", "--output", str(output_dir / "docs.json")],
        ),
        (
            "governance-validation",
            [python, "scripts/quality/validate_governance.py", "--root", "docs", "--format", "json", "--output", str(output_dir / "governance.json")],
        ),
        (
            "secret-scan",
            [python, "scripts/quality/scan_secrets.py", "--baseline", ".secrets.baseline", "--format", "sarif", "--output", str(output_dir / "secrets.sarif"), "--summary-output", str(output_dir / "secrets.json")],
        ),
        (
            "validator-unit-tests",
            [python, "-m", "unittest", "discover", "-s", "tests/quality", "-v"],
        ),
    ]
    results: list[dict[str, Any]] = []
    for name, command in commands:
        try:
            results.append(_run(root, name, command))
        except subprocess.TimeoutExpired as exc:
            results.append({
                "name": name,
                "command": command,
                "exit_code": 124,
                "duration_seconds": 120,
                "stdout": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
                "stderr": "Command timed out",
                "result": "FAIL",
            })

    evidence_files = sorted(path for path in output_dir.iterdir() if path.is_file() and path.name != "p00-gate-summary.json")
    artifacts = [
        {
            "path": path.relative_to(root).as_posix(),
            "sha256": file_sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in evidence_files
    ]
    overall = "PASS" if all(item["exit_code"] == 0 for item in results) else "FAIL"
    summary = {
        "schema_version": "1.0.0",
        "evidence_id": "P00-EV-011",
        "gate_id": "P00-INITIAL-CI",
        "result": overall,
        "created_at": utc_now(),
        "producer": {
            "tool": "run_p00_gates.py",
            "tool_version": "1.0.0",
            "python_version": sys.version.split()[0],
            "command": "python scripts/quality/run_p00_gates.py --output-dir build/evidence",
        },
        "repository": repository_state(root),
        "execution_environment": {
            "ci": os.environ.get("CI", "").lower() == "true",
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_job": os.environ.get("GITHUB_JOB"),
            "network_required": False,
        },
        "results": results,
        "artifacts": artifacts,
        "artifact_set_sha256": hashlib.sha256("".join(item["sha256"] for item in artifacts).encode()).hexdigest(),
        "related_criteria": ["P00-AC-012", "P00-AC-013", "P00-T-001-AC-001", "P00-T-001-AC-002"],
        "sensitivity": "INTERNAL",
        "retention_class": "P00_FOUNDATION_EVIDENCE",
        "limitations": [
            "A local PASS proves command equivalence and local execution only; hosted GitHub Actions execution is separate evidence.",
            "External links are not network-checked by the documentation validator.",
            "The initial secret scanner is pattern-based and does not replace a later approved specialist scanner.",
        ],
    }
    summary_path = output_dir / "p00-gate-summary.json"
    write_json(summary_path, summary)
    print(json.dumps({"evidence_id": "P00-EV-011", "result": overall, "output": str(summary_path)}))
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

