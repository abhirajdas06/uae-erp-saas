# Initial CI Quality-Gate Specification

| Property | Value |
|---|---|
| Document ID | QUAL-CI-001 |
| Version | 1.2 |
| Status | APPROVED SPECIFICATION |
| Date | 28 October 2026 |
| Owner | QA / Security / DevOps / Architecture |
| Approval Scope | CI contract only; workflow implementation and production deployment remain unauthorized |

## 1. Purpose

This document defines the initial GitHub Actions quality-gate contract for P00 and the minimum extensible gate model for later phases. It specifies reproducible command interfaces, permissions, evidence, failure behavior, and controlled exceptions.

The P00 workflow and dependency-free quality scripts have local-equivalence evidence and successful hosted evidence from GitHub Actions run `40647091699`, artifact `12798425785`, as recorded by P00-EV-011. Application tests, containers and release pipelines do not yet exist. Protected-branch enforcement and later application gates remain separate work. A planned command becomes an enforced gate only after its implementation is reviewed and its first evidence is recorded.

## 2. Governing Controls

- [ADR-015 — Automated Testing and CI Quality Gates](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-015-automated-testing-and-ci-quality-gates.md)
- [ADR-016 — Docker-Based Deployment Architecture](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-016-docker-based-deployment-architecture.md)
- [ADR-017 — Secrets and Environment Configuration](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-017-secrets-and-environment-configuration.md)
- [ADR-018 — Audit Logging and Sensitive-Data Handling](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-018-audit-logging-and-sensitive-data-handling.md)
- [Security Requirements](SECURITY_REQUIREMENTS.md)
- [Testing Strategy](TESTING_STRATEGY.md)
- [P00 Manifest Schema](../02-phases/P00_FOUNDATION/P00_MANIFEST_SCHEMA.md)

## 3. Gate Principles

1. A required gate fails closed; missing, skipped, cancelled, or stale results do not pass.
2. Pull requests run with untrusted-code assumptions and no production secrets.
3. Required checks are reproducible from a clean checkout using the locked project toolchain.
4. PostgreSQL-dependent behavior is tested against a supported PostgreSQL service, not substituted with SQLite.
5. Results are bound to the exact commit SHA.
6. Critical security, tenant-isolation, financial-integrity, migration, and authorization failures are non-waivable for production release.
7. Deployment is a separate, protected workflow and is never an implicit consequence of a documentation or test gate.
8. An exception is a risk decision with expiry and evidence, not a passing test result.

## 4. Workflow and Trigger Model

| Workflow class | Trigger | Code trust | Secrets | Purpose |
|---|---|---|---|---|
| Pull-request validation | `pull_request` | Untrusted | None except platform-generated read token | Fast and required change validation |
| Main-branch validation | Push/merge to protected default branch | Reviewed | Test-only, narrowly scoped if unavoidable | Full deterministic integration suite and evidence |
| Scheduled assurance | Schedule plus manual dispatch | Default-branch code | Read-only scanner credentials only when approved | Dependency, secret, and deeper security checks |
| Release candidate | Signed/versioned candidate and manual approval | Protected ref | Release-scoped | Build, attest, migration rehearsal, release evidence |
| Deployment | Explicit protected-environment dispatch | Approved artifact | Environment-scoped | Future deployment only; outside P00 authorization |

`pull_request_target` MUST NOT execute pull-request code. Reusable workflows must pin a reviewed version and declare their permissions and inputs.

## 5. Initial Gate Catalogue

