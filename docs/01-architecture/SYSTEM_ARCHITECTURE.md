# UAE ERP SaaS — System Architecture

| Property | Value |
|---|---|
| Document ID | ARCH-001 |
| Version | 1.0 |
| Status | APPROVED — Architecture Baseline |
| Product | UAE ERP SaaS |
| Architecture Style | Modular Monolith |
| Backend | Python, Django, Django REST Framework where required |
| Database | PostgreSQL |
| Frontend | Django Templates, HTMX, Tailwind CSS |
| Background Processing | Celery and Redis |
| Application Server | Gunicorn |
| Reverse Proxy | Nginx |
| Containerization | Docker |
| Automated Testing | pytest, pytest-django |
| CI/CD | GitHub Actions |
| Primary Development Agent | OpenAI Codex |
| Parent Documents | MASTER_PRODUCT_SPECIFICATION.md, PRODUCT_REQUIREMENTS.md, MODULE_CATALOGUE.md, DEVELOPMENT_ROADMAP.md |

---

# 1. Purpose

This document defines the system architecture for the UAE ERP SaaS platform.

It establishes the technical boundaries, components, data flows, security principles, and integration patterns that all implementation phases must follow.

The document serves as the authoritative architectural reference for:

- Application structure.
- Django application boundaries.
- Multi-tenant data isolation.
- Authentication and authorization.
- Subscription and module entitlement enforcement.
- Business-domain separation.
- Financial transaction integrity.
- Background job execution.
- External integrations.
- Error handling and observability.
- Testing and deployment.
- Future architectural evolution.

Detailed implementation specifications must remain consistent with this document. Where a proposed implementation requires an architectural change, the change must be reviewed and recorded before implementation proceeds.

# 2. Architectural Objectives

The system must satisfy the following objectives.

## 2.1 Functional objectives

The platform will support configurable ERP modules, including:

- CRM.
- Sales.
- Invoicing.
- UAE e-invoicing integration.
- Accounting.
- VAT.
- Procurement.
- Inventory.
- HRMS.
- Payroll.
- Projects.
- Expenses.
- Fixed assets.
- Banking.
- Reporting.
- External integrations.

The core platform must support tenant registration, user management, subscriptions, module entitlements, billing, auditability, and administrative controls.

Customers must be able to purchase approved modules without requiring a separate deployment for each module.

## 2.2 Non-functional objectives

The architecture must support:

1. Strong tenant isolation.
2. Server-side authorization.
3. Financial correctness and traceability.
4. Configurable subscriptions and pricing.
5. Maintainable application boundaries.
6. Incremental module delivery.
7. Automated testing and continuous integration.
8. Secure handling of credentials and sensitive data.
9. Reliable background processing.
10. Recoverable deployments and database changes.
11. Measurable performance and capacity.
12. Future expansion without unnecessary architectural complexity.

## 2.3 Design philosophy

The system should be **simple enough to build and operate initially, but structured enough to grow into a substantial commercial ERP platform**.

The architecture must avoid two extremes:

- A tightly coupled Django application where every feature depends directly on every other feature.
- A premature microservices architecture that introduces unnecessary network, deployment, consistency, and operational complexity.

The initial implementation will use a modular monolith with explicit domain boundaries.

---

# 3. High-Level Architecture

## 3.1 Logical architecture

The application is divided into the following logical layers:

1. Presentation layer.
2. Application and use-case layer.
3. Domain and business-rule layer.
4. Infrastructure and integration layer.
5. Persistence layer.

Cross-cutting capabilities include authentication, authorization, tenant context, module entitlements, auditing, logging, and error handling.

```text
                         USERS
                           |
                           v
                    HTTPS / TLS
                           |
                           v
                        NGINX
                           |
                           v
                  GUNICORN / DJANGO
                           |
             +-------------+-------------+
             |                           |
             v                           v
      PRESENTATION LAYER           API LAYER
   Django Templates / HTMX      Django REST Framework
             |                           |
             +-------------+-------------+
                           |
                           v
                 APPLICATION SERVICES
                           |
           +---------------+----------------+
           |               |                |
           v               v                v
      CORE PLATFORM    ERP DOMAINS      SAAS SERVICES
      Tenants          CRM              Subscriptions
      Users            Sales            Entitlements
      Permissions      Invoicing        SaaS Billing
      Audit            Accounting       Module Registry
           |               |                |
           +---------------+----------------+
                           |
                           v
                 DOMAIN SERVICE BOUNDARIES
                           |
             +-------------+-------------+
             |                           |
             v                           v
       POSTGRESQL                   INTEGRATION LAYER
       Primary DB                   Provider Adapters
             |                      External APIs
             |                      Webhooks
             |                           |
             v                           v
       Durable Records             External Systems


                 ASYNCHRONOUS PROCESSING
                           |
                           v
                   CELERY WORKERS
                           |
                           v
                         REDIS
                    Broker / Cache
```

This diagram is a logical representation, not a requirement to deploy every component on a separate server.

The initial deployment may place several components on one host or a small number of hosts, provided that the deployment remains secure and its capacity and availability limitations are understood.

Redis must not be treated as the authoritative store for financial transactions, subscriptions, or other business records.

## 3.2 Architectural layers

| Layer | Responsibility | Examples |
|---|---|---|
| Presentation | Render pages and handle user interaction | Django Templates, HTMX |
| API | Expose controlled application interfaces | Django REST Framework |
| Application | Coordinate business use cases and transactions | Invoice issuance service |
| Domain | Enforce business invariants and state transitions | Journal posting rules |
| Infrastructure | Integrate with databases, queues, storage, and providers | Celery tasks, provider adapters |
| Persistence | Store durable business records | PostgreSQL |
| Cross-cutting | Enforce shared security and operational policies | Tenant context, audit service |

These layers are logical boundaries. They do not require every layer to be a separate Python package or deployment unit.

---

# 4. Architecture Style: Modular Monolith

## 4.1 Definition

The application will initially run as one Django project with multiple Django applications, each representing a well-defined technical or business domain.

A domain may contain:

