# PROJECTS — Project Operations Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-PROJECTS-001 |
| Status | READY FOR REVIEW — PROJECT POLICY REQUIRED |
| Owning phase / app | P08 / `projects` |

## 1. Purpose and Boundary

Own tenant project identity, lifecycle, membership, tasks, milestones, assignments and operational progress under `PROJ-001` and P08-SPEC-001. CRM owns customers, HRMS owns employees, Expenses owns claims and Accounting owns ledger/cost accounting. Project references never confer customer, employee or financial authorization.

Initial scope excludes authoritative timesheets, billing, resource capacity, project accounting, revenue recognition and portfolio optimization.

## 2. Actors and Permissions

Project administrator, project manager, member, viewer, auditor and purpose-bound support. Create, configure, assign, transition, close/reopen, report/export and privileged support actions are separate and object-scoped.

## 3. Conceptual Model and Lifecycle

`Project`, `ProjectMember`, `Milestone`, `Task`, `TaskAssignment`, `ProjectStatusHistory` and optional approved `ProjectReferenceSnapshot`. Draft → active → on-hold → completed/closed/cancelled transitions use explicit rules. Task hierarchy depth, dates, dependencies and progress calculation are bounded and cycle-safe.

## 4. Rules and Verification

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

## 5. Operations and Decisions

Monitor invalid transitions, dependency cycles, overdue/open work, unauthorized reads and bulk exports. `DEC-PROJ-001` must settle initial project, task, timesheet, costing and closure scope before schema work.
