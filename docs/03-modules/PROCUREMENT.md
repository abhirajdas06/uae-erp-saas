# PROCUREMENT — Procurement Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-PROCUREMENT-001 |
| Status | READY FOR REVIEW |
| Owning phase / app | P06 / `procurement` |

## 1. Purpose and Boundaries

Own tenant supplier records and approved purchasing workflows under `INVN-001`–`INVN-002` and P06-SPEC-001. Included: suppliers/contacts, requisitions if enabled, purchase orders/lines/revisions/approvals, receipt requests/evidence, returns, supplier-bill capture/reference and PO-receipt-bill reconciliation.

Inventory owns stock movements; VAT owns tax policy; Accounting owns liabilities/expenses/inventory postings; Banking owns payment/settlement. A purchase order is not a receipt, supplier bill, payment or ledger entry. Customs, logistics, procurement marketplaces and supplier portals are excluded.

## 2. Actors and Permissions

Requester, buyer, purchasing approver, receiver, supplier-master manager, AP reviewer, procurement reporter and auditor. Supplier create/change, requisition, PO create/revise/approve/cancel, receipt request/confirm, return, bill match, export and sensitive supplier-field access are separate permissions with maker-checker thresholds.

## 3. Model and Historical Integrity

Conceptual records: `Supplier`, `SupplierContact`, `PurchaseRequisition`, `PurchaseOrder`, `PurchaseOrderRevision`, `PurchaseOrderLine`, `ReceiptReference`, `PurchaseReturn`, `SupplierBillReference`, `MatchFinding` and durable conversion/reconciliation operations.

- UUIDs plus tenant/legal entity; same-tenant supplier/item/location/source relationships.
- Supplier bank/tax/contact fields are classified; duplicate candidates and merges are controlled/audited.
- PO revisions snapshot supplier, delivery/billing data, item/service descriptions, UOM, quantity, price, currency, discount/tax inputs, terms and approvals.
- Accepted/approved revisions cannot be silently altered. Cancellation/close/return preserves history.
- Source/version/purpose idempotency prevents repeated PO conversion, receipt, return, bill or posting requests.

## 4. Workflows

Draft/requisition → review/approve → sourcing/PO draft → approval → issued → partially/fully received → partially/fully billed → closed/cancelled, with only approved transitions. Amount/entity/item/risk thresholds are policy driven; approval of a stale revision is rejected.

Goods receipt calls Inventory with approved PO revision/line, location, quantity/UOM, date and idempotency key. Inventory returns movement evidence; Procurement records it but never writes stock. Over/under receipt, tolerance, service receipt and returns require approved policy. Supplier bill capture is evidence/matching only until the owning payables contract is approved.

## 5. Business Rules

| ID | Rule / verification |
|---|---|
| PROCM-001 | Suppliers are scoped, duplicate-controlled, permissioned and auditable; model/security tests |
| PROCM-002 | PO revisions/states/approvals are valid and accepted snapshots immutable; workflow tests |
| PROCM-003 | Server calculates approved Decimal totals/currency/tax inputs; financial tests |
| PROCM-004 | PO/receipt/bill/payment/posting concepts never collapse; boundary tests |
| PROCM-005 | Receipt/return requests are quantity/UOM/source bounded and idempotent; contract/concurrency tests |
| PROCM-006 | Inventory/Accounting/VAT writes occur only through owning versioned contracts; architecture tests |
| PROCM-007 | Repeated/reordered events and failures reconcile without duplicate effect; resilience tests |
| PROCM-008 | Entitlement, permission, tenant/entity/object isolation and RLS cover all paths; IDOR/RLS tests |
| PROCM-009 | Supplier-sensitive data/log/export/file controls pass; privacy/security tests |
| PROCM-010 | Reports reconcile PO/receipt/return/bill status with explicit date/currency semantics; report tests |
| PROCM-011 | Migrations/restore preserve revision/source/movement/match/audit links; recovery tests |
| PROCM-012 | Missing purchasing/tolerance/tax/accounting policy fails closed; readiness tests |

## 6. Interfaces and Operations

Consumes mapped inventory/service item snapshots; issues versioned receipt/return and future accounting/VAT requests. UI/API/imports cannot bypass revisions/approvals or create completed/received state. Imports create validated drafts with preview/idempotency. Exports are bounded, formula-safe and audited.

Monitor stale approvals, duplicate suppliers, over-receipt, unmatched/duplicate bills, failed integrations, reconciliation backlog and bulk exports. Restore validates document/revision counts and amounts by currency, receipt/return movement links, match state, outbox and audit.

## 7. Decisions/Evidence

APPR-P06-002/003/004 govern ownership, workflow/tolerances and financial integrations. Use P06 prompts; tests/evidence are in P06-TRACE-001.
