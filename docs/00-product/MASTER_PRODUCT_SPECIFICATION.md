# Master Product Specification
## Modular UAE ERP SaaS Platform

| Property | Value |
|---|---|
| Product | UAE ERP SaaS |
| Document ID | PROD-MASTER-001 |
| Version | 1.0 |
| Status | APPROVED — Product Planning Baseline; Regulatory and Launch Decisions Pending |
| Target Market | United Arab Emirates |
| Product Type | Multi-tenant, modular ERP SaaS |
| Primary Backend | Python and Django |
| Primary Database | PostgreSQL |
| Document Owner | Product Owner |
| Review Frequency | At each major product or architecture milestone |

---

# 1. Purpose of This Document

This document defines the overall product vision, business objectives, functional boundaries, architectural principles, security expectations, commercial model, and implementation direction for the UAE ERP SaaS platform.

It is the primary product reference for the project.

All subsequent product, architecture, module, phase, testing, deployment, and agent specifications must be consistent with this document or explicitly document an approved deviation.

This document serves as the foundation for:

- Product requirements.
- Technical architecture.
- Module specifications.
- Database design.
- Subscription and entitlement design.
- Implementation phases.
- Automated testing.
- Security and compliance reviews.
- Deployment and operations.
- Product release decisions.

## 1.1 Document Status

This is an initial product specification.

It establishes the proposed product direction but does not imply that every requirement has been finalized or approved.

Requirements are classified as follows:

| Classification | Meaning |
|---|---|
| Confirmed Direction | An explicitly established project objective or architectural direction |
| Proposed Default | A recommended approach that remains subject to approval where material |
| Pending Decision | A question that requires a decision before the affected functionality is finalized |
| Externally Validated Requirement | A requirement supported by an identified, authoritative external source and verified for applicability |
| Implemented | Functionality verified in the application code |
| Accepted | Functionality or a deliverable that has satisfied its applicable acceptance criteria |

A requirement must not be marked implemented or accepted solely because it appears in this document.

External regulatory requirements must not be marked validated without supporting evidence.

---

# 2. Product Vision

Build a secure, modular, scalable, and commercially viable ERP Software-as-a-Service platform for businesses operating in the United Arab Emirates.

The platform should allow each business to select the operational modules it needs, subscribe to an appropriate plan, and manage its business activities through a unified application.

Rather than requiring every customer to purchase a complete ERP suite, the platform should support configurable module combinations, subject to module dependencies and commercial rules.

The system should provide a common foundation for customer management, sales, invoicing, accounting, taxation, procurement, inventory, human resources, payroll, projects, expenses, fixed assets, banking, and reporting.

The long-term objective is to provide an integrated business management platform that can serve different business sizes and operational requirements without sacrificing data isolation, financial integrity, maintainability, or operational reliability.

## 2.1 Product Mission

Provide businesses with an adaptable ERP platform in which customers can purchase the capabilities they need and expand their use of the platform as their businesses grow.

## 2.2 Core Value Proposition

The platform is intended to deliver the following benefits:

1. **Modularity:** Customers can select suitable modules instead of being required to purchase every capability.
2. **Integrated operations:** Related business processes can share data through controlled interfaces.
3. **Operational visibility:** Authorized users can access relevant business information and reports.
4. **Configurable subscriptions:** Plans, module entitlements, and commercial rules can be managed centrally.
5. **Security:** Customer data is isolated and access is controlled through server-side authorization.
6. **Financial reliability:** Financial operations use explicit business rules, transaction controls, and auditability.
7. **Extensibility:** New modules and integrations can be introduced without uncontrolled coupling.
8. **Operational readiness:** Deployment, monitoring, backup, restoration, and maintenance are part of the product's engineering requirements.

These are intended product benefits. Their achievement must be demonstrated through implementation and verification.

---

# 3. Product Objectives

The platform must be designed to achieve the following objectives.

## 3.1 Business Objectives

- Establish a modular ERP SaaS offering for UAE businesses.
- Allow configurable subscription plans and module combinations.
- Support recurring subscription revenue.
- Allow customers to add or remove eligible modules according to defined subscription rules.
- Support customer onboarding and organization configuration.
- Enable centralized SaaS administration.
- Provide a foundation for adding integrations and additional ERP capabilities.
- Support a commercially sustainable deployment and operating model.

## 3.2 Technical Objectives

- Establish a maintainable Django-based application.
- Use PostgreSQL for transactional business data.
- Maintain clear module boundaries.
- Enforce tenant isolation across all relevant application layers.
- Enforce permissions and subscription entitlements on the server side.
- Maintain automated tests for critical business rules.
- Provide repeatable development and deployment workflows.
- Support safe database migrations and data recovery.
- Establish appropriate logging, monitoring, and auditability.
- Avoid unnecessary infrastructure and premature architectural complexity.

## 3.3 Regulatory Objectives

The product must be designed to accommodate applicable UAE business and regulatory requirements.

The applicable requirements must be identified and validated for the intended customer types, business activities, and effective dates.

Areas requiring investigation include:

- UAE VAT.
- UAE e-invoicing.
- Accounting and financial recordkeeping.
- Payroll and employment-related obligations.
- Personal data protection.
- Data hosting and cross-border data transfers, where applicable.
- Record retention.
- Electronic document integrity.
- Applicable industry-specific requirements.

