# ACCOUNTING — General Ledger and Financial Accounting Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-ACCOUNTING-001 |
| Status | APPROVED SPECIFICATION — FINANCE POLICY GATES REMAIN |
| Owning phase / app | P05 / `accounting` |
| Tenant-owned data | Yes; explicit legal-entity scope |

## 1. Purpose and Boundaries

Own chart of accounts, fiscal periods, journals, posted entries/lines, reversals, ledger queries, trial balance and financial-statement foundations under `ACC-001`–`ACC-005`, ADR-011/013 and P05-SPEC-001.

Source modules own invoices, supplier documents, inventory, payroll, assets, expenses and bank transactions. They request posting through versioned services and cannot create ledger lines directly. VAT owns tax policy/snapshots/workpapers. Excluded initially: consolidation, budgets, advanced cost accounting, full FX revaluation, revenue recognition, bank feeds and any accounting-standard certification.

## 2. Actors and Permissions

Account/configuration manager; journal preparer; journal approver; posting operator; period-close/reopen approver; finance reporter; auditor; purpose-bound support. Account maintenance, draft, approval, posting, reversal, close, reopen, export and privileged access are distinct permissions. Separation-of-duty thresholds are policy-driven.

## 3. Model and Ownership

Conceptual records: `Account`, `AccountType`, `FiscalYear`, `AccountingPeriod`, `Journal`, `JournalEntry`, `JournalLine`, `PostingOperation`, `ReversalLink`, `FinancialStatementMapping` and `ReconciliationFinding`.

- UUIDs plus tenant/legal entity; same-tenant/entity references are enforced.
- Account code uniqueness scope, hierarchy, type/normal-balance and retirement behavior require approved policy.
- Lines carry debit or credit, transaction/base currency amounts and approved dimensions; no floats.
- Posted entries snapshot descriptions, sources, currencies/rates, amounts, policies, approvals and dates required for reproduction.
- Unique source/version/purpose and idempotency prevent duplicate postings.
- Posted entries/lines are append-oriented and protected from ordinary update/delete.

## 4. Workflows and Invariants

**Chart/period:** configuration validates scope and prevents changes that reinterpret posted history. Periods do not overlap in an entity/fiscal calendar. Close validates approved reconciliations; reopen requires stronger permission, reason and audit.

**Draft/approval:** server validates dates, accounts, dimensions, decimal ranges/currencies, source and approvals. Draft changes are version-controlled; stale approval is rejected.

**Posting:** one transaction locks the draft/source/period, revalidates policy and permissions, proves debit=credit under approved base-currency rules, writes posted lines/audit/outbox, and commits. Any failure writes no partial ledger. Repeats return the same result; changed-payload key reuse conflicts.

**Reversal/adjustment:** create a linked equal/opposite entry in an eligible period with reason and approval. Correct values use a new adjustment; originals remain. Closed history is never silently reopened or overwritten.

**Reporting/reconciliation:** ledger/trial balance derive from posted lines. Statement mappings are versioned. Source/control balances and cached/report projections reconcile to the ledger; cross-currency totals are not aggregated without an approved conversion basis.

## 5. Business Rules

| ID | Rule / verification |
|---|---|
| ACCM-001 | Account codes/types/statuses and entity ownership follow approved constraints; model tests |
| ACCM-002 | Period overlap/closed-state/backdate/reopen controls are enforced at service/database boundaries; workflow tests |
| ACCM-003 | Posted entries balance and commit atomically or not at all; property/transaction tests |
| ACCM-004 | Posted meaning cannot be edited/deleted through UI/API/admin/import/task/runtime role; immutability tests |
| ACCM-005 | Posting/reversal is idempotent and safe under concurrency; concurrency/failure tests |
| ACCM-006 | Source modules cannot directly write ledger and duplicate source purpose is rejected; boundary tests |
| ACCM-007 | Reversal preserves original and equal/opposite approved effect; financial tests |
| ACCM-008 | Ledger/trial balance reproduce and reconcile by entity/period/account/currency; reconciliation tests |
| ACCM-009 | AR/AP control balances link to source records without transferring subledger ownership; contract tests |
| ACCM-010 | Permission/segregation/entitlement/isolation/RLS cover all paths; security tests |
| ACCM-011 | Audit records actor/source/policy/approval/correlation without prohibited data; audit tests |
| ACCM-012 | Migrations/restore preserve totals, links, sequences and history; migration/recovery tests |

## 6. Interfaces and Operations

Versioned posting request includes tenant/legal entity, source type/ID/version/purpose/hash, posting date, policy version, currency/rate evidence, lines/dimensions and idempotency key. Result returns stable operation/entry IDs and status; errors distinguish validation, permission, period, duplicate/conflict and failure without data leakage. Outbox publishes posted/reversed facts after commit.

UI covers account/period setup, journal preparation/approval/post, reversal and traceable ledger/drill-down. Imports create drafts only through preview/validation/idempotency; cannot mark posted. Exports are bounded, permissioned, formula-safe and currency/policy explicit.

Monitor duplicate-source conflicts, failed/unbalanced/stale drafts, closed-period attempts, reversal anomalies, reconciliation differences, unauthorized mutation and report bounds. Recovery verifies per-entity/period/account/currency debit-credit totals, source/reversal links, mappings, outbox and audit.

## 7. Decisions and Evidence

