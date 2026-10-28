# Multi-Tenancy Architecture and Tenant Isolation

| Property | Value |
|---|---|
| Document ID | ARCH-004 |
| Document | `docs/01-architecture/MULTI_TENANCY.md` |
| Product | UAE ERP SaaS |
| Version | 1.0 |
| Status | APPROVED — Tenant-Isolation Architecture Baseline |
| Last Reviewed | 27 October 2026 |
| Primary Stack | Django, PostgreSQL, Celery, Redis |
| Architecture | Modular monolith, shared database, shared schema |
| Security Classification | Critical architecture document |
| Applies To | All tenant-owned data, services, APIs, background jobs and integrations |

---

# 1. Purpose

This document defines the multi-tenancy architecture for the UAE ERP SaaS platform.

It establishes how the application will isolate data and operations belonging to different customer organizations while allowing the platform to operate from a shared application deployment and PostgreSQL database.

The architecture must support:

- Multiple customer organizations within one SaaS deployment.
- Multiple users belonging to the same organization.
- Users who are members of multiple organizations.
- Multiple legal entities and branches within an organization.
- Independent module subscriptions and entitlements.
- Organization-specific financial, tax, accounting and operational data.
- Tenant-aware background processing and scheduled jobs.
- Secure document storage, exports, integrations and reporting.
- Auditable platform administration and controlled support access.
- Future scaling without requiring an immediate migration to a database-per-tenant model.

**Core principle: A user must never access another tenant's data merely because they know, guess or manipulate a record identifier.**

Tenant isolation must be enforced through multiple independent controls. It must not depend exclusively on developers remembering to add a tenant filter to every query.

# 2. Architectural Decision

## 2.1 Selected architecture

The initial production architecture will use:

- One Django application codebase.
- One shared PostgreSQL database.
- One shared PostgreSQL schema for application tables.
- A `tenant_id` column on tenant-owned business records.
- Django middleware for authentication and active-tenant resolution.
- Membership-based authorization.
- Tenant-aware application services and data access.
- PostgreSQL Row-Level Security (RLS) as defense in depth.
- Database constraints to prevent invalid cross-tenant relationships.
- Explicit tenant context propagation into Celery tasks.
- Tenant-scoped storage, downloads and integrations.
- Automated cross-tenant isolation tests.

This is a shared-schema, row-level multi-tenancy model.

### Logical architecture

```text
                    SaaS Platform
                          |
              +-----------+-----------+
              |                       |
          Tenant A                 Tenant B
              |                       |
       Tenant A Users           Tenant B Users
              |                       |
              +-----------+-----------+
                          |
                  Django Application
                          |
             Authentication and Membership
                          |
                 Active Tenant Context
                          |
             Tenant-Aware Service Layer
                          |
                 PostgreSQL Database
                          |
                 Row-Level Security
                          |
              Tenant-Scoped Business Data
```

The application and database are shared, but customer data access is restricted by tenant.

## 2.2 Why shared-schema multi-tenancy?

The initial design is appropriate for a modular ERP SaaS because it provides:

1. Lower operational complexity than maintaining a separate database for every customer.
2. Centralized migrations and application upgrades.
3. Efficient use of database connections and infrastructure.
4. A consistent subscription and module-entitlement system.
5. Easier consolidated platform monitoring.
6. A practical starting point for small and medium-sized UAE businesses.

However, shared-schema multi-tenancy introduces a critical requirement: every tenant-owned data access path must enforce isolation correctly.

A database-per-tenant or schema-per-tenant architecture may be considered later for customers requiring stronger physical separation, dedicated infrastructure or specific contractual arrangements. That is a future architectural decision, not a requirement for the initial implementation.

# 3. Terminology and Domain Boundaries

The following concepts must remain distinct.

## 3.1 Tenant

A tenant represents a customer organization using the SaaS platform.

Examples:

- A trading company.
- A technology services company.
- A retail business.
- A professional services firm.

A tenant owns its users' organizational membership, subscriptions, business configuration and tenant-scoped operational data.

Suggested model:

`tenants.Tenant`

## 3.2 User

A user is an authenticated identity.

A user is not automatically a tenant.

One user may belong to multiple tenants, subject to the access granted by each organization.

For example, an accountant may have access to several customer organizations. Access to one organization must not imply access to another.

Suggested model:

`users.User`

## 3.3 Tenant membership

Membership connects a user to a tenant and defines their organizational role and access status.

Suggested model:

`tenants.TenantMembership`

A membership may contain:

- Tenant.
- User.
- Membership status.
- Organization-level role.
- Invitation status.
- Joined timestamp.
- Revocation timestamp.
- Created and updated timestamps.

Membership status should use controlled values such as:

- INVITED
- ACTIVE
- SUSPENDED
- REVOKED

A revoked or suspended membership must not authorize business-data access.

## 3.4 Legal entity

A legal entity represents a legally distinct business within a tenant.

A tenant may contain one or more legal entities, depending on its business structure and commercial plan.

Examples:

- A holding organization with several subsidiaries.
- A group operating multiple registered companies.
- A business maintaining separate legal entities for different activities.

Suggested model:

`tenants.LegalEntity`

Legal entities may have their own:

- Registered business names.
- Tax registrations.
- VAT configurations.
- Corporate tax profiles.
- Accounting books.
- Invoice numbering sequences.
- Financial reporting requirements.

Legal-entity boundaries must be enforced separately from tenant boundaries.

**A legal entity is not a tenant.** Multiple legal entities can belong to one tenant, while separate tenants must remain isolated even if they share an accountant or service provider.

## 3.5 Branch

A branch represents an operational location within a legal entity.

Examples include offices, warehouses, retail outlets and operating locations.

Suggested model:

`tenants.Branch`

A branch may be used to scope transactions, inventory, reporting and operational permissions.

## 3.6 Platform operator

A platform operator is an authorized person or service responsible for operating the SaaS platform.

Platform operators may need access to tenant metadata for:

- Subscription support.
- Tenant provisioning.
- Operational troubleshooting.
- Service health monitoring.
- Customer support.

Platform-operator privileges must not automatically grant unrestricted access to customer financial or personal data.

Any exceptional customer-data access must follow an explicit, auditable support-access process.

# 4. Security Principles

Every implementation must follow these principles.

## 4.1 Deny by default

If the active tenant cannot be established, tenant-scoped business-data access must fail.

The application must never silently fall back to:

- All tenants.
- The first available tenant.
- A default customer.
- A previously selected tenant.
- A tenant identifier supplied by an untrusted request.

## 4.2 Tenant context is not authorization

Knowing a tenant UUID does not establish permission to access that tenant.

Authorization requires, at minimum:

1. An authenticated user or explicitly authorized service identity.
2. A valid tenant.
3. An active membership or an approved service authorization.
4. Permission to perform the requested operation.
5. Access to the requested module.
6. Satisfaction of module dependencies.
7. Any applicable legal-entity, branch or record-level restrictions.

The effective authorization rule is:

```text
ACCESS ALLOWED =
    Valid Identity
    AND Valid Tenant Context
    AND Active Membership or Authorized Service Identity
    AND Required Permission
    AND Required Module Entitlement
    AND Satisfied Module Dependencies
    AND Applicable Business-Scope Restrictions
```

## 4.3 Multiple independent controls

Tenant isolation must be enforced at several layers:

| Layer | Responsibility |
|---|---|
| Authentication | Establish the user or service identity |
| Membership | Establish organizational access |
| Request middleware | Resolve the active tenant |
| Permission layer | Authorize the operation |
| Application services | Enforce business rules and tenant ownership |
| ORM/data access | Scope queries to the active tenant |
| PostgreSQL RLS | Restrict rows available to the application database role |
| Database constraints | Prevent invalid cross-tenant relationships |
| Storage layer | Restrict access to tenant-owned files |
| Task processing | Preserve and revalidate tenant context |
| Audit system | Record sensitive access and administrative actions |
| Automated tests | Detect isolation failures and regressions |

No single layer replaces the others.

# 5. Tenant Identification and Resolution

## 5.1 Tenant selection

The platform must support an explicit active-tenant selection mechanism.

For example, a user who belongs to two organizations may select the organization they intend to work in after signing in.