| Gate ID | Gate | P00 requirement | Failure behavior |
|---|---|---|---|
| CI-GATE-001 | Repository and manifest validation | Required once validator exists | Blocks merge |
| CI-GATE-002 | Markdown links and identifier integrity | Required | Blocks merge for internal failures |
| CI-GATE-003 | ADR/status/approval consistency | Required | Blocks merge. Includes the P01 authorization interlock: P01 may be `AWAITING_APPROVAL` or `AUTHORIZED`, and `AUTHORIZED` requires a recorded `APPR-P01-001` in the decision register, so a phase cannot be self-authorized by an agent or by an edit to the status table alone |
| CI-GATE-004 | Secret scanning | Required | Blocks merge; exposed secret triggers incident handling |
| CI-GATE-005 | Dependency and lock integrity | Required when dependency files exist | Blocks merge on unsupported/unlocked state |
| CI-GATE-006 | Python lint and format | Required when Python source exists | Blocks merge |
| CI-GATE-007 | Type/static analysis | Required by affected component policy | Blocks merge at configured severity |
| CI-GATE-008 | Unit/component tests | Required when implementation exists | Blocks merge |
| CI-GATE-009 | PostgreSQL integration and tenant-isolation tests | Required from P01 | Blocks merge; non-waivable for affected changes |
| CI-GATE-010 | Migration safety and clean-database rehearsal | Required for migration changes | Blocks merge/release |
| CI-GATE-011 | Container build and image inspection | Required when Docker assets exist | Blocks release |
| CI-GATE-012 | Contract/API/schema compatibility | Required for exposed contract changes | Blocks merge or requires approved breaking version |
| CI-GATE-013 | Security test suite and artifact review | Risk-triggered and release-required | Blocks release at policy threshold |
| CI-GATE-014 | Release evidence completeness | Release candidate only | Blocks release |

For the documentation-only P00 state, CI-GATE-001 through CI-GATE-004 are the initial implementation target. Gates for absent source, migrations, containers, and contracts report `NOT_APPLICABLE` with machine-verifiable applicability evidence; they are not silently skipped.

## 6. Reproducible Command Contract

### 6.1 Canonical entry points

The first four commands and the aggregate P00 command are implemented; later application, migration, and container commands remain specifications until their referenced files exist:

```text
python scripts/quality/validate_manifests.py --phase orchestration/phase-manifest.yml --task orchestration/task-manifest.yml --format json --output build/evidence/manifests.json
python scripts/quality/validate_docs.py --root docs --format json --output build/evidence/docs.json
python scripts/quality/validate_governance.py --root docs --format json --output build/evidence/governance.json
python scripts/quality/scan_secrets.py --baseline .secrets.baseline --format sarif --output build/evidence/secrets.sarif
python scripts/quality/run_p00_gates.py --output-dir build/evidence
python -m ruff format --check .
python -m ruff check --output-format=github .
python -m pytest -m "not integration" --junitxml=build/evidence/unit.xml
python -m pytest -m integration --junitxml=build/evidence/integration.xml
python -m pytest tests/security/tenant_isolation --junitxml=build/evidence/tenant-isolation.xml
python scripts/quality/check_migrations.py --output build/evidence/migrations.json
docker compose -f compose.test.yml build --pull
docker compose -f compose.test.yml run --rm test
```

Tool adoption still requires pinned dependencies and reviewed configuration. These command names do not add dependencies by themselves. If a selected tool changes, the public command contract should remain stable through project-owned wrappers where practical.

### 6.2 Reproducibility requirements

Each command MUST:

- Run from a clean checkout without developer-global packages.
- Use a pinned Python runtime and lock file or immutable test image.
- Be non-interactive and independent of wall-clock locale/timezone except explicit UTC fixtures.
- Declare required services, environment variables, and network access.
- Use synthetic, deterministic fixtures; never production data.
- Return `0` only for a passing result and a distinct non-zero code for validation/tooling failure where practical.
- Write structured evidence to `build/evidence/` and keep console output free of secrets.
- Support local execution and CI with equivalent semantics.
- Record tool and ruleset versions.

Network access is disabled after dependency acquisition for deterministic tests unless a test explicitly uses a controlled mock or approved sandbox. Tests do not call live e-invoicing, payment, payroll, banking, email, or government endpoints.

## 7. GitHub Actions Permission Baseline

Workflow permissions are set at workflow and job level. The default is:

```yaml
permissions:
  contents: read
```

Additional rules:

