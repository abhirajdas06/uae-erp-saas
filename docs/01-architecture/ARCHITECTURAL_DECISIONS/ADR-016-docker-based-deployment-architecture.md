# ADR-016: Docker-Based Deployment Architecture

| Field | Details |
|---|---|
| ADR ID | ADR-016 |
| Title | Docker-Based Deployment Architecture |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 28 October 2026 |
| Decision Owner | Product Architect / DevOps Lead |
| Reviewers | Architecture, Security, Development, Database, DevOps, Operations |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-001, ADR-002, ADR-009, ADR-010, ADR-015, ADR-017, ADR-018, ADR-019 |
| Related Requirements | OPS-001–OPS-004, NFR-004–NFR-011, DEP-001–DEP-003 |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DEVELOPMENT_ROADMAP.md`, `AGENTS.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The Django modular monolith requires repeatable development, test, staging, and production execution for the web application, background workers, scheduler, static assets, migrations, PostgreSQL, Redis, and supporting operational components.

Host-specific manual installation creates drift and makes builds difficult to reproduce. Containers provide a consistent application runtime, but Docker alone does not provide high availability, secret management, backup, monitoring, data residency, or production authorization.

The project does not currently have approved hosting, availability, capacity, or recovery targets. This ADR therefore defines the deployable unit and safety contract without selecting Kubernetes, a cloud provider, or a paid managed service.

## 2. Decision Drivers

- Reproducible application builds and runtime dependencies.
- One coherent release for the modular monolith.
- Separate web, worker, scheduler, and migration process roles.
- Environment parity without copying production data or secrets.
- Safe database migrations and rollback/forward-recovery planning.
- Least privilege, small attack surface, and supply-chain traceability.
- Portability across an approved initial hosting topology.
- Explicit separation of persistent data from disposable containers.

## 3. Options Considered

### Option A: Docker images with Compose for local/test orchestration and an approved production container runtime

**Advantages:** reproducible runtime, process separation, portable artifacts, and practical development workflows.

**Disadvantages:** image security, registry, orchestration, logging, networking, and persistent-service operations still require design.

### Option B: Direct host installation

**Advantages:** fewer container concepts and possibly lower overhead for one host.

**Disadvantages:** configuration drift, difficult reproducibility, shared-host dependency conflicts, and weaker artifact promotion.

### Option C: Kubernetes immediately

**Advantages:** rich orchestration and scaling features.

**Disadvantages:** unjustified operational complexity before workload, availability, and team requirements are known.

### Option D: Platform-specific serverless deployment

**Advantages:** reduced host management for supported workloads.

**Disadvantages:** background workers, long-running tasks, migrations, file handling, networking, and portability may be constrained; no requirement currently justifies lock-in.

## 4. Decision

Package the Django application as a versioned Docker image. Use the same application image for web, Celery worker, scheduler, management, and migration roles, selecting the process through explicit commands. Use Docker Compose for approved local-development and integration-test orchestration. Production runs the immutable image on an approved container runtime and topology selected through deployment planning.

Kubernetes is not part of the initial architecture. It may be considered later only through a separate evidence-based decision.

### 4.1 Image architecture

- Build from a pinned, supported base image.
- Use multi-stage builds where they reduce production tools and attack surface.
- Install dependencies from locked manifests with integrity controls where supported.
- Run application processes as a non-root user.
- Exclude source-control metadata, test secrets, local files, caches, and build credentials.
- Set deterministic locale, timezone, and runtime behavior where required.
- Record source revision, build date, dependency metadata, and immutable image digest.

The image must not contain production secrets or environment-specific customer configuration.

### 4.2 Process roles

The initial logical roles are:

- Nginx or an approved reverse proxy, normally outside the Django image.
- Gunicorn web process.
- Celery worker processes with approved queues.
- One authoritative scheduler process.
- One-shot migration/release job.
- One-shot administrative commands under explicit authorization.

Do not run unrelated long-lived processes under an opaque supervisor in one container merely to reduce container count. Local Compose may group services on one host; that does not merge their operational responsibilities.

### 4.3 Persistent services and data

PostgreSQL, Redis, object/file storage, backups, and logs have explicit persistent-service designs. Container writable layers are disposable and must not be the only location of customer data, uploaded files, audit evidence, secrets, or backups.

Managed or self-hosted PostgreSQL and Redis are both possible pending operational review. Their production lifecycle is not defined solely by an application Compose file.

### 4.4 Environment separation

Maintain separate local, test, staging/pre-production, and production configuration and credentials. Images should be promoted between environments without rebuilding from different source when practical; environment behavior comes from validated configuration and approved external services.

Production data must not be copied into lower environments without an explicit, protected, and legally reviewed process.

### 4.5 Networking and exposure

- Expose only required public ports through the approved ingress/reverse proxy.
- Keep database, Redis, workers, scheduler, and internal administrative endpoints on restricted networks.
- Use TLS for public traffic and protected internal traffic where the threat model requires it.
- Health endpoints reveal minimal information.
- Egress to providers is controlled and observable where practical.

### 4.6 Static and uploaded files

Static assets are built and versioned reproducibly, then served through the approved proxy or asset service. Uploaded and generated customer files use the storage architecture decided in ADR-019; they are not tied to one web container.

### 4.7 Migrations and release sequence

