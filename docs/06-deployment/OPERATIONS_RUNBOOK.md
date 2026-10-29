# Operations Runbook Index and Control Specification

| Property | Value |
|---|---|
| Document ID | DEP-RUN-001 |
| Status | READY FOR REVIEW — EXECUTABLE COMMANDS PENDING IMPLEMENTATION |

## 1. Runbook Contract

Each executable runbook records ID/owner/reviewer, purpose/trigger, impact and required authorization, supported environment/version, prerequisites/access, exact commands with safe parameters, expected output, stop/abort conditions, verification/reconciliation, rollback/forward-recovery, evidence path, escalation and last exercise date. Commands never embed secrets or broad destructive targets.

## 2. Required Runbooks

- Service health triage; web/worker/scheduler restart and graceful drain.
- Queue backlog, failed/dead-letter/uncertain task investigation and approved replay.
- Database connections/locks/slow query/storage; migration failure and reconciliation.
- Redis degradation/loss and task redelivery verification.
- Object upload/scan/delivery failure and metadata/content reconciliation.
- Certificate/domain/secret expiry, rotation and compromise response.
- Provider outage, callback backlog, rate limit and uncertain external operation.
- Backup failure, PostgreSQL/object restore and tenant logical recovery.
- Release rollback/forward-fix and emergency disable/feature rollback.
- Tenant suspension/reactivation/offboarding, support grant and break-glass review.
- Financial/subledger/payroll/inventory/bank reconciliation exception.
- Capacity saturation, disk/connection/queue/provider quota and telemetry outage.

## 3. Daily/Periodic Controls

Review critical alerts/incidents, backup freshness, failed/uncertain operations, security/privileged events, expiring certificates/secrets/consents, capacity trends, provider health and reconciliation exceptions at approved cadence. Periodically review access, patch/vulnerabilities, restore drills, alert/runbook quality, retention/disposal, costs and risk register.

## 4. Shift/Handoff and Maintenance

Handoff records active incidents/changes, degraded services, uncertain operations, backlog, expiring items, pending approvals and next actions. Maintenance uses change/release policy, customer communications where required, monitoring suppression bounds and post-maintenance verification.

## 5. Exercise Evidence

Named operator executes in a representative environment from the saved runbook; observer records timing, deviations, unsafe ambiguity, expected/actual outputs, reconciliation, findings and update approval. An unexercised placeholder is not launch evidence.