This specification does not establish that the platform is compliant with any particular law or regulation.

---

# 4. Target Market

## 4.1 Primary Market

The initial target market is businesses operating in the United Arab Emirates.

Potential customer segments include:

- Small and medium-sized businesses.
- Trading and distribution businesses.
- Retail and wholesale businesses.
- Service providers.
- Project-based businesses.
- Businesses managing inventory and procurement.
- Businesses requiring integrated financial and operational records.
- Organizations that need employee management and payroll capabilities.

These segments are candidate markets. Their prioritization, specific requirements, and willingness to pay must be validated through market research.

## 4.2 Customer Profiles

The platform should accommodate different operational requirements without assuming that all customers need the same configuration.

Illustrative profiles include:

### Profile A: Service Business

Potential requirements:

- CRM.
- Sales.
- Invoicing.
- Accounting.
- VAT.
- Expenses.
- Projects.
- Reporting.

### Profile B: Trading Business

Potential requirements:

- CRM.
- Sales.
- Invoicing.
- Accounting.
- VAT.
- Procurement.
- Inventory.
- Banking.
- Reporting.

### Profile C: Project-Based Business

Potential requirements:

- CRM.
- Sales.
- Invoicing.
- Accounting.
- VAT.
- Projects.
- Expenses.
- Fixed Assets.
- Reporting.

### Profile D: Business With Employees

Potential requirements:

- Core Platform.
- Users and Permissions.
- HRMS.
- Payroll.
- Accounting.
- Reporting.

These profiles illustrate possible module combinations. They are not predefined commercial plans.

The final plans must be established in `COMMERCIAL_MODEL.md`.

## 4.3 Customer Configuration

Each customer organization may require configuration for:

- Legal and trading names.
- Registered business address.
- Country and applicable jurisdiction.
- Default currency.
- Time zone.
- Financial year.
- Invoice numbering.
- Tax registrations and tax settings, where applicable.
- User roles and permissions.
- Enabled modules.
- Subscription plan.
- Business-specific preferences.
- Applicable accounting settings.

The exact configuration fields and validation requirements must be defined in the relevant module specifications.

---

# 5. Product Scope

## 5.1 Included in the Intended Product

The intended product includes the following capabilities.

### A. SaaS Platform

- Tenant registration and onboarding.
- Organization configuration.
- User and role management.
- Authentication and session management.
- Subscription management.
- Module selection and entitlements.
- Plan configuration.
- SaaS administration.
- Subscription billing.
- Auditability of important administrative operations.

### B. CRM and Sales

- Customer and prospect records.
- Contact management.
- Lead management.
- Sales opportunities.
- Sales workflows.
- Sales documents.
- Customer activity history.
- Integration with invoicing and reporting where appropriate.

### C. Invoicing

- Customer invoices.
- Invoice line items.
- Invoice numbering.
- Invoice statuses.
- Applicable tax calculations.
- Credit notes and corrections, subject to approved business rules.
- Customer payment tracking.
- PDF or other supported document generation.
- Invoice history and auditability.
- Integration with accounting.
- Integration with the selected e-invoicing provider where required.

### D. UAE E-Invoicing

- Provider integration.
- Provider configuration.
- Submission workflows.
- Submission status tracking.
- Error handling.
- Retry and duplicate-submission safeguards.
- Reconciliation of local and provider-side statuses.
- Retention of relevant transaction references and responses.
- Monitoring of failed submissions.

The final requirements depend on the validated UAE regulatory framework, the selected provider, and the provider's documented interface.

### E. Accounting and VAT

- Chart of accounts.
- Journal entries.
- General ledger.
- Accounts receivable.
- Accounts payable.
- Financial periods.
- Financial reporting.
- VAT configuration.
- Tax calculations.
- Tax-related reporting.
- Reconciliation.
- Financial audit history.

The final accounting and tax scope must be defined against applicable requirements and approved accounting policies.

### F. Procurement and Inventory

- Supplier management.
- Purchase requests and purchase orders, where required.
- Goods receipt.
- Inventory locations.
- Stock movements.
- Stock balances.
- Inventory adjustments.
- Inventory valuation.
- Purchase-related workflows.
- Integration with accounting.

### G. HRMS and Payroll

- Employee records.
- Organizational structure.
- Leave management.
- Attendance-related functionality, where included.
- Payroll calculations.
- Payroll records.
- Payroll approvals.
- Relevant financial postings.
- Applicable statutory reports and integrations.

Payroll rules must be validated for the intended customer categories and employment arrangements.

### H. Projects, Expenses, and Fixed Assets

- Project records.
- Project tasks and status tracking.
- Project-related expenses.
- Expense submissions and approvals.
- Expense reimbursement records.
- Fixed asset registers.
- Depreciation calculations.
- Asset transfers, disposals, and adjustments.

### I. Banking and Finance

- Bank account records.
- Bank transaction imports where supported.
- Reconciliation workflows.
- Payment tracking.
- Financial summaries.
- Relevant accounting integration.

Bank feeds and direct bank connectivity must be treated as separate integration capabilities, not assumed to be available by default.

### J. Reporting and Integrations

- Operational reports.
- Financial reports.
- Dashboards.
- Data exports.
- Approved external integrations.
- API access where included in the applicable plan.
- Background processing for appropriate reporting and integration tasks.

### K. Administration and Operations

