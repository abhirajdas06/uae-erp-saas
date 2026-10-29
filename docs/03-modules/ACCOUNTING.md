# ACCOUNTING — General Ledger and Financial Accounting Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-ACCOUNTING-001 |
| Status | READY FOR REVIEW |
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
