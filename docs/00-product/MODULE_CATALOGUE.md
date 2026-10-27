# UAE ERP SaaS — Module Catalogue

| Document Attribute | Value |
|---|---|
| Document ID | MOD-CAT-001 |
| Version | 1.0 |
| Status | Initial Draft — Pending Approval |
| Product | UAE ERP SaaS |
| Document Type | Product Module Catalogue |
| Parent Document | `docs/00-product/MASTER_PRODUCT_SPECIFICATION.md` |
| Related Documents | `PRODUCT_REQUIREMENTS.md`, `TARGET_MARKET.md`, `COMMERCIAL_MODEL.md`, `DEVELOPMENT_ROADMAP.md` |
| Primary Market | United Arab Emirates |
| Product Architecture | Modular Multi-Tenant SaaS |
| Intended Audience | Product Owner, Architect, Developers, QA Engineers, Commercial Team |

---

# 1. Purpose

This document defines the official module catalogue for the UAE ERP SaaS platform.

It establishes:

- The modules that constitute the product.
- The purpose and scope of each module.
- The functional capabilities expected from each module.
- The boundaries between modules.
- Dependencies between modules.
- The distinction between platform functionality and paid ERP modules.
- Commercial availability and release status.
- Module access and entitlement requirements.
- Module integration principles.
- Module-level acceptance requirements.
- Rules for adding, modifying, retiring, and commercializing modules.

This document is the authoritative product-level reference for module scope.

Detailed implementation requirements belong in the relevant phase specifications, architecture documents, and module specifications.

# 2. Product Architecture Principles

## 2.1 Modular Monolith

The initial implementation must use a modular monolith.

The application should consist of clearly separated Django applications and domain services within one deployable product unless a documented architecture decision approves a different approach.

Do not create a separate microservice for every ERP module.

The modular monolith should provide:

- Clear domain boundaries.
- Explicit ownership of business logic.
- Controlled cross-module interactions.
- Shared identity and tenant infrastructure.
- Consistent database transactions where appropriate.
- Independent module-level testing.
- A maintainable path for future extraction of services if justified.

## 2.2 Module Independence

Each module should own its principal business rules, data models, services, and permissions.

For example:

- CRM owns leads, opportunities, and sales-pipeline activities.
- Invoicing owns customer invoice workflows.
- Accounting owns the general ledger and accounting periods.
- Inventory owns stock quantities and stock movements.
- HRMS owns employee records and HR workflows.
- Payroll owns payroll calculations and payroll records.

A module may reference another module's records through explicit relationships or domain services.

It must not bypass another module's business rules by directly modifying that module's internal data.

## 2.3 Shared Platform Capabilities

Some capabilities are foundational infrastructure rather than separately purchasable modules.

These include:

- Tenant management.
- Authentication.
- Authorization.
- User management.
- Subscription management.
- Module entitlements.
- Audit infrastructure.
- Notifications infrastructure.
- Background task infrastructure.
- System configuration.
- Platform administration.

These capabilities support the commercial product and should not be duplicated in every ERP module.

Whether any foundational capability becomes a separately priced service is a future commercial decision.

## 2.4 Module Availability

A module's presence in this catalogue does not mean it is implemented or available for sale.

The platform must distinguish between:

1. Planned modules.
2. Modules in development.
3. Internal-only modules.
4. Pilot modules.
5. Commercially available modules.
6. Deprecated modules.
7. Retired modules.

Only modules approved for commercial release may be offered for purchase.

# 3. Module Classification

The product is divided into five functional groups.

| Group | Purpose |
|---|---|
| Platform Core | Identity, tenancy, permissions, subscriptions, entitlements |
| Customer and Revenue Operations | CRM, sales, invoicing, e-invoicing |
| Finance and Operations | Accounting, VAT, procurement, inventory, banking |
| People and Business Management | HRMS, payroll, projects, expenses, fixed assets |
| Insights and Connectivity | Reporting, analytics, integrations |

This classification is for product organization. It does not determine pricing or subscription packaging.

# 4. Module Lifecycle and Commercial Status

## 4.1 Lifecycle States

Every module must have a controlled lifecycle state.

| State | Meaning | Purchase Rules |
|---|---|---|
| `PLANNED` | Approved or proposed for future development | Not purchasable |
| `IN_DEVELOPMENT` | Under implementation | Not purchasable |
| `INTERNAL_ONLY` | Available only to authorized internal users | Not purchasable |
| `PILOT` | Available to specifically approved pilot tenants | Restricted to approved tenants |
| `AVAILABLE` | Approved for commercial use | Purchasable if dependencies and eligibility checks pass |
| `DEPRECATED` | Scheduled for retirement or replacement | No new purchases by default |
| `RETIRED` | No longer supported for normal use | Not purchasable |

A transition to `AVAILABLE` must require release approval and evidence that the module meets its acceptance criteria.

## 4.2 Status Is Not Entitlement

Lifecycle status and customer entitlement are different concepts.

A module can be commercially available while a tenant is not entitled to use it.

For example:

- The module is available for purchase.
- The tenant has not subscribed to it.
- The tenant has not completed a required upgrade.
- A required dependency is missing.
- The tenant's subscription is suspended.
- The module is restricted by an approved administrative policy.

In these cases, the module must not be accessible merely because its lifecycle state is `AVAILABLE`.

## 4.3 Status Is Not Implementation Completeness

The frontend must not infer module completeness from the existence of a Django application, database table, URL, or navigation item.

