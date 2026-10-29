# Launch Report Catalogue

| Property | Value |
|---|---|
| Document ID | PROD-REPORTS-001 |
| Status | PROPOSED CATALOGUE — `DEC-REP-001` APPROVAL REQUIRED |
| Owner | Product Owner / Reporting domain owner |
| Related documents | `MASTER_PRODUCT_SPECIFICATION.md`, `../03-modules/REPORTING.md`, `../03-modules/ACCOUNTING.md`, `../05-quality/DATA_PROTECTION_AND_RETENTION.md` |

## 1. Purpose and Boundary

`MASTER_PRODUCT_SPECIFICATION.md` section 14 states that the initial report catalogue remains to be defined, and `../03-modules/REPORTING.md` REPM-001 requires every report to have an approved definition before implementation while `DEC-REP-001` must approve the launch catalogue. Without a named catalogue, no reporting work can be bounded, estimated or tested. This document proposes that catalogue.

This document owns the report definition contract, the proposed launch catalogue, sensitivity and entitlement mapping, statutory-output boundaries and deliberate exclusions. It does not own report execution architecture, authorization, caching, resource limits or artifact handling, which remain with `../03-modules/REPORTING.md`; nor financial truth, which remains with `../03-modules/ACCOUNTING.md`.

Every report in this catalogue is `PROPOSED`. None is approved, specified to field level or implemented. A report listed here confers no commitment until `DEC-REP-001` approves it and its owning phase specifies it.

## 2. Report Definition Contract

Before implementation, each report requires a definition recording all of the following. A report implemented without a complete definition is a defect under REPM-001.

| Field | Requirement |
|---|---|
| Report ID and version | Stable identifier and version; a semantic change creates a new version |
| Owning module | Single owning module specification |
| Source of truth | The authoritative records it reads; financial totals must reconcile to Accounting per REPM-004 |
| Parameters | Name, type, required status, default, and validation for each |
| Date semantics | Transaction date, posting date or as-of basis, and the period convention |
| Currency semantics | Base, transaction or presentation currency, and the rounding treatment under ADR-013 |
| Time zone and as-of behavior | How the tenant time zone and cut-off apply |
| Required permission | The permission a viewer must hold |
| Required entitlement | The module entitlement that makes it available |
| Sensitivity | Data classification of its most sensitive column, per `../05-quality/DATA_PROTECTION_AND_RETENTION.md` |
| Field-level restrictions | Columns requiring additional authority |
| Resource class | Expected volume, cost and whether background execution is required |
| Output formats | Screen, printable document, and machine-readable export where permitted |
| Retention | Retention class for snapshots and artifacts |
| Reconciliation test | The fixture-based test proving its totals agree with the source of truth |

## 3. Cross-Cutting Rules

| ID | Requirement |
|---|---|
| RPT-001 | Every report is tenant-scoped, and tenant, role, object and field filters apply before aggregation and before caching, per REPM-002 |
| RPT-002 | A report never presents a financial total calculated differently from the authoritative record without a documented, approved reason, per `MASTER_PRODUCT_SPECIFICATION.md` section 14 |
| RPT-003 | A report is a read-only view; it never changes authoritative business state |
| RPT-004 | A report containing `C3` or higher data requires export permission and is audited as a disclosure |
| RPT-005 | A report that can return large result sets executes in the background with an authorization-revalidated delivery step |
| RPT-006 | A report reflects only the modules the tenant is entitled to; an unentitled source produces an explicit unavailability message, not a partial or silently filtered figure |
| RPT-007 | Every report declares whether it is reproducible as at a past date, and a snapshot is retained where reproducibility is required |
| RPT-008 | Report labels, headings and exports are localizable and direction-correct per `../01-architecture/LOCALIZATION_AND_BILINGUAL_UI.md`, while numeric exports remain machine-parseable |
| RPT-009 | A report is never presented as a statutory filing, a submission or evidence of compliance |

## 4. Proposed Launch Catalogue

Sensitivity uses the classification in `../05-quality/DATA_PROTECTION_AND_RETENTION.md`. Resource class is `S` for small and interactive, `M` for moderate, and `L` for large and background-only.

### 4.1 Accounting and Finance

| ID | Report | Purpose | Source of truth | Sensitivity | Class |
|---|---|---|---|---|---|
| RPT-101 | Trial balance | Account balances for a period, with opening, movement and closing | General ledger | C2 | S |
| RPT-102 | General ledger detail | Transaction-level account activity with running balance | General ledger | C2 | M |
| RPT-103 | Journal register | All journal entries with status, actor and source document | General ledger | C2 | M |
| RPT-104 | Profit and loss | Income and expense by period, with comparatives | General ledger | C2 | S |
| RPT-105 | Balance sheet | Financial position as at a date | General ledger | C2 | S |
| RPT-106 | Cash flow summary | Movement by cash and bank account; method requires approval | General ledger and banking | C2 | M |
| RPT-107 | Account reconciliation status | Control account against subsidiary ledger, with differences | General ledger and subsidiary ledgers | C2 | M |
| RPT-108 | Period close status | Closed, open and pending periods with blocking items | Accounting | C1 | S |
| RPT-109 | Audit trail extract | Who changed what, when, within a scope | Audit foundation | C4 | L |

