# INVENTORY — Inventory Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-INVENTORY-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Owning phase / app | P06 / `inventory` |

## 1. Purpose and Boundaries

Own stock items/mappings, units, warehouses/locations, movements, balances/projections, reservations if enabled, counts/adjustments and approved valuation (`INVN-003`–`INVN-005`). Procurement/Sales initiate business intent; Inventory alone changes stock. Accounting owns financial postings.

Excluded unless separately approved: manufacturing, advanced planning, lots/serials/expiry, landed cost, consignment, kits, drop shipment, multi-UOM conversion complexity and automated replenishment.

## 2. Actors and Permissions

Item master manager, warehouse manager, receiver, issuer/picker, transfer operator, counter, adjustment approver, valuation reviewer, reporter and auditor. Item/location/UOM configuration, movement creation/approval, reservation, count, adjustment, backdate, negative-stock exception, valuation and export are distinct permissions scoped by tenant/entity/warehouse.

## 3. Model and Invariants

Conceptual records: `InventoryItem`, `SalesItemMapping`, `UnitOfMeasure`, `UOMConversion`, `Warehouse`, `StockLocation`, `StockMovement`, `StockMovementLine`, `StockBalanceProjection`, `StockReservation`, `StockCount`, `StockAdjustment`, `ValuationLayer` and `InventoryReconciliationFinding`.

- UUID, tenant/entity and approved warehouse/location ownership; item/UOM/location relationships are same-scope.
- Quantities and costs use typed Decimal precision. Conversions have explicit direction/version/effective dates.
- Movement is append-oriented and identifies source type/ID/version/purpose, reason, date, item/UOM, locations and actor/system.
- Balance is derived from or continuously reconciled to movements. Projection/cache is not independent truth.
- Transfer debits source and credits destination atomically. Correction uses linked reversal/adjustment, not movement edit/delete.
- One source/version/purpose/idempotency key produces one effect.

## 4. Movement and Valuation Workflows

Receipt, issue, transfer, return, reservation consume/release, count variance and adjustment each use an owning service with permission, entitlement, scope, UOM, availability/negative policy, source, date/period, idempotency, locking, audit and outbox validation. Failure commits no partial effect.

Reservation is not movement or ownership; it affects availability only under approved priority/expiry/overcommit rules. Counts freeze or define a cutoff/scope, compare physical and system quantity, require variance approval and create explicit adjustment movements.

Valuation requires approved method, cost source, currency/rate, precision/rounding, cutoff, negative-stock treatment, returns/corrections and accounting mapping. Layers/snapshots preserve historical method/input; no silent current-cost rewrite.

## 5. Business Rules

| ID | Rule / verification |
|---|---|
| INVMOD-001 | Item/UOM/location identity and mapping are explicit, scoped and historically stable; model tests |
| INVMOD-002 | No stock quantity changes outside movement service/database protections; mutation tests |
| INVMOD-003 | Movement/transfer is atomic, balanced where applicable and idempotent; transaction tests |
| INVMOD-004 | Concurrent receipt/issue/reserve/transfer cannot over-issue or corrupt balances; concurrency tests |
| INVMOD-005 | Negative stock/backdate/tolerance follow approved policy and audit; policy tests |
| INVMOD-006 | Reversal/adjustment/count preserves original and reason/approval; workflow tests |
| INVMOD-007 | Balance/availability reconcile to movements/reservations at cutoff; reconciliation tests |
| INVMOD-008 | Valuation follows approved immutable method/layers and reconciles quantity/value/accounting; financial tests |
| INVMOD-009 | Source integrations cannot directly mutate stock or duplicate effects; contract tests |
| INVMOD-010 | Entitlement/permission/tenant/entity/warehouse/RLS protect all paths; isolation tests |
| INVMOD-011 | Reports/imports/exports are bounded, authorized and UOM/currency/cutoff explicit; surface tests |
| INVMOD-012 | Migration/restore preserves movement, balance, reservation, valuation, source and audit integrity; recovery tests |

## 6. Operations and Decisions

Monitor negative/overcommit attempts, movement/projection difference, reservation age, count variance, valuation/accounting mismatch, lock contention, duplicate/conflict and unauthorized adjustment. Recovery recalculates/reconciles per item/location/UOM quantities and per method/currency value from authoritative records.

APPR-P06-002–004 settle item mapping, UOM/movement policies and valuation. Use P06 task prompts and P06-TRACE-001.

## 7. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved.

| Gate | Disposition for `inventory` |
|---|---|
| RDY-001 attributes | Section 3 names the owned records and invariants. Quantities and valuations use `NUMERIC` and `Decimal` with precision, scale and rounding approved before migration per ADR-013; every tenant-owned row carries a mandatory indexed tenant reference and UUID primary key; item, location, movement and valuation-layer relationships are same-tenant foreign keys, with check constraints preventing a negative on-hand quantity where the approved policy forbids it |
| RDY-002 states | Section 4 owns movement and valuation workflows. A posted movement is immutable per ADR-011; correction is a linked reversing movement, never an edit, so the valuation history remains reconstructable |
| RDY-003 testable rules | Satisfied by the business rules in section 5, each with a named verification method |
| RDY-004 permissions | `inventory.view_item`, `inventory.configure_item`, `inventory.view_stock`, `inventory.record_receipt`, `inventory.record_issue`, `inventory.record_transfer`, `inventory.record_adjustment`, `inventory.approve_adjustment`, `inventory.perform_count`, `inventory.approve_count_variance`, `inventory.configure_valuation_policy`, `inventory.export_inventory_data`, `inventory.view_all_inventory`. Recording a movement, approving an adjustment and approving a count variance are separate, with maker-checker on adjustments and variances because both change asset value |
| RDY-005 interface surfaces | Item master, stock-on-hand views by item and location, movement history, transfer and adjustment entry, stock count worksheets and variance review, mapped to the data table, quantity cell, form and destructive confirmation dialog components in `../01-architecture/UI_DESIGN_SYSTEM.md`; adjustments and variance approvals are confirmed per `UIX-036` |
| RDY-006 reports and imports | Owns `RPT-406` stock on hand and valuation, `RPT-407` stock movement history, `RPT-408` stock ageing and slow-moving items and `RPT-409` reorder and shortage exceptions in `../00-product/REPORT_CATALOGUE.md`. Item and location master import follows `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` domain 3, and opening quantities and valuation enter through domain 6, where they must reconcile to the inventory control account before commit and are all-or-nothing per `MIG-053` |
| RDY-007 document numbering | Registered in `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md`: stock movement, stock adjustment, stock transfer and stock count, each allocated at confirmation and scoped to tenant, entity and period. Gapless requirements follow `DEC-SEQ-002` |
| RDY-008 notifications | Registered in `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md`: adjustment awaiting approval, count variance detected, negative stock prevented, reorder threshold breached and transfer received. Reorder and operational messages are digest-eligible; a count variance and a prevented negative stock are not digested because both indicate a control failure |
| RDY-009 classification and retention | Item, quantity and valuation data is `C2` and contains no personal data; supplier and cost information may be commercially sensitive. Retention class is `RET-01` where movements form part of the accounting record, under `../05-quality/DATA_PROTECTION_AND_RETENTION.md`; periods remain unresolved pending `DEC-PRIV-005` and none is asserted here |
| RDY-010 threats | `THR-010`, `THR-011`, `THR-034` race producing duplicate or lost movements and incorrect valuation, `THR-021` self-approved adjustment, `ABU-01` altering a posted movement, `ABU-06` back-dating into a closed period, `ABU-07` bulk extraction of cost and pricing data |
| RDY-011 decision dependencies | `DEC-P06-001` remains open for valuation method, negative-stock policy, costing granularity and count variance authority. Valuation fails closed without an approved effective policy, and negative stock is prevented by default until an exception is approved |
| RDY-012 regulatory assertions | None. VAT consequences of stock movements are owned by `UAE_VAT.md`, and capital-asset treatment by `FIXED_ASSETS.md` |

## 8. Migration, Compatibility and Recovery

Valuation is path-dependent, so a change to the valuation method or costing granularity cannot be applied retroactively without a recorded revaluation plan and before-and-after control-account reconciliation; silently recomputing history would falsify prior financial statements. A precision change requires before-and-after quantity and value totals plus recovery evidence.

Restore verification confirms item and movement counts, on-hand quantity by item and location, valuation layers and their total value against the inventory control account in Accounting, document-number high-water marks, open count worksheets, outbox age and audit completeness.