- SaaS administration.
- Subscription administration.
- Tenant support workflows.
- Audit logs.
- System health monitoring.
- Background job monitoring.
- Backup and recovery procedures.
- Security controls.
- Release and deployment procedures.

## 5.2 Explicitly Outside Initial Scope Unless Approved

The following are not automatically included in the initial release:

- Native mobile applications.
- A marketplace for third-party extensions.
- Microservices architecture.
- AI-driven autonomous accounting.
- AI-driven autonomous payroll processing.
- Unverified regulatory integrations.
- Direct integrations with every UAE bank.
- Every possible payment gateway.
- Every possible external accounting system.
- Country-specific tax functionality outside the approved initial market.
- Industry-specific functionality without an approved business case.
- Unlimited customization of individual customer workflows.
- Guaranteed legal, tax, or accounting outcomes.
- Automated production deployment without required approvals.

These capabilities may be considered in later releases.

---

# 6. Product and System Boundaries

The product consists of two related but distinct business domains.

## 6.1 SaaS Provider Domain

This domain is operated by the company providing the ERP platform.

It manages:

- Customer subscriptions to the SaaS platform.
- Subscription plans.
- Module catalogue.
- Pricing configuration.
- Subscription invoices.
- SaaS payment status.
- Subscription lifecycle.
- Entitlements.
- SaaS administration.
- Platform-level operational records.

## 6.2 Customer ERP Domain

This domain is used by customer organizations to manage their own businesses.

It manages, as applicable:

- Their customers and suppliers.
- Their sales and purchases.
- Their invoices.
- Their financial records.
- Their employees and payroll records.
- Their inventory and assets.
- Their projects and expenses.
- Their tax-related business records.

## 6.3 Mandatory Separation

The following distinction is fundamental:

**SaaS subscription billing is not the same as ERP customer invoicing.**

For example:

- The SaaS provider may invoice a customer organization for its monthly ERP subscription.
- That customer organization may use the ERP invoicing module to invoice its own customers.

These are separate transactions with different ownership, permissions, numbering rules, business rules, and accounting implications.

The architecture must not conflate them.

---

# 7. Multi-Tenancy Requirements

## 7.1 Tenant Model

The platform is intended to serve multiple customer organizations through a shared application.

Each customer organization is represented by a tenant.

A tenant may contain:

- Organization settings.
- Users and memberships.
- Business records.
- Module entitlements.
- Subscription references.
- Audit events.
- Integration configuration.
- Files and generated documents.
- Other tenant-owned data.

The final data model must define the relationships between tenants, users, subscriptions, and business records.

## 7.2 Isolation Requirements

The platform must prevent unauthorized access to another tenant's data.

Tenant isolation must be enforced across:

- Database queries.
- Service-layer operations.
- Views and API endpoints.
- Background jobs.
- Scheduled tasks.
- File access.
- Exports and reports.
- Search functionality.
- Caching.
- Integration callbacks.
- Administrative workflows.

Every tenant-owned object must have a documented ownership and authorization model.

## 7.3 Proposed Technical Direction

The proposed default is:

- A shared PostgreSQL database.
- Tenant identifiers on applicable tenant-owned business records.
- Centralized tenant-resolution and authorization mechanisms.
- Explicit tenant scoping in data-access paths.
- Database constraints where appropriate.
- Automated tests for cross-tenant access.
- Consideration of PostgreSQL Row-Level Security (RLS) as an additional isolation layer.

The precise implementation of tenant resolution, transaction handling, connection pooling, background tasks, and RLS must be established in the approved architecture.

RLS must not be treated as automatically safe merely because policies exist. The design must account for database roles, connection reuse, transaction boundaries, and how tenant context is established and cleared.

## 7.4 Platform-Level Administration

Platform administrators may need access to tenant metadata and support functions.

Any elevated access to customer business data must be explicitly authorized, narrowly scoped, appropriately logged, and consistent with applicable privacy and contractual obligations.

Administrative access must not become an unrestricted bypass of tenant-isolation controls.

---

# 8. Modular Architecture

## 8.1 Architectural Approach

The intended architecture is a modular monolith.

The application should have one primary deployable Django application initially, with functional modules separated through explicit responsibilities and interfaces.

Modules may contain their own models, services, views, forms, tasks, permissions, and tests, depending on their complexity.

Shared capabilities must be provided through clearly defined interfaces rather than duplicated implementations.

## 8.2 Module Independence

A module must not directly depend on the internal implementation details of unrelated modules without an approved reason.

Cross-module interactions should use documented interfaces, services, or events where appropriate.

For example:

- Invoicing may request accounting postings through an approved accounting interface.
- Inventory may generate accounting events through an approved integration boundary.
- Payroll may create accounting entries through an approved posting service.
- Subscription management may update entitlements through the approved entitlement mechanism.
- E-invoicing may receive invoice data through a defined integration contract.

These examples describe intended boundaries. The actual interfaces must be documented and tested.

## 8.3 Module Lifecycle

Each module should have a defined lifecycle.

Suggested states include:

- Proposed.
- Specified.
- In Development.
- Implemented.
- Testing.
- Accepted.
- Available for Sale.
- Deprecated.

The exact state model must be defined in the module catalogue and release process.

A module must not be marked available for sale merely because its database models or interface screens exist.

## 8.4 Shared Platform Services

Potential shared services include:

- Tenant resolution.
- Authentication.
- Authorization.
- Entitlement evaluation.
- Audit logging.
- Notifications.
- File handling.
- Numbering services.
- Currency and precision handling.
- Integration infrastructure.
- Background task infrastructure.
- Error reporting.
- Shared reporting utilities.

The architecture must determine which capabilities belong in the core platform and which belong in business modules.

---

# 9. Subscription and Entitlement Model

## 9.1 Commercial Principle

Customers should be able to purchase an eligible combination of modules according to the approved commercial model.

The platform should support configurable subscription plans and module-based entitlements.

The final pricing structure, billing cadence, minimum subscription rules, and payment policies remain subject to approval in `COMMERCIAL_MODEL.md`.

## 9.2 Entitlement Enforcement

An entitlement determines whether a tenant is authorized to use a particular module or capability.

Entitlements must be evaluated on the server side.

User-interface visibility may reflect entitlements, but it is not an authorization mechanism.

The entitlement system must support, where applicable:

- Tenant identification.
- Subscription status.
- Enabled modules.
- Plan restrictions.
- Module dependencies.
- Effective dates.
- Grace periods, if approved.
- Feature restrictions.
- Administrative overrides, if approved.
- Auditable changes.

## 9.3 Module Dependencies

A module may require another module or a shared platform capability.

For example, advanced accounting workflows may depend on the core platform and appropriate invoicing or financial interfaces.

The final dependency graph must be explicit, validated, and free of unintended circular dependencies.

The subscription engine must prevent invalid module combinations.

## 9.4 Subscription Lifecycle

The final design must define behavior for:

- Subscription creation.
- Initial activation.
- Module additions.
- Module removals.
- Plan changes.
- Renewals.
- Failed payments.
- Grace periods, if applicable.
- Suspension.
- Cancellation.
- Reactivation.
- Expiration.
- Data retention after cancellation.
- Export or retrieval of customer data.

The system must not assume that subscription expiration immediately authorizes permanent deletion of business data.

Data retention, customer access, suspension, and deletion policies must be documented and validated before implementation.

---

# 10. Authentication, Users, and Permissions

The platform must implement a clear authorization model.

The detailed design belongs in `AUTHENTICATION_AND_PERMISSIONS.md`.

At minimum, the model must distinguish:

- Platform-level administrators.
- Tenant-level administrators.
- Tenant users.
- Role-based permissions.
- Module entitlements.
- Object-level authorization where required.
- Background service identities.
- Integration credentials and service access.

Authorization must consider the relevant combination of tenant, user, role, action, object ownership, and module entitlement.

The system must not assume that a user who can access one module is authorized to access every module.

High-risk operations should require appropriate permissions and auditability.

Examples include:

- Posting financial transactions.
- Approving payroll.
- Changing tax configuration.
- Modifying subscription entitlements.
- Exporting sensitive data.
- Changing user permissions.
- Accessing support-level administrative functions.

The final role matrix and approval workflows must be documented before implementation of the affected functionality.

---

# 11. Financial Integrity and Auditability

## 11.1 Financial Data Principles

Financial data must be accurate, traceable, and consistent.

The system must use explicit rules for:

- Monetary precision.
- Currency handling.
- Rounding.
- Tax calculation.
- Transaction boundaries.
- Posting and reversal.
- Document numbering.
- Duplicate processing.
- Corrections.
- Reconciliation.
- Period closure, where applicable.

Monetary calculations should use appropriate decimal representations rather than binary floating-point arithmetic.

## 11.2 Transaction Integrity

Related financial operations must use appropriate database transactions.

The implementation must address:

- Partial failure.
- Concurrent updates.
- Duplicate requests.
- Retry behavior.
- Database constraints.
- Idempotency where applicable.
- Rollback behavior.
- Consistency between source documents and accounting records.

## 11.3 Auditability

Important operations should create suitable audit records.

Examples include:

- Financial posting.
- Invoice issuance and correction.
- Permission changes.
- Tax configuration changes.
- Subscription changes.
- Payroll approval.
- Inventory adjustments.
- Administrative access to sensitive records.

Audit records should capture relevant actors, timestamps, actions, object references, and appropriate change details.

Audit logging must avoid unnecessary exposure of secrets or sensitive personal information.

The final audit model and retention requirements must be documented in the architecture and applicable module specifications.

## 11.4 Posted Financial Records

The design must define when a record becomes posted or otherwise financially authoritative.

Where appropriate, posted financial records should be corrected through controlled reversals, credit notes, adjustments, or other approved workflows rather than silently overwritten or deleted.

Exact rules must follow the approved accounting and regulatory requirements.

---

# 12. UAE Business and Regulatory Requirements

## 12.1 General Rule

The platform is intended for UAE businesses, but the applicability of specific legal requirements may differ according to customer circumstances.

The product must not assume that every customer has identical VAT obligations, payroll arrangements, reporting requirements, or e-invoicing obligations.

Regulatory applicability must be established for the intended customer types and validated against current authoritative sources.

## 12.2 UAE VAT

The VAT module must be designed around validated tax requirements.

The specification must eventually address:

- Tax registrations and relevant identifiers.
- Tax codes and applicable rates.
- Taxable, exempt, and zero-rated treatments where applicable.
- Tax-inclusive and tax-exclusive pricing.
- Tax calculation and rounding.
- Credit notes and adjustments.
- Input and output VAT records.
- Tax-period reporting.
- Relevant accounting entries.
- Tax-related audit history.

