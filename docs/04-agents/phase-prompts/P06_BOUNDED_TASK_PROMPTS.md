# P06 — Bounded Task Prompt Pack

| Property | Value |
|---|---|
| Document ID | P06-PROMPTS-001 |
| Status | APPROVED PROMPT BASELINE — IMPLEMENTATION NOT AUTHORIZED |

Every prompt requires an authorized manifest with exact policy versions, commit/files, migrations, tests, reviewers and evidence paths.

## P06-T01 — Policy, Ownership and Contracts

Resolve or disable supplier/item master, P03 mapping, purchasing documents, UOM, negative/reservation/count, valuation and Accounting/VAT contracts. Evidence EV-001–002; tests 001–010. No dependent schema before approval.

## P06-T02 — Supplier and Purchase Foundation

Implement supplier/contact, duplicate/lifecycle/sensitivity, requisition if enabled, PO/line/revision/calculation/approval/issue/cancel/close, audit, migrations and tests. Evidence EV-003–004; tests 011–035 plus security/migration cases.

## P06-T03 — Items, UOM, Warehouses and Locations

Implement approved inventory item/P03 mapping, UOM/conversion and location hierarchy/lifecycle with same-scope constraints and history. Evidence EV-005; tests 061–070.

## P06-T04 — Receipt, Issue, Transfer and Movement Integrity

Implement movement-only stock, procurement receipt/return, issue/transfer, atomicity, idempotency, locking, negative/backdate policy, balance projection/reconciliation and tests. Evidence EV-006; tests 036–048, 071–080.

## P06-T05 — Reservations, Counts and Adjustments

Implement only approved reservations/availability, physical count cutoff, variance approval, linked adjustment/reversal and reconciliation. Evidence EV-007; tests 081–088.

## P06-T06 — Valuation and Financial Integration

After APPR-P06-004, implement exact approved valuation layers/cost precision/corrections and versioned Accounting/VAT requests/reconciliation. Evidence EV-008–009; tests 089–112.

## P06-T07 — Surfaces and Security

Deliver accessible UI/API/reports, draft-only imports, safe exports/files, permission/entitlement/object/warehouse/RLS and sensitive supplier/cost/audit controls. Evidence EV-010–011; tests 113–143.

## P06-T08 — Migration, Recovery and Operations

Prove clean/upgrade/overlap, restricted roles, quantity/value/source reconciliation, backup/restore, performance/locking, monitoring/runbooks and full gates. Evidence EV-012–013; tests 144–166.

## P06-T09 — Independent Review and Exit

Reproduce evidence, disposition findings/exceptions and prepare separate phase-exit and production-scope decisions. Evidence EV-014; tests 167–170. Reviewer cannot approve own work.
