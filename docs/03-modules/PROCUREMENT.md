# PROCUREMENT — Procurement Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-PROCUREMENT-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
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

## 8. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved.

| Gate | Disposition for `procurement` |
|---|---|
| RDY-001 attributes | Section 3 names the owned records and historical-integrity invariants. Every monetary field uses `NUMERIC` and `Decimal` with precision, scale and rounding approved before migration per ADR-013; every tenant-owned row carries a mandatory indexed tenant reference and UUID primary key per ADR-014; supplier, item, order, receipt and invoice-reference relationships are same-tenant foreign keys with database-level uniqueness on document numbers in their approved scope |
| RDY-002 states | Section 4 owns the requisition, order, receipt and matching workflows. Approved and received records are immutable per ADR-011; correction is a linked amendment or reversal, never an edit |
| RDY-003 testable rules | Satisfied by the business rules in section 5, each with a named verification method |
| RDY-004 permissions | `procurement.view_requisition`, `procurement.add_requisition`, `procurement.submit_requisition`, `procurement.approve_requisition`, `procurement.view_order`, `procurement.add_order`, `procurement.approve_order`, `procurement.send_order`, `procurement.cancel_order`, `procurement.record_receipt`, `procurement.match_invoice`, `procurement.resolve_match_exception`, `procurement.configure_supplier`, `procurement.export_procurement_data`, `procurement.view_all_procurement`. Requisition approval, order approval, receipt recording and invoice matching are separate, with maker-checker on approvals |
| RDY-005 interface surfaces | Requisition and order entry with a line-item editor, approval queues, receipt recording, three-way match exception review and supplier management, mapped to the line-item editor, data table, status badge and confirmation dialog components in `../01-architecture/UI_DESIGN_SYSTEM.md`, with destructive and approval actions confirmed per `UIX-036` |
| RDY-006 reports and imports | Owns `RPT-401` purchases by period and supplier, `RPT-402` purchase order status, `RPT-403` payables ageing, `RPT-404` supplier statement and `RPT-405` goods receipt and three-way match exceptions in `../00-product/REPORT_CATALOGUE.md`. Supplier and item master import follows `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` domains 2 and 3, and open purchase orders enter through domain 7; import may never create a received or matched state |
| RDY-007 document numbering | Registered in `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md`: purchase requisition, purchase order, goods receipt and supplier invoice reference, each with its allocation point at approval or confirmation and scoped to tenant, entity and period. Gapless requirements follow `DEC-SEQ-002`, with conservative defaults until confirmed |
| RDY-008 notifications | Registered in `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md`: requisition awaiting approval, requisition approved or rejected, order approved, order sent, receipt recorded, match exception raised and order overdue. Approval-workflow messages are digest-eligible; a match exception is not digested. Outbound delivery of a purchase order to a supplier is an authorized external disclosure gated by `DEC-NTF-005` |
| RDY-009 classification and retention | Order, receipt and pricing data is `C2`; supplier contact data is `C3`; supplier bank detail, where held, is `C4` and subject to the maker-checker change control that `ABU-03` requires. Retention classes are `RET-01` for records forming part of the accounting record, `RET-07` for bank detail and `RET-08` for supplier contacts; periods remain unresolved pending `DEC-PRIV-005` and none is asserted here |
| RDY-010 threats | `THR-010`, `THR-011`, `THR-034` race producing duplicate receipt or match effects, `THR-021` self-approval, `ABU-03` payment diversion through altered supplier bank details, `ABU-05` self-approval across separation of duties, `ABU-07` bulk extraction of supplier and pricing data, `ABU-10` suppressing an exception |
| RDY-011 decision dependencies | `DEC-P06-001` remains open for ownership, approval thresholds and matching tolerance. Matching tolerance defaults to zero and approval thresholds fail closed until approved |
| RDY-012 regulatory assertions | None. Input VAT treatment on purchases is owned by `UAE_VAT.md` and is not asserted here |

## 9. Migration, Compatibility and Recovery

Supplier and item master changes must never rewrite the snapshot held on an approved order or recorded receipt, because those snapshots evidence what was agreed and received. A precision change to a monetary field requires before-and-after totals and recovery evidence.

Restore verification confirms order and receipt counts, per-currency committed and received totals, document-number high-water marks, three-way match state, payables control-account reconciliation with Accounting, outbox age and audit completeness.
