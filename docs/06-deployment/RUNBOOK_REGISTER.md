# Operations Runbook Register

| Document ID | DEP-RUN-REG-001 |
|---|---|
| Status | PLANNED — COMMANDS/CONTACTS REQUIRE IMPLEMENTATION |

| Runbook ID | Scenario | Owner role | Required by | Current state |
|---|---|---|---|---|
| RUN-001 | Web application unavailable/degraded | On-call Operations | P12 rehearsal | BLOCKED_IMPLEMENTATION |
| RUN-002 | Worker/queue backlog or poison task | Application Operations | First Celery workload | BLOCKED_IMPLEMENTATION |
| RUN-003 | PostgreSQL saturation/failover/recovery | Database Owner | P12 rehearsal | BLOCKED_TOPOLOGY |
| RUN-004 | Suspected cross-tenant exposure | Security Incident Commander | First tenant data | BLOCKED_IMPLEMENTATION |
| RUN-005 | Financial integrity/reconciliation failure | Finance Domain Owner | First financial release | BLOCKED_IMPLEMENTATION |
| RUN-006 | Secret compromise/rotation | Security / Operations | First deployed secret | BLOCKED_SECRETS_BACKEND |
| RUN-007 | File/object loss, malware or authorization incident | File/Storage Owner | First file workflow | BLOCKED_IMPLEMENTATION |
| RUN-008 | Provider timeout/duplicate/uncertain outcome | Owning Integration | First provider integration | BLOCKED_PROVIDER |
| RUN-009 | Backup restore and point-in-time recovery | Database / Storage Owner | P12 rehearsal | BLOCKED_TOPOLOGY |
| RUN-010 | Failed deployment/migration containment | Release / Database Owner | First release | BLOCKED_IMPLEMENTATION |
| RUN-011 | Capacity exhaustion/noisy tenant | Operations / Architecture | P11 load test | BLOCKED_WORKLOAD_MODEL |
| RUN-012 | Monitoring/alerting pipeline failure | Observability Owner | P12 rehearsal | BLOCKED_TOOL_SELECTION |

Each runbook is created from `RUNBOOK_TEMPLATE.md`, exercised in the target-like environment, and records version, evidence and next exercise. Real contacts, commands and credentials never belong in public documentation or evidence artifacts.
