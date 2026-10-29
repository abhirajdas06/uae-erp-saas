# P06 — Procurement and Inventory Phase Specification

| Property | Value |
|---|---|
| Document ID | P06-SPEC-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Implementation authorization | NOT GRANTED |

## 1. Objective and Authority

Deliver tenant-safe supplier purchasing and controlled stock operations integrated through explicit P03 Sales and P05 Accounting/VAT contracts. Implements `INVN-001`–`INVN-005`, Roadmap Phase 6, ADR-003–006, ADR-010–011, ADR-013–015 and ADR-018–020.

## 2. Entry Gates

- P01 tenancy/IAM/audit, P02 entitlements, P03 item/customer/sales contracts and P05 posting/VAT contracts required by enabled workflows are approved and verified.
- Product/item master ownership, purchasing scope, units, negative-stock, reservation, costing/valuation and accounting policies are approved or affected behavior is disabled.
- Product Owner approves bounded P06 scope (`APPR-P06-001`).

## 3. Included Scope

- Tenant-scoped suppliers and contacts with duplicate/review lifecycle.
- Purchase requisitions when enabled; purchase orders/lines, revisions, approvals, cancellation and close.
- Goods receipt, return/correction and three-way evidence foundation without conflating PO, receipt, supplier bill or payment.
- Inventory item mapping, units/conversions, warehouses/locations, controlled receipt/issue/transfer/adjustment/count and optional reservation.
- Movement-derived/reconciled balances, concurrency/idempotency, lot/serial/expiry only if explicitly approved.
- Approved valuation layers/costing and versioned Accounting/VAT posting requests.
- UI, reports, imports/exports, audit, isolation, migrations, recovery and operations.

## 4. Excluded Scope

- Supplier payment/banking, customs/import compliance, logistics/shipping, manufacturing/MRP, advanced quality, demand planning, vendor portals or EDI unless separately approved.
- Unapproved lot/serial/expiry/landed-cost/consignment/drop-ship/multi-UOM/negative-stock/valuation behavior.
- Direct ledger/tax writes or direct stock updates from Procurement, Sales, Invoicing or admin/import paths.

## 5. Ownership and Contracts

`procurement` owns suppliers, requisitions, purchase orders, purchase receipts references and supplier-bill capture/reconciliation workflow. `inventory` owns inventory items/mappings, UOM, warehouses/locations, movements, balances/projections, reservations, counts, adjustments and valuation layers. P03 Sales item ownership is mapped/versioned; it is not silently duplicated. Accounting owns journal entries; VAT owns tax policy; Procurement does not prove supplier payment.

## 6. Core Controls

- Purchase approval uses immutable revision snapshots, amount/entity thresholds and stale-approval rejection.
- A PO authorizes intent; only an accepted inventory receipt changes stock. Supplier bill is separate evidence.
- Every quantity change is an atomic movement. Transfers create balanced source/destination effects in one operation; loss/difference is explicit.
- Quantity/UOM conversions, precision and residual rules are versioned. Client balances/totals are never authoritative.
- Duplicate source/purpose/idempotency keys and concurrency locking prevent repeated receipts/issues/reservations/postings.
- Negative stock, backdating, over-receipt/return, adjustment and count variance follow approved policy and permissions.
- Valuation method/currency/cost precision/cutoff/correction are approved before valuation layers or postings. Historical movements never revalue from current master data without an explicit revaluation workflow.

## 7. Security, Migration and Operations

Supplier bank/tax/contact data, costs/margins and stock adjustments are sensitive. Separate create/approve/receive/adjust/count/value/export permissions and enforce entitlement plus tenant/entity/warehouse/object scope across UI/API/service/task/admin/report/cache/files. Use approved RLS and audit.

Migrations preserve UUID/tenant keys, UOM/precision, movement/source/correction/valuation links and old/new overlap. Backup/restore reconciles per tenant/entity/item/location/UOM quantity and value, reservations, document links, sequences, outbox and audit. Monitor negative/over-receipt attempts, stale approvals, duplicate/conflicting operations, balance/movement/valuation/ledger mismatches and long locks.