Possible URL structures include:

```text
/app/<tenant-slug>/dashboard/
```

or:

```text
/api/v1/tenants/<tenant-uuid>/invoices/
```

The URL format is not itself a security control.

The application must validate the selected tenant against the authenticated user's active memberships.

## 5.2 Never trust client-supplied tenant identifiers

A tenant UUID supplied through a URL, request body, query parameter or header is an identifier, not proof of authorization.

The application must not authorize a request merely because:

```python
request.data["tenant_id"]
```

matches an existing tenant.

Instead, the tenant must be resolved and verified against the authenticated principal.

Example:

```python
from rest_framework.exceptions import PermissionDenied

from apps.tenants.models import TenantMembership


def resolve_user_tenant(*, user, tenant_id):
    membership = (
        TenantMembership.objects
        .select_related("tenant")
        .filter(
            user=user,
            tenant_id=tenant_id,
            status=TenantMembership.Status.ACTIVE,
        )
        .first()
    )

    if membership is None:
        raise PermissionDenied(
            "You do not have access to this organization."
        )

    return membership.tenant
```

This example assumes the membership model uses the indicated fields and enum. Codex must adapt the implementation to the actual models and project conventions.

The active membership must be checked on every new request. Do not rely on a tenant identifier stored in a long-lived client session as the sole authorization mechanism.

## 5.3 Tenant resolution requirements

Tenant resolution must:

- Require authentication for protected tenant routes.
- Verify tenant existence and operational status.
- Verify the user's active membership.
- Reject suspended, revoked or invalid memberships.
- Validate any required legal-entity or branch context.
- Establish a trusted server-side tenant context.
- Fail closed when resolution is ambiguous.
- Avoid revealing whether an inaccessible tenant exists.
- Clear tenant context after the request or transaction.

Public routes such as login, password reset, health checks and public marketing pages may operate without a tenant context where explicitly permitted.

These exceptions must be narrowly defined.

## 5.4 Tenant slugs and identifiers

Use UUIDs for internal tenant identifiers.

A tenant may also have a human-readable slug for navigation.

Tenant slugs are not authorization credentials. They may be changed according to an explicit policy, and all access must still be validated against the authenticated principal.

Avoid using sequential integer identifiers for externally exposed tenant or financial-record identifiers where UUIDs are more appropriate.

UUIDs do not replace authorization.

# 6. Database Ownership and Tenant Columns

## 6.1 Tenant-owned models

Every tenant-owned business model must have an explicit ownership strategy.

For ordinary tenant-owned records, use a non-null `tenant_id` foreign key.

Example:

```python
import uuid

from django.db import models


class TenantOwnedModel(models.Model):
    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.PROTECT,
        db_index=True,
    )

    class Meta:
        abstract = True
```

This is a starting point, not a complete implementation of the tenancy architecture.

Codex must not blindly inherit this abstract class into every model. Some models have different ownership rules, global scope or special lifecycle requirements.

## 6.2 Tenant-owned data examples

The following data is ordinarily tenant-owned:

- Customers and leads.
- Suppliers.
- Sales orders.
- Quotations.
- Customer invoices and credit notes.
- Purchase orders.
- Goods receipts.
- Inventory movements.
- Stock balances.
- Accounting journals.
- Journal entries.
- Chart-of-account configuration.
- VAT transactions and returns.
- E-invoicing submissions and provider responses.
- Employees and payroll records.
- Projects and expenses.
- Fixed assets.
- Bank accounts and reconciliation records.
- Tenant-specific integrations.
- Tenant attachments and exports.
- Tenant audit events.
- Tenant-specific reporting configurations.

The exact ownership rule must be documented for each model in its owning Django app.

## 6.3 Platform-owned data

Some records are global platform configuration and do not belong to one tenant.

Examples may include:

- Country reference data.
- Currency reference data.
- ISO country and currency codes.
- Public system-wide reference tables.
- Software release metadata.
- Platform-level feature definitions.
- Public product catalogue definitions.
- Global module definitions.
- System configuration that is explicitly global.

Global data must be read-only or tightly controlled where appropriate.

A global table must not be used to store tenant-specific business information without an explicit design decision.

## 6.4 Tenant-specific configuration

A global definition and a tenant-specific instance must be treated as separate concepts when both are needed.

For example:

```text
Global Module Definition
          |
          +---- Tenant A Subscription
          |
          +---- Tenant B Subscription
```

Similarly:

```text
Global Currency Definition
          |
          +---- Tenant A Accounting Configuration
          |
          +---- Tenant B Accounting Configuration
```

Global reference data must not become a backdoor for exposing tenant-specific values.

## 6.5 Tenant identifier immutability

For ordinary business records, `tenant_id` must be immutable after creation.

Moving a record from one tenant to another is not a normal update operation.

If a legitimate transfer is required, it must use a separately authorized, audited migration workflow that evaluates:

- Ownership.
- Legal-entity implications.
- Financial history.
- Relationships and dependencies.
- Attachments.
- Audit history.
- External references.
- Regulatory retention.
- Subscription and entitlement requirements.

Do not implement cross-tenant transfer as a generic editable tenant field.

# 7. Django Application Architecture

## 7.1 Standard tenant context

The request should expose a validated tenant context through a clearly defined interface, for example:

```python
request.tenant
request.tenant_membership
request.legal_entity
request.branch
```

The last two attributes should be optional unless the route requires them.

The application must not accept a client-provided tenant object as trusted context.

## 7.2 Middleware responsibilities

Tenant middleware should:

1. Run after authentication middleware.
2. Identify whether the request requires tenant context.
3. Resolve the tenant from the supported routing mechanism.
4. Validate the user's membership.
5. Establish the request's trusted tenant context.
6. Reject invalid tenant selections.
7. Avoid retaining tenant context across requests.

Middleware should not contain complex accounting, subscription or domain logic.

A recommended processing sequence is:

```text
Request
  |
  v
Security and Session Middleware
  |
  v
Authentication Middleware
  |
  v
Tenant Resolution
  |
  v
Membership Validation
  |
  v
Permission and Entitlement Checks
  |
  v
Tenant-Aware Application Service
  |
  v
Database Transaction and RLS Context
  |
  v
Response
```

The exact middleware order must be verified against the selected authentication implementation.

## 7.3 Application-service enforcement

Tenant-scoped business operations should use explicit application services.

Example:

```python
def create_customer(
    *,
    tenant,
    actor,
    name,
    email=None,
):
    """
    Create a customer within the explicitly supplied tenant.

    The caller must already have resolved and authorized the
    active tenant. This service must also enforce the applicable
    permission and business rules.
    """

    if tenant is None:
        raise ValueError("Tenant context is required.")

    # Perform authorization and business validation here.

    return Customer.objects.create(
        tenant=tenant,
        name=name,
        email=email,
    )
```

The real implementation must also apply permission checks, validation, transactions, audit events and any required idempotency controls.

A service must not accept arbitrary tenant IDs from untrusted request data and treat them as authorization.

## 7.4 Avoid direct tenant-owned writes from views

Views, serializers and templates should not implement independent tenant-ownership rules.

Prefer:

```text
View or API Endpoint
        |
        v
Serializer / Form Validation
        |
        v
Application Service
        |
        v
Tenant-Aware Query and Transaction
        |
        v
Domain Model and Database Constraints
```

This structure reduces the risk that different entry points enforce inconsistent rules.

## 7.5 Tenant-aware querysets

Tenant-scoped queries should make their ownership constraints explicit.

Example:

```python
def customers_for_tenant(*, tenant):
    return Customer.objects.filter(tenant=tenant)
```

A view can then use:

```python
customers = customers_for_tenant(
    tenant=request.tenant,
)
```

For sensitive objects, retrieve records through the tenant scope:

```python
invoice = get_object_or_404(
    Invoice.objects.filter(tenant=request.tenant),
    pk=invoice_id,
)
```

Do not retrieve an unrestricted record first and then assume the caller is entitled to it.

RLS remains a separate database-level safeguard.

## 7.6 Managers and querysets

Tenant-aware model managers and custom querysets may improve consistency, but they must not be the only isolation mechanism.

Django's default manager can be bypassed by:

- Explicit alternate managers.
- Raw SQL.
- Certain bulk operations.
- Background jobs.
- Administrative code.
- Newly introduced application code.

Do not make the assumption that a custom manager automatically secures every query.

## 7.7 Raw SQL

Raw SQL against tenant-owned tables is permitted only when:

- The query has a documented purpose.
- Tenant context is established.
- Tenant isolation is enforced by the database.
- Any explicit tenant predicates are correct.
- Parameters are passed safely.
- Tests cover the query's isolation behavior.

Never concatenate untrusted values into SQL statements.

## 7.8 Django signals

Signals must not be the only mechanism responsible for tenant assignment, authorization or financial integrity.

Tenant ownership should be established explicitly in the application service that creates the record.

If signals are used for secondary effects, they must not assume that every caller has established a valid tenant context.

# 8. PostgreSQL Row-Level Security

> **Accepted decision:** ADR-004 establishes `app.current_tenant_id` as the canonical transaction-local PostgreSQL tenant-context key. All examples in this document use that key.

## 8.1 Purpose

PostgreSQL Row-Level Security provides a database-level mechanism for restricting which rows can be read or modified by a database role.

The ERP must use RLS as defense in depth for tenant-owned tables.

RLS is particularly important for protecting against:

- Missing tenant filters.
- Incorrectly scoped querysets.
- Accidental unrestricted queries.
- Some classes of application defects.
- Cross-tenant access introduced by future modules.

RLS does not replace application authorization, business validation or database constraints.

## 8.2 Runtime database role

The Django application must connect using a restricted runtime database role.

That role must not be:

- A PostgreSQL superuser.
- A role with `BYPASSRLS`.
- The owner of protected tables unless the design explicitly accounts for owner behavior.

Prefer separate roles for:

- Application runtime.
- Schema migrations.
- Controlled maintenance.
- Read-only reporting, if needed.

The migration role may require additional privileges. It must not be used for ordinary application requests.

## 8.3 RLS tenant context

The application will establish the active tenant ID as a transaction-local PostgreSQL setting.

Example SQL:

```sql
SELECT set_config(
    'app.current_tenant_id',
    '00000000-0000-0000-0000-000000000001',
    true
);
```

The third argument, `true`, makes the setting local to the current transaction.

The application must set the tenant context after entering the database transaction and before accessing tenant-owned tables.

**A tenant context must never be established through a persistent connection-level setting that can leak into a later request.**

Connection pooling makes this especially important.

## 8.4 Example RLS policy

Assume a tenant-owned table named `crm_customer`.

First enable RLS:

```sql
ALTER TABLE crm_customer
ENABLE ROW LEVEL SECURITY;
```

Force RLS for the table owner as an additional safeguard:

```sql
ALTER TABLE crm_customer
FORCE ROW LEVEL SECURITY;
```

Create a policy:

```sql
CREATE POLICY crm_customer_tenant_isolation
ON crm_customer
FOR ALL
TO app_runtime
USING (
    tenant_id = NULLIF(
        current_setting('app.current_tenant_id', true),
        ''
    )::uuid
)
WITH CHECK (
    tenant_id = NULLIF(
        current_setting('app.current_tenant_id', true),
        ''
    )::uuid
);
```

Replace `app_runtime` with the actual restricted application database role.

This example assumes `tenant_id` is a UUID.

### Policy behavior

`USING` determines which existing rows the role can access or modify.

`WITH CHECK` determines which rows may be inserted or which new row values are permitted by the policy for updates.

If the tenant context is absent, the expression evaluates to a non-matching value for a normal UUID tenant ID, so tenant rows are not accessible through this policy.

A malformed non-empty tenant setting may produce a UUID-cast error. This should fail closed rather than grant access.

The application must still reject missing tenant context before executing business operations.

## 8.5 RLS coverage

Every tenant-owned table must be evaluated for RLS coverage.

The implementation checklist must include:

- Main business tables.
- Child and detail tables.
- Join tables.
- Financial transaction tables.
- Audit tables.
- Attachment metadata.
- Integration configuration.
- Webhook delivery records.
- Background-job state stored in tenant-owned tables.
- Tenant-specific reporting data.
- Any custom tables introduced by future modules.

RLS policies must be generated and reviewed as part of the database migration process.

A migration must not silently introduce a tenant-owned table without the required ownership column, constraints and security policy.

## 8.6 RLS policy limitations

RLS does not automatically make an incorrectly designed schema safe.

In particular:

- Tables without RLS remain outside this protection.
- Database superusers and roles with `BYPASSRLS` can bypass policies.
- Table owners normally bypass RLS unless `FORCE ROW LEVEL SECURITY` is used.
- Security-definer functions may create privileged execution paths.
- A compromised application that can set arbitrary tenant context may attempt to impersonate another tenant.
- Incorrect relationships can still create integrity problems even when ordinary row access is filtered.

Therefore, RLS must be combined with restricted roles, explicit tenant authorization, composite database constraints and security testing.

The runtime application role must not be allowed to alter policies, disable RLS or perform unrestricted schema changes.

## 8.7 Important trust boundary

A custom PostgreSQL setting such as `app.current_tenant_id` is not an independent identity credential.

A database role that can execute arbitrary SQL and set this variable to any tenant UUID may be able to select another tenant's rows.

RLS based on a custom setting protects against missing filters and many accidental access paths. It does not, by itself, protect against a fully compromised application runtime with unrestricted SQL execution.

The security model must therefore also protect:

- Application credentials.
- SQL execution paths.
- Database role privileges.
- Tenant-context creation.
- Administrative access.
- Secret storage.
- Deployment and migration permissions.

# 9. Django Transaction and RLS Integration

## 9.1 Transaction requirements

Tenant context must be transaction-local.

A tenant-scoped database operation must follow this order:

1. Resolve and authorize the tenant.
2. Begin a database transaction.
3. Set the transaction-local tenant context.
4. Execute tenant-scoped database operations.
5. Commit or roll back.
6. Exit the transaction.

Do not set the RLS context outside the transaction and assume it will remain correct.

Do not rely on a prior request's database connection state.

## 9.2 Reference implementation

A possible context manager is:

```python
from contextlib import contextmanager

from django.db import connection, transaction


@contextmanager
def tenant_transaction(tenant):
    """
    Establish transaction-local PostgreSQL tenant context.

    The tenant must already have been resolved and authorized
    by the caller.
    """

    if tenant is None:
        raise ValueError("Tenant context is required.")

    with transaction.atomic():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT set_config(
                    'app.current_tenant_id',
                    %s,
                    true
                )
                """,
                [str(tenant.pk)],
            )

        yield
```

Usage:

```python
with tenant_transaction(tenant):
    customer = Customer.objects.create(
        tenant=tenant,
        name="Example Customer",
    )
```

This is a reference implementation, not a complete transaction-management framework.

Before production use, verify:

- The tenant has already been authorized.
- The context manager is compatible with nested transactions.
- The code runs on the intended database connection.
- All relevant queries occur within the transaction.
- No database operation escapes the intended transaction.
- Connection pooling and worker behavior have been tested.
- Transaction rollback and exception handling work correctly.

For PostgreSQL, the transaction-local setting is reverted when the transaction ends. Nested Django transactions normally use savepoints, so the implementation must be tested carefully to ensure context establishment and rollback behavior are correct.

## 9.3 Request and transaction boundaries

Do not assume that Django request middleware alone creates a suitable database transaction.

The implementation must deliberately define where tenant transactions begin and end.

Possible approaches include:

- Explicit application-service transactions.
- A tenant-aware transaction wrapper used by protected views.
- A carefully designed middleware and transaction integration.

Choose one documented pattern and apply it consistently.

Avoid enabling global `ATOMIC_REQUESTS` without evaluating its implications for:

- Streaming responses.
- Long-running requests.
- Database lock duration.
- Nested transactions.
- Background tasks.
- Connection utilization.

## 9.4 Tenant context cleanup

The application must not retain tenant context in:

- Module-level global variables.
- Shared mutable singleton objects.
- Long-lived worker state.
- Reusable request objects.
- Persistent thread-local state without guaranteed cleanup.
- Unscoped caches.
- Persistent database connection settings.

