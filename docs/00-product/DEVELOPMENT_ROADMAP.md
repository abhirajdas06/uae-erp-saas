# UAE ERP SaaS — Development Roadmap

| Property | Value |
|---|---|
| Document ID | ROADMAP-001 |
| Version | 1.0 |
| Status | Initial Draft — Pending Approval |
| Product | UAE ERP SaaS |
| Architecture | Modular Monolith |
| Primary Framework | Django |
| Database | PostgreSQL |
| Frontend | Django Templates, HTMX, Tailwind CSS |
| Background Processing | Celery and Redis |
| Deployment | Docker, Nginx, Gunicorn |
| Testing | pytest, pytest-django |
| Development Agent | OpenAI Codex |
| Roadmap Owner | Product Owner |
| Parent Documents | MASTER_PRODUCT_SPECIFICATION.md, PRODUCT_REQUIREMENTS.md, COMMERCIAL_MODEL.md, MODULE_CATALOGUE.md |

---

# 1. Purpose

This document defines the development sequence for building, testing, deploying, and operating a modular, multi-tenant ERP SaaS platform designed initially for businesses operating in the United Arab Emirates.

The roadmap establishes:

- Development phases and their order.
- Dependencies between phases and modules.
- Deliverables and required documentation.
- Testing and quality requirements.
- Phase-specific acceptance criteria.
- Human approval gates.
- Deployment and operational readiness requirements.
- Rules governing the use of OpenAI Codex and supporting agents.
- Conditions under which functionality may be released to customers.

This document is the authoritative source for development sequencing.

Detailed implementation requirements belong in the individual phase specifications and module specifications.

## 1.1 Guiding principle

**Build a secure, operationally reliable SaaS foundation before building a large collection of ERP features.**

Each phase must leave the repository in a tested, documented, and maintainable state.

A phase is not complete merely because the code has been generated or the primary user interface appears to work.

Completion requires implementation evidence, automated tests, security checks, documentation, and explicit approval.

---

# 2. Product Delivery Strategy

The product will be developed as a modular monolith.

The initial architecture will use a single Django codebase, a shared PostgreSQL cluster, and clearly separated application domains. Supporting services such as Redis and Celery will be introduced where justified by the requirements.

The system will not be split into microservices during the initial development roadmap.

## 2.1 Development principles

1. **Requirements before implementation:** Every significant feature must trace back to an approved requirement.
2. **Foundation before features:** Tenant isolation, authentication, authorization, auditability, and deployment foundations must precede commercial modules.
3. **Incremental delivery:** Implement and validate a small, coherent scope in each phase.
4. **Testable development:** Every meaningful business rule must have automated test coverage.
5. **Secure by default:** Tenant isolation and server-side authorization must be enforced independently of the user interface.
6. **Financial integrity:** Financial transactions must preserve accounting invariants, audit trails, and appropriate transaction boundaries.
7. **Configurable commercial rules:** Prices, module availability, subscription rules, and module dependencies must not be scattered as hardcoded business logic.
8. **Operational readiness:** Backups, recovery, monitoring, and deployment procedures must be developed before production launch.
9. **Explicit release controls:** Features must not become commercially available solely because they exist in the codebase.
10. **Human approval:** Codex agents may prepare changes and evidence, but designated human reviewers approve phase completion and production releases.

## 2.2 Delivery approach

Use a sequential phase-gated approach with limited parallel development inside approved boundaries.

For example, while the core platform is being implemented, the architecture agent may prepare detailed CRM and accounting specifications. However, a feature agent must not implement dependent business functionality before its required platform contracts and dependencies are approved.

Parallel work is permitted only when tasks have:
- Clearly defined interfaces.
- Explicit ownership of files and components.
- No unresolved dependency on unfinished architecture.
- A plan for integrating and testing the results.

---

# 3. Phase Overview

The product roadmap consists of thirteen phases, beginning with Phase 0 and ending with Phase 12.

| Phase | Phase ID | Name | Primary Outcome |
|---|---|---|---|
| P0 | P0-FOUNDATION | Foundation & Architecture | Approved architecture, repository structure, development standards, and delivery controls |
| P1 | P1-CORE-PLATFORM | Core Platform & Multi-Tenancy | Secure tenant-aware application foundation |
| P2 | P2-SUBSCRIPTION-ENGINE | Module Catalogue, Subscription & Billing | Configurable subscriptions, module entitlements, and SaaS billing foundation |
| P3 | P3-CRM-SALES-INVOICING | CRM, Sales & Basic Invoicing | First coherent customer-facing commercial workflow |
| P4 | P4-UAE-EINVOICING | UAE E-Invoicing Provider Integration | Validated integration with the selected provider and applicable UAE requirements |
| P5 | P5-ACCOUNTING-VAT | Accounting & UAE VAT | Accounting ledger, financial reporting foundations, and configurable VAT handling |
| P6 | P6-PROCUREMENT-INVENTORY | Procurement & Inventory | Supplier purchasing and stock-control workflows |
| P7 | P7-HRMS-PAYROLL | HRMS & Payroll | Employee management and validated payroll workflows |
| P8 | P8-PROJECTS-EXPENSES-ASSETS | Projects, Expenses & Fixed Assets | Project tracking, expense management, and asset accounting |
| P9 | P9-BANKING-ADVANCED-FINANCE | Banking & Advanced Finance | Bank reconciliation and additional financial controls |
| P10 | P10-REPORTING-INTEGRATIONS | Reporting, Analytics & Integration Hub | Consolidated reports, dashboards, and controlled integrations |
| P11 | P11-ENTERPRISE-READINESS | Advanced SaaS Administration & Enterprise Readiness | Advanced administration, governance, and scale-readiness improvements |
| P12 | P12-PRODUCTION-LAUNCH | Production Deployment, Launch & Operations | Production release, operational handover, and post-launch controls |

**Important:** P0 is a planning and engineering-foundation phase, not a substitute for implementing the actual application. P12 is not merely deployment; it includes launch validation and operational readiness.

---

# 4. Phase Dependencies

The roadmap is sequential by default, but certain specification and testing activities may proceed in parallel.

| Phase | Required Dependencies | May Prepare in Parallel |
|---|---|---|
| P0 | None | Initial product discovery and requirement clarification |
| P1 | P0 approved | Detailed specifications for subscription, CRM, and accounting |
| P2 | P1 approved | CRM workflow design and provider research |
| P3 | P1 approved; P2 entitlement contracts available | E-invoicing provider evaluation; accounting design |
| P4 | P3 invoice model and workflow approved; provider and regulatory assumptions validated | Accounting and VAT implementation planning |
| P5 | P1 and P3 approved; P4 coordination plan established | Procurement and inventory specifications |
| P6 | P1 approved; product and accounting integration contracts agreed | HRMS specification and data-protection review |
| P7 | P1 approved; employee, payroll, and statutory requirements validated | Projects and expenses specifications |
| P8 | P1 and relevant financial integration contracts approved | Banking integration research |
| P9 | P5 accounting foundation approved; relevant P6/P8 integrations available where required | Reporting design and integration framework planning |
| P10 | Relevant underlying modules and reporting contracts approved | Enterprise-readiness assessment |
| P11 | Core commercial workflows implemented; security and operational foundations established | Production infrastructure preparation |
| P12 | Required launch scope implemented; release gates satisfied | No unapproved production changes |

## 4.1 Dependency rules

