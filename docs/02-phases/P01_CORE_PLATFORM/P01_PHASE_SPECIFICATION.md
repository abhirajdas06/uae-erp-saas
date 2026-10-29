# P01 — Core Platform and Multi-Tenancy Phase Specification

| Property | Value |
|---|---|
| Phase ID | P01 |
| Legacy roadmap alias | P1 / `P1-CORE-PLATFORM` |
| Document ID | P01-SPEC-001 |
| Version | 1.0 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Date | 28 October 2026 |
| Phase Owner | Product Owner |
| Technical Owners | Architecture / Security / Core Platform |
| Required Reviewers | Product, Architecture, Security, QA, Database, DevOps |
| Current Authorization | Specification only |
| Implementation Authorization | Not granted |
| Depends On | Approved P00 exit and explicit P01 start authorization |

## 1. Purpose

P01 defines the smallest implementation increment that can establish a secure Django/PostgreSQL foundation for later ERP modules. It covers platform bootstrap, tenant identity, membership, authentication, scoped authorization, trusted tenant context, tenant-aware integrity, a reviewed PostgreSQL RLS pilot, audit/logging foundations, health checks, migrations, local container support, and CI verification.

This document specifies future implementation work but does not authorize it. No P01 task may begin until the P00 exit gate and separate P01 start authorization are recorded.

The canonical phase traceability is [P01_TRACEABILITY_AND_TEST_MATRIX.md](P01_TRACEABILITY_AND_TEST_MATRIX.md); its mandatory detailed tenant-isolation plan is [P01_TENANT_ISOLATION_TEST_MATRIX.md](P01_TENANT_ISOLATION_TEST_MATRIX.md).

## 2. Governing Sources

- [Repository Instructions](../../../AGENTS.md).
- [Product Requirements](../../00-product/PRODUCT_REQUIREMENTS.md), especially TEN-001–TEN-005, IAM-001–IAM-005, AUD-001, OPS-001, NFR-001–NFR-003, NFR-006, NFR-008, NFR-009, DEP-001, and DEP-002.
- [Development Roadmap](../../00-product/DEVELOPMENT_ROADMAP.md), Phase 1.
- [System Architecture](../../01-architecture/SYSTEM_ARCHITECTURE.md).
- [Django Application Structure](../../01-architecture/DJANGO_APP_STRUCTURE.md).
- [Database Design](../../01-architecture/DATABASE_DESIGN.md).
- [Multi-Tenancy](../../01-architecture/MULTI_TENANCY.md).
- [Authentication and Permissions](../../01-architecture/AUTHENTICATION_AND_PERMISSIONS.md).
- Accepted ADR-001 through ADR-005, ADR-014 through ADR-018; ADR-006, ADR-007, ADR-008, and ADR-009 apply at defined seams.
- [Security Requirements](../../05-quality/SECURITY_REQUIREMENTS.md), approved baseline.
- [Testing Strategy](../../05-quality/TESTING_STRATEGY.md), approved baseline.
- [P00 Specification](../P00_FOUNDATION/P00_PHASE_SPECIFICATION.md) and [P00 Traceability](../P00_FOUNDATION/P00_TRACEABILITY_MATRIX.md).

Accepted ADRs override conflicting draft architecture prose. Before implementation, the quality baselines and this phase specification must be explicitly approved.

## 3. Objective

Deliver and independently verify a minimal platform foundation that:

1. Starts reproducibly in an approved development/test environment.
2. Uses PostgreSQL as the authoritative database.
3. Establishes stable user and tenant identities.
4. Prevents one tenant from reading, creating, changing, deleting, referencing, exporting, or administratively accessing another tenant's data.
5. Enforces authentication, membership, permissions, object scope, and platform-administration separation server-side.
6. Provides trustworthy audit and diagnostic foundations without leaking secrets or sensitive data.
7. Produces repeatable migration, test, CI, and review evidence.

P01 is an engineering foundation, not a commercial ERP release.

## 4. Entry Gate

All conditions are mandatory before P01 implementation starts:

