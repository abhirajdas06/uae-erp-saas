# TENANTS — Tenant Management Specification

| Property | Value |
|---|---|
| Document ID | MOD-TENANTS-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Owning Phase | P01 |
| Django App | `tenants` |
| Domain Owner | Tenant identity, lifecycle, membership, and trusted tenant context |
| Commercial Module | No |
| Tenant-Owned Data | Mixed |

## 1. Purpose

`tenants` establishes the authoritative customer-tenant boundary for every protected operation. It owns `Tenant`, `TenantMembership`, approved organizational scope, provisioning, lifecycle enforcement, and trusted request/service/database context.

## 2. Governing sources

- P01 phase specification and tenant-isolation test matrix
- `MULTI_TENANCY.md`, `DATABASE_DESIGN.md`, and `AUTHENTICATION_AND_PERMISSIONS.md`
- ADR-002, ADR-003, ADR-004, ADR-005, and ADR-014
- SEC-002 through SEC-005; TST-003 through TST-006

## 3. Scope

Included:

- tenant identity and active/suspended/closed lifecycle;
- membership creation, invitation/activation where explicitly tasked, suspension, and removal;
- atomic initial tenant provisioning;
- trusted tenant selection and context;
- minimum legal-entity/branch scope required by P01 authorization;
- same-tenant constraints and RLS pilot.

Excluded:

- subscription, trial, pricing, billing, and commercial entitlement state;
- UAE VAT registrations, payroll establishments, or regulatory profiles;
- tenant deletion, automated offboarding, or tenant-level restore implementation;
- cross-tenant support access without separately approved platform authorization.

## 4. Authoritative records

| Record | Ownership | Key invariants |
|---|---|---|
| Tenant | Platform-managed customer boundary | UUID identity; explicit lifecycle; no business-data cascade deletion |
| TenantMembership | Tenant/user association | Unique tenant/user pair; valid lifecycle; user identity remains owned by `users` |
| LegalEntity | Tenant-owned organizational scope, if included | Direct tenant key; same-tenant references |
| Branch | Tenant-owned scope, if included | Direct tenant key; belongs to same-tenant legal entity |

## 5. Lifecycle and provisioning

Provisioning must use an application service and transaction. It creates the tenant, initial membership, required defaults, and audit evidence atomically where possible. A durable idempotency key prevents duplicate tenants from retry or double submission.

Lifecycle behavior:

- `ACTIVE`: authorized active memberships may operate.
- `SUSPENDED`: protected writes are denied; permitted read/export behavior requires an approved policy.
- `CLOSED`: normal access denied; data is retained under approved retention/recovery policy.

No lifecycle state deletes business data automatically.

## 6. Requirements

| ID | Requirement | Verification |
|---|---|---|
| TEN-MOD-001 | Every tenant-owned record has an authoritative tenant path | Model inventory review |
| TEN-MOD-002 | Tenant selection is accepted only from trusted server-side context plus active membership | Request negative tests |
| TEN-MOD-003 | Cross-tenant object identifiers return safe denial without existence disclosure | IDOR tests |
| TEN-MOD-004 | Provisioning is atomic, idempotent, and audited | Transaction/retry tests |
| TEN-MOD-005 | Tenant/user membership uniqueness is database-enforced | PostgreSQL constraint tests |
| TEN-MOD-006 | Critical tenant-owned relationships enforce same-tenant integrity in the database | Constraint tests |
| TEN-MOD-007 | `app.current_tenant_id` is transaction-local and cleared across pooled reuse | PostgreSQL pooling tests |
| TEN-MOD-008 | Runtime roles cannot bypass or alter approved RLS policies | Restricted-role tests |
| TEN-MOD-009 | Background tasks receive validated tenant identity and re-establish context explicitly | Task isolation tests |
| TEN-MOD-010 | Reports, exports, caches, files, admin, and audit queries preserve tenant scope | Cross-channel isolation matrix |
| TEN-MOD-011 | Suspension/closure behavior is deterministic and does not delete records | Lifecycle tests |
| TEN-MOD-012 | Cross-tenant operations require an explicit platform capability and audit trail | Permission/security review |

## 7. RLS pilot

The P01 task must name protected tables and define `USING` and `WITH CHECK` policies. Candidate tables are memberships, legal entities, branches, membership-role assignments, and tenant audit events.

RLS is defense-in-depth. Application queries, object lookup, services, tasks, admin, reports, and exports remain explicitly tenant-scoped.

## 8. Security and privacy

Tenant UUIDs are identifiers, not secrets or authorization. Tenant names and metadata may be sensitive and must not appear in unauthenticated diagnostics. Support/platform access is separate from tenant roles, time-bounded where appropriate, justified, and audited.

## 9. Acceptance and tests

Exit requires execution of every applicable scenario in `P01_TENANT_ISOLATION_TEST_MATRIX.md`, including request, service, task, report/export, cache/file, admin, RLS, pooling, constraint, provisioning, suspension, concurrency, and regression paths.

No SQLite-only result can satisfy PostgreSQL constraint or RLS criteria.

## 10. Pending decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| TEN-DEC-001 | Minimum LegalEntity/Branch scope in P01 | Product / Architecture | P01 task manifest | Include only fields needed for authorization scope |
| TEN-DEC-002 | Suspended tenant read/export policy | Product / Security | Lifecycle implementation | Deny writes; explicitly enumerate any permitted reads |
| TEN-DEC-003 | Tenant closure/recovery workflow | Product / Legal / DevOps | Production data handling | Retain data; design recovery before deletion |
