# Deployment and Environment Promotion Guide

| Property | Value |
|---|---|
| Document ID | DEP-GUIDE-001 |
| Status | PROCEDURE SPECIFICATION — COMMANDS PENDING IMPLEMENTATION |

## 1. Preconditions

Use only an approved release candidate with immutable image digest, provenance/SBOM/scans, passing required CI/evidence, approved configuration schema, reviewed migrations, current backup/restore status, capacity headroom, change ticket/window, named release commander and rollback/forward-recovery plan. Verify target environment identity before any action.

## 2. Promotion Procedure

1. Record release manifest: commit, digest, config, migrations, static assets, modules/integrations and evidence.
2. Validate environment inventory, dependencies, quotas, certificates, secrets references and monitoring.
3. Confirm backup/recovery checkpoint and restore confidence appropriate to the change.
4. Run preflight commands in read-only/dry-run mode; capture redacted output and exit codes.
5. Quiesce or manage incompatible traffic/tasks/schedules according to the release plan.
6. Run the single authorized migration job with lock/duration monitoring; stop on unapproved divergence.
7. Deploy digest by explicit role with readiness/startup checks; retain previous artifact/config identity.
8. Promote static assets and restart/reload roles in the approved compatibility order.
9. Execute health, smoke, tenant-isolation, authorization, financial/reconciliation and provider checks for release scope.
10. Observe defined stabilization signals; compare errors, latency, queues, database and business invariants.
11. Declare success, rollback, forward-fix or incident; update release/evidence/CMDB and communicate.

## 3. Migration Safety

Expand/migrate/contract is preferred for incompatible schema changes. Assess table size, locks, rewrite, duration, indexes, old/new application overlap, worker/scheduler compatibility, backfill throttling, rollback boundary and reconciliation. Code rollback never automatically reverses schema or data migration.

## 4. Failure Handling

Abort before external effects if preflight fails. After possible external/data effects, preserve evidence and follow release/incident procedures. Do not improvise destructive SQL, restore production over live data or rerun uncertain commands. Use a separately reviewed forward fix or recovery plan.

## 5. Required Evidence

Exact reproducible commands/versions, actor/time/environment, exit status and redacted logs; migration timing/locks/counts; deployed digest/config; health/smoke/security/business reconciliation; monitoring window; decision and approver; deviations/exceptions and follow-up.