| ID | Entry condition | Required evidence | Current state |
|---|---|---|---|
| P01-ENT-001 | P00 exit approved | P00 approval record | OPEN |
| P01-ENT-002 | Explicit P01 implementation authorization | Product Owner authorization with scope/version | OPEN |
| P01-ENT-003 | P01 specification approved | Approval section in this document | SATISFIED |
| P01-ENT-004 | Tenant-isolation test matrix approved | Approval section in test matrix | OPEN |
| P01-ENT-005 | Security requirements approved | QUAL-SEC-001 approval | SATISFIED |
| P01-ENT-006 | Testing strategy approved | QUAL-TST-001 approval | SATISFIED |
| P01-ENT-007 | Initial product increment and non-goals approved | Product scope decision | OPEN |
| P01-ENT-008 | CI/manifest baseline can enforce P01 task and evidence gates | Executed CI/validation evidence | OPEN |
| P01-ENT-009 | No unresolved critical P01 security/architecture decision | Decision/risk review | OPEN |

## 5. Bounded Scope

### 5.1 Project and environment bootstrap

- Create the Django project only through an authorized P01 task.
- Configure supported Python, Django, PostgreSQL, pytest, and pytest-django versions through pinned/locked dependencies.
- Establish typed development/test/production settings composition under ADR-017.
- Provide a secret-free `.env.example` or equivalent configuration catalogue.
- Provide Docker/Compose support for approved local development and integration testing under ADR-016.
- Establish health/readiness endpoints that disclose no tenant or secret data.

### 5.2 Initial Django applications

Only these domain applications are in P01 implementation scope:

| Application | P01 responsibility |
|---|---|
| `core` | Technical primitives, health checks, shared safe exceptions, request/correlation foundations |
| `tenants` | Tenant identity/lifecycle foundation, `TenantMembership`, minimum organizational scope, trusted tenant context |
| `users` | Custom user identity, authentication lifecycle, roles, permissions, membership-role assignments |
| `audit` | Minimal append-oriented audit-event persistence and protected recording interface |

Installing an app does not make future commercial modules available. No other ERP domain application is implemented in P01.

### 5.3 Minimum authoritative models

P01 may implement only the models required for its accepted workflows, subject to approved model specifications and migration review:

- `users.User` using the approved custom Django user model.
- `tenants.Tenant` with stable UUID identity and explicit lifecycle state.
- `tenants.TenantMembership` with tenant/user uniqueness and lifecycle state.
- Minimum `tenants.LegalEntity` and `tenants.Branch` records only if required for approved P01 authorization scope; UAE tax/payroll configuration is excluded.
- `users.Role`, `users.Permission`, role-permission mapping, and membership-role assignment with tenant-aware integrity.
- `audit.AuditEvent` containing minimal safe actor, tenant, action, resource, time, outcome, and correlation metadata.

Every model requires an ownership classification, UUID/bigint rationale, tenant path, mutable/immutable fields, constraints, indexes, audit behavior, retention classification, and authorization rules before migration creation.

### 5.4 Tenant provisioning and lifecycle foundation

- Provide one controlled, server-side tenant-provisioning operation.
- Create the tenant and initial authorized membership atomically where feasible.
- Record material lifecycle and membership changes in audit evidence.
- Define active, suspended, and closed/disabled behavior needed for P01 access enforcement.
- Make repeated or failed provisioning safe and investigable.

Public self-service registration, commercial trials, subscription creation, and automated billing are excluded until P02/commercial policy approval.

### 5.5 Authentication and sessions

- Implement approved session-based browser authentication using supported Django facilities.
- Include login, logout, password change, and secure recovery only to the extent approved in the P01 task specification.
- Enforce secure production session/cookie/CSRF/host/proxy configuration.
- Implement abuse controls and safe error behavior for exposed authentication endpoints.
- Establish MFA extension points; platform-privileged production access cannot launch without the approved MFA control.

Federation, social login, public registration, SSO, and broad machine authentication are excluded.

### 5.6 Authorization foundation

