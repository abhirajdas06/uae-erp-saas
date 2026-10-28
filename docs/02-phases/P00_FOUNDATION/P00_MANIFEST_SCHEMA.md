# P00 Phase and Task Manifest Schema

| Property | Value |
|---|---|
| Document ID | P00-MANIFEST-001 |
| Version | 1.0 |
| Status | APPROVED SPECIFICATION |
| Date | 28 October 2026 |
| Owner | Project Governance / Architecture / QA / DevOps |
| Approval Scope | Manifest contract only; no implementation or phase-exit authorization |

## 1. Purpose

This document defines the canonical, machine-readable contract for phase and task manifests. It converts the roadmap's planning model into a validation contract without creating an orchestration engine or authorizing application implementation.

The implemented initial files are:

- `orchestration/phase-manifest.yml`
- `orchestration/task-manifest.yml`

The initial implementation uses the JSON-compatible subset of YAML and parses it with Python's standard-library JSON parser. This is valid YAML 1.2, rejects executable/custom YAML tags by construction, and keeps the P00 gate dependency-free. A future move to broader YAML syntax requires a pinned safe parser and a reviewed compatibility change.

The repository does not treat prose status claims as evidence. A manifest status is valid only when its required approvals, dependencies, acceptance criteria, and evidence references are present and independently verifiable.

## 2. Governing Sources

- [Development Roadmap](../../00-product/DEVELOPMENT_ROADMAP.md)
- [P00 Phase Specification](P00_PHASE_SPECIFICATION.md)
- [P00 Traceability Matrix](P00_TRACEABILITY_MATRIX.md)
- [Testing Strategy](../../05-quality/TESTING_STRATEGY.md)
- [CI Quality-Gate Specification](../../05-quality/CI_QUALITY_GATES.md)
- [ADR-015](../../01-architecture/ARCHITECTURAL_DECISIONS/ADR-015-automated-testing-and-ci-quality-gates.md)
- [ADR-017](../../01-architecture/ARCHITECTURAL_DECISIONS/ADR-017-secrets-and-environment-configuration.md)
- [Pending Decisions](../../07-project-management/DECISIONS_PENDING.md)

## 3. Identifier and Version Rules

1. Canonical phase identifiers are `P00` through `P12`.
2. Historical labels such as `P0` or `P0-FOUNDATION` may appear as aliases but MUST NOT be used as primary keys.
3. Task identifiers use `<phase>-T-NNN`, for example `P00-T-001`.
4. Acceptance criteria use `<phase>-AC-NNN`; evidence uses `<phase>-EV-NNN`.
5. Exception identifiers use `EXC-YYYY-NNN` and decision identifiers use the canonical decision register.
6. Identifiers are immutable and never reused after cancellation.
7. `schema_version` follows semantic versioning. A breaking field or meaning change increments the major version.

## 4. Phase Manifest Contract

The root document is an object with `schema_version`, `generated_at`, and `phases`.

| Field | Type | Required | Validation rule |
|---|---|---:|---|
| `schema_version` | string | Yes | Exact supported manifest schema version, initially `1.0.0` |
| `generated_at` | timestamp | Yes | UTC RFC 3339 value; informational, not approval evidence |
| `phases` | array | Yes | At least one phase; unique `id` values |

Each phase object uses the following contract:

| Field | Type | Required | Validation rule |
|---|---|---:|---|
| `id` | string | Yes | `^P[0-1][0-9]$` plus numeric range validation from 00 through 12 |
| `title` | string | Yes | Matches the current phase register |
| `aliases` | string array | No | Unique; cannot equal another canonical phase ID |
| `status` | enum | Yes | One phase status from Section 6 |
| `specification` | repository path | Yes | Existing Markdown file inside the repository |
| `owner_roles` | string array | Yes | At least one accountable role; no personal secrets or emails |
| `dependencies` | phase-ID array | Yes | Existing IDs only; no self-reference or cycles |
| `entry_criteria` | criteria array | Yes | Stable ID, statement, required evidence, state |
| `exit_criteria` | criteria array | Yes | Stable ID, statement, required evidence, state |
| `required_decisions` | decision-ID array | Yes | Every referenced ID resolves in the decision register |
| `required_adrs` | ADR-ID array | Yes | Every ADR resolves and has an allowed status |
| `tasks` | task-ID array | Yes | Every ID resolves in the task manifest and points back to this phase |
| `evidence` | evidence-reference array | Yes | Content-addressed or immutable run/file references |
| `approvals` | approval array | Yes | Role, scope, decision, date, and evidence reference |
| `implementation_authorized` | boolean | Yes | False unless a separate explicit human authorization exists |
| `authorization_reference` | string/null | Yes | Required when `implementation_authorized` is true |
| `exceptions` | exception-ID array | Yes | Active exceptions applicable to this phase |
| `updated_at` | timestamp | Yes | UTC RFC 3339 |