Commercial availability requires explicit approval.

A module is not commercially available merely because:

- Its models exist.
- A page renders.
- An API endpoint returns a response.
- A developer marks a feature as complete.
- The module appears in a demonstration.
- A migration has been applied.

# 5. Authoritative Module Registry

The following registry defines the proposed product modules.

All modules begin as `PLANNED` unless the product owner explicitly approves another state.

| Code | Module | Django App | Group | Initial Status | Commercial Module? |
|---|---|---|---|---|---|
| CORE | Platform Core | `core` | Platform | Foundation | No |
| TENANTS | Tenant Management | `tenants` | Platform | Foundation | No |
| USERS | Users and Access Control | `users` | Platform | Foundation | No |
| SUBSCRIPTIONS | Subscription Management | `subscriptions` | Platform | Planned | No |
| BILLING | SaaS Subscription Billing | `billing` | Platform | Planned | No |
| CRM | Customer Relationship Management | `crm` | Customer and Revenue | Planned | Yes |
| SALES | Sales Management | `sales` | Customer and Revenue | Planned | Yes |
| INVOICING | Customer Invoicing | `invoicing` | Customer and Revenue | Planned | Yes |
| E_INVOICING | UAE E-Invoicing Integration | `e_invoicing` | Customer and Revenue | Planned | Yes |
| ACCOUNTING | Accounting | `accounting` | Finance and Operations | Planned | Yes |
| VAT | VAT Management | `vat` | Finance and Operations | Planned | Yes |
| PROCUREMENT | Procurement | `procurement` | Finance and Operations | Planned | Yes |
| INVENTORY | Inventory Management | `inventory` | Finance and Operations | Planned | Yes |
| HRMS | Human Resource Management | `hrms` | People and Business Management | Planned | Yes |
| PAYROLL | Payroll | `payroll` | People and Business Management | Planned | Yes |
| PROJECTS | Project Management | `projects` | People and Business Management | Planned | Yes |
| EXPENSES | Expense Management | `expenses` | People and Business Management | Planned | Yes |
| FIXED_ASSETS | Fixed Asset Management | `fixed_assets` | Finance and Operations | Planned | Yes |
| BANKING | Banking and Reconciliation | `banking` | Finance and Operations | Planned | Yes |
| REPORTING | Reporting and Analytics | `reporting` | Insights and Connectivity | Planned | Yes |
| INTEGRATIONS | Integration Hub | `integrations` | Insights and Connectivity | Planned | Yes |

### Registry Rules

1. Module codes must be unique and stable.
2. Existing module codes must not be silently reused for a different purpose.
3. Django application names must remain consistent with approved architecture.
4. Module names and descriptions may change without changing stable identifiers.
5. Commercial status must be explicitly maintained.
6. Module dependencies must be recorded in structured configuration.
7. Pricing must be managed by the commercial pricing system.
8. Lifecycle status must not be inferred from subscription status.
9. Customer access must be determined by the entitlement engine.
10. The registry must be kept consistent with the development roadmap.

# 6. Platform Core

## 6.1 CORE — Platform Core

**Purpose:** Provide shared technical infrastructure for the ERP platform.

### Responsibilities

- Common application configuration.
- Shared domain utilities.
- Common error handling.
- Health checks.
- System-wide settings.
- Shared identifiers and utilities.
- Common document-generation infrastructure where appropriate.
- Application-level integration points.

### Exclusions

The core module must not become a general-purpose location for every business rule.

CRM, accounting, payroll, inventory, and other domain logic must remain in their owning applications.

### Acceptance Criteria

- Shared infrastructure has documented ownership.
- Domain-specific logic remains in the appropriate module.
- Common utilities are tested.
- Core changes do not silently bypass tenant or authorization controls.

## 6.2 TENANTS — Tenant Management

**Purpose:** Manage customer organizations and tenant-level configuration.

### Responsibilities

- Tenant creation.
- Tenant status.
- Tenant profile.
- Organization details.
- Tenant-specific settings.
- Default currency and time zone.
- Fiscal-year configuration.
- Tenant branding.
- Tenant lifecycle management.
- Tenant-scoped configuration.

### Exclusions

Tenant management must not own the commercial pricing engine or individual ERP business workflows.

### Acceptance Criteria

- Tenant records are uniquely identifiable.
- Tenant lifecycle changes are auditable.
- Tenant data is isolated according to the approved tenancy architecture.
- Tenant settings are not accidentally shared across organizations.
- Authorized tenant administrators can manage permitted organization settings.

## 6.3 USERS — Users and Access Control

**Purpose:** Manage identities, memberships, roles, and permissions.

### Responsibilities

- User accounts.
- Tenant membership.
- Authentication integration.
- Role assignment.
- Permission checks.
- User invitations, if enabled.
- User activation and deactivation.
- Session and access security.
- Administrative access controls.

### Exclusions

This module does not determine which commercial modules a tenant has purchased.

Commercial entitlements and user permissions must be checked together where relevant.

### Acceptance Criteria

- A user cannot access a tenant without valid membership and authorization.
- Permissions are enforced server-side.
- Role changes are auditable.
- Users cannot grant themselves administrative privileges.
- Sensitive permissions follow least-privilege principles.

## 6.4 SUBSCRIPTIONS — Subscription Management

**Purpose:** Manage the commercial subscription relationship between the SaaS provider and each tenant.

### Responsibilities

