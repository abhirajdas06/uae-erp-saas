# REPORTING — Reporting and Analytics Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-REPORTING-001 |
| Status | READY FOR REVIEW — REPORT CATALOGUE APPROVAL REQUIRED |
| Owning phase / app | P10 / `reporting` |

## 1. Purpose and Boundary

Own versioned report definitions, authorized execution/snapshots, generated artifacts, saved configurations when approved and operational delivery evidence under `REP-001`–`REP-003`. Source domains own business truth; Accounting owns ledger and financial-statement truth.

No unrestricted SQL/report builder, cross-tenant benchmark, warehouse or speculative KPI is included.

## 2. Actors and Permissions

Report viewer, domain report analyst, report configurator, scheduler/export requester, auditor and purpose-bound support. View, configure, schedule, export, access sensitive columns and privileged diagnostics are separate and object/field scoped.

## 3. Conceptual Model

`ReportDefinition`, `ReportVersion`, `ReportParameterSchema`, `SavedReport`, `ReportRun`, `ReportSnapshot`, `ReportArtifact`, `ReportDelivery` and `ReportReconciliationFinding`. Definitions pin sources, semantics, access policy, sensitivity and resource class. Artifacts are private and immutable for their version.

## 4. Rules and Verification

| ID | Rule / verification |
|---|---|
| REPM-001 | Definition/version/owner/source/semantics are complete and approved; catalogue tests |
| REPM-002 | Tenant/role/object/field/entitlement filters apply before aggregation and cache; isolation tests |
| REPM-003 | Timezone/as-of/date-range/currency/rounding/null/late-data semantics reproduce fixtures |
| REPM-004 | Financial totals reconcile to Accounting; other totals reconcile to named source contracts |
| REPM-005 | Query/row/time/memory/concurrency limits and cancellation protect shared capacity |
| REPM-006 | Saved/scheduled/background reports snapshot authorization and revalidate delivery access |
| REPM-007 | Exports are safe, private, checksummed, expiring and auditable; file/security tests |
| REPM-008 | Cache keys and invalidation include tenant, definition/version, parameters and authorization scope |
| REPM-009 | UI/API/accessibility/locale/RTL behavior is accurate for supported scope |
| REPM-010 | Migration/restore preserves definitions, evidence and artifacts per retention policy |

## 5. Operations and Decisions

Monitor latency, resource use, failed/cancelled runs, reconciliation drift, sensitive exports and artifact access. `DEC-REP-001` must approve the launch report catalogue, semantics, freshness, resource classes and retention.
