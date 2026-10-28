# ADR-004: Tenant Isolation and PostgreSQL Row-Level Security

| Field | Details |
|---|---|
| ADR ID | ADR-004 |
| Title | Tenant Isolation and PostgreSQL Row-Level Security |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / Security Lead |
| Reviewers | Architecture, Security, Database, Development, DevOps |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-002, ADR-003, ADR-005, ADR-006, ADR-014, ADR-018 |
| Related Requirements | TEN-001–TEN-005, IAM-002–IAM-005, REP-001–REP-003, NFR-001, NFR-005, NFR-009 |
| Related Documents | `MULTI_TENANCY.md`, `DATABASE_DESIGN.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `EVENT_AND_TASK_PROCESSING.md`, `API_STANDARDS.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

ADR-002 proposes a shared PostgreSQL database and shared schema. This concentrates multiple customers' information in the same tables and makes tenant isolation a critical security boundary.

Application filters alone are vulnerable to omissions in views, services, tasks, reports, exports, raw SQL, administrative utilities, and future code. PostgreSQL Row-Level Security (RLS) can provide defense-in-depth, but unsafe database roles, missing policies, incorrect connection context, or untested administrative paths can create false confidence.

Existing documents also use two tenant-context setting names: `app.tenant_id` and `app.current_tenant_id`. A single key is required before implementation.

## 2. Decision Drivers

- Prevent cross-tenant reads, writes, references, caches, files, and exports.
- Fail closed when tenant context is absent or invalid.
- Preserve explicit application authorization and object-level rules.
- Support HTTP, APIs, Celery tasks, reports, support tools, and migrations.
- Avoid tenant context leaking through pooled connections.
- Permit controlled, audited platform operations.
- Provide testable evidence under production-equivalent database roles.

## 3. Options Considered

### Option A: Layered application isolation plus phased PostgreSQL RLS

Use trusted application context, tenant-aware services and queries, tenant-aware constraints, and RLS for approved tenant-owned tables.

**Advantages:** independent controls, protection against missing filters, database-enforced writes, and stronger regression resistance.

**Disadvantages:** policy, transaction, role, migration, and operational complexity.

### Option B: Application filtering without RLS

**Advantages:** simpler database setup and local development.

**Disadvantages:** one missed scope can expose data; raw SQL and administrative paths receive less protection.

### Option C: RLS as the sole isolation mechanism

**Advantages:** centralized row filtering.

**Disadvantages:** does not establish identity, membership, permissions, entitlements, legal-entity scope, or safe privileged access.

### Option D: Database or schema per tenant

**Advantages:** stronger physical or namespace separation.

**Disadvantages:** contradicts proposed ADR-002 and adds provisioning, migration, reporting, recovery, and connection-management costs not yet justified.

## 4. Decision

Use layered tenant isolation. Application-level isolation is mandatory for every tenant-aware operation. PostgreSQL RLS will be introduced as defense-in-depth on approved tenant-owned tables through a phased, test-driven rollout.

RLS must never replace authentication, active membership validation, authorization, entitlement evaluation, object checks, or business invariants.

### 4.1 Canonical tenant context

The canonical PostgreSQL transaction-local setting is:

`app.current_tenant_id`

Trusted server-side code must set it inside the transaction that performs tenant-owned database access:

```sql
SELECT set_config('app.current_tenant_id', '<validated-tenant-uuid>', true);
```

Client input must never be copied into this setting without membership, actor, and operation validation. The setting name is a convention, not a credential.

### 4.2 Context lifecycle

- Resolve the requested tenant from a trusted route, session, credential, or operation record.
- Authenticate the actor or authorized service identity.
- Validate active membership and applicable scope.
- Start the database transaction.
- Set `app.current_tenant_id` transaction-locally.
- Execute tenant-owned work through approved services.
- End the transaction before returning the connection.

Autocommit operations that depend on RLS require a reviewed wrapper that guarantees the same lifecycle. Session-persistent settings are prohibited for ordinary request and worker operations.

### 4.3 Table classification

Every table must be classified as:

- Tenant-owned.
- Platform-global.
- Tenant-configurable global reference.
- Operational or integration data with an explicit ownership path.

Tenant-owned tables should carry a direct, immutable `tenant_id` when practical. An indirect ownership path requires documented justification, enforceable joins or constraints, and equivalent isolation tests.

### 4.4 RLS policy rules

For each protected table:

- Enable RLS and determine whether `FORCE ROW LEVEL SECURITY` is required.
- Define both `USING` and `WITH CHECK` behavior.
- Treat missing context as no tenant access.
- Prevent ownership changes through ordinary updates.
- Review views, functions, partitions, and materialized views separately.
- Test read, insert, update, delete, and upsert behavior.
- Version policy changes through reviewed migrations.

Illustrative policies in architecture documents are not production-ready migrations.

### 4.5 Database roles

Ordinary web and worker roles must not be superusers, table owners that bypass intended protection, or members of roles with `BYPASSRLS`. They must not be able to disable RLS, alter policies, or set arbitrary privileged role state.

Migration, backup, and maintenance roles must be separate where operationally practical. Privileged procedures require restricted access, audit evidence, and explicit runbooks.

### 4.6 Referential integrity

Tenant isolation applies to relationships as well as queries. A Tenant A record must not reference a Tenant B record.