- Subscription lifecycle.
- Subscription items.
- Billing periods.
- Module selection.
- Module dependency validation.
- Upgrades and downgrades.
- Trial state, if enabled.
- Cancellation.
- Renewal scheduling.
- Subscription history.
- Subscription-related events.

### Exclusions

The subscription module must not duplicate payment-provider logic or customer ERP invoicing logic.

### Acceptance Criteria

- Subscription transitions follow documented rules.
- Subscription changes are auditable.
- Module selection is validated against the catalogue.
- Dependency violations are rejected.
- Subscription state changes are processed safely and consistently.

## 6.5 BILLING — SaaS Subscription Billing

**Purpose:** Calculate and collect charges for the SaaS platform itself.

### Responsibilities

- Pricing configuration integration.
- Subscription charge calculation.
- SaaS subscription invoices.
- Payment transaction records.
- Payment-provider integration.
- Payment reconciliation.
- Discounts and credits, if enabled.
- Failed-payment handling.
- Commercial billing reports.

### Exclusions

This module must not own customer invoices generated by tenant businesses.

### Acceptance Criteria

- Subscription invoices are separate from tenant sales invoices.
- Financial calculations use decimal arithmetic.
- Payment events are processed idempotently.
- Issued invoices preserve historical content.
- Payment status is based on verified provider information or authorized reconciliation.

# 7. CRM — Customer Relationship Management

**Module Code:** `CRM`

**Django App:** `crm`

**Purpose:** Manage leads, prospects, customer relationships, and sales opportunities.

## 7.1 Core Features

- Lead management.
- Contact management.
- Company or account records.
- Opportunity management.
- Sales pipeline stages.
- Lead source tracking.
- Follow-up activities.
- Notes and interaction history.
- Tasks and reminders.
- Customer communication history.
- Lead assignment.
- Basic CRM dashboards.

## 7.2 Business Entities

Potential entities include:

- Lead.
- Contact.
- Account.
- Opportunity.
- Pipeline.
- PipelineStage.
- Activity.
- CRMTask.
- LeadSource.

The final model must avoid unnecessary duplication of customer and supplier master records.

## 7.3 Integration Boundaries

CRM may reference shared customer or organization records where appropriate.

Sales owns sales documents and commercial order workflows.

CRM must not independently implement invoice accounting or payment reconciliation.

## 7.4 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Optional integrations may include Sales, Invoicing, Reporting, and Integrations.

## 7.5 Acceptance Criteria

- CRM records are tenant-scoped.
- Pipeline stages are configurable where approved.
- Users can only access records permitted by their roles.
- Activities can be linked to the appropriate CRM record.
- CRM operations do not create accounting entries without the appropriate downstream workflow.

# 8. SALES — Sales Management

**Module Code:** `SALES`

**Django App:** `sales`

**Purpose:** Manage the commercial process between customer interest and fulfillment or invoicing.

## 8.1 Core Features

- Quotations.
- Quotation line items.
- Quotation versioning or revision history, as required.
- Sales orders.
- Sales order line items.
- Order status management.
- Approval workflows, where configured.
- Customer pricing rules, if approved.
- Sales document generation.
- Order-to-invoice workflow.
- Sales performance reports.

## 8.2 Business Entities

Potential entities include:

- Quotation.
- QuotationLine.
- SalesOrder.
- SalesOrderLine.
- SalesDocumentRevision.
- SalesApproval.

## 8.3 Integration Boundaries

Sales owns quotations and sales orders.

Invoicing owns issued customer invoices and credit notes.

Inventory owns stock availability and stock movements.

Accounting owns accounting entries generated by approved business events.

## 8.4 Dependencies

Required platform capabilities.

Customer and product references must be resolved through approved shared records or explicit module integrations.

Invoicing and Inventory are optional dependencies unless the enabled workflow requires them.

## 8.5 Acceptance Criteria

- Quotation totals are calculated on the server.
- Accepted quotations can follow the approved order-creation workflow.
- Sales orders preserve their transaction history.
- Orders cannot bypass required approval controls.
- Stock availability is obtained through the inventory domain where applicable.
- Sales order creation does not duplicate stock or accounting logic.

# 9. INVOICING — Customer Invoicing

**Module Code:** `INVOICING`

**Django App:** `invoicing`

**Purpose:** Manage customer invoices, credit notes, payment allocations, and invoice lifecycle.

## 9.1 Core Features

- Customer invoices.
- Invoice line items.
- Credit notes.
- Invoice numbering.
- Invoice issue dates and due dates.
- Customer payment recording.
- Payment allocation.
- Outstanding balance calculation.
- Invoice status management.
- Customer statements, where approved.
- PDF generation.
- Invoice email delivery, where enabled.
- Receivables summaries.
- Invoice audit history.

## 9.2 Business Entities

Potential entities include:

- CustomerInvoice.
- CustomerInvoiceLine.
- CreditNote.
- CreditNoteLine.
- CustomerPayment.
- PaymentAllocation.
- InvoiceSequence.
- InvoiceDocument.

The final model must distinguish invoice documents from payment transactions and accounting entries.

## 9.3 Integration Boundaries

Invoicing owns customer invoice documents and invoice balances.

Accounting owns the authoritative ledger.

Banking owns bank transaction imports and reconciliation.

E-invoicing owns external e-invoicing submission and response workflows.

VAT provides or coordinates approved tax calculation and reporting rules according to the final architecture.

## 9.4 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Additional dependencies must be determined by the selected invoicing and accounting architecture.

## 9.5 Acceptance Criteria

