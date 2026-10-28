# ADR-001: Modular Monolith Architecture

| Field | Details |
|---|---|
| ADR ID | ADR-001 |
| Title | Modular Monolith Architecture |
| Status | ACCEPTED |
| Decision Date | 27 October 2026 |
| Decision Owner | Product Architect / Technical Lead |
| Reviewers | Architecture, Security, Development, DevOps |
| Project | UAE ERP SaaS Platform |
| Affected Phases | P00–P12 |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DJANGO_APP_STRUCTURE.md`, `DATABASE_DESIGN.md`, `MULTI_TENANCY.md`, `MODULE_DEPENDENCIES.md`, `ENTITLEMENT_ENGINE.md`, `EVENT_AND_TASK_PROCESSING.md` |
| Supersedes | None |
| Superseded By | None |

---

## 1. Context

The UAE ERP SaaS platform will provide multiple business capabilities through a configurable module catalogue. Customers will subscribe to the modules relevant to their businesses, with access controlled by subscription entitlements, user permissions, module dependencies, and platform policies.

The planned product includes:

- Core platform and tenant management
- User management and access control
- Subscription management and SaaS billing
- CRM and sales
- Invoicing and UAE e-invoicing integration
- Accounting and VAT
- Procurement and inventory
- HRMS and payroll
- Projects, expenses, and fixed assets
- Banking and financial integrations
- Reporting and analytics
- External integrations and enterprise administration

These capabilities share important business concepts, including tenants, legal entities, users, permissions, customers, suppliers, invoices, accounting entries, subscriptions, and audit records.

Financial operations also require reliable transaction boundaries, consistent data, traceable state transitions, and recoverable integration workflows.

The architecture must support independent module development without creating unnecessary deployment complexity or compromising tenant isolation, financial integrity, or maintainability.

The platform will initially be developed using Django and PostgreSQL, with Django REST Framework used selectively, Django Templates with HTMX and Tailwind CSS for the primary interface, and Celery with Redis for asynchronous processing.

### 1.1 Problem Statement

The project needs an architecture that:

1. Supports a growing set of ERP modules.
2. Allows modules to be developed and tested with clear ownership boundaries.
3. Enforces tenant isolation and server-side authorization.
4. Supports commercial module activation and deactivation.
5. Maintains transactional consistency for financial and inventory operations.
6. Integrates with external providers without coupling the entire application to their availability.
7. Remains practical to deploy, monitor, debug, and maintain with a small development team.
8. Allows future architectural evolution when justified by measurable requirements.

### 1.2 Architectural Constraints

The following constraints inform this decision:

- Django is the primary application framework.
- PostgreSQL is the authoritative relational database.
- The initial application is operated as one deployable Django application.
- Commercial modules share platform-level services such as identity, tenant context, authorization, audit, and entitlement evaluation.
- External integrations may be unavailable, slow, or return uncertain outcomes.
- Regulatory and financial workflows require stronger integrity controls than ordinary CRUD operations.
- Development is assisted by AI coding agents, which must follow explicit architectural boundaries.

---

## 2. Decision Drivers

The selected architecture must balance the following priorities.

| Driver | Requirement |
|---|---|
| Maintainability | Keep domain responsibilities explicit and code understandable. |
| Modularity | Allow individual ERP modules to evolve without unrestricted cross-module coupling. |
| Tenant isolation | Enforce tenant boundaries across requests, jobs, services, and database operations. |
| Financial integrity | Support atomic business transactions, immutable posted records where required, and auditable corrections. |
| Development efficiency | Minimize unnecessary infrastructure and deployment overhead. |
| Operational simplicity | Make local development, deployment, backups, monitoring, and incident recovery manageable. |
| Extensibility | Permit additional ERP modules and integrations without redesigning the entire application. |
| Testability | Support unit, integration, security, and end-to-end testing. |
| Commercial flexibility | Allow module entitlements to change without deleting the customer's existing business data. |
| Scalability | Support vertical scaling and targeted optimization before introducing distributed services. |
| Regulatory adaptability | Allow UAE-specific tax and e-invoicing requirements to evolve without spreading provider-specific logic across the application. |

---

## 3. Options Considered

### Option A: Modular Monolith

A single Django application contains multiple explicitly bounded business modules.

Each module owns its domain models, application services, business rules, migrations, tests, and interfaces. Modules execute within the same application process where appropriate and initially share one PostgreSQL database.

Background workers execute asynchronous tasks using Celery and Redis.

The application is deployed as a single application release, although web processes and background workers may run as separate processes or containers.

**Advantages**

- Straightforward deployment and environment management.
- Supports database transactions across related domain operations.
- Low initial infrastructure and operational complexity.
- Easier debugging and end-to-end testing.
- Clear module boundaries without requiring network calls between internal modules.
- Suitable for a small team building a broad ERP product.
- Allows independent scaling of web and worker processes.
- Provides a path to extract services later when justified.

**Disadvantages**

- Requires discipline to prevent modules from becoming tightly coupled.
- Individual modules cannot be independently deployed as separate releases.
- A defect in shared application code can affect multiple modules.
- A single database can create contention as workload increases.
- Poorly designed synchronous operations can affect overall application responsiveness.

### Option B: Microservices Architecture

Each major business capability runs as a separately deployable service, with defined network interfaces and independently managed service boundaries.

Services communicate through APIs and/or messaging. Database ownership and distributed transaction requirements must be defined for each service.

**Advantages**

- Independent deployment and scaling of services.
- Strong process-level isolation between services.
- Independent technology choices where justified.
- Suitable for organizations with mature distributed-systems capabilities and multiple independently operating teams.

**Disadvantages**

- Requires service discovery or endpoint management, inter-service authentication, distributed tracing, and more complex observability.
- Introduces network failure modes and latency into internal workflows.
- Complicates operations spanning invoices, inventory, accounting, and other domains.
- Requires careful handling of eventual consistency, message delivery, idempotency, and reconciliation.
- Increases infrastructure and operational costs.
- Creates more deployment pipelines and failure scenarios.
- Adds complexity before the product's workload and domain boundaries are fully understood.

### Option C: Traditional Monolith Without Enforced Module Boundaries

The application is implemented as one Django codebase with relatively unrestricted imports and cross-domain model access.

**Advantages**

- Simple initial project structure.
- Low setup overhead.
- Fast for small prototypes with limited domain complexity.

**Disadvantages**

- Business logic tends to spread across views, models, signals, and unrelated applications.
- Domain ownership becomes unclear.
- Changes in one module can unintentionally affect another.
- Commercial module boundaries become harder to enforce.
- Testing and refactoring become increasingly difficult as the product grows.
- AI coding agents may introduce inconsistent implementations when boundaries are not documented.

### Option D: Separate Django Applications with Independent Deployments

Each major module is implemented as a separate Django application or project and deployed independently.

**Advantages**

- Clear separation between deployable components.
- Some independent release and scaling capabilities.
- Potentially useful when modules have substantially different operational requirements.

**Disadvantages**

- Adds service communication and deployment complexity.
- Requires explicit ownership of shared data and identity.
- Can introduce duplicated infrastructure and application services.
- Creates cross-application consistency challenges.
- Provides limited benefit when the team and workload do not justify separate deployments.

---

## 4. Decision

**Adopt a modular monolith built with Django and PostgreSQL for the initial production architecture.**

The application must be organized into explicitly bounded domain modules, with documented responsibilities, controlled dependencies, and enforceable rules for cross-module interactions.

The architecture is a modular monolith, not an unrestricted monolith and not a collection of microservices.

### 4.1 Application Structure

The Django project will contain a single primary application configuration and multiple domain-oriented Django apps.

The initial domain structure will include:

| Domain | Primary responsibility |
|---|---|
| `core` | Shared platform primitives, common utilities, health checks, and foundational abstractions. |
| `tenants` | Tenant lifecycle, tenant context, organizations, and tenant membership relationships where assigned by the approved domain model. |
| `users` | Authentication, user identity, and account lifecycle. |
| `audit` | Audit-event recording and access to audit evidence. |
| `subscriptions` | Module catalogue, subscriptions, module selections, entitlement evaluation, and entitlement lifecycle. |
| `billing` | SaaS subscription charges, payment records, and billing workflows. |
| `crm` | Customer relationship management and CRM-owned records. |
| `sales` | Sales workflows, quotations, and order-related business operations. |
| `invoicing` | Commercial invoices, credit notes, numbering, and invoice lifecycle. |
| `e_invoicing` | External e-invoicing provider adapters, submissions, acknowledgements, and reconciliation. |
| `accounting` | Chart of accounts, journals, ledger entries, posting, and accounting periods. |
| `vat` | VAT configuration, tax calculations, and VAT reporting support. |
| `procurement` | Supplier purchasing, purchase orders, and procurement workflows. |
| `inventory` | Stock locations, stock movements, inventory balances, and valuation interfaces. |
| `hrms` | Employee records and HR administration. |
| `payroll` | Payroll calculations, payroll periods, and payroll processing. |
| `projects` | Project planning, assignments, and project status. |
| `expenses` | Expense claims, approvals, and expense processing. |
| `fixed_assets` | Asset registers, depreciation, disposal, and asset accounting integration. |
| `banking` | Bank accounts, statement imports, and reconciliation workflows. |
| `reporting` | Reporting and analytical read models. |
| `integrations` | Shared integration infrastructure and integration registry where appropriate. |

The final ownership of shared entities must remain consistent with `DJANGO_APP_STRUCTURE.md` and `DATABASE_DESIGN.md`. The table above establishes domain boundaries, not permission for every app to access every other app's models directly.

### 4.2 Database Strategy

The initial architecture will use:

- One PostgreSQL database deployment.
- One application database and schema strategy as defined in `DATABASE_DESIGN.md`.
- Shared-schema multi-tenancy unless an approved ADR changes that decision.
- Tenant identifiers on tenant-owned business records.
- Explicit tenant-aware application services and data-access rules.
- Database constraints and transaction boundaries for critical business invariants.
- PostgreSQL Row-Level Security as defense-in-depth where specified by the approved multi-tenancy design.

A shared database does not mean unrestricted data access. Every tenant-owned operation must enforce tenant scope, including background jobs, administrative tools, reporting, and integration callbacks.

### 4.3 Module Boundaries

Each module must have:

1. A documented business responsibility.
2. Clear ownership of its domain models and data.
3. Application services for important business operations.
4. Validated state transitions.
5. Tenant-aware data-access behavior.
6. Explicit dependencies on other modules.
7. Tests for its business rules and security boundaries.
8. Documented integration points.
9. Migrations owned and maintained with the module.
10. A defined entitlement relationship when the module is commercial.

A module must not bypass another module's business rules by directly modifying its internal records.

### 4.4 Cross-Module Communication

Modules should communicate through explicit interfaces.

Preferred mechanisms are:

1. Application-service calls for synchronous operations requiring immediate results.
2. Domain-owned selectors or query interfaces for permitted read operations.
3. Internal events and asynchronous tasks for workflows that can safely execute asynchronously.
4. Provider adapters for external systems.

Direct imports of another module's private implementation details are discouraged and must be justified.

Cross-module dependencies must be recorded in `MODULE_DEPENDENCIES.md`.

Circular dependencies are prohibited. If two modules require mutual access, the design must be refactored around clearer ownership, a shared contract, or an explicit orchestration service.

### 4.5 Transaction Boundaries

Business operations must use explicit transaction boundaries appropriate to their integrity requirements.

Examples include:

- Issuing an invoice and committing its business state.
- Posting a balanced accounting journal.
- Recording a stock movement and updating the corresponding inventory state.
- Activating a subscription and updating its module entitlements.
- Recording an external operation and its durable intent for asynchronous processing.

Operations that must be atomic within PostgreSQL should use database transactions and appropriate constraints.

External network calls must not be treated as part of a PostgreSQL transaction that can roll back the remote side effect. Where reliable asynchronous delivery is required, use the documented outbox, idempotency, retry, and reconciliation patterns.

### 4.6 Deployment Model

The application will initially be released as one Django application version.

The production deployment may run separate processes or containers for:

- Django web requests through Gunicorn.
- Celery workers.
- Celery beat or an equivalent scheduler.
- PostgreSQL.
- Redis.
- Nginx or an equivalent reverse proxy.
- Monitoring, logging, and backup components.

These are operational process boundaries, not automatically independent business microservices.

Web and worker processes must use compatible application versions and database schemas during deployment. Schema migrations must follow a controlled process that considers active workers and rollback limitations.

### 4.7 Module Entitlements

Commercial modules must be activated through the central entitlement engine.

A module's presence in the codebase does not mean it is commercially available or accessible to a customer.

Access must consider:

- Tenant status.
- Subscription status and applicable grace-period policy.
- Module lifecycle and sellability.
- Selected subscription modules.
- Required module dependencies.
- User permissions.
- Object-level scope.
- Applicable business rules and platform policies.

Disabling a commercial entitlement must not automatically delete the module's historical business records.

### 4.8 External Integrations

External providers must be accessed through explicit adapters and integration contracts.

Provider-specific request formats, authentication, callbacks, retry rules, and response mapping must not be spread throughout unrelated business modules.

The e-invoicing integration must support the approved UAE regulatory framework and selected provider requirements. This ADR does not certify regulatory compliance or select an accredited provider.

---

## 5. Architectural Rules

The following rules are mandatory once this ADR is accepted.

### Rule 1: Domain Ownership

Each business entity has one authoritative owning module.

Other modules must not independently redefine the entity's authoritative state.

### Rule 2: No Unrestricted Cross-Module Writes

A module must not directly modify another module's records while bypassing the owning module's validation, permissions, or state-transition logic.

### Rule 3: Explicit Service Interfaces

Important business operations must be implemented through documented application-service interfaces rather than scattered across templates, views, signals, and tasks.

### Rule 4: Tenant Context Is Mandatory

Tenant-owned data access must use validated tenant context. The active tenant cannot be trusted merely because a client supplied a tenant identifier.

### Rule 5: Authorization Is Server-Side

UI visibility is not authorization. Views, API endpoints, services, background jobs, and administrative operations must enforce the applicable permissions and entitlements.

### Rule 6: Financial Integrity Is Enforced

Financial records must use appropriate decimal precision, database constraints, transaction boundaries, audit trails, and controlled correction or reversal procedures.

Posted accounting entries must not be silently rewritten to conceal or erase their financial history.

### Rule 7: No Hidden Business Workflows

Important business operations must not depend exclusively on implicit model signals or undocumented side effects.

Signals may support suitable framework-level behavior, but core financial and regulatory workflows require explicit orchestration and testable service contracts.

### Rule 8: External Effects Must Be Recoverable

External operations must account for timeouts, duplicate requests, uncertain outcomes, provider rejections, and delayed callbacks.

Use idempotency, durable operation records, bounded retries, and reconciliation where appropriate.

### Rule 9: No Premature Microservices

Do not split a module into a separately deployed service merely to achieve conceptual modularity.

Service extraction requires a documented ADR supported by measurable operational, organizational, security, or scaling needs.

### Rule 10: Architecture Changes Require Review

AI coding agents and developers must not silently weaken these rules. Material changes require an ADR or an explicitly approved revision process.

---

## 6. Rationale

The modular monolith is the preferred initial architecture because it balances the ERP's domain complexity with the practical needs of early development and production operation.

### 6.1 Domain Modularity Without Distributed-System Overhead

ERP modules have different responsibilities, but many operations cross domain boundaries.

For example, an invoicing workflow may involve customer information, tax calculation, invoice issuance, accounting posting, and e-invoicing submission.

Keeping these capabilities within one application allows synchronous application-service calls and PostgreSQL transactions where appropriate. External operations can remain asynchronous and recoverable.

This avoids introducing network boundaries before the business workflows and ownership rules are sufficiently mature.

### 6.2 Efficient Development

A single deployable application reduces the number of repositories, runtime configurations, deployment pipelines, service endpoints, and operational failure modes that must be managed.

This is especially useful while the module catalogue, commercial packaging, and UAE-specific workflows are still being implemented and validated.

### 6.3 Controlled Future Evolution

A modular monolith does not prohibit microservices indefinitely.

If a domain develops a genuinely different scaling profile, security boundary, deployment cadence, or operational ownership model, its extraction can be evaluated using production evidence and a dedicated ADR.

Good domain boundaries established now reduce the cost of that future decision.

---

## 7. Consequences

### 7.1 Positive Consequences

- A unified application architecture.
- Lower initial infrastructure complexity.
- Explicit ownership of business domains.
- Easier local development and integrated testing.
- Simpler deployment and incident diagnosis.
- Support for atomic database transactions across appropriate business operations.
- Centralized enforcement of tenant context, permissions, and entitlements.
- A controlled path for future service extraction.

### 7.2 Negative Consequences

- Internal module boundaries require active governance.
- A shared application release can make unrelated modules part of the same release cycle.
- A single database may become a contention point.
- Incorrectly designed cross-module calls can create hidden coupling.
- A shared runtime may allow resource-intensive operations to affect other workloads unless resource limits and worker separation are configured.

### 7.3 Mitigations

| Risk | Mitigation |
|---|---|
| Modules become tightly coupled | Enforce domain ownership, dependency documentation, and import rules. |
| Cross-tenant data exposure | Tenant-aware services, authorization checks, RLS where approved, and isolation tests. |
| Slow background workloads affect web requests | Separate web and worker processes, use bounded queues, and monitor resource usage. |
| Database contention | Measure query latency and connection usage; optimize indexes and transactions before considering architectural changes. |
| Failed external operations | Durable operation records, idempotency, retries, and reconciliation. |
| Uncontrolled architectural changes by AI agents | Root `AGENTS.md` governance, accepted ADRs, code review, and automated checks. |
| Difficult future extraction | Maintain explicit domain ownership and minimize reliance on private cross-module implementation details. |

---

## 8. Security and Tenant Isolation

The modular monolith does not itself guarantee security or tenant isolation.

The following requirements remain mandatory:

1. Every request must establish and validate the user's active tenant context.
2. Every tenant-owned read and write must enforce the relevant tenant scope.
3. User permissions and module entitlements must be evaluated server-side.
4. Background tasks must establish tenant context explicitly and validate resource ownership.
5. Platform administration and customer administration must remain separate privilege boundaries.
6. Database access must use appropriately restricted credentials.
7. PostgreSQL RLS, when enabled, must be configured and tested so pooled connections cannot retain another request's tenant context.
8. Cross-tenant isolation must be tested through HTTP requests, service calls, APIs, exports, reporting, and background tasks.
9. Sensitive financial, payroll, banking, and integration operations must produce appropriate audit evidence.
10. Secrets must be supplied through approved environment-specific secret-management mechanisms.

Detailed requirements remain governed by `MULTI_TENANCY.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, and `SECURITY_REQUIREMENTS.md`.