### 4.2 Sales, Receivables and Invoicing

| ID | Report | Purpose | Source of truth | Sensitivity | Class |
|---|---|---|---|---|---|
| RPT-201 | Sales by period | Revenue by period, with comparatives | Sales and ledger | C2 | S |
| RPT-202 | Sales by customer, item or salesperson | Revenue composition analysis | Sales | C2 | M |
| RPT-203 | Invoice register | All issued invoices with status, tax treatment and totals | Invoicing | C2 | M |
| RPT-204 | Credit and debit note register | Corrections issued, with reason and linked invoice | Invoicing | C2 | S |
| RPT-205 | Receivables ageing | Outstanding balances by time band, reconciled to the control account | Receivables | C2 | M |
| RPT-206 | Customer statement | Per-customer account activity and balance, as a sendable document | Receivables | C3 | S |
| RPT-207 | Collections and receipts | Receipts applied and unapplied, by period | Receivables and banking | C2 | M |
| RPT-208 | Quotation and order pipeline | Open quotations and orders by stage and value | CRM and Sales | C2 | S |
| RPT-209 | E-invoicing submission status | Submission outcome, acknowledgement and exception state per document | E-invoicing module and provider evidence | C2 | M |

### 4.3 Tax

| ID | Report | Purpose | Source of truth | Sensitivity | Class |
|---|---|---|---|---|---|
| RPT-301 | VAT summary by tax treatment | Output and input amounts grouped by treatment for a tax period | Ledger and tax records | C2 | M |
| RPT-302 | VAT transaction detail | Transaction-level support for each summary line | Ledger and tax records | C2 | L |
| RPT-303 | VAT return preparation view | Figures arranged to support return preparation | Ledger and tax records | C2 | M |
| RPT-304 | Tax reconciliation | Tax control accounts against the computed position, with differences | Ledger | C2 | M |
| RPT-305 | Non-compliant document exception report | Documents missing mandatory content or failing validation | Invoicing and e-invoicing | C2 | M |

`RPT-301` to `RPT-305` are preparation aids. None is a return, a filing, a submission or evidence of a tax position. Their line composition, grouping and labelling require the tax-specialist confirmation recorded in `../07-project-management/DECISIONS_PENDING.md` before implementation, and no figure may be labelled as a return box reference until that confirmation is dated and sourced.

### 4.4 Procurement, Payables and Inventory

| ID | Report | Purpose | Source of truth | Sensitivity | Class |
|---|---|---|---|---|---|
| RPT-401 | Purchases by period and supplier | Spend composition | Procurement and ledger | C2 | M |
| RPT-402 | Purchase order status | Open, partially received and closed orders | Procurement | C2 | S |
| RPT-403 | Payables ageing | Outstanding supplier balances by time band, reconciled to the control account | Payables | C2 | M |
| RPT-404 | Supplier statement | Per-supplier activity and balance | Payables | C3 | S |
| RPT-405 | Goods receipt and three-way match exceptions | Order, receipt and invoice mismatches | Procurement | C2 | M |
| RPT-406 | Stock on hand and valuation | Quantity and value by item and location, reconciled to the inventory control account | Inventory | C2 | M |
| RPT-407 | Stock movement history | Receipts, issues, transfers and adjustments | Inventory | C2 | L |
| RPT-408 | Stock ageing and slow-moving items | Holding period analysis | Inventory | C2 | M |
| RPT-409 | Reorder and shortage exceptions | Items below threshold or short against demand | Inventory | C2 | S |

### 4.5 Payroll and Human Resources

| ID | Report | Purpose | Source of truth | Sensitivity | Class |
|---|---|---|---|---|---|
| RPT-501 | Payroll run summary | Totals by component and cost centre for a run | Payroll | C4 | M |
| RPT-502 | Payroll register | Per-employee gross, deductions and net for a run | Payroll | C4 | M |
| RPT-503 | Payslip | Per-employee statement as a sendable document | Payroll | C4 | S |
| RPT-504 | Payroll journal reconciliation | Payroll totals against posted ledger entries | Payroll and ledger | C2 | S |
| RPT-505 | Wage protection submission status | File generation and submission outcome per period | Payroll | C4 | M |
| RPT-506 | End of service provision and settlement | Accrued and settled terminal entitlements | Payroll and HR | C4 | M |
| RPT-507 | Employee master and headcount | Headcount, movement, joiners and leavers | HR | C3 | S |
| RPT-508 | Leave balance and liability | Entitlement, taken, balance and accrued liability | HR | C3 | M |
| RPT-509 | Document expiry exceptions | Identity, residency and licence documents approaching expiry | HR | C4 | S |

Payroll reports are restricted by default to explicitly authorized payroll roles and carry field-level restriction on salary and bank detail columns.

### 4.6 Projects, Expenses and Assets

