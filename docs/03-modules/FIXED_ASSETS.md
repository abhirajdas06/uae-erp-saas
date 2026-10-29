# FIXED_ASSETS — Fixed Asset Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-FIXED-ASSETS-001 |
| Status | APPROVED CONTRACT BASELINE; EXPANDED IMPLEMENTATION DETAIL PROPOSED — ASSET/DEPRECIATION POLICY REQUIRED |
| Owning phase / app | P08 / `fixed_assets` |
| Domain owner | Fixed Asset Accounting |
| Commercial module | Yes |
| Tenant-owned data | Yes |
| Readiness | Expanded under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`; sections 4–14 are PROPOSED and unapproved |

## 1. Purpose and Boundary

Own the asset register, category and book-policy assignment, acquisition and in-service snapshots, locations and custodians, depreciation schedules and runs, transfers, corrections and disposals under `FA-001`–`FA-002` and [P08-SPEC-001](../02-phases/P08_PROJECTS_EXPENSES_ASSETS/P08_PHASE_SPECIFICATION.md). Procurement owns purchase and receipt evidence; Accounting owns journal entries and financial statements.

Governing sources: `FA-001`–`FA-002`, P08-SPEC-001, ADR-003–ADR-006, ADR-010, ADR-011, ADR-013–ADR-015, ADR-018, `ARCH-SEQ-001`, `ARCH-NOTIFY-001`, `ARCH-MIGRATION-001`, `QUAL-PRIV-001`, `QUAL-THREAT-001`, `PROD-REPORTS-001`.

Revaluation, impairment, component accounting, leases, construction in progress, tax-book and complex multi-book accounting are disabled until separately specified and approved.

## 2. Actors and Authorization

| Actor | Permitted scope |
|---|---|
| Asset registrar | Register assets and maintain non-financial attributes |
| Custodian | View assigned assets and confirm custody |
| Asset accountant / preparer | Prepare depreciation runs and accounting requests |
| Depreciation reviewer / approver | Review and finalize runs |
| Disposal approver | Authorize disposals and retirements |
| Reconciler | Investigate and resolve reconciliation findings |
| Auditor | Read-only evidence review |
| Purpose-bound support | Time-bounded, audited privileged access under ADR-018 |

Concrete permission codenames, satisfying `RDY-004`:

`fixed_assets.view_asset`, `fixed_assets.add_asset`, `fixed_assets.change_asset`, `fixed_assets.activate_asset`, `fixed_assets.transfer_asset`, `fixed_assets.assign_custody`, `fixed_assets.configure_category`, `fixed_assets.configure_book_policy`, `fixed_assets.prepare_depreciation_run`, `fixed_assets.approve_depreciation_run`, `fixed_assets.finalize_depreciation_run`, `fixed_assets.correct_asset`, `fixed_assets.approve_disposal`, `fixed_assets.prepare_posting`, `fixed_assets.reconcile_asset`, `fixed_assets.export_asset_data`, `fixed_assets.view_all_assets`.

Policy configuration, acquisition, in-service activation, run preparation, approval and finalization, correction, disposal and posting are separated. A preparer cannot approve or finalize their own run.

## 3. Domain Ownership

| Record / capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Asset category and book policy | `fixed_assets` | Direct tenant | Policy service |
| Fixed asset and its financial snapshot | `fixed_assets` | Direct tenant and legal entity | Asset service |
| Location and custody history | `fixed_assets` | Asset tenant | Append-only history services |
| Depreciation schedule, run, line | `fixed_assets` | Asset tenant | Depreciation services |
| Transfer, disposal, correction | `fixed_assets` | Asset tenant | Authorized workflow services |
| Posting operation | `fixed_assets` | Asset tenant | Durable operation service |
| Purchase and receipt evidence | `procurement` | Same-tenant reference | Snapshot read only |
| Journal entry, period, ledger balance | `accounting` | Same-tenant reference | Accounting contract |
| Project or cost-centre reference | `projects` | Same-tenant reference | Reference contract |

## 4. Data Model Requirements

Conceptual entities: `AssetCategory`, `AssetBookPolicy`, `FixedAsset`, `AssetLocationHistory`, `AssetCustodyHistory`, `DepreciationSchedule`, `DepreciationRun`, `DepreciationLine`, `AssetPostingOperation`, `AssetTransfer`, `AssetDisposal`, `AssetReconciliationFinding`.

Field-level requirements satisfying `RDY-001`:

| Entity | Required attributes |
|---|---|
| `AssetCategory` | UUID id; tenant FK; code unique per tenant; name; default book-policy reference; default account references; active flag |
| `AssetBookPolicy` | Tenant FK; version; effective from and to dates; depreciation method; convention; frequency; useful-life basis; residual-value basis; currency and precision; immutable once referenced by a finalized run |
| `FixedAsset` | UUID id; tenant FK; legal-entity FK; asset tag per `ARCH-SEQ-001`; description; category FK; referenced book-policy version; acquisition source reference; acquisition date; in-service date; `NUMERIC` cost, residual value and accumulated depreciation; useful life; currency; `status`; optional project, location and custodian references; created and updated timestamps and actors |
| `AssetLocationHistory` | Asset FK; location; effective from and to dates; actor; append-only |
| `AssetCustodyHistory` | Asset FK; custodian reference in the same tenant; effective from and to dates; actor; append-only |
| `DepreciationSchedule` | Asset FK; referenced policy version; period; `NUMERIC` planned charge; opening and closing net book value; generated-at; supersession reference |
| `DepreciationRun` | Tenant FK; period; `status`; prepared-by, approved-by and finalized-by actors with timestamps; totals by account; stale-guard token |
| `DepreciationLine` | Run FK; asset FK; `NUMERIC` charge; opening and closing net book value; calculation inputs; immutable once the run is finalized; unique per run and asset |
| `AssetPostingOperation` | Run or disposal FK; idempotency key; payload version; status including an explicit uncertain state; attempt history; ledger reference where returned |
| `AssetTransfer` | Asset FK; from and to entity, location or cost centre; effective date; approver; reason |
| `AssetDisposal` | Asset FK; disposal date; method; `NUMERIC` proceeds; computed gain or loss; approver; reason; linked posting operation |
| `AssetReconciliationFinding` | Tenant FK; scope; detected-at; finding type; amounts; resolution state |

Constraints: UUID primary keys; mandatory tenant and legal-entity ownership; `NUMERIC`/`Decimal` for every monetary value with precision, scale and rounding approved before migration per ADR-013; check constraints preventing net book value below the approved residual value and preventing accumulated depreciation exceeding cost less residual value; unique asset tag in its approved scope; unique depreciation line per run and asset; same-tenant foreign keys throughout; no hard deletion of an asset, finalized run, line, disposal or posting operation through any ordinary path.

## 5. Workflows and States

| Record | States |
|---|---|
| `FixedAsset` | `CANDIDATE`, `REGISTERED`, `IN_SERVICE`, `SUSPENDED`, `HELD_FOR_DISPOSAL`, `DISPOSED`, `RETIRED` |
| `DepreciationRun` | `DRAFT`, `PENDING_APPROVAL`, `APPROVED`, `FINALIZING`, `FINALIZED`, `FAILED` |
| `AssetPostingOperation` | `PENDING`, `SENT`, `CONFIRMED`, `FAILED`, `UNCERTAIN` |
| `AssetDisposal` | `PROPOSED`, `APPROVED`, `POSTED`, `REVERSED` |

Permitted asset transitions: `CANDIDATE`→`REGISTERED`/`RETIRED`; `REGISTERED`→`IN_SERVICE`/`RETIRED`; `IN_SERVICE`→`SUSPENDED`/`HELD_FOR_DISPOSAL`; `SUSPENDED`→`IN_SERVICE`/`HELD_FOR_DISPOSAL`; `HELD_FOR_DISPOSAL`→`DISPOSED`/`IN_SERVICE`; `DISPOSED` and `RETIRED` are terminal except through an authorized linked reversal. Depreciation accrues only in `IN_SERVICE`, and a suspension rule is applied only where `DEC-FA-001` approves it.

A draft run may be recalculated. A finalized run and its lines are immutable per ADR-011; correction is by a linked adjustment or reversal, never by edit. Finalization, posting and disposal each execute within a database transaction and emit durable intent before any external effect, so a rollback cannot leave a partially finalized period. Concurrent or repeated finalization or posting for one period and asset produces exactly one effect.

## 6. Business Rules

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
| FAM-011 | Asset tag allocation is unique, concurrency-safe and rollback-safe per `ARCH-SEQ-001`; numbering tests |
| FAM-012 | A closed accounting period rejects a new depreciation or disposal posting; period tests |
| FAM-013 | Preparer and approver of a run are distinct actors; separation-of-duties tests |
| FAM-014 | Excluded treatments (revaluation, impairment, component, lease, construction in progress, tax book) are unreachable rather than partially implemented; negative tests |

## 7. Tenant Isolation, Security and Sensitive Data

Every request, service, task, report, export, cache and administrative path derives trusted tenant context and validates same-tenant relationships, with row-level security as defence in depth. Protect against insecure direct object reference to another tenant's asset, mass assignment of cost, accumulated depreciation, status or tenant, and formula injection in register exports.

Applicable threats from `QUAL-THREAT-001`, satisfying `RDY-010`: `THR-010`, `THR-011`, `THR-014`, `THR-034` race producing duplicate period charges, `THR-021` self-approval of a run or disposal, `ABU-01` altering a posted record, `ABU-06` back-dating into a closed period, `ABU-07` bulk extraction of the asset register.

Data classification and retention, satisfying `RDY-009`: asset register and depreciation data is `C2`; custodian identity is `C3`. Retention classes are `RET-01` for the register and depreciation history as part of the accounting record, and `RET-04` where an asset is a capital asset or real estate for which a longer period may apply. Both periods remain unresolved pending `DEC-PRIV-005`; none is asserted here.

## 8. Entitlements and Degraded Access

`FIXED_ASSETS` entitlement and the relevant user permission are both required on every path. Suspension or expiry denies new registration, run preparation, finalization, disposal and posting by default; approved read, export and legally required correction may be explicitly allowed and audited. Deactivation never deletes the register, finalized runs or posting evidence, and never prevents required retention or recovery.

## 9. Integrations and Events

- Procurement: read a validated same-tenant purchase and receipt snapshot for capitalization; a later procurement change must not rewrite the acquisition snapshot.
- Accounting: publish versioned, balanced depreciation and disposal facts; Accounting owns journal entries, periods and ledger references, and the control-account reconciliation required by `RPT-608`.
- Projects: validate a same-tenant project or cost-centre reference.
- HRMS and Users: read a validated same-tenant custodian snapshot.
- Reporting: expose register and schedule facts for `RPT-607` and `RPT-608`.

Durable intent and the transactional outbox per ADR-010 protect finalization and posting. Reconciliation detects register-to-ledger, schedule-to-run, run-to-posting and disposal-to-proceeds mismatches.

## 10. UI, API, Reports, Imports and Exports

Django and HTMX surfaces cover the asset register with filters, asset detail with financial and custody history, category and book-policy configuration, run preparation and review with totals, finalization confirmation, transfer, disposal approval, posting status and reconciliation review. Surfaces use the data table, monetary cell, form, status badge, destructive confirmation dialog and asynchronous operation status components in `ARCH-UI-001`. Finalization and disposal require explicit confirmation naming the asset or period and the effect per `UIX-036`.

Reports registered in `PROD-REPORTS-001`: `RPT-607` fixed asset register, `RPT-608` depreciation schedule reconciled to the ledger.

Imports follow `ARCH-MIGRATION-001` domains 5 and 6: asset register import with cost and accumulated depreciation as opening balances, which must reconcile to their control accounts before commit and are all-or-nothing. Import cannot create a finalized run and cannot bypass tag uniqueness. Exports are private, authorized, formula-safe, checksummed and audited.

Document types registered in `ARCH-SEQ-001`, satisfying `RDY-007`: asset tag, allocated at registration, tenant and entity scoped; and asset disposal record reference, allocated at approval. Gapless requirements follow `DEC-SEQ-002`; conservative gapless defaults apply until confirmed.

Notifications registered in `ARCH-NOTIFY-001`, satisfying `RDY-008`: run prepared and awaiting approval, run finalized, posting failed or uncertain, disposal approved, custody assigned, and reconciliation variance detected. Financial-category notifications are not digested.

## 11. Regulatory and Financial Readiness

This module establishes no capitalization threshold, depreciation method, useful life, residual-value rule, impairment policy or tax depreciation treatment. Those are configuration approved under `DEC-FA-001`, and the module fails closed without an approved effective policy. Corporate tax and VAT capital-asset consequences are owned by Accounting and `MOD-UAE-VAT-001`. No regulatory period or treatment is asserted here, per `RDY-012`; retention remains subject to `DEC-PRIV-005` and `ISSUE-008`.

## 12. Operations, Migration and Recovery

Monitor missing or expired policy, stale schedules, duplicate source references, run failures, posting mismatches, negative or below-residual book values, unauthorized transfer or disposal attempts, closed-period rejections and reconciliation variance. Runbooks cover a failed finalization transaction, an uncertain posting requiring manual confirmation, an incorrect finalized run requiring an authorized adjustment, a disposal reversal, and restore reconciliation.

Migration preserves asset identity, cost, accumulated depreciation, schedules, finalized runs, disposals and audit history; a precision change requires before-and-after totals and recovery evidence. Restore verifies asset counts, total cost, accumulated depreciation and net book value against the ledger control accounts, tag high-water marks, posting idempotency keys, outbox age and audit completeness.

## 13. Acceptance Criteria, Tests and Evidence

Acceptance criteria are `FAM-001`–`FAM-014` and the applicable criteria in `P08-AC-001`–`P08-AC-018`. Required tests are the asset scenarios within `P08-TST-001`–`P08-TST-171`. Evidence records are `P08-EV-010`–`P08-EV-014` in the [P08 matrix](../02-phases/P08_PROJECTS_EXPENSES_ASSETS/P08_TRACEABILITY_AND_TEST_MATRIX.md).

All scenarios are `NOT_RUN`. Depreciation arithmetic is tested against fixtures covering boundary values, full-life run-out, residual-value floors, mid-period acquisition and disposal, and the rounding-sensitive cases required by `QUAL-TESTDATA-001` TD-014.

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| DEC-FA-001 | Capitalization threshold, depreciation methods, useful lives, residual values, conventions, correction and disposal behavior, and the excluded advanced treatments | Finance domain owner / Product | Any schema or calculation work | Begin with straight-line, monthly convention and a single book; keep revaluation, impairment, component and tax books excluded |
| DEC-SEQ-002 | Whether the asset tag or disposal reference carries a statutory expectation | Tax specialist | Numbering implementation | Default to gapless and conservative until confirmed |
| DEC-PRIV-005 | Retention periods for the register, including any longer capital-asset or real-estate period, and resolution of `ISSUE-008` | Tax and finance specialists | Automated disposal | Confirm with dated authoritative sources; retain under obligation until then |
| DEC-GOV-007 | Phase-entry specification gate covering this expansion | Product Owner / Architecture | P08 implementation authorization | Approve the gate and this expanded specification together |

## 15. Implementation Prompt

Use the [P08 orchestration prompt](../04-agents/phase-prompts/P08_PROJECTS_EXPENSES_ASSETS.md) and the asset tasks in the [P08 bounded task prompts](../04-agents/phase-prompts/P08_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest; no implementation is authorized by this document.