Request context may be stored in a well-defined request-local structure, but it must not become a cross-request authorization source.

# 10. Cross-Tenant Referential Integrity

## 10.1 The problem

Suppose an invoice belongs to Tenant A but references a customer belonging to Tenant B.

Even if both records exist, that relationship is invalid.

Filtering invoice queries alone does not prevent every such data-integrity defect.

The database must reject cross-tenant relationships wherever practical.

## 10.2 Composite foreign-key strategy

For important tenant-owned relationships, use composite uniqueness and foreign-key constraints.

For example:

```sql
ALTER TABLE crm_customer
ADD CONSTRAINT uq_customer_tenant_id
UNIQUE (tenant_id, id);
```

Then enforce the invoice-to-customer relationship:

```sql
ALTER TABLE sales_invoice
ADD CONSTRAINT fk_invoice_customer_same_tenant
FOREIGN KEY (tenant_id, customer_id)
REFERENCES crm_customer (tenant_id, id);
```

This requires both referenced columns to satisfy the appropriate unique constraint.

If the invoice's `tenant_id` belongs to Tenant A, PostgreSQL will reject a reference to a customer in Tenant B.

The exact table and constraint names must match the implemented schema.

## 10.3 Django implementation

Django supports database constraints, but composite foreign keys are not uniformly represented as ordinary `ForeignKey` fields across all supported Django versions.

The implementation team must evaluate the supported framework version and select a maintainable implementation.

Possible approaches include:

- Explicit PostgreSQL constraints in carefully managed migrations.
- Supported database features in the chosen framework version.
- A compatible schema-management strategy with migration tests.

Do not claim composite tenant foreign-key protection exists merely because both models have a `tenant` field.

The actual PostgreSQL schema must contain the relevant constraints.

## 10.4 Relationships requiring particular attention

Enforce same-tenant ownership for relationships such as:

- Invoice → Customer.
- Invoice line → Invoice.
- Invoice → Legal entity.
- Purchase order → Supplier.
- Purchase order line → Purchase order.
- Inventory movement → Product.
- Inventory movement → Warehouse.
- Journal entry → Accounting period.
- Journal line → Journal entry.
- Expense → Employee.
- Payroll record → Employee.
- Fixed asset → Legal entity.
- E-invoicing submission → Invoice.
- Attachment metadata → Parent record.
- Subscription configuration → Tenant.
- Integration configuration → Tenant.

Some relationships may involve a legal entity or branch as well as a tenant. The design must ensure the referenced legal entity or branch belongs to the same tenant.

## 10.5 Child records

A child record must not be allowed to reference a parent from another tenant.

Where practical, enforce this with composite foreign keys.

Where database constraints cannot express the complete invariant, enforce it in a transactionally safe domain service and cover it with negative tests.

For financial records, application-only validation is not an adequate substitute when a robust database constraint is feasible.

# 11. Legal-Entity and Branch Isolation

Tenant isolation is the outer boundary. Legal-entity and branch access provide additional restrictions inside a tenant.

## 11.1 Legal-entity authorization

Users may be authorized to access:

- All legal entities in a tenant.
- Selected legal entities.
- Specific branches within selected legal entities.
- Read-only financial information.
- Operational information without access to sensitive financial records.

The permission model must support these distinctions without creating inconsistent rules across modules.

## 11.2 Financial transaction ownership

Financial documents should identify the legal entity responsible for the transaction.

Examples:

- Customer invoices.
- Credit notes.
- Supplier bills.
- VAT transactions.
- Accounting journals.
- Payroll postings.
- Fixed asset transactions.

The application must validate that the selected legal entity belongs to the active tenant.

## 11.3 Branch-level scope

Branch restrictions may apply to:

- Inventory.
- Warehouses.
- Sales operations.
- Purchases.
- Employee assignments.
- Operational reporting.

A branch restriction must not be treated as a tenant boundary.

Users with tenant-wide financial reporting access may need consolidated reports across branches, while operational users may have narrower access.

These rules must be explicitly defined in the permission model.

# 12. Authentication and Authorization

## 12.1 Membership is necessary but not sufficient

An active membership permits consideration of access, not unrestricted access to every function.

A user must also have the relevant permissions.

For example:

| Role | Typical capability |
|---|---|
| Tenant Owner | Manage organization and authorized settings |
| Tenant Administrator | Manage permitted users and configuration |
| Finance Manager | Manage authorized financial operations |
| Accountant | Perform permitted accounting tasks |
| Sales Manager | Manage authorized sales activities |
| Sales Representative | Access permitted sales records |
| Inventory Manager | Manage authorized inventory operations |
| HR Manager | Access permitted HR operations |
| Employee | Access permitted self-service functions |
| Read-Only Auditor | Review authorized records without modifying them |

These are illustrative role categories. The final role model must be documented in `AUTHENTICATION_AND_PERMISSIONS.md`.

## 12.2 Object-level authorization

Permission checks must apply to the actual object being accessed.

A user authorized to view invoices must not automatically gain access to:

- All customer records.
- All legal entities.
- All branches.
- All attachments.
- All payroll information.
- All accounting configuration.

Object-level authorization must be applied before returning protected data or performing state changes.

## 12.3 API security

All tenant-scoped API endpoints must validate:

- Authentication.
- Active tenant membership.
- Required permission.
- Module entitlement.
- Record ownership.
- Legal-entity and branch scope, where applicable.
- Request validation.
- Rate limits and abuse controls, where required.

API list endpoints must use tenant-scoped querysets.

API detail endpoints must not retrieve arbitrary records and rely only on frontend restrictions.

## 12.4 HTTP status handling

Use consistent failure behavior.

For example:

- `401 Unauthorized` when authentication is required but absent or invalid.
- `403 Forbidden` when the user is authenticated but lacks permission.
- `404 Not Found` when a record is outside the authorized scope and the application intentionally avoids revealing its existence.

The exact behavior must be consistent across the application and documented in `API_STANDARDS.md`.

# 13. Tenant Provisioning

## 13.1 Provisioning workflow

Tenant creation must be performed through a controlled application service.

Recommended workflow:

```text
Provisioning Request
        |
        v
Validate Request and Identity
        |
        v
Create Tenant
        |
        v
Create Initial Legal Entity
        |
        v
Create Initial Membership
        |
        v
Initialize Default Configuration
        |
        v
Initialize Subscription State
        |
        v
Initialize Required Platform Records
        |
        v
Record Audit Events
        |
        v
Mark Provisioning Complete
```

The exact order may vary depending on the final subscription model.

## 13.2 Provisioning requirements

Provisioning must:

- Use an atomic transaction where feasible.
- Be idempotent.
- Prevent duplicate initial memberships.
- Avoid duplicate default configuration.
- Apply safe default permissions.
- Avoid enabling unpurchased commercial modules.
- Create the minimum required legal-entity structure.
- Record the actor and provisioning source.
- Support safe retries.
- Report failures without leaving a tenant falsely marked as ready.

For longer-running provisioning operations, use an explicit provisioning state machine and background jobs.

## 13.3 Tenant lifecycle

Suggested tenant states:

- PROVISIONING
- ACTIVE
- SUSPENDED
- DEACTIVATION_PENDING
- DEACTIVATED

The state model must define which operations remain available in each state.

For example, a suspended tenant might be prevented from creating new transactions while still allowing authorized billing administrators to resolve an account issue.

A deactivated tenant must not become accessible merely because an old session or tenant URL still exists.

## 13.4 Tenant deletion

Do not immediately hard-delete tenants and all associated data as a routine administrative action.

A controlled lifecycle may require:

1. Deactivation.
2. Revocation of active sessions and credentials where appropriate.
3. Suspension of scheduled jobs and integrations.
4. Assessment of financial and regulatory retention obligations.
5. Application of retention or legal-hold rules.
6. Authorized export, where applicable.
7. A documented deletion or anonymization process.
8. Verification of backup-expiry and recovery implications.

The actual process must be aligned with contractual obligations and applicable UAE law.

# 14. Module Entitlements and Tenant Isolation

The platform uses a configurable commercial module catalogue.

A tenant's subscription determines which commercial modules it may use, but subscription status does not override tenant isolation.