APPR-P05-002 must settle legal entity, chart, base/multi-currency, precision/rounding, dimensions, approvals, period close/reopen, opening balances and FX scope before dependent schema/posting. Use P05 task prompts; test/evidence requirements are in P05-TRACE-001.

## 8. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved.

| Gate | Disposition for `accounting` |
|---|---|
| RDY-001 attributes | Section 3 names the owned records and ownership boundaries. Every monetary field uses `NUMERIC` and `Decimal` with precision, scale and the named rounding stages approved before migration per ADR-013; every tenant-owned row carries a mandatory indexed tenant reference and UUID primary key; account, journal, line, period and currency relationships are same-tenant foreign keys, with a database-level constraint that each journal entry balances to zero in the base currency and that no line references a closed period |
| RDY-002 states | Section 4 owns workflows and invariants. Journal entries move from draft to posted, and a posted entry is immutable per ADR-011; correction is a linked reversal or adjusting entry, never an edit or deletion. Period states of open, closing and closed are authoritative for every module that posts |
| RDY-003 testable rules | Satisfied by the business rules in section 5, each with a named verification method |
| RDY-004 permissions | `accounting.view_account`, `accounting.configure_chart_of_accounts`, `accounting.view_journal`, `accounting.add_journal`, `accounting.post_journal`, `accounting.reverse_journal`, `accounting.view_ledger`, `accounting.configure_period`, `accounting.close_period`, `accounting.reopen_period`, `accounting.configure_currency`, `accounting.view_financial_statement`, `accounting.export_accounting_data`, `accounting.view_all_accounting`. Preparing and posting a journal are separate, and closing or reopening a period is separate from both, with maker-checker on posting, reversal and period close |
| RDY-005 interface surfaces | Chart of accounts management, journal entry with a balanced-line editor and running totals, posting confirmation, ledger enquiry with drill-down, period close workspace with blocking items, and financial statement views, mapped to the line-item editor, monetary cell, data table and destructive confirmation dialog components in `../01-architecture/UI_DESIGN_SYSTEM.md`. Posting, reversal and period close are confirmed per `UIX-036` and name the effect |
| RDY-006 reports and imports | Owns `RPT-101` trial balance, `RPT-102` general ledger detail, `RPT-103` journal register, `RPT-104` profit and loss, `RPT-105` balance sheet, `RPT-106` cash flow summary subject to `DEC-REP-003`, `RPT-107` account reconciliation status and `RPT-108` period close status in `../00-product/REPORT_CATALOGUE.md`, and is the source of truth to which every other financial report reconciles per `REPM-004`. Chart of accounts import follows `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` domain 1 and opening balances domain 6, where the trial balance must balance exactly before commit per `MIG-052` and a difference is never written to a suspense account automatically per `MIG-054` |
| RDY-007 document numbering | Registered in `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md`: journal entry, recurring journal, payment voucher, receipt voucher, contra entry, period-close record and revaluation entry, each allocated at posting and scoped to tenant, entity and fiscal period. These are the document types most likely to carry a statutory sequential expectation, so the conservative gapless default in `SEQ-022` applies until `DEC-SEQ-002` records a dated confirmation |
| RDY-008 notifications | Registered in `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md`: journal awaiting approval, journal posted, journal reversed, period close blocked, period closed, period reopened and control-account reconciliation variance detected. All are financial category, mandatory and never digested |
| RDY-009 classification and retention | Ledger and journal data is `C2`; a narrative or counterparty reference may contain `C3`. Retention class is `RET-01`, and `RET-02` where a record supports a tax filing, under `../05-quality/DATA_PROTECTION_AND_RETENTION.md`. `PRIV-043` prohibits unattended automated disposal of these classes, and `PRIV-034` prohibits deleting a posted record to satisfy an erasure request. Periods remain unresolved pending `DEC-PRIV-005` and `ISSUE-008`; none is asserted here |
| RDY-010 threats | `THR-010`, `THR-011`, `THR-034` race producing double posting, `THR-021` self-approval, `THR-030` injection through a raw query, `ABU-01` modifying or deleting a posted record to conceal activity, `ABU-05` self-approval across separation of duties, `ABU-06` back-dating into a closed period to alter a filed position, `ABU-07` bulk extraction, `ABU-10` suppressing audit |
| RDY-011 decision dependencies | `DEC-FIN-001`–`DEC-FIN-005` remain open for precision, rounding, posting, reversal and valuation policy, and the chart of accounts structure requires approval before schema work. Calculation and posting fail closed without an approved effective policy, per the existing P05 fail-closed posture |
| RDY-012 regulatory assertions | None. This module asserts no accounting standard, corporate tax treatment or statutory statement format; a profit-and-loss report is never presented as a corporate tax return, consistent with `../01-architecture/DATABASE_DESIGN.md` section 2.3 |

## 9. Migration, Compatibility and Recovery

The ledger is the financial system of record, so no migration may alter a posted entry, and a precision or rounding change requires before-and-after trial balances, a recorded reconciliation and recovery evidence. Rewriting shared migration history affecting posted data is prohibited without an approved plan under `AGENTS.md` section 13.

Restore verification confirms that the trial balance balances to zero in the base currency, that account and journal counts match, that every subsidiary ledger reconciles to its control account, that period states and close evidence are intact, that document-number high-water marks are consistent, and that audit continuity is unbroken.
