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

## 11. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved.

| Gate | Disposition for `tenants` |
|---|---|
| RDY-001 attributes | Section 4 names the authoritative records and invariants. Field detail is pinned to `../01-architecture/DATABASE_DESIGN.md` sections 5.1 to 5.5, which define tenant, legal entity, branch and membership structures with naming, key, timestamp and monetary conventions; this module does not restate them and must not diverge from them |
| RDY-002 states | Tenant lifecycle states and permitted transitions are owned by section 5; suspension and closure are deterministic and never delete records per TEN-MOD-011 |
| RDY-003 testable rules | Satisfied by `TEN-MOD-001`–`TEN-MOD-012`, each with a named verification method, plus the 53 scenarios in the [P01 tenant isolation matrix](../02-phases/P01_CORE_PLATFORM/P01_TENANT_ISOLATION_TEST_MATRIX.md) |
| RDY-004 permissions | `tenants.view_tenant`, `tenants.add_tenant`, `tenants.change_tenant_lifecycle`, `tenants.view_membership`, `tenants.add_membership`, `tenants.change_membership`, `tenants.remove_membership`, `tenants.configure_legal_entity`, `tenants.configure_branch`, `tenants.switch_tenant_context`, `tenants.view_all_tenants` as a platform-only capability |
| RDY-005 interface surfaces | Tenant context indicator and switcher in the authenticated shell, tenant list and detail in the platform-administration shell, membership management, and lifecycle confirmation, all mapped to `../01-architecture/UI_DESIGN_SYSTEM.md` `UIX-001`, `UIX-004` and `UIX-036` |
| RDY-006 reports and imports | Contributes to `RPT-801` tenant and subscription status, a provider-domain report never visible to a tenant. Tenant provisioning data entry is operator-driven; business data import is owned by `../01-architecture/DATA_MIGRATION_AND_IMPORT.md`, whose `MIG-002` requires the target tenant to be resolved server-side and never read from a file |
| RDY-007 document numbering | Tenant code is registered in `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md` as a provider-domain identifier, strictly separate from tenant ERP document numbering per `SEQ-005`. It is non-gapless master data |
| RDY-008 notifications | Registered in `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md`: tenant provisioned, tenant suspended, tenant reactivated, tenant closure scheduled, membership granted, membership suspended and membership removed. Membership and lifecycle messages are security category, mandatory and never digested |
| RDY-009 classification and retention | Tenant and legal-entity records are `C2`; membership links a `C3` user identity. Retention follows `RET-15` for terminated-tenant data and `RET-09` for lifecycle audit, under `../05-quality/DATA_PROTECTION_AND_RETENTION.md`. `PRIV-012` and `DEC-PRIV-011` govern the grace period, export window and disposal authority; no period is asserted here |
| RDY-010 threats | `THR-010`, `THR-011`, `THR-015` client-supplied tenant identifier, `THR-016` cross-tenant inference, `THR-017` connection or migration path without isolation enforcement, `THR-020` tenant user reaching a platform function, `THR-022` entitlement state manipulation, and `THR-RES-01` tenant administrator authority accepted by design |
| RDY-011 decision dependencies | `TEN-DEC-001` and `TEN-DEC-002` remain open. Suspended-tenant read and export behavior denies writes and enumerates permitted reads explicitly; absent that enumeration the behavior fails closed |
| RDY-012 regulatory assertions | None. Data residency is unresolved under `DEC-PRIV-004` and is not asserted by this module |

## 12. Migration, Compatibility and Recovery

The tenant boundary is the platform's foundational contract, so a change to tenant identity, the membership uniqueness rule or the `app.current_tenant_id` context key is a platform-wide breaking change requiring an ADR and a coordinated migration plan under `AGENTS.md` section 13. The canonical context key is fixed by ADR-004 and `DEC-SEC-002` and must not be altered by an implementation convenience.

Shared-database restore has a multi-tenant blast radius, recorded as `RISK-009`. Tenant-level recovery therefore requires the procedure in `../06-deployment/BACKUP_AND_RECOVERY.md`, and a restore is verified by confirming tenant and membership counts, membership uniqueness, same-tenant referential integrity across every dependent domain, row-level security policy presence and the runtime role's inability to bypass it, and audit continuity for lifecycle events.