For every protected operation, validate both tenant access and module entitlement.

Example:

```text
Tenant A
  ├── CRM: Enabled
  ├── Sales: Enabled
  ├── Invoicing: Enabled
  └── HRMS: Not Entitled

Tenant B
  ├── CRM: Enabled
  ├── Sales: Not Entitled
  ├── Invoicing: Not Entitled
  └── HRMS: Enabled
```

Tenant A must not access HRMS because its entitlement is absent.

Tenant B must not access Tenant A's sales or invoice records even if the relevant module becomes enabled.

The entitlement engine must be enforced in the application service layer, as described in `ENTITLEMENT_ENGINE.md`.

RLS is responsible for tenant row isolation; it is not the sole mechanism for commercial module authorization.

Platform modules such as authentication and tenant management must remain available as required for core operation, independently of the customer's commercial module selection.

# 15. Background Jobs and Celery

Background tasks are a major source of accidental tenant-context leakage because they execute outside the normal HTTP request lifecycle.

## 15.1 Explicit tenant identity

Every tenant-scoped Celery task must receive an explicit tenant identifier or a reference to a tenant-owned job record.

Example:

```python
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from apps.tenants.models import Tenant


@shared_task
def process_tenant_job(tenant_id, job_id):
    try:
        tenant = Tenant.objects.get(pk=tenant_id)
    except ObjectDoesNotExist:
        return

    # Validate tenant status and job ownership.
    # Establish transaction-local RLS context.
    # Execute tenant-scoped work through application services.
    # Record success or failure.
```

This is a structural example. Production code must implement the actual job model, status transitions, retry rules, authorization policy and error handling.

## 15.2 Task requirements

Tenant-scoped jobs must:

- Carry an explicit tenant identifier.
- Revalidate that the tenant exists and is in an appropriate state.
- Establish tenant context within the worker's database transaction.
- Confirm that referenced jobs and records belong to the same tenant.
- Apply module-entitlement checks when relevant.
- Use idempotency controls where duplicate execution is possible.
- Record tenant-scoped execution outcomes.
- Clear context at transaction completion.
- Avoid reusing mutable tenant state between tasks.

## 15.3 Never infer tenant from a previous task

A Celery worker may process tasks for different tenants sequentially.

The next task must not inherit its tenant identity from the previous task.

Do not rely on:

- Global variables.
- Module-level active-tenant values.
- Unreset thread-local state.
- Persistent database settings.
- A previous task's model instance.
- Implicit tenant context captured from an unrelated request.

## 15.4 Scheduled jobs

Scheduled jobs must define their scope explicitly.

Examples:

- A task for one tenant.
- A task that enumerates eligible tenants through a privileged, controlled platform process.
- A platform maintenance task that operates only on global data.

A platform-wide job must not disable tenant protections casually.

For cross-tenant processing, the implementation should enumerate eligible tenant IDs through a controlled process and execute each tenant's work under a separate tenant context.

## 15.5 Task retries and idempotency

Retries must not produce duplicate business effects.

This is particularly important for:

- Invoice issuance.
- E-invoicing submissions.
- Payment processing.
- Accounting postings.
- Payroll processing.
- Inventory movements.
- External notifications.

Use idempotency keys, unique constraints and explicit state transitions where appropriate.

Do not assume that a Celery task executes exactly once.

# 16. Cache Isolation

Caching can bypass otherwise correct database isolation if cache keys omit tenant identity.

## 16.1 Cache-key requirements

Tenant-specific cache keys must include the tenant identifier.

Example:

```text
tenant:<tenant_uuid>:crm:customer-list:<query_hash>
```

For legal-entity-specific data:

```text
tenant:<tenant_uuid>:entity:<entity_uuid>:accounting:trial-balance:<period>
```

The actual key format may differ, but the ownership scope must be represented.

## 16.2 Data that must be scoped

Apply tenant-aware cache keys to:

- Customer and supplier lists.
- Invoice summaries.
- Dashboard metrics.
- Accounting reports.
- Inventory balances.
- Employee information.
- Tenant settings.
- Module-entitlement results.
- Permission results.
- Generated report metadata.

## 16.3 Cache invalidation

Cache invalidation must account for:

- Tenant suspension.
- Membership revocation.
- Permission changes.
- Subscription changes.
- Module entitlement changes.
- Legal-entity access changes.
- Branch access changes.
- Financial data updates.

Do not treat cached authorization decisions as permanently valid.

Use appropriate TTLs, versioning or explicit invalidation.

## 16.4 Shared cache entries

Shared cache entries are permitted only for genuinely global, non-sensitive data.

Do not place tenant-specific financial or personal information into a global cache entry.

# 17. File Storage, Attachments and Exports

Tenant isolation extends beyond PostgreSQL.

## 17.1 Storage organization

Use a tenant-scoped object-storage structure, for example:

```text
tenants/
  <tenant_uuid>/
    documents/
    invoices/
    attachments/
    exports/
    reports/
```

The path is an organizational convention, not an authorization mechanism.

The application must validate ownership before generating download links or serving files.

## 17.2 Upload requirements

Uploads must:

- Be associated with a validated tenant.
- Validate file type and size.
- Use safe filenames or generated storage keys.
- Prevent path traversal.
- Avoid trusting client-supplied storage paths.
- Apply malware scanning where appropriate to the risk and deployment.
- Restrict access to sensitive documents.
- Record relevant metadata and audit events.

## 17.3 Download requirements

Before a file can be downloaded, the application must validate:

1. The requesting identity.
2. The active tenant.
3. Ownership of the file metadata.
4. Ownership of the parent record, if applicable.
5. Required permissions.
6. Legal-entity or branch scope, where relevant.

If signed URLs are used, they must be short-lived and generated only after authorization.

A signed URL should not become a long-lived, uncontrolled public access path.

## 17.4 Export isolation

Exports must be generated using tenant-scoped data access.

A report generator must not query all invoices and filter the results only when constructing the final spreadsheet or PDF.

The tenant restriction must apply at the data retrieval stage.

Generated exports must inherit the appropriate tenant ownership and access restrictions.

Temporary files must be deleted according to a defined cleanup policy.

## 17.5 Backup and recovery

Backups contain tenant data and must be protected accordingly.

The backup process must include:

- Restricted backup credentials.
- Encryption at rest and in transit, as appropriate.
- Controlled access to backup storage.
- Retention and deletion policies.
- Recovery testing.
- Procedures for restoring the shared database.
- A documented approach for tenant-level recovery requests.

A full shared-database restore can affect every tenant. Tenant-level recovery therefore requires a separate recovery procedure that extracts or restores the relevant tenant's data and relationships safely.

# 18. Reporting and Analytics

Reports must respect the same ownership rules as transactional screens.

This applies to:

- Dashboards.
- Financial reports.
- Trial balances.
- VAT reports.
- Corporate tax workpapers.
- Inventory valuation.
- Payroll summaries.
- Business intelligence datasets.
- CSV and Excel exports.
- Scheduled reports.
- External analytics integrations.

## 18.1 Query-time scoping

Filter tenant-owned records at the query or data-access layer.

Do not rely on presentation-layer filtering.

## 18.2 Aggregation risks

Tenant isolation must apply to aggregate queries as well as individual rows.

A global aggregate can leak information even when no raw record is returned.

For example, a tenant must not be able to infer another tenant's revenue, payroll costs or customer counts from a shared dashboard endpoint.

## 18.3 Materialized views

Materialized views and summary tables must have explicit ownership rules.

Where a materialized view contains tenant-specific data, its refresh and access model must preserve tenant separation.

Do not assume that RLS on source tables automatically secures the output of every view or materialized view.

Review view ownership, execution privileges and RLS behavior for the selected PostgreSQL version.

## 18.4 Read replicas

If read replicas are introduced, verify that:

- The same security policies and schema are present.
- Application queries establish the correct tenant context.
- Read-only credentials have restricted privileges.
- Replication does not expose data through administrative interfaces.
- Cached or replicated reporting datasets retain tenant ownership.

# 19. Integrations and Webhooks

Each tenant's integration configuration must be isolated.

Examples include:

- E-invoicing service providers.
- Payment providers.
- Banking integrations.
- Email delivery.
- External CRM systems.
- Accounting exports.
- Customer-specific API connections.

## 19.1 Integration credentials

Credentials must be stored securely and associated with the correct tenant.

Do not expose raw secrets through:

- API responses.
- Application logs.
- Error pages.
- Audit event payloads.
- Admin list views.
- Exported configuration files.

Use an appropriate secret-management mechanism and encryption strategy for the deployment.

## 19.2 Webhook processing

Inbound webhooks must not be trusted to establish tenant context simply because they include a tenant UUID.

Resolve the integration configuration using a validated provider identity, webhook secret, signed request or other supported authentication mechanism.

Then establish the appropriate tenant context and verify that the referenced records belong to that tenant.

## 19.3 E-invoicing isolation

E-invoicing records and provider interactions must be scoped to the relevant tenant and legal entity.

This includes:

- Provider configuration.
- Invoice payloads.
- Submission attempts.
- Provider acknowledgements.
- Validation errors.
- Retry state.
- External identifiers.
- Credit-note relationships.
- Regulatory evidence.

The integration must use the correct legal-entity and provider configuration for the transaction.

The platform must not assume that every UAE business can use the same provider credentials or that every regulatory workflow has identical applicability.

Regulatory and provider requirements must be validated independently of tenant isolation.

# 20. Audit Logging and Support Access

## 20.1 Tenant-scoped audit events

Audit events must record relevant security and business actions.

Where appropriate, include:

- Tenant identifier.
- Actor identifier.
- Action.
- Resource type.
- Resource identifier.
- Timestamp.
- Outcome.
- Correlation identifier.
- Relevant legal entity.
- Source or execution context.
- Approved support-access reference, if applicable.

Audit payloads must avoid unnecessary personal data, credentials or sensitive financial details.

## 20.2 Cross-tenant access attempts

The platform should record significant denied access attempts, particularly:

- Attempts to access a record outside the active tenant.
- Invalid tenant selection.
- Suspicious changes to tenant context.
- Unauthorized administrative actions.
- Attempts to access protected attachments or exports.
- Repeated authorization failures.

Logging must be proportionate and must not create a secondary data-leak channel.

## 20.3 Platform support access

Support access to customer data must be explicitly controlled.

Recommended controls include:

- A dedicated support-access workflow.
- Strong authentication.
- A stated business reason.
- Approval for sensitive access where required.
- Time-limited authorization.
- Least-privilege access.
- Tenant-visible or tenant-auditable records where appropriate.
- Automatic expiration.
- Review of privileged actions.

Platform staff must not obtain unrestricted customer-data access merely by having a platform administration account.

## 20.4 Django admin

Django admin must be treated as a privileged application surface.

Tenant-owned model administration must:

- Scope list and detail access appropriately.
- Validate tenant ownership on writes.
- Enforce permissions.
- Avoid unrestricted bulk actions.
- Avoid exposing all tenants' records to ordinary staff.
- Log sensitive administrative operations.

A custom admin interface may be necessary where the standard Django admin cannot express the required security model cleanly.

---

# 21. Superusers and Privileged Operations

Django's `is_superuser` flag must not be treated as an automatic exemption from the application's tenant-security requirements.

The architecture must distinguish between:

- A tenant administrator.
- An application support operator.
- A deployment or migration operator.
- A controlled data-recovery process.

## 21.1 Runtime behavior

Normal application requests must use the restricted runtime database role, even when the authenticated application user has elevated Django permissions.

Database superuser credentials must never be used by ordinary web requests or Celery tasks.

## 21.2 Cross-tenant administrative operations

When an authorized platform operator must inspect or modify tenant data:

1. Validate the operator's platform-level permission.
2. Establish the intended target tenant explicitly.
3. Require a documented purpose where appropriate.
4. Use a controlled tenant-scoped execution path.
5. Record the action in the audit system.
6. Restrict the operation to the minimum required scope.
7. Avoid bypassing RLS unless a separately approved maintenance procedure requires it.

## 21.3 Database maintenance

Certain maintenance operations may require elevated database access.

Such operations must use dedicated credentials, controlled execution environments and auditable procedures.

They must not become normal application behavior.

Any temporary RLS bypass must be explicitly approved, limited in scope and followed by verification that normal protections are restored.

---

# 22. Tenant Context in Tests and Development

## 22.1 Test isolation

Automated tests must verify that tenant context is established correctly.

Tests must not rely exclusively on manually adding `tenant_id` filters to querysets.

They must exercise the actual middleware, application-service and database-security paths.

## 22.2 Test database role

Where practical, RLS tests must use a database role with the same relevant restrictions as the production application role.

Running all isolation tests as a PostgreSQL superuser can create false confidence because superusers bypass RLS.

## 22.3 Fixtures and factories

Test factories must explicitly create:

- Tenant A.
- Tenant B.
- Users for each tenant.
- Memberships.
- Tenant-owned records for each tenant.
- Legal entities and branches, where required.

Avoid fixtures that silently create tenantless business records when the production model requires a tenant.

## 22.4 Test isolation

Tests that establish PostgreSQL tenant context must clean up through transaction boundaries.

Tests must not depend on the order in which they execute.

Test workers must not reuse stale tenant context.

## 22.5 Development convenience

Development tools may offer convenient tenant selection, but they must not weaken production isolation rules.

Do not disable RLS in development and then assume production behavior has been tested.

Where RLS is temporarily unavailable in a lightweight local environment, the limitation must be explicit and a dedicated PostgreSQL integration-test environment must validate the production policy.

---

# 23. Required Security Test Scenarios

The following scenarios are mandatory acceptance requirements.

| ID | Scenario | Expected result |
|---|---|---|
| MT-001 | Tenant A user requests Tenant A customer | Allowed when permissions permit |
| MT-002 | Tenant A user requests Tenant B customer by UUID | Denied or returned as not found |
| MT-003 | Tenant A user submits Tenant B customer ID while creating an invoice | Rejected |
| MT-004 | Tenant A user attempts to create a record with Tenant B's tenant ID | Rejected |
| MT-005 | Tenant A user attempts to change an existing record's tenant ID | Rejected |
| MT-006 | Query executes without tenant context | Tenant rows inaccessible through RLS |
| MT-007 | Tenant A transaction establishes context, then transaction ends | Context does not leak into the next transaction |
| MT-008 | Same database connection is reused for Tenant B | Tenant B sees only authorized Tenant B data |
| MT-009 | User has memberships in Tenants A and B | Only the explicitly selected and authorized tenant is active |
| MT-010 | Membership is revoked | Subsequent protected requests are denied |
| MT-011 | Tenant is suspended | Access follows the documented suspension policy |
| MT-012 | Tenant A invoice references Tenant B customer | Database rejects the relationship |
| MT-013 | Tenant A job references Tenant B invoice | Job validation rejects the operation |
| MT-014 | Tenant A requests Tenant B attachment | Download denied |
| MT-015 | Tenant A requests a Tenant B export | Download denied |
| MT-016 | Tenant A dashboard queries financial aggregates | Results include only authorized Tenant A data |
| MT-017 | Tenant A cache is populated, then Tenant B requests equivalent data | Tenant B receives only Tenant B data |
| MT-018 | Tenant A webhook references a Tenant B record | Request rejected |
| MT-019 | Platform operator performs approved support access | Access follows the approved scope and is audited |
| MT-020 | Runtime role attempts to disable RLS | Operation denied |
| MT-021 | Runtime role is checked for superuser or `BYPASSRLS` privileges | Neither privilege is granted |
| MT-022 | Bulk update or delete executes under Tenant A context | Only permitted Tenant A rows are affected |
| MT-023 | Raw SQL accesses a protected tenant table | RLS restricts rows to the active tenant |
| MT-024 | Tenant A report includes related records | No Tenant B records or aggregates leak through joins |
| MT-025 | Celery worker processes tasks for different tenants sequentially | No tenant context leaks between tasks |
| MT-026 | Tenant provisioning is retried | Duplicate tenants or initial records are not created unintentionally |
| MT-027 | Legal entity from Tenant B is selected in Tenant A transaction | Rejected |
| MT-028 | Tenant A user attempts to access a restricted branch | Denied according to branch permissions |
| MT-029 | A newly created tenant-owned table is introduced | Migration review detects missing isolation controls |
| MT-030 | Tenant data is restored through a recovery workflow | Ownership and relationships remain valid |

