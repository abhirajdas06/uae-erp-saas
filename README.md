# UAE ERP SaaS Platform

A modular, multi-tenant Enterprise Resource Planning (ERP) platform designed for businesses operating in the United Arab Emirates (UAE).

The platform is intended to allow businesses to select and subscribe to the ERP modules they need, manage their operations through a unified application, and expand their subscriptions as their requirements grow.

This repository contains the product specifications, architecture documentation, development instructions, implementation plans, automated tests, deployment configuration, and application source code.

> **Project status:** Documentation and architecture planning.
>
> **Important:** The presence of a documented feature does not mean that it has been implemented, tested, released, or approved for production. Actual implementation status must be established from the source code, test results, release records, and approved project status documents.

---

## 1. Product Vision

Build a reliable, secure, modular ERP SaaS platform that helps UAE businesses manage their business operations through configurable subscriptions and integrated workflows.

The platform should support businesses that need a subset of ERP capabilities without requiring every customer to purchase the complete suite.

The system should provide:

- Modular subscriptions and configurable plans.
- Secure multi-tenant business environments.
- Role-based access control.
- Customer and sales management.
- Customer invoicing and financial operations.
- Accounting and UAE VAT functionality.
- UAE e-invoicing provider integration.
- Procurement and inventory management.
- Human resources and payroll.
- Projects, expenses, and fixed assets.
- Banking and financial workflows.
- Reporting, analytics, and external integrations.
- SaaS administration and subscription management.
- Production deployment, monitoring, backup, and recovery capabilities.

These are product objectives, not claims that the functionality currently exists.

The detailed requirements and implementation priorities are maintained in the product specifications and development roadmap.

---

## 2. Core Product Principles

### 2.1 Modular ERP

The ERP must be organized into well-defined functional modules.

Modules should have clear responsibilities, documented dependencies, controlled interfaces, and independently testable business logic.

A module must not become available to customers simply because its code exists. It must meet the project's implementation, verification, and commercial-release requirements.

### 2.2 Subscription-Based Access

Customers should be able to subscribe to an appropriate plan and select eligible modules according to the commercial model.

The platform must enforce module access on the server side.

Module availability, dependencies, subscription status, and applicable pricing should be controlled by approved configuration and business rules rather than scattered hardcoded conditions.

### 2.3 Multi-Tenant Security

The platform must isolate each customer's business data and enforce appropriate authorization throughout the application.

Tenant isolation must cover all applicable data access paths, including:

- Web requests.
- APIs.
- Background jobs.
- Reports and exports.
- File storage.
- Integrations.
- Administrative workflows.

Security must not depend solely on hiding interface elements.

### 2.4 Financial Integrity

Financial records must be accurate, traceable, and protected against unauthorized or inconsistent changes.

Accounting, taxation, invoicing, payroll, and payment workflows must follow explicitly documented business rules.

Monetary calculations, transaction boundaries, audit history, corrections, reversals, and duplicate-processing safeguards must be addressed where applicable.

### 2.5 UAE Market Requirements

The product is intended for businesses operating in the UAE.

Applicable tax, accounting, payroll, privacy, e-invoicing, and other regulatory requirements must be validated against current authoritative sources.

Regulatory interpretations, effective dates, provider capabilities, and unresolved questions must be documented.

The platform must not claim regulatory compliance or provider approval without sufficient evidence.

### 2.6 Production Readiness

Production readiness includes security, testing, deployment, monitoring, backup, restoration, recovery, and operational documentation.

A successful development build is not sufficient evidence that the system is ready for production.

---

## 3. Intended Technology Stack

The current intended technology direction is documented below. These choices must be confirmed against the approved architecture before implementation.

| Component | Intended technology | Purpose |
|---|---|---|
| Backend | Python and Django | Application logic and server-side workflows |
| API | Django REST Framework, where required | API endpoints and integrations |
| Database | PostgreSQL | Transactional and business data |
| Frontend | Django templates, HTMX, and Tailwind CSS | Server-rendered user interface and interactive workflows |
| Background processing | Celery and Redis, where required | Asynchronous jobs and scheduled processing |
| Application server | Gunicorn | Serving the Django application |
| Reverse proxy | Nginx | Request routing, TLS termination, and web serving |
| Containerization | Docker and Docker Compose | Reproducible development and suitable deployment workflows |
| Testing | pytest and pytest-django | Automated application testing |
| Version control | Git and GitHub | Source control and collaborative development |
| CI/CD | GitHub Actions or an approved alternative | Automated validation and delivery workflows |

### Architecture approach

The initial architectural preference is a **modular monolith**.

This approach keeps related business functionality in one deployable application while maintaining explicit module boundaries.