---

## 9. Data Integrity and Migration

### 9.1 Database Integrity

Business invariants must be enforced at the strongest appropriate layer.

Use a combination of:

- PostgreSQL constraints.
- Foreign-key relationships.
- Unique constraints and indexes.
- Atomic transactions.
- Concurrency-safe service logic.
- Validated state transitions.
- Idempotency controls.
- Automated tests.

Application validation alone is insufficient for invariants that must remain true under concurrent requests.

### 9.2 Migration Ownership

Each Django application owns and maintains its migrations.

Cross-app migrations must declare dependencies explicitly and must not rely on undocumented migration ordering.

Migrations affecting large tables or critical financial workflows require review for locking, runtime, rollback feasibility, and deployment sequencing.

### 9.3 Schema Evolution

Use backward-compatible schema changes when practical:

1. Introduce new fields or tables.
2. Deploy compatible application code.
3. Backfill existing data when necessary.
4. Switch reads and writes.
5. Remove obsolete structures only after compatibility is verified.

Not every migration is safely reversible. Destructive changes require backups, a recovery plan, and explicit approval.

---

## 10. Operational Impact

The modular monolith will require a controlled release process covering:

- Application builds and dependency management.
- Automated tests and security checks.
- Database migrations.
- Web and worker deployment compatibility.
- Environment-specific configuration.
- Secrets management.
- Database backups and recovery testing.
- Application and task monitoring.
- Error reporting and structured logs.
- Capacity and performance monitoring.
- Rollback and forward-fix procedures.

