# P01 Tenant-Isolation Test Matrix

| Property | Value |
|---|---|
| Document ID | P01-TEN-TEST-001 |
| Version | 1.0 |
| Status | APPROVED VERIFICATION BASELINE — ALL TESTS NOT RUN |
| Date | 28 October 2026 |
| Parent Phase | [P01 Phase Specification](P01_PHASE_SPECIFICATION.md) |
| Owners | QA / Security / Database |
| Required Reviewers | Architecture, Security, QA, Database, Core Platform |
| Execution State | NOT_RUN — implementation is not authorized |

## 1. Purpose

This matrix defines the minimum tenant-isolation evidence required for P01. It converts TEN-001 through TEN-003, IAM-002 through IAM-005, accepted ADR-002, ADR-004, ADR-005, ADR-014, SEC-002, SEC-005, SEC-012, SEC-013, TST-003, TST-004, TST-006, TST-009, and TST-013 into executable scenarios.

Rows are plans, not results. No row may become `PASSED` without recorded execution evidence from the named environment and role.

## 2. Test Data and Environment Contract

The suite requires synthetic fixtures containing:

- Tenant A and Tenant B with distinct UUIDs and lifecycle states.
- User A with active Tenant A membership only.
- User B with active Tenant B membership only.
- User AB with independently scoped memberships in both tenants.
- A suspended membership and a suspended tenant.
- Tenant-specific legal entity/branch records when implemented.
- Distinct roles, permissions, membership-role assignments, and tenant-scoped audit records.
- Same-shaped objects in both tenants so empty/missing data cannot create false positives.

Database evidence must use PostgreSQL and:

- A migration/owner role used only for controlled schema changes.
- A runtime role that is not superuser, has no `BYPASSRLS`, cannot alter schema/policies, and does not rely on owner bypass.
- `app.current_tenant_id` set transaction-locally.
- The same relevant pooling/connection behavior intended for production.

## 3. Status and Priority

Priority values:

- `MANDATORY`: failure or skip blocks P01 exit.
- `CONDITIONAL`: mandatory if the named surface exists in P01.
- `DEFERRED`: belongs to a later phase and must remain linked, not silently removed.

Execution states are `NOT_RUN`, `PASSED`, `FAILED`, `BLOCKED`, `SKIPPED_APPROVED`, and `NOT_APPLICABLE_REVIEWED`. Critical scenarios are not eligible for routine skip approval.

## 4. Tenant Context and Request Isolation

| Test ID | Priority | Scenario / action | Expected result | Level | Linked controls | State |
|---|---|---|---|---|---|---|
| P01-TEN-TST-001 | MANDATORY | Active User A selects Tenant A through the approved server-side flow | Tenant A context established; access proceeds to later checks | Integration | TEN-003; ADR-004; SEC-002; TST-004 | NOT_RUN |
| P01-TEN-TST-002 | MANDATORY | User A submits Tenant B UUID/slug directly | Request denied without confirming Tenant B existence | Security | TEN-002, TEN-003; IAM-002; SEC-002, SEC-005 | NOT_RUN |
| P01-TEN-TST-003 | MANDATORY | Protected request has no tenant context | Fails closed; no tenant-owned query succeeds | Integration/DB | TEN-003; ADR-004 | NOT_RUN |
| P01-TEN-TST-004 | MANDATORY | Tenant identifier is malformed or unknown | Safe denial/error; no context or data disclosure | Security | TEN-003; SEC-002, SEC-006 | NOT_RUN |
| P01-TEN-TST-005 | MANDATORY | Active user requests a suspended tenant | Access follows approved suspension policy and is denied for protected work | Integration | TEN-005; IAM-002 | NOT_RUN |
| P01-TEN-TST-006 | MANDATORY | User's Tenant A membership is suspended/revoked | Subsequent Tenant A access denied within policy window | Integration | IAM-002; ADR-005; SEC-005 | NOT_RUN |
| P01-TEN-TST-007 | MANDATORY | User AB switches from Tenant A to Tenant B | Membership and permissions are revalidated; context becomes B only | Integration | TEN-003; IAM-002, IAM-003 | NOT_RUN |
| P01-TEN-TST-008 | MANDATORY | Sequential requests on reused connection process A then B | B cannot see A; transaction-local context does not leak | PostgreSQL integration | ADR-004; SEC-002; TST-004 | NOT_RUN |
| P01-TEN-TST-009 | MANDATORY | Exception occurs after Tenant A context is established | Transaction closes/rolls back; next request has no stale A context | PostgreSQL integration | ADR-004; NFR-006 | NOT_RUN |
| P01-TEN-TST-010 | MANDATORY | Public health/login route operates without tenant | Only explicitly public behavior works; no tenant data is queried/exposed | Integration | TEN-003; SEC-004 | NOT_RUN |