### 4.1 Criterion object

Every entry or exit criterion contains:

```yaml
- id: P00-AC-001
  statement: "The approved architecture baseline is internally consistent."
  state: NOT_STARTED
  mandatory: true
  verification: DOCUMENT_REVIEW
  evidence_refs: []
  owner_roles: [Architecture]
```

Allowed criterion states are `NOT_STARTED`, `PARTIAL`, `VERIFIED`, `FAILED`, `DEFERRED`, and `NOT_APPLICABLE`. `DEFERRED` and `NOT_APPLICABLE` require a reason, approver, and destination or applicability evidence.

## 5. Task Manifest Contract

The root document is an object with `schema_version`, `generated_at`, and `tasks`. Each task object contains:

| Field | Type | Required | Validation rule |
|---|---|---:|---|
| `id` | string | Yes | `^P[0-1][0-9]-T-[0-9]{3}$` plus phase range validation from 00 through 12 |
| `phase_id` | phase ID | Yes | Existing phase; reverse reference is required |
| `title` | string | Yes | Concise outcome, not an activity-only label |
| `objective` | string | Yes | Testable outcome |
| `status` | enum | Yes | One task status from Section 6 |
| `scope.included` | string array | Yes | Explicit bounded work |
| `scope.excluded` | string array | Yes | Material non-goals |
| `owner_role` | string | Yes | Accountable role |
| `reviewer_roles` | string array | Yes | Risk-appropriate independent reviewers |
| `dependencies` | task-ID array | Yes | Existing IDs; no cycles |
| `requirements` | requirement-ID array | Yes | Resolvable product/phase/control identifiers |
| `adrs` | ADR-ID array | Yes | Applicable accepted decisions |
| `risks` | risk-ID array | Yes | Resolvable risk register entries |
| `decisions` | decision-ID array | Yes | Blocking and non-blocking decision references |
| `acceptance_criteria` | criteria array | Yes | Stable IDs with verification method |
| `commands` | command array | Yes | Reproducible commands or explicit documentation-only declaration |
| `permissions` | permission object | Yes | Minimum source, workflow, secret, database, and deployment access |
| `evidence_requirements` | evidence array | Yes | Required format, producer, retention class, and sensitivity |
| `rollback_or_recovery` | string | Yes | Recovery action or justified `NOT_APPLICABLE` |
| `implementation_authorized` | boolean | Yes | Cannot be inferred from specification approval |
| `authorization_reference` | string/null | Yes | Required when implementation is authorized |
| `exceptions` | exception-ID array | Yes | Active, unexpired exceptions only |
| `updated_at` | timestamp | Yes | UTC RFC 3339 |

### 5.1 Command object

```yaml
- id: CMD-001
  purpose: "Validate documentation links and identifiers"
  run_from: "."
  command: "python scripts/quality/validate_docs.py --root docs --format json --output build/evidence/docs.json"
  image_or_runtime: "project-toolchain-lock"
  network: "disabled"
  expected_exit: 0
  produces: ["build/evidence/docs.json"]
```

Commands MUST be non-interactive, pin or inherit a locked runtime, declare their working directory, avoid hidden local state, return non-zero on failure, and produce deterministic evidence where practical. A command is not marked executable until its referenced script/configuration exists.

### 5.2 Permissions object

The object declares least privilege rather than a person:

```yaml
permissions:
  repository: read
  pull_requests: read
  actions: none
  id_token: none
  secrets: []
  database_role: none
  object_storage: none
  deployment_environment: none
```

Any write, secret, OIDC, database, storage, or deployment permission requires a specific purpose and reviewer. Wildcard secret access is prohibited.

## 6. Status and Transition Rules

### 6.1 Phase statuses

`PLANNED`, `SPECIFICATION_IN_PROGRESS`, `AWAITING_APPROVAL`, `READY`, `IN_PROGRESS`, `BLOCKED`, `IN_REVIEW`, `REJECTED`, `AWAITING_HUMAN_APPROVAL`, `APPROVED`, `DEFERRED`, `CANCELLED`.

Key guards:

- `READY` requires approved scope, satisfied entry criteria, resolved blocking decisions, an approved test/evidence plan, and separate implementation authorization.
- `IN_PROGRESS` requires `implementation_authorized: true` and an authorization reference.
- `IN_REVIEW` requires all mandatory implementation tasks to be `DONE` or have valid exceptions.
- `APPROVED` requires verified exit evidence and a recorded human exit approval. Task completion alone is insufficient.
- `BLOCKED` requires at least one resolvable blocker reference.
- `DEFERRED` and `CANCELLED` require rationale, approver, and impact assessment.

