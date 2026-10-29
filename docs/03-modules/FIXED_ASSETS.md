# FIXED_ASSETS — Fixed Asset Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-FIXED-ASSETS-001 |
| Status | APPROVED SPECIFICATION — ASSET/DEPRECIATION POLICY REQUIRED |
| Owning phase / app | P08 / `fixed_assets` |

## 1. Purpose and Boundary

Own the asset register, category/book-policy assignment, acquisition/in-service snapshots, locations/custodians, depreciation schedules/runs, transfers, corrections and disposals under `FA-001`–`FA-002` and P08-SPEC-001. Procurement owns purchase/receipt evidence; Accounting owns journal entries and financial statements.

Revaluation, impairment, component, lease, construction-in-progress, tax-book and complex multi-book accounting are disabled until separately specified and approved.

## 2. Actors and Permissions

Asset registrar, custodian, asset accountant/preparer, depreciation reviewer/approver, disposal approver, reconciler, auditor and purpose-bound support. Policy configuration, acquisition, in-service activation, run preparation, approval/finalization, correction, disposal and posting are separated.

## 3. Model and Lifecycle

`AssetCategory`, `AssetBookPolicy`, `FixedAsset`, `AssetLocationHistory`, `AssetCustodyHistory`, `DepreciationSchedule`, `DepreciationRun`, `DepreciationLine`, `AssetPostingOperation`, `AssetTransfer`, `AssetDisposal` and `AssetReconciliationFinding`.

Candidate → registered → in service → suspended/held → disposed/retired. Cost, residual value, useful life, method, convention, start/stop date, frequency, currency and precision are versioned snapshots.

## 4. Rules and Verification

| ID | Rule / verification |
|---|---|
| FAM-001 | Asset identity/source/entity/category/acquisition and in-service facts are complete and duplicate-controlled |
| FAM-002 | Only approved effective book policy calculates; missing/ambiguous policy fails closed |
| FAM-003 | Decimal depreciation is deterministic and never reduces book value below approved residual value |
| FAM-004 | Draft recalculation is controlled; finalized run/line is immutable and stale-safe |
| FAM-005 | Concurrent/repeated run or posting cannot duplicate period/asset effects |
| FAM-006 | Transfer/custody/location history preserves dates and authorization without rewriting finance snapshots |
| FAM-007 | Disposal/correction/reversal is linked and reconciles cost, accumulated depreciation, proceeds and net book value |
| FAM-008 | Accounting requests are versioned, balanced, idempotent and source-reconciled |
| FAM-009 | Permissions, entitlement, tenant isolation, RLS and exports protect all asset paths |
| FAM-010 | Migration/restore reconciles asset count, cost, depreciation, net book value, postings, files and audit |

## 5. Operations and Decisions

Monitor missing/expired policy, stale schedule, duplicate source, run failure, posting mismatch, negative/below-residual book value, unauthorized transfer/disposal and reconciliation variance. `DEC-FA-001` must approve capitalization threshold, methods, useful lives, residual values, conventions, corrections/disposals and excluded advanced treatments.