- Invoice totals are calculated server-side.
- Issued invoices cannot be silently overwritten.
- Invoice numbers are unique within the approved numbering scope.
- Credit notes follow approved correction rules.
- Payment allocations cannot exceed permitted amounts.
- Customer invoice balances are consistent with recorded payments and credits.
- All financial changes are auditable.
- Tenant data remains isolated.

# 10. E_INVOICING — UAE E-Invoicing Integration

**Module Code:** `E_INVOICING`

**Django App:** `e_invoicing`

**Purpose:** Integrate the ERP with a selected UAE e-invoicing provider or approved service arrangement.

## 10.1 Core Features

Subject to confirmed requirements:

- Provider configuration.
- Secure credential management.
- Invoice submission.
- Submission status tracking.
- Provider response processing.
- Validation error handling.
- Retry management.
- Credit-note submission where required.
- External reference storage.
- Submission audit history.
- Reconciliation of uncertain submissions.
- Provider health monitoring.

## 10.2 Integration Principles

The module must isolate provider-specific logic behind a documented adapter or interface.

It must not assume that all providers expose identical APIs or follow identical workflows.

The implementation must support the validated provider requirements and applicable regulatory rules.

## 10.3 Dependencies

Customer Invoicing and the relevant tenant configuration.

Other dependencies must be determined by the selected provider and validated implementation design.

## 10.4 Acceptance Criteria

- Provider credentials are protected.
- Submissions are traceable.
- Duplicate processing is prevented where the provider workflow supports idempotency.
- Transient failures can be retried safely.
- Invalid submissions are reported clearly.
- External status is not inferred from a local invoice status.
- Provider responses are preserved according to the approved audit policy.
- Compliance claims are not made without the required evidence and approval.

# 11. ACCOUNTING — General Ledger and Financial Accounting

**Module Code:** `ACCOUNTING`

**Django App:** `accounting`

**Purpose:** Maintain the authoritative financial ledger and accounting records for each tenant.

## 11.1 Core Features

- Chart of accounts.
- Journal entries.
- Journal entry lines.
- General ledger.
- Accounting periods.
- Period closing and locking.
- Accounts receivable control accounts.
- Accounts payable control accounts.
- Bank and cash accounts.
- Trial balance.
- Profit and loss statement.
- Balance sheet.
- General ledger reports.
- Reversal entries.
- Audit trail.
- Opening balances, where approved.

## 11.2 Business Entities

Potential entities include:

- Account.
- JournalEntry.
- JournalLine.
- AccountingPeriod.
- FiscalYear.
- JournalSequence.
- AccountingConfiguration.
- PostingBatch.

## 11.3 Financial Integrity

The accounting domain must enforce balanced journal entries according to the approved accounting model.

Issued or posted financial entries must not be silently edited or deleted.

Corrections must use an approved reversal or adjustment workflow.

The system must support transaction-safe posting and protect against duplicate posting of the same business event.

## 11.4 Integration Boundaries

Accounting receives approved posting events from invoicing, procurement, inventory, banking, expenses, fixed assets, and payroll where those modules are enabled.

The accounting module owns ledger posting and financial statements.

Operational modules must not independently modify general ledger balances.

## 11.5 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Other modules may integrate with accounting without necessarily being required for the basic general ledger.

## 11.6 Acceptance Criteria

- Posted journal entries satisfy the approved balancing rules.
- Financial posting is transactional.
- Duplicate posting is prevented.
- Closed periods enforce the approved restrictions.
- Reversals preserve historical records.
- Financial statements reconcile to the underlying ledger.
- Access to financial data follows explicit permissions.
- Accounting calculations are covered by automated tests.

# 12. VAT — Value Added Tax Management

**Module Code:** `VAT`

**Django App:** `vat`

**Purpose:** Provide tax configuration, tax calculation support, and tax reporting for validated UAE VAT workflows.

## 12.1 Core Features

Subject to confirmed requirements:

- Tax codes.
- Tax rates.
- Tax treatment configuration.
- Tax-inclusive and tax-exclusive calculations.
- Tax classification of transaction lines.
- Input and output VAT tracking.
- Credit-note tax adjustments.
- VAT reporting periods.
- VAT reports.
- Supporting transaction details.
- Tax calculation audit history.

## 12.2 Integration Boundaries

VAT calculation rules must be centralized and consistently used by relevant business workflows.

The module must not independently duplicate tax calculation logic in invoicing, procurement, or other applications.

The final architecture must define how VAT data is represented in accounting entries.

## 12.3 Dependencies

Invoicing and/or Accounting may be required, depending on the approved implementation scope.

The final dependency must be documented before commercial release.

## 12.4 Acceptance Criteria

- Tax codes and rates are configurable under controlled permissions.
- Calculations follow documented rules.
- Rounding behavior is deterministic.
- Historical transactions retain their applicable tax information.
- Reports can be reconciled to supporting transaction records.
- Tax treatment is reviewed against applicable requirements.
- The product does not claim compliance based solely on the existence of VAT fields or reports.

# 13. PROCUREMENT — Procurement Management

**Module Code:** `PROCUREMENT`

**Django App:** `procurement`

**Purpose:** Manage supplier purchasing workflows.

## 13.1 Core Features

- Supplier records or supplier references.
- Purchase requisitions, if approved.
- Purchase orders.
- Purchase order line items.
- Approval workflows.
- Goods receipts.
- Supplier bill capture.
- Purchase order status tracking.
- Purchase returns, if required.
- Supplier transaction history.
- Purchase reporting.