### 6.2 Task statuses

`TODO`, `READY`, `IN_PROGRESS`, `BLOCKED`, `IN_REVIEW`, `FAILED`, `DONE`, `CANCELLED`.

`DONE` requires every mandatory acceptance criterion to be verified, required commands to pass, evidence to be recorded, reviewers to complete their checks, and no expired exception to be relied upon.

## 7. Evidence Contract

Every evidence reference MUST contain:

- Stable evidence ID and evidence type.
- Producing command or manual-review procedure.
- Repository commit SHA and, where applicable, CI run/job ID.
- UTC creation time and producer identity/role.
- Result: `PASS`, `FAIL`, `PARTIAL`, or `NOT_APPLICABLE`.
- Immutable artifact path or URL plus SHA-256 digest where supported.
- Format and tool/schema version.
- Sensitivity classification and retention category.
- Related requirement, criterion, task, exception, and approval IDs.
- Expiry or revalidation trigger when evidence can become stale.

Evidence MUST NOT contain credentials, unrestricted customer data, live payroll/banking data, or full sensitive provider payloads. Failed evidence is retained according to the approved evidence policy; reruns do not erase earlier failures.

## 8. Exception Contract

An exception record requires:

- ID, affected gate/control/command, scope, and precise reason.
- Risk statement and severity.
- Compensating controls and verification evidence.
- Requester, risk owner, required approvers, approval date, and immutable approval reference.
- Start date, expiry date, and remediation owner/date.
- Whether release is permitted and which environments are excluded.

Exceptions cannot waive tenant-isolation failures, authorization bypass, exposed credentials, destructive migration safety, known critical exploitable vulnerabilities, financial-integrity violations, missing required human approval, or false regulatory evidence. Expired exceptions fail closed.

## 9. Initial P00 Example

```yaml
schema_version: 1.0.0
generated_at: "2026-10-28T00:00:00Z"
phases:
  - id: P00
    title: Foundation and Architecture
    aliases: [P0, P0-FOUNDATION]
    status: SPECIFICATION_IN_PROGRESS
    specification: docs/02-phases/P00_FOUNDATION/P00_PHASE_SPECIFICATION.md
    owner_roles: [Product, Architecture, Security, QA, DevOps]
    dependencies: []
    entry_criteria: []
    exit_criteria:
      - id: P00-AC-001
        statement: "The approved architecture baseline is internally consistent."
        state: PARTIAL
        mandatory: true
        verification: DOCUMENT_REVIEW
        evidence_refs: []
        owner_roles: [Architecture]
    required_decisions: [DEC-GOV-002, DEC-QA-002, DEC-QA-003]
    required_adrs: [ADR-001, ADR-002, ADR-015, ADR-017]
    tasks: []
    evidence: []
    approvals: []
    implementation_authorized: false
    authorization_reference: null
    exceptions: []
    updated_at: "2026-10-28T00:00:00Z"
```

## 10. Schema Validation Acceptance Criteria

- [x] JSON-compatible YAML parses safely without custom object constructors.
- [x] Schema version is supported and explicit.
- [x] IDs, paths, reverse references, and status values are valid.
- [x] Dependency graphs are acyclic.
- [x] Blocking decisions prevent active task/phase states as applicable.
- [x] Current status guards are enforced.
- [x] Evidence declarations and approval records are validated.
- [x] Exceptions fail closed until the full exception-record validator is implemented.
- [x] `implementation_authorized` cannot become true without a separate reference.
- [x] Secret-value keys are prohibited in manifests.
- [x] Validation produces machine-readable output and a non-zero exit on failure.

Implementation evidence is recorded in [P00-EV-010](evidence/P00-EV-010.json).

## 11. Approval

**Current Status:** APPROVED SPECIFICATION

- **Approved By:** Product Owner — explicit instruction to review and approve documents matching the market-standard baseline
- **Approval Date:** 28 October 2026
- **Approval Notes:** This approves the schema contract and zero-padded phase identifiers. It does not assert that manifest files, validators, or CI execution evidence exist, does not approve P00 exit, and does not authorize P01 implementation.

## 12. Change Log

| Version | Date | Status | Description |
|---|---|---|---|
| 1.0 | 28 October 2026 | APPROVED SPECIFICATION | Initial phase/task manifest, evidence, permission, transition, and exception contract. |
| 1.1 | 28 October 2026 | IMPLEMENTED | Recorded the dependency-free JSON-compatible YAML implementation and validator evidence. |