Migrations run as an explicit, authorized release step, not independently on every web or worker startup. The deployment plan must define:

1. Pre-deployment backup/recovery readiness.
2. Migration compatibility and lock analysis.
3. Image and configuration validation.
4. Staged schema/application rollout where required.
5. Worker and scheduler compatibility.
6. Health and smoke checks.
7. Rollback or forward-recovery path.
8. Post-deployment reconciliation.

A code rollback does not reverse a migration automatically.

### 4.8 Health and lifecycle

Containers support appropriate liveness, readiness, and startup checks. Readiness must distinguish application startup from ability to serve safely. Graceful shutdown must stop accepting work, finish or safely release in-flight requests/tasks, and preserve durable operation state.

### 4.9 Image promotion and release identity

Deploy immutable image digests, not mutable tags alone. Record which digest, configuration version, migration set, and release approval reached each environment. Rebuilds require new identity even from the same source revision.

### 4.10 Local development

Local Compose may provide Django, PostgreSQL, Redis, and supporting services with safe non-production defaults. It must not embed real credentials, impersonate production security evidence, or require every optional production component for simple documentation work.

### 4.11 Production topology

The first production topology remains pending capacity, budget, data-residency, availability, RPO/RTO, and operational-support decisions. A single host may be suitable only for an explicitly approved bounded pilot with documented failure and recovery limitations. Docker Compose alone is not evidence of production high availability.

## 5. Rationale

A single immutable application image matches the modular monolith and avoids separate builds for web and workers. Explicit process roles preserve operational isolation. Compose supports reproducible local and integration environments without committing the project to a premature production orchestrator.

## 6. Consequences

### Positive consequences

- Reproducible application runtime and dependency set.
- Consistent artifact promotion and rollback identity.
- Clear web, worker, scheduler, and migration roles.
- Portability across reasonable container hosting options.

### Negative consequences and trade-offs

- Requires image scanning, registry, build, and runtime operations.
- Production persistent services still need separate management.
- Container networking and filesystem assumptions require testing.
- Local Compose can differ materially from managed production services.

### Risks and mitigations

- **Secrets in layers:** build-context controls, secret scanning, and runtime injection.
- **Mutable releases:** deploy digests and record provenance.
- **Data on ephemeral layers:** external persistent services and recovery tests.
- **Unsafe automatic migrations:** dedicated release job and approval gate.
- **Oversized privileged image:** multi-stage build, non-root runtime, and minimal packages.

## 7. Security and Tenant-Isolation Implications

- Containers do not replace application or RLS tenant isolation.
- Runtime identities receive only required network, file, database, broker, and storage access.
- Web and worker roles may require different credentials and permissions.
- Administrative commands and shell access are privileged and audited.
- Images, registries, runners, and hosts require patching and vulnerability response.

## 8. Data Integrity and Migration

- Persistent data is outside disposable containers.
- Migration jobs use separately authorized credentials.
- Deployment overlap preserves old/new schema compatibility where required.
- Backup and restore are tested independently of image rebuild.
- Stateful rollback uses an approved database recovery plan.

## 9. Operational Impact

Operations must manage registry access, image retention, vulnerability updates, runtime health, resource limits, logs, metrics, host capacity, TLS, DNS, backups, recovery, and incident response. Hosting costs and topology must be approved before production.

## 10. Implementation Requirements

1. Create deployment and infrastructure specifications before production implementation.
2. Define a locked, multi-stage, non-root application image.
3. Define Compose services for authorized development and test use.
4. Establish image build, scan, provenance, registry, and promotion controls.
5. Define release/migration ordering and recovery.
6. Externalize secrets, media, logs, database, Redis persistence, and backups.
7. Define health checks, graceful shutdown, and resource limits.
8. Select production topology only after capacity, residency, RPO/RTO, and cost review.

## 11. Validation and Acceptance Criteria

- [ ] A clean environment builds the same declared application artifact reproducibly.
- [ ] Production image runs as non-root and contains no known real secrets.
- [ ] Web, worker, scheduler, and migration roles use explicit commands.
- [ ] Customer data survives container replacement.
- [ ] Database and Redis are not publicly exposed.
- [ ] Migrations do not run concurrently from every application replica.
- [ ] Health checks and graceful shutdown behave correctly.
- [ ] Image digest and source revision are recorded for deployment.
- [ ] Rollback/forward-recovery and restore procedures are exercised.
- [ ] Compose is not represented as proof of production availability.

## 12. Alternatives Rejected

- Unmanaged direct-host installation is rejected as the standard.
- Kubernetes is rejected for the initial architecture absent evidence.
- Production secrets baked into images are rejected.
- Customer data on container writable layers is rejected.
- Automatic migration from every web startup is rejected.

## 13. References

- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- `docs/01-architecture/ARCHITECTURAL_DECISIONS/ADR-001-modular-monolith-architecture.md`
- Docker documentation: https://docs.docker.com/
- Docker Compose documentation: https://docs.docker.com/compose/
- Django deployment checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** One immutable Docker application image, explicit process roles, Compose for local/test, and a separately approved production container topology.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; provider, region, topology, capacity, managed services, RPO/RTO, and cost remain unresolved.

Hosting provider, region, topology, capacity, managed services, RPO/RTO, and cost remain unresolved and block production deployment. They do not block deployment-document drafting.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial Docker-based deployment decision accepted after standards review. |