1. A dependent phase cannot be marked complete while a required upstream dependency remains unresolved.
2. Research and specification work may begin early, but implementation must respect approved interfaces and dependency contracts.
3. Optional integrations must not block the initial launch unless the approved launch scope requires them.
4. Regulatory, accounting, and payroll assumptions must be documented and validated before the associated functionality is represented as production-ready.
5. If a dependency changes, the phase manifest and affected specifications must be updated before further implementation.

---

# 5. Phase 0 — Foundation & Architecture

**Phase ID:** `P0-FOUNDATION`

**Objective:** Establish an approved, consistent foundation for product development and AI-assisted engineering.

## 5.1 Scope

- Finalize the master product specification.
- Establish the requirements baseline.
- Finalize the initial module catalogue.
- Define the development roadmap.
- Define the Django application structure.
- Define the multi-tenancy strategy.
- Establish architecture decision records.
- Establish coding standards and testing strategy.
- Establish Codex agent responsibilities.
- Define the repository structure and documentation conventions.
- Define phase and task manifests.
- Establish human approval gates.
- Define the initial CI pipeline.
- Identify unresolved product and regulatory decisions.

## 5.2 Deliverables

- `AGENTS.md`
- `README.md`
- `docs/00-product/MASTER_PRODUCT_SPECIFICATION.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/00-product/TARGET_MARKET.md`
- `docs/00-product/COMMERCIAL_MODEL.md`
- `docs/00-product/MODULE_CATALOGUE.md`
- `docs/00-product/DEVELOPMENT_ROADMAP.md`
- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- `docs/01-architecture/DJANGO_APP_STRUCTURE.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/01-architecture/MODULE_DEPENDENCIES.md`
- `docs/01-architecture/ENTITLEMENT_ENGINE.md`
- `docs/01-architecture/API_STANDARDS.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- Initial architecture decision records.
- Initial CI workflow.
- Phase and task manifest schemas.
- Initial risk and decision registers.

## 5.3 Acceptance criteria

- [ ] Product scope and non-goals are documented.
- [ ] Requirements have unique, stable identifiers.
- [ ] Each planned module has a documented purpose and boundary.
- [ ] The initial dependency graph is reviewed for circular dependencies.
- [ ] The multi-tenancy approach is documented.
- [ ] Financial data ownership and transaction principles are documented.
- [ ] The entitlement engine has a defined contract.
- [ ] Security and testing standards are documented.
- [ ] The initial repository structure is approved.
- [ ] Unresolved decisions have named owners and explicit consequences.
- [ ] The first implementation phase has a bounded, testable scope.
- [ ] Codex instructions prohibit fabricated test results and unapproved scope expansion.

## 5.4 Exit gate

**Gate:** Architecture and product foundation approved.

The Product Owner and designated technical reviewer must approve the architecture baseline before P1 begins implementation.

---

# 6. Phase 1 — Core Platform & Multi-Tenancy

**Phase ID:** `P1-CORE-PLATFORM`

**Objective:** Build the secure application foundation on which every business module depends.

## 6.1 Scope

- Initialize the Django project.
- Configure PostgreSQL.
- Establish development and test environments.
- Implement tenant registration and lifecycle foundations.
- Implement tenant context resolution.
- Implement user authentication.
- Implement tenant membership and roles.
- Implement server-side permission checks.
- Establish tenant-aware query and service patterns.
- Establish audit-event foundations.
- Configure application logging.
- Implement health checks.
- Configure database migrations.
- Establish CI test execution.
- Establish a basic Docker development environment.

## 6.2 Core security requirements

Every tenant-owned business operation must verify the active tenant and the requesting user's access to that tenant.

The application must not trust a tenant identifier supplied by a browser, API request, URL parameter, or background-task payload without validating it against an authorized server-side context.

Tenant isolation must be enforced consistently across:
- HTML views.
- API endpoints.
- Service-layer operations.
- Querysets and managers.
- Background jobs.
- File access.
- Exports and reports.
- Administrative operations.

PostgreSQL Row-Level Security may be used as a defense-in-depth control, provided its policies, database roles, connection behavior, and transaction lifecycle are designed and tested correctly. It must not be treated as a substitute for application-level authorization.

## 6.3 Deliverables

- Django project and settings structure.
- Core, tenant, and user applications.
- Tenant lifecycle models and services.
- User and tenant membership models.
- Authentication and authorization foundations.
- Audit-event model and recording service.
- Tenant-aware query and service conventions.
- Docker development configuration.
- Database migration baseline.
- Initial automated security tests.
- CI pipeline running linting and tests.
- Development setup guide.

## 6.4 Acceptance criteria

- [ ] A developer can initialize the application using documented instructions.
- [ ] Database migrations execute successfully on a clean database.
- [ ] Users can authenticate using the approved authentication flow.
- [ ] Tenant membership is checked on protected operations.
- [ ] Cross-tenant read and write attempts are denied.
- [ ] Tests cover tenant context resolution and missing context.
- [ ] Tests cover unauthorized tenant membership.
- [ ] Tenant isolation is tested through views, APIs, and service methods.
- [ ] Background tasks cannot use an unvalidated tenant context.
- [ ] Sensitive operations produce appropriate audit events.
- [ ] Secrets are not committed to the repository.
- [ ] CI passes the required automated checks.
- [ ] Error responses do not disclose data belonging to another tenant.

## 6.5 Exit gate

**Gate:** Core security and tenancy approved.

No commercial ERP module may be declared production-ready until tenant isolation and authorization have passed their required tests.

---

# 7. Phase 2 — Module Catalogue, Subscription & Billing

**Phase ID:** `P2-SUBSCRIPTION-ENGINE`

**Objective:** Enable configurable subscriptions and control access to modules according to each customer's purchased plan.

## 7.1 Scope

- Implement the module registry.
- Implement module lifecycle states.
- Implement subscription plans or configurable subscription arrangements.
- Implement subscription line items.
- Implement module entitlements.
- Implement module dependency validation.
- Implement subscription lifecycle transitions.
- Implement SaaS billing foundations.
- Implement subscription invoice records.
- Define payment-provider integration contracts.
- Implement subscription status and access evaluation.
- Establish administrative controls for module availability.

## 7.2 Core business rules

The system must distinguish between:

1. A module existing in the codebase.
2. A module being enabled for internal use.
3. A module being available for pilot customers.
4. A module being approved for commercial sale.
5. A tenant having purchased or otherwise been granted access to that module.
6. A user having permission to perform a particular action inside that module.

These conditions must not be represented by a single Boolean field.

A module should only be offered for purchase when its lifecycle state and commercial release controls permit it.

A tenant's effective access must be evaluated against tenant status, user permissions, subscription status, module entitlement, and required dependencies.

Conceptually:

`Access Allowed = Tenant Active AND User Authorized AND Subscription Permits Access AND Module Entitled AND Dependencies Satisfied`

The implementation must also handle applicable exceptions, such as authorized platform administration, without bypassing tenant isolation.

## 7.3 SaaS billing separation

SaaS subscription billing represents charges for using the ERP platform.

ERP customer invoicing represents invoices a tenant issues to its own customers.

These are different business domains and must not share a model merely because both involve invoices or payments.

## 7.4 Deliverables

- Module registry and lifecycle management.
- Subscription and subscription-line models.
- Entitlement evaluation service.
- Dependency validation service.
- Subscription lifecycle service.
- SaaS billing models and service layer.
- Payment-provider integration interface.
- Subscription administration screens.
- Automated tests for entitlement decisions.
- Module activation and deactivation documentation.

## 7.5 Acceptance criteria

- [ ] Modules are registered through a consistent catalogue.
- [ ] Module lifecycle state is separate from tenant entitlement.
- [ ] Module prices and commercial availability are configurable.
- [ ] Dependency validation prevents invalid subscriptions.
- [ ] A tenant cannot access a module it has not purchased or been granted.
- [ ] A user without the required role cannot access protected functions.
- [ ] Subscription status changes affect access according to approved rules.
- [ ] SaaS subscription invoices are separate from ERP customer invoices.
- [ ] Failed payment behavior follows an explicitly approved policy.
- [ ] Repeated payment-provider events do not create duplicate financial records.
- [ ] Module access is tested at the UI, API, service, and background-task boundaries where applicable.
- [ ] Internal-only and unreleased modules are not shown as purchasable.
- [ ] The module catalogue can evolve without changing unrelated modules.

## 7.6 Exit gate

**Gate:** Commercial access and entitlement controls approved.

No module may be commercially sold until its release status, dependencies, pricing configuration, and entitlement behavior have been validated.

---

# 8. Phase 3 — CRM, Sales & Basic Invoicing

**Phase ID:** `P3-CRM-SALES-INVOICING`

**Objective:** Deliver the first coherent business workflow for customers, sales, and invoicing.

## 8.1 Scope

### CRM
- Customer and contact management.
- Lead management.
- Lead status and ownership.
- Activity tracking.
- Customer search and filtering.
- Basic sales pipeline functionality.

### Sales
- Quotations.
- Quotation line items.
- Quotation status transitions.
- Quotation-to-invoice workflow where applicable.
- Customer and product references.

### Invoicing
- Invoice creation.
- Invoice line items.
- Invoice numbering.
- Invoice issue dates and due dates.
- Draft and issued invoice states.
- Payment recording foundations.
- Outstanding balance calculation.
- Credit-note requirements and workflow design.
- Printable invoice documents.

## 8.2 Financial controls

- Issued invoices must not be silently overwritten.
- Corrections to finalized financial documents must follow the approved amendment, cancellation, or credit-note process.
- Invoice numbering rules must be documented and tested.
- Monetary calculations must use appropriate decimal arithmetic and currency precision.
- Totals must be calculated server-side.
- Invoice status transitions must be validated.
- Customer data and financial documents must remain tenant-isolated.

## 8.3 Deliverables

- CRM application.
- Sales application.
- Invoicing application.
- Customer and contact workflows.
- Quotation workflow.
- Invoice lifecycle service.
- Invoice rendering templates.
- Invoice numbering configuration.
- Financial calculation tests.
- User documentation for the first commercial workflow.

## 8.4 Acceptance criteria

- [ ] Authorized users can create and manage customer records.
- [ ] Leads and sales activities can be tracked.
- [ ] Quotations can be created and moved through valid states.
- [ ] Approved workflows can generate invoices.
- [ ] Invoice totals are calculated server-side.
- [ ] Invoice numbering is protected against unintended duplicates.
- [ ] Issued invoices cannot be silently edited.
- [ ] Appropriate cancellation or correction workflows are enforced.
- [ ] Tenant isolation applies to customers, quotations, invoices, and payments.
- [ ] Financial calculations have automated boundary and rounding tests.
- [ ] Invoice documents display the required configured business details.
- [ ] Access to invoice functions follows module entitlements and user permissions.

## 8.5 Exit gate

**Gate:** Initial commercial workflow approved.

The product may proceed to a controlled pilot only if the Product Owner explicitly approves the available feature scope and any remaining limitations are documented.

---

# 9. Phase 4 — UAE E-Invoicing Provider Integration

**Phase ID:** `P4-UAE-EINVOICING`

**Objective:** Integrate the invoicing workflow with a selected provider after validating applicable UAE e-invoicing requirements.

## 9.1 Scope

- Research the applicable UAE e-invoicing framework.
- Confirm the intended customer segments and rollout obligations.
- Evaluate eligible providers and their technical capabilities.
- Select a provider subject to commercial and compliance review.
- Document provider API contracts.
- Implement the provider adapter.
- Implement invoice submission and status tracking.
- Implement retry and failure-handling behavior.
- Store relevant provider references and responses.
- Implement reconciliation between ERP invoices and provider submissions.
- Implement sandbox and integration tests.
- Document operational procedures for rejected or delayed submissions.

## 9.2 Regulatory qualification

Regulatory requirements, effective dates, implementation obligations, data formats, transmission procedures, and provider eligibility must be validated against current authoritative UAE sources and the selected provider's current documentation.

Do not assume that a generic invoice API constitutes regulatory compliance.

Do not represent the product as compliant merely because a submission endpoint has been integrated.

Any compliance statement must be supported by validated requirements, a tested implementation, and appropriate specialist review.

## 9.3 Integration design principles

- Keep provider-specific code behind a defined adapter interface.
- Keep provider identifiers separate from internal invoice identifiers.
- Preserve the original internal invoice and relevant version information.
- Use idempotency controls for submission and retry operations.
- Do not automatically treat a timeout as proof that a submission failed.
- Reconcile uncertain submission outcomes before retrying where required.
- Keep provider credentials outside source control.
- Record appropriate audit events.
- Protect sensitive invoice payloads and provider responses.
- Make provider status transitions explicit.

## 9.4 Deliverables

- Regulatory assumptions and validation register.
- Provider evaluation and selection record.
- E-invoicing integration architecture.
- Provider adapter.
- Submission and status-tracking workflows.
- Retry and reconciliation services.
- Provider sandbox tests.
- Failure-handling runbook.
- Updated invoice lifecycle documentation.

## 9.5 Acceptance criteria

- [ ] The selected provider and applicable integration requirements are documented.
- [ ] The supported invoice format and validation rules are defined.
- [ ] Provider credentials are stored securely.
- [ ] Submission results are linked to the correct internal invoice.
- [ ] Duplicate submissions are controlled through documented idempotency and reconciliation behavior.
- [ ] Timeouts and uncertain results are handled safely.
- [ ] Rejected submissions can be investigated and corrected.
- [ ] Provider responses and status transitions are auditable.
- [ ] Automated tests cover success, rejection, timeout, retry, and duplicate-event scenarios.
- [ ] Sandbox testing is completed where the provider makes it available.
- [ ] Operational procedures cover outages and delayed responses.
- [ ] Compliance claims remain limited to the requirements actually validated.

## 9.6 Exit gate

**Gate:** Provider integration and compliance assumptions reviewed.

Production release requires the relevant provider validation, legal or specialist review where appropriate, and approval of the specific intended production scope.

---

# 10. Phase 5 — Accounting & UAE VAT

**Phase ID:** `P5-ACCOUNTING-VAT`

**Objective:** Establish a reliable accounting foundation and implement VAT workflows according to validated business and regulatory requirements.

## 10.1 Scope

### Accounting
- Chart of accounts.
- Fiscal periods.
- Journal entries.
- Journal entry lines.
- Posting and reversal workflows.
- General ledger.
- Trial balance.
- Accounting period controls.
- Financial statement foundations.

### VAT
- Configurable VAT codes and rates.
- Tax treatment rules.
- Tax calculation services.
- VAT treatment on supported sales and purchase documents.
- Tax reporting foundations.
- Validation of applicable UAE VAT requirements.

## 10.2 Accounting principles

- Posted journal entries must balance.
- Posted financial records must not be silently overwritten.
- Corrections must use controlled reversal or adjustment workflows.
- Posting operations must be transactional.
- Account and period validation must occur before posting.
- Financial reports must be reproducible from the underlying records.
- Monetary values must use appropriate decimal arithmetic.
- Accounting periods must have explicit open and closed states.
- Financial changes must be auditable.

## 10.3 VAT principles

VAT rules must be configurable and versioned where required.

The system must not assume that every transaction uses the same rate or tax treatment.

The implementation must support only those tax treatments that have been validated for the approved product scope. Edge cases outside that scope must be documented rather than silently treated as ordinary transactions.

## 10.4 Deliverables

- Accounting models and services.
- Chart-of-accounts configuration.
- Journal posting and reversal services.
- General ledger and trial balance reports.
- Fiscal-period controls.
- VAT calculation service.
- VAT code configuration.
- Supported VAT reporting outputs.
- Accounting and VAT test suite.
- Financial reconciliation documentation.

## 10.5 Acceptance criteria

- [ ] Posted journal entries balance.
- [ ] Invalid journal entries cannot be posted.
- [ ] Posting and reversal operations are transactional.
- [ ] Closed periods enforce the approved posting restrictions.
- [ ] Posted financial records preserve their audit history.
- [ ] Trial balance totals reconcile to the ledger.
- [ ] Sales and purchase transactions map correctly to supported accounts.
- [ ] VAT calculations use approved rules and decimal arithmetic.
- [ ] VAT behavior is tested across supported transaction types.
- [ ] Reports reconcile to their underlying source records.
- [ ] Tenant isolation is enforced across all financial records.
- [ ] Financial corrections follow approved workflows.
- [ ] Applicable UAE VAT assumptions are reviewed and documented.

## 10.6 Exit gate

**Gate:** Accounting integrity and VAT behavior approved.

Financial workflows must pass reconciliation and integrity tests before being offered as production accounting functionality.

---

# 11. Phase 6 — Procurement & Inventory

**Phase ID:** `P6-PROCUREMENT-INVENTORY`

**Objective:** Implement supplier purchasing and stock-control workflows integrated with the approved accounting and product foundations.

## 11.1 Scope

### Procurement
- Supplier records.
- Purchase requisitions where included in scope.
- Purchase orders.
- Purchase order lines.
- Purchase order status transitions.
- Goods receipt.
- Supplier invoice references.
- Purchase-order and receipt reconciliation.

### Inventory
- Product and service catalogue integration.
- Warehouses and locations.
- Stock movements.
- Receipts and issues.
- Transfers.
- Stock adjustments.
- Stock availability.
- Stock valuation design and implementation.
- Inventory movement history.

## 11.2 Inventory controls

- Stock quantities must not be modified without a recorded movement or approved adjustment.
- Concurrent stock operations must preserve inventory consistency.
- The approved stock valuation method must be documented before valuation-dependent financial posting is implemented.
- Transfers must record both the source and destination effects.
- Negative inventory behavior must be explicitly configured.
- Reversals and corrections must preserve movement history.

## 11.3 Deliverables

- Procurement application.
- Inventory application.
- Supplier workflows.
- Purchase order workflow.
- Goods receipt workflow.
- Warehouse and location configuration.
- Stock movement services.
- Inventory valuation implementation for the approved method.
- Procurement and inventory reports.
- Stock reconciliation tests.

## 11.4 Acceptance criteria

- [ ] Authorized users can manage suppliers.
- [ ] Purchase orders follow valid status transitions.
- [ ] Goods receipts are traceable to their source documents.
- [ ] Stock movements are recorded as auditable transactions.
- [ ] Transfers preserve total quantity across locations, subject to recorded losses or adjustments.
- [ ] Concurrent operations cannot silently corrupt stock balances.
- [ ] Negative stock behavior follows an approved policy.
- [ ] Stock valuation follows the approved method.
- [ ] Inventory and financial records reconcile where integration is enabled.
- [ ] Tenant isolation applies to suppliers, warehouses, products, and movements.
- [ ] Stock adjustments require appropriate authorization.

## 11.5 Exit gate

**Gate:** Procurement and inventory integrity approved.

Stock movement, concurrency, and valuation tests must pass before production inventory usage is approved.

---

# 12. Phase 7 — HRMS & Payroll

**Phase ID:** `P7-HRMS-PAYROLL`

**Objective:** Deliver employee management and payroll functionality based on validated UAE employment and payroll requirements.

## 12.1 Scope

### HRMS
- Employee profiles.
- Department and designation records.
- Employment status.
- Employment dates.
- Document references and controlled document access.
- Leave policy and leave request foundations.
- Leave balances and approval workflows.

### Payroll
- Payroll periods.
- Payroll runs.
- Earnings and deduction components.
- Payroll calculation engine.
- Review and approval workflow.
- Payslip generation.
- Payroll records and audit history.
- Required statutory or regulated integrations within approved scope.

## 12.2 Compliance and data protection

Payroll and employee data require stricter access controls than ordinary operational data.

Access must be limited by role, tenant, and the sensitivity of the information.

Payroll rules, leave policies, employment requirements, and any applicable statutory reporting obligations must be validated before implementation is represented as suitable for production use.

Do not assume that one payroll configuration applies to every UAE employer or employment arrangement.

## 12.3 Deliverables

- HRMS application.
- Employee and department workflows.
- Leave management foundations.
- Payroll calculation service.
- Payroll approval workflow.
- Payslip rendering.
- Payroll audit controls.
- Data-access and retention documentation.
- Payroll test suite.
- Validated requirements register for supported payroll scenarios.

## 12.4 Acceptance criteria

- [ ] Employee records are tenant-isolated.
- [ ] Sensitive employee information has field- and action-appropriate access controls.
- [ ] Leave balances follow approved policy rules.
- [ ] Payroll calculations are deterministic for a fixed set of inputs and rule versions.
- [ ] Payroll runs can be reviewed before finalization.
- [ ] Finalized payroll records cannot be silently overwritten.
- [ ] Payslips are accessible only to authorized users.
- [ ] Payroll corrections preserve an audit trail.
- [ ] Tests cover rounding, deductions, effective dates, and supported edge cases.
- [ ] Supported statutory rules have been validated.
- [ ] Data retention and access procedures are documented.

## 12.5 Exit gate

**Gate:** HRMS and payroll rules reviewed.

Payroll must not be commercially represented as fully compliant until the supported employment scenarios and applicable regulatory requirements have been validated.

---

# 13. Phase 8 — Projects, Expenses & Fixed Assets

**Phase ID:** `P8-PROJECTS-EXPENSES-ASSETS`

**Objective:** Expand the platform into project operations, expense control, and fixed-asset management.

## 13.1 Scope

### Projects
- Project records.
- Project ownership.
- Tasks and milestones.
- Project status.
- Project-related customer and commercial references.
- Basic project reporting.

### Expenses
- Expense records.
- Expense categories.
- Employee or user submissions.
- Receipt attachments where supported.
- Approval workflows.
- Reimbursement tracking.
- Accounting integration.

### Fixed Assets
- Asset register.
- Asset categories.
- Acquisition records.
- In-service dates.
- Depreciation configuration.
- Depreciation schedules.
- Disposal and retirement workflows.
- Asset-related accounting entries.

## 13.2 Deliverables

- Projects application.
- Expenses application.
- Fixed-assets application.
- Approval workflows.
- Attachment access controls.
- Expense-to-accounting integration.
- Asset depreciation services.
- Asset lifecycle workflows.
- Related reports and tests.

## 13.3 Acceptance criteria

- [ ] Project records and related activities are tenant-isolated.
- [ ] Expense approval rules are enforced server-side.
- [ ] Expense attachments are accessible only to authorized users.
- [ ] Approved expenses follow the configured accounting workflow.
- [ ] Asset acquisition and disposal events are recorded.
- [ ] Depreciation follows the approved method and configuration.
- [ ] Asset postings reconcile to relevant accounting records.
- [ ] Corrections preserve historical records and audit events.
- [ ] Financial integrations are tested for duplicate and partial execution.
- [ ] Reports reconcile to their underlying records.

## 13.4 Exit gate

**Gate:** Operational and financial integration approved.

Project, expense, and asset workflows must be tested independently and together wherever financial posting is enabled.

---

# 14. Phase 9 — Banking & Advanced Finance

**Phase ID:** `P9-BANKING-ADVANCED-FINANCE`

**Objective:** Improve financial operations through bank reconciliation and additional finance controls.

## 14.1 Scope

- Bank account records.
- Bank statement import.
- Transaction normalization.
- Matching suggestions.
- Manual reconciliation.
- Reconciliation status.
- Unmatched transaction review.
- Payment allocation.
- Additional financial controls approved for the release.
- Optional bank connectivity research and implementation.

## 14.2 Integration principles

Bank connectivity must be implemented only after the provider, authorization model, supported institutions, data format, and operational requirements have been evaluated.

A file-import workflow may be implemented independently of a direct banking integration.

Credentials and tokens must be stored securely. Imported transactions must be deduplicated using reliable provider identifiers or a documented reconciliation strategy.

## 14.3 Deliverables

- Banking application.
- Bank account management.
- Statement import and parsing.
- Reconciliation service.
- Matching workflow.
- Duplicate-import protection.
- Financial reconciliation reports.
- Bank integration adapter, if approved.
- Operational procedures for unmatched transactions.

## 14.4 Acceptance criteria

- [ ] Bank accounts are tenant-isolated.
- [ ] Statement imports validate the expected format.
- [ ] Re-importing a statement does not silently duplicate transactions.
- [ ] Matching and reconciliation preserve audit history.
- [ ] Unmatched transactions can be reviewed and resolved.
- [ ] Reconciliation results can be reproduced.
- [ ] Financial postings are transactional and idempotent where appropriate.
- [ ] Direct bank integrations, if implemented, follow the approved security and authorization model.

## 14.5 Exit gate

**Gate:** Reconciliation integrity approved.

Banking functionality must pass import, duplicate-detection, matching, and reconciliation tests before production release.

---

# 15. Phase 10 — Reporting, Analytics & Integration Hub

**Phase ID:** `P10-REPORTING-INTEGRATIONS`

**Objective:** Provide consolidated reporting and a controlled framework for external integrations.

## 15.1 Scope

### Reporting and analytics
- Standard operational reports.
- Sales reporting.
- Receivables and payables reporting.
- Financial reporting.
- Inventory reporting.
- HR and payroll reporting where authorized.
- Dashboard foundations.
- Date-range and filtering controls.
- Export functionality.
- Report authorization and tenant isolation.

### Integration hub
- Integration registry.
- External credential references.
- Integration configuration.
- Webhook receiving and delivery.
- Retry policies.
- Idempotency.
- Integration event logs.
- Integration health indicators.
- Rate limits and access controls.

## 15.2 Reporting principles

Reports must respect the same tenant, role, and module-entitlement restrictions as the underlying records.

Financial reports must use approved accounting sources rather than independently recalculating financial balances through inconsistent application-specific logic.

Exports must be treated as data-access operations and audited where appropriate.

## 15.3 Deliverables

- Reporting application.
- Standard report definitions.
- Dashboard framework.
- Controlled export services.
- Integration registry.
- Webhook infrastructure.
- Integration retry and logging services.
- Report performance tests.
- Documentation for supported integrations.

## 15.4 Acceptance criteria

- [ ] Reports enforce tenant isolation.
- [ ] Reports enforce appropriate role permissions.
- [ ] Financial reports reconcile to approved source records.
- [ ] Exported files contain only authorized information.
- [ ] Large reports have defined performance and resource limits.
- [ ] Webhook delivery and processing are idempotent where required.
- [ ] Failed integrations are observable and recoverable.
- [ ] Credentials are not exposed in logs or API responses.
- [ ] Integration failures do not corrupt the underlying business transaction.
- [ ] Report and integration contracts are documented.

## 15.5 Exit gate

**Gate:** Reporting and integration controls approved.

Reporting must be validated for data correctness and access isolation. Integrations must be validated for security, retries, and failure recovery.

---

# 16. Phase 11 — Advanced SaaS Administration & Enterprise Readiness

**Phase ID:** `P11-ENTERPRISE-READINESS`

**Objective:** Strengthen platform administration, governance, security, and operational readiness for a wider customer base.

## 16.1 Scope

The final scope must be based on actual customer requirements and a formal readiness assessment.

Potential capabilities include:

- Enhanced tenant administration.
- Subscription and entitlement administration.
- Support-access controls.
- Controlled support impersonation, if approved.
- Advanced audit search and export.
- Configurable retention policies.
- Data export and deletion workflows.
- Organization branding.
- Locale and timezone controls.
- Arabic and right-to-left interface improvements, if included in the approved launch scope.
- Performance optimization.
- Security hardening.
- Dependency and vulnerability management.
- Accessibility improvements.
- Enterprise configuration options.
- Additional administrative reporting.

## 16.2 Operational controls

- Support access must be authorized, limited, and auditable.
- Privileged administrative actions must be logged.
- Data export and deletion must follow documented retention and legal requirements.
- Tenant lifecycle operations must not leave inaccessible or orphaned data.
- Performance improvements must be based on measured bottlenecks.
- Optional enterprise capabilities must not weaken tenant isolation.

## 16.3 Deliverables

- SaaS administration improvements.
- Support-access policy and controls.
- Enhanced audit and retention mechanisms.
- Security review report.
- Performance assessment.
- Accessibility and localization assessment.
- Operational-readiness checklist.
- Updated support runbooks.

## 16.4 Acceptance criteria

- [ ] Privileged administrative operations require appropriate authorization.
- [ ] Support access follows an approved policy.
- [ ] Sensitive administrative actions are auditable.
- [ ] Data export and deletion workflows are documented and tested where implemented.
- [ ] Performance bottlenecks are assessed using reproducible tests.
- [ ] Security findings are tracked and resolved or explicitly accepted by authorized reviewers.
- [ ] Localization behavior is tested for supported locales.
- [ ] Enterprise features are covered by tenant-isolation tests.
- [ ] Operations staff have documented procedures for routine administration.

## 16.5 Exit gate

**Gate:** Enterprise-readiness review approved.

The platform must have a documented security, performance, and operational risk position before the production launch decision.

---

# 17. Phase 12 — Production Deployment, Launch & Operations

**Phase ID:** `P12-PRODUCTION-LAUNCH`

**Objective:** Deploy the approved release into production, verify operational readiness, and establish controlled post-launch operations.

## 17.1 Scope

### Infrastructure
- Production environment provisioning.
- Environment-specific configuration.
- Container image build and release.
- Database provisioning.
- Database migration procedure.
- Reverse proxy and application server configuration.
- TLS configuration.
- Domain and DNS configuration.
- Static and media file strategy.
- Background worker deployment.
- Scheduled task deployment.
- Secret management.

### Security
- Production security configuration.
- Least-privilege access.
- Administrative access review.
- Security-header review.
- Rate limiting where required.
- Dependency and image scanning.
- Logging and sensitive-data review.

### Operations
- Application monitoring.
- Infrastructure monitoring.
- Error reporting.
- Backup automation.
- Restore testing.
- Incident response.
- Release and rollback procedures.
- Support and escalation procedures.

### Launch
- User acceptance testing.
- Production smoke tests.
- Tenant onboarding validation.
- Subscription and payment validation.
- Invoice workflow validation.
- Provider integration validation where in scope.
- Launch approval.
- Post-launch review.

## 17.2 Deliverables

- `docs/06-deployment/DEPLOYMENT_ARCHITECTURE.md`
- `docs/06-deployment/INFRASTRUCTURE_REQUIREMENTS.md`
- `docs/06-deployment/ENVIRONMENT_VARIABLES.md`
- `docs/06-deployment/DEPLOYMENT_GUIDE.md`
- `docs/06-deployment/BACKUP_AND_RECOVERY.md`
- `docs/06-deployment/MONITORING_AND_ALERTING.md`
- `docs/06-deployment/OPERATIONS_RUNBOOK.md`
- Production Docker and deployment configuration.
- CI/CD release workflow.
- Migration and rollback procedures.
- Backup and restore evidence.
- Security assessment.
- Performance and capacity assessment.
- User acceptance test evidence.
- Production launch checklist.
- Incident response and escalation documentation.

## 17.3 Acceptance criteria

- [ ] A clean deployment can be completed using the approved deployment guide.
- [ ] Required secrets are injected securely.
- [ ] Production settings do not rely on development defaults.
- [ ] HTTPS is configured correctly for public application traffic.
- [ ] Database migrations have been rehearsed on a representative environment.
- [ ] Migration failure and rollback limitations are documented.
- [ ] Background workers and scheduled tasks operate correctly.
- [ ] Health checks report application and dependency status appropriately.
- [ ] Monitoring and alerting are configured for critical failures.
- [ ] Automated backups are configured.
- [ ] A restore test has demonstrated that backups are usable.
- [ ] Recovery objectives are documented and tested to the extent required by the approved service target.
- [ ] Production smoke tests pass.
- [ ] Tenant isolation tests pass against the release candidate.
- [ ] Critical security findings are resolved or explicitly accepted by authorized decision-makers.
- [ ] The release has a documented rollback or forward-recovery procedure.
- [ ] User acceptance testing is approved.
- [ ] Support ownership and incident escalation paths are documented.
- [ ] The Product Owner explicitly authorizes production launch.

## 17.4 Exit gate

**Gate:** Production launch approved.

Production deployment is complete only when the release is verified, operational ownership is assigned, and the launch decision is recorded.

---

# 18. Cross-Phase Quality Gates

Every phase must satisfy the following requirements unless a documented exception has been approved.

## 18.1 Requirements traceability

Each feature or task must reference one or more requirement IDs.

For example:

- Tenant isolation work references the applicable `TEN-*` requirements.
- Entitlement work references the applicable `SUB-*` requirements.
- Invoice workflows reference the applicable `INV-*` requirements.
- VAT work references the applicable `VAT-*` requirements.
- Deployment work references the applicable `DEP-*` requirements.

The actual identifiers must match the approved requirements document.

Do not invent identifiers when an appropriate requirement already exists.

If a requirement is missing, record the gap and request approval before expanding the scope.

## 18.2 Code quality

Required checks should include:

- Formatting.
- Linting.
- Static analysis where configured.
- Type checking where adopted.
- Django system checks.
- Database migration checks.
- Automated tests.
- Dependency security checks.
- Secret scanning.
- Container image scanning where applicable.

The project must select and configure its actual tools in P0. The roadmap does not require every available tool to be adopted if an approved equivalent meets the requirement.

## 18.3 Testing

The testing strategy must include the following categories as applicable:

| Test Type | Purpose |
|---|---|
| Unit tests | Validate individual business rules and calculations |
| Integration tests | Validate interactions between services, models, and external adapters |
| API tests | Validate request handling, authorization, validation, and response contracts |
| UI tests | Validate critical user workflows |
| Tenant-isolation tests | Detect cross-tenant access and data leakage |
| Permission tests | Verify role and action authorization |
| Financial-integrity tests | Verify posting, balances, rounding, and reconciliation |
| Idempotency tests | Verify safe retries and duplicate-event handling |
| Migration tests | Verify schema changes on representative database states |
| Security tests | Verify relevant access-control and security requirements |
| Performance tests | Validate agreed workload and latency targets |
| Recovery tests | Validate backup restoration and recovery procedures |

Tests must reflect the actual implemented behavior. Agents must not claim tests passed unless they were executed and their results were observed.

## 18.4 Documentation

Documentation must be updated whenever implementation changes affect:

- Public or internal APIs.
- Database schema.
- Module dependencies.
- Entitlement behavior.
- Environment variables.
- Security controls.
- Deployment procedures.
- Business rules.
- Operational recovery.
- Known limitations.

## 18.5 Release safety

A phase must not be marked complete if it contains an unresolved critical defect affecting:

- Tenant isolation.
- Authentication or authorization.
- Financial integrity.
- Data loss.
- Secret exposure.
- Unauthorized access to sensitive data.
- Required regulatory processing within the approved release scope.

Any exception requires explicit written approval from the authorized decision-maker, a documented risk assessment, and a mitigation plan. Legal or regulatory obligations cannot be waived by a software project approval.

---

# 19. Definition of Phase Completion

A phase is complete only when all required conditions below are satisfied.

1. Scope is implemented according to the approved phase specification.
2. Acceptance criteria have been evaluated.
3. Automated tests have been executed.
4. Test results and failures are recorded.
5. Required code review is complete.
6. Security implications have been assessed.
7. Database migrations have been validated where applicable.
8. Documentation has been updated.
9. Known defects and limitations have been recorded.
10. Requirement traceability has been updated.
11. The phase completion report has been prepared.
12. Required human approval has been obtained.

A successful build or green test suite does not, by itself, establish that all requirements have been met.

## 19.1 Required phase evidence

Each phase should produce an evidence package containing:

- Scope summary.
- Tasks completed.
- Requirements addressed.
- Files and applications changed.
- Database changes.
- Tests executed and results.
- Security review findings.
- Known defects and limitations.
- Deployment or migration implications.
- Documentation changes.
- Remaining risks.
- Human approval decision.

Store phase-specific evidence alongside the relevant phase documentation or in a clearly linked project record.

---

# 20. Codex Agent Execution Model

OpenAI Codex will be the primary implementation agent. Additional agents may assist with architecture, testing, security review, code review, DevOps, and documentation.

The exact agent orchestration mechanism must be documented separately in `docs/04-agents/ORCHESTRATOR.md`.

## 20.1 Agent responsibilities

| Agent | Primary Responsibility |
|---|---|
| Orchestrator | Select approved tasks, validate dependencies, coordinate work, and prepare phase evidence |
| Architect | Review architecture, interfaces, dependencies, and design changes |
| Developer | Implement approved tasks and tests |
| Test Engineer | Validate acceptance criteria and identify missing coverage |
| Security Reviewer | Assess access control, tenant isolation, secrets, and security risks |
| Code Reviewer | Review correctness, maintainability, and regressions |
| DevOps Agent | Maintain CI/CD, deployment, infrastructure, and recovery documentation |
| Documentation Agent | Maintain specifications, traceability, and user/operational documentation |

Agent names describe responsibilities; they do not imply that every agent runs continuously or autonomously.

## 20.2 Agent operating rules

Every agent must:

1. Read `AGENTS.md`.
2. Read the relevant approved specifications.
3. Check task dependencies.
4. Work only within its assigned scope.
5. Follow existing architectural decisions.
6. Avoid unrelated refactoring.
7. Add or update tests for relevant behavior.
8. Run the required checks when the environment permits.
9. Report commands executed and their actual outcomes.
10. Identify assumptions and unresolved decisions.
11. Update relevant documentation.
12. Avoid committing secrets, credentials, or production data.
13. Avoid destructive database or infrastructure actions without explicit authorization.
14. Request approval when a requirement or architecture decision must change.

Agents must never fabricate test results, deployment outcomes, regulatory approval, provider certification, or successful external integrations.

## 20.3 Parallel execution rules

Parallel tasks must have:
- Clear file and component ownership.
- Defined input and output contracts.
- Explicit dependency conditions.
- Independent tests where possible.
- A controlled integration and review step.

Do not assign multiple agents to make conflicting changes to the same core model, migration chain, or architecture contract without a defined coordination process.

## 20.4 Human approval boundaries

Human approval is required before:

- Approving major architecture changes.
- Changing approved product scope.
- Changing financial or regulatory business rules.
- Selecting or changing a production provider with commercial or compliance implications.
- Performing destructive data operations.
- Applying risky production migrations.
- Deploying a production release.
- Marking a phase formally approved.
- Publishing claims of regulatory compliance.

---

# 21. Phase and Task Status Management

The project must maintain a machine-readable phase manifest and task manifest.

Recommended files:

- `orchestration/phase-manifest.yml`
- `orchestration/task-manifest.yml`

## 21.1 Phase statuses

Use the following statuses consistently:

| Status | Meaning |
|---|---|
| `PLANNED` | The phase is identified but work has not started |
| `SPECIFICATION_IN_PROGRESS` | The phase specification is being prepared |
| `AWAITING_APPROVAL` | Required specifications or decisions are awaiting approval |
| `READY` | Dependencies and scope are approved for implementation |
| `IN_PROGRESS` | Authorized implementation is underway |
| `BLOCKED` | Work cannot proceed because of an unresolved dependency or decision |
| `IN_REVIEW` | Implementation is complete enough for formal validation |
| `REJECTED` | Review identified issues requiring correction |
| `AWAITING_HUMAN_APPROVAL` | Technical validation is complete and approval is pending |
| `APPROVED` | The phase has passed its exit gate |
| `DEFERRED` | The phase is intentionally postponed |
| `CANCELLED` | The phase has been formally cancelled |

Do not mark a phase `APPROVED` merely because all tasks are marked complete.

## 21.2 Task statuses

Recommended task statuses:

- `TODO`
- `READY`
- `IN_PROGRESS`
- `BLOCKED`
- `IN_REVIEW`
- `FAILED`
- `DONE`
- `CANCELLED`

A task marked `DONE` must have verifiable completion evidence appropriate to its scope.

## 21.3 Manifest integrity

The orchestration process must validate:

- Unique phase and task identifiers.
- Valid status values.
- Required dependency references.
- Absence of dependency cycles.
- Required acceptance criteria.
- Required evidence for completion.
- Correct phase-to-task mappings.
- Explicit approval records for phase transitions.

The manifests are coordination tools. They must not become a second, contradictory source of product requirements.

---

# 22. Initial Phase Manifest

The following is the recommended initial phase sequence. It may be used to seed `orchestration/phase-manifest.yml` after the schema is defined and validated.

```yaml
roadmap:
  id: UAE-ERP-SAAS-ROADMAP
  version: "1.0"
  status: AWAITING_APPROVAL