Microservices should not be introduced without a documented requirement and an approved architecture decision.

Additional infrastructure should be introduced only when justified by functionality, security, reliability, or operational needs.

---

## 4. ERP Module Overview

The following catalogue describes the intended functional scope. Final module boundaries, dependencies, commercial availability, and implementation order are governed by the approved module catalogue and roadmap.

| Module | Intended responsibility |
|---|---|
| Core Platform | Shared application capabilities and foundational services |
| Tenants | Tenant registration, organization configuration, and isolation |
| Users | User accounts, roles, and access management |
| Subscriptions | Subscription lifecycle, plans, renewals, and module entitlements |
| SaaS Billing | Charges, subscription invoices, and payments associated with the ERP SaaS service |
| CRM | Customer relationships, leads, and sales opportunities |
| Sales | Sales workflows and related business transactions |
| Invoicing | Invoices and related documents created by ERP customers for their own customers |
| UAE E-Invoicing | Integration with the selected and validated UAE e-invoicing provider |
| Accounting | General ledger and core accounting operations |
| VAT | Tax codes, VAT calculations, and applicable tax reporting |
| Procurement | Supplier and purchasing workflows |
| Inventory | Stock, warehouses, stock movements, and inventory controls |
| HRMS | Employee records and human resources workflows |
| Payroll | Payroll calculations and associated processes |
| Projects | Project planning, tracking, and project-related records |
| Expenses | Expense recording, approvals, and reimbursement workflows |
| Fixed Assets | Asset registers, depreciation, and asset lifecycle management |
| Banking and Finance | Bank transactions, reconciliation, and related financial workflows |
| Reporting and Integrations | Reporting, analytics, and external-system connectivity |
| SaaS Administration | Platform-level administration, support, and operational controls |

The final catalogue must identify which modules are foundational, optional, dependent on other modules, or independently sellable.

**SaaS billing and ERP customer invoicing are separate business functions and must remain clearly separated in the architecture.**

---

## 5. Development Roadmap

The project follows the approved 13-phase roadmap.

| Phase | Name | Primary objective |
|---|---|---|
| P00 | Foundation and Architecture | Establish requirements, architecture, development standards, and foundational tooling |
| P01 | Core Platform and Multi-Tenancy | Implement the foundational tenant-aware platform |
| P02 | Subscription Engine | Implement plans, module selection, subscription lifecycle, and SaaS billing foundations |
| P03 | CRM, Sales and Basic Invoicing | Implement initial customer, sales, and invoicing workflows |
| P04 | UAE E-Invoicing Integration | Integrate the selected provider according to validated requirements |
| P05 | Accounting and UAE VAT | Implement approved accounting and tax functionality |
| P06 | Procurement and Inventory | Implement purchasing, stock, and inventory workflows |
| P07 | HRMS and Payroll | Implement employee management and approved payroll functionality |
| P08 | Projects, Expenses and Fixed Assets | Implement project, expense, and asset workflows |
| P09 | Banking and Advanced Finance | Implement banking-related and advanced financial functionality |
| P10 | Reporting, Analytics and Integrations | Implement reporting and approved integration capabilities |
| P11 | Enterprise Readiness | Address advanced administration, reliability, security, and enterprise requirements |
| P12 | Production Launch and Operations | Validate production deployment, operational readiness, and launch requirements |

The roadmap defines intended sequencing. It does not authorize implementation of every phase.

Phase dependencies, scope, acceptance criteria, required tests, and approval gates must be documented before the corresponding implementation work begins.

---

## 6. Repository Structure

The repository is organized to separate product decisions, technical architecture, implementation phases, module specifications, agent instructions, quality standards, deployment guidance, and project status.

