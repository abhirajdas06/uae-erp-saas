# Deployment and Operations Documentation Index

| Document ID | DEP-INDEX-001 |
|---|---|
| Status | CANONICAL INVENTORY |

| Document | Authority |
|---|---|
| `DEPLOYMENT_ARCHITECTURE.md` | Provider-neutral production topology and trust boundaries |
| `INFRASTRUCTURE_REQUIREMENTS.md` | Required capability classes and selection constraints |
| `ENVIRONMENT_VARIABLES.md` | Configuration/secrets contract; exact inventory is implementation-generated |
| `DEPLOYMENT_GUIDE.md` | Release/deployment/migration procedure |
| `RELEASE_AND_ROLLBACK.md` | Compatibility, containment and forward-recovery policy |
| `BACKUP_AND_RECOVERY.md` | Backup/PITR/object recovery and reconciliation |
| `MONITORING_AND_ALERTING.md` | Signals, alert contract and observability safety |
| `INCIDENT_RESPONSE.md` | Incident roles, severity, containment, evidence and review |
| `OPERATIONS_RUNBOOK.md` | Runbook governance and response categories |
| `RUNBOOK_REGISTER.md` / `RUNBOOK_TEMPLATE.md` | Stable planned runbook IDs and implementation template |
| `CAPACITY_AND_PERFORMANCE.md` | Capacity/load evidence; product targets are in QUAL-PERF-001 |
| `OPERATIONAL_EVIDENCE_SPECIFICATION.md` | Required evidence metadata and integrity |
| `PRODUCTION_LAUNCH_CHECKLIST.md` | P12 deployment and separate business-launch checklist |
| `EXTERNAL_API_AND_ACCESS_REQUIREMENTS.md` | Every external API, service and account the build needs, what is blocked without each, and how to obtain it |

Actual provider, region, topology, contacts, secrets backend, SLO/RPO/RTO, capacity, alert thresholds and commands remain blocked on `DEC-OPS-*`, implementation and measured rehearsal. Documentation does not authorize infrastructure purchase, deployment or launch.

`DEC-OPS-001` determines legal/business data-location and residency constraints. `DEC-OPS-004` selects a provider/region/topology that satisfies those constraints. They are related but not duplicate decisions.
