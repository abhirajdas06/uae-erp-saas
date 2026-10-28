# ADR-002: Shared PostgreSQL Database and Schema

| Field | Details |
|---|---|
| ADR ID | ADR-002 |
| Title | Shared PostgreSQL Database and Schema |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / Technical Lead |
| Reviewers | Architecture, Security, Database, DevOps |
| Project | UAE ERP SaaS Platform |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-001 |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DATABASE_DESIGN.md`, `MULTI_TENANCY.md`, `DJANGO_APP_STRUCTURE.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `ENTITLEMENT_ENGINE.md` |
| Supersedes | None |
| Superseded By | None |

---

## 1. Context

The UAE ERP SaaS platform will serve multiple business customers through a shared application. Each customer operates within a tenant context and may have multiple legal entities, branches, users, subscriptions, and commercial modules.

The platform will store business information including:

- Customer and supplier records.
- Sales quotations and orders.
- Commercial invoices and credit notes.
- Accounting journals and financial transactions.
- VAT calculations and reporting records.
- Procurement and inventory movements.
- Employee and payroll information.
- Subscription and SaaS billing records.
- External integration requests and responses.
- Audit events and compliance evidence.

This data has different sensitivity and integrity requirements. Financial, employee, and tax-related records require particularly strong access controls and traceability.

The platform needs a database strategy that provides reliable tenant isolation while keeping infrastructure, application development, deployment, backup, and maintenance manageable.

ADR-001 establishes a modular monolith architecture using Django and PostgreSQL. This ADR defines the initial PostgreSQL tenancy and schema strategy.

### 1.1 Problem Statement

The architecture must establish:

1. How multiple tenants share database infrastructure.
2. How tenant-owned records are identified.
3. How cross-tenant data access is prevented.
4. How database constraints support tenant isolation.
5. How PostgreSQL Row-Level Security (RLS) may provide defense-in-depth.
6. How cross-module transactions and relationships are handled.
7. How schema changes and tenant growth are managed.
8. How backups and recovery work under a shared database model.
9. Under what conditions a different database isolation strategy should be considered.

---

## 2. Decision Drivers

| Driver | Requirement |
|---|---|
| Tenant isolation | One tenant must not access another tenant's data. |
| Data integrity | Relationships and business invariants must be enforced. |
| Financial correctness | Accounting and financial operations require reliable transactions. |
| Development simplicity | Django applications should use a consistent database strategy. |
| Operational cost | Initial infrastructure should be appropriate for an early-stage SaaS product. |
| Scalability | The architecture should support growth without requiring immediate redesign. |
| Maintainability | Migrations and schema changes should remain manageable. |
| Security | Application and database controls should reinforce each other. |
| Backup and recovery | The platform must support documented recovery procedures. |
| Regulatory adaptability | Retention, export, and isolation requirements must be configurable where needed. |
| Future flexibility | Alternative tenant-isolation models must remain possible if justified. |

---

## 3. Options Considered

### Option A: Shared Database, Shared Schema

All tenants use one PostgreSQL database and a shared set of application tables.

Tenant-owned records contain a tenant identifier. Database constraints, application services, authorization checks, and optionally RLS enforce tenant boundaries.

**Advantages**

- Lowest initial infrastructure complexity.
- Efficient use of database resources.
- Straightforward cross-module queries and transactions.
- One coordinated migration strategy.
- Easier shared reporting and platform-level administration.
- Well suited to a modular monolith.

**Disadvantages**

- A tenant-isolation defect can expose data belonging to multiple customers.
- Tenants share database resources.
- Database-level per-tenant backup and restore is more complicated.
- Schema changes affect the shared database.
- Large tenants or expensive queries can affect other tenants unless resource usage is managed.

### Option B: Shared Database, Separate Schema per Tenant

Each tenant has a separate PostgreSQL schema within a shared database.

**Advantages**