- Models.
- Query and repository functions.
- Application services.
- Forms and serializers.
- Views and API endpoints.
- Permission policies.
- Tasks.
- Domain-specific tests.
- Templates and static assets.

The domain remains part of the same deployable application.

## 4.2 Reasons for choosing a modular monolith

This approach provides:

- Straightforward deployment.
- Transactional access to PostgreSQL.
- Easier local development.
- Lower infrastructure cost at the beginning.
- Reduced operational overhead.
- Consistent authentication and tenant context.
- Easier integration testing.
- Clearer ownership of business logic.

It also provides a future path to service extraction if a domain later requires independent scaling, release cadence, or isolation.

## 4.3 Required modularity rules

1. Each domain owns its business rules and state transitions.
2. Other domains must not bypass those rules by directly modifying another domain's internal state.
3. Cross-domain operations should use documented application-service interfaces.
4. Read-only cross-domain queries may use explicitly approved query interfaces.
5. Shared utilities must remain generic and must not become a repository for unrelated business logic.
6. Circular domain dependencies are prohibited unless an approved architecture decision explains and resolves the design.
7. Cross-domain writes must have clearly defined transaction and failure semantics.
8. Domain contracts must be covered by automated tests.

## 4.4 What not to do

Do not create:

- One enormous `models.py` containing the entire ERP.
- A generic service layer with hundreds of unrelated functions.
- A single shared model that represents every kind of business document.
- Direct database modifications that bypass domain services.
- Circular imports between business domains.
- A separate microservice for every module.
- A module that depends on another module's private implementation details.
- A configurable workflow engine before actual requirements justify one.

---

# 5. Technology Stack

The following is the approved initial stack, subject to the version-pinning decision recorded during foundation work.

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Application logic |
| Web framework | Django | Server-side application |
| API framework | Django REST Framework | API endpoints where required |
| Database | PostgreSQL | Durable relational data |
| Frontend rendering | Django Templates | Server-rendered interface |
| Dynamic interactions | HTMX | Partial page updates and interactive workflows |
| CSS | Tailwind CSS | UI styling |
| Background tasks | Celery | Asynchronous processing |
| Broker and optional cache | Redis | Task transport and selected cache workloads |
| Application server | Gunicorn | Django process serving |
| Reverse proxy | Nginx | HTTPS termination, routing, and static file serving |
| Containers | Docker | Repeatable development and deployment |
| Automated testing | pytest, pytest-django | Unit and integration tests |
| CI/CD | GitHub Actions | Automated validation and controlled releases |
| Dependency management | Approved Python dependency manager | Reproducible installations |
| Source control | Git | Version history and collaboration |

## 5.1 Technology selection rules

- Pin supported dependency versions.
- Use supported Python and Django releases selected for the deployment environment.
- Do not use development-only server configurations in production.
- Do not add a JavaScript framework unless an approved product requirement justifies it.
- Do not introduce additional infrastructure services without a documented need.
- Use supported libraries for cryptography, authentication, and financial operations rather than implementing these primitives from scratch.

## 5.2 API-first does not mean API-only

Django Templates and HTMX will be the default for the primary web interface.

Django REST Framework should be used where an API provides clear value, such as:

- External integrations.
- Mobile or separate frontend clients.
- Structured data exchange.
- Webhook endpoints.
- Selected asynchronous UI operations.

Do not create API endpoints for every page automatically.

The application-service layer must remain reusable by HTML views, API endpoints, and background tasks.

---

# 6. Django Project and Application Structure

The detailed application structure belongs in:

`docs/01-architecture/DJANGO_APP_STRUCTURE.md`

The following is the target logical structure.

```text
uae-erp-saas/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── test.py
│   │   └── production.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── celery.py
│
├── apps/
│   ├── core/
│   ├── tenants/
│   ├── users/
│   ├── audit/
│   ├── subscriptions/
│   ├── billing/
│   ├── crm/
│   ├── sales/
│   ├── invoicing/
│   ├── e_invoicing/
│   ├── accounting/
│   ├── vat/
│   ├── procurement/
│   ├── inventory/
│   ├── hrms/
│   ├── payroll/
│   ├── projects/
│   ├── expenses/
│   ├── fixed_assets/
│   ├── banking/
│   ├── reporting/
│   └── integrations/
│
├── templates/
├── static/
├── tests/
├── scripts/
├── docs/
├── orchestration/
├── manage.py
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── AGENTS.md
```

This structure is a target, not a requirement to implement every app in P0.

Applications should be introduced when their implementation phase is approved.

## 6.1 App registration and naming

- Use stable Django app labels.
- Avoid renaming apps after production migrations exist unless a migration plan is approved.
- Keep app configuration in `apps.py`.
- Keep domain URLs within their owning apps.
- Use project-level URL configuration to compose app routes.
- Keep environment-specific settings separate.
- Do not commit production secrets.

## 6.2 Model ownership

Each domain owns the lifecycle of its primary records.

Examples:

| Domain | Owns |
|---|---|
| Tenants | Tenant lifecycle and tenant configuration |
| Users | User accounts, membership, and role assignments |
| Subscriptions | Subscription state and subscription lines |
| Billing | SaaS subscription charges and payment records |
| CRM | Leads, contacts, and CRM activities |
| Sales | Quotations and sales workflow |
| Invoicing | ERP customer invoices and credit-note workflows |
| E-Invoicing | Provider submissions, provider statuses, and external references |
| Accounting | Chart of accounts, journals, ledger entries, and fiscal periods |
| VAT | Tax codes, tax rules, and supported tax calculation configuration |
| Procurement | Purchase orders and purchasing workflow |
| Inventory | Stock locations, movements, and valuation records |
| HRMS | Employee records and HR workflows |
| Payroll | Payroll runs and payroll calculations |
| Projects | Projects, tasks, and milestones |
| Expenses | Expense claims and approvals |
| Fixed Assets | Asset register and depreciation records |
| Banking | Bank statements and reconciliation records |
| Reporting | Report definitions and reporting execution |
| Integrations | Integration configuration and generic delivery records |