Use composite uniqueness and foreign-key constraints such as `(tenant_id, id)` where appropriate and supported by the schema. Where a database constraint is not practical, use explicit validation plus security tests and document the residual risk.

### 4.7 Non-HTTP paths

Celery tasks, scheduled jobs, reports, exports, imports, webhooks, management commands, cache keys, file paths, support tools, and administrative interfaces must establish tenant scope explicitly.

Task payloads must contain stable identifiers, not trusted authorization conclusions. Workers must reload the operation, validate ownership and current state, and then establish database context.

### 4.8 Platform operations

Cross-tenant operations are prohibited by default. Approved platform operations require:

- A dedicated service and permission.
- Explicit bounded scope.
- A restricted operational role or safe per-tenant iteration.
- Audit records identifying actor, purpose, tenants affected, and outcome.
- Tests demonstrating that ordinary tenant users cannot invoke the path.

### 4.9 Rollout strategy

RLS will not be enabled across every table in one unvalidated migration. Rollout must proceed by table group:

1. Classify ownership and add required constraints.
2. Implement context establishment and restricted roles.
3. Add policies for a bounded table group.
4. Run application and direct-database isolation tests.
5. Validate migrations, background tasks, admin, and support workflows.
6. Expand coverage only after evidence is recorded.

## 5. Rationale

Layered controls reduce dependence on any one developer, query helper, or database policy. The canonical transaction-local key eliminates incompatible examples. A phased rollout avoids deploying untested policies that could either expose data or make the platform inoperable.

## 6. Consequences

### Positive consequences

- Stronger defense against omitted tenant filters.
- Database-enforced ownership on reads and writes.
- Clear test and migration requirements.
- Safer shared-schema operation.

### Negative consequences and trade-offs

- PostgreSQL-specific integration tests are mandatory.
- Transactions and connection behavior require discipline.
- Privileged maintenance and cross-tenant reporting become more complex.
- Policy coverage must evolve with the schema.

### Risks and mitigations

- **False confidence:** test through every access path and restricted role.
- **Context leakage:** use transaction-local settings and pooling tests.
- **Role bypass:** inspect runtime privileges automatically.
- **Missing policy on new table:** add schema checks and migration review gates.
- **Performance overhead:** measure plans and add evidence-based tenant-leading indexes.

## 7. Security and Tenant-Isolation Implications

This ADR defines a critical security boundary. Any exemption, RLS bypass, cross-tenant operation, or change in tenant ownership requires security review. UUIDs and obscured URLs are not access controls.

The application must avoid revealing whether a cross-tenant object exists. Error behavior should use the approved not-found or denied policy without exposing sensitive identifiers.

## 8. Data Integrity and Migration

- Tenant ownership is immutable through ordinary workflows.
- Backfills must validate ownership before enabling non-null constraints or RLS.
- Policy migrations require rollback and lock-impact analysis.
- Data migration code must run under a role and context appropriate to its scope.
- Tenant-level restoration from a shared backup requires isolated recovery and integrity validation.

## 9. Operational Impact

Operations must monitor policy errors, denied database access, suspicious cross-tenant attempts, context failures, and privileged activity. Incident response must assume potential multi-tenant impact until scope is established.

## 10. Implementation Requirements

1. Replace conflicting `app.tenant_id` examples with `app.current_tenant_id` after approval.
2. Maintain a table ownership and RLS coverage inventory.
3. Create a reviewed tenant-context transaction helper.
4. Establish restricted runtime database roles.
5. Add tenant-aware constraints and indexes.
6. Add schema checks for missing policies and unsafe roles.
7. Build cross-tenant test factories and negative test suites.
8. Define privileged support and maintenance workflows.
9. Document pooler behavior before production use.

## 11. Validation and Acceptance Criteria

- [ ] Every table has a documented ownership classification.
- [ ] Tenant A cannot read, create, modify, delete, reference, export, or cache Tenant B data.
- [ ] Missing and malformed tenant context fail closed.
- [ ] Runtime roles have neither superuser nor `BYPASSRLS` capability.
- [ ] Context does not leak between requests, tasks, transactions, or pooled connections.
- [ ] HTTP, API, service, task, report, export, file, and admin paths have negative tests.
- [ ] Cross-tenant foreign keys are prevented.
- [ ] Platform operations are separately authorized and audited.
- [ ] Policy migrations and rollback behavior are tested on PostgreSQL.
- [ ] Performance is measured under representative tenant-scoped queries.

## 12. Alternatives Rejected

- Application-only isolation is rejected as the sole control.
- RLS-only isolation is rejected because it cannot express the complete authorization model.
- Immediate per-tenant schemas or databases are rejected under proposed ADR-002 absent stronger requirements.
- Session-persistent tenant settings are rejected for ordinary pooled connections.

## 13. References

- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- PostgreSQL row security: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- PostgreSQL configuration functions: https://www.postgresql.org/docs/current/functions-admin.html
- Django transactions: https://docs.djangoproject.com/en/stable/topics/db/transactions/

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Layered application isolation plus phased PostgreSQL RLS using `app.current_tenant_id`.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; restricted runtime roles, pooling behavior, policy coverage, and source-key reconciliation remain mandatory verification work.

This accepted decision governs tenant-owned data access design. Production use still requires implementation evidence and security review.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial layered tenant-isolation and RLS decision accepted after standards review. |