The applicable tax rules, exceptions, effective dates, and reporting requirements must be verified.

Do not hardcode unverified tax assumptions into shared business logic.

## 12.3 UAE E-Invoicing

The e-invoicing module must be designed around the validated regulatory requirements and the selected provider's documented integration contract.

The implementation must address, as applicable:

- Applicable invoice and transaction types.
- Required data fields.
- Data validation.
- Document and message formats.
- Submission requirements.
- Acknowledgements and statuses.
- Rejection handling.
- Retry behavior.
- Duplicate prevention.
- Provider outages.
- Reconciliation.
- Record retention.
- Operational monitoring.
- Provider changes and versioning.

Before implementation, the project must establish:

1. The applicable UAE requirements and their effective dates.
2. Which customer categories and transactions are in scope.
3. The appropriate provider or integration route.
4. Provider capabilities and commercial terms.
5. Authentication and connectivity requirements.
6. Required testing and acceptance procedures.
7. Error-handling and support responsibilities.

No provider must be described as approved or accredited without verification against the relevant authoritative source.

The platform must not claim regulatory compliance solely because invoices can be submitted successfully to a provider.

## 12.4 Payroll and Employment Requirements

Payroll functionality must be based on validated requirements applicable to the intended customer and employee categories.

The project must investigate relevant requirements concerning:

- Employee records.
- Salary components.
- Allowances and deductions.
- Payroll periods.
- Leave and attendance inputs.
- End-of-service calculations where applicable.
- Applicable payment and reporting processes.
- Required records and retention.
- Relevant external integrations.

The precise scope must be established before implementing statutory payroll calculations.

## 12.5 Privacy and Data Protection

The platform must identify applicable personal data protection obligations.

The design must consider:

- Purpose limitation.
- Data minimization.
- Access controls.
- Data retention.
- Data export.
- Correction and deletion workflows where legally applicable.
- Auditability.
- Data processing by external providers.
- Cross-border transfers where relevant.
- Incident response.
- Customer and provider responsibilities.

Hosting location and data residency requirements must be validated rather than assumed.

## 12.6 Regulatory Evidence Register

Regulatory requirements should be tracked with the following information:

| Field | Description |
|---|---|
| Requirement ID | Unique requirement identifier |
| Regulatory area | VAT, e-invoicing, payroll, privacy, or another applicable area |
| Requirement | Concise description |
| Source | Official source or authoritative reference |
| Source date | Publication or effective date, where available |
| Verification date | Date the source was reviewed |
| Applicability | Customer categories and conditions |
| Product impact | Affected modules and workflows |
| Status | Pending, verified, requires review, or superseded |
| Reviewer | Responsible reviewer |
| Evidence | Supporting notes, references, or approved interpretation |

The project must maintain this evidence as part of requirements traceability.

---

# 13. User Experience Requirements

The application should provide a consistent and efficient business interface.

The detailed design system and interaction patterns must be established separately.

The intended experience should prioritize:

- Clear navigation.
- Consistent layouts.
- Responsive design.
- Accessible forms and controls.
- Effective search and filtering.
- Useful validation messages.
- Clear business statuses.
- Efficient data-entry workflows.
- Appropriate empty states.
- Consistent error handling.
- Role-appropriate dashboards.
- Clear module availability.
- Useful loading and processing feedback.

The user interface must not expose modules or actions as usable when the current tenant lacks the necessary entitlement or authorization.

Hiding unavailable modules is a usability measure, not a security boundary.

The frontend direction is Django templates, HTMX, and Tailwind CSS unless an approved architecture decision changes it.

A separate single-page application or native mobile application is not part of the initial scope unless approved.

---

# 14. Reporting and Data Export

Reporting must respect tenant isolation, permissions, and module entitlements.

The platform should support operational and financial reporting according to the modules available to each tenant.

The reporting design must address:

- Report definitions.
- Filtering.
- Date ranges.
- Currency and precision.
- Time-zone handling.
- Tenant-scoped data access.
- Large-result processing.
- Export permissions.
- Background report generation where required.
- Auditability of sensitive exports.
- Performance limits.

Reports must use approved business rules and must not calculate financial totals differently from the authoritative underlying records without an explicitly documented reason.

The initial report catalogue remains to be defined.

---

# 15. External Integrations

External integrations must use documented interfaces and controlled configuration.

Potential integration categories include:

- UAE e-invoicing providers.
- Payment gateways.
- Banking services.
- Email delivery.
- SMS or messaging providers.
- Identity services.
- Document storage.
- External accounting or business systems.
- Reporting and data export tools.

These are candidate integration categories, not commitments to support every provider.

For each approved integration, the relevant specification must document:

- Purpose.
- Provider selection.
- Supported capabilities.
- Authentication.
- Data exchanged.
- Timeouts and retries.
- Idempotency.
- Error handling.
- Rate limits.
- Logging.
- Secrets management.
- Testing.
- Provider dependencies.
- Expected operational costs where relevant.

Provider-specific logic should be isolated from unrelated business logic.

---

# 16. Non-Functional Requirements

The product must define measurable non-functional requirements before production acceptance.

The following areas require explicit targets.

## 16.1 Security

Requirements must address authentication, authorization, tenant isolation, secrets, input validation, dependency security, file handling, logging, and vulnerability remediation.

