# ADR-015: Automated Testing and CI Quality Gates

| Field | Details |
|---|---|
| ADR ID | ADR-015 |
| Title | Automated Testing and CI Quality Gates |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 28 October 2026 |
| Decision Owner | Technical Lead / Quality Lead |
| Reviewers | Architecture, Security, Development, QA, DevOps, Product |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-001–ADR-014, ADR-016, ADR-017, ADR-018, ADR-020 |
| Related Requirements | PRD-003–PRD-004, OPS-001–OPS-004, NFR-001–NFR-009, DEP-001–DEP-003 |
| Related Documents | `AGENTS.md`, `PRODUCT_REQUIREMENTS.md`, `DEVELOPMENT_ROADMAP.md`, `SYSTEM_ARCHITECTURE.md`, `API_STANDARDS.md`, `EVENT_AND_TASK_PROCESSING.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The platform combines tenant isolation, permissions, subscriptions, accounting, tax, payroll, integrations, background processing, and deployment operations. A small happy-path test suite cannot establish that these boundaries are safe. Manual agent reports are also insufficient evidence unless the checks were actually executed and their results retained.

The repository identifies pytest, pytest-django, PostgreSQL, and GitHub Actions as the intended baseline. The project still needs a decision defining required test layers, risk-based CI gates, evidence, failure handling, and exceptions.

## 2. Decision Drivers

- Detect tenant-isolation, authorization, financial, migration, and integration regressions before merge.
- Use production-relevant PostgreSQL behavior for database-specific controls.
- Keep feedback fast enough for routine development while retaining deep release checks.
- Produce truthful, reproducible verification evidence.
- Prevent flaky, skipped, or disabled checks from silently becoming acceptance.
- Link requirements and risks to tests and release gates.
- Protect CI secrets, artifacts, and test data.

## 3. Options Considered

### Option A: Layered automated testing with risk-based mandatory CI gates

Run fast checks on every change, PostgreSQL-backed integration and security checks for affected areas, and broader release/recovery checks at defined gates.

**Advantages:** balanced feedback, strong critical-boundary coverage, and traceable evidence.

**Disadvantages:** CI design, test data, maintenance, and execution cost.

### Option B: Unit tests only for pull requests

**Advantages:** fast and simple.

**Disadvantages:** misses RLS, migrations, constraints, task delivery, integration, and deployment behavior.

### Option C: Primarily manual acceptance testing

**Advantages:** flexible exploratory coverage.

**Disadvantages:** weak repeatability, slow regression detection, and insufficient security evidence.

### Option D: Run every test for every change

**Advantages:** maximum uniformity.

**Disadvantages:** excessive latency and resource use as the ERP grows; encourages bypassing slow gates.

## 4. Decision

Adopt layered automated testing with risk-based mandatory CI gates. GitHub Actions is the proposed initial CI service, subject to repository and hosting approval. The test commands and evidence format must remain runnable outside GitHub Actions so the project is not dependent on one CI vendor.

No change may be reported as verified unless its required checks were executed successfully or a documented, authorized exception records the missing evidence and risk.

### 4.1 Test layers

The strategy includes:

- Unit tests for pure business rules and calculations.
- Model and database tests for constraints and lifecycle rules.
- Application-service tests for transactions, authorization, concurrency, and state changes.
- View, HTMX, and API contract tests.
- Tenant-isolation and permission denial tests.
- Entitlement and dependency tests.
- Financial calculation, posting, reversal, and reconciliation tests.
- Task, outbox, retry, duplicate-delivery, and recovery tests.
- Provider adapter and webhook contract tests using approved test doubles or sandboxes.
- Migration and deployment compatibility tests.
- Security, dependency, secret, and static-analysis checks.
- Focused end-to-end, accessibility, performance, backup/restore, and operational exercises.

Not every layer runs on every change, but every critical requirement must have an identified verification layer and gate.

### 4.2 CI gate classes

| Gate | When | Minimum purpose |
|---|---|---|
| Change gate | Every proposed change | Formatting, linting, fast tests, documentation/identifier validation, secret detection, and affected static checks |
| Integration gate | Changes affecting database, security, tasks, APIs, or integrations | PostgreSQL tests, migrations, tenant isolation, authorization, task/integration behavior |
| Main-branch gate | Merge or protected-branch update | Required suite, image build, migration checks, contract/schema validation, and artifacts |
| Release-candidate gate | Before an approved release | Full applicable regression, security, deployment, performance, recovery, and manual review evidence |
| Production gate | Before production deployment | Approved release record, backup/recovery readiness, migration plan, smoke checks, and explicit authorization |

The exact workflow files and branch rules will be created only during an authorized implementation task.

### 4.3 PostgreSQL fidelity

Tests for RLS, constraints, transactions, locks, indexes, migrations, and PostgreSQL-specific SQL must run against a supported PostgreSQL version using a production-equivalent restricted runtime role where relevant. SQLite is not acceptable evidence for those behaviors.

### 4.4 Critical negative testing

Every critical access or integrity control requires denied and failure cases, including:

- Cross-tenant read, write, reference, cache, export, task, and file access.
- Missing, revoked, or out-of-scope membership and permissions.
- Disabled entitlements and invalid dependencies.
- Duplicate, concurrent, stale, and out-of-order operations.
- Closed periods, unbalanced posting, and immutable records.
- Provider timeout, rejection, duplicate callback, and uncertain outcome.
- Missing secrets, unsafe roles, invalid configuration, and migration failure.

### 4.5 Test determinism and isolation

Tests must control time, random values, external calls, locale, and timezone where those affect outcomes. Each test must isolate database, cache, file, broker, and external state. Parallel execution must not create shared tenant context or ordering dependencies.

Flaky tests are defects. A flaky test may be quarantined only with an owner, issue, risk assessment, expiry date, and replacement gate where the control is critical.

### 4.6 Test data

Use synthetic data or explicitly approved sanitized fixtures. Production credentials, tokens, payment data, payroll records, identity documents, and customer files are prohibited in source control and ordinary CI.

Generated artifacts and logs must apply the same sensitive-data controls as the application.

### 4.7 Coverage and mutation evidence

Coverage percentages are diagnostic, not proof of correctness. The project may adopt minimum thresholds after a representative baseline exists, but critical requirements need explicit scenario coverage regardless of aggregate percentage.

Mutation testing or equivalent stronger techniques may be introduced for high-risk calculations and policy code when cost-effective.

### 4.8 Migration and deployment tests

Schema changes require forward migration tests, data validation, deployment-overlap analysis, and rollback or forward-recovery evidence. Destructive and long-running migrations require dedicated review against representative data volume.

Container images and static assets must build reproducibly. A successful unit test job does not establish deployability.

### 4.9 CI security

CI jobs use least-privilege identities and scoped secrets. Untrusted code must not receive production credentials or deployment authority. Fork and pull-request workflows require safe secret behavior. Actions and build dependencies must be pinned or otherwise controlled through the approved supply-chain policy.

### 4.10 Evidence and traceability

CI must retain, for an approved duration:

- Commit or source revision.
- Environment and dependency versions.
- Commands and selected test scope.
- Pass, fail, skip, and xfail counts.
- Relevant logs with redaction.
- Coverage and schema reports where configured.
- Image or artifact digests.
- Required review and exception records.

Requirements traceability links critical requirement IDs to tests and acceptance evidence.

### 4.11 Gate failures and exceptions

Required failures block merge or release. Tests must not be deleted, skipped, weakened, or marked expected-failure merely to obtain a green pipeline.

An exception requires an authorized approver, reason, risk, compensating evidence, scope, expiry, and tracking issue. Critical tenant-isolation, credential-exposure, financial-integrity, or destructive-migration failures are not eligible for routine waiver.

## 5. Rationale

Layered gates give rapid routine feedback while preserving deeper evidence for high-risk changes and releases. Production-equivalent PostgreSQL and negative tests address the platform's most consequential failure modes. Vendor-independent commands make CI replaceable and support local reproduction.

## 6. Consequences

### Positive consequences

- Earlier detection of security and integrity regressions.
- Reproducible, evidence-based task and release status.
- Clearer requirement-to-test traceability.
- Safer migrations and dependency updates.

### Negative consequences and trade-offs

- CI infrastructure and test maintenance require ongoing effort.
- PostgreSQL, browser, integration, and recovery tests add execution time.
- Some provider and operational tests require controlled external environments.
- Flaky-test governance creates short-term delivery friction.

### Risks and mitigations

- **Slow pipelines:** test selection, parallelism, caching, and separate release gates without weakening critical checks.
- **False green results:** production-relevant roles/configuration and evidence review.
- **Secret exposure:** scoped CI identities, redaction, and untrusted-workflow isolation.
- **Coverage gaming:** scenario traceability and risk-based review.
- **Skipped tests accumulating:** explicit reporting, owners, and expiry.

## 7. Security and Tenant-Isolation Implications

- Tenant-isolation and authorization tests are mandatory architecture tests.
- Security controls require negative tests, not only successful paths.
- CI artifacts and logs must not leak secrets or sensitive fixtures.
- Deployment credentials must be unavailable to ordinary test jobs.
- Security-scan findings require severity, ownership, and resolution or explicit human acceptance.

## 8. Data Integrity and Migration

- Database tests use PostgreSQL for PostgreSQL behavior.
- Migration tests verify constraints, RLS, backfills, locking assumptions, and historical integrity.
- Financial migrations include reconciliation totals and exception reporting.
- Test cleanup must not hide transaction or constraint failures.

## 9. Operational Impact

CI reliability, queue time, duration, flaky rate, artifact retention, and runner security must be monitored. Build and test outages have documented fallback rules; they do not authorize unverified production release.

## 10. Implementation Requirements

1. Create `docs/05-quality/TESTING_STRATEGY.md` and security/release standards before implementation authorization.
2. Define reproducible local commands for every CI job.
3. Establish protected branches and required checks when Git governance is available.
4. Provide PostgreSQL-backed test infrastructure and restricted-role RLS tests.
5. Create requirement/test/evidence traceability.
6. Add secret, dependency, migration, schema, and documentation checks.
7. Define release and production evidence packages.
8. Define exception, flaky-test, and artifact-retention policies.

## 11. Validation and Acceptance Criteria

- [ ] Required checks cannot be bypassed by ordinary contributors.
- [ ] CI commands reproduce locally or in the documented container environment.
- [ ] PostgreSQL-specific tests run against PostgreSQL.
- [ ] Critical controls have allowed, denied, duplicate, concurrent, and failure tests as applicable.
- [ ] Failed and skipped tests are visible in evidence.
- [ ] Untrusted workflows cannot access deployment or production secrets.
- [ ] Migration and image-build checks run before release.
- [ ] Critical requirements link to automated or explicitly manual evidence.
- [ ] Exceptions are authorized, expiring, and auditable.
- [ ] Production deployment requires a separate explicit gate.

## 12. Alternatives Rejected

- Unit tests alone are rejected as insufficient.
- Aggregate coverage alone is rejected as an acceptance criterion.
- SQLite-only database evidence is rejected for PostgreSQL controls.
- Manual-only regression testing is rejected.
- Automatically deploying every green commit to production is rejected.

## 13. References

- `AGENTS.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- pytest documentation: https://docs.pytest.org/
- pytest-django documentation: https://pytest-django.readthedocs.io/
- GitHub Actions documentation: https://docs.github.com/actions
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Layered automated testing with risk-based mandatory CI gates and GitHub Actions as the initial CI service.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; exact tools, thresholds, runner topology, artifact retention, and branch rules remain implementation decisions.

Exact coverage thresholds, runner topology, retention periods, scanning tools, and branch rules remain implementation decisions. CI implementation still requires a bounded authorized task.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial automated testing and CI quality-gate decision accepted after standards review. |