The application should be containerized using Docker for reproducible development and deployment.

Production topology, hosting region, availability targets, backup retention, and recovery objectives remain subject to the relevant deployment documentation and approved infrastructure decisions.

---

## 11. Conditions for Reconsideration

The modular monolith remains the default unless material evidence justifies a change.

Reconsider this decision if one or more of the following occur:

1. A domain requires independent scaling that cannot be met economically through process or worker separation.
2. A module needs a materially different security or network isolation boundary.
3. A domain requires a separate deployment cadence that cannot reasonably be achieved within the existing release model.
4. Independent teams require separately owned deployment and operational responsibilities.
5. Database contention or application resource contention remains unacceptable after targeted optimization.
6. A third-party integration requires a dedicated execution boundary because of its reliability, security, or workload characteristics.
7. Regulatory or contractual obligations require a different isolation or hosting architecture.

These conditions trigger an architectural review; they do not automatically authorize a migration to microservices.

Any proposed change must assess data ownership, consistency, service contracts, security, operational cost, migration risk, and recovery behavior.

---

## 12. Implementation Requirements

The following work must be completed to implement this decision.

| ID | Requirement | Expected Evidence |
|---|---|---|
| ADR001-IMP-001 | Establish the Django project and configuration structure. | Reviewed project structure and settings separation. |
| ADR001-IMP-002 | Establish the domain app structure. | Django applications with documented responsibilities. |
| ADR001-IMP-003 | Document module dependencies. | Updated `MODULE_DEPENDENCIES.md`. |
| ADR001-IMP-004 | Establish cross-module service conventions. | Coding standards and representative tests. |
| ADR001-IMP-005 | Establish tenant-aware data-access conventions. | Tenant isolation implementation and tests. |
| ADR001-IMP-006 | Establish transaction and state-transition conventions. | Service-layer implementation and integrity tests. |
| ADR001-IMP-007 | Establish background-task conventions. | Reviewed Celery configuration and task contracts. |
| ADR001-IMP-008 | Establish application and worker deployment. | Container configuration and deployment documentation. |
| ADR001-IMP-009 | Add automated quality gates. | CI tests, linting, security checks, and migration checks. |
| ADR001-IMP-010 | Add architecture governance to Codex instructions. | Updated root `AGENTS.md`. |