- Enforce deny-by-default tenant-scoped RBAC.
- Validate active membership before tenant access.
- Validate action, object, tenant, legal-entity/branch scope, workflow state, sensitive field, and separation of duties where applicable.
- Keep platform-administration permission separate from tenant roles.
- Restrict Django admin with the same ownership and tenant rules; it is not an automatic bypass.
- Provide a documented permission catalogue for P01 operations.

The P02 entitlement engine is excluded. P01 must expose a clear future entitlement decision seam without implementing a fake allow-all commercial entitlement service. P01 core platform operations are classified explicitly as platform foundation capabilities.

### 5.7 Trusted tenant context

- Resolve tenant context from a trusted route/session/server-side selection and active membership.
- Never trust a tenant UUID supplied by a client without independent authorization.
- Establish an explicit application tenant context for protected operations.
- Establish `app.current_tenant_id` transaction-locally for RLS-covered database work.
- Clear context through transaction/request boundaries and verify pooled-connection reuse.
- Reject missing, malformed, inactive, or unauthorized contexts safely.

### 5.8 Tenant-aware database integrity and RLS pilot

Every P01 table must be classified as tenant-owned, platform-global, tenant-configurable global reference, or operational with an explicit ownership path.

Tenant-owned relationships must use direct `tenant_id` where practical and database-enforced same-tenant references for critical relationships. UUID possession never proves authorization.

The P01 RLS pilot must cover the approved set of P01 tenant-owned tables. The model specification must name each table, policy, `USING`/`WITH CHECK` behavior, owner, runtime role, migration/rollback procedure, and tests. At minimum, the review must consider:

- Tenant memberships.
- Legal entities and branches implemented in P01.
- Membership-role assignments.
- Tenant-scoped audit events.

The runtime role must not be superuser, table owner for protected access, or possess `BYPASSRLS`; it cannot alter policies or schema. RLS is defense-in-depth and does not replace application authorization or constraints.

### 5.9 Audit and logging foundation

- Record approved material authentication, tenant, membership, role/permission, platform-access, and lifecycle events.
- Write required critical audit evidence in the protected transaction or an equally durable design.
- Prevent ordinary users from changing/deleting audit events.
- Implement structured application logging with correlation and safe tenant references.
- Exclude secrets, tokens, cookies, passwords, and unnecessary personal data.
- Define retention categories without inventing legal periods.

P01 does not implement a complete enterprise SIEM, legal-hold system, or customer-facing audit product.

### 5.10 Migrations, testing, and CI

- Create clean-install migrations only through reviewed tasks.
- Test constraints, RLS policies, migration/rollback or forward-fix assumptions, and restricted database roles on PostgreSQL.
- Implement mandatory automated tests from the tenant-isolation matrix.
- Run formatting/lint/static checks selected by the approved toolchain.
- Run secret/dependency checks and expose skipped/failed tests in evidence.
- Keep CI commands reproducible locally or in the approved test containers.

## 6. Explicit Non-Goals

P01 excludes:

- Module catalogue, subscription, entitlement, pricing, trials, SaaS billing, or payment provider implementation.
- CRM, sales, invoicing, e-invoicing, accounting, VAT, procurement, inventory, HRMS, payroll, projects, expenses, assets, banking, and reporting features.
- Customer business documents, file storage workflows, bulk exports, or provider integrations.
- Public/partner REST APIs beyond an explicitly approved operational need.
- Celery business workflows or transactional outbox implementation unless a specific P01 foundation task proves they are required; their contracts remain governed by ADR-009 and ADR-010.
- Production hosting/provider selection, production deployment, or customer onboarding.
- Full data-retention, backup/restore, disaster-recovery, SIEM, or observability-platform implementation.
- Claims of security certification, UAE compliance, production readiness, or commercial availability.

## 7. Planned Task Packages

Every task requires a separate authorized task record before execution.

