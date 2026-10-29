# Infrastructure Requirements

| Property | Value |
|---|---|
| Document ID | DEP-INFRA-001 |
| Status | READY FOR REVIEW — SIZING AND PROVIDER SELECTION OPEN |

## 1. Required Capabilities

| Capability | Minimum contract | Evidence before production |
|---|---|---|
| Compute/runtime | Immutable digest deployment; non-root; role-specific commands; resource requests/limits; graceful restart | Build/deploy/replacement/load evidence |
| Ingress/TLS/DNS | Approved domains, TLS renewal, redirect/HSTS policy, request/body/time limits, trusted proxies, restricted admin endpoints | External TLS/header/routing tests and ownership records |
| PostgreSQL | Supported version, encryption, restricted network/roles, durable storage, monitoring, backup/PITR as required, tested restore | Role/RLS/connectivity, migration, backup/restore and capacity evidence |
| Redis | Restricted/authenticated service, memory/eviction/persistence semantics documented, monitoring, no authoritative-only data | Loss/restart/task redelivery and load evidence |
| Object storage | Private buckets/containers, encryption, version/lifecycle, signed delivery, malware workflow, backup/recovery and reconciliation | Cross-tenant/file/restore tests |
| Secrets | Approved backend, workload identity/access, audit, rotation/version, break-glass and recovery | Injection/rotation/revoke/leak-scan tests |
| Registry/build | Protected registry, immutable digest, signed/provenance/SBOM as approved, retention and vulnerability policy | Rebuild/promotion/scan evidence |
| Observability | Central logs, metrics, traces/correlation where approved, alerts, dashboards, retention and protected access | Signal/alert/runbook drill evidence |
| Backup storage | Encrypted, isolated credentials/account where feasible, immutable/protected retention, inventory and deletion controls | Scheduled jobs, integrity and independent restore evidence |
| CI/CD | Protected environments, least-privilege federation/tokens, approvals, artifact integrity and audit | Pipeline and unauthorized-release tests |

## 2. Environment Inventory

Every environment inventory records provider/account/project, region/zone, network/subnets/firewalls, domains/certificates, compute roles/counts, database/Redis/storage/backup/observability services, identities, owners, data classification, maintenance window, dependencies, capacity, costs and expiry.

## 3. Production Baseline

- No default/test credentials, development debug, wildcard origins/hosts, public database/Redis or unprotected object storage.
- Separate human and workload identities; MFA and privileged access review.
- Time synchronization, supported OS/runtime, patching and vulnerability response.
- Resource limits and quotas prevent one process/tenant/job from exhausting shared capacity.
- Provider quotas, account limits and support/escalation paths are documented.
- Cost budgets/alerts and ownership exist; estimates are labelled until verified.

## 4. Open Selection Gates

`DEC-OPS-001` selects region/provider/residency; `DEC-OPS-002` selects availability/RPO/RTO; `DEC-OPS-003` selects object storage; `DEC-OPS-004` selects production topology/operations model. No vendor or paid service is selected by this document.
