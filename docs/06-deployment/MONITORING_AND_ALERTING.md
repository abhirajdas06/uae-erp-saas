# Monitoring and Alerting Specification

| Property | Value |
|---|---|
| Document ID | DEP-OBS-001 |
| Status | READY FOR REVIEW — SERVICE TARGETS AND TOOLING OPEN |

## 1. Signal Principles

Observability must answer whether users are safe, data is correct, dependencies are healthy and operators can act. Signals carry environment, service/role, release and correlation—not tenant/customer/personal/financial payloads unless explicitly minimized and protected. Logs, metrics, traces and audit have distinct purposes under ADR-018.

## 2. Required Coverage

| Area | Example signals and conditions |
|---|---|
| User service | request rate/error/latency, readiness, authentication/authorization anomalies, rate limits |
| Django/Gunicorn | workers, timeouts, exceptions, saturation, deploy/release identity |
| PostgreSQL | availability, connections, latency, locks/deadlocks, replication/PITR/backup state, storage, slow queries |
| Redis/Celery | availability, memory/eviction, queue depth/age, task failure/retry/runtime, workers, scheduler heartbeat |
| Files | upload/scan/quarantine/delivery errors, storage capacity, metadata/content reconciliation |
| Integrations | availability/latency/rate, auth/certificate/consent expiry, callback failures, uncertain/dead-letter operations |
| Business integrity | posting/reconciliation drift, duplicate suppression, e-invoice/payroll/bank exceptions, subscription/entitlement anomalies |
| Security | privileged access, support/break-glass, secret/config change, repeated denial, suspicious export/file access |
| Backup/recovery | job freshness/failure, WAL/object protection, restore-drill age and unresolved recovery findings |
| Capacity/cost | CPU/memory/storage/connections/queue/provider quotas, trends, headroom and budget anomalies |

## 3. Alert Contract

Every alert has ID, owner/service, severity, condition/window, data source, runbook, notification/escalation, dedup/suppression, expected response, test method and review date. Alerts are symptom/action based, not raw noise. Maintenance and deployment suppression is bounded and audited; critical blind spots remain visible.

Severity: `SEV1` major security/data-integrity/tenant exposure or broad outage; `SEV2` material degradation or critical workflow unavailable; `SEV3` limited degradation/action needed; `SEV4` informational/trend. Actual incident classification follows INCIDENT_RESPONSE.md.

## 4. Dashboards, Retention and Access

Provide release/service health, database/queues, integrations, business reconciliation, security, backup/recovery and capacity dashboards. Access is least privilege; sensitive searches/exports are audited. Retention and sampling are category-approved. Telemetry outage is monitored independently where practical.

## 5. Evidence

Synthetic signal/alert tests, notification delivery, escalation acknowledgment, runbook execution, false-positive/negative review, redaction scans, dashboard permissions, retention, telemetry failure behavior and post-incident alert improvements.
