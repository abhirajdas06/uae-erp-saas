# PROJECTS — Project Operations Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-PROJECTS-001 |
| Status | APPROVED CONTRACT BASELINE; EXPANDED IMPLEMENTATION DETAIL PROPOSED — PROJECT POLICY REQUIRED |
| Owning phase / app | P08 / `projects` |
| Domain owner | Project Operations |
| Commercial module | Yes |
| Tenant-owned data | Yes |
| Readiness | Expanded under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`; sections 5–14 are PROPOSED and unapproved |

## 1. Purpose and Boundary

Own tenant project identity, lifecycle, membership, tasks, milestones, assignments and operational progress under `PROJ-001` and [P08-SPEC-001](../02-phases/P08_PROJECTS_EXPENSES_ASSETS/P08_PHASE_SPECIFICATION.md). CRM owns customers, HRMS owns employees, Expenses owns claims and Accounting owns ledger/cost accounting. Project references never confer customer, employee or financial authorization.

Governing sources: `PROJ-001`, P08-SPEC-001, ADR-003–ADR-006, ADR-011, ADR-013–ADR-015, ADR-018, `ARCH-UI-001`, `ARCH-SEQ-001`, `ARCH-NOTIFY-001`, `ARCH-MIGRATION-001`, `QUAL-PRIV-001`, `QUAL-THREAT-001`, `PROD-REPORTS-001`.

Initial scope excludes authoritative timesheets, billing, resource capacity, project accounting, revenue recognition and portfolio optimization.

## 2. Actors and Authorization

| Actor | Permitted scope |
|---|---|
| Project administrator | Configure project types, codes, statuses and tenant-wide settings |
| Project manager | Manage assigned projects, membership, tasks, milestones and transitions |
| Project member | View and update assigned tasks within object scope |
| Project viewer | Read-only access to permitted projects |
| Auditor | Read-only history and evidence review |
| Purpose-bound support | Time-bounded, audited privileged read under ADR-018 |

Concrete permission codenames, satisfying `RDY-004`:

`projects.view_project`, `projects.add_project`, `projects.change_project`, `projects.transition_project`, `projects.close_project`, `projects.reopen_project`, `projects.manage_member`, `projects.view_task`, `projects.add_task`, `projects.change_task`, `projects.assign_task`, `projects.manage_milestone`, `projects.configure_project_settings`, `projects.export_project_data`, `projects.view_all_projects`.

Create, configure, assign, transition, close/reopen, report/export and privileged support actions are separate and object-scoped. Entitlement is additionally required and never substitutes for permission.

## 3. Domain Ownership

| Record / capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Project, code, lifecycle state | `projects` | Direct tenant | Project service |
| Project membership | `projects` | Project tenant | Membership service |
| Milestone, task, assignment | `projects` | Project tenant | Task service |
| Status history | `projects` | Project tenant | Append-only transition service |
| Customer master | `crm` | Same-tenant reference | Snapshot read only |
| Employee master | `hrms` | Same-tenant reference | Snapshot read only |
| Expense claim referencing a project | `expenses` | Same-tenant reference | Expenses service |
| Project cost and revenue in the ledger | `accounting` | Same-tenant reference | Accounting contract |

Accounting, Expenses and Reporting consume versioned project facts through explicit contracts; they do not mutate project records.

## 4. Data Model Requirements

Conceptual entities: `Project`, `ProjectMember`, `Milestone`, `Task`, `TaskAssignment`, `ProjectStatusHistory` and the optional approved `ProjectReferenceSnapshot`.

Field-level requirements satisfying `RDY-001`:

| Entity | Required attributes |
|---|---|
| `Project` | UUID public id; tenant FK (mandatory, indexed); approved legal-entity FK where configured; normalized `code` unique within approved scope; name; optional description; `status`; optional customer reference; optional manager reference; planned and actual start and end dates; currency where amounts are displayed; created and updated timestamps; created-by and updated-by actor references |
| `ProjectMember` | Project FK; user or employee reference in the same tenant; role; effective from and to dates; unique active membership per project and member |
| `Milestone` | Project FK; name; target date; optional completion date; `status`; ordering key |
| `Task` | Project FK; optional parent task FK; normalized reference unique within the project; name; `status`; optional assignee; planned and actual dates; progress percentage bounded 0–100; depth-bounded hierarchy |
| `TaskAssignment` | Task FK; assignee reference in the same tenant; assigned-at timestamp; assigning actor; optional released-at timestamp |
| `ProjectStatusHistory` | Project FK; from-status; to-status; actor; timestamp; reason; append-only |

Constraints: UUID primary keys per ADR-014; mandatory tenant ownership on every tenant-owned row; `NUMERIC`/`Decimal` for any monetary or percentage value per ADR-013; database-level uniqueness for project code in its approved scope and task reference within a project; check constraints for date ordering and progress bounds; foreign keys restricted to the same tenant; no hard deletion of a project, task or status history that is referenced by expense, asset or accounting records.

Dates are calendar business dates and are not shifted by time-zone conversion, per `ARCH-L10N-001` L10N-031.

## 5. Workflows and States

| Record | States | Transition authority |
|---|---|---|
| `Project` | `DRAFT`, `ACTIVE`, `ON_HOLD`, `COMPLETED`, `CLOSED`, `CANCELLED` | `projects.transition_project`; close and reopen require `projects.close_project` and `projects.reopen_project` |
| `Milestone` | `PLANNED`, `IN_PROGRESS`, `ACHIEVED`, `MISSED`, `CANCELLED` | `projects.manage_milestone` |
| `Task` | `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`, `CANCELLED` | `projects.change_task`, or assignee within object scope |

Permitted project transitions: `DRAFT`→`ACTIVE`/`CANCELLED`; `ACTIVE`→`ON_HOLD`/`COMPLETED`/`CANCELLED`; `ON_HOLD`→`ACTIVE`/`CANCELLED`; `COMPLETED`→`CLOSED`/`ACTIVE` where reopen is approved; `CLOSED`→`ACTIVE` only by explicit authorized reopen with recorded reason; `CANCELLED` is terminal. Every other transition is rejected.

Close preconditions follow approved policy under `DEC-PROJ-001`: open task handling, pending expense claims referencing the project, and assigned assets. Where the policy is unapproved the module fails closed and refuses close rather than guessing. Task hierarchy depth, dates, dependencies and progress calculation are bounded and cycle-safe.

## 6. Business Rules

| ID | Rule / verification |
|---|---|
| PROJM-001 | Project code is normalized and unique in approved tenant/entity scope; duplicate/concurrency tests |
| PROJM-002 | Customer/employee/user references are same-tenant and independently authorized; IDOR tests |
| PROJM-003 | Task hierarchy is acyclic, depth-bounded and date/status valid; property/workflow tests |
| PROJM-004 | Membership and assignment do not grant unrelated CRM/HR/finance access; permission tests |
| PROJM-005 | Close/reopen follows approved open-task/expense/asset rules and preserves history; transition tests |
| PROJM-006 | Reports derive operational facts and disclose semantics; no ledger/billing claim; report tests |
| PROJM-007 | Entitlement, tenant isolation, RLS, cache/task/report/export paths fail closed; isolation tests |
| PROJM-008 | Migration/restore preserves codes, hierarchy, assignments, states and audit; recovery tests |
| PROJM-009 | Every state change is recorded in append-only history with actor, time and reason; history tests |
| PROJM-010 | An unapproved closure, costing or timesheet policy disables the dependent behavior rather than applying a default; fail-closed tests |
| PROJM-011 | Progress and date values are validated server-side; a client-supplied progress or status is never authoritative; tamper tests |
| PROJM-012 | Bulk membership, assignment and export operations declare limits, authorization scope and partial-failure reporting; bulk tests |

## 7. Tenant Isolation, Security and Sensitive Data

Every request, service, task, report, export, cache, file and administrative path derives trusted tenant context and validates same-tenant relationships, with PostgreSQL row-level security as defence in depth per ADR-004. A lookup outside the tenant returns a neutral not-found response and never confirms existence.

Applicable threats from `QUAL-THREAT-001`, satisfying `RDY-010`: `THR-010` object reference across tenants; `THR-011` missing tenant filter in reports and aggregates; `THR-012` cache key omitting tenant; `THR-013` background task without tenant context; `THR-014` export artifact authorization; `THR-021` self-granting authority through membership; `ABU-07` bulk extraction of project and member data.

Data classification and retention, satisfying `RDY-009`: project and task records are `C2`; member and assignee identity is `C3`; no `C4` data is stored by this module. Retention class `RET-08` applies to member references and `RET-01` where a project is referenced by a posted financial record, under `QUAL-PRIV-001`. Project history referenced by financial records is never disposed of while the financial obligation persists.

Logs and metrics exclude member personal data beyond identifiers required for correlation.

## 8. Entitlements and Degraded Access

`PROJECTS` entitlement and the relevant user permission are both required on every path, including fragments and exports, per ADR-006. Suspension or expiry denies creation and mutation by default; approved read and export for remediation may be explicitly allowed and audited. Deactivation never deletes project data or breaks references held by Expenses, Fixed Assets or Accounting.

## 9. Integrations and Events

- CRM: read a validated same-tenant customer snapshot; later customer merge or retirement must not rewrite project history.
- HRMS: read a validated same-tenant employee snapshot for membership and assignment.
- Expenses: expose a stable project reference contract for claim coding; a project in a non-chargeable state rejects new references under approved policy.
- Fixed Assets: expose the same reference contract for asset assignment.
- Accounting: publish versioned project facts for cost and revenue analysis; Accounting owns postings and periods.
- Reporting: expose project operational facts for `RPT-601`–`RPT-604` in `PROD-REPORTS-001`.

Material project lifecycle facts are published through the transactional outbox per ADR-010. Consumers are idempotent and version-tolerant. Reconciliation detects project-to-expense, project-to-asset and project-to-ledger reference mismatches.

## 10. UI, API, Reports, Imports and Exports

Django and HTMX surfaces cover the project list with filters, project detail, membership management, task board and list, milestone management, transition confirmation, history, and reconciliation review. Surfaces use the shell, data table, form, status badge, confirmation dialog and empty-state components in `ARCH-UI-001`; destructive and closure actions require the explicit confirmation required by `UIX-036`.

Reports owned by this module and registered in `PROD-REPORTS-001`: `RPT-601` project profitability (operational inputs only; Accounting owns financial truth), `RPT-602` budget against actual, `RPT-603` work in progress and unbilled, `RPT-604` timesheet summary where timesheets are approved.

Imports follow `ARCH-MIGRATION-001` domain 5: project master and membership import through previewed, bounded, idempotent staged services. Import cannot create a closed or historical state, and cannot bypass code uniqueness. Exports are private, authorized, formula-safe and audited.

No document number is allocated by this module beyond the project code, which is registered in `ARCH-SEQ-001` as a non-gapless, tenant-scoped master-data code; it is not a financial document number.

Notifications registered in the `ARCH-NOTIFY-001` catalogue, satisfying `RDY-008`: project assignment, task assignment, milestone due and missed, project state change, and closure blocked. All are operational category, digest-eligible and opt-out permitted; none is mandatory.

## 11. Regulatory and Financial Readiness

This module establishes no accounting, tax, payroll or statutory position. It produces no statutory output and submits nothing to any authority. Project profitability figures are operational and must not be presented as financial statements; `RPT-601` carries that disclosure. No regulatory fact is asserted, per `RDY-012`.

## 12. Operations, Migration and Recovery

Monitor invalid transition attempts, dependency cycles, overdue and open work, closure blocks, unauthorized read attempts, bulk export volume and reconciliation variance. Runbooks cover a stuck transition, an erroneous closure requiring authorized reopen, an orphaned reference after a CRM or HRMS change, and restore reconciliation.

Migration preserves project codes, hierarchy, assignments, states and audit history. Restore verifies project and task counts, code uniqueness, membership integrity, referential consistency with Expenses and Fixed Assets, outbox state and audit completeness.

## 13. Acceptance Criteria, Tests and Evidence

Acceptance criteria are `PROJM-001`–`PROJM-012` and the applicable criteria in `P08-AC-001`–`P08-AC-018`. Required tests are the project scenarios within `P08-TST-001`–`P08-TST-171`, including `P08-TST-001`–`P08-TST-010` for policy readiness and `P08-TST-011`–`P08-TST-025` for the project foundation. Evidence records are `P08-EV-001`–`P08-EV-003` in the [P08 matrix](../02-phases/P08_PROJECTS_EXPENSES_ASSETS/P08_TRACEABILITY_AND_TEST_MATRIX.md).

All scenarios are `NOT_RUN`. Automated tests use the synthetic multi-tenant baseline in `QUAL-TESTDATA-001` and assert a cross-tenant negative outcome alongside each positive one.

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| DEC-PROJ-001 | Initial project, task, timesheet, costing and closure scope | Product / Operations / Finance | Schema work in P08-T02 | Start with project, milestone and task only; keep timesheets and costing out until Accounting contracts exist |
| DEC-GOV-007 | Phase-entry specification gate covering this expansion | Product Owner / Architecture | P08 implementation authorization | Approve the gate and this expanded specification together |

`DEC-PROJ-001` governs closure preconditions, chargeability and any costing behavior. Until it is approved, dependent behavior stays disabled and visible as unavailable rather than defaulted.

## 15. Implementation Prompt

Use the [P08 orchestration prompt](../04-agents/phase-prompts/P08_PROJECTS_EXPENSES_ASSETS.md) and tasks P08-T02–T03 in the [P08 bounded task prompts](../04-agents/phase-prompts/P08_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest; no implementation is authorized by this document.