A domain may reference records owned by another domain, but it must not take over their lifecycle without an explicit design decision.

---

# 7. Multi-Tenant Architecture

## 7.1 Initial tenancy model

The initial implementation will use:

**Shared application, shared PostgreSQL database, shared schema, tenant-owned records identified by `tenant_id`.**

Each tenant represents a customer organization using the SaaS platform.

The architecture must be designed so that a later move to dedicated databases or isolated deployments remains possible without requiring every business rule to be rewritten.

## 7.2 Tenant-owned records

Every tenant-owned business record must be associated with a tenant directly or through a clearly documented ownership relationship.

Examples include:

- Customers.
- Suppliers.
- Products.
- Quotations.
- Invoices.
- Journal entries.
- Inventory movements.
- Employees.
- Payroll records.
- Projects.
- Expenses.
- Fixed assets.
- Bank statements.
- Reports and exports.

Global platform records, such as immutable reference data or the global module catalogue, may exist without a tenant association when that ownership model is explicitly documented.

## 7.3 Tenant context

The application must establish an authorized tenant context before performing tenant-specific business operations.

The context may be resolved from:

- The authenticated user's authorized organization selection.
- A tenant-specific subdomain, after validating the user's membership.
- An API credential associated with an authorized tenant.
- A trusted integration configuration.

A tenant identifier supplied by a client is a selector, not proof of authorization.

## 7.4 Tenant context lifecycle

For a normal authenticated request:

1. Authenticate the user.
2. Resolve the requested tenant.
3. Validate the user's membership and tenant status.
4. Establish the active tenant context.
5. Apply authorization and module entitlement checks.
6. Execute the application service.
7. Record required audit events.
8. Return a response without disclosing unauthorized records.

The exact middleware and service design belongs in `MULTI_TENANCY.md`.

## 7.5 Database query isolation

Tenant-aware data access must be consistent.

Recommended practices include:

- Tenant-scoped service methods.
- Tenant-aware query helpers.
- Explicit tenant filtering on tenant-owned querysets.
- Composite uniqueness constraints where business identifiers are tenant-specific.
- Foreign-key consistency checks where required.
- Automated tests for cross-tenant reads and writes.
- Optional PostgreSQL Row-Level Security as defense in depth.

Avoid relying exclusively on developers remembering to add `filter(tenant=request.tenant)` in every view.

The architecture must provide reusable patterns that make correct tenant scoping the default.

## 7.6 Tenant isolation requirements

The following operations must be tested for cross-tenant access:

- Direct record lookup.
- List and search endpoints.
- Create and update operations.
- Delete and archive operations.
- File downloads.
- Report generation.
- Exports.
- Background jobs.
- Webhook processing.
- Bulk imports.
- Administrative actions.

## 7.7 Background jobs

A background task must receive an explicit, validated tenant identifier or another trusted reference from which tenant ownership can be established.

The task must not rely on request-local state or thread-local context surviving after the request has ended.

Before accessing tenant-owned data, the task must:

1. Load the relevant tenant.
2. Verify the tenant's state where applicable.
3. Resolve the target record within that tenant.
4. Apply the task's authorization and business rules.
5. Record the task outcome.

## 7.8 Platform administrators

Platform administrators and customer-organization administrators are separate security roles.

Platform-level privileges must not automatically expose all customer business data without an explicit policy.

Support access, if implemented, must be authorized, limited in scope, and auditable.

---

# 8. Authentication and Authorization

Detailed rules belong in:

`docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`

## 8.1 Authentication

Authentication establishes the identity of a user or integration.

The implementation should use Django's established authentication mechanisms, supplemented by an approved authentication provider or MFA mechanism where required.

The system must define:

- Account registration.
- Login and logout.
- Password reset.
- Email verification where required.
- Session management.
- Account deactivation.
- Session expiration.
- API authentication.
- Integration credential management.

## 8.2 Authorization

Authorization determines what an authenticated identity can do.

It must account for:

1. User identity.
2. Tenant membership.
3. Tenant status.
4. Role and permissions.
5. Module entitlement.
6. Record-level access restrictions where applicable.
7. Sensitive-data access rules.
8. Business workflow state.

The frontend may hide unavailable actions, but hiding a button is not authorization.

Every protected operation must enforce its permissions on the server.

## 8.3 Authorization example

A user requesting access to an invoice must pass all relevant checks:

```text
Authenticated
    AND Active Tenant Membership
    AND Tenant Active
    AND Invoice Belongs to Active Tenant
    AND Invoicing Module Entitled
    AND User Has Required Permission
    AND Invoice Action Is Allowed in Current State
```

If any required check fails, the operation must be denied.

## 8.4 Default-deny behavior

- Unspecified permissions must not grant access.
- Disabled modules must not expose protected business operations.
- Deactivated users must not retain access through existing sessions or API credentials.
- Tenant membership revocation must take effect according to the approved session and authorization policy.
- Privileged actions must require explicit permission.

---

# 9. Module Catalogue and Entitlement Architecture

The module catalogue defines what functionality exists and whether it may be offered commercially.

The entitlement engine determines whether a tenant has access to a module.

These are separate responsibilities.

## 9.1 Module registry

The module registry should describe:

- Stable module code.
- Display name.
- Description.
- Lifecycle state.
- Whether it is commercially sellable.
- Dependencies.
- Pricing configuration reference.
- Supported capabilities.
- Compatibility or migration constraints where needed.

The global module catalogue is platform configuration, not tenant-owned business data.

## 9.2 Subscription records

The subscription domain should own:

- Subscription status.
- Subscription plan or configuration.
- Subscription period.
- Subscription line items.
- Purchased modules.
- Effective dates.
- Renewal and cancellation state.
- Approved trial or grace-period state.

SaaS billing should own the related billing documents and payment records.

The precise ownership boundary between subscriptions and billing must be documented in their respective module specifications.

## 9.3 Entitlement evaluation

The entitlement engine should expose a consistent service contract.

Conceptually:

```python
is_module_available(
    tenant=tenant,
    module_code="INVOICING",
    user=user,
    action="invoice.create",
)
```

