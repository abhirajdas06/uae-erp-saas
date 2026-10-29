# P05 — Accounting and UAE VAT Phase Specification

| Property | Value |
|---|---|
| Document ID | P05-SPEC-001 |
| Status | APPROVED SPECIFICATION — FINANCE/TAX POLICY GATES REMAIN |
| Phase | P05 |
| Regulatory cut-off | 29 October 2026 |
| Implementation authorization | NOT GRANTED |

## 1. Objective and Authority

Establish the tenant/legal-entity accounting ledger and effective-dated UAE VAT calculation/reporting foundation for explicitly approved transaction types. Implements `ACC-001`–`ACC-005`, `VAT-001`–`VAT-003`, `REP-002`, applicable NFRs, ADR-011, ADR-013–015, ADR-018 and [REG-SRC-001](../../00-product/UAE_REGULATORY_SOURCE_REGISTER.md).

This phase is not accounting, tax or filing advice and does not represent automatic FTA filing or statutory compliance.

## 2. Entry Gates

- P01 tenant/IAM/audit, P02 entitlement and relevant P03 immutable source contracts are verified.
- Accounting ownership, legal-entity model, currency/rounding, posting/period policy and VAT supported-treatment policy are approved.
- Product Owner approves bounded P05 implementation (`APPR-P05-001`).
- Tax-dependent schema/behavior waits for `APPR-P05-003`; unsupported treatments remain disabled.

## 3. Included Scope

- Tenant/legal-entity chart of accounts, account types/statuses and controlled configuration.
- Fiscal years/periods, journals, draft entries/lines, posting, reversal/adjustment and close/reopen controls.
- Immutable balanced ledger, source uniqueness, trial balance, general ledger and financial-statement foundations.
- Receivable/payable control-account posting and source reconciliation; business subledgers remain in their source modules.
- Effective-dated VAT registrations/configuration, tax codes/treatments, calculation service and immutable tax snapshots.
- Approved sales and later purchase tax integration contracts; VAT transaction register, reconciliation and return workpapers.
- Permissions, segregation, audit, tenant isolation, reports/exports, migrations, recovery, monitoring and test evidence.

## 4. Excluded Scope

- Inventing accounting policies, a statutory chart, tax advice, unsupported VAT treatments or filing credentials.
- Automatic FTA return filing/payment, tax-registration workflow, tax-group consolidation, corporate tax, payroll tax or customs.
- P06 supplier documents, P09 bank truth/reconciliation, consolidation, revenue recognition, budgets, advanced FX/revaluation, or IFRS certification unless separately approved.
- Editing/deleting posted entries or recomputing historical values from current policy/rates.

## 5. Domain Ownership

`accounting` owns accounts, periods, journals, entries/lines, postings, reversals, ledger queries, trial balance and financial-statement mappings. `vat` owns tax registrations/configuration, effective-dated tax rules/codes, calculation policy, tax snapshots, VAT transaction classifications, adjustments, reconciliations and return workpapers. Source modules own commercial documents; they request calculation/posting through versioned contracts and cannot write ledger lines directly.

## 6. Accounting Controls

- Drafts are editable under authorization; posting is one transactional service that validates tenant/legal entity, approval, open period, accounts/dimensions, exact currency amounts, balance, source idempotency, audit and outbox.
- Every posted entry is balanced under the approved base/transaction-currency policy. Partial posting is impossible.
- Protected posted meaning is immutable. Corrections use linked reversal plus adjustment/new entry; original and reason remain.
- Closing/reopening is authorized, audited and reconciliation-backed. Closed-period posting fails; exceptional reopen/backdate requires approved policy.
- Ledger/report data derives from posted lines. Accelerators reconcile to authoritative lines and are rebuildable.
- Source event/version is unique per posting purpose; repeats return the original result or conflict on changed payload.

## 7. VAT Controls

- Rules are jurisdiction/legal-entity/registration/document/treatment/effective-date/version specific. No one-rate shortcut.
- Tax calculation uses `Decimal`, approved taxable-base, inclusivity, line/category/document rounding and residual rules; client totals never control.
- Issued/posted transactions snapshot inputs, tax outcome, currency, source and ruleset version. Later configuration cannot alter history.
- VAT transaction register and workpapers reconcile from source tax snapshots to accounting tax/control accounts with explicit differences.
- Corrections/credits/adjustments reference originals and apply approved period/treatment rules.
- Filing outputs are labelled workpapers/drafts unless an exact current FTA format and submission contract is separately approved.

## 8. Security, Isolation and Operations

Create/configure/approve/post/reverse/close/reopen/tax-configure/report/export are separate permissions, with entitlement additionally enforced. Every service, report, export, task, cache, admin and restore path is tenant/legal-entity scoped with approved RLS. Sensitive margins, tax identifiers, payroll/bank-source dimensions and unrestricted ledger exports use least privilege and audit.

Migrations define UUID/tenant keys, precision/scale/ranges, same-tenant references, uniqueness, backfills and old/new compatibility. Changes to posted or tax history require before/after per-tenant/legal-entity/currency/account/tax reconciliation and recovery evidence. Monitoring covers unbalanced drafts, failed/duplicate postings, closed-period attempts, source-ledger/VAT differences, policy expiry, export volume and privileged changes.