## 16.2 Performance

The project must establish target response times, expected workloads, database performance expectations, and acceptable background-processing delays.

Targets must be based on expected usage and validated through testing.

## 16.3 Availability and Reliability

The project must define service availability objectives, maintenance expectations, failure handling, and recovery procedures.

Availability commitments must not be published until supported by the deployment design and operating model.

## 16.4 Scalability

The architecture must support growth in:

- Tenants.
- Users.
- Business records.
- Transactions.
- Background jobs.
- Uploaded files.
- Reporting workloads.

Scaling strategies must be supported by evidence and operational requirements.

## 16.5 Maintainability

The application must use consistent coding standards, modular design, automated tests, and documented interfaces.

Technical debt and architectural compromises must be recorded and reviewed.

## 16.6 Observability

The platform must provide suitable logs, metrics, alerts, and diagnostic information.

Observability must support troubleshooting without unnecessarily exposing sensitive information.

## 16.7 Backup and Recovery

The deployment design must establish backup frequency, retention, restoration testing, recovery objectives, and responsibilities.

Recovery Point Objective (RPO) and Recovery Time Objective (RTO) must be explicitly defined before production approval.

## 16.8 Accessibility and Compatibility

The project must define supported browsers, responsive behavior, accessibility expectations, and any relevant device constraints.

## 16.9 Internationalization

The platform should be designed to support the formatting and configuration needs of UAE businesses.

The following capabilities require explicit design decisions:

- Time zones.
- Date and number formatting.
- Currency formatting.
- Arabic and English interface requirements.
- Right-to-left layout.
- Multilingual business documents.
- Character encoding.
- Locale-aware search and sorting.

Arabic-language support, right-to-left layouts, and other localization capabilities must be assigned explicit scope and acceptance criteria rather than assumed complete.

---

# 17. Data Management and Retention

The platform must define how business data is created, updated, retained, exported, archived, and deleted.

The data lifecycle must address:

- Tenant onboarding.
- Business record creation.
- Import and migration.
- Document storage.
- Audit history.
- Subscription suspension.
- Subscription cancellation.
- Customer data export.
- Retention obligations.
- Deletion eligibility.
- Backup expiration.
- Legal holds where applicable.
- Data restoration.

Customer cancellation must not automatically trigger irreversible deletion of all associated data.

The correct handling depends on contractual commitments, applicable law, financial recordkeeping requirements, and approved retention policies.

Sensitive data must not be copied into logs, test fixtures, or development environments without an approved and appropriate purpose.

---

# 18. SaaS Administration

The platform requires a separate administration capability for operating the SaaS service.

The initial administrative scope should be defined to cover, where approved:

- Tenant management.
- Subscription administration.
- Plan and module configuration.
- Entitlement management.
- Subscription status.
- Operational health.
- Background task monitoring.
- Integration status.
- Audit records.
- Support workflows.
- Release status.

Administrative capabilities must use explicit permissions and suitable audit records.

Administrative changes must not bypass financial integrity, tenant isolation, or approved business rules.

The exact distinction between platform administration and tenant administration must be documented.

---

# 19. Commercial Model

The intended commercial model is modular SaaS subscription pricing.

Customers should be able to purchase a plan and eligible modules according to configurable commercial rules.

The detailed commercial design belongs in `COMMERCIAL_MODEL.md`.

That document must resolve:

- Subscription plans.
- Module pricing.
- Billing frequency.
- Currency.
- Trial availability.
- Setup or onboarding charges, if any.
- Module dependencies and pricing.
- Usage-based pricing, if applicable.
- Discounts.
- Taxes applicable to SaaS charges.
- Payment methods.
- Renewal rules.
- Upgrade and downgrade behavior.
- Failed payment handling.
- Suspension and cancellation.
- Refunds and credits.
- Commercial terms and customer communication.

The platform must distinguish SaaS subscription revenue from financial transactions recorded by customer organizations.

Pricing amounts must not be invented in the architecture or module specifications. They must come from approved commercial configuration.

---

# 20. Technical Architecture Direction

## 20.1 Backend

Django is the intended primary application framework.

Django applications should be organized around clearly defined functional responsibilities.

Django REST Framework should be introduced where API requirements justify it, rather than adding API layers without a defined use case.

## 20.2 Database

PostgreSQL is the intended primary database.

Database design must address:

- Tenant ownership.
- Referential integrity.
- Unique constraints.
- Indexing.
- Transaction boundaries.
- Migration safety.
- Auditability.
- Financial precision.
- Data lifecycle.
- Appropriate access controls.

## 20.3 Frontend

Django templates, HTMX, and Tailwind CSS are the intended frontend technologies.

Shared components and consistent interface patterns should be used where appropriate.

## 20.4 Background Processing

Celery and Redis are proposed for tasks that should not run synchronously within a web request.

Potential use cases include:

- Email delivery.
- Scheduled processing.
- Large exports.
- External provider communication.
- Retryable integrations.
- Long-running report generation.

Task execution must preserve tenant context, authorization boundaries, idempotency, and appropriate observability.

## 20.5 Deployment

Docker-based development and deployment workflows are proposed.

Production deployment must be defined separately according to security, availability, cost, operational capacity, and applicable data-location requirements.

## 20.6 Architecture Governance

Material changes to the technology stack, tenant-isolation model, module boundaries, financial posting architecture, or external integration strategy require documented review.