- `pull-requests: read` or `checks: write` is granted only to a job that demonstrably needs it.
- `id-token: write` is prohibited in validation workflows and limited to protected deployment/release jobs using an approved trust policy.
- `contents: write`, package publication, release creation, and deployments require separate protected jobs and approvals.
- Fork pull requests receive no repository or environment secrets.
- Production and shared staging credentials are never available to pull-request jobs.
- Third-party actions are pinned to immutable full commit SHAs and reviewed before update.
- Credentials use least scope, environment protection, short lifetime, and rotation.
- Self-hosted runners are not used for untrusted pull-request code unless ephemeral isolation and reset are independently approved.
- Workflow changes require CODEOWNERS-style review by DevOps/Security once repository controls are implemented.
- Concurrency cancellation may stop superseded validation runs but cannot rewrite their retained evidence.

## 8. Evidence Handling

### 8.1 Required evidence envelope

Every required job publishes a small machine-readable summary containing:

- Gate ID, result, commit SHA, workflow/run/job identifiers, and UTC timestamps.
- Command, tool/ruleset versions, runner/image identity, and applicable configuration digest.
- Test totals and pass/fail/skip/error counts.
- Artifact names, SHA-256 digests, sensitivity labels, and retention categories.
- Requirement, ADR, task, criterion, decision, and exception references.
- Applicability reason for `NOT_APPLICABLE`.

Preferred formats are JSON for summaries, JUnit XML for tests, SARIF for supported security/static findings, OpenAPI diff reports for API compatibility, and SPDX or CycloneDX for a future SBOM.

### 8.2 Protection and retention

- Evidence contains no secrets and minimizes personal, payroll, banking, financial, or provider payload data.
- Raw sensitive fixtures and request/response bodies are not uploaded as routine artifacts.
- Artifact access follows least privilege and is auditable where the platform supports it.
- Failed evidence is retained alongside successful reruns according to the approved evidence-retention category.
- Retention durations are selected before workflow implementation under DEC-DATA-002; no arbitrary legal period is asserted here.
- Security findings may use restricted artifacts; public annotations contain only remediation-safe detail.
- Evidence required for release is copied or referenced in a durable release record so ordinary CI expiry cannot erase the approval basis.
- The initial workflow inherits the repository's configured artifact-retention default; selecting an explicit duration remains part of DEC-DATA-002 and later repository governance.

## 9. Branch, Merge, and Release Rules

The protected default branch SHOULD require:

- Pull request review and resolved conversations.
- All applicable required gates on the current head SHA.
- Review of workflow, dependency, migration, security-control, and ADR changes by designated owners.
- No direct push except a separately governed emergency process.
- No force push or history deletion.
- Linear history or an explicitly selected merge policy with traceable commit identity.

Stale approvals are dismissed when relevant content changes. Administrative bypass is disabled or restricted to a logged emergency role. A bypass does not manufacture passing evidence and requires retrospective review.

Release gates additionally require immutable artifact identity, dependency/SBOM evidence when implemented, migration rehearsal, vulnerability disposition, rollback/recovery evidence, approval of active exceptions, and human release approval. Production deployment remains a separate authorization.

## 10. Exception and Flaky-Test Rules

### 10.1 Exception request

An exception MUST record the fields in P00-MANIFEST-001 plus:

- Exact required check and affected commit/release scope.
- Why remediation cannot occur before the deadline.
- Whether the exception permits merge, release, deployment, or only continued investigation.
- Reproduction and compensating-verification commands.

Security approves security-control exceptions; Architecture/Database approve data and migration exceptions; Finance approves financial-control exceptions; Product Owner approves residual product/release risk. The risk owner cannot be the sole approver of their own exception.

### 10.2 Non-waivable outcomes

No exception permits production release with:

- A demonstrated cross-tenant read/write/existence leak or RLS bypass.
- Broken authentication/authorization on an affected path.
- A live credential or signing key exposed in source, logs, images, or artifacts.
- A known exploitable critical vulnerability without verified containment and authorized incident handling.
- Unrehearsed destructive or irreversible migration behavior.
- Financial posting imbalance, unauthorized mutation, or correction-integrity failure.
- Missing mandatory human approval or fabricated/misattributed evidence.