Additional tests must be added when a new module introduces a new tenant-owned model, relationship, integration or access path.

---

# 24. Performance and Scalability

Multi-tenancy must not introduce avoidable query overhead or uncontrolled tenant interference.

## 24.1 Indexing

Tenant-owned tables will commonly need indexes beginning with `tenant_id`.

Examples:

```sql
CREATE INDEX idx_customer_tenant_name
ON crm_customer (tenant_id, name);
```

```sql
CREATE INDEX idx_invoice_tenant_date
ON sales_invoice (tenant_id, invoice_date);
```

These are illustrative indexes. The final index design must reflect actual query patterns, constraints and table sizes.

## 24.2 Unique constraints

Tenant-specific unique values should normally use composite uniqueness.

For example:

```sql
ALTER TABLE crm_customer
ADD CONSTRAINT uq_customer_tenant_external_code
UNIQUE (tenant_id, external_code);
```

This allows different tenants to use the same external code while preventing unintended duplicates within a tenant.

For financial document numbering, uniqueness may also need legal-entity, document-series or financial-period dimensions.

## 24.3 Query performance

The implementation must evaluate:

- Tenant-filtered query plans.
- RLS policy overhead.
- Composite index effectiveness.
- Join performance.
- Large-tenant behavior.
- Reporting and export workloads.
- Connection-pool utilization.
- Long-running transactions.
- Celery worker concurrency.

RLS must not be disabled merely to improve performance without a formal security review.

## 24.4 Noisy-neighbor controls

A single tenant must not be allowed to consume disproportionate shared resources without controls.

Potential controls include:

- Per-tenant API rate limits.
- Background-job concurrency limits.
- Export size limits.
- Request timeouts.
- Query timeouts for suitable workloads.
- Report-generation queues.
- Storage quotas.
- Tenant-level usage monitoring.

Limits should be configurable where they are part of the commercial model.

Do not introduce arbitrary hard limits that contradict a customer's subscription or contractual terms.

---

# 25. Data Protection and UAE Considerations

Tenant isolation is necessary but does not independently establish legal or regulatory compliance.

The platform must separately evaluate applicable requirements for:

- UAE Personal Data Protection Law and any applicable exclusions or special regimes.
- UAE VAT records.
- UAE Corporate Tax records.
- UAE e-invoicing.
- Employee and payroll data.
- Financial record retention.
- Data export and deletion.
- Hosting location and cross-border processing.
- Customer contractual obligations.

Applicable requirements may differ by business activity, legal entity, regulatory status and processing arrangement.

The product must not make blanket compliance claims merely because RLS or tenant isolation has been implemented.

## 25.1 Personal data

Employee, customer, supplier-contact and other personal data must be accessible only to appropriately authorized users.

HRMS and payroll require additional permission restrictions because of the sensitivity of their records.

## 25.2 Retention and deletion

Tenant deactivation must not automatically delete records that must be retained under applicable law or contract.

Retention rules must be documented and configurable where appropriate.

Deletion workflows must evaluate:

- Legal retention.
- Tax and accounting requirements.
- Regulatory obligations.
- Contractual commitments.
- Legal holds.
- Backup retention.
- Personal-data minimization obligations.

## 25.3 Regulatory configuration

Regulatory rules must be maintained separately from tenant-isolation logic.

The tenancy architecture must provide reliable ownership and access boundaries, while the accounting, VAT, corporate tax and e-invoicing modules implement their own validated regulatory requirements.

---

# 26. Database Migration and Schema Governance

## 26.1 New tenant-owned models

Before adding a new tenant-owned model, the developer must document:

- The owning Django app.
- Whether the model is tenant-owned or global.
- Its `tenant_id` strategy.
- Its legal-entity and branch relationships.
- Its unique constraints.
- Its foreign-key ownership rules.
- Its RLS policy.
- Its indexes.
- Its retention policy.
- Its access permissions.
- Its tests.

## 26.2 Migration acceptance

A migration introducing a tenant-owned table must not be considered complete until it has:

1. Added the ownership field.
2. Backfilled existing rows safely, where applicable.
3. Applied required non-null constraints.
4. Added relevant indexes and uniqueness constraints.
5. Added cross-tenant referential-integrity constraints where required.
6. Enabled and configured RLS.
7. Verified the runtime role's access behavior.
8. Added automated tests.
9. Documented any temporary migration exceptions.
10. Confirmed rollback or recovery considerations.

For an existing table, do not add a non-null tenant column without a safe backfill and validation strategy.

## 26.3 Migration role and runtime role

Database schema migrations must run using a dedicated migration identity.

The runtime application role must not receive broad schema-alteration privileges.

This separation reduces the impact of an application-level compromise and prevents ordinary business operations from modifying security policies.

## 26.4 Automated schema checks

CI should include checks that detect:

- Tenant-owned models without an ownership strategy.
- Missing RLS policies on required tables.
- Missing expected tenant indexes.
- Missing composite constraints for designated critical relationships.
- Runtime-role privilege drift.
- Unexpected migration changes affecting RLS.
- Isolation tests that fail under the restricted database role.

These checks may use custom Django system checks, migration inspection scripts, database introspection and automated tests.

They should be introduced incrementally and made mandatory for the relevant protected models.

---

# 27. Observability and Incident Response

The platform must be able to investigate suspected tenant-isolation failures.

## 27.1 Required operational signals

Monitor:

- Repeated cross-tenant access denials.
- Missing tenant-context errors.
- RLS policy violations.
- Database permission errors.
- Unexpected changes to tenant ownership.
- Failed provisioning jobs.
- Tenant-scoped task failures.
- Unauthorized attachment or export requests.
- Unusual administrative access.
- Changes to runtime database-role privileges.

## 27.2 Incident handling

If a tenant-isolation incident is suspected:

1. Follow the security incident response procedure.
2. Preserve relevant logs and audit evidence.
3. Determine the affected tenants and data types.
4. Identify the access path and timeframe.
5. Contain the affected route, task, credential or integration.
6. Assess legal and contractual notification requirements.
7. Correct the underlying defect.
8. Add regression tests.
9. Verify the fix under the production-equivalent database role.
10. Document the incident and corrective actions.

Do not assume that a successful application-level test proves the absence of a database-level isolation defect.

---

# 28. Implementation Plan

Multi-tenancy must be implemented before commercial ERP modules depend on it.

| Stage | Scope | Required output |
|---|---|---|
| P0 — Foundation | Database roles, tenant model conventions, configuration and test environment | Foundation supports safe tenant-aware development |
| P1 — Core Platform | Tenant, legal entity, branch, membership, middleware and permissions | Tenant context and identity isolation work end to end |
| P2 — Subscription Engine | Tenant subscriptions, module entitlements and subscription lifecycle | Entitlements operate independently for each tenant |
| P3 — CRM, Sales and Invoicing | Tenant-owned business records and relationships | Core commercial modules pass isolation tests |
| P4 — UAE E-Invoicing | Tenant and legal-entity scoped provider configuration and submissions | E-invoicing data and tasks are isolated |
| P5 — Accounting and VAT | Financial records, journals, VAT transactions and reports | Financial ownership and integrity controls are tested |
| P6 — Procurement and Inventory | Suppliers, warehouses, stock and procurement | Inventory relationships and operations are isolated |
| P7 — HRMS and Payroll | Employee, payroll and HR data | Sensitive employee data has additional access controls |
| P8 — Projects, Expenses and Assets | Tenant-owned projects, expenses and assets | Cross-module ownership is enforced |
| P9 — Banking and Advanced Finance | Bank connections, payments and reconciliation | Integration credentials and financial workflows are isolated |
| P10 — Reporting and Integrations | Reports, analytics, external integrations and webhooks | Derived data and integration paths preserve isolation |
| P11 — Enterprise Readiness | Administrative controls, monitoring and security hardening | Production security and operational reviews pass |
| P12 — Production Launch | Deployment, recovery, monitoring and incident readiness | Production isolation acceptance is completed |