Implementation must be delivered incrementally through the approved roadmap. This ADR does not require all commercial modules to be implemented before the core platform can be tested or deployed.

---

## 13. Validation and Acceptance Criteria

The implementation satisfies this ADR when:

- [ ] The application runs as a single primary Django codebase.
- [ ] Domain modules have explicit responsibilities and documented ownership.
- [ ] Cross-module dependencies are documented.
- [ ] Circular module dependencies are prevented or detected.
- [ ] Important business operations use explicit application-service interfaces.
- [ ] Tenant isolation is enforced across requests, services, and background tasks.
- [ ] Authorization and module entitlements are checked server-side.
- [ ] Critical business invariants are enforced through transactions and database constraints where appropriate.
- [ ] Financial posting and correction workflows preserve auditability.
- [ ] External operations use appropriate idempotency and recovery mechanisms.
- [ ] Web and worker processes can be deployed and operated with compatible application versions.
- [ ] Automated tests cover representative cross-module and tenant-isolation scenarios.
- [ ] CI checks enforce the required code-quality and security controls.
- [ ] Architecture-sensitive changes are governed through ADRs.
- [ ] Deployment and recovery procedures are documented and tested to the extent required by the current phase.

Acceptance evidence must be linked to the relevant pull requests, test reports, and deployment documentation.