phases:
  - id: P0-FOUNDATION
    sequence: 0
    status: PLANNED
    dependencies: []

  - id: P1-CORE-PLATFORM
    sequence: 1
    status: PLANNED
    dependencies:
      - P0-FOUNDATION

  - id: P2-SUBSCRIPTION-ENGINE
    sequence: 2
    status: PLANNED
    dependencies:
      - P1-CORE-PLATFORM

  - id: P3-CRM-SALES-INVOICING
    sequence: 3
    status: PLANNED
    dependencies:
      - P1-CORE-PLATFORM
      - P2-SUBSCRIPTION-ENGINE

  - id: P4-UAE-EINVOICING
    sequence: 4
    status: PLANNED
    dependencies:
      - P3-CRM-SALES-INVOICING

  - id: P5-ACCOUNTING-VAT
    sequence: 5
    status: PLANNED
    dependencies:
      - P1-CORE-PLATFORM
      - P3-CRM-SALES-INVOICING

  - id: P6-PROCUREMENT-INVENTORY
    sequence: 6
    status: PLANNED
    dependencies:
      - P1-CORE-PLATFORM
      - P5-ACCOUNTING-VAT

  - id: P7-HRMS-PAYROLL
    sequence: 7
    status: PLANNED
    dependencies:
      - P1-CORE-PLATFORM

  - id: P8-PROJECTS-EXPENSES-ASSETS
    sequence: 8
    status: PLANNED
    dependencies:
      - P1-CORE-PLATFORM
      - P5-ACCOUNTING-VAT

  - id: P9-BANKING-ADVANCED-FINANCE
    sequence: 9
    status: PLANNED
    dependencies:
      - P5-ACCOUNTING-VAT

  - id: P10-REPORTING-INTEGRATIONS
    sequence: 10
    status: PLANNED
    dependencies:
      - P1-CORE-PLATFORM
      - P5-ACCOUNTING-VAT

  - id: P11-ENTERPRISE-READINESS
    sequence: 11
    status: PLANNED
    dependencies:
      - P1-CORE-PLATFORM
      - P2-SUBSCRIPTION-ENGINE

  - id: P12-PRODUCTION-LAUNCH
    sequence: 12
    status: PLANNED
    dependencies:
      - P0-FOUNDATION
      - P1-CORE-PLATFORM
