# Testing Strategy — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | QUAL-TST-001 |
| Version | 1.0 |
| Status | APPROVED BASELINE |
| Date | 28 October 2026 |
| Owner | QA Lead / Architecture |
| Reviewers | QA, Security, Architecture, DevOps, Product, Finance, Domain Owners |
| Applies To | P00–P12 and every authorized implementation task |

## 1. Purpose

This strategy defines how the project will verify requirements, accepted ADRs, migrations, security controls, financial integrity, tenant isolation, integrations, and operational readiness. It implements [ADR-015](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-015-automated-testing-and-ci-quality-gates.md) and supports the acceptance criteria of ADR-001 through ADR-020.

Testing provides evidence, not proof of absence of defects or regulatory compliance. No check may be reported as passed unless it was executed successfully in the stated environment.

## 2. Principles

1. Test behavior and invariants, not framework implementation details alone.
2. Use the lowest-cost test that supplies trustworthy evidence, then add integration/end-to-end tests at critical seams.
3. Negative, duplicate, concurrent, timeout, rollback, and recovery scenarios are first-class.
4. PostgreSQL-specific behavior is tested on PostgreSQL, not inferred from SQLite.
5. Tenant isolation, authorization, financial integrity, secrets, and destructive migrations are non-waivable routine gates.
6. Tests are deterministic, isolated, reproducible, and safe to run outside production.
7. Coverage percentages are diagnostic; requirement and risk coverage determine acceptance.
8. Manual review supplements but does not replace repeatable automated evidence.

## 3. Test Classification

| Layer | Primary purpose | Typical scope |
|---|---|---|
| Static checks | Fast prevention and consistency | Formatting, linting, types, imports, docs, identifiers, schemas, secrets, dependencies |
| Unit | Pure rule correctness | Calculations, validators, policies, mappings, state decisions |
| Model/database | Relational integrity | Constraints, transactions, locks, RLS, migrations, query behavior |
| Application service | Business operation integrity | Authorization, transactions, lifecycle, idempotency, audit/outbox |
| Transport | Interface behavior | Forms, views, HTMX fragments, DRF endpoints, errors, OpenAPI |
| Integration | Component/provider seams | PostgreSQL, Redis/Celery, object storage, email, provider adapters |
| Contract | Compatibility | OpenAPI, webhooks, events, provider/file schemas |
| End-to-end | Critical user journey | Bounded browser/system paths under production-like configuration |
| Operational | Production readiness | Image, migration, backup/restore, monitoring, rollback, failover exercises |
| Security | Abuse resistance | Tenant escape, authz bypass, injection, replay, secrets, files, misconfiguration |
| Performance | Capacity and degradation | Critical latency, throughput, queues, reports, exports, database plans |

## 4. Environments and Fidelity

### 4.1 Local development

Fast tests MUST run with documented commands. Docker Compose MAY provide PostgreSQL, Redis, workers, and compatible test services. Local shortcuts cannot replace CI/release evidence.

### 4.2 Change-gate CI

Every proposed change runs deterministic formatting, linting, documentation/link/identifier checks, secret detection, affected static checks, fast tests, and the risk-selected PostgreSQL suite. Untrusted contributions have no deployment secrets.

### 4.3 Integration CI

Database, security, task, API, file, and integration changes run PostgreSQL-backed migrations and tests with production-relevant extensions and restricted roles where applicable. Redis/Celery, object storage emulation, and provider doubles use explicit versions.

### 4.4 Release candidate

Release candidates run the full applicable suite against the immutable candidate image and production-like configuration. Evidence includes migrations, startup checks, security/dependency/image scans, critical end-to-end flows, contract compatibility, and rollback/recovery prerequisites.

### 4.5 Controlled external environments

Provider sandboxes, certification systems, browser matrices, and recovery environments are isolated from production credentials and data. Tests record provider/version/environment and distinguish mocks from external evidence.

Production is not a general test environment. Approved smoke and synthetic checks MUST be non-destructive and tenant-safe.

## 5. Test Data