### 10.3 Flaky tests

- A flaky test is a failed test until triaged; blind rerun-to-green is prohibited.
- Automatic reruns, if enabled, retain every attempt and identify the test as flaky.
- Quarantine requires an exception ID, owner, expiry, issue, compensating coverage, and exclusion from any safety-critical pass calculation.
- Tenant-isolation, authorization, financial-integrity, migration-safety, and secret-exposure tests cannot be quarantined for release.

## 11. Failure and Recovery Behavior

- Product failure blocks the affected merge/release.
- CI infrastructure failure results in `ERROR`, not `PASS`; retry is allowed with both attempts retained.
- A compromised runner/action/dependency invalidates affected evidence and triggers credential/artifact impact review.
- A cancelled superseded run is not acceptable evidence for its commit.
- Required provider outage tests use mocks/sandboxes; a third-party outage never justifies testing against production.
- Emergency fixes use the same non-waivable checks and require a time-bounded retrospective review.

## 12. P00 Implementation Sequence

1. Add pinned quality-tool dependencies and configurations through a bounded, authorized P00 task.
2. Implement manifest, documentation, and governance validators with unit tests.
3. Add an initial workflow with `contents: read`, timeouts, concurrency, and no secrets.
4. Run it on a clean branch and preserve structured evidence.
5. Review permissions, action SHAs, logs, artifacts, failure behavior, and exception handling.
6. Make approved checks required on the protected default branch.
7. Update P00-EV-010 and P00-EV-011; do not mark P00 approved until all exit evidence and Product Owner approval exist.

## 13. Acceptance Criteria

- [x] Every initial enforced gate has a stable ID, reproducible local command, owner, applicability rule, and failure behavior.
- [x] The workflow defaults to read-only permissions and has no pull-request secrets.
- [x] Actions and the Python runtime are immutably pinned.
- [x] Evidence binds results to commit, command, tool version, configuration/content digest, and dirty-tree state.
- [x] Missing or failed checks produce a non-zero result and cannot satisfy the local aggregate gate.
- [x] Manifest exceptions fail closed; future exception support must implement the approved scoped/expiring contract.
- [x] Tooling errors and timeouts fail the aggregate gate rather than becoming a pass.
- [x] Local and CI execution use the same `run_p00_gates.py` command.
- [x] The workflow contains no deployment job or production permission.
- [x] Hosted GitHub Actions execution recorded by P00-EV-011: run `40647091699`, artifact `12798425785`.
- [ ] Protected-branch enforcement and application-level gates remain pending their authorized implementation phases.

Local equivalence and workflow-review evidence is recorded in [P00-EV-011](../02-phases/P00_FOUNDATION/evidence/P00-EV-011.json).

## 14. Approval

**Current Status:** APPROVED SPECIFICATION

- **Approved By:** Product Owner — explicit instruction to review and approve documents matching the market-standard baseline
- **Approval Date:** 28 October 2026
- **Approval Notes:** This approves the CI quality-gate contract. Exact tool versions, workflow files, numeric coverage thresholds, runner selection, artifact retention durations, and branch configuration must be implemented and evidenced through separately authorized work. No deployment is approved.

## 15. Change Log

| Version | Date | Status | Description |
|---|---|---|---|
| 1.0 | 28 October 2026 | APPROVED SPECIFICATION | Initial reproducibility, permission, evidence, exception, failure, and release-gate contract. |
| 1.1 | 28 October 2026 | IMPLEMENTED LOCALLY | Initial read-only workflow and dependency-free gates implemented; hosted execution remains pending. |
| 1.2 | 29 October 2026 | HOSTED BASELINE VERIFIED | Reconciled successful hosted run `40647091699` and artifact `12798425785`; retained protected-branch and future application gates as pending. |