This is an illustrative interface. The actual signature must be established in the detailed implementation specification.

The evaluation should consider:

- Module lifecycle state.
- Commercial availability.
- Tenant subscription status.
- Tenant's purchased modules.
- Effective dates.
- Required module dependencies.
- Tenant status.
- User permissions.
- Relevant action-level restrictions.

## 9.4 No scattered entitlement logic

Do not implement independent subscription checks in every view.

Business operations must use the approved entitlement service or an equivalent centralized policy interface.

## 9.5 Module dependencies

Dependencies must be declared and validated.

For example:

- E-invoicing depends on the invoicing domain and a supported integration configuration.
- VAT workflows depend on the relevant invoicing or purchasing workflows and validated tax rules.
- Accounting integrations depend on approved posting contracts.
- Payroll accounting depends on the accounting interfaces required by the supported workflow.
- Reporting must respect the availability and authorization rules of its source modules.

The final dependency graph must be validated for cycles.

Optional integrations should not be treated as mandatory module dependencies unless the approved business requirement requires them.

---

# 10. Domain Boundaries and Integration Contracts

## 10.1 Cross-domain communication

Domains within the modular monolith should communicate through explicit service interfaces.

For example:

- Sales requests invoice creation through the invoicing service.
- Invoicing requests a posting operation through the approved accounting interface when accounting integration is enabled.
- E-invoicing receives a finalized invoice reference and submits it through a provider adapter.
- Expenses request accounting treatment through the accounting integration contract.
- Inventory requests stock valuation and accounting integration through approved interfaces.

These examples describe architectural intent. The exact workflow and transaction boundary must be specified for each integration.

## 10.2 Direct model access

Not all cross-domain model access is prohibited.

Read-only references and queries may be acceptable where documented.

However, another domain must not bypass the owning domain's business rules by directly updating its internal fields or state.

For example, a sales view must not issue arbitrary updates to an issued invoice's totals.

## 10.3 Synchronous versus asynchronous operations

Use synchronous application-service calls when:

- The user requires an immediate result.
- A transaction must be completed before returning.
- The operation is short-running.
- Failure must be reported immediately.

Use asynchronous tasks when:

- The work is long-running.
- The operation involves slow external providers.
- Retry and reconciliation are required.
- The user can tolerate eventual completion.
- A scheduled execution is appropriate.

Do not move a transaction into a background task merely to avoid designing its consistency requirements.

## 10.4 Events

Domain events may be used to signal meaningful business changes.

Examples:

- Invoice issued.
- Journal entry posted.
- Subscription activated.
- Inventory receipt recorded.
- Payroll run finalized.

Events should represent facts that have already occurred, rather than commands that may or may not succeed.

If reliable delivery is required, use a transactional outbox or another explicitly designed durable delivery mechanism. Do not assume that committing a database transaction and publishing a Redis message are one atomic operation.

---

# 11. Database Architecture

The detailed schema and modelling standards belong in:

`docs/01-architecture/DATABASE_DESIGN.md`

## 11.1 Primary database

PostgreSQL is the authoritative store for application business data.

The database must preserve:

- Referential integrity.
- Unique business identifiers.
- Financial consistency.
- Tenant ownership.
- Transactional updates.
- Durable workflow state.
- Audit history where required.

## 11.2 Data modelling principles

- Use explicit foreign-key relationships.
- Add database constraints for important invariants.
- Use indexes based on expected query patterns.
- Use decimal types for financial amounts.
- Avoid using floating-point types for currency.
- Store timestamps consistently, normally in UTC.
- Keep tenant-specific configuration associated with the appropriate tenant.
- Separate transactional business records from derived reporting data.
- Use explicit status fields and validated state transitions.
- Avoid storing critical business rules only in templates or frontend code.

## 11.3 Tenant-aware constraints

When an identifier is unique only within a tenant, enforce that rule using an appropriate database constraint.

Examples may include:

- Customer codes.
- Supplier codes.
- Document numbers.
- Warehouse codes.
- Employee codes.

The exact constraint depends on the business rule and numbering model.

Where a related record must belong to the same tenant, the application must enforce that invariant, and the database should provide additional protection where a practical schema design permits it.

## 11.4 Migrations

Every schema change must use reviewed Django migrations.

Migration rules:

1. Migrations must be committed with the code that requires them.
2. Destructive migrations require explicit review.
3. Data migrations must be safe, repeatable where practical, and appropriately tested.
4. Large production migrations must be assessed for locking and execution time.
5. Rollback limitations must be documented.
6. Production migration procedures must include recovery planning.
7. Agents must not run destructive production migrations without explicit authorization.

## 11.5 Financial records

Financial documents and ledger entries must preserve their business history.

Posted or finalized financial records must not be silently overwritten.

Corrections must follow the appropriate amendment, reversal, adjustment, or credit-note workflow.

The exact behavior depends on the document type and applicable accounting rules.

## 11.6 Data retention and deletion

The system must define retention and deletion policies for:

- Tenant data.
- User accounts.
- Audit events.
- Financial documents.
- Payroll records.
- Provider submissions.
- Uploaded documents.
- Integration logs.
- Backups.

Do not implement blanket cascading deletion across financial and audit records without validating the applicable retention, legal, and business requirements.

---

# 12. Financial Transaction Architecture

Financial correctness is a core architectural requirement.

## 12.1 Transaction boundaries

Operations that update related financial records must use appropriate database transactions.

Examples include:

- Posting a journal entry and its lines.
- Finalizing an invoice and recording the associated state transition.
- Recording an inventory movement and updating its durable valuation effects.
- Finalizing a payroll run and recording its accounting integration, where applicable.
- Allocating a payment to one or more invoices.

The precise transaction boundary must be defined per use case.

## 12.2 Idempotency

An operation is idempotent when repeating the same logical request does not create unintended duplicate effects.

Idempotency controls are required where retries may occur, particularly for:

- Payment-provider events.
- E-invoicing submissions.
- Bank statement imports.
- Webhook processing.
- Background task retries.
- External API callbacks.
- Financial posting workflows.