```text
uae-erp-saas/
│
├── AGENTS.md
├── README.md
├── CONTRIBUTING.md
├── docker-compose.yml
├── manage.py
│
├── docs/
│   ├── 00-product/
│   ├── 01-architecture/
│   ├── 02-phases/
│   ├── 03-modules/
│   ├── 04-agents/
│   ├── 05-quality/
│   ├── 06-deployment/
│   ├── 07-project-management/
│   ├── 08-requirements-traceability/
│   └── 09-templates/
│
├── orchestration/
│   ├── phase-manifest.yml
│   ├── task-manifest.yml
│   ├── notification-config.example.yml
│   └── schemas/
│
├── apps/
├── tests/
├── scripts/
│
└── .github/
    ├── workflows/
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

This is the intended repository organization, not a declaration that every directory or file already exists.

Create application files, infrastructure configuration, and automation when they are needed for an authorized task. Do not create non-functional placeholders solely to match this tree.

---

## 7. Documentation Navigation

### Product specifications

Location: `docs/00-product/`

| Document | Purpose |
|---|---|
| `MASTER_PRODUCT_SPECIFICATION.md` | Authoritative product vision, scope, and major requirements |
| `PRODUCT_REQUIREMENTS.md` | Functional and non-functional requirements |
| `TARGET_MARKET.md` | Target customers and UAE market considerations |
| `COMMERCIAL_MODEL.md` | Subscription, pricing, and module-selection principles |
| `MODULE_CATALOGUE.md` | Module definitions, boundaries, dependencies, and availability |
| `DEVELOPMENT_ROADMAP.md` | Implementation phases and sequencing |
| `GLOSSARY.md` | Controlled vocabulary for platform, financial and UAE regulatory terms |
| `REPORT_CATALOGUE.md` | Proposed launch report catalogue and report definition contract |
| `UAE_REGULATORY_SOURCE_REGISTER.md` | Dated regulatory sources, verification dates and revalidation requirements |

### Architecture

Location: `docs/01-architecture/`

Contains the system architecture, Django application structure, database design, tenant isolation, authentication, permissions, module dependencies, entitlements, API standards, background processing, and architecture decisions.

Also contains the UI design system and interaction standards, localization and bilingual interface standards, document numbering and sequence allocation, notifications and outbound communications, and tenant data migration, import and export.

### Phase specifications

Location: `docs/02-phases/`

Each implementation phase should contain its approved specification, MVP scope, tasks, acceptance criteria, test plan, and deployment requirements.

### Module specifications

Location: `docs/03-modules/`

Defines module responsibilities, business rules, data models, permissions, interfaces, dependencies, and testing requirements.

### Agent instructions

Location: `docs/04-agents/`

Defines the operating responsibilities, authority, required inputs, outputs, and handoff rules for the orchestrator and supporting development agents.

### Quality standards

Location: `docs/05-quality/`

Defines coding standards, testing strategy, security requirements, performance expectations, definition of done, and release criteria.

Also defines accessibility and browser support, the platform threat model, data protection and records retention, test data and fixtures, and developer onboarding and the contribution workflow. New contributors start at the root `CONTRIBUTING.md`.

### Deployment and operations

Location: `docs/06-deployment/`

Defines deployment architecture, infrastructure requirements, environment configuration, deployment instructions, backup and recovery, monitoring, and operational procedures.

### Project management

Location: `docs/07-project-management/`

Maintains current project status, phase status, risks, unresolved decisions, and change history.

### Traceability and templates

Locations:

- `docs/08-requirements-traceability/`
- `docs/09-templates/`

The traceability documentation connects requirements to implementation tasks and verification evidence. Templates provide consistent formats for specifications, tasks, test plans, architecture decisions, and completion reports.

---

## 8. Development Workflow

All development must follow a controlled, documented process.

### Step 1: Understand the task

Read the applicable repository instructions and approved specifications.

Inspect existing code and tests before planning changes.

### Step 2: Confirm scope

Identify the task's objective, dependencies, affected components, acceptance criteria, and required approvals.

Raise conflicts or missing requirements before implementation.

### Step 3: Plan the implementation

Define a bounded implementation plan.

Identify relevant security, tenant-isolation, financial-integrity, and integration concerns.

### Step 4: Implement

Make only the changes required by the authorized task.

Follow approved architecture and coding standards.

### Step 5: Test

Run relevant automated tests and other required checks.

Add regression tests for changed behavior and security tests for applicable access boundaries.

### Step 6: Review

Obtain the required code, security, and functional reviews.

Resolve blocking findings before acceptance.

### Step 7: Document

Update relevant specifications, operational documentation, status records, and change history.

### Step 8: Verify completion

Record actual test results, review outcomes, outstanding issues, and required approvals.

Do not report completion without the evidence required by the task or phase.

### Step 9: Obtain phase approval

The orchestrator may prepare a phase completion report, but the next phase must not begin until its required approval has been granted.

---

## 9. Agent Orchestration Principles

The project may use specialized agents for architecture, implementation, testing, security review, code review, DevOps, and documentation.

The orchestrator coordinates those agents using the approved specifications and task manifests.

Agents must:

- Operate within their assigned scope.
- Use the same authoritative requirements.
- Identify dependencies before making shared changes.
- Avoid conflicting edits to shared files.
- Provide verifiable outputs.
- Report failures and blockers honestly.
- Escalate decisions outside their authority.

Parallel execution is appropriate for independent tasks. Shared database models, migrations, security-sensitive components, and common interfaces require explicit coordination.

Automation must not independently authorize production deployment, destructive database operations, or material architectural changes.

Notifications must reflect verified status rather than unverified completion claims.

---

## 10. Security and Regulatory Considerations

Security and regulatory considerations must be incorporated into design, implementation, testing, and deployment.

The project must address, as applicable:

- Tenant isolation.
- Authentication and authorization.
- Secure session and secret management.
- Protection of personal and financial information.
- Auditability of important business operations.
- Secure file handling.
- Background task authorization.
- Dependency and vulnerability management.
- Backup protection and recovery.
- External integration security.
- Applicable UAE privacy, tax, payroll, and e-invoicing requirements.

Regulatory requirements must be verified using current authoritative sources.

Provider selection, data residency, applicable statutory deadlines, and compliance obligations must be documented and validated rather than assumed.

---

## 11. Testing and Release Standards

Each implementation phase must define its own acceptance criteria and required tests.

The overall testing strategy should include:

- Unit tests.
- Database and model tests.
- Service-layer tests.
- API and view tests.
- Permission and tenant-isolation tests.
- Integration tests.
- Financial calculation tests.
- Regression tests.
- Relevant end-to-end tests.
- Security checks.
- Deployment validation.

The project's definition of done and release criteria determine whether a change or phase is accepted.

A passing test suite is necessary where required, but does not independently establish regulatory compliance or production readiness.

---

## 12. Deployment and Operations

Deployment documentation must be developed alongside the application rather than postponed until the final phase.

The project must document:

- Supported deployment architecture.
- Infrastructure sizing and assumptions.
- Application configuration.
- PostgreSQL and Redis configuration, where applicable.
- Domain, DNS, and TLS.
- Background workers and scheduled jobs.
- Static and uploaded file handling.
- Secrets management.
- Database migration procedures.
- Backup and restoration.
- Monitoring and alerting.
- Rollback and recovery.
- Incident response.
- Security updates.
- Scaling considerations.
- Estimated operational costs.

Infrastructure estimates must distinguish assumptions from verified provider pricing.

Production deployment requires explicit authorization and satisfaction of the approved release criteria.

---

## 13. Current Project Status

The initial project activity is to establish and validate the product documentation and development control system.

The intended initial milestones are:

1. Establish repository-wide development instructions.
2. Establish this README and documentation index.
3. Define the authoritative product specification.
4. Define functional and non-functional requirements.
5. Establish the commercial model and module catalogue.
6. Approve the implementation roadmap.
7. Define and review the technical architecture.
8. Establish agent instructions, documentation templates, and orchestration rules.
9. Define phase-level acceptance criteria and verification requirements.
10. Begin implementation only after the applicable scope has been approved.

The actual status of each milestone must be maintained in the project management documents.

Do not infer completion from this list.

---

## 14. Project Decision and Change Management

Material changes to product scope, architecture, commercial rules, security requirements, financial behavior, regulatory assumptions, or phase dependencies must be documented.

Where appropriate, record decisions as Architecture Decision Records (ADRs) under:

`docs/01-architecture/ARCHITECTURAL_DECISIONS/`

Each decision should include:

- Context.
- Problem or requirement.
- Options considered.
- Decision.
- Rationale.
- Consequences and trade-offs.
- Status.
- Date and approver, where applicable.

Unresolved decisions must be tracked in the project management documentation.

Agents must not silently replace approved decisions with their own preferences.

---

## 15. Definition of Success

The project will be successful when it delivers a modular ERP SaaS platform that:

- Provides well-defined, integrated business modules.
- Enforces subscription entitlements and tenant isolation.
- Preserves financial integrity and appropriate audit history.
- Implements validated UAE business and regulatory requirements.
- Has appropriate automated test coverage and documented verification evidence.
- Can be deployed and operated using documented procedures.
- Supports reliable backup, restoration, monitoring, and recovery.
- Has clearly defined commercial plans and module dependencies.
- Can be maintained and extended without uncontrolled coupling.
- Makes truthful, evidence-based claims about its capabilities and readiness.

All success criteria must ultimately be translated into measurable requirements and acceptance tests.

---

## 16. Getting Started

Before implementing features:

1. Read `AGENTS.md`.
2. Review the product specifications in `docs/00-product/`.
3. Review the approved architecture in `docs/01-architecture/`.
4. Review the relevant phase and module specifications.
5. Confirm the authorized task and acceptance criteria.
6. Inspect the existing repository and development environment.
7. Implement only the authorized scope.
8. Run required tests and checks.
9. Update documentation and status records.
10. Report actual results and unresolved issues.

If a required specification does not yet exist, identify the missing document and create or request approval for it as appropriate.

Do not substitute guessed requirements for missing approved specifications.

---

## 17. Final Rule

**Build from approved requirements, implement in controlled phases, verify with evidence, and obtain approval before advancing through gated milestones.**

Security, tenant isolation, financial integrity, maintainability, and truthful reporting take priority over implementation speed.