The final architecture is defined by `SYSTEM_ARCHITECTURE.md` and approved Architecture Decision Records.

---

# 21. Development Phases

The product is intended to be implemented through the following phases.

| Phase | Name | Expected outcome |
|---|---|---|
| P00 | Foundation and Architecture | Approved requirements, architecture, standards, and development controls |
| P01 | Core Platform and Multi-Tenancy | Secure tenant-aware application foundation |
| P02 | Subscription Engine | Plans, module entitlements, and SaaS billing foundations |
| P03 | CRM, Sales and Basic Invoicing | Initial customer-facing business workflows |
| P04 | UAE E-Invoicing Integration | Validated integration with the selected provider |
| P05 | Accounting and UAE VAT | Approved accounting and tax functionality |
| P06 | Procurement and Inventory | Purchasing and inventory workflows |
| P07 | HRMS and Payroll | Employee management and approved payroll functionality |
| P08 | Projects, Expenses and Fixed Assets | Project and asset-related workflows |
| P09 | Banking and Advanced Finance | Banking and advanced financial workflows |
| P10 | Reporting, Analytics and Integrations | Reporting and approved external integrations |
| P11 | Enterprise Readiness | Advanced administration, security, reliability, and operational capabilities |
| P12 | Production Launch and Operations | Production validation and controlled launch |

Each phase must define its own scope, dependencies, deliverables, acceptance criteria, tests, and approval requirements.

The roadmap must be revisited if regulatory requirements, provider dependencies, technical discoveries, or validated customer needs materially change the implementation sequence.

---

# 22. Acceptance and Release Principles

A feature is not complete merely because its interface exists or its primary workflow works under ideal conditions.

Acceptance must consider the feature's approved requirements and applicable quality standards.

Depending on the feature, acceptance may require:

- Functional correctness.
- Permission enforcement.
- Tenant-isolation verification.
- Financial-integrity tests.
- Validation and error handling.
- Duplicate-processing protection.
- Integration tests.
- Regression tests.
- Security review.
- Performance checks.
- Documentation.
- Operational readiness.
- Required human approval.

A module may be implemented but not commercially sellable.

A phase may have completed coding but still be undergoing testing or review.

The status model must distinguish these conditions.

Production release requires satisfaction of the approved release criteria and explicit authorization.

---

# 23. Documentation and Requirements Traceability

All major product requirements must have stable identifiers.

Suggested identifier conventions:

| Requirement category | Prefix | Example |
|---|---|---|
| Product requirement | PRD | PRD-001 |
| Functional requirement | FR | FR-001 |
| Non-functional requirement | NFR | NFR-001 |
| Security requirement | SEC | SEC-001 |
| Tenant-isolation requirement | TEN | TEN-001 |
| Financial requirement | FIN | FIN-001 |
| Regulatory requirement | REG | REG-001 |
| Integration requirement | INT | INT-001 |
| Deployment requirement | DEP | DEP-001 |

The final conventions should be defined in `REQUIREMENT_ID_CONVENTIONS.md`.

Requirements must be traceable to relevant:

- Product areas.
- Modules.
- Implementation phases.
- Tasks.
- Test cases.
- Acceptance evidence.
- Release decisions.

When a requirement changes, affected documents and tests must be identified.

The project must avoid maintaining conflicting versions of the same business rule across unrelated documents.

---

# 24. AI Agent Operating Requirements

AI agents must follow the repository instructions in `AGENTS.md`.

The orchestrator and supporting agents must work from approved specifications and explicit task assignments.

## 24.1 Required Behavior

Agents must:

- Inspect relevant documentation before acting.
- Inspect existing code before modifying it.
- Identify unresolved requirements.
- Stay within their authorized scope.
- Coordinate shared-file changes.
- Add or update tests.
- Run required checks where possible.
- Record actual verification results.
- Update relevant documentation.
- Report blockers and limitations.
- Request approval for material decisions outside their authority.

## 24.2 Prohibited Behavior

Agents must not:

- Implement unapproved features.
- Invent regulatory requirements.
- Claim tests passed when they were not run.
- Claim compliance without supporting evidence.
- Bypass tenant-isolation controls.
- Introduce undocumented financial behavior.
- Modify production data without authorization.
- Perform destructive database operations without explicit approval.
- Commit secrets.
- Automatically advance to the next phase without satisfying its approval gates.
- Treat generated documentation as evidence of implemented functionality.

## 24.3 Completion Reports

Task and phase completion reports must identify:

- Scope completed.
- Files changed.
- Tests and checks executed.
- Results and evidence.
- Review status.
- Known limitations.
- Outstanding defects.
- Decisions required.
- Required approvals.
- Recommended next action.

---

# 25. Open Product Decisions

The following decisions must be tracked and resolved according to their implementation dependencies.

The list is an initial register, not an exhaustive list of every future product decision.

