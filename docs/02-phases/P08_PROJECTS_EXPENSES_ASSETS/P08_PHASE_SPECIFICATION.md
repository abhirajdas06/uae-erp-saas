# P08 — Projects, Expenses and Fixed Assets Phase Specification

| Property | Value |
|---|---|
| Document ID | P08-SPEC-001 |
| Status | READY FOR REVIEW — DOMAIN AND FINANCE POLICY APPROVAL REQUIRED |
| Implementation authorization | NOT GRANTED |

## 1. Objective and Authority

Deliver bounded project operations, employee/business expense control and a fixed-asset register with deterministic depreciation, without duplicating Accounting, Banking, Payroll or document-storage authority. This phase implements `PROJ-001`, `EXP-001`, `FA-001` and `FA-002` under ADR-003–006, ADR-010–011, ADR-013–015 and ADR-018–020.

This specification is an implementation contract candidate, not proof of accounting, tax or regulatory compliance.

## 2. Entry Gates

- P01 tenancy/IAM/audit, P02 entitlement and P05 accounting posting contracts are verified for the enabled scope.
- P03 customer references, P06 item/procurement/receipt references, P07 employee references and P09 settlement references are used only where their contracts are available.
- Project/time/costing, expense/reimbursement/VAT and asset/depreciation policies are approved and versioned.
- Product Owner approves bounded P08 scope (`APPR-P08-001`) before implementation.

## 3. Included Scope

- Projects: tenant projects, customer reference, members, tasks, milestones, status, dates, assignments and operational progress.
- Expenses: categories, claims, lines, currencies, private receipts, draft/submitted/approved/rejected/cancelled lifecycle, reimbursement evidence and versioned accounting/VAT requests.
- Fixed assets: asset categories/register, acquisition/in-service facts, location/custodian, approved depreciation schedule/runs, transfers, disposals and accounting requests.
- Role/object/field permissions, entitlement, tenant isolation, audit, imports/exports, reports, migrations, recovery and monitoring.

## 4. Excluded Scope

- Advanced resource planning, timesheets, project billing, earned value, project accounting, revenue recognition or portfolio optimization unless separately approved.
- Travel booking, corporate-card feeds, OCR as an authoritative source, cash advances, per-diem/tax rules or direct payment initiation.
- Asset revaluation, impairment, component accounting, lease accounting, tax depreciation, construction-in-progress or complex multi-book accounting unless separately approved.
- Direct ledger writes, bank settlement and silent inference of finance/tax policy.

## 5. Ownership and Boundaries

`projects` owns operational projects, tasks, milestones, memberships and progress. CRM owns customers; HRMS owns employees; Accounting owns ledger, cost-centre and financial reporting truth.

`expenses` owns claims, claim lines, receipt links, approvals and reimbursement workflow evidence. Accounting owns postings and VAT treatment; Payroll or Banking owns an approved reimbursement route and settlement evidence.

`fixed_assets` owns the asset register, book-policy assignment, depreciation calculations/schedules and asset lifecycle. Procurement owns purchase/receipt evidence; Accounting owns capitalisation, depreciation and disposal postings.

All cross-module references are tenant-aware, stable and validated. Downstream records snapshot the business facts needed to reproduce historical results.

## 6. Core Controls

- Workflows use explicit transitions, optimistic/concurrency protection and maker-checker where financial effects arise.
- Authoritative amounts use `Decimal`, explicit currency and ADR-013 rounding stages; client totals are never trusted.
- Approved/finalized claims, schedules and posting evidence are append-oriented. Corrections, reversals, reclassifications and disposals remain linked.
- Source/purpose/version idempotency prevents duplicate reimbursement, depreciation and accounting effects.
- Expense receipts and asset evidence follow ADR-019 private-file controls; download authorization is re-evaluated.
- A changed project/customer/employee/item master does not rewrite historical expense or asset snapshots.

## 7. Domain Rules

### 7.1 Projects