## 5. Service, ORM, and Object Isolation

| Test ID | Priority | Scenario / action | Expected result | Level | Linked controls | State |
|---|---|---|---|---|---|---|
| P01-TEN-TST-011 | MANDATORY | Tenant-aware selector/service runs under Tenant A | Returns only A records | Service/DB | TEN-002; ADR-002, ADR-004 | NOT_RUN |
| P01-TEN-TST-012 | MANDATORY | User A requests Tenant B object by valid UUID | Denied/not found safely; no B fields disclosed | View/service security | TEN-002; IAM-004; SEC-005 | NOT_RUN |
| P01-TEN-TST-013 | MANDATORY | User A attempts to update Tenant B object | No change commits; attempt handled/audited as specified | Service/DB | TEN-002; IAM-004 | NOT_RUN |
| P01-TEN-TST-014 | MANDATORY | User A attempts to delete Tenant B object | No delete/cascade occurs | Service/DB | TEN-002; IAM-004 | NOT_RUN |
| P01-TEN-TST-015 | MANDATORY | Create request supplies Tenant B ownership while context is A | Protected ownership ignored/rejected; no B record created | Service/DB | ADR-014; SEC-005, SEC-006 | NOT_RUN |
| P01-TEN-TST-016 | MANDATORY | Tenant A child references Tenant B parent | Database constraint rejects relationship | PostgreSQL | ADR-002, ADR-014; TST-003, TST-004 | NOT_RUN |
| P01-TEN-TST-017 | MANDATORY | Bulk update/delete includes mixed-tenant identifiers | Only authorized A scope considered; B unchanged; unsafe bulk call rejected | Service/DB | TEN-002; IAM-004 | NOT_RUN |
| P01-TEN-TST-018 | MANDATORY | Raw SQL under Tenant A accesses RLS-protected table without explicit tenant filter | RLS returns/changes only A rows | PostgreSQL security | ADR-004; SEC-002 | NOT_RUN |
| P01-TEN-TST-019 | MANDATORY | Ordinary operation attempts to change immutable `tenant_id` | Operation rejected at service/database boundary | Service/DB | TEN-001; ADR-014 | NOT_RUN |
| P01-TEN-TST-020 | MANDATORY | Valid UUID for B is presented in form/API ownership field | UUID possession does not grant access; field rejected or safely ignored | Transport/service | IAM-004; ADR-014 | NOT_RUN |

## 6. PostgreSQL RLS and Role Isolation

| Test ID | Priority | Scenario / action | Expected result | Level | Linked controls | State |
|---|---|---|---|---|---|---|
| P01-TEN-TST-021 | MANDATORY | Restricted runtime role queries protected table with no context | Default-deny: no tenant rows accessible | PostgreSQL security | ADR-004; SEC-002 | NOT_RUN |
| P01-TEN-TST-022 | MANDATORY | Context is Tenant A and table contains A/B records | SELECT returns A only | PostgreSQL security | ADR-002, ADR-004 | NOT_RUN |
| P01-TEN-TST-023 | MANDATORY | Context A attempts INSERT with Tenant B ownership | `WITH CHECK`/constraint rejects insert | PostgreSQL security | ADR-004, ADR-014 | NOT_RUN |
| P01-TEN-TST-024 | MANDATORY | Context A attempts UPDATE/DELETE of B row | No B row is visible or modified | PostgreSQL security | ADR-004 | NOT_RUN |
| P01-TEN-TST-025 | MANDATORY | Context A attempts to reassign A row to B | Policy/constraint rejects ownership change | PostgreSQL security | ADR-004, ADR-014 | NOT_RUN |
| P01-TEN-TST-026 | MANDATORY | Runtime role attributes are inspected | Not superuser; no `BYPASSRLS`; no schema/policy alteration rights | PostgreSQL inspection/test | ADR-004; SEC-002 | NOT_RUN |
| P01-TEN-TST-027 | MANDATORY | Runtime role attempts `ALTER TABLE ... DISABLE ROW LEVEL SECURITY` or policy change | Permission denied | PostgreSQL security | ADR-004 | NOT_RUN |
| P01-TEN-TST-028 | MANDATORY | Protected table ownership/`FORCE ROW LEVEL SECURITY` configuration is inspected and exercised | Ordinary protected access cannot use owner bypass | PostgreSQL security | ADR-004 | NOT_RUN |
| P01-TEN-TST-029 | MANDATORY | Transaction-local setting ends, connection is reused | `app.current_tenant_id` is absent/new value only; prior tenant inaccessible | PostgreSQL pooling | TEN-003; ADR-004 | NOT_RUN |
| P01-TEN-TST-030 | MANDATORY | RLS migration is applied to clean database | Policies enabled with correct `USING`/`WITH CHECK`; verification query passes | Migration/PostgreSQL | ADR-004; NFR-009 | NOT_RUN |
| P01-TEN-TST-031 | MANDATORY | RLS migration/forward-fix failure is simulated | Failure is visible; schema/policy does not remain silently half-secured | Migration/PostgreSQL | ADR-004, ADR-015; TST-014 | NOT_RUN |
| P01-TEN-TST-032 | MANDATORY | Referential-integrity error is triggered with cross-tenant identifier | Error is safe and does not disclose protected B data | PostgreSQL/transport | ADR-004, ADR-014; SEC-006 | NOT_RUN |