## 13.2 Integration Boundaries

Procurement owns purchase orders and procurement workflows.

Inventory owns stock receipts and stock movements.

Accounting owns supplier liability and expense or inventory postings.

The architecture must distinguish purchase orders, goods receipts, supplier bills, and payments.

## 13.3 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Inventory and Accounting integrations are required for workflows that depend on those modules.

## 13.4 Acceptance Criteria

- Purchase orders follow configured approval rules.
- Goods receipts are traceable to relevant purchase documents.
- Supplier bills are not confused with purchase orders.
- Inventory receipts are processed through the inventory domain.
- Financial postings occur through approved accounting workflows.
- Duplicate receipt or posting events are prevented.

# 14. INVENTORY — Inventory Management

**Module Code:** `INVENTORY`

**Django App:** `inventory`

**Purpose:** Manage products, stock quantities, warehouses, and inventory movements.

## 14.1 Core Features

- Product and stock item records.
- Product categories.
- Units of measure, where required.
- Warehouse and storage locations.
- Stock balances.
- Stock receipts.
- Stock issues.
- Stock transfers.
- Stock adjustments.
- Physical stock counts.
- Stock reservations, if required.
- Inventory movement history.
- Reorder thresholds, if approved.
- Inventory reports.

Additional features such as lot tracking, serial tracking, expiry dates, and landed costs require separate scope approval.

## 14.2 Business Entities

Potential entities include:

- Product.
- ProductVariant, if required.
- UnitOfMeasure.
- Warehouse.
- StockLocation.
- StockMovement.
- StockMovementLine.
- StockAdjustment.
- StockCount.
- StockReservation.

The final schema must define whether products are shared master records or owned directly by inventory.

## 14.3 Stock Integrity

Stock balances must be derived from or reconciled against controlled stock movements.

The system must prevent unauthorized stock changes.

Stock adjustments must capture the reason, actor, timestamp, and relevant approval.

Concurrent transactions must not create invalid stock balances or duplicate movements.

Negative inventory behavior must be explicitly configured and tested.

## 14.4 Integration Boundaries

Inventory owns stock movements and quantity calculations.

Procurement initiates purchase workflows.

Sales initiates fulfillment workflows.

Accounting owns financial inventory valuation postings.

The system must not allow invoicing or procurement views to directly modify stock balances outside the approved inventory service.

## 14.5 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Procurement, Sales, and Accounting are integration dependencies for specific workflows.

## 14.6 Acceptance Criteria

- Every stock movement is traceable.
- Stock balances follow documented movement rules.
- Concurrent stock operations preserve consistency.
- Transfers record both the source and destination.
- Adjustments are auditable.
- Tenant stock records are isolated.
- Inventory valuation is not advertised until its calculation and accounting integration are implemented and tested.

# 15. HRMS — Human Resource Management

**Module Code:** `HRMS`

**Django App:** `hrms`

**Purpose:** Manage employee records and approved HR workflows.

## 15.1 Core Features

- Employee profiles.
- Employee identifiers.
- Departments.
- Designations.
- Employment status.
- Employment-related documents.
- Leave types.
- Leave requests.
- Leave approvals.
- Attendance records or integration, where approved.
- Employee history.
- HR reports.
- Access-controlled employee information.

## 15.2 Integration Boundaries

HRMS owns employee master data and HR workflows.

Payroll owns payroll calculations and payroll records.

The authentication system owns application users and login identities.

An employee record must not automatically create a login account unless the approved workflow explicitly requires it.

## 15.3 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Payroll may integrate with HRMS when both modules are enabled.

## 15.4 Acceptance Criteria

- Employee records are tenant-scoped.
- Sensitive information has restricted access.
- Employee lifecycle changes are auditable.
- Leave balances follow documented rules.
- Attendance records have traceable sources.
- Deactivation does not silently delete historical employment or payroll records.

# 16. PAYROLL — Payroll Management

**Module Code:** `PAYROLL`

**Django App:** `payroll`

**Purpose:** Calculate and maintain payroll records according to approved employer configurations and validated requirements.

## 16.1 Core Features

Subject to confirmed scope:

- Payroll periods.
- Salary structures.
- Earnings and deductions.
- Payroll input records.
- Payroll calculations.
- Payroll review and approval.
- Payroll registers.
- Payslip generation.
- Payroll adjustment records.
- Payroll history.
- Approved payroll exports or integrations.
- End-of-service calculations where validated.
- WPS-related functionality where applicable and approved.

## 16.2 Integration Boundaries

Payroll owns payroll calculation and payroll records.

HRMS provides approved employee information.

Accounting receives approved payroll posting events.

Banking may support payment reconciliation.

Payroll must not directly modify the general ledger.

## 16.3 Dependencies

HRMS is the proposed required dependency.

Accounting may be required for financial posting workflows.

The exact dependency configuration must be approved.

## 16.4 Acceptance Criteria

- Payroll calculations follow versioned, documented rules.
- Payroll runs are traceable.
- Approved payroll records cannot be silently altered.
- Adjustments use controlled workflows.
- Confidential payroll information is restricted.
- Repeated processing does not duplicate payroll postings.
- Jurisdiction-specific requirements are validated before commercial release.

# 17. PROJECTS — Project Management

**Module Code:** `PROJECTS`

**Django App:** `projects`

**Purpose:** Manage projects, tasks, milestones, assignments, and operational progress.