## 8. Acceptance Criteria

| ID | Criterion |
|---|---|
| P06-AC-001 | Approved item/supplier/UOM/purchasing/inventory/valuation policies and disabled scope are recorded |
| P06-AC-002 | Suppliers are tenant-scoped, permissioned, auditable and safely deactivated/merged |
| P06-AC-003 | Purchase documents use valid revisioned states, approvals and immutable accepted snapshots |
| P06-AC-004 | PO, receipt, supplier bill, payment and accounting consequences remain distinct and traceable |
| P06-AC-005 | Receipts/returns are idempotent, quantity-bounded and linked to approved source/version |
| P06-AC-006 | Warehouses/locations/items/UOMs are scoped, valid and historically stable |
| P06-AC-007 | Every stock change is an authorized atomic movement; no direct balance mutation exists |
| P06-AC-008 | Transfers preserve total quantity except explicit approved variance/loss |
| P06-AC-009 | Concurrency/retry cannot corrupt balances, over-issue or duplicate movement |
| P06-AC-010 | Negative stock, reservation, adjustment, count and backdate follow approved policy |
| P06-AC-011 | Movement-derived balances/projections reconcile by item/location/UOM/cutoff |
| P06-AC-012 | Approved valuation is exact, historically reproducible and reconciles to stock/cost sources |
| P06-AC-013 | Accounting/VAT requests are versioned/idempotent and reconcile without direct downstream writes |
| P06-AC-014 | Permission, entitlement, tenant/entity/warehouse isolation and RLS tests pass |
| P06-AC-015 | Sensitive supplier/cost/export/file/audit controls pass |
| P06-AC-016 | UI/API/reports/imports/exports are accurate, bounded and accessible |
| P06-AC-017 | Migration/backup/restore/replay and inventory/financial reconciliation pass |
| P06-AC-018 | Performance/locking/monitoring/runbooks and full quality gates pass |
| P06-AC-019 | Finance/Operations/Security/Database and independent QA reviews are dispositioned |
| P06-AC-020 | Product Owner approves phase exit and separately any production inventory scope |

## 9. Task/Evidence Plan

P06-T01 policy/ownership (`P06-EV-001–002`); P06-T02 suppliers/procurement (`P06-EV-003–004`); P06-T03 item/UOM/location (`P06-EV-005`); P06-T04 movements/receipts/transfers (`P06-EV-006`); P06-T05 reservations/adjustments/counts (`P06-EV-007`); P06-T06 valuation/accounting/VAT (`P06-EV-008–009`); P06-T07 surfaces/security (`P06-EV-010–011`); P06-T08 migration/recovery/operations (`P06-EV-012–013`); P06-T09 independent exit (`P06-EV-014`).

## 10. Pending Approvals

| ID | Decision / approver | Recommendation and recording method | Blocks |
|---|---|---|---|
| APPR-P06-001 | Bounded scope — Product Owner | “I approve P06-SPEC-001 as the bounded P06 implementation scope, subject to its named gates.” | P06 implementation |
| APPR-P06-002 | Item/supplier/purchasing ownership — Product/Architecture/Operations | Approve Inventory as stock-item owner with explicit P03 sales-item mapping; define requisition/PO/receipt/bill/return scope in a versioned policy | Schema/workflows |
| APPR-P06-003 | UOM/negative stock/reservation/adjustment/count policy — Product/Operations/Finance | Approve precise enabled behavior and disable advanced options otherwise | Movement schema/activation |
| APPR-P06-004 | Costing/valuation/accounting/VAT — Finance/Tax/Architecture | Approve method, precision, cutoff, corrections, accounts and contracts in versioned policy | Valuation/postings |
| APPR-P06-005 | Exit/production — Product Owner after independent reviews | Record exact enabled warehouses/items/features/evidence/limitations/rollback separately from phase exit | Exit/production |