- Greater physical separation of tenant tables.
- Some tenant-specific maintenance and export operations may be easier.
- Can provide an intermediate isolation strategy without separate database deployments.

**Disadvantages**

- Schema provisioning and migration complexity increases with tenant count.
- Search paths and schema selection must be handled safely.
- Shared reporting and cross-schema relationships become more complicated.
- Connection pooling and RLS strategies require careful design.
- Thousands of tenant schemas can become difficult to maintain.

### Option C: Separate Database per Tenant

Each tenant has a dedicated database, potentially on shared or separate PostgreSQL infrastructure.

**Advantages**

- Stronger database-level separation.
- Tenant-specific backup, restore, migration, and performance management can be easier to isolate.
- Supports customers with dedicated database requirements.
- Can reduce some cross-tenant blast-radius risks.

**Disadvantages**

- More complex provisioning and database lifecycle management.
- Migrations must be coordinated across many databases.
- Connection management and monitoring become more complicated.
- Cross-tenant analytics require additional infrastructure or aggregation.
- Infrastructure and operational costs may increase significantly.

### Option D: Hybrid Multi-Tenancy

Most customers use a shared database and schema, while selected enterprise customers use a dedicated schema or database.

**Advantages**

- Allows different isolation levels for different customer requirements.
- Can support enterprise contracts or special hosting arrangements.
- Provides a migration path for unusually large tenants.

**Disadvantages**

- Requires tenant-to-database routing and provisioning infrastructure.
- Increases deployment, migration, testing, backup, and operational complexity.
- Every supported isolation mode expands the system's test matrix.
- Cross-tenant reporting and platform administration become more complex.

---

## 4. Decision

**Adopt a shared PostgreSQL database and shared application schema for the initial SaaS architecture.**

Every tenant-owned business record must be associated with an authoritative tenant identifier, directly or through a documented ownership relationship.

Tenant isolation must be enforced at multiple layers:

1. Authentication and active-tenant validation.
2. Server-side authorization.
3. Tenant-aware application services and query interfaces.
4. Database relationships and constraints.
5. PostgreSQL RLS where approved and correctly configured.
6. Automated tenant-isolation tests.
7. Auditing and operational monitoring.

A shared schema does not imply unrestricted data access.

This decision does not prohibit dedicated databases or a future hybrid architecture. Those approaches require a separate ADR supported by validated requirements and operational evidence.

---

## 5. Tenant Ownership Model

### 5.1 Tenant Identity

The platform must have one authoritative tenant entity managed by the tenant-management domain.

Each tenant must have a stable, non-reused identifier. UUIDs are the preferred identifier strategy, subject to consistency with the approved database design.

The tenant identifier is an ownership and isolation attribute, not a secret or authorization credential.

A tenant ID supplied by a browser, API client, task payload, or integration callback must never be trusted without validation.

### 5.2 Tenant-Owned Records

Business records that belong to a tenant must have a clear ownership path.

For example:

- Customers and suppliers belong to a tenant.
- Sales documents belong to a tenant.
- Invoices and credit notes belong to a tenant.
- Accounting entries belong to a tenant.
- Stock movements belong to a tenant.
- Employee and payroll records belong to a tenant.
- Tenant-specific integration configurations belong to a tenant.

Where a business record is associated with a legal entity or branch, its tenant ownership must remain consistent with that relationship.

### 5.3 Direct Tenant Identifiers

Prefer a direct `tenant_id` field on frequently queried tenant-owned records where it improves isolation, query clarity, or database enforcement.

Do not add redundant tenant identifiers indiscriminately.

If a record stores both `tenant_id` and `legal_entity_id`, the database or application must ensure that the legal entity belongs to the same tenant.

A foreign key to a legal entity alone is not sufficient if the application cannot reliably enforce tenant ownership through that relationship.

### 5.4 Platform-Level Records

Some records may be global rather than tenant-owned, including:

- Module catalogue definitions.
- Platform configuration.
- Global permission definitions.
- Shared reference data explicitly approved for global use.