## 7. Membership, Permission, and Administrative Isolation

| Test ID | Priority | Scenario / action | Expected result | Level | Linked controls | State |
|---|---|---|---|---|---|---|
| P01-TEN-TST-033 | MANDATORY | User has role in Tenant A only and acts in B | Role grants no B permission | Authorization | IAM-003; ADR-005 | NOT_RUN |
| P01-TEN-TST-034 | MANDATORY | User has view permission but attempts update/delete | Denied server-side | Authorization | IAM-003, IAM-004; SEC-005 | NOT_RUN |
| P01-TEN-TST-035 | CONDITIONAL | User lacks required legal-entity/branch scope | Object/action denied despite tenant membership | Authorization | IAM-004; ADR-005 | NOT_RUN |
| P01-TEN-TST-036 | MANDATORY | Tenant administrator attempts platform administration | Denied; platform permissions remain separate | Authorization/security | IAM-005; ADR-005 | NOT_RUN |
| P01-TEN-TST-037 | MANDATORY | Django admin user accesses out-of-scope tenant record | Denied; admin is not a tenant/RLS bypass | Admin security | IAM-005; ADR-004, ADR-005 | NOT_RUN |
| P01-TEN-TST-038 | CONDITIONAL | Approved support operator requests bounded Tenant A access | Purpose/scope/time checks enforced and action audited | Security/audit | IAM-005; SEC-005, SEC-012 | NOT_RUN |
| P01-TEN-TST-039 | MANDATORY | Role/permission is revoked during active session | Subsequent authorization reflects revocation within policy window | Authorization | IAM-003; ADR-005 | NOT_RUN |
| P01-TEN-TST-040 | MANDATORY | Permission or membership cache contains stale allow | Revoked access is not improperly retained | Integration/security | IAM-002, IAM-003; SEC-005 | NOT_RUN |

## 8. Provisioning, Audit, Logging, and Concurrency

| Test ID | Priority | Scenario / action | Expected result | Level | Linked controls | State |
|---|---|---|---|---|---|---|
| P01-TEN-TST-041 | MANDATORY | Authorized tenant provisioning succeeds | Tenant and initial membership are consistent and correctly owned | Service/transaction | TEN-001; ADR-003, ADR-014 | NOT_RUN |
| P01-TEN-TST-042 | MANDATORY | Provisioning fails after partial work | Transaction rolls back or durable recovery state is explicit; no orphan access | Transaction/failure | NFR-006; ADR-003 | NOT_RUN |
| P01-TEN-TST-043 | MANDATORY | Provisioning request is repeated/concurrent | No unintended duplicate tenant/membership; deterministic outcome | Concurrency/idempotency | TEN-001; NFR-007 | NOT_RUN |
| P01-TEN-TST-044 | MANDATORY | Membership revocation races with protected operation | Defined locking/authorization policy prevents unauthorized commit | Concurrency/security | IAM-002; ADR-005 | NOT_RUN |
| P01-TEN-TST-045 | MANDATORY | Material membership/role/platform change succeeds | Tenant, actor, action, target, time, and outcome audit evidence recorded | Audit integration | AUD-001; ADR-018 | NOT_RUN |
| P01-TEN-TST-046 | MANDATORY | Tenant user queries audit records | Only authorized tenant/scope records visible | Audit/security | ADR-004, ADR-018; SEC-012 | NOT_RUN |
| P01-TEN-TST-047 | MANDATORY | Audit persistence required for protected state change is forced to fail | Protected state change rolls back/fails | Transaction/audit | ADR-018; SEC-012 | NOT_RUN |
| P01-TEN-TST-048 | MANDATORY | Authentication/authorization/tenant error is logged | Correlation and safe tenant reference present; secrets and protected B data absent | Logging/security | OPS-001; ADR-018 | NOT_RUN |

