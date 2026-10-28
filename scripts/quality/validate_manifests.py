"""Validate the P00 phase/task manifests without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from common import emit_and_exit, evidence_envelope, finding, load_json, repository_root, safe_repo_path

PHASE_ID = re.compile(r"^P(?:0[0-9]|1[0-2])$")
TASK_ID = re.compile(r"^P(?:0[0-9]|1[0-2])-T-[0-9]{3}$")
CRITERION_ID = re.compile(r"^P(?:0[0-9]|1[0-2])(?:-T-[0-9]{3})?-AC-[0-9]{3}$")
ADR_ID = re.compile(r"^ADR-[0-9]{3}$")
DECISION_ID = re.compile(r"^DEC-[A-Z]+-[0-9]{3}$")
PHASE_STATUSES = {
    "PLANNED", "SPECIFICATION_IN_PROGRESS", "AWAITING_APPROVAL", "READY", "IN_PROGRESS",
    "BLOCKED", "IN_REVIEW", "REJECTED", "AWAITING_HUMAN_APPROVAL", "APPROVED", "DEFERRED", "CANCELLED",
}
TASK_STATUSES = {"TODO", "READY", "IN_PROGRESS", "BLOCKED", "IN_REVIEW", "FAILED", "DONE", "CANCELLED"}
CRITERION_STATES = {"NOT_STARTED", "PARTIAL", "VERIFIED", "FAILED", "DEFERRED", "NOT_APPLICABLE"}
PHASE_REQUIRED = {
    "id", "title", "status", "specification", "owner_roles", "dependencies", "entry_criteria", "exit_criteria",
    "required_decisions", "required_adrs", "tasks", "evidence", "approvals", "implementation_authorized",
    "authorization_reference", "exceptions", "updated_at",
}
TASK_REQUIRED = {
    "id", "phase_id", "title", "objective", "status", "scope", "owner_role", "reviewer_roles", "dependencies",
    "requirements", "adrs", "risks", "decisions", "acceptance_criteria", "commands", "permissions",
    "evidence_requirements", "rollback_or_recovery", "implementation_authorized", "authorization_reference",
    "exceptions", "updated_at",
}
FORBIDDEN_VALUE_KEYS = {"password", "secret", "token", "api_key", "private_key", "credential"}


def _duplicates(values: list[str]) -> set[str]:
    return {value for value in values if values.count(value) > 1}


def _cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    found: list[list[str]] = []
    visiting: list[str] = []
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            found.append(visiting[visiting.index(node):] + [node])
            return
        if node in visited:
            return
        visiting.append(node)
        for child in graph.get(node, []):
            if child in graph:
                visit(child)
        visiting.pop()
        visited.add(node)

    for node in graph:
        visit(node)
    return found


def _validate_criteria(items: Any, owner: str, findings: list[dict[str, Any]]) -> None:
    if not isinstance(items, list):
        findings.append(finding("MANIFEST_TYPE", f"{owner} criteria must be an array"))
        return
    ids: list[str] = []
    for item in items:
        if not isinstance(item, dict):
            findings.append(finding("MANIFEST_TYPE", f"{owner} criterion must be an object"))
            continue
        criterion_id = item.get("id")
        if not isinstance(criterion_id, str) or not CRITERION_ID.fullmatch(criterion_id):
            findings.append(finding("MANIFEST_CRITERION_ID", f"Invalid criterion ID in {owner}: {criterion_id!r}"))
        else:
            ids.append(criterion_id)
        if item.get("state") not in CRITERION_STATES:
            findings.append(finding("MANIFEST_CRITERION_STATE", f"Invalid state for {criterion_id!r}"))
        if item.get("mandatory") not in {True, False}:
            findings.append(finding("MANIFEST_CRITERION_MANDATORY", f"Criterion {criterion_id!r} needs boolean mandatory"))
        if item.get("state") in {"DEFERRED", "NOT_APPLICABLE"} and not item.get("reason"):
            findings.append(finding("MANIFEST_CRITERION_REASON", f"Criterion {criterion_id!r} requires a reason"))
    for duplicate in _duplicates(ids):
        findings.append(finding("MANIFEST_DUPLICATE_CRITERION", f"Duplicate criterion ID: {duplicate}"))


def _scan_secret_values(value: Any, path: str, findings: list[dict[str, Any]]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            if key.lower() in FORBIDDEN_VALUE_KEYS and child not in (None, "", [], {}):
                findings.append(finding("MANIFEST_SECRET_VALUE", f"Manifest contains a prohibited value at {child_path}"))
            _scan_secret_values(child, child_path, findings)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_secret_values(child, f"{path}[{index}]", findings)


def validate(phase_data: Any, task_data: Any, root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    if not isinstance(phase_data, dict) or phase_data.get("schema_version") != "1.0.0":
        findings.append(finding("MANIFEST_PHASE_SCHEMA", "Phase manifest schema_version must be 1.0.0"))
    if not isinstance(task_data, dict) or task_data.get("schema_version") != "1.0.0":
        findings.append(finding("MANIFEST_TASK_SCHEMA", "Task manifest schema_version must be 1.0.0"))
    phases = phase_data.get("phases", []) if isinstance(phase_data, dict) else []
    tasks = task_data.get("tasks", []) if isinstance(task_data, dict) else []
    if not isinstance(phases, list) or not phases:
        findings.append(finding("MANIFEST_PHASES", "Phase manifest needs a non-empty phases array"))
        phases = []
    if not isinstance(tasks, list) or not tasks:
        findings.append(finding("MANIFEST_TASKS", "Task manifest needs a non-empty tasks array"))
        tasks = []

    phase_ids = [p.get("id") for p in phases if isinstance(p, dict) and isinstance(p.get("id"), str)]
    task_ids = [t.get("id") for t in tasks if isinstance(t, dict) and isinstance(t.get("id"), str)]
    for duplicate in _duplicates(phase_ids):
        findings.append(finding("MANIFEST_DUPLICATE_PHASE", f"Duplicate phase ID: {duplicate}"))
    for duplicate in _duplicates(task_ids):
        findings.append(finding("MANIFEST_DUPLICATE_TASK", f"Duplicate task ID: {duplicate}"))

    decisions_text = (root / "docs/07-project-management/DECISIONS_PENDING.md").read_text(encoding="utf-8")
    decision_ids = set(re.findall(r"\bDEC-[A-Z]+-[0-9]{3}\b", decisions_text))
    decision_statuses = {
        match.group(1): match.group(2)
        for match in re.finditer(
            r"^\| (DEC-[A-Z]+-[0-9]{3}) \|.*\| (OPEN|RECOMMENDED|AWAITING_APPROVAL|APPROVED|REJECTED|DEFERRED|SUPERSEDED|RESOLVED) \|",
            decisions_text,
            re.MULTILINE,
        )
    }
    adr_files = {path.name[:7] for path in (root / "docs/01-architecture/ARCHITECTURAL_DECISIONS").glob("ADR-[0-9][0-9][0-9]-*.md")}
    for schema_name in ("phase-manifest.schema.json", "task-manifest.schema.json"):
        schema_path = root / "orchestration/schemas" / schema_name
        try:
            schema_data = load_json(schema_path)
            if schema_data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                findings.append(finding("MANIFEST_SCHEMA_DRAFT", f"{schema_name} is not JSON Schema draft 2020-12"))
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            findings.append(finding("MANIFEST_SCHEMA_PARSE", f"Unable to parse {schema_name}: {exc}"))

    phase_graph: dict[str, list[str]] = {}
    task_graph: dict[str, list[str]] = {}
    for phase in phases:
        if not isinstance(phase, dict):
            findings.append(finding("MANIFEST_PHASE_TYPE", "Every phase must be an object"))
            continue
        phase_id = phase.get("id")
        missing = sorted(PHASE_REQUIRED - phase.keys())
        if missing:
            findings.append(finding("MANIFEST_PHASE_FIELDS", f"{phase_id!r} missing: {', '.join(missing)}"))
        if not isinstance(phase_id, str) or not PHASE_ID.fullmatch(phase_id):
            findings.append(finding("MANIFEST_PHASE_ID", f"Invalid phase ID: {phase_id!r}"))
            continue
        if phase.get("status") not in PHASE_STATUSES:
            findings.append(finding("MANIFEST_PHASE_STATUS", f"Invalid phase status for {phase_id}"))
        spec = phase.get("specification")
        spec_path = safe_repo_path(root, spec) if isinstance(spec, str) else None
        if spec_path is None or not spec_path.is_file():
            findings.append(finding("MANIFEST_SPEC_PATH", f"Phase {phase_id} specification does not resolve: {spec!r}"))
        dependencies = phase.get("dependencies", [])
        if not isinstance(dependencies, list):
            findings.append(finding("MANIFEST_DEPENDENCY_TYPE", f"Phase {phase_id} dependencies must be an array"))
            dependencies = []
        phase_graph[phase_id] = dependencies
        for dependency in dependencies:
            if dependency not in phase_ids:
                findings.append(finding("MANIFEST_PHASE_REFERENCE", f"Phase {phase_id} references missing dependency {dependency}"))
        for task_id in phase.get("tasks", []):
            if task_id not in task_ids:
                findings.append(finding("MANIFEST_TASK_REFERENCE", f"Phase {phase_id} references missing task {task_id}"))
        for decision_id in phase.get("required_decisions", []):
            if not isinstance(decision_id, str) or not DECISION_ID.fullmatch(decision_id) or decision_id not in decision_ids:
                findings.append(finding("MANIFEST_DECISION_REFERENCE", f"Phase {phase_id} has unresolved decision {decision_id!r}"))
            elif phase.get("status") in {"READY", "IN_PROGRESS", "IN_REVIEW", "APPROVED"} and decision_statuses.get(decision_id) != "APPROVED":
                findings.append(finding("MANIFEST_DECISION_GUARD", f"Active phase {phase_id} depends on unapproved decision {decision_id}"))
        for adr_id in phase.get("required_adrs", []):
            if not isinstance(adr_id, str) or not ADR_ID.fullmatch(adr_id) or adr_id not in adr_files:
                findings.append(finding("MANIFEST_ADR_REFERENCE", f"Phase {phase_id} has unresolved ADR {adr_id!r}"))
        authorized = phase.get("implementation_authorized")
        authorization = phase.get("authorization_reference")
        if authorized is not False and authorized is not True:
            findings.append(finding("MANIFEST_AUTHORIZATION_TYPE", f"Phase {phase_id} authorization must be boolean"))
        if authorized and not authorization:
            findings.append(finding("MANIFEST_AUTHORIZATION", f"Phase {phase_id} is authorized without a reference"))
        if phase.get("status") in {"READY", "IN_PROGRESS"} and not authorized:
            findings.append(finding("MANIFEST_STATUS_GUARD", f"Phase {phase_id} cannot be {phase.get('status')} without authorization"))
        approval_fields = {"role", "scope", "decision", "date", "evidence_reference"}
        for approval in phase.get("approvals", []):
            if not isinstance(approval, dict) or not approval_fields.issubset(approval) or not approval.get("evidence_reference"):
                findings.append(finding("MANIFEST_APPROVAL_FIELDS", f"Phase {phase_id} has an incomplete approval record"))
        if phase.get("exceptions"):
            findings.append(finding("MANIFEST_EXCEPTION_UNSUPPORTED", f"Phase {phase_id} exceptions fail closed until the exception validator is implemented"))
        _validate_criteria(phase.get("entry_criteria"), phase_id, findings)
        _validate_criteria(phase.get("exit_criteria"), phase_id, findings)
        phase_evidence = set(phase.get("evidence", []))
        for evidence_id in phase_evidence:
            evidence_path = root / "docs/02-phases" / f"{phase_id}_FOUNDATION" / "evidence" / f"{evidence_id}.json"
            if phase_id == "P00" and not evidence_path.is_file():
                findings.append(finding("MANIFEST_EVIDENCE_FILE", f"Declared evidence {evidence_id} does not resolve to {evidence_path.relative_to(root).as_posix()}"))
        for criterion in [*phase.get("entry_criteria", []), *phase.get("exit_criteria", [])]:
            if isinstance(criterion, dict):
                for evidence_id in criterion.get("evidence_refs", []):
                    if evidence_id not in phase_evidence:
                        findings.append(finding("MANIFEST_EVIDENCE_REFERENCE", f"Phase criterion {criterion.get('id')} references undeclared evidence {evidence_id}"))
        if phase.get("status") == "APPROVED" and any(
            criterion.get("mandatory") and criterion.get("state") != "VERIFIED"
            for criterion in phase.get("exit_criteria", []) if isinstance(criterion, dict)
        ):
            findings.append(finding("MANIFEST_EXIT_GUARD", f"Approved phase {phase_id} has unverified mandatory exit criteria"))

    for task in tasks:
        if not isinstance(task, dict):
            findings.append(finding("MANIFEST_TASK_TYPE", "Every task must be an object"))
            continue
        task_id = task.get("id")
        missing = sorted(TASK_REQUIRED - task.keys())
        if missing:
            findings.append(finding("MANIFEST_TASK_FIELDS", f"{task_id!r} missing: {', '.join(missing)}"))
        if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
            findings.append(finding("MANIFEST_TASK_ID", f"Invalid task ID: {task_id!r}"))
            continue
        phase_id = task.get("phase_id")
        if phase_id not in phase_ids or not task_id.startswith(f"{phase_id}-"):
            findings.append(finding("MANIFEST_TASK_PHASE", f"Task {task_id} has invalid phase {phase_id!r}"))
        if task.get("status") not in TASK_STATUSES:
            findings.append(finding("MANIFEST_TASK_STATUS", f"Invalid task status for {task_id}"))
        dependencies = task.get("dependencies", [])
        if not isinstance(dependencies, list):
            findings.append(finding("MANIFEST_DEPENDENCY_TYPE", f"Task {task_id} dependencies must be an array"))
            dependencies = []
        task_graph[task_id] = dependencies
        for dependency in dependencies:
            if dependency not in task_ids:
                findings.append(finding("MANIFEST_TASK_DEPENDENCY", f"Task {task_id} references missing task {dependency}"))
        for adr_id in task.get("adrs", []):
            if adr_id not in adr_files:
                findings.append(finding("MANIFEST_ADR_REFERENCE", f"Task {task_id} has unresolved ADR {adr_id!r}"))
        for decision_id in task.get("decisions", []):
            if decision_id not in decision_ids:
                findings.append(finding("MANIFEST_DECISION_REFERENCE", f"Task {task_id} has unresolved decision {decision_id!r}"))
            elif task.get("status") in {"READY", "IN_PROGRESS", "IN_REVIEW", "DONE"} and decision_statuses.get(decision_id) != "APPROVED":
                findings.append(finding("MANIFEST_DECISION_GUARD", f"Active task {task_id} depends on unapproved decision {decision_id}"))
        authorized = task.get("implementation_authorized")
        if authorized is not False and authorized is not True:
            findings.append(finding("MANIFEST_AUTHORIZATION_TYPE", f"Task {task_id} authorization must be boolean"))
        if authorized and not task.get("authorization_reference"):
            findings.append(finding("MANIFEST_AUTHORIZATION", f"Task {task_id} is authorized without a reference"))
        if task.get("status") in {"READY", "IN_PROGRESS", "IN_REVIEW", "DONE"} and not authorized:
            findings.append(finding("MANIFEST_STATUS_GUARD", f"Task {task_id} cannot be {task.get('status')} without authorization"))
        if task.get("exceptions"):
            findings.append(finding("MANIFEST_EXCEPTION_UNSUPPORTED", f"Task {task_id} exceptions fail closed until the exception validator is implemented"))
        commands = task.get("commands", [])
        if not isinstance(commands, list) or not commands:
            findings.append(finding("MANIFEST_COMMANDS", f"Task {task_id} needs at least one reproducible command"))
        else:
            command_fields = {"id", "purpose", "run_from", "command", "image_or_runtime", "network", "expected_exit", "produces"}
            for command in commands:
                if not isinstance(command, dict) or not command_fields.issubset(command):
                    findings.append(finding("MANIFEST_COMMAND_FIELDS", f"Task {task_id} has an incomplete command contract"))
        permissions = task.get("permissions")
        permission_fields = {"repository", "pull_requests", "actions", "id_token", "secrets", "database_role", "object_storage", "deployment_environment"}
        if not isinstance(permissions, dict) or not permission_fields.issubset(permissions):
            findings.append(finding("MANIFEST_PERMISSION_FIELDS", f"Task {task_id} has an incomplete permission contract"))
        elif not isinstance(permissions.get("secrets"), list):
            findings.append(finding("MANIFEST_PERMISSION_SECRETS", f"Task {task_id} secrets permission must be an array"))
        _validate_criteria(task.get("acceptance_criteria"), task_id, findings)
        task_evidence = {
            item.get("id") for item in task.get("evidence_requirements", []) if isinstance(item, dict)
        }
        for criterion in task.get("acceptance_criteria", []):
            if isinstance(criterion, dict):
                for evidence_id in criterion.get("evidence_refs", []):
                    if evidence_id not in task_evidence:
                        findings.append(finding("MANIFEST_EVIDENCE_REFERENCE", f"Task criterion {criterion.get('id')} references undeclared evidence {evidence_id}"))
        if task.get("status") == "DONE" and any(
            criterion.get("mandatory") and criterion.get("state") != "VERIFIED"
            for criterion in task.get("acceptance_criteria", []) if isinstance(criterion, dict)
        ):
            findings.append(finding("MANIFEST_DONE_GUARD", f"Done task {task_id} has unverified mandatory criteria"))

    for cycle in _cycles(phase_graph):
        findings.append(finding("MANIFEST_PHASE_CYCLE", "Phase dependency cycle: " + " -> ".join(cycle)))
    for cycle in _cycles(task_graph):
        findings.append(finding("MANIFEST_TASK_CYCLE", "Task dependency cycle: " + " -> ".join(cycle)))
    for task in tasks:
        if isinstance(task, dict) and task.get("id") not in {
            item for phase in phases if isinstance(phase, dict) for item in phase.get("tasks", [])
        }:
            findings.append(finding("MANIFEST_REVERSE_REFERENCE", f"Task {task.get('id')!r} is not referenced by its phase"))
    _scan_secret_values(phase_data, "phase_manifest", findings)
    _scan_secret_values(task_data, "task_manifest", findings)
    return findings, {"phase_count": len(phases), "task_count": len(tasks), "decision_count": len(decision_ids), "adr_count": len(adr_files)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--format", choices=["json"], default="json")
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repository_root()
    phase_path = safe_repo_path(root, args.phase)
    task_path = safe_repo_path(root, args.task)
    findings: list[dict[str, Any]] = []
    phase_data: Any = {}
    task_data: Any = {}
    for label, path in (("phase", phase_path), ("task", task_path)):
        try:
            data = load_json(path) if path and path.is_file() else None
            if data is None:
                raise FileNotFoundError(path)
            if label == "phase":
                phase_data = data
            else:
                task_data = data
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(finding("MANIFEST_PARSE", f"Unable to parse {label} manifest safely as JSON-compatible YAML: {exc}"))
    validation_findings, metrics = validate(phase_data, task_data, root)
    findings.extend(validation_findings)
    inputs = [path for path in (phase_path, task_path) if path and path.is_file()]
    evidence = evidence_envelope(
        gate_id="CI-GATE-001",
        command="python scripts/quality/validate_manifests.py",
        root=root,
        input_files=inputs,
        findings=findings,
        metrics=metrics,
    )
    return emit_and_exit(evidence, Path(args.output))


if __name__ == "__main__":
    sys.exit(main())