- Use factories/builders with explicit tenant and legal-entity ownership.
- Generate synthetic data; do not copy production data by default.
- Security fixtures include at least two tenants, multiple memberships/scopes, revoked access, and platform roles.
- Financial fixtures identify currency, precision, calculation-policy version, dates, and expected reconciliation totals.
- Provider/file fixtures are licensed or internally created, versioned, bounded, and free of live secrets.
- Random/property tests record seeds on failure.
- Time-dependent tests use controlled clocks and explicit time zones.
- Cleanup failures are visible; transaction rollbacks must not hide integrity defects.

## 6. Core Verification Requirements

### TST-001 — Requirement and evidence traceability

Every P0/P1 requirement and ADR acceptance criterion MUST map to an automated test or an explicitly owned manual/operational verification.

**Acceptance criteria:** Unique test IDs, evidence location, last result, environment, owner, and unresolved gap are recorded.

### TST-002 — Unit and rule testing

Pure calculations, validators, state decisions, permission predicates, entitlement policy, provider mappings, and serialization rules MUST have focused tests including boundary and invalid inputs.

**Acceptance criteria:** Tests are deterministic, do not require unnecessary infrastructure, and cover named business examples.

### TST-003 — PostgreSQL and model integrity

Constraints, indexes, transactions, concurrency, RLS, native UUID/NUMERIC behavior, and database error handling MUST be tested on the supported PostgreSQL version.

**Acceptance criteria:** Tests exercise constraints directly and do not rely solely on model validation.

### TST-004 — Tenant-isolation architecture suite

Every tenant-owned access path MUST have allowed and denied cases under [ADR-002](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-002-shared-postgresql-database-and-schema.md), [ADR-004](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-004-tenant-isolation-and-postgresql-rls.md), and [ADR-014](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-014-uuid-primary-keys-and-tenant-aware-references.md).

**Acceptance criteria:** The matrix covers ORM, services, raw SQL, views/APIs, tasks, reports, exports, caches, files, administration, missing context, pooled-connection reuse, object references, and restricted runtime roles.

### TST-005 — Authentication and session suite

Tests MUST cover login, logout, session rotation/expiry, credential change/recovery, enumeration resistance, throttling, MFA policy, CSRF, secure cookies, host/origin/proxy settings, and privileged access.

**Acceptance criteria:** Both successful and abuse paths are verified without exposing secrets in artifacts.

### TST-006 — Authorization and entitlement suite

Tests MUST independently cover membership, roles, object/organizational scope, protected fields, workflow state, separation of duties, support access, and module entitlement under ADR-005/006.

**Acceptance criteria:** Revoked, expired, disabled, conflicting, cross-tenant, direct-URL, bulk, and task scenarios deny safely.

### TST-007 — UI, HTMX, and accessibility suite

Server-rendered and HTMX flows MUST verify full-page/fragment behavior, CSRF, validation, authorization parity, safe escaping, focus/error behavior, and keyboard/accessibility expectations under [ADR-007](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-007-server-rendered-ui-with-htmx-and-tailwind.md).

**Acceptance criteria:** Critical workflows have browser tests; reusable components receive automated accessibility checks plus targeted manual review.

### TST-008 — API and external-contract suite

Approved APIs MUST conform to [ADR-008](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-008-selective-use-of-django-rest-framework.md) and [ADR-020](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-020-api-versioning-and-external-integration-contracts.md).

**Acceptance criteria:** OpenAPI validity/conformance, compatibility diffs, authentication, authorization, tenancy, pagination, filtering, errors, decimals, dates, identifiers, idempotency, rate limits, mass assignment, and unknown versions/fields are tested.

### TST-009 — Task and outbox reliability suite

Celery tasks and outbox consumers MUST be tested for at-least-once delivery under [ADR-009](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-009-celery-redis-and-background-task-execution.md) and [ADR-010](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-010-transactional-outbox-and-event-delivery.md).

**Acceptance criteria:** Duplicate, concurrent, late, reordered, malformed, retry-exhausted, worker-crash, broker-loss, and stuck-dispatch scenarios preserve authoritative state and are observable.

### TST-010 — Financial integrity suite

Financial tests MUST verify [ADR-011](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-011-financial-data-integrity-and-immutable-posted-entries.md) and [ADR-013](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-013-monetary-precision-currency-and-rounding.md).

**Acceptance criteria:** Tests cover lifecycle transitions, protected-field immutability, balance, precision/scale, currencies, rounding stages, residuals, reversals, credit/adjustment links, closed periods, idempotency, concurrency, rollback, and reconciliation totals.