Global records must be identified explicitly. They must not be treated as tenant-owned merely because a request is operating within a tenant context.

Shared reference data must be read-only or modified only through controlled platform administration where appropriate.

---

## 6. Tenant Isolation Requirements

### 6.1 Application-Level Enforcement

All tenant-owned data access must be scoped to a validated tenant context.

Application code must not rely on developers remembering to add arbitrary tenant filters to every query.

Use centralized tenant-aware services, query interfaces, reusable authorization policies, and appropriate manager or selector conventions.

Application-level controls must cover:

- HTML views.
- Django REST Framework endpoints.
- Application services.
- Exports and reports.
- Background tasks.
- Webhooks and integration callbacks.
- Django Admin.
- Management commands.
- Scheduled jobs.
- Support and platform administration tools.

### 6.2 Active Tenant Validation

The application must validate:

1. The authenticated user.
2. The user's membership in the selected tenant.
3. The tenant's status.
4. Any applicable legal-entity or branch scope.
5. The user's permissions for the requested operation.
6. The relevant module entitlement.
7. The ownership of any requested object.

An authenticated user must not gain access to another tenant merely by changing a URL, request parameter, form field, or API payload.

### 6.3 Fail-Closed Behavior

If tenant context is missing, invalid, ambiguous, or inconsistent, tenant-owned data access must fail closed.

Do not silently fall back to an unrestricted query.

Platform-level tasks that legitimately operate across tenants must use explicitly authorized workflows with auditable scope.

---

## 7. PostgreSQL Row-Level Security

### 7.1 Decision

PostgreSQL RLS should be used as defense-in-depth for suitable tenant-owned tables, subject to a documented implementation and testing plan.

RLS does not replace application authorization, object-level permission checks, or domain validation.

### 7.2 Policy Design

For each RLS-protected table, the implementation must define:

- Whether the table is tenant-owned or global.
- The tenant identifier used by the policy.
- The trusted database-session tenant context.
- Read and write policy behavior.
- Insert and update checks.
- Platform administration behavior.
- Background-task behavior.
- Migration and maintenance behavior.
- Connection-pooling reset requirements.

Policies must be designed deliberately for the actual PostgreSQL role and connection configuration.

### 7.3 Tenant Context

Where session-level configuration is used to communicate tenant context to PostgreSQL, the value must be set by trusted server-side code.

Illustrative SQL:

```sql
SELECT set_config('app.current_tenant_id', '<validated-tenant-uuid>', true);
```

The third argument requests transaction-local configuration.

The example is illustrative, not a complete production policy.

The application must establish the tenant context inside the appropriate database transaction and ensure that it cannot leak across pooled connections or unrelated operations.

Never accept a database tenant context directly from an untrusted client.

### 7.4 Example Policy

A simplified example for a table containing a `tenant_id` column is:

```sql
ALTER TABLE sales_customer ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales_customer FORCE ROW LEVEL SECURITY;

CREATE POLICY sales_customer_tenant_isolation
ON sales_customer
USING (
    tenant_id = current_setting('app.current_tenant_id', true)::uuid
)
WITH CHECK (
    tenant_id = current_setting('app.current_tenant_id', true)::uuid
);
```

**This example must not be copied into production without adaptation and testing.**

Important considerations:

- A missing setting must not result in unrestricted access.
- The table and column names must match the actual schema.
- The application database role must not bypass RLS.
- Table owners, superusers, and roles with `BYPASSRLS` privileges require special attention.
- `FORCE ROW LEVEL SECURITY` changes how table owners are subject to policies but does not make superusers or `BYPASSRLS` roles subject to them.
- The behavior of policy expressions, casts, null values, and transaction-local settings must be tested.
- Migration and maintenance procedures must be designed to avoid accidental unrestricted access.
- RLS policies must be reviewed for both reads and writes.

### 7.5 Database Role Strategy