## 9. Acceptance Criteria

| ID | Criterion |
|---|---|
| P05-AC-001 | Approved legal-entity, accounting, currency/rounding and VAT policy versions are recorded; unsupported behavior is disabled |
| P05-AC-002 | Chart accounts are tenant/legal-entity scoped, valid, uniquely coded in approved scope and safely retired |
| P05-AC-003 | Fiscal periods have explicit state; close/reopen/backdate controls and evidence are enforced |
| P05-AC-004 | Journal drafts validate accounts, dimensions, dates, currencies, amounts and approvals |
| P05-AC-005 | Posting commits one balanced immutable ledger result or none and is safe under retry/concurrency |
| P05-AC-006 | Posted corrections preserve original, linked reversal/adjustment, reason, actor and eligible period |
| P05-AC-007 | Source-to-ledger contracts prevent direct writes and duplicate postings |
| P05-AC-008 | General ledger and trial balance reproduce from posted lines and reconcile by tenant/entity/currency |
| P05-AC-009 | AR/AP control balances reconcile to approved source records without moving subledger ownership |
| P05-AC-010 | VAT rules/codes are effective-dated, authorized, audited and historically reproducible |
| P05-AC-011 | VAT calculations use approved Decimal, base, inclusivity, rounding/residual and correction policies |
| P05-AC-012 | Tax snapshots cannot drift after source issue/posting or ruleset change |
| P05-AC-013 | VAT register/workpapers reconcile source snapshots, ledger tax accounts and documented adjustments |
| P05-AC-014 | Outputs do not claim filing/compliance outside exact validated scope |
| P05-AC-015 | Permission, segregation, entitlement, tenant isolation, RLS and privileged-access tests pass |
| P05-AC-016 | Audit evidence is sufficient and redacted; protected posted/tax records resist ordinary mutation/deletion |
| P05-AC-017 | Clean/upgrade/overlap migration, backup/restore and financial reconciliation pass |
| P05-AC-018 | Reports/exports are authorized, formula-safe, bounded and currency/treatment explicit |
| P05-AC-019 | Full financial, property, concurrency, failure, security and performance gates pass |
| P05-AC-020 | Finance, qualified UAE tax, Security, Database, Operations and independent QA reviews are dispositioned |
| P05-AC-021 | Product Owner approves P05 exit and separately approves production accounting/VAT scope |

## 10. Task Order and Evidence

| Task | Scope | Evidence |
|---|---|---|
| P05-T01 | Accounting/tax/currency policy and contracts | P05-EV-001–002 |
| P05-T02 | Chart, legal entity, fiscal periods and journals | P05-EV-003 |
| P05-T03 | Posting, immutable ledger, reversal and period close | P05-EV-004–005 |
| P05-T04 | Source posting/AR/AP reconciliation contracts | P05-EV-006 |
| P05-T05 | VAT configuration and calculation service | P05-EV-007–008 |
| P05-T06 | VAT register, adjustments, reconciliation and workpapers | P05-EV-009 |
| P05-T07 | UI, reports, exports and audit/security | P05-EV-010–011 |
| P05-T08 | Migration, recovery, performance and operations | P05-EV-012–013 |
| P05-T09 | Independent specialist review and exit | P05-EV-014–015 |

## 11. Exit Gate

All P05-AC-001–021 are `VERIFIED`; there is no critical/high isolation, authorization, financial-integrity, posting, tax-calculation, historical-drift, secret or migration finding; supported/disabled policies and current source reviews are recorded; reconciliations balance or explain every difference; and specialist plus Product Owner approvals are explicit. Exit does not approve tax filing or production scope beyond the recorded decision.

## 12. Pending Approvals

| ID | Decision / approver | Review and recommendation | Recording method | Blocks |
|---|---|---|---|---|
| APPR-P05-001 | Bounded phase scope — Product Owner | Approve foundation ledger + validated VAT workpapers; keep filing/advanced scope excluded | “I approve P05-SPEC-001 as the bounded P05 implementation scope, subject to its named gates.” | P05 implementation |
| APPR-P05-002 | Accounting/currency/period policy — Finance + Product + Architecture | Approve legal-entity/base currency, precision, accounts, dimensions, posting, reversal, close/reopen, opening balance and initial FX scope | Versioned finance policy record referencing ADR-011/013 and enabled limitations | Schema/posting implementation |
| APPR-P05-003 | UAE VAT policy — qualified UAE tax reviewer + Finance/Product | Approve supported treatments, evidence, invoice/credit rules, calculations, rounding, adjustments, periods, workpaper mappings and source versions | Signed/versioned VAT policy referencing REG-SRC IDs/checksums/effective date | Tax schema/calculation/report activation |
| APPR-P05-004 | Exit/production — Product Owner after independent reviews | Approve exact accounting/VAT production scope and limitations; filing remains separate | Explicit P05 exit and production-scope statement | Phase exit / production |