## 9. Conditional Cross-Boundary Scenarios

These become mandatory if the surface exists in P01. Otherwise reviewers record `NOT_APPLICABLE_REVIEWED` with evidence that the surface is absent.

| Test ID | Priority | Scenario / action | Expected result | Level | Linked controls | State |
|---|---|---|---|---|---|---|
| P01-TEN-TST-049 | CONDITIONAL | P01 background task processes A then B sequentially | Task reloads durable tenant context; no leakage between tasks | Task/PostgreSQL | ADR-009; SEC-013; TST-009 | NOT_RUN |
| P01-TEN-TST-050 | CONDITIONAL | Background task runs after membership/authority revocation | Approved revalidation/system-authority rule enforced | Task/security | ADR-005, ADR-009 | NOT_RUN |
| P01-TEN-TST-051 | CONDITIONAL | Tenant-scoped cache uses same logical key for A/B | Values remain isolated; invalidation cannot expose another tenant | Integration/security | TEN-002; SEC-002 | NOT_RUN |
| P01-TEN-TST-052 | CONDITIONAL | P01 exposes an API/HTMX endpoint | Same tenant/membership/permission/object checks as service/full page | Transport/security | ADR-007, ADR-008; SEC-005, SEC-007 | NOT_RUN |
| P01-TEN-TST-053 | CONDITIONAL | Any P01 file/download/export/report exists | Retrieval is tenant-scoped before presentation and cross-tenant identifier fails safely | Integration/security | TEN-002; SEC-008 | NOT_RUN |

## 10. Deferred Later-Phase Isolation Coverage

The following are outside P01 implementation but must be added to later phase matrices before their features are accepted:

- Subscription and entitlement caches/transitions.
- CRM/sales/invoice/accounting/VAT domain records.
- Provider webhooks and e-invoicing operations.
- Financial posting, inventory, payroll, banking, and reconciliation.
- File/object storage, exports, reports, analytics, and search indexes.
- Cross-tenant platform support tools and customer data portability/recovery.

P01 establishes patterns and test infrastructure; later phases must test their own tables and surfaces rather than inheriting a blanket assurance claim.

## 11. Evidence Requirements

Each executed row records:

- Test ID and automated test path/name.
- Requirement/ADR/SEC/TST references.
- Commit and image revision.
- PostgreSQL version and database role attributes.
- Relevant configuration and pooling mode.
- Fixture tenants/users/scopes using synthetic identifiers.
- Command, start/end time, result, and safe artifact link.
- Skips, failures, exceptions, owner, and reviewer.

Evidence must prove the intended protected rows exist. A test that returns no rows because fixtures are empty is invalid.

## 12. Automation and Gate Rules

- `MANDATORY` rows run in the applicable P01 integration/security gate.
- RLS/database rows run on PostgreSQL with restricted runtime credentials.
- Tests must assert both allowed A behavior and denied B behavior where applicable.
- Random ordering/parallel execution must not create hidden shared tenant context.
- Failed or skipped mandatory tests block P01 exit.
- Test weakening/deletion requires review of the linked requirement and matrix row.
- A production-only manual assertion cannot replace an automatable negative test.

## 13. Matrix Acceptance Criteria

- [x] P01-TEN-TST-001 through P01-TEN-TST-053 have unique identifiers.
- [x] Every mandatory P01 tenant boundary has allowed and denied scenarios.
- [x] RLS tests specify restricted PostgreSQL roles and transaction-local context.
- [x] Request, service, ORM, raw SQL, admin, audit, concurrency, and pooling paths are covered.
- [x] Conditional surfaces have explicit activation rules.
- [x] Later-phase surfaces are deferred with named scope, not assumed secure.
- [x] Evidence format prevents empty-fixture and superuser false confidence.
- [x] Security, QA, Architecture, and Database review is recorded by the scoped approval; execution remains separate.

## 14. Approval

**Current Status:** APPROVED VERIFICATION BASELINE — ALL TESTS NOT RUN

- **Recommended disposition:** Approve as the minimum P01 tenant-isolation verification contract after security, database, architecture, and QA review.
- **Approved By:** Product Owner — explicit market-standard review instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Approval authorizes no test execution or implementation until the P01 entry gate is satisfied.

## 15. Change Log

| Version | Date | Status | Description |
|---|---|---|---|
| 1.0 | 28 October 2026 | APPROVED VERIFICATION BASELINE | P01 tenant-isolation verification contract approved; all scenarios remain `NOT_RUN`. |