Use restricted application database credentials.

The ordinary web and worker application roles must not have superuser or `BYPASSRLS` privileges.

Where operationally practical, use separate credentials for:

- Application runtime.
- Database migrations.
- Backup operations.
- Restricted administrative maintenance.

The privileges assigned to each role must follow least privilege.

The application must not rely on a privileged role that bypasses RLS during ordinary tenant operations.

### 7.6 RLS Testing

Tests must verify that:

- Tenant A cannot read Tenant B's records.
- Tenant A cannot insert records owned by Tenant B.
- Tenant A cannot update a record to change its ownership to Tenant B.
- Missing tenant context denies tenant-owned access.
- Invalid tenant context fails safely.
- Tenant context does not leak between transactions or pooled connections.
- Background tasks establish the correct context.
- Ordinary application credentials cannot bypass RLS.
- Administrative access follows explicit, auditable policies.

---

## 8. Tenant-Aware Referential Integrity

Tenant isolation must extend beyond query filters.

### 8.1 Cross-Tenant Relationships

A record owned by Tenant A must not reference an entity owned by Tenant B unless a specifically approved cross-tenant relationship exists.

For example, an invoice belonging to Tenant A must not reference a customer belonging to Tenant B.

### 8.2 Composite Constraints

For selected tenant-owned relationships, use composite uniqueness and foreign-key constraints when supported by the actual schema and Django migration strategy.

Illustrative PostgreSQL design:

```sql
ALTER TABLE sales_customer
ADD CONSTRAINT uq_sales_customer_tenant_id
UNIQUE (tenant_id, id);

ALTER TABLE sales_invoice
ADD CONSTRAINT fk_sales_invoice_customer_same_tenant
FOREIGN KEY (tenant_id, customer_id)
REFERENCES sales_customer (tenant_id, id);
```

This is a conceptual example. The actual table names, key types, existing constraints, and migration sequence must match the implemented schema.

The referenced column pair must have an appropriate unique constraint or unique index.

The design must also account for:

- Nullable relationships.
- Tenant-owned parent and child records.
- Legal-entity and branch ownership.
- Cross-module relationships.
- Django ORM limitations or migration requirements.
- Existing data validation and backfilling.

### 8.3 Ownership Changes

Tenant ownership changes must not be implemented as ordinary updates.

Transferring business records between tenants requires an explicit business process, authorization, audit trail, and validation of related financial, legal, and regulatory implications.

Where transfer is not supported, ownership changes must be prohibited.

---

## 9. Database Transactions and Concurrency

A shared PostgreSQL database allows appropriate business operations to use local database transactions.

The following operations require explicit transaction design:

- Invoice numbering and issuance.
- Accounting journal posting.
- Inventory movements and balance updates.
- Subscription activation and entitlement changes.
- Payment and reconciliation state transitions.
- E-invoicing operation records and outbox events.

Use database constraints, atomic transactions, suitable locking, and idempotency controls where appropriate.

Avoid long-running database transactions that remain open while waiting for external HTTP calls.

External provider calls must use the durable operation and recovery patterns documented in `EVENT_AND_TASK_PROCESSING.md`.

---

## 10. Schema and Migration Management

### 10.1 Shared Migration Strategy

All tenants initially share the same application schema.

Django migrations must be version-controlled, reviewed, and executed through a controlled deployment process.

A schema migration must not assume that it can be independently applied to one tenant.

### 10.2 Migration Requirements

Before applying a migration, evaluate:

- Table size and expected execution time.
- Locking behavior.
- Index creation strategy.
- Data backfill requirements.
- Compatibility with active web processes and Celery workers.
- Rollback feasibility.
- Backup availability.
- Potential impact on financial and regulatory workflows.

### 10.3 Backward-Compatible Changes

Where practical, use staged migrations:

1. Add compatible schema elements.
2. Deploy code that supports the old and new representations.
3. Backfill data in controlled batches.
4. Switch reads and writes.
5. Remove obsolete structures in a later release.

