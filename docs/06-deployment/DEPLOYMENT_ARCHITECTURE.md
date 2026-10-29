# Deployment Architecture

| Property | Value |
|---|---|
| Document ID | DEP-ARCH-001 |
| Status | READY FOR REVIEW — TOPOLOGY/PROVIDER DECISIONS OPEN |
| Authority | ADR-016, ADR-017, ADR-019 |

## 1. Purpose and Principles

Define the provider-neutral production deployment boundary for the Django modular monolith. One immutable application image supplies explicit web, worker, scheduler, migration and administrative commands. Containers are replaceable; PostgreSQL, object storage, backup evidence, secrets and operational telemetry are external persistent services.

Docker is the packaging architecture, not evidence of availability, security or recovery. Kubernetes and microservices are excluded from the initial design unless a later ADR demonstrates need.

## 2. Logical Topology

```text
Internet -> DNS/TLS/WAF-or-proxy -> Nginx/ingress -> Gunicorn web replicas
                                              |-> restricted admin/health routes
Django web/worker/scheduler -> PostgreSQL (authoritative relational data)
                            -> Redis (broker and approved ephemeral workloads)
                            -> private object storage (customer/generated files)
                            -> approved external providers
                            -> centralized logs/metrics/traces/alerts
Release job -> migration command -> PostgreSQL
Backup service -> encrypted isolated backup storage -> restore environment
```

Only ingress is public. Database, Redis, workers, scheduler, migration/admin commands and storage control planes use restricted networks and identities.

## 3. Environments and Promotion

Local, CI/test, staging/pre-production and production have separate credentials, data, endpoints and access. Build once from a reviewed revision, record provenance/SBOM and promote the immutable digest. Production-like staging uses synthetic or explicitly approved protected data; production data is not casually copied downward.

Each deployment records source commit, image digest, dependency lock/SBOM, configuration schema/version, migration set, static artifact, enabled modules/integrations, approvers and timestamps.

## 4. Process and Identity Boundaries

- Web: request-serving credentials and least required database/storage/network access.
- Worker: queue-specific identity, explicit tenant context and graceful task shutdown.
- Scheduler: exactly one logical scheduler per schedule namespace; no duplicate periodic intent.
- Migration: one-shot, separately authorized, stronger schema privilege only for the job duration.
- Administrative command: ticketed, scoped, audited and disabled by default.
- Proxy/ingress: TLS, request limits, safe headers, trusted proxy configuration and minimal health exposure.

## 5. Persistence and Failure Domains

Customer data never relies on container writable layers. PostgreSQL durability, replica/failover strategy if selected, Redis loss semantics, object versioning/replication, backup isolation and telemetry retention are separately configured. A topology decision documents region, failure domains, single points, maintenance, capacity, RPO/RTO and cost.

## 6. Security and Isolation

Runtime is non-root with read-only/minimal filesystem where practical, pinned images, vulnerability scanning, resource limits and no embedded secrets. Network, database, broker, storage and provider permissions differ by role. Infrastructure does not replace tenant scoping, RLS, authorization or entitlements.

## 7. Availability and Scaling

Scale web/worker roles from measured demand. Database connections, queue depth, storage throughput and provider limits are first-class constraints. Horizontal replicas require stateless requests, shared sessions/cache where approved, singleton scheduling and schema compatibility. No HA claim is made until failure tests demonstrate it.

## 8. Acceptance Evidence

- Approved topology diagram/inventory and threat/failure analysis.
- Reproducible non-root image, digest/provenance/SBOM/scan evidence.
- Network/identity/secret/storage least-privilege tests.
- Clean deploy, migration, smoke, graceful shutdown and replacement tests.
- Capacity, failover/degradation, backup/restore and observability evidence.
- Recorded provider/region/cost/RPO/RTO decisions and launch approval.
