"""Shared, dependency-free helpers for P00 quality gates."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

TOOL_VERSION = "1.0.0"
EXCLUDED_PARTS = {".git", "build", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git_value(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() or None


def repository_state(root: Path) -> dict[str, Any]:
    status = git_value(root, "status", "--porcelain")
    return {
        "commit_sha": git_value(root, "rev-parse", "HEAD") or "UNAVAILABLE",
        "branch": git_value(root, "branch", "--show-current") or "UNAVAILABLE",
        "working_tree_dirty": bool(status),
    }


def iter_repository_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in EXCLUDED_PARTS for part in path.relative_to(root).parts):
            continue
        yield path


def content_digest(root: Path, paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted({p.resolve() for p in paths}):
        relative = path.relative_to(root.resolve()).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_repo_path(root: Path, value: str) -> Path | None:
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def evidence_envelope(
    *,
    gate_id: str,
    command: str,
    root: Path,
    input_files: Iterable[Path],
    findings: list[dict[str, Any]],
    metrics: dict[str, Any],
    result: str | None = None,
) -> dict[str, Any]:
    files = list(input_files)
    state = repository_state(root)
    outcome = result or ("PASS" if not findings else "FAIL")
    return {
        "schema_version": "1.0.0",
        "gate_id": gate_id,
        "result": outcome,
        "created_at": utc_now(),
        "producer": {
            "tool": Path(sys.argv[0]).name,
            "tool_version": TOOL_VERSION,
            "python_version": sys.version.split()[0],
            "command": command,
        },
        "repository": {
            **state,
            "content_sha256": content_digest(root, files),
        },
        "metrics": metrics,
        "findings": findings,
        "sensitivity": "INTERNAL",
        "retention_class": "P00_FOUNDATION_EVIDENCE",
    }


def emit_and_exit(evidence: dict[str, Any], output: Path) -> int:
    write_json(output, evidence)
    print(json.dumps({"gate_id": evidence["gate_id"], "result": evidence["result"], "output": str(output)}))
    return 0 if evidence["result"] == "PASS" else 1


def finding(code: str, message: str, path: str | None = None, line: int | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {"code": code, "message": message, "severity": "ERROR"}
    if path is not None:
        value["path"] = path
    if line is not None:
        value["line"] = line
    return value