Use durable idempotency records, unique constraints, provider identifiers, or other appropriate controls.

Do not rely solely on checking whether a button was clicked previously.

## 12.3 Concurrency

Concurrent operations must not silently corrupt financial or inventory state.

Use appropriate database constraints, row locking, atomic updates, or optimistic concurrency controls.

For example, two concurrent requests must not both finalize the same invoice or consume the same available stock without the intended consistency controls.

## 12.4 Monetary calculations

- Use decimal arithmetic.
- Define currency precision and rounding rules.
- Avoid converting monetary values to binary floating-point numbers.
- Validate line totals and document totals on the server.
- Document tax rounding behavior.
- Ensure reports use consistent financial rules.
- Test edge cases involving rounding, discounts, tax, partial payments, and reversals.

## 12.5 External systems

External provider calls must not be assumed to participate in the same PostgreSQL transaction.

For example, an e-invoicing provider may accept a request while the client experiences a timeout.

The application must represent uncertain outcomes explicitly and reconcile them before retrying when duplicate external effects are possible.

---

# 13. Background Processing Architecture

Celery will be used for approved asynchronous work.

Redis may be used as the Celery broker and for selected cache workloads.

## 13.1 Appropriate tasks

Examples include:

- Sending notifications.
- Generating large reports.
- Processing imports.
- Submitting invoices to external providers.
- Reconciling provider statuses.
- Delivering webhooks.
- Running scheduled billing operations.
- Performing selected scheduled maintenance tasks.

## 13.2 Task design rules

Each task must define:

- Input parameters.
- Tenant context requirements.
- Idempotency behavior.
- Retry policy.
- Timeout policy.
- Error handling.
- Logging requirements.
- Expected side effects.
- Completion status.
- Recovery or reconciliation procedure.

## 13.3 Task reliability

Celery delivery and execution behavior must not be treated as a guarantee that a business operation executes exactly once.

Tasks may be retried, duplicated, delayed, or interrupted.

Where duplicate execution would create financial or business damage, enforce idempotency in durable application state and database constraints.

## 13.4 Task payloads

Task payloads should contain stable identifiers and the minimum necessary data.

Prefer passing a tenant identifier and a business-record identifier rather than serializing entire model objects.

On execution, reload the relevant records and validate their state.

Do not place secrets, payment credentials, or unnecessary sensitive personal data in task payloads or logs.

## 13.5 Scheduling

Scheduled jobs must have:

- Explicit schedules.
- Documented ownership.
- Duplicate-execution controls where required.
- Monitoring.
- Failure handling.
- A recovery procedure.

The architecture must identify the scheduling mechanism and prevent unintended duplicate schedulers in production.

---

# 14. External Integration Architecture

External integrations must be isolated behind provider-specific adapters.

Examples include:

- SaaS payment providers.
- UAE e-invoicing providers.
- Banking providers.
- Email delivery.
- SMS delivery.
- Identity providers.
- External business systems.

## 14.1 Adapter pattern

A domain should depend on an internal integration contract rather than provider-specific implementation details.

Conceptually:

```text
ERP Domain
    |
    v
Internal Integration Contract
    |
    v
Provider Adapter
    |
    v
External Provider API
```

The internal contract should describe the business operation, expected result, error categories, and idempotency behavior.

The adapter translates between the internal contract and the provider's API.

## 14.2 Provider isolation

Provider-specific response structures must not spread throughout unrelated business domains.

For example, a payment provider's raw status strings should be translated into an approved internal status model.

Provider replacement should require changes primarily to the adapter and configuration, although differences in provider capabilities may still require business-level changes.

## 14.3 Credentials

- Store credentials in environment configuration or an approved secret-management system.
- Do not commit secrets.
- Do not return secrets in API responses.
- Redact credentials and tokens from logs.
- Restrict access to integration settings.
- Support credential rotation.
- Separate sandbox and production credentials.
- Define procedures for suspected credential compromise.

## 14.4 Webhooks

Webhook handlers must:

1. Verify authenticity using the provider's supported mechanism.
2. Validate the expected payload structure.
3. Reject unauthorized or malformed requests.
4. Deduplicate events where required.
5. Persist enough information for reliable processing.
6. Avoid performing long-running work inside the request.
7. Return appropriate responses.
8. Process the event using a controlled asynchronous workflow where appropriate.
9. Record processing outcomes.
10. Support investigation and recovery of failed events.

A webhook's claimed tenant identifier must not be trusted without validating its association with the authenticated provider configuration and relevant business record.

## 14.5 Integration failure handling

The integration layer must distinguish between:

- Validation errors.
- Authentication failures.
- Authorization failures.
- Rate limits.
- Provider outages.
- Timeouts.
- Permanent rejection.
- Transient failures.
- Unknown or uncertain outcomes.

Retries should be limited to errors for which retrying is appropriate.

For operations with possible external side effects, the system must reconcile uncertain results before repeating the operation when necessary.

---

# 15. Authentication, Sessions, and API Security

## 15.1 Browser sessions

For the server-rendered application, use Django's established session and CSRF protections.

The implementation must define:

- Secure cookie settings.
- Session expiration.
- Session invalidation.
- CSRF protection.
- HTTPS requirements.
- Authentication failure behavior.
- Appropriate login throttling or abuse controls.

Production cookie and transport settings must be explicitly configured.

## 15.2 API security

API endpoints must use an authentication mechanism appropriate to the client.

For browser-based session authentication, maintain CSRF protection for unsafe methods.

For machine-to-machine integrations, use an approved credential or token mechanism with explicit scopes, tenant association, expiration or rotation controls, and revocation behavior.

Do not assume that every API should use the same authentication mechanism.

## 15.3 Input validation

All untrusted input must be validated on the server.

Validation includes:

- Request parameters.
- Form submissions.
- API payloads.
- File uploads.
- Webhook payloads.
- Imported files.
- External provider responses.

Use Django forms, serializers, validators, and domain-level checks as appropriate.

Input validation does not replace authorization.

## 15.4 File uploads

Where document uploads are supported:

- Enforce file-size limits.
- Validate permitted file types.
- Do not trust client-provided MIME types alone.
- Generate safe storage names.
- Restrict access through authorization checks.
- Avoid serving untrusted uploads as executable content.
- Define malware-scanning requirements according to risk and deployment scope.
- Apply retention and deletion policies.
- Protect uploaded payroll, financial, and identity documents.

---

# 16. Frontend Architecture

## 16.1 Default interface approach

Use Django Templates for server-rendered pages, HTMX for targeted interactions, and Tailwind CSS for styling.

This approach should support:

- Administrative dashboards.
- CRM workflows.
- Forms and tables.
- Sales and invoicing screens.
- Approval workflows.
- Subscription management.
- Reports and configuration screens.

## 16.2 Frontend responsibilities

The frontend is responsible for:

- Presenting data.
- Collecting user input.
- Displaying validation errors.
- Communicating application state.
- Hiding unavailable navigation options for usability.
- Providing appropriate loading and error states.

The frontend is not responsible for enforcing security, module entitlements, financial calculations, or critical business invariants.

## 16.3 Reusable UI components

Establish shared components for:

- Navigation.
- Forms.
- Tables.
- Search and filtering.
- Pagination.
- Modal dialogs.
- Confirmation flows.
- Status indicators.
- Notifications.
- Error messages.
- Empty states.
- Loading indicators.
- Permission-aware actions.

Shared components must not introduce business logic that belongs to a domain service.

## 16.4 Accessibility and localization

The UI must follow the approved accessibility and localization requirements.

The architecture should avoid assumptions that prevent support for Arabic or right-to-left layouts if these are included in the approved roadmap.

Date, time, currency, and number formatting should be driven by explicit locale and tenant configuration rather than hardcoded strings.

---

# 17. Auditability and Logging

Audit events and application logs serve different purposes.

## 17.1 Audit events

Audit events record meaningful business or security actions.

Examples include:

- Tenant creation and deactivation.
- User role changes.
- Module activation.
- Subscription changes.
- Invoice issuance or cancellation.
- Journal posting or reversal.
- Payroll finalization.
- Privileged support access.
- Sensitive export operations.

Audit records should capture the information required to investigate an action, such as:

- Actor identity where known.
- Tenant context.
- Action type.
- Target record reference.
- Timestamp.
- Outcome.
- Correlation or request identifier where useful.

Avoid recording unnecessary sensitive values or entire financial or personal documents in audit metadata.

## 17.2 Application logs

Application logs support debugging and operational monitoring.

They should provide:

- Timestamp.
- Severity.
- Component or logger.
- Request or correlation identifier where available.
- Relevant tenant reference where appropriate.
- Error classification.
- Task or integration identifier where applicable.

Logs must not expose passwords, tokens, session identifiers, or unnecessary personal and financial information.

## 17.3 Error reporting

Unexpected errors must be observable without disclosing sensitive information to end users.

Production responses should not expose stack traces or internal configuration.

Detailed error information should be available only through appropriately protected operational systems.

---

# 18. Caching Architecture

Caching must be introduced selectively and only where correctness can be preserved.

Redis may be used for approved caching workloads.

## 18.1 Suitable uses

Potential uses include:

- Reusable reference data.
- Non-sensitive navigation metadata.
- Expensive derived values with clear invalidation rules.
- Rate-limiting counters.
- Selected short-lived operational data.

## 18.2 Cache isolation

Tenant-sensitive cache entries must include the appropriate tenant and authorization context in their cache keys.

A cache must not allow one tenant to receive another tenant's data.

Sensitive data should not be cached unless there is a clear requirement and a reviewed security design.

## 18.3 Cache correctness

- Define cache expiration.
- Define invalidation rules.
- Do not treat cache values as authoritative financial records.
- Do not rely on cached entitlements without a documented freshness and invalidation policy.
- Ensure that cache failure does not silently grant access.
- Avoid caching authorization decisions longer than the approved security policy allows.

The initial implementation should prefer correctness over aggressive caching.

---

# 19. API and Error Contract

The detailed API conventions belong in:

`docs/01-architecture/API_STANDARDS.md`

## 19.1 API principles

- Use stable URL and resource conventions.
- Validate input consistently.
- Enforce authentication and authorization.
- Use appropriate HTTP status codes.
- Document request and response schemas.
- Avoid exposing internal database details unnecessarily.
- Apply pagination to potentially large collections.
- Define filtering and sorting behavior.
- Protect sensitive endpoints with appropriate rate limits.
- Version APIs when compatibility requirements justify it.

## 19.2 Error responses

API errors should use a consistent structure.