---

## 14. Alternatives Rejected

### Microservices as the Initial Architecture

Rejected for the initial implementation because it would introduce distributed transactions, network failure modes, independent service deployment, and additional operational overhead before the workload, organizational structure, and domain boundaries justify them.

This is not a permanent prohibition against service extraction.

### Unrestricted Traditional Monolith

Rejected because it does not provide sufficient architectural controls for a multi-tenant ERP containing financial, regulatory, subscription, and sensitive employee data.

### Independently Deployed Django Applications for Every Module

Rejected as the default because the expected benefits do not currently justify the additional deployment, data ownership, communication, and consistency complexity.

These alternatives may be reconsidered if requirements materially change.

---

## 15. References

Internal project documents:

- `docs/00-product/MASTER_PRODUCT_SPECIFICATION.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/00-product/MODULE_CATALOGUE.md`
- `docs/00-product/DEVELOPMENT_ROADMAP.md`
- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- `docs/01-architecture/DJANGO_APP_STRUCTURE.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- `docs/01-architecture/MODULE_DEPENDENCIES.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/01-architecture/ENTITLEMENT_ENGINE.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- `docs/05-quality/SECURITY_REQUIREMENTS.md`

Technical references:

- Django documentation: https://docs.djangoproject.com/
- PostgreSQL documentation: https://www.postgresql.org/docs/
- Celery documentation: https://docs.celeryq.dev/

Review the current versions of technical references before implementing version-specific behavior.

---

## 16. Approval

**Current status:** ACCEPTED

- **Approved by:** Product Owner — explicit project instruction
- **Approval date:** 28 October 2026
- **Approval notes:** Accepted as the initial architecture baseline following `docs/07-project-management/ADR_STANDARDS_REVIEW.md`. Implementation still requires phase authorization.

---

## 17. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial architecture decision accepted after standards review. |

**Final architectural principle:** Maintain strong internal domain boundaries within a single deployable Django application, enforce tenant and business invariants explicitly, and introduce distributed services only when measurable requirements justify their additional complexity.