```

**Manifest implementation note:** The manifest above captures minimum planning dependencies, not the complete release-readiness graph. Before a phase is marked `READY`, the orchestrator must validate its actual requirements, implementation dependencies, and applicable launch gates.

For example, a production release of a module depends on that module being implemented and approved, even though the generic P12 entry above lists only the foundation dependencies. The task manifest and release checklist must represent the actual launch scope.

---

# 23. Risk Management

Maintain `docs/07-project-management/RISKS_AND_ISSUES.md`.

The following risks should be recorded from the beginning.

| Risk ID | Risk | Impact | Initial Mitigation |
|---|---|---|---|
| R-001 | Tenant data leakage | Critical | Tenant-aware service design, authorization checks, isolation tests, optional database defense in depth |
| R-002 | Scope expansion across ERP modules | High | Approved phase boundaries and explicit change control |
| R-003 | Incorrect financial calculations | Critical | Decimal arithmetic, transactional posting, reconciliation, automated financial tests |
| R-004 | Invalid or outdated UAE regulatory assumptions | High | Validate authoritative requirements and obtain appropriate specialist review |
| R-005 | E-invoicing provider limitations | High | Evaluate provider capabilities before committing to the integration design |
| R-006 | Circular module dependencies | High | Dependency graph validation and domain ownership rules |
| R-007 | Premature microservice decomposition | Medium | Maintain a modular monolith unless measured needs justify a change |
| R-008 | AI-generated code defects | High | Automated tests, human review, security review, and traceability |
| R-009 | Uncontrolled schema changes | High | Reviewed migrations, migration tests, and backup/recovery procedures |
| R-010 | Poor production recovery | Critical | Tested backups, documented recovery objectives, and restore exercises |
| R-011 | Incomplete subscription entitlement checks | High | Central entitlement service and boundary tests |
| R-012 | Sensitive payroll data exposure | Critical | Least privilege, tenant isolation, controlled exports, and security tests |
| R-013 | Background-task duplication | High | Idempotency, retry policies, durable status tracking, and monitoring |
| R-014 | Unvalidated pricing assumptions | Medium | Customer research, configurable pricing, and controlled commercial rollout |
| R-015 | Underestimated infrastructure demand | Medium | Capacity planning, load testing, monitoring, and scaling thresholds |

Risk ratings must be reviewed as evidence becomes available.

---

# 24. Decision Management

Maintain `docs/07-project-management/DECISIONS_PENDING.md`.

A decision record must include:

- Decision ID.
- Question.
- Why the decision matters.
- Available options.
- Recommendation, if one can be justified.
- Decision owner.
- Deadline or phase dependency.
- Final decision.
- Date approved.
- Affected documents and modules.

Decisions that may block implementation include:

1. Initial customer segment and launch scope.
2. Subscription pricing model.
3. Payment provider for SaaS subscriptions.
4. Provider selection for UAE e-invoicing.
5. Applicable e-invoicing requirements and rollout obligations.
6. Supported VAT scenarios.
7. Accounting policies and inventory valuation method.
8. Supported payroll and employment scenarios.
9. Supported currencies, locales, and languages.
10. Hosting region and data residency requirements.
11. Initial tenant and user capacity targets.
12. Availability and recovery objectives.
13. Data retention and deletion rules.
14. Launch module set.
15. Customer onboarding and support process.

Do not silently resolve a material business, legal, regulatory, or financial decision by choosing a convenient implementation default.

Where a decision does not block the current phase, record it and continue within the approved boundaries.

---

# 25. Deployment Planning Across Phases

Deployment is not postponed until P12.

Each phase must include deployment considerations for the functionality it introduces.

| Phase | Required Deployment Considerations |
|---|---|
| P0 | Local development setup, repository conventions, initial CI |
| P1 | Application configuration, database setup, migrations, health checks |
| P2 | Subscription configuration, scheduled billing tasks, payment-provider secrets |
| P3 | Invoice rendering, storage, application permissions, financial data backups |
| P4 | Provider credentials, network access, integration monitoring, retry and reconciliation procedures |
| P5 | Financial migration safety, accounting reconciliation, sensitive-data controls |
| P6 | Stock transaction integrity, import handling, inventory performance |
| P7 | Payroll privacy, access controls, sensitive exports, retention |
| P8 | Attachment storage, scheduled depreciation, approval workflows |
| P9 | Bank statement storage, import limits, reconciliation recovery |
| P10 | Report performance, export limits, webhook delivery and retries |
| P11 | Administrative controls, support access, security review, operational capacity |
| P12 | Production release, recovery tests, monitoring, support handover |

Production credentials and customer data must not be copied into development or testing environments without an explicitly approved and appropriately protected process.

---

# 26. Release Strategy

The product should be released incrementally.

Recommended release stages:

## Stage A — Internal development

Purpose:
- Validate architecture.
- Test the core application.
- Identify integration and usability issues.

Restrictions:
- No external production claims.
- No unapproved use of real customer data.
- No assumption of regulatory compliance.

## Stage B — Internal pilot

Purpose:
- Validate end-to-end workflows with controlled users.
- Confirm core tenant, entitlement, and business rules.
- Gather implementation and usability feedback.

Requirements:
- Explicitly approved pilot scope.
- Known limitations documented.
- Appropriate access and data controls.
- Tested backup and recovery procedures for any real data.

## Stage C — Controlled customer pilot

Purpose:
- Validate a bounded release with selected customers.
- Evaluate actual workflows and operational demand.

Requirements:
- Formal pilot approval.
- Customer-facing limitations documented.
- Support and escalation process defined.
- Data protection and contractual requirements reviewed.
- Critical security and data-integrity defects resolved.

## Stage D — General availability

Purpose:
- Make the approved commercial scope generally available.

Requirements:
- Release criteria satisfied.
- Commercial module catalogue accurate.
- Pricing and entitlement behavior validated.
- Production monitoring and support operational.
- Required regulatory and provider reviews completed for applicable functionality.
- Product Owner approval recorded.

**General availability is a product decision, not an automatic result of reaching P12.**

---

# 27. Change Control

Changes to this roadmap must be reviewed when they affect:

- Product scope.
- Phase sequencing.
- Architecture.
- Tenant isolation.
- Module ownership.
- Subscription and entitlement rules.
- Financial integrity.
- Regulatory assumptions.
- Deployment requirements.
- Release criteria.

Every material change must record:

1. The proposed change.
2. The reason.
3. Affected requirements and modules.
4. Dependencies and risks.
5. Testing implications.
6. Deployment implications.
7. Approval decision.

Codex may propose changes but must not silently rewrite approved requirements or phase boundaries.

Minor corrections to spelling, formatting, and non-substantive documentation may be made without a formal architectural decision, provided they do not alter the intended meaning.

---

# 28. Roadmap Metrics

Track delivery progress using evidence-based measures.

Recommended metrics:

| Metric | Purpose |
|---|---|
| Approved requirements implemented | Measures requirement delivery |
| Requirements with passing acceptance tests | Measures verifiable acceptance coverage |
| Tasks completed with evidence | Measures traceable delivery |
| Open critical and high-severity defects | Measures release risk |
| Tenant-isolation test results | Measures a critical security control |
| Financial reconciliation failures | Measures financial integrity |
| CI success rate | Measures integration stability |
| Escaped defects | Measures defects discovered after phase approval |
| Migration test results | Measures schema-change reliability |
| Backup restore test results | Measures recovery readiness |
| Phase approval status | Measures governance progress |
| Open blocking decisions | Identifies work that cannot safely proceed |

Do not use code volume, number of generated files, or number of completed prompts as primary indicators of product progress.

A feature is complete when its required behavior is implemented and verified, not when code has been generated.

---

# 29. Recommended Implementation Order

The following order is recommended for the first development cycle.

1. Approve the master product specification and requirements.
2. Approve the initial module catalogue and roadmap.
3. Finalize the architecture and multi-tenancy contracts.
4. Establish repository conventions and Codex instructions.
5. Build the core platform and tenant-isolation tests.
6. Build subscription and entitlement services.
7. Implement the first CRM, sales, and invoicing workflow.
8. Validate the initial workflow with controlled users.
9. Finalize e-invoicing provider and regulatory decisions before committing to a production integration.
10. Implement accounting and VAT foundations.
11. Add procurement, inventory, HRMS, payroll, projects, expenses, fixed assets, and banking according to validated demand and dependency requirements.
12. Build reporting and integrations on stable domain contracts.
13. Complete enterprise-readiness and operational reviews.
14. Deploy the approved launch scope through a controlled release process.
15. Monitor the production system and prioritize improvements using observed customer needs and operational evidence.

This order prioritizes a secure, usable commercial foundation without requiring every planned ERP module to be completed before the first controlled pilot.

The final launch scope must be approved separately.

---

# 30. Final Governance Rule

This roadmap is a planning baseline, not permission for unrestricted implementation.

**The authoritative development sequence is:**

`Approved Requirements → Approved Architecture → Approved Phase Specification → Approved Tasks → Implementation → Automated Validation → Review → Human Approval → Next Phase`

Codex and supporting agents must preserve this sequence.

When a requirement is unclear, a dependency is missing, a security boundary is uncertain, or a financial or regulatory rule is unvalidated, the responsible agent must document the issue and request clarification rather than inventing a definitive answer.

The objective is to produce a maintainable, secure, commercially configurable, deployment-ready UAE ERP SaaS platform—not merely a collection of generated application features.