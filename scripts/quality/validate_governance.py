"""Validate ADR, phase, approval, workflow, and evidence governance invariants."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from common import emit_and_exit, evidence_envelope, finding, repository_root, safe_repo_path


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate(root: Path, docs_root: Path) -> tuple[list[dict[str, object]], dict[str, object], list[Path]]:
    findings: list[dict[str, object]] = []
    inputs: list[Path] = []
    adr_dir = docs_root / "01-architecture/ARCHITECTURAL_DECISIONS"
    adr_files = sorted(adr_dir.glob("ADR-[0-9][0-9][0-9]-*.md"))
    inputs.extend(adr_files)
    numbers = [int(path.name[4:7]) for path in adr_files]
    if numbers != list(range(1, 21)):
        findings.append(finding("GOV_ADR_SEQUENCE", f"Expected ADR-001 through ADR-020, got {numbers}"))
    for path in adr_files:
        text = _read(path)
        if not re.search(r"^\| Status \| ACCEPTED \|\s*$", text, re.MULTILINE):
            findings.append(finding("GOV_ADR_STATUS", "ADR file is not ACCEPTED", path.relative_to(root).as_posix()))
        if not re.search(r"\*\*Current status:\*\* ACCEPTED", text, re.IGNORECASE):
            findings.append(finding("GOV_ADR_APPROVAL", "ADR approval section is not ACCEPTED", path.relative_to(root).as_posix()))

    register = adr_dir / "README.md"
    decisions = docs_root / "07-project-management/DECISIONS_PENDING.md"
    phase_status = docs_root / "07-project-management/PHASE_STATUS.md"
    p00_matrix = docs_root / "02-phases/P00_FOUNDATION/P00_TRACEABILITY_MATRIX.md"
    p01_matrix = docs_root / "02-phases/P01_CORE_PLATFORM/P01_TENANT_ISOLATION_TEST_MATRIX.md"
    quality_files = [
        docs_root / "05-quality/SECURITY_REQUIREMENTS.md",
        docs_root / "05-quality/TESTING_STRATEGY.md",
        docs_root / "05-quality/CI_QUALITY_GATES.md",
    ]
    inputs.extend([register, decisions, phase_status, p00_matrix, p01_matrix, *quality_files])
    register_text = _read(register)
    for number in range(1, 21):
        adr_id = f"ADR-{number:03d}"
        pattern = rf"^\| {adr_id} \|.*\| ACCEPTED \|"
        if not re.search(pattern, register_text, re.MULTILINE):
            findings.append(finding("GOV_ADR_REGISTER", f"{adr_id} is not ACCEPTED in the ADR register"))

    decision_text = _read(decisions)
    for decision_id in ("DEC-GOV-002", "DEC-GOV-006", "DEC-QA-005"):
        if not re.search(rf"^\| {decision_id} \|.*\| APPROVED \|", decision_text, re.MULTILINE):
            findings.append(finding("GOV_DECISION_STATUS", f"{decision_id} is not APPROVED in the decision register"))
    phase_text = _read(phase_status)
    if not re.search(r"^\| P00 \|.*\| (?:SPECIFICATION_IN_PROGRESS|IN_PROGRESS|IN_REVIEW|AWAITING_HUMAN_APPROVAL|APPROVED) \|", phase_text, re.MULTILINE):
        findings.append(finding("GOV_P00_STATUS", "P00 phase status is not an allowed lifecycle state"))
    p01_awaiting = re.search(r"^\| P01 \|.*\| AWAITING_APPROVAL \| Not authorized \|", phase_text, re.MULTILINE)
    p01_authorized = re.search(r"^\| P01 \|.*\| AUTHORIZED \|", phase_text, re.MULTILINE)
    if not (p01_awaiting or p01_authorized):
        findings.append(finding("GOV_P01_GUARD", "P01 phase status is not an allowed lifecycle state"))
    elif p01_authorized and not re.search(r"APPR-P01-001", decision_text):
        findings.append(
            finding(
                "GOV_P01_GUARD",
                "P01 is AUTHORIZED but no APPR-P01-001 authorization is recorded in the decision register",
            )
        )

    p00_text = _read(p00_matrix)
    p00_ids = sorted(set(re.findall(r"\bP00-AC-[0-9]{3}\b", p00_text)))
    expected_p00 = [f"P00-AC-{number:03d}" for number in range(1, 18)]
    if p00_ids != expected_p00:
        findings.append(finding("GOV_P00_CRITERIA", "P00 acceptance criteria are incomplete or non-sequential"))
    p01_text = _read(p01_matrix)
    p01_ids = sorted(set(re.findall(r"\bP01-TEN-TST-[0-9]{3}\b", p01_text)))
    expected_p01 = [f"P01-TEN-TST-{number:03d}" for number in range(1, 54)]
    if p01_ids != expected_p01:
        findings.append(finding("GOV_P01_TEST_IDS", "P01 tenant-isolation test IDs are incomplete or non-sequential"))
    rows = re.findall(r"^\| P01-TEN-TST-[0-9]{3} \|.*\| ([A-Z_]+) \|\s*$", p01_text, re.MULTILINE)
    if len(rows) != 53 or any(state != "NOT_RUN" for state in rows):
        findings.append(finding("GOV_P01_TEST_STATE", "Every P01 tenant-isolation scenario must remain NOT_RUN before execution"))

    for path in quality_files:
        text = _read(path)
        if "| Status | APPROVED" not in text:
            findings.append(finding("GOV_QUALITY_STATUS", "Quality baseline is not approved", path.relative_to(root).as_posix()))

    workflow = root / ".github/workflows/p00-quality.yml"
    if workflow.exists():
        inputs.append(workflow)
        workflow_text = _read(workflow)
        required_fragments = [
            "permissions:\n  contents: read",
            "id-token: none",
            "python scripts/quality/run_p00_gates.py --output-dir build/evidence",
            "timeout-minutes:",
        ]
        for fragment in required_fragments:
            if fragment not in workflow_text:
                findings.append(finding("GOV_WORKFLOW_CONTROL", f"Workflow is missing required control: {fragment!r}"))
        if "pull_request_target" in workflow_text:
            findings.append(finding("GOV_WORKFLOW_TRIGGER", "Workflow must not use pull_request_target"))
        uses = re.findall(r"^\s*- uses:\s*([^\s]+)", workflow_text, re.MULTILINE)
        for action in uses:
            ref = action.rsplit("@", 1)[-1]
            if not re.fullmatch(r"[0-9a-f]{40}", ref):
                findings.append(finding("GOV_ACTION_PIN", f"Action is not pinned to a full SHA: {action}"))
    else:
        findings.append(finding("GOV_WORKFLOW_MISSING", "Initial P00 workflow is missing"))

    metrics: dict[str, object] = {
        "adr_count": len(adr_files),
        "p00_acceptance_criteria_count": len(p00_ids),
        "p01_tenant_test_count": len(p01_ids),
        "p01_not_run_count": rows.count("NOT_RUN"),
        "workflow_present": workflow.exists(),
    }
    return findings, metrics, inputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--format", choices=["json"], default="json")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repository_root()
    docs_root = safe_repo_path(root, args.root)
    if docs_root is None or not docs_root.is_dir():
        findings = [finding("GOV_ROOT", f"Documentation root does not exist: {args.root!r}")]
        metrics: dict[str, object] = {}
        inputs: list[Path] = []
    else:
        findings, metrics, inputs = validate(root, docs_root)
    evidence = evidence_envelope(
        gate_id="CI-GATE-003",
        command="python scripts/quality/validate_governance.py",
        root=root,
        input_files=inputs,
        findings=findings,
        metrics=metrics,
    )
    return emit_and_exit(evidence, Path(args.output))


if __name__ == "__main__":
    sys.exit(main())