| Task ID | Task | Depends on | Primary evidence |
|---|---|---|---|
| P01-T01 | Toolchain and Django project bootstrap | Entry gate | Locked dependencies, startup/system checks |
| P01-T02 | Typed settings and safe environment configuration | P01-T01 | Configuration tests, secret/image inspection |
| P01-T03 | PostgreSQL and migration foundation | P01-T01/T02 | Clean migration and database-role evidence |
| P01-T04 | Custom user and authentication foundation | P01-T02/T03 | IAM tests and security review |
| P01-T05 | Tenant, membership, and provisioning foundation | P01-T03/T04 | Model/transaction/idempotency tests |
| P01-T06 | Tenant context resolution and transaction integration | P01-T05 | Context and pooled-connection tests |
| P01-T07 | RBAC, object/organizational scope, and platform separation | P01-T04–T06 | Permission matrix and negative tests |
| P01-T08 | Tenant-aware constraints and RLS pilot | P01-T03/T05–T07 | Restricted-role PostgreSQL test evidence |
| P01-T09 | Audit and structured logging foundation | P01-T04–T08 | Audit/redaction/transaction tests |
| P01-T10 | Health/readiness and operational diagnostics | P01-T01/T02/T03 | Health/security tests |
| P01-T11 | Docker development/test environment | P01-T01–T03 | Reproducible build/start/test evidence |
| P01-T12 | CI gates and full P01 verification | P01-T01–T11 | CI evidence package and traceability |
| P01-T13 | Documentation, runbooks, and phase evidence | P01-T01–T12 | Reviewed evidence index and completion report |

Parallel execution is prohibited where tasks would independently change models, migrations, tenant middleware/context, settings, or authorization interfaces.

## 8. Deliverables

| ID | Deliverable | Exit requirement |
|---|---|---|
| P01-DEL-001 | Reproducible Django/PostgreSQL development and test bootstrap | Mandatory |
| P01-DEL-002 | Approved dependency and configuration manifests | Mandatory |
| P01-DEL-003 | `core`, `tenants`, `users`, and `audit` application foundations | Mandatory |
| P01-DEL-004 | Custom user, tenant, membership, and approved authorization models | Mandatory |
| P01-DEL-005 | Controlled tenant provisioning and lifecycle foundation | Mandatory |
| P01-DEL-006 | Trusted request/service/database tenant context | Mandatory |
| P01-DEL-007 | Tenant-aware constraints and reviewed RLS pilot | Mandatory |
| P01-DEL-008 | Authentication, RBAC, object scope, and platform separation | Mandatory |
| P01-DEL-009 | Audit and structured logging foundation | Mandatory |
| P01-DEL-010 | Health/readiness endpoints | Mandatory |
| P01-DEL-011 | PostgreSQL migrations and migration evidence | Mandatory |
| P01-DEL-012 | Tenant-isolation and IAM automated suites | Mandatory |
| P01-DEL-013 | CI execution evidence | Mandatory |
| P01-DEL-014 | Developer/setup/security/operations documentation | Mandatory |
| P01-DEL-015 | P01 completion report and approval record | Mandatory |

## 9. Acceptance Criteria

### 9.1 Bootstrap and configuration

- **P01-AC-001:** A developer can build, configure, migrate, test, and start the approved P01 stack using documented commands.
- **P01-AC-002:** Supported runtime/framework/database versions and dependency locks are explicit.
- **P01-AC-003:** Production-critical settings fail closed; development defaults cannot activate silently in production.
- **P01-AC-004:** No real secret exists in source, examples, images, logs, tests, or ordinary artifacts.
- **P01-AC-005:** Health/readiness endpoints disclose no tenant, configuration, credential, or sensitive business data.

### 9.2 Identity, authentication, and membership

- **P01-AC-006:** The custom user model is configured before initial migrations and uses supported authentication primitives.
- **P01-AC-007:** Login/logout and approved credential flows enforce session, CSRF, abuse, and safe-error controls.
- **P01-AC-008:** A user without active membership cannot access tenant-owned data.
- **P01-AC-009:** Membership suspension/revocation prevents subsequent access within the approved policy window.
- **P01-AC-010:** Tenant provisioning and membership lifecycle changes are atomic/recoverable, authorized, and audited.

### 9.3 Authorization and tenant context

