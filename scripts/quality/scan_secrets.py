"""Conservative, dependency-free secret-pattern scanner for the P00 repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from common import EXCLUDED_PARTS, file_sha256, finding, iter_repository_files, repository_root, repository_state, utc_now, write_json

PATTERNS = {
    "PRIVATE_KEY": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "AWS_ACCESS_KEY": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "GITHUB_TOKEN": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,255}\b"),
    "GITHUB_FINE_GRAINED_TOKEN": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,255}\b"),
    "OPENAI_KEY": re.compile(r"\bsk-[A-Za-z0-9_-]{20,255}\b"),
    "DATABASE_URI_CREDENTIAL": re.compile(r"\b(?:postgres(?:ql)?|mysql|redis)://[^\s:/]+:[^\s@/]+@", re.IGNORECASE),
}
TEXT_SUFFIXES = {
    ".md", ".py", ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".conf", ".txt", ".env", ".sh", ".ps1",
}


def _baseline(path: Path) -> set[str]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    values = data.get("allowed_fingerprints", []) if isinstance(data, dict) else []
    return {value for value in values if isinstance(value, str)}


def scan(root: Path, baseline_path: Path) -> tuple[list[dict[str, Any]], list[Path], int]:
    allowed = _baseline(baseline_path)
    findings: list[dict[str, Any]] = []
    inputs: list[Path] = [baseline_path] if baseline_path.exists() else []
    scanned = 0
    for path in iter_repository_files(root):
        relative = path.relative_to(root).as_posix()
        if any(part in EXCLUDED_PARTS for part in path.relative_to(root).parts):
            continue
        if path.name.startswith(".env") and path.name != ".env.example":
            findings.append(finding("TRACKED_ENV_FILE", "Local environment file is present in repository scope", relative))
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".gitignore"}:
            continue
        if path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        scanned += 1
        inputs.append(path)
        for line_number, line in enumerate(text.splitlines(), 1):
            for code, pattern in PATTERNS.items():
                for match in pattern.finditer(line):
                    fingerprint = hashlib.sha256(f"{relative}:{code}:{match.group(0)}".encode()).hexdigest()
                    if fingerprint in allowed:
                        continue
                    findings.append(finding(code, f"Potential secret detected; fingerprint={fingerprint[:12]}", relative, line_number))
    return findings, inputs, scanned


def _sarif(findings: list[dict[str, Any]]) -> dict[str, Any]:
    results = []
    for item in findings:
        result: dict[str, Any] = {
            "ruleId": item["code"],
            "level": "error",
            "message": {"text": item["message"]},
        }
        if item.get("path"):
            result["locations"] = [{
                "physicalLocation": {
                    "artifactLocation": {"uri": item["path"]},
                    "region": {"startLine": item.get("line", 1)},
                }
            }]
        results.append(result)
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "p00-secret-scan", "version": "1.0.0"}},
            "results": results,
        }],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--format", choices=["sarif"], default="sarif")
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary-output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repository_root()
    baseline_path = (root / args.baseline).resolve()
    findings, inputs, scanned = scan(root, baseline_path)
    output = Path(args.output)
    write_json(output, _sarif(findings))
    summary = {
        "schema_version": "1.0.0",
        "gate_id": "CI-GATE-004",
        "result": "PASS" if not findings else "FAIL",
        "created_at": utc_now(),
        "producer": {"tool": "scan_secrets.py", "tool_version": "1.0.0", "python_version": sys.version.split()[0]},
        "repository": {
            **repository_state(root),
            "content_sha256": hashlib.sha256("".join(file_sha256(path) for path in inputs).encode()).hexdigest(),
        },
        "metrics": {"files_scanned": scanned, "finding_count": len(findings)},
        "findings": findings,
        "sarif_output": str(output),
        "sensitivity": "INTERNAL",
        "retention_class": "P00_FOUNDATION_EVIDENCE",
    }
    summary_path = Path(args.summary_output) if args.summary_output else output.with_suffix(".summary.json")
    write_json(summary_path, summary)
    print(json.dumps({"gate_id": "CI-GATE-004", "result": summary["result"], "output": str(output)}))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())