Illustrative example:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The submitted data is invalid.",
    "details": {
      "invoice_date": [
        "The invoice date is required."
      ]
    },
    "request_id": "example-request-id"
  }
}
```

This is an example contract, not a fixed requirement to expose all fields for every error.

Responses must not disclose whether an unauthorized user can access another tenant's private records.

Error details must be appropriate to the caller and the failure type.

---

# 20. Security Architecture

Security must be incorporated into the design and implementation of every phase.

## 20.1 Core controls

- Tenant isolation.
- Server-side authorization.
- Secure authentication and session handling.
- CSRF protection for applicable browser requests.
- Secure secret storage.
- Input validation.
- Output encoding.
- Protection against unauthorized object access.
- Dependency vulnerability management.
- Secure file handling.
- Auditability of privileged actions.
- Rate limiting where appropriate.
- Safe error handling.
- Backup and recovery.
- Controlled production access.

## 20.2 Least privilege

Application users, integration credentials, background workers, deployment identities, and database roles should receive only the privileges needed for their responsibilities.

## 20.3 Secure defaults

- Deny access when required authorization cannot be established.
- Do not expose internal errors to external users.
- Do not disable security controls to make a test pass.
- Do not hardcode secrets.
- Do not bypass entitlement checks for convenience.
- Do not treat a hidden UI action as a security control.
- Do not trust external data without validation.

## 20.4 Security review triggers

A focused security review is required when changes affect:

- Authentication.
- Tenant context.
- Permission enforcement.
- Database isolation.
- External integrations.
- File access.
- Financial posting.
- Payroll or other sensitive personal data.
- Support impersonation.
- Production deployment or secrets.

---

# 21. Performance and Scalability

The initial architecture must support measured growth without unnecessary infrastructure complexity.

## 21.1 Initial performance approach

- Use PostgreSQL indexes based on observed query patterns.
- Avoid unbounded querysets and unnecessary database round trips.
- Use pagination for large collections.
- Use appropriate select-related and prefetch-related patterns.
- Move long-running operations to background processing where appropriate.
- Profile actual bottlenecks before introducing complex optimizations.
- Measure report execution and export resource usage.
- Establish baseline load tests before setting production targets.

## 21.2 Horizontal scaling

The web application should be designed to run multiple application instances without depending on process-local state for shared business correctness.

Durable shared state belongs in PostgreSQL or another explicitly selected shared service.

Sessions, caches, background tasks, and uploaded files must use an architecture compatible with the intended deployment topology.

## 21.3 Capacity assumptions

Do not invent final capacity targets before understanding the initial customer segment, expected users, transaction volume, reporting workload, and hosting budget.

Record capacity assumptions in:

`docs/06-deployment/INFRASTRUCTURE_REQUIREMENTS.md`

Review them before production launch and after significant growth.

---

# 22. Deployment Architecture

The detailed deployment design belongs in:

`docs/06-deployment/DEPLOYMENT_ARCHITECTURE.md`

## 22.1 Logical production components

The production deployment is expected to include:

- Nginx or an approved equivalent reverse proxy.
- Gunicorn serving Django.
- Django application processes.
- PostgreSQL.
- Celery workers.
- Redis where required.
- A scheduling mechanism for periodic tasks.
- Static asset delivery.
- Private media storage where applicable.
- Logging and monitoring.
- Backup and recovery mechanisms.

The exact topology depends on the approved availability, security, data-residency, and budget requirements.

## 22.2 Initial deployment option

A cost-conscious initial deployment may place the application, worker, and Redis services on one or more appropriately sized hosts, with PostgreSQL hosted separately or managed where feasible.

This is an initial option, not a fixed requirement.

Before production, evaluate:

- Failure isolation.
- Resource contention.
- Database performance.
- Backup and restore capability.
- Network exposure.
- Data residency.
- Recovery objectives.
- Expected customer load.
- Operational skills and support capacity.

## 22.3 Environment separation

Maintain distinct configurations for:

- Local development.
- Automated testing.
- Staging or pre-production.
- Production.

Production secrets and customer data must not be copied into lower environments without an explicitly approved and protected process.

## 22.4 Deployment safety

Deployments must include:

- Reproducible builds.
- Configuration validation.
- Database migration review.
- Health checks.
- Smoke tests.
- Logging and monitoring.
- Rollback or forward-recovery planning.
- Post-deployment verification.

A code rollback does not automatically reverse a database migration. Migration recovery must be designed separately.

---

# 23. Observability and Operational Reliability

The application must be observable from the initial implementation rather than only after the ERP modules are complete.

## 23.1 Health checks

Provide appropriate checks for:

- Application availability.
- Database connectivity.
- Background worker health.
- Critical dependency availability.

A health endpoint must not disclose secrets or detailed infrastructure configuration.

Separate lightweight liveness checks from deeper readiness checks where appropriate.

## 23.2 Monitoring

Monitoring should cover:

- Application errors.
- Request latency.
- Database availability and performance.
- Queue depth and task failures.
- External integration failures.
- Scheduled-task failures.
- Storage capacity.
- Resource utilization.
- Backup success.
- Recovery test results.

## 23.3 Incident response

The operational runbook must define:

- Incident severity.
- Escalation path.
- Investigation procedures.
- Communication responsibilities.
- Recovery actions.
- Evidence preservation.
- Post-incident review.

## 23.4 Recovery objectives

Recovery Point Objective (RPO) and Recovery Time Objective (RTO) must be explicitly approved based on business needs and infrastructure cost.

Do not claim a recovery objective has been met until the relevant backup, restoration, and recovery procedures have been tested.

---

# 24. Testing Architecture

The detailed testing strategy belongs in:

`docs/05-quality/TESTING_STRATEGY.md`

## 24.1 Test layers

| Layer | Purpose |
|---|---|
| Unit | Validate business rules and calculations |
| Application-service | Validate use cases and transaction behavior |
| Database integration | Validate constraints, relationships, and transaction semantics |
| API | Validate endpoint contracts, authentication, and authorization |
| UI | Validate critical user workflows |
| Tenant isolation | Detect cross-tenant data access |
| Financial integrity | Validate posting, rounding, and reconciliation |
| Integration | Validate provider adapters and failure handling |
| Idempotency | Validate safe retry and duplicate-event handling |
| Migration | Validate schema evolution |
| Security | Validate access controls and relevant security boundaries |
| Performance | Validate agreed workload and latency targets |
| Recovery | Validate backup restoration and operational procedures |

## 24.2 Required architectural tests

The project must maintain automated tests for:

- Unauthorized cross-tenant record access.
- Invalid tenant context.
- Missing or revoked tenant membership.
- Disabled or unentitled modules.
- Invalid module dependencies.
- Unauthorized financial posting.
- Duplicate financial operations.
- Concurrent state transitions.
- External integration failures.
- Background-task retries.
- Sensitive-data access controls.

## 24.3 Test data

Use synthetic or otherwise appropriately approved test data.

Do not place real customer credentials, payment details, payroll data, or sensitive business documents into source control.

---

# 25. Architecture Decision Records

Significant technical decisions must be documented under:

`docs/01-architecture/ARCHITECTURAL_DECISIONS/`

Each decision record should contain:

1. Decision identifier.
2. Title.
3. Status.
4. Context.
5. Decision.
6. Alternatives considered.
7. Rationale.
8. Consequences.
9. Security implications.
10. Operational implications.
11. Date and approver.

## 25.1 Initial decisions to record

| ADR | Decision |
|---|---|
| ADR-001 | Adopt a modular monolith |
| ADR-002 | Use shared PostgreSQL schema with tenant identifiers initially |
| ADR-003 | Establish explicit domain ownership and service contracts |
| ADR-004 | Define tenant isolation and PostgreSQL RLS |
| ADR-005 | Define authentication and authorization model |
| ADR-006 | Define module entitlement and dependency enforcement |
| ADR-007 | Use Django Templates and HTMX as the default UI architecture |
| ADR-008 | Define selective use of Django REST Framework |
| ADR-009 | Use Celery and Redis for approved asynchronous processing |
| ADR-010 | Define transactional outbox and event delivery |
| ADR-011 | Protect financial integrity and posted entries |
| ADR-012 | Define the UAE e-invoicing provider boundary |
| ADR-013 | Define monetary precision, currency and rounding |
| ADR-014 | Define UUID primary keys and tenant-aware references |
| ADR-015 | Define automated testing and CI quality gates |
| ADR-016 | Define Docker-based deployment architecture |
| ADR-017 | Define secrets and environment configuration |
| ADR-018 | Define audit logging and sensitive-data handling |
| ADR-019 | Define file and document storage |
| ADR-020 | Define API versioning and external integration contracts |

This list mirrors the canonical register in `ARCHITECTURAL_DECISIONS/README.md`. Candidate entries without files are not decisions and have no approval status. Draft ADRs remain proposals until explicit human approval is recorded.

---

# 26. Architectural Constraints for Codex

Codex must follow the constraints below.

## 26.1 General constraints

1. Read `AGENTS.md` before making changes.
2. Read the relevant product, architecture, phase, and module specifications.
3. Do not implement modules outside the approved phase.
4. Do not invent unresolved financial, regulatory, or commercial rules.
5. Do not introduce a new infrastructure dependency without a documented justification.
6. Do not introduce microservices without an approved architecture decision.
7. Do not duplicate business rules across views, serializers, and tasks.
8. Do not bypass domain services to update another domain's protected state.
9. Do not make tenant isolation dependent on frontend behavior.
10. Do not hardcode module prices or entitlement decisions across the codebase.

## 26.2 Database constraints

1. Use Django migrations for schema changes.
2. Preserve financial and audit history.
3. Avoid destructive migrations without explicit review.
4. Use database constraints for important invariants wherever practical.
5. Use decimal arithmetic for financial values.
6. Validate tenant ownership for cross-domain references.
7. Test concurrency-sensitive operations.
8. Document migration and recovery implications.

## 26.3 Integration constraints

1. Use provider adapters.
2. Keep secrets outside source control.
3. Validate external payloads.
4. Implement retries only where appropriate.
5. Make side-effecting operations idempotent where required.
6. Do not assume external calls are transactionally coupled to PostgreSQL.
7. Record relevant integration outcomes.
8. Provide a recovery path for uncertain or failed operations.

## 26.4 Verification constraints

1. Add tests for changed behavior.
2. Run the relevant test suite where the environment permits.
3. Report the actual commands executed.
4. Report failures honestly.
5. Do not fabricate successful checks.
6. Update affected documentation.
7. Identify unresolved risks and assumptions.
8. Request approval when the implementation conflicts with the architecture.

---

# 27. Architectural Evolution

The modular monolith is the initial architecture, not an irreversible commitment.

A domain may be considered for extraction into a separate service only when there is evidence of a specific need.

Potential reasons include:

- Independent scaling requirements.
- Independent release cadence.
- A clear security or operational isolation requirement.
- A separate team owning the domain.
- A measurable bottleneck that cannot be addressed adequately within the monolith.
- An external integration workload with distinct reliability requirements.

Before extraction, document:

- The business reason.
- The current bottleneck or constraint.
- Alternatives considered.
- Data ownership.
- API and event contracts.
- Transaction boundaries.
- Consistency requirements.
- Deployment and monitoring impact.
- Failure and recovery behavior.
- Migration and rollback plan.

Do not split a module into a service merely because it has a separate Django application.

---

# 28. Architecture Approval Checklist

Before P1 implementation is approved, verify the following:

## Product and domain boundaries

- [ ] Product requirements are approved.
- [ ] Module ownership is documented.
- [ ] Initial commercial scope is identified.
- [ ] Cross-domain integration contracts are documented.
- [ ] Module dependency rules are defined.

## Security

- [ ] Tenant isolation strategy is documented.
- [ ] Authentication and authorization boundaries are defined.
- [ ] Platform administration is separated from tenant administration.
- [ ] Entitlement checks are centralized.
- [ ] Sensitive-data handling principles are documented.
- [ ] Secrets-management expectations are established.

## Data and financial integrity

- [ ] Database modelling principles are approved.
- [ ] Tenant-aware uniqueness and relationships are addressed.
- [ ] Financial transaction principles are documented.
- [ ] Idempotency requirements are defined.
- [ ] Migration review rules are established.
- [ ] Audit-event requirements are documented.

## Operations

- [ ] Development and testing environments are defined.
- [ ] CI requirements are established.
- [ ] Deployment architecture has an approved initial direction.
- [ ] Logging and health-check expectations are defined.
- [ ] Backup and recovery responsibilities are identified.
- [ ] Production release controls are documented.

## Governance

- [ ] Architecture decision records are created for approved decisions.
- [ ] Open decisions are recorded with owners.
- [ ] The initial phase has clear acceptance criteria.
- [ ] Codex instructions reflect the approved architecture.
- [ ] Human approval authority is defined.

---

# 29. Final Architectural Rule

The platform must evolve through explicit, testable domain boundaries.

The governing architecture is:

**Django modular monolith + PostgreSQL + tenant-aware authorization + centralized entitlements + domain-owned business logic + durable financial transactions + controlled asynchronous processing + provider adapters + tested production operations.**

Every implementation decision must support at least one of the following:

- Correct business behavior.
- Stronger security.
- Better maintainability.
- Improved operational reliability.
- Measurable performance.
- Validated product requirements.

Complexity without a demonstrated requirement should be avoided.

Where this document leaves a material question unresolved, Codex must record the question and request a decision rather than silently inventing a permanent architectural rule.