| ID | Report | Purpose | Source of truth | Sensitivity | Class |
|---|---|---|---|---|---|
| RPT-601 | Project profitability | Revenue, cost and margin by project | Projects and ledger | C2 | M |
| RPT-602 | Project budget against actual | Variance by project and cost category | Projects | C2 | M |
| RPT-603 | Work in progress and unbilled | Unbilled time and cost by project | Projects | C2 | M |
| RPT-604 | Timesheet summary | Recorded time by employee, project and period | Projects | C3 | M |
| RPT-605 | Expense claim register and status | Claims by status, claimant and period | Expenses | C3 | S |
| RPT-606 | Expense analysis by category | Spend composition and policy exceptions | Expenses | C2 | M |
| RPT-607 | Fixed asset register | Cost, additions, disposals, depreciation and net book value | Fixed assets | C2 | M |
| RPT-608 | Depreciation schedule | Charge by period and asset class, reconciled to the ledger | Fixed assets and ledger | C2 | M |

### 4.7 Banking

| ID | Report | Purpose | Source of truth | Sensitivity | Class |
|---|---|---|---|---|---|
| RPT-701 | Bank reconciliation statement | Statement against ledger, with unreconciled items | Banking and ledger | C2 | M |
| RPT-702 | Cash and bank position | Balances by account as at a date | Banking and ledger | C2 | S |
| RPT-703 | Payment run and instruction status | Instructions, outcomes and exceptions | Banking | C4 | M |
| RPT-704 | Unreconciled and ageing exceptions | Items outstanding beyond a threshold | Banking | C2 | S |

### 4.8 Platform and Provider Domain

These reports belong to the provider domain and are never visible to a tenant.

| ID | Report | Purpose | Source of truth | Sensitivity | Class |
|---|---|---|---|---|---|
| RPT-801 | Tenant and subscription status | Lifecycle state, plan and entitlement per tenant | Tenants and subscriptions | C2 | S |
| RPT-802 | Subscription revenue and billing status | Platform invoicing, collection and dunning position | SaaS billing | C2 | M |
| RPT-803 | Module adoption and usage | Entitlement against actual use | Platform | C1 | M |
| RPT-804 | Platform operational health | Availability, error rate, queue and job health | Operations | C1 | S |
| RPT-805 | Security and access review | Privileged access, support access and anomalous activity | Audit and operations | C4 | M |

## 5. Deliberate Exclusions

The following remain out of scope at launch, consistent with `../03-modules/REPORTING.md` section 1.

| Exclusion | Reason |
|---|---|
| Unrestricted ad hoc SQL or free-form report builder | Tenant isolation, resource and correctness risk |
| Cross-tenant benchmarking or aggregated market data | Requires an approved business requirement and a documented authorization and privacy model |
| Data warehouse, data lake or external analytics replication | Separate architecture decision, not a reporting feature |
| Statutory return filing or submission from a report | Regulatory scope owned by the tax and e-invoicing modules |
| Predictive, forecasting or scoring analytics | Speculative; excluded under `AGENTS.md` section 2 |
| Scheduled distribution to external recipients | Requires the disclosure decision `DEC-NTF-005` |

## 6. Acceptance and Tests

| ID | Verification |
|---|---|
| RPT-TST-001 | Every implemented report has an approved definition with a complete contract |
| RPT-TST-002 | Each financial report reconciles to its source of truth against fixtures |
| RPT-TST-003 | Subsidiary-ledger reports reconcile to their control accounts |
| RPT-TST-004 | Tenant, role, object and field filters apply before aggregation and before caching |
| RPT-TST-005 | A cross-tenant request returns no foreign data through any report, parameter, cache or artifact path |
| RPT-TST-006 | An unentitled module produces an explicit unavailability outcome rather than a partial figure |
| RPT-TST-007 | Reports containing `C3` or higher data require export permission and produce a disclosure audit entry |
| RPT-TST-008 | Date, currency, rounding, time-zone and as-of semantics reproduce fixture expectations |
| RPT-TST-009 | Large reports execute in the background and revalidate authorization at delivery |
| RPT-TST-010 | Reproducible-as-at reports return identical figures from a retained snapshot |
| RPT-TST-011 | Labels and exports are localizable and direction-correct while numeric exports remain machine-parseable |
| RPT-TST-012 | No report is labelled as a filing, submission or compliance evidence |

All scenarios are `NOT_RUN` until the owning phase implements the reports.

## 7. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-REP-001 | Approve the launch report catalogue, semantics, freshness, resource classes and retention. This document is the proposal for that decision | Product Owner |
| DEC-REP-002 | Confirm, with dated authoritative sources, the line composition and labelling of `RPT-301` to `RPT-305`, and whether any may reference return box numbers | Tax specialist |
| DEC-REP-003 | Approve the cash flow method for `RPT-106` | Finance domain owner |
| DEC-REP-004 | Approve the default role-to-report visibility matrix, particularly for payroll and banking reports | Product Owner |
| DEC-REP-005 | Approve which reports must be reproducible as at a past date and therefore retain snapshots | Finance domain owner / Privacy reviewer |

These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`. No report is approved by this document.