Golden examples MUST be approved by finance/tax reviewers before they establish UAE-specific expected results.

### TST-011 — E-invoicing and provider suite

Tests MUST keep invoice state separate from provider transport/status under [ADR-012](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-012-uae-e-invoicing-provider-integration-boundary.md).

**Acceptance criteria:** Canonical snapshots, schema versions, provider mapping, webhook authenticity/replay, duplicate submission, timeout/unknown outcome, reconciliation, correction links, evidence retention, and sandbox/certification results are covered.

Mocks alone are insufficient for production approval. Test success does not establish regulatory compliance.

### TST-012 — File and export suite

Tests MUST verify [ADR-019](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-019-file-and-document-storage.md).

**Acceptance criteria:** Tests cover type/size validation, misleading names/MIME, path traversal, quarantine, scan outcomes, active content, authorization, expired signed URLs, cross-tenant parent references, immutable versions, cleanup, checksums, missing/orphan objects, export expiry, and recovery.

### TST-013 — Audit, logging, and sensitive-data suite

Tests MUST verify required audit triggers, transactional failure behavior, append restrictions, access, redaction, correlation, retention/legal hold, evidence export, and alerts under [ADR-018](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-018-audit-logging-and-sensitive-data-handling.md).

**Acceptance criteria:** Tests assert prohibited secrets and sensitive payloads are absent from logs and CI artifacts.

### TST-014 — Migration and backward-compatibility suite

Every migration MUST be reviewed for existing data, locking, reversibility/forward-fix, RLS/constraint behavior, mixed-version deployment, backfill, and rollback implications.

**Acceptance criteria:** Clean install and upgrade-path tests run; destructive or long-running operations have approved runbooks and reconciliation evidence.

### TST-015 — Deployment and configuration suite

The immutable image and process roles MUST be tested under [ADR-016](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-016-docker-based-deployment-architecture.md) and [ADR-017](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-017-secrets-and-environment-configuration.md).

**Acceptance criteria:** Image build, non-root runtime, startup validation, health/readiness, web/worker/scheduler commands, migration job, static assets, no embedded secrets, graceful shutdown, and configuration failure are tested.

### TST-016 — Security verification suite

Applicable requirements in [SECURITY_REQUIREMENTS.md](SECURITY_REQUIREMENTS.md) MUST have automated negative tests and/or independent manual verification.

**Acceptance criteria:** Secret, dependency, static, image, configuration, tenant escape, authorization bypass, injection, replay, file, and abuse tests run at the defined gate; findings are triaged rather than silently ignored.

### TST-017 — Performance and capacity suite

Critical workflows MUST have approved workload assumptions, response/throughput/queue targets, and representative data volumes before production acceptance.

**Acceptance criteria:** Tests capture database queries/plans, N+1 behavior, lock contention, reports/exports, worker backlog, resource use, and degradation limits. Results are compared with approved targets, not arbitrary industry numbers.

### TST-018 — Backup, restore, and operational exercise

Production readiness MUST include restoration and recovery exercises for database, objects, required configuration references, and audit evidence.

**Acceptance criteria:** Measured RPO/RTO, metadata/object reconciliation, tenant isolation, application usability, monitoring/alerting, and documented gaps are recorded. A backup job alone is not restore evidence.

## 7. CI and Release Gates

| Gate | Trigger | Required evidence |
|---|---|---|
| Documentation | Every documentation change | Links, identifiers, required sections, register consistency, diff review |
| Change | Every code/configuration change | Format/lint/types as applicable, unit/affected tests, secret scan, docs, migration check |
| Architecture/security | Tenancy, auth, finance, tasks, APIs, files, integrations | PostgreSQL suites, negative tests, threat/design review, contract/schema checks |
| Integration | Component boundary changes | Versioned services, migration, Celery/Redis/storage/provider-double tests |
| Release | Candidate image | Full applicable suite, image/dependency scans, migration/rollback evidence, critical E2E |
| Production | Explicit deployment approval | Release evidence, backup/restore status, monitoring, runbooks, unresolved-risk disposition |

Required failures block the gate. Tests cannot be deleted, weakened, skipped, or marked expected-failure merely to create a green result.