| ID | Decision | Why it matters | Required before |
|---|---|---|---|
| DEC-001 | Final commercial plans and module pricing | Determines subscription configuration and commercial behavior | Finalization of P02 commercial rules |
| DEC-002 | Subscription payment provider | Determines payment integration and billing workflows | Implementation of the relevant payment workflows |
| DEC-003 | UAE e-invoicing provider and applicable integration route | Determines interfaces, message formats, testing, and operational dependencies | Finalization of P04 implementation |
| DEC-004 | Applicable UAE e-invoicing requirements and effective dates | Determines required workflows and release conditions | Finalization of P04 requirements |
| DEC-005 | Exact customer segments for the initial release | Influences feature prioritization and commercial packaging | Approval of the initial release scope |
| DEC-006 | Hosting provider and deployment region | Influences deployment architecture, costs, and data-location considerations | Production architecture approval |
| DEC-007 | Data residency and cross-border data-transfer requirements | Influences infrastructure and provider selection | Approval of the production data architecture |
| DEC-008 | Initial language and localization scope | Influences interface, document generation, and testing | Approval of initial UX requirements |
| DEC-009 | Initial currency and multi-currency requirements | Influences accounting and financial data models | Finalization of financial architecture |
| DEC-010 | Accounting policies and posting rules | Influences ledger design, transaction integrity, and financial reporting | Finalization of P05 requirements |
| DEC-011 | Applicable payroll rules and customer categories | Influences payroll calculations and compliance requirements | Finalization of P07 requirements |
| DEC-012 | Subscription cancellation, suspension, and retention policy | Influences entitlements, customer access, and data lifecycle | Finalization of P02 lifecycle rules |
| DEC-013 | Service availability and recovery targets | Influences production infrastructure and operating costs | Production readiness approval |
| DEC-014 | Target tenant volume and expected workload | Influences infrastructure sizing and performance targets | Production capacity planning |
| DEC-015 | Support access and tenant-data access policy | Influences authorization, privacy, and auditability | Finalization of platform administration |

Each decision must have an owner, status, evidence or rationale, and approval record as appropriate.

Decisions must not be marked resolved merely because an agent has proposed an answer.

---

# 26. Risks and Mitigations

The project must maintain a current risk register.

Initial risks include:

| Risk | Potential impact | Proposed mitigation |
|---|---|---|
| Unclear product requirements | Rework and inconsistent implementation | Establish approved product and module specifications |
| Conflicting documentation | Agents implement different interpretations | Define document authority and run consistency checks |
| Weak tenant isolation | Unauthorized cross-customer data access | Centralize tenant controls and require isolation tests |
| Premature module coupling | Expensive changes as the product grows | Define module boundaries and integration contracts |
| Incorrect financial calculations | Financial inaccuracies and potential compliance issues | Explicit business rules, decimal arithmetic, and extensive tests |
| Incorrect regulatory assumptions | Rework and potential compliance failures | Verify authoritative requirements and document evidence |
| Unverified e-invoicing provider capabilities | Integration delays or unsuitable architecture | Validate provider selection and contract before implementation |
| Excessive infrastructure complexity | Higher costs and operational burden | Begin with a justified modular monolith and scale as needed |
| Uncontrolled AI changes | Regressions and unauthorized scope expansion | Bounded tasks, reviews, CI, and approval gates |
| Incomplete backup procedures | Data loss or prolonged recovery | Test backup restoration and define recovery objectives |
| Inadequate operational monitoring | Delayed detection of failures | Establish monitoring, alerting, and incident procedures |
| Uncontrolled scope growth | Delayed delivery and unclear priorities | Explicit release scope and documented change control |

Risk ownership and mitigation status must be maintained in `RISKS_AND_ISSUES.md`.

---

# 27. Definition of Product Success

The product will be considered successful when the approved release meets measurable business, technical, security, and operational requirements.

The release must demonstrate that:

1. Tenants can operate within appropriately isolated business environments.
2. Users receive only the permissions and entitlements they are authorized to use.
3. Modules operate according to documented business rules.
4. Financial records preserve required integrity and auditability.
5. Approved UAE-specific requirements are implemented and verified for the intended scope.
6. External integrations handle errors, retries, and failures appropriately.
7. Required automated tests and security checks pass.
8. Deployment and operational procedures are documented and tested.
9. Backup restoration and recovery procedures meet approved objectives.
10. Commercial plans and module availability follow approved configuration.
11. Known limitations and unresolved issues are documented.
12. Production release has received the required approvals.

Quantitative targets for performance, availability, recovery, tenant capacity, and commercial outcomes must be established in their respective specifications.

---

# 28. Immediate Next Steps

After this document is saved, the next activities should be:

1. Review this specification against the intended business model.
2. Identify any missing product objectives or scope boundaries.
3. Confirm which proposed defaults should become approved decisions.
4. Record unresolved questions in the project decision register.
5. Create `PRODUCT_REQUIREMENTS.md` with uniquely identified functional and non-functional requirements.
6. Create `TARGET_MARKET.md`.
7. Create `COMMERCIAL_MODEL.md`.
8. Create `MODULE_CATALOGUE.md`.
9. Create `DEVELOPMENT_ROADMAP.md`.
10. Review the product documents for consistency before finalizing the technical architecture.

Do not begin full ERP implementation solely because this document has been created.

The product specification, architecture, and phase requirements must be sufficiently defined and approved before their corresponding implementation tasks are authorized.

---

# 29. Final Principle

The UAE ERP SaaS platform must be developed as a controlled product engineering program rather than a collection of independently generated features.

Every significant feature must have a defined business purpose, an approved specification, a clear architectural boundary, appropriate tests, and verifiable acceptance criteria.

**Approved requirements govern implementation. Verification evidence governs completion. Explicit authorization governs progression to the next phase.**