## 17.1 Core Features

- Project records.
- Project status.
- Task management.
- Task assignment.
- Milestones.
- Due dates.
- Project activities.
- Project notes.
- Project-level reporting.
- Project expense references.
- Project customer references.
- Basic workload visibility, if approved.

Time tracking, resource planning, and advanced project costing require additional scope approval.

## 17.2 Integration Boundaries

Projects owns project and task records.

Expenses owns expense transactions.

Accounting owns financial postings.

CRM may supply customer references.

The project module must not duplicate the accounting ledger or expense approval engine.

## 17.3 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

CRM and Expenses are optional integrations depending on the selected workflows.

## 17.4 Acceptance Criteria

- Project records are tenant-scoped.
- Task assignments follow user permissions.
- Project status changes are traceable.
- Project reports use authorized data.
- Project records can reference related customer or expense records without duplicating their financial data.

# 18. EXPENSES — Expense Management

**Module Code:** `EXPENSES`

**Django App:** `expenses`

**Purpose:** Capture, review, approve, and report business expenses.

## 18.1 Core Features

- Expense claims.
- Expense categories.
- Expense dates and amounts.
- Receipt attachments.
- Employee or user references.
- Project references, where applicable.
- Approval workflows.
- Reimbursement status.
- Expense reporting.
- Tax information, where applicable.
- Expense audit history.

Corporate card feeds and automated receipt extraction require separate approval.

## 18.2 Integration Boundaries

Expenses owns expense records and approval workflows.

Accounting owns financial postings.

Payroll may support approved employee reimbursement workflows where explicitly designed.

Projects may provide project references.

## 18.3 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Accounting is required for workflows that post approved expenses to the ledger.

## 18.4 Acceptance Criteria

- Expense amounts are calculated and validated server-side.
- Attachments follow approved file security controls.
- Approval workflows are auditable.
- Unauthorized users cannot approve their own claims where segregation-of-duties rules prohibit it.
- Financial posting is traceable and idempotent.

# 19. FIXED_ASSETS — Fixed Asset Management

**Module Code:** `FIXED_ASSETS`

**Django App:** `fixed_assets`

**Purpose:** Maintain the fixed asset register and approved asset accounting workflows.

## 19.1 Core Features

- Asset register.
- Asset categories.
- Acquisition information.
- Asset location and custodian.
- Useful-life configuration.
- Depreciation methods.
- Depreciation schedules.
- Asset transfers.
- Asset disposals.
- Asset impairment or revaluation workflows, if approved.
- Asset reporting.
- Asset audit history.

## 19.2 Integration Boundaries

Fixed Assets owns asset records and depreciation schedules.

Procurement may provide acquisition references.

Accounting owns financial postings.

The asset register must reconcile with approved accounting entries according to the configured accounting policy.

## 19.3 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Accounting is required for the complete financial posting workflow.

## 19.4 Acceptance Criteria

- Asset records preserve acquisition history.
- Depreciation follows documented methods and parameters.
- Depreciation runs are safe to retry.
- Disposals and adjustments are traceable.
- Financial postings are idempotent.
- Changes do not silently rewrite previously posted accounting entries.

# 20. BANKING — Banking and Reconciliation

**Module Code:** `BANKING`

**Django App:** `banking`

**Purpose:** Manage bank account records, imported bank transactions, and reconciliation workflows.

## 20.1 Core Features

- Bank account configuration.
- Bank statement import.
- Bank transaction records.
- Transaction matching.
- Manual reconciliation.
- Reconciliation status.
- Unmatched transaction reports.
- Bank balance summaries.
- Reconciliation history.
- Supported bank-feed integration, if approved.

Direct bank connectivity must not be assumed to exist.

## 20.2 Integration Boundaries

Banking owns imported bank transaction records and reconciliation workflows.

Accounting owns the general ledger.

Invoicing provides customer payment references.

Procurement or accounting may provide supplier payment references.

## 20.3 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Accounting is required for complete ledger reconciliation.

## 20.4 Acceptance Criteria

- Imported transactions are traceable to their source.
- Duplicate imports are detected using documented matching rules.
- Reconciliation operations are auditable.
- Bank statement data is tenant-isolated.
- Reconciliation does not silently create duplicate accounting entries.
- Bank credentials are protected if a supported bank integration requires them.

# 21. REPORTING — Reporting and Analytics

**Module Code:** `REPORTING`

**Django App:** `reporting`

**Purpose:** Provide management reporting across authorized business domains.

## 21.1 Core Features

- Module-specific reports.
- Management dashboards.
- Date-range filters.
- Exportable reports, where approved.
- Summary metrics.
- Report scheduling, if approved.
- Saved report configurations, if approved.
- Cross-module reporting where dependencies are satisfied.

## 21.2 Reporting Boundaries

Reporting consumes data from authoritative domain sources.

It must not become an alternative source of truth for financial or operational records.

Financial reports must reconcile to the underlying accounting ledger.

Operational reports must use documented definitions for their metrics.

## 21.3 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Specific reports may require CRM, Invoicing, Accounting, Inventory, HRMS, or other modules.

## 21.4 Acceptance Criteria

- Reports enforce tenant isolation.
- Reports enforce role-based access.
- Metric definitions are documented.
- Financial totals reconcile to authoritative records.
- Export operations do not bypass authorization.
- Expensive reports use appropriate query optimization and background processing when necessary.

# 22. INTEGRATIONS — Integration Hub

**Module Code:** `INTEGRATIONS`

