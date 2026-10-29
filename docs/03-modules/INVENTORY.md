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
