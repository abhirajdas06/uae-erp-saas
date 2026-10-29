# P03 — Bounded Task Prompt Pack

| Property | Value |
|---|---|
| Document ID | P03-PROMPTS-001 |
| Status | READY FOR REVIEW |
| Use with | `IMPLEMENTATION_TASK_PROMPT_TEMPLATE.md` and `P03_CRM_SALES_INVOICING.md` |

These task bodies are not implementation authorization. The orchestrator adds the explicit authorization, exact commit/file scope, current decisions, commands, reviewers, evidence locations, and prohibited paths before dispatch.

## P03-T01 — Decision and Contract Baseline

**Objective:** Resolve or explicitly disable schema/workflow-affecting P03 choices and publish reviewed domain/service contracts.

**Scope:** Customer/party ownership; sellable-item ownership; legal-entity/sequence scope; permissions/approval thresholds; currencies/precision/rounding; tax behavior; correction/payment policy; CRM-to-Sales, Sales-to-Invoicing, and future P04/P05/P06/P09 seams. Update decisions/risks.

**Acceptance/evidence:** P03-AC-003–004, 008–009, 018; P03-EV-001–002, 013. No business feature code. Unresolved behavior must be disabled with testable rejection.

## P03-T02 — CRM Customer, Account, and Contact Foundation

**Objective:** Implement tenant-safe authoritative customer/account/contact records and downstream snapshot service.

**Scope:** Models, normalization, lifecycle, relationships, duplicate candidates/review, search, permissions, audit, import/export boundaries, migrations, and tests. No quotation/invoice tables.

**Acceptance/evidence:** P03-AC-001, 003, 016–020; P03-TST-001–012, 102–152 as applicable; P03-EV-002–003, 009–012. No silent merge or global uniqueness assumption.

## P03-T03 — CRM Lead, Opportunity, and Activity Workflow

**Objective:** Implement configurable lead/opportunity stages, assignment, activities, and history.

**Scope:** Tenant configuration, state machine, ownership/scope, concurrency, notes/tasks, audit, events, UI, reports, and tests. Winning an opportunity cannot directly create invoices/accounting records.

**Acceptance/evidence:** P03-AC-002, 016–019; P03-TST-013–018, 102–141; P03-EV-004, 009–011.

## P03-T04 — Commercial Item and Quotation Foundation

**Objective:** Implement the approved non-stock commercial reference and quotation calculation/revision model.

**Scope:** Commercial item/service, optional future inventory mapping, quotation/lines, Decimal/currency/calculation policy, revision snapshots, sequence if approved, draft document, permissions, audit, migrations, and tests. No stock or invoice ownership.

**Acceptance/evidence:** P03-AC-004–005, 008, 016–020; P03-TST-019–032, 102–152; P03-EV-002, 005, 009–013.

## P03-T05 — Quotation Approval, Acceptance, and Sales Orders

**Objective:** Implement approved quotation transitions, acceptance evidence, sales orders, approvals, cancellation, and conversion operations.

**Scope:** Approval thresholds, separation of duties, stale revision defense, acceptance channel, order lifecycle, quote-to-order and invoice-request idempotency, outbox/reconciliation, UI, and tests. Fulfillment remains an interface/status unless separately specified.

**Acceptance/evidence:** P03-AC-005–006, 016–019; P03-TST-025–040, 102–141; P03-EV-005, 009–011.

## P03-T06 — Invoice Draft and Calculation

**Objective:** Implement tenant-issued invoice drafts and reproducible authoritative calculations.

**Scope:** Invoice/lines, source contract, customer/item snapshot, dates/terms, Decimal/currency/precision/discount/tax-policy inputs, server calculation, approval preparation, permissions, audit, migrations, and tests. No issuance until policies are approved.

**Acceptance/evidence:** P03-AC-007–008, 016–020; P03-TST-041–053, 102–152; P03-EV-002, 006, 009–013. Missing policy rejects; no hardcoded UAE rule or client totals.

## P03-T07 — Invoice Numbering, Issue, and Immutable Snapshot

**Objective:** Implement one atomic, concurrency-safe invoice issue path.

**Scope:** Sequence/reservation, approved scope and gap behavior, locking/idempotency, final recalculation, snapshot freeze, status, database/service protections, audit/outbox, failure recovery, admin/import restrictions, and tests.

**Acceptance/evidence:** P03-AC-009–011, 016–020; P03-TST-054–068, 102–152; P03-EV-006, 009–013. One complete issue or none; no number reuse or silent issued mutation.

## P03-T08 — Credit Notes and Corrections

**Objective:** Implement linked, bounded correction workflows without rewriting issued invoices.

**Scope:** Credit draft/lines, remaining-credit calculation, approval, sequence/issue, cancellation/replacement hooks, balance effect, audit/outbox/reconciliation, permissions, concurrency/idempotency, and tests. Only approved correction policy is enabled.

**Acceptance/evidence:** P03-AC-012, 014, 016–020; P03-TST-069–078, 102–152; P03-EV-007, 009–013.

## P03-T09 — Customer Payments, Allocations, and Balances

**Objective:** Implement customer-payment evidence, allocation/reversal, outstanding balance, and reconciliation foundation.

**Scope:** Payment record/state, duplicate reference/idempotency, same-tenant/customer/currency allocation, locking, partial/full behavior, reversal/unallocation, balance equation, statement query, audit/outbox/reconciliation, and tests. No bank-feed truth or payment gateway.

**Acceptance/evidence:** P03-AC-013–014, 016–020; P03-TST-079–091, 102–152; P03-EV-007, 009–013.

## P03-T10 — Documents, UI/API, Reports, Imports, and Exports

**Objective:** Deliver accessible server-rendered workflows and safe document/data boundaries.

**Scope:** Django/HTMX screens, forms, calculation/conflict UX, private rendering/storage/download, approved APIs, reports/statements, bounded draft/payment imports, exports, visual/accessibility/file security, retries, retention, and tests.

**Acceptance/evidence:** P03-AC-001–017, 019; P03-TST-001–123, 135–141 as applicable; P03-EV-003–009, 011. Rendering failure does not change financial state; direct paths repeat authorization.

## P03-T11 — Durable Integrations and Full Verification

**Objective:** Complete cross-domain reliability, migrations, security, performance, recovery, and operations evidence.

**Scope:** Transactional outbox/inbox as required, versioned contracts, duplicate/reordered/retry/replay tests, source/downstream reconciliation, full matrix, restricted-role/RLS tests, clean/upgrade/overlap migration, backup/restore, monitoring/runbooks, specialist reviews, and defect closure.

**Acceptance/evidence:** P03-AC-001–021; P03-TST-001–155; P03-EV-001–013. Do not mark unexecuted checks passed or enable unapproved regulated behavior.

## P03-T12 — Exit Evidence and Independent Review

**Objective:** Produce a reproducible, independent P03 completion report for human decision.

**Scope:** Map every criterion to current evidence; verify commands/artifacts/digests; disposition defects, exceptions, risks, limitations, disabled policies, and approvals; obtain independent QA/Security/Privacy/Database/Finance/UX/Operations reviews; prepare Product Owner decision and separate pilot decision.

**Acceptance/evidence:** P03-AC-022; P03-TST-156; P03-EV-014. The reviewer cannot approve their own work. P03 exit, P04 authorization, controlled pilot, and production release are separate human gates.