This is a dependency map, not permission to defer basic tenant isolation until a later phase. All tenant-owned tables must follow the approved isolation model from their initial implementation.

---

# 29. Pending Architecture Decisions

The following decisions require explicit review and resolution.

| ID | Decision | Required outcome |
|---|---|---|
| MT-DEC-001 | Tenant identifier | Confirm UUID strategy and immutability |
| MT-DEC-002 | Tenant resolution | Select and document the supported URL and session model |
| MT-DEC-003 | Transaction strategy | Define the standard Django transaction and RLS-context integration |
| MT-DEC-004 | Runtime database role | Define exact privileges and prohibit superuser/BYPASSRLS access |
| MT-DEC-005 | RLS migration strategy | Define automated policy creation, verification and rollback |
| MT-DEC-006 | Composite foreign keys | Select the supported implementation approach and critical relationship coverage |
| MT-DEC-007 | Legal-entity permissions | Define access across entities and branches |
| MT-DEC-008 | Platform support access | Define approval, expiry, audit and review requirements |
| MT-DEC-009 | Tenant lifecycle | Define suspension, deactivation, deletion and recovery behavior |
| MT-DEC-010 | Tenant recovery | Define how one tenant is restored from a shared database backup |
| MT-DEC-011 | Cache isolation | Standardize tenant-scoped cache keys and invalidation |
| MT-DEC-012 | File storage | Select storage architecture and access-control implementation |
| MT-DEC-013 | Reporting | Define isolation for materialized views, analytics and exports |
| MT-DEC-014 | Background jobs | Standardize tenant context and task idempotency |
| MT-DEC-015 | Testing environment | Ensure RLS tests run under production-equivalent restricted roles |
| MT-DEC-016 | Tenant-level limits | Define usage and noisy-neighbor controls |
| MT-DEC-017 | Future dedicated tenancy | Define criteria for considering database-per-tenant or dedicated infrastructure |

Decisions must be recorded in the architecture decision records under:

`docs/01-architecture/ARCHITECTURAL_DECISIONS/`

No unresolved decision may be treated as approved merely because a developer has chosen an implementation.

---

# 30. Instructions for Codex and Development Agents

Every development agent must comply with this document.

## 30.1 Before implementing a feature

The agent must determine:

- Whether the model is tenant-owned or global.
- Which tenant owns each business record.
- Which legal entity or branch restrictions apply.
- Which permissions are required.
- Which module entitlements are required.
- Which related records must belong to the same tenant.
- Whether background processing is involved.
- Whether attachments, exports or caches are involved.
- Which RLS policies and database constraints are required.

## 30.2 During implementation

The agent must:

- Use explicit tenant-aware application services.
- Resolve tenants through trusted server-side context.
- Avoid trusting tenant IDs from client payloads.
- Scope record retrieval to the authorized tenant.
- Establish transaction-local RLS context.
- Preserve tenant context in background tasks.
- Apply database constraints to critical relationships.
- Avoid cross-tenant cache or storage paths.
- Add positive and negative authorization tests.
- Follow the established Django app boundaries.

## 30.3 Prohibited shortcuts

Agents must not:

- Disable RLS to make a test pass.
- Use a database superuser in normal application code.
- Grant `BYPASSRLS` to the runtime role.
- Add tenant ownership only at the frontend.
- Assume UUIDs provide authorization.
- Create tenant-owned models without an isolation plan.
- Use unrestricted querysets for protected records.
- Accept arbitrary tenant IDs as authorization.
- Store tenant context in shared mutable state.
- Make cross-tenant data transfers through ordinary model updates.
- Bypass database constraints without documented approval.
- Claim isolation is complete without automated evidence.

## 30.4 Required implementation evidence

For each relevant feature, the agent must provide:

1. Models and migrations changed.
2. Tenant-ownership classification.
3. RLS policies and migration evidence.
4. Database constraint changes.
5. Authorization implementation.
6. Positive and negative isolation tests.
7. Background-task or storage tests, where relevant.
8. Test commands and actual results.
9. Known limitations.
10. Confirmation that the runtime database role has the expected restrictions.

Agents must report failures honestly. A test that was not run must not be reported as passing.

---

# 31. Definition of Done

The multi-tenancy foundation is ready for production consideration only when all applicable criteria below are satisfied.

## Architecture

- [ ] Tenant, user, membership, legal entity and branch are separate concepts.
- [ ] Shared-schema multi-tenancy is documented and implemented.
- [ ] Tenant ownership is defined for every tenant-owned model.
- [ ] Global reference data is explicitly distinguished from tenant data.
- [ ] Tenant context resolution is consistent across supported entry points.

## Application security

- [ ] Protected requests require valid authentication.
- [ ] Tenant membership is verified server-side.
- [ ] Tenant IDs supplied by clients are never treated as authorization.
- [ ] Permissions and module entitlements are enforced.
- [ ] Object-level access is tenant-scoped.
- [ ] Sensitive administrative operations are controlled and audited.

## Database security

- [ ] Tenant-owned tables have the required RLS policies.
- [ ] RLS is enabled and appropriately forced on protected tables.
- [ ] Runtime credentials cannot bypass RLS.
- [ ] Transaction-local tenant context is established correctly.
- [ ] Context does not leak between transactions or requests.
- [ ] Critical cross-tenant relationships are protected by database constraints.
- [ ] Runtime credentials cannot modify security policies or perform unrestricted schema changes.

## Background processing and storage

- [ ] Celery tasks receive explicit tenant context.
- [ ] Task retries and idempotency are tested.
- [ ] Cache keys include tenant scope where required.
- [ ] Attachments and exports enforce ownership.
- [ ] Webhooks validate integration identity and tenant ownership.
- [ ] Reporting and aggregate queries preserve tenant boundaries.

## Testing and operations

- [ ] Cross-tenant isolation tests pass under a restricted database role.
- [ ] Negative tests cover manipulated IDs and invalid relationships.
- [ ] Tenant provisioning is idempotent.
- [ ] Tenant suspension and membership revocation are tested.
- [ ] Backup and tenant-recovery procedures are documented.
- [ ] Security logging and incident response procedures are defined.
- [ ] CI checks identify missing tenant-isolation controls.
- [ ] Architecture and security reviews have been completed.

**Release rule:** A feature that introduces a tenant-isolation vulnerability must not be released, even if its functional tests pass.

---

# 32. References

Use the official documentation to validate framework and database behavior during implementation.

- Django documentation: <https://docs.djangoproject.com/>
- Django database transactions: <https://docs.djangoproject.com/en/5.2/topics/db/transactions/>
- Django security guidance: <https://docs.djangoproject.com/en/5.2/topics/security/>
- PostgreSQL Row Security Policies: <https://www.postgresql.org/docs/current/ddl-rowsecurity.html>
- PostgreSQL `SET` and configuration parameters: <https://www.postgresql.org/docs/current/sql-set.html>
- PostgreSQL constraints: <https://www.postgresql.org/docs/current/ddl-constraints.html>
- Celery documentation: <https://docs.celeryq.dev/>

The project must use documentation matching the actual pinned Django, PostgreSQL and Celery versions. Do not assume that behavior in the latest documentation is identical to the deployed version.

---

# 33. Final Architectural Rule

The platform must implement tenant isolation as a system-wide invariant.

Every module, query, task, integration, export and administrative operation must preserve the same ownership boundary.

The intended security model is:

```text
Authenticated Identity
        |
        v
Validated Tenant Membership
        |
        v
Explicit Active Tenant Context
        |
        v
Permission + Module Entitlement
        |
        v
Tenant-Aware Application Service
        |
        v
Transaction-Local PostgreSQL Context
        |
        v
RLS + Database Constraints
        |
        v
Authorized Business Operation
```

No module may establish its own weaker alternative.

This architecture provides the foundation for securely extending the ERP across CRM, sales, invoicing, UAE e-invoicing, accounting, VAT, procurement, inventory, HRMS, payroll, banking and reporting.

It does not, by itself, certify regulatory compliance or eliminate every possible application-security vulnerability. Production readiness requires implementation evidence, security testing, database-role verification and formal review.