- **P01-AC-011:** Permissions, object scope, legal-entity/branch scope, and platform roles are enforced server-side and deny by default.
- **P01-AC-012:** A user with multiple memberships accesses only the explicitly selected and revalidated tenant.
- **P01-AC-013:** Missing, malformed, inactive, forged, or unauthorized tenant context fails closed without disclosing protected existence.
- **P01-AC-014:** Context does not leak across requests, exceptions, transactions, tasks/test workers, or pooled database connections.
- **P01-AC-015:** HTML, service, administrative, and any approved API paths enforce equivalent tenant and authorization policy.

### 9.4 Database integrity and RLS

- **P01-AC-016:** Every table has a reviewed ownership classification and every tenant-owned model has an authoritative tenant path.
- **P01-AC-017:** Tenant A cannot read, create, update, delete, reference, enumerate, or administratively access Tenant B data.
- **P01-AC-018:** Critical cross-tenant relationships are prevented by PostgreSQL constraints, not application checks alone.
- **P01-AC-019:** RLS policies enforce approved read/write boundaries under production-relevant restricted roles.
- **P01-AC-020:** Runtime roles are not superuser, table owner for ordinary protected access, or `BYPASSRLS`, and cannot alter policies/schema.
- **P01-AC-021:** `app.current_tenant_id` is transaction-local and pooled connection reuse cannot retain prior tenant access.
- **P01-AC-022:** Policy migrations, clean install, forward migration, and rollback/forward-fix expectations are tested on PostgreSQL.

### 9.5 Audit, logging, quality, and evidence

- **P01-AC-023:** Required authentication, tenant, membership, permission, support/platform, and lifecycle events create safe append-oriented audit evidence.
- **P01-AC-024:** Required audit persistence failure prevents the protected state change where the specification requires atomic evidence.
- **P01-AC-025:** Logs and audit metadata contain correlation context but exclude prohibited secrets and unnecessary sensitive values.
- **P01-AC-026:** All mandatory tenant-isolation matrix scenarios pass; failures/skips remain visible.
- **P01-AC-027:** PostgreSQL-specific tests run on PostgreSQL using restricted roles for RLS evidence.
- **P01-AC-028:** Required CI checks are non-bypassable by ordinary contributors or have an explicit expiring exception approved under policy.
- **P01-AC-029:** Documentation, requirements, ADRs, tests, migrations, and evidence remain traceable and consistent.
- **P01-AC-030:** No critical unresolved defect affects tenant isolation, authentication, authorization, secrets, audit integrity, or migration safety.
- **P01-AC-031:** P01 completion and transition receive explicit human approval; no commercial/production claim is inferred.

## 10. Tenant-Isolation Verification Gate

The [tenant-isolation test matrix](P01_TENANT_ISOLATION_TEST_MATRIX.md) is mandatory. At minimum:

- Every scenario marked `MANDATORY` must be automated unless an explicitly approved manual method is the only valid evidence.
- RLS scenarios must use PostgreSQL and a production-relevant restricted role.
- Tests must use at least two tenants and identities with distinct memberships/scopes.
- Allowed and denied behavior must be asserted; empty fixture data is insufficient.
- Cross-tenant attempts must not disclose whether the target exists.
- Context-cleanup tests must exercise sequential connection/task reuse.
- Any skipped critical scenario blocks exit.

## 11. Migration and Data Safety

- Initial migrations are reviewed before merge and never rewritten after shared acceptance without an approved plan.
- Tenant ownership, unique constraints, same-tenant foreign keys, RLS policies, and indexes are version-controlled.
- Migration tests cover clean database, representative upgrade path when applicable, restricted-role behavior, and failure/forward-fix procedure.
- Destructive migration operations are outside ordinary P01 authorization.
- Test data is synthetic and explicitly tenant-scoped.

## 12. Security Review Requirements

Security review must confirm:

- Threat model for tenant context, membership, RLS, admin/support, and provisioning.
- Authentication/session/CSRF/host/proxy configuration.
- Permission and object-scope matrix.
- Runtime database roles and RLS policies.
- Secret and environment boundaries.
- Audit/log redaction and privileged-access evidence.
- Dependency, container, CI, and migration controls.
- All high/critical findings have disposition before exit.