## 8. Defect, Flaky-Test, and Exception Governance

- Failures are reproducible records with environment, seed/data, logs, and ownership.
- A flaky test is a defect. Quarantine requires owner, issue, reason, compensating evidence, and expiry.
- Skips and expected failures are reported and reviewed; critical-control tests cannot be routinely quarantined.
- Security findings use the severity and exception process in `SECURITY_REQUIREMENTS.md`.
- An exception records scope, risk, compensating controls, approver, expiry, and follow-up evidence.
- Critical tenant-isolation, secret-exposure, financial-integrity, or destructive-migration failures are not eligible for ordinary waiver.

## 9. Coverage and Exit Criteria

The project does not use one repository-wide percentage as proof of quality. Coverage reports identify untested code, but exit decisions use:

- Requirement and ADR acceptance-criterion coverage.
- Risk and state-transition coverage.
- Changed-code and critical-domain coverage.
- Negative, concurrency, failure, and recovery evidence.
- Open defect severity and residual-risk disposition.
- Production-like environment and provider evidence.

A phase exits only when its mandatory tests pass, manual/operational evidence is complete, exceptions are authorized, and the phase approval is explicit.

## 10. Evidence Format

Each execution record includes:

- Commit/image revision and configuration profile.
- Test command, suite/version, environment, and dependency versions.
- Start/end time and result counts including skipped/expected failures.
- Artifact links, safe logs, and reports.
- Requirements/ADRs verified.
- Failures, defects, exceptions, and reviewer.

Artifacts MUST not contain production secrets or unnecessary personal, financial, payroll, banking, identity, or customer data.

## 11. ADR Acceptance-Criteria Map

| ADR group | Principal verification |
|---|---|
| ADR-001, ADR-003 | Import/dependency rules, ownership review, service-boundary tests |
| ADR-002, ADR-004, ADR-014 | TST-003, TST-004, migration and restricted-role tests |
| ADR-005, ADR-006 | TST-005, TST-006 |
| ADR-007, ADR-008, ADR-020 | TST-007, TST-008 |
| ADR-009, ADR-010 | TST-009 |
| ADR-011, ADR-013 | TST-010 |
| ADR-012 | TST-011 |
| ADR-015 | CI/release gates, evidence and exception governance |
| ADR-016, ADR-017 | TST-015 and release checks |
| ADR-018 | TST-013 |
| ADR-019 | TST-012 |

## 12. Tools and Initial Direction

- `pytest` and `pytest-django` for Python/Django tests.
- PostgreSQL for database and tenancy evidence.
- Django's test client and DRF test tools for server interfaces.
- Browser automation selected during implementation planning for critical E2E/accessibility flows.
- GitHub Actions as the approved initial CI service under ADR-015; commands remain vendor-independent.
- Security, dependency, secret, image, schema, and documentation tools selected through bounded implementation tasks.

Tool selection does not change the required outcomes and must not introduce unreviewed production data or credentials.

## 13. References

- [ADR-015 — Automated Testing and CI Quality Gates](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-015-automated-testing-and-ci-quality-gates.md)
- [Security Requirements](SECURITY_REQUIREMENTS.md)
- [OWASP ASVS 5.0.0](https://asvs.owasp.org/)
- [NIST SP 800-218 SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Django testing documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [pytest documentation](https://docs.pytest.org/)
- [pytest-django documentation](https://pytest-django.readthedocs.io/)
- [GitHub Actions security guidance](https://docs.github.com/en/actions/how-tos/secure-your-work)
- [OpenAPI Specification](https://spec.openapis.org/oas/)
- `docs/00-product/PRODUCT_REQUIREMENTS.md`

## 14. Approval

**Current Status:** APPROVED BASELINE

- **Recommended option:** Adopt the layered, risk-based strategy and mandatory CI/release gates defined here.
- **Approved By:** Product Owner — explicit market-standard review instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Exact tools, quantitative targets, coverage thresholds, browsers, runners, retention periods, and provider test environments remain bounded implementation or operational decisions.

## 15. Change Log

| Version | Date | Status | Description |
|---|---|---|---|
| 1.0 | 28 October 2026 | APPROVED BASELINE | Initial testing strategy linked to ADR controls and acceptance criteria; execution evidence remains required. |