Project codes are unique within the approved tenant/legal-entity scope. Status, dates, task hierarchy depth, assignment and completion rules are explicit. Project closure blocks or warns on open tasks/expenses/assets according to approved policy. Operational progress is never presented as an Accounting balance.

### 7.2 Expenses

A claim records claimant identity type, entity, currency, category, date, merchant/business purpose, line amounts, tax facts, receipts and policy version. Submission validates duplicates and required evidence. Approval is separate from preparation; stale changes invalidate approval. Reimbursement statuses distinguish prepared, submitted, accepted, rejected, uncertain and settled only when evidence supports them.

### 7.3 Fixed Assets

Each asset has stable identity, entity, category, acquisition source/cost/currency, in-service date, location/custodian and policy version. Depreciation requires approved method, useful life, residual value, convention, frequency, precision and start/stop rules. Runs are deterministic, transactional and immutable after posting. Disposal/correction creates linked evidence and reconciliation; it does not erase history.

## 8. Migration, Recovery and Operations

Migrations preserve tenant ownership, workflow state, snapshots, source/version keys, files, schedule/run versions and posting/reimbursement links. Backfills with financial effect require dry-run before/after totals and Finance approval. Restore evidence reconciles claims, approved/reimbursed totals, assets, accumulated depreciation, net book value, postings, files, outbox and audit.

Monitor stale approvals, duplicate claims, suspicious receipt/file access, reimbursement uncertainty, depreciation exceptions, posting mismatch, asset policy expiry, bulk exports and cross-tenant denials.

## 9. Acceptance Criteria

| ID | Criterion |
|---|---|
| P08-AC-001 | Approved scope and project/expense/asset policies are versioned; unsupported behavior fails closed |
| P08-AC-002 | Project identity, lifecycle, task/milestone hierarchy and assignments are tenant-safe and historically traceable |
| P08-AC-003 | Project closure and operational reporting enforce approved open-work rules without claiming ledger authority |
| P08-AC-004 | Expense claim facts, totals, currency, receipts and policy snapshot are deterministic and complete |
| P08-AC-005 | Expense submission/approval/correction is authorized, maker-checker, stale-safe and historically preserved |
| P08-AC-006 | Duplicate claims and repeated reimbursement/posting requests cannot create duplicate effects |
| P08-AC-007 | Reimbursement/provider states are evidence-based and never overstate settlement |
| P08-AC-008 | Expense Accounting/VAT requests are versioned, idempotent and reconciled |
| P08-AC-009 | Asset identity, acquisition/in-service facts, location/custodian and policy assignment preserve history |
| P08-AC-010 | Depreciation is exact, deterministic and reproducible from approved effective policy and snapshots |
| P08-AC-011 | Depreciation finalization and Accounting requests are transactional, immutable and duplicate-safe |
| P08-AC-012 | Transfer, correction and disposal preserve linked history and reconcile cost/depreciation/net-book-value |
| P08-AC-013 | Permissions, entitlements, object/field controls, tenant scoping and RLS protect every surface |
| P08-AC-014 | Files, exports, logs, audit and support access meet sensitive-data controls |
| P08-AC-015 | Migration and restore reconcile operational, financial, file, audit and event evidence |
| P08-AC-016 | Performance, monitoring, incident/runbook and accessibility evidence meets approved targets |
| P08-AC-017 | Finance, Security, Database and independent review findings are dispositioned before exit |
| P08-AC-018 | Product Owner records bounded phase exit separately from any production activation |

## 10. Evidence and Approval Gates

Planned evidence `P08-EV-001`–`P08-EV-014` is defined by P08-TRACE-001. Required approvals are `APPR-P08-001` scope, `APPR-P08-002` project/time/costing, `APPR-P08-003` expense/reimbursement/VAT, `APPR-P08-004` asset/depreciation and `APPR-P08-005` exit. Approval instructions are canonical in `DECISIONS_PENDING.md`.