Destructive or irreversible migrations require explicit review and a recovery plan.

### 10.4 Tenant-Specific Schema Changes

The initial architecture does not support independent schema versions for individual tenants.

Tenant-specific feature availability must be handled through the module lifecycle, entitlements, configuration, and compatible application behavior rather than tenant-specific database schemas.

---

## 11. Backup and Recovery

### 11.1 Shared Database Implications

The initial shared-database model uses database-level backups and recovery mechanisms.

A database restore may affect multiple tenants. Recovery planning must account for the shared blast radius.

### 11.2 Required Controls

The production design must specify:

- Backup frequency.
- Point-in-time recovery requirements.
- Backup encryption.
- Backup retention.
- Access restrictions.
- Off-site or cross-region storage where required.
- Restoration testing.
- Recovery Point Objective (RPO).
- Recovery Time Objective (RTO).
- Procedures for accidental deletion or data corruption.

Actual RPO and RTO values must be approved in the deployment and operational requirements; they must not be assumed from this ADR.

### 11.3 Tenant-Level Recovery

Restoring one tenant's data from a shared database backup may require a separate recovery workflow.

Possible approaches include restoring the backup to an isolated database, extracting the affected tenant's records, validating related dependencies, and importing the data through a controlled procedure.

Tenant-level recovery must preserve referential integrity, auditability, and financial consistency.

It must not be assumed that copying rows directly is safe.

### 11.4 Deletion and Retention

Tenant deletion, subscription termination, data export, retention, and legal holds must follow the approved retention policy and applicable legal requirements.

Deactivating a tenant or subscription must not automatically delete historical accounting, tax, invoice, payroll, or audit records.

---

## 12. Performance and Scalability

### 12.1 Initial Strategy

Begin with one appropriately sized PostgreSQL deployment and measure actual workload before introducing additional database topology.

Performance controls should include:

- Tenant-aware indexes.
- Query-plan analysis.
- Connection-pool management.
- Query timeouts where appropriate.
- Pagination and bounded exports.
- Background processing for long-running tasks.
- Database connection and lock monitoring.
- Resource and workload monitoring.
- Limits for expensive reporting queries.

### 12.2 Indexing

Indexes should reflect common access patterns, including tenant-scoped queries.

For example, where appropriate:

```sql
CREATE INDEX idx_sales_invoice_tenant_created
ON sales_invoice (tenant_id, created_at DESC);
```

This is illustrative. Actual indexes must be selected based on query patterns, data distribution, uniqueness requirements, and query-plan evidence.

Do not add indexes indiscriminately; they increase storage and write overhead.

### 12.3 Read Scaling

Read replicas, caching, reporting databases, or separate analytical infrastructure may be introduced when workload evidence justifies them.

Read replicas introduce replication lag and must not be used for operations requiring immediate consistency without an explicit consistency strategy.

Critical authorization and financial decisions must not rely on stale replicated data where that could violate business rules.

### 12.4 Tenant Workload Isolation

Large tenants and expensive workloads must be monitored.

Use bounded asynchronous workloads, query optimization, resource limits, and appropriate scheduling to reduce the risk of one tenant degrading service for others.

Database sharding is not part of the initial implementation.

---

## 13. Security and Data Protection

The shared database model requires strong access controls because multiple customers' records reside within the same database.

Required controls include:

- Least-privilege database roles.
- Tenant-aware data-access services.
- RLS where approved.
- Encryption in transit.
- Encryption at rest through the selected infrastructure.
- Secure secret management.
- Restricted database administration.
- Auditing of privileged operations.
- Controlled exports and data downloads.
- Sensitive-field access restrictions.
- Backup protection.
- Security monitoring.
- Tenant-isolation regression tests.

Payroll, employee, banking, tax, and financial data require additional role and permission controls.

The database strategy alone does not establish compliance with UAE data-protection, tax, or record-retention obligations. Applicable requirements must be verified independently.

---

## 14. Rationale

A shared database and shared schema provide the lowest justified initial operational complexity while retaining PostgreSQL transactions, referential integrity, migration consistency, and consolidated observability. The approach is suitable only when paired with explicit tenant ownership, restricted runtime roles, application-level scoping, tenant-aware constraints, and tested RLS defense-in-depth.

The alternative tenancy topologies remain valid reconsideration options when contractual, regulatory, recovery, capacity, or workload evidence justifies their additional cost.

## 15. Consequences

### Positive consequences

- One migration sequence and operational database baseline.
- Local transactions across related domain operations.
- Lower initial provisioning, monitoring, backup, and connection-management complexity.
- Efficient cross-domain reporting under controlled tenant scope.

### Negative consequences and trade-offs

- Isolation failures can have a multi-tenant blast radius.
- Tenant-level restore and deletion are more complex than database-level recovery.
- Large tenants can create noisy-neighbor pressure.
- RLS, database-role, constraint, and context-management discipline is mandatory.

### Risks and mitigations

- **Cross-tenant access:** layered application controls, RLS, constraints, and negative tests.
- **Shared recovery impact:** point-in-time recovery, isolated restore procedures, and tenant-level extraction validation.
- **Migration contention:** staged migrations, lock analysis, compatibility windows, and rollback planning.
- **Capacity concentration:** tenant-aware monitoring, query limits, indexing, and evidence-based topology review.

## 16. Operational Impact

Operations must manage one shared schema across all tenants, use least-privilege runtime roles, monitor tenant-skewed workloads, test full and tenant-level recovery, and coordinate migrations with web and worker compatibility. Production runbooks must cover RLS policy failures, privileged maintenance, suspected cross-tenant exposure, backup restoration, and controlled topology reconsideration.

---

## 17. Conditions for Reconsideration

The shared-schema model remains the default until measurable requirements justify an alternative.

Reconsider the decision if:

1. A customer contract requires dedicated database infrastructure.
2. Regulatory or contractual obligations require stronger tenant-level isolation.
3. A tenant's workload consistently degrades service for other tenants despite optimization.
4. Database capacity or operational limits cannot be addressed economically through normal scaling.
5. Tenant-specific backup and recovery requirements cannot be met adequately.
6. Independent tenant migration or maintenance becomes a material operational requirement.
7. Security analysis identifies risks that cannot be sufficiently mitigated within the shared-schema design.
8. A hybrid deployment model becomes commercially and operationally justified.

A trigger for reconsideration does not automatically authorize a change.

Any proposed alternative must be assessed for migration complexity, application routing, RLS, connection management, backup and recovery, reporting, operational cost, and data portability.

---

## 18. Implementation Requirements

| ID | Requirement | Expected Evidence |
|---|---|---|
| ADR002-IMP-001 | Establish the authoritative tenant model. | Reviewed tenant model and ownership rules. |
| ADR002-IMP-002 | Identify tenant-owned and global tables. | Documented ownership inventory. |
| ADR002-IMP-003 | Add tenant identifiers where required. | Reviewed models and migrations. |
| ADR002-IMP-004 | Enforce tenant-aware service and query conventions. | Shared implementation patterns and tests. |
| ADR002-IMP-005 | Prevent cross-tenant relationships. | Appropriate database constraints and validation. |
| ADR002-IMP-006 | Design RLS policies for selected tables. | Reviewed SQL policies and role configuration. |
| ADR002-IMP-007 | Prevent RLS context leakage. | Transaction and connection-pooling tests. |
| ADR002-IMP-008 | Establish least-privilege database roles. | Reviewed database privileges. |
| ADR002-IMP-009 | Establish migration governance. | Migration review and deployment procedures. |
| ADR002-IMP-010 | Define backup and recovery requirements. | Approved backup and recovery documentation. |
| ADR002-IMP-011 | Add cross-tenant security tests. | Automated regression tests. |
| ADR002-IMP-012 | Monitor database performance and capacity. | Operational metrics and alerts. |

Implementation must be phased. RLS must not be enabled across the entire database without first validating policies, application roles, migrations, background tasks, and administrative workflows.

---

## 19. Validation and Acceptance Criteria

The implementation satisfies this ADR when:

- [ ] All tenant-owned tables have documented ownership rules.
- [ ] Tenant identifiers and relationships are consistent with the approved data model.
- [ ] Tenant context is validated server-side.
- [ ] Application queries cannot silently fall back to unrestricted tenant-owned data access.
- [ ] Cross-tenant references are prevented through appropriate database constraints or validated enforcement mechanisms.
- [ ] RLS policies, where enabled, enforce the intended read and write boundaries.
- [ ] Runtime database credentials cannot bypass RLS.
- [ ] Tenant context is correctly reset or scoped across pooled database connections.
- [ ] HTTP, API, service, task, export, and administrative access paths are covered by tenant-isolation tests.
- [ ] Migration procedures account for compatibility, locking, and recovery.
- [ ] Backup restoration is tested.
- [ ] Backup retention and recovery objectives have been approved.
- [ ] Tenant-level data export and recovery procedures are documented where required.
- [ ] Performance monitoring can identify expensive queries and resource contention.
- [ ] Changes to the tenancy model require architectural review.

Evidence must be linked to implementation pull requests, test results, operational documentation, and security reviews.

---

## 20. Alternatives Rejected

### Separate Database per Tenant as the Default

Not selected initially because it introduces significant provisioning, connection management, migration, monitoring, backup, and reporting complexity before the product's customer scale and isolation requirements are known.

It remains a possible option for specific enterprise requirements.

### Separate Schema per Tenant as the Default

Not selected because the operational and migration complexity increases with tenant count and does not eliminate the need for robust application authorization.

It may be reconsidered if specific isolation or operational requirements justify it.

### Application-Only Tenant Filtering

Rejected as the sole isolation mechanism because a missed filter, incorrect query, or future regression could expose data across tenants.

Database constraints and RLS provide additional protection where correctly designed and implemented.

### RLS as the Only Isolation Mechanism

Rejected because RLS does not replace authentication, user authorization, object-level access checks, application business rules, or secure administrative workflows.

The approved approach uses layered controls.

---

## 21. References

### Internal Documents

- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- `docs/01-architecture/DJANGO_APP_STRUCTURE.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/01-architecture/ENTITLEMENT_ENGINE.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- `docs/06-deployment/BACKUP_AND_RECOVERY.md`
- `docs/06-deployment/DEPLOYMENT_ARCHITECTURE.md`

### Technical References

- PostgreSQL Row Security Policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- PostgreSQL Constraints: https://www.postgresql.org/docs/current/ddl-constraints.html
- PostgreSQL Backup and Restore: https://www.postgresql.org/docs/current/backup.html
- PostgreSQL Configuration Functions: https://www.postgresql.org/docs/current/functions-admin.html
- Django Database Documentation: https://docs.djangoproject.com/en/stable/topics/db/
- Django Migration Documentation: https://docs.djangoproject.com/en/stable/topics/migrations/

Verify version-specific behavior against the PostgreSQL and Django versions selected for deployment.

---

## 22. Approval

**Current Status:** ACCEPTED

- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted as the initial database-tenancy direction following `docs/07-project-management/ADR_STANDARDS_REVIEW.md`. Dedicated topology, recovery objectives, and tenant-level recovery remain separate decisions.

---

## 23. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial shared PostgreSQL database and schema decision accepted after standards review. |

**Final architectural principle:** Use a shared PostgreSQL database and schema for the initial SaaS platform, with explicit tenant ownership, layered isolation controls, integrity-preserving relationships, tested recovery procedures, and a documented path to stronger isolation when justified.