**Django App:** `integrations`

**Purpose:** Provide controlled integration infrastructure for supported external services.

## 22.1 Core Features

Potential capabilities include:

- Integration configuration.
- Credential references.
- API connection settings.
- Webhook registration.
- Integration event tracking.
- Synchronization jobs.
- Retry management.
- Integration error logs.
- Import and export workflows.
- Integration health status.
- Per-tenant integration settings.

The initial release should implement only integrations justified by approved product requirements.

## 22.2 Integration Boundaries

The integration hub owns shared integration infrastructure.

Domain-specific adapters may remain within their owning modules when they require specialized business logic.

For example, e-invoicing submission behavior should remain associated with the e-invoicing domain, even if shared authentication, monitoring, or event infrastructure is reused.

## 22.3 Dependencies

Platform Core, Tenant Management, and Users and Access Control.

Individual integrations may have additional dependencies.

## 22.4 Acceptance Criteria

- Credentials are stored securely.
- Integration operations are tenant-scoped.
- Failures are observable and recoverable.
- Retried operations do not duplicate business effects.
- External API responses are validated.
- Integration status is not treated as proof that a business transaction succeeded unless the relevant confirmation has been verified.

# 23. Proposed Module Dependencies

The following is an initial dependency hypothesis. It must be validated during architecture design.

| Module | Proposed Dependency | Reason |
|---|---|---|
| CRM | Platform Core, Tenants, Users | Shared infrastructure |
| SALES | Platform Core, Tenants, Users | Sales workflows |
| INVOICING | Platform Core, Tenants, Users | Customer invoice management |
| E_INVOICING | INVOICING and provider configuration | Submission of supported invoice documents |
| ACCOUNTING | Platform Core, Tenants, Users | Financial ledger |
| VAT | Relevant invoicing and/or accounting workflows | Tax calculation and reporting |
| PROCUREMENT | Platform Core, Tenants, Users | Purchasing workflows |
| INVENTORY | Platform Core, Tenants, Users | Stock management |
| HRMS | Platform Core, Tenants, Users | Employee management |
| PAYROLL | HRMS | Employee and payroll information |
| PROJECTS | Platform Core, Tenants, Users | Project management |
| EXPENSES | Platform Core, Tenants, Users | Expense management |
| FIXED_ASSETS | Accounting for complete financial posting | Asset accounting |
| BANKING | Accounting for complete reconciliation | Financial reconciliation |
| REPORTING | Depends on each specific report | Data-source availability |
| INTEGRATIONS | Platform Core, Tenants, Users | Shared integration infrastructure |

### Dependency Rules

1. Shared platform dependencies must be documented.
2. Optional integrations must not automatically become mandatory commercial dependencies.
3. A module must not be activated when a required dependency is unavailable.
4. The system must explain dependency requirements before purchase.
5. Paid dependencies must be included in the displayed price calculation.
6. Removing a dependency must be blocked or coordinated with dependent modules.
7. Circular module dependencies must be rejected.
8. Dependency changes must be reviewed and tested.
9. The entitlement engine must enforce dependencies server-side.
10. Module dependencies must be stored as structured configuration rather than scattered conditional statements.

The final dependency graph belongs in `docs/01-architecture/MODULE_DEPENDENCIES.md`.

# 24. Shared Business Records and Domain Ownership

A modular ERP must avoid creating competing sources of truth for the same business entity.

## 24.1 Customer Records

The product must define a consistent ownership model for customer records.

CRM may own lead and opportunity workflows.

Customer master data used by invoicing and accounting must follow an approved shared-record strategy.

The architecture must avoid maintaining unrelated customer records in CRM, Sales, and Invoicing without a controlled synchronization mechanism.

## 24.2 Supplier Records

Procurement may own supplier onboarding and procurement-specific information.

Accounting may require supplier payment and tax information.

The system must define a consistent supplier identity and record ownership model.

## 24.3 Product Records

The architecture must define whether product master data is owned by Inventory or a shared product domain.

Sales, Procurement, and Invoicing must reference the approved product model rather than independently creating incompatible product definitions.

## 24.4 Employee Records

HRMS owns employee master records.

Payroll references approved employee and employment information.

The authentication system remains responsible for login identities and access control.

## 24.5 Financial Records

Accounting owns the authoritative general ledger.

Other modules may own operational documents and emit approved posting events.

No module may maintain a separate, conflicting general ledger.

# 25. Module Entitlement Rules

## 25.1 Entitlement Evaluation

For each module-protected operation, the backend must evaluate the relevant conditions.

A simplified conceptual rule is:

`Access Allowed = Tenant Valid AND User Authorized AND Module Entitled AND Dependencies Satisfied`

Additional restrictions may apply depending on subscription status, effective dates, tenant status, and approved policies.

## 25.2 Entitlement Enforcement Points

Entitlements must be enforced in:

- Django views.
- DRF endpoints.
- Domain services.
- Background jobs where appropriate.
- File downloads.
- Report generation.
- Data exports.
- Integration endpoints.
- Other interfaces that expose protected functionality.

## 25.3 Frontend Behavior

The frontend should use entitlement information to determine:

- Which modules appear in navigation.
- Which pages are available.
- Which actions are enabled.
- Which upgrade prompts should be shown.

Frontend visibility is a usability mechanism, not an authorization boundary.

## 25.4 Expired or Removed Entitlements

When a module entitlement ends:

- New protected operations must follow the approved access policy.
- Existing business data must remain preserved.
- Historical records must not be deleted automatically.
- Data export must follow the approved policy.
- Shared records used by other modules must not be deleted merely because one module is removed.
- Financial records must remain available according to the applicable retention and access rules.

# 26. Module-Level Quality Requirements

All commercially available modules must meet the following baseline requirements.

## 26.1 Tenant Isolation

- All tenant-owned business data must be scoped to the correct tenant.
- Cross-tenant access must be prevented.
- Tenant context must be validated server-side.
- Background tasks must preserve the correct tenant context.
- Tests must verify tenant isolation.

## 26.2 Authorization

- Permissions must be checked server-side.
- Sensitive actions must require explicit authorization.
- Administrative operations must be auditable.
- Direct API access must not bypass module entitlements.

## 26.3 Data Integrity

- Database constraints must enforce critical invariants where possible.
- Financial and operational changes must use controlled services.
- Duplicate business events must be prevented where relevant.
- Destructive operations must follow documented rules.

## 26.4 Auditability

The system must record relevant events such as:

- Creation of important business records.
- Approval and rejection.
- Changes to sensitive fields.
- Financial posting.
- Stock adjustments.
- Payroll approval.
- Subscription changes.
- Administrative overrides.

The exact audit scope must be defined for each module.

## 26.5 Testing

Each module must include:

- Unit tests.
- Service-level tests.
- API or view tests.
- Permission tests.
- Tenant isolation tests.
- Dependency integration tests.
- Failure-path tests.
- Regression tests for critical workflows.

## 26.6 Documentation

Each module must have a maintained specification describing:

- Scope.
- Business rules.
- Data ownership.
- Models.
- APIs and interfaces.
- Permissions.
- Dependencies.
- Events.
- Background jobs.
- Error handling.
- Acceptance criteria.
- Test requirements.
- Deployment considerations.

# 27. Commercial Release Checklist

Before any module moves to `AVAILABLE`, the release owner must confirm the following.

### Product Readiness

- Scope is documented.
- Required workflows are implemented.
- Acceptance criteria are satisfied.
- Known limitations are documented.
- User-facing descriptions are accurate.

### Technical Readiness

- Database migrations are tested.
- APIs and views are tested.
- Tenant isolation tests pass.
- Permission tests pass.
- Module entitlement checks are implemented.
- Dependencies are validated.
- Error handling is implemented.
- Background tasks are retry-safe where required.

### Financial Readiness

For modules that affect money, tax, payroll, inventory valuation, or financial records:

- Calculations are documented.
- Financial invariants are enforced.
- Duplicate posting is prevented.
- Audit records are available.
- Relevant specialist review is complete.
- Required reconciliation tests pass.

### Security Readiness

- Sensitive data is protected.
- Access controls are reviewed.
- File uploads and exports are secured where applicable.
- Secrets are not exposed.
- Critical administrative actions are audited.

### Commercial Readiness

- Module price is approved, if separately priced.
- Dependencies are commercially configured.
- Customer-facing descriptions are approved.
- Subscription and entitlement behavior is tested.
- Support procedures are documented.
- Any regulatory or integration claims have supporting evidence.

### Release Approval

The module may be marked `AVAILABLE` only after the authorized release owner approves the required evidence.

# 28. Module Addition and Change Control

Adding or changing a module requires a documented proposal.

The proposal must include:

1. Business justification.
2. Target customer segment.
3. Problem being solved.
4. Functional scope.
5. Non-goals.
6. Data ownership.
7. Proposed Django application.
8. Dependencies.
9. Subscription and pricing implications.
10. Security and permission requirements.
11. Integration requirements.
12. Testing strategy.
13. Deployment and migration impact.
14. Support and maintenance implications.
15. Acceptance criteria.
16. Release status.

The product owner must approve material scope changes.

Architecture changes must follow the applicable architecture decision process.

# 29. Instructions for Codex and Other Development Agents

AI development agents must treat this catalogue as an authoritative product boundary.

They must:

1. Use the stable module codes defined here.
2. Follow the approved Django application structure.
3. Avoid implementing unapproved modules as commercially available.
4. Avoid hardcoding module prices.
5. Avoid hardcoding dependencies in multiple parts of the application.
6. Preserve the separation between subscription billing and tenant invoicing.
7. Enforce module entitlements server-side.
8. Preserve tenant isolation.
9. Respect domain ownership boundaries.
10. Avoid duplicating financial calculations across modules.
11. Add automated tests for every new module workflow.
12. Update module specifications when scope changes.
13. Update the dependency graph when dependencies change.
14. Update the requirements traceability matrix.
15. Record unresolved design questions rather than inventing answers.
16. Never claim regulatory compliance without validated evidence and approval.
17. Never mark a module commercially available without release authorization.

When a task requires functionality outside the approved module scope, the agent must identify the scope gap and request or prepare a documented change proposal.

# 30. Definition of Completion

This catalogue is ready for implementation planning when:

- The module registry has been reviewed.
- Module ownership boundaries are documented.
- Proposed dependencies have been validated.
- Shared customer, supplier, product, employee, and financial record ownership is defined.
- Commercial availability states are approved.
- The initial release module selection is confirmed.
- Module-level acceptance requirements are accepted.
- Open questions have owners.
- The architecture and roadmap reference this catalogue.

The catalogue does not mean that all listed modules are implemented or ready for sale.

Commercial availability must be established independently through implementation, testing, security review, operational readiness, and explicit release approval.

---

**End of Document**