## 13. Operational and Deployment Boundaries

P01 may establish development/test container and CI behavior, but it does not approve production deployment. P01 documents:

- Process roles and startup commands.
- Required PostgreSQL role separation.
- Health/readiness semantics.
- Logging and audit destinations as interfaces, not provider commitments.
- Migration execution procedure.
- Known backup/recovery dependencies and deferred production decisions.

Production region, topology, scaling, RPO/RTO, retention, monitoring provider, secrets backend, and customer onboarding remain outside P01.

## 14. Required Evidence Package

| Evidence ID | Evidence |
|---|---|
| P01-EV-001 | Approved phase and task authorizations |
| P01-EV-002 | Dependency locks, configuration catalogue, and build metadata |
| P01-EV-003 | Architecture/model/ownership and threat reviews |
| P01-EV-004 | Migration plans and executed PostgreSQL results |
| P01-EV-005 | Authentication/permission test reports |
| P01-EV-006 | Tenant-isolation matrix with executed results and artifacts |
| P01-EV-007 | Restricted-role/RLS policy and pooling evidence |
| P01-EV-008 | Audit/logging/redaction evidence |
| P01-EV-009 | Secret/dependency/container/static scan results |
| P01-EV-010 | CI run, skipped/failure/exception report, and reproducible commands |
| P01-EV-011 | Setup, migration, troubleshooting, and security documentation |
| P01-EV-012 | Open defect/risk/decision review |
| P01-EV-013 | Independent QA and security review dispositions |
| P01-EV-014 | P01 completion report and Product Owner exit approval |

Evidence must identify commit/image revision, environment, commands, results, limitations, reviewer, and safe artifact location. Unexecuted tests are recorded as `NOT_RUN`.

## 15. Exit Gate

**Gate name:** Core Security and Tenant Isolation Verified

P01 may be marked `APPROVED` only when:

- P01-AC-001 through P01-AC-031 are satisfied.
- Mandatory tenant-isolation and IAM scenarios pass without hidden skips.
- No critical/high unresolved issue undermines tenant isolation, authorization, secret safety, audit integrity, or migration correctness unless the project's policy explicitly permits and records acceptance; critical isolation failures are not routine exceptions.
- Architecture, Security, QA, Database, and DevOps reviewers have recorded dispositions for their scope.
- Product Owner explicitly approves P01 completion.

P01 approval does not authorize P02, production deployment, customer onboarding, or commercial availability.

## 16. Change Control

- Additions beyond the bounded apps/workflows require scope review and Product Owner approval.
- Changes conflicting with accepted ADRs require amended/superseding ADR approval.
- New requirements/tests receive stable identifiers; identifiers are never reused.
- A change to tenancy models, context, RLS, roles, permissions, settings, or migrations requires coordinated architecture/security/QA review.
- Deferred work must identify its later phase and consequence.

## 17. Current Assessment

| Area | State |
|---|---|
| P00 exit | OPEN |
| P01 specification | APPROVED; implementation not authorized |
| Tenant-isolation matrix | APPROVED VERIFICATION BASELINE; all tests `NOT_RUN` |
| Security/testing standards | APPROVED BASELINES |
| P01 task authorization | NOT_GRANTED |
| Implementation | NOT_STARTED |
| Test execution | NOT_RUN |
| Phase status | SPECIFICATION_IN_PROGRESS |

## 18. Approval

**Current Status:** APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED

- **Recommended disposition:** Approve as the bounded P01 implementation specification after P00 exit and Product, Architecture, Security, QA, Database, and DevOps review.
- **Approved By:** Product Owner — explicit market-standard review instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Approval of this specification must be followed by a separate explicit authorization to start P01 implementation tasks.

## 19. Change Log

| Version | Date | Status | Description |
|---|---|---|---|
| 1.0 | 28 October 2026 | APPROVED SPECIFICATION | Bounded P01 specification approved; P00 exit and separate implementation authorization remain required. |
