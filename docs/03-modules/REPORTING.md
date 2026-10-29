# REPORTING — Reporting and Analytics Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-REPORTING-001 |
| Status | APPROVED CONTRACT BASELINE; EXPANDED IMPLEMENTATION DETAIL PROPOSED — REPORT CATALOGUE APPROVAL REQUIRED |
| Owning phase / app | P10 / `reporting` |
| Domain owner | Reporting and Analytics |
| Commercial module | Yes |
| Tenant-owned data | Yes |
| Readiness | Expanded under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`; sections 3–14 are PROPOSED and unapproved |

## 1. Purpose and Boundary

Own versioned report definitions, authorized execution and snapshots, generated artifacts, saved configurations where approved, and operational delivery evidence under `REP-001`–`REP-003` and [P10-SPEC-001](../02-phases/P10_REPORTING_INTEGRATIONS/P10_PHASE_SPECIFICATION.md). Source domains own business truth; Accounting owns ledger and financial-statement truth.

Governing sources: `REP-001`–`REP-003`, P10-SPEC-001, [PROD-REPORTS-001](../00-product/REPORT_CATALOGUE.md), ADR-003–ADR-006, ADR-011, ADR-013, ADR-018, ADR-019, `ARCH-UI-001`, `ARCH-L10N-001`, `ARCH-NOTIFY-001`, `QUAL-PRIV-001`, `QUAL-THREAT-001`.

No unrestricted SQL or free-form report builder, cross-tenant benchmark, data warehouse or speculative key performance indicator is included.

## 2. Actors and Authorization

| Actor | Permitted scope |
|---|---|
| Report viewer | Run and view permitted reports |
| Domain report analyst | Run domain reports including sensitive columns where authorized |
| Report configurator | Manage saved configurations and parameters within approved limits |
| Scheduler / export requester | Schedule and export where permitted |
| Auditor | Read-only execution and access evidence |
| Purpose-bound support | Time-bounded, audited privileged diagnostics under ADR-018 |

Concrete permission codenames, satisfying `RDY-004`:

`reporting.view_report`, `reporting.run_report`, `reporting.view_sensitive_column`, `reporting.configure_saved_report`, `reporting.schedule_report`, `reporting.export_report`, `reporting.view_report_snapshot`, `reporting.manage_definition`, `reporting.view_execution_evidence`, `reporting.view_all_reports`.

View, configure, schedule, export, access sensitive columns and privileged diagnostics are separate and object and field scoped. Entitlement is additionally required and never substitutes for permission.

## 3. Domain Ownership

| Record / capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Report definition and version | `reporting` | Platform-owned catalogue; tenant-scoped availability | Definition service under `DEC-REP-001` |
| Saved report and parameters | `reporting` | Direct tenant and owner | Saved-report service |
| Run, snapshot, artifact, delivery | `reporting` | Direct tenant | Execution and delivery services |
| Reconciliation finding | `reporting` | Direct tenant | Reconciliation service |
| Business facts in every source domain | Owning module | Same-tenant reference | Read-only contracts |
| Ledger and financial-statement truth | `accounting` | Same-tenant reference | Read-only contract |

Reporting never writes authoritative business state and never recomputes a financial total by an unapproved method.

## 4. Data Model Requirements

Conceptual entities: `ReportDefinition`, `ReportVersion`, `ReportParameterSchema`, `SavedReport`, `ReportRun`, `ReportSnapshot`, `ReportArtifact`, `ReportDelivery`, `ReportReconciliationFinding`.

Field-level requirements satisfying `RDY-001`:

| Entity | Required attributes |
|---|---|
| `ReportDefinition` | UUID id; catalogue identifier matching `PROD-REPORTS-001`; name key for localization; owning module; category; required permission; required entitlement; sensitivity; resource class; active flag |
| `ReportVersion` | Definition FK; version; effective dates; pinned source contracts; semantics including date basis, currency basis, rounding, null and late-data handling; access policy; reproducibility requirement; approval reference |
| `ReportParameterSchema` | Version FK; parameter name; type; required flag; default; validation rules; allowed-value source |
| `SavedReport` | Tenant FK; owner reference; definition and version reference; parameter values; sharing scope where approved; created and updated timestamps |
| `ReportRun` | Tenant FK; definition and version reference; requesting actor; authorization snapshot; parameter values; requested-at; started-at; completed-at; `status`; row count; resource usage; correlation identifier |
| `ReportSnapshot` | Run FK; as-of timestamp; stored result reference; checksum; retention class; immutable |
| `ReportArtifact` | Run FK; format; private storage reference; byte size; SHA-256 checksum; expiry; immutable for its version |
| `ReportDelivery` | Run FK; channel; recipient reference; authorization revalidation result; attempt history; terminal outcome |
| `ReportReconciliationFinding` | Tenant FK; definition reference; detected-at; variance amounts; resolution state |

Constraints: UUID primary keys; mandatory tenant ownership on every tenant-owned row; `NUMERIC`/`Decimal` for monetary results per ADR-013; immutability of snapshots and artifacts for their version; unique definition identifier and unique version per definition; same-tenant foreign keys for saved reports, runs, snapshots, artifacts and deliveries; expiry enforcement on artifacts; no hard deletion of an execution record required as access evidence.

Artifacts are private and immutable for their version. A definition pins its sources, semantics, access policy, sensitivity and resource class.

## 5. Workflows and States

| Record | States |
|---|---|
| `ReportRun` | `QUEUED`, `RUNNING`, `COMPLETED`, `TRUNCATED`, `CANCELLED`, `FAILED`, `DENIED` |
| `ReportArtifact` | `AVAILABLE`, `EXPIRED`, `DISPOSED` |
| `ReportDelivery` | `PENDING`, `DELIVERED`, `FAILED`, `SUPPRESSED` |

Execution sequence: resolve the definition and version, validate parameters against the schema, evaluate permission, entitlement, object and field scope, apply tenant and authorization filters before aggregation, enforce the resource class and row, time and memory limits, produce the result, snapshot it where reproducibility is required, generate artifacts on request, and record execution evidence.

A run that would exceed its resource class executes in the background and revalidates authorization at delivery. A scheduled run resolves recipients and authorization at dispatch time, never at schedule time. A `TRUNCATED` result is labelled as truncated and never presented as complete. Cancellation is supported and releases resources.

## 6. Business Rules

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
| REPM-011 | A report is never labelled as a statutory filing, submission or compliance evidence; disclosure tests |
| REPM-012 | An unentitled or unavailable source produces an explicit unavailability outcome, never a silently partial figure; fail-closed tests |
| REPM-013 | A reproducible-as-at report returns identical figures from its retained snapshot; reproducibility tests |
| REPM-014 | No report writes authoritative business state through any path; read-only tests |

## 7. Tenant Isolation, Security and Sensitive Data

Every request, service, task, report, export, cache, file and administrative path derives trusted tenant context and validates same-tenant relationships, with row-level security as defence in depth. Tenant, role, object and field filters are applied before aggregation and before any cache write, so a cached aggregate can never leak across tenants or authorization scopes.

Applicable threats from `QUAL-THREAT-001`, satisfying `RDY-010`: `THR-010`, `THR-011` missing tenant filter in an aggregate, `THR-012` cache key omitting tenant or authorization scope, `THR-013` scheduled run without tenant context, `THR-014` artifact served without authorization, `THR-005` expensive report abuse exhausting shared capacity, `THR-035` sensitive data in logs, `ABU-07` bulk extraction of the customer or employee base through a report or export.

Data classification and retention, satisfying `RDY-009`: a report inherits the classification of its most sensitive column, up to `C4` for payroll and banking reports. Retention classes are `RET-12` for artifacts and snapshots and `RET-10` for execution logs, with `RET-09` where execution evidence forms part of the audit trail, under `QUAL-PRIV-001`. Access to and export of `C3` or higher data is audited as a disclosure, and volume anomalies are alerted.

Exports are formula-safe to prevent spreadsheet formula injection. Logs and metrics record definition, version, parameters metadata and resource usage, never result content.

## 8. Entitlements and Degraded Access

`REPORTING` entitlement and the relevant user permission are both required on every path, and each report additionally requires the entitlement of the source module it reads. Suspension or expiry denies scheduling and new background execution by default; approved read and export for remediation and offboarding may be explicitly allowed and audited. Deactivation never deletes retained snapshots or execution evidence required for audit.

## 9. Integrations and Events

- Every source domain: read versioned facts through its published read-only contract; a report never queries another module's internal tables directly.
- Accounting: financial totals reconcile to the ledger per `REPM-004`.
- Notifications: report-ready and scheduled-delivery messages use the `ARCH-NOTIFY-001` catalogue and never embed `C3` or higher content.
- Integrations: outbound scheduled delivery to an external recipient is an authorized disclosure gated by `DEC-NTF-005` and is out of launch scope.

Reconciliation detects report-to-source variance, snapshot drift, artifact expiry failures and delivery authorization failures. Material delivery facts use the transactional outbox per ADR-010.

## 10. UI, API, Reports, Imports and Exports

Django and HTMX surfaces cover the report catalogue filtered by entitlement and permission, parameter entry with validation, result tables with pagination and sorting, resource and truncation notices, background run status, artifact download, saved report management, schedule management where approved, snapshot history and reconciliation findings. Surfaces use the data table, monetary cell, date cell, filter panel, pagination, empty state, skeleton loader and asynchronous operation status components in `ARCH-UI-001`.

Labels, headings, parameter names and artifact filenames are localizable and direction-correct per `ARCH-L10N-001`, while numeric exports remain machine-parseable with a declared decimal convention and encoding per `L10N-044`.

The catalogue this module serves is `PROD-REPORTS-001`, covering `RPT-101`–`RPT-805`. This module owns no business document numbering, so no entry is required in `ARCH-SEQ-001` beyond artifact references. Imports are out of scope; this module reads and never ingests business data.

Notifications registered in `ARCH-NOTIFY-001`, satisfying `RDY-008`: report completed, report failed, report truncated, scheduled delivery failed, artifact expiring, and reconciliation variance detected. All are operational and digest-eligible except reconciliation variance.

## 11. Regulatory and Financial Readiness

This module produces no statutory filing, return or submission, and no report output is evidence of compliance. The VAT preparation reports `RPT-301`–`RPT-305` are preparation aids whose line composition and labelling require `DEC-REP-002`; no return box reference may be applied until that decision records a dated source. No regulatory fact is asserted here, per `RDY-012`.

## 12. Operations, Migration and Recovery

Monitor execution latency, resource consumption, failed and cancelled runs, truncation frequency, reconciliation drift, sensitive exports, artifact access and expiry, cache hit behavior and delivery failures. Runbooks cover a runaway report consuming shared capacity, a reconciliation variance against Accounting, a failed scheduled delivery, an artifact expiry failure, a cache invalidation incident and restore reconciliation.

Migration preserves definitions, versions, snapshots, artifacts and execution evidence per retention policy. Restore verifies definition and version integrity, snapshot checksums, artifact availability and expiry state, and audit completeness.

## 13. Acceptance Criteria, Tests and Evidence

Acceptance criteria are `REPM-001`–`REPM-014` and the applicable criteria in `P10-AC-001`–`P10-AC-017`. Required tests are the reporting scenarios within `P10-TST-001`–`P10-TST-171`, including `P10-TST-001`–`P10-TST-015` for catalogue and semantics readiness. Evidence records are `P10-EV-001`–`P10-EV-008` in the [P10 matrix](../02-phases/P10_REPORTING_INTEGRATIONS/P10_TRACEABILITY_AND_TEST_MATRIX.md).

All scenarios are `NOT_RUN`. Reconciliation tests use the balanced synthetic financial baseline in `QUAL-TESTDATA-001` TD-030 and assert that each financial report agrees with its source of truth, and that a cross-tenant request returns no foreign data through any report, parameter, cache or artifact path.

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| DEC-REP-001 | Launch report catalogue, metric semantics, source and reconciliation, freshness, resource classes and retention | Product / Domain owners / Finance / Security / Operations | Any report implementation or activation | Approve `PROD-REPORTS-001` as the catalogue proposal; begin with named standard reports only |
| DEC-REP-002 | VAT preparation report line composition and labelling | Tax specialist | VAT reporting implementation | Label nothing as a return box reference until a dated source confirms it |
| DEC-REP-003 | Cash flow method for `RPT-106` | Finance domain owner | Cash flow reporting | Approve the method explicitly |
| DEC-REP-004 | Default role-to-report visibility matrix | Product Owner | Report authorization | Restrict payroll and banking reports to authorized roles by default |
| DEC-REP-005 | Which reports require snapshots for as-at reproducibility | Finance domain owner / Privacy reviewer | Snapshot and retention design | Require snapshots for financial and statutory-support reports |
| DEC-GOV-007 | Phase-entry specification gate covering this expansion | Product Owner / Architecture | P10 implementation authorization | Approve the gate and this expanded specification together |

## 15. Implementation Prompt

Use the [P10 orchestration prompt](../04-agents/phase-prompts/P10_REPORTING_INTEGRATIONS.md) and the reporting tasks in the [P10 bounded task prompts](../04-agents/phase-prompts/P10_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest; no implementation is authorized by this document.
