# ADR-009: Celery, Redis, and Background Task Execution

| Field | Details |
|---|---|
| ADR ID | ADR-009 |
| Title | Celery, Redis, and Background Task Execution |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / DevOps Lead |
| Reviewers | Architecture, Security, Development, DevOps, Operations |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-001, ADR-003, ADR-004, ADR-005, ADR-006, ADR-010, ADR-012, ADR-017, ADR-018 |
| Related Requirements | OPS-002, INT-001–INT-002, NFR-001, NFR-005–NFR-007, DEP-001–DEP-003 |
| Related Documents | `EVENT_AND_TASK_PROCESSING.md`, `SYSTEM_ARCHITECTURE.md`, `MULTI_TENANCY.md`, `API_STANDARDS.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The platform needs asynchronous and scheduled processing for email, documents, imports, exports, subscription changes, provider integrations, reporting, reconciliation, e-invoicing, and other workloads that should not block an HTTP request.

Task delivery is not exactly once. Workers can stop after a side effect but before acknowledging a message; messages can be redelivered; retries can overlap; and an external timeout can leave the actual provider outcome uncertain. Redis is suitable as a Celery broker and supporting cache, but it must not become the sole durable record of critical business work.

## 2. Decision Drivers

- Reliable, observable, and bounded asynchronous execution.
- Explicit tenant and authorization context.
- Safe retries and duplicate delivery.
- Durable business state in PostgreSQL.
- Independent scaling of web and worker processes without microservices.
- Workload isolation and operational recovery.
- Secure message serialization and secret handling.

## 3. Options Considered

### Option A: Celery with Redis broker and PostgreSQL operation records

**Advantages:** mature Django ecosystem, flexible workers and scheduling, straightforward initial operations, and durable business truth remains in PostgreSQL.

**Disadvantages:** at-least-once behavior, broker operations, and task-idempotency discipline are required.

### Option B: Synchronous request processing

**Advantages:** simplest transaction flow.

**Disadvantages:** request timeouts, poor user experience, inability to handle long-running or scheduled work, and weak recovery.

### Option C: Database polling without Celery

**Advantages:** one durable store.

**Disadvantages:** custom worker framework, scheduling, concurrency, retry, and monitoring burden.

### Option D: Managed queues or a different broker immediately

**Advantages:** potentially stronger durability or managed operations.

**Disadvantages:** additional cost and provider dependency without an approved requirement. It remains a reconsideration option.

## 4. Decision

Use Celery for approved background and scheduled tasks, with Redis as the initial broker and supporting transient infrastructure. PostgreSQL remains authoritative for business state, required work, operation status, idempotency, and audit evidence.

Design every task for at-least-once delivery. No task may assume that delivery, execution, acknowledgement, or a returned provider response proves exactly-once business completion.

### 4.1 Appropriate task use

Tasks are appropriate for bounded work that is slow, retryable, scheduled, resource intensive, or crosses an external boundary. Small local operations that require immediate atomic consistency should remain synchronous within a database transaction.

### 4.2 Task contract

Task messages contain stable identifiers and minimal routing context, such as:

- Task contract name and version.
- Tenant identifier where applicable.
- Durable operation or object identifier.
- Correlation identifier.
- Initiating actor reference where required for audit.
- Safe, bounded parameters.

Do not serialize model instances, passwords, API keys, access tokens, full sensitive documents, or unbounded payloads into broker messages.

### 4.3 Tenant and authorization context

Workers must load the durable operation, validate its tenant ownership and current state, establish the transaction-local tenant context under ADR-004, and call the same application services used by synchronous interfaces.

A queued task does not preserve a user's session or permanent authority. The owning workflow must define whether current authorization is revalidated, whether the task runs as a constrained system operation, and how revocation affects pending work.

### 4.4 Idempotency and concurrency

Tasks with side effects require a durable idempotency key or operation record and a defined concurrency strategy. Duplicate delivery must produce the same valid business outcome or a safe no-op.

Use database constraints, state transitions, row locks, advisory locks, leases, or compare-and-set behavior as justified by the workflow. A Celery task ID alone is not a sufficient business idempotency key.

### 4.5 Retry policy

Retries must be explicit, bounded, and classified by failure type:

- Transient infrastructure or provider failure may retry with backoff and jitter.
- Validation, authorization, unsupported state, and permanent provider rejection must not retry blindly.
- Uncertain external outcomes require status inquiry or reconciliation before repeating a side effect.
- Exhausted retries must leave a discoverable durable failure state.

Default retry counts, timeouts, and backoff profiles are deployment decisions that must be approved per task category.

### 4.6 Acknowledgement and worker failure

Celery acknowledgement settings, visibility timeouts, prefetch, worker termination, and late acknowledgement behavior must be selected and tested for each workload profile. Configuration must favor recoverable duplicate delivery over silent loss for critical work.

Tasks must tolerate worker termination between local commit, external effect, result recording, and broker acknowledgement.

### 4.7 Queue topology

Begin with a small number of explicit queues. Separate workloads only when latency, resource, security, or failure characteristics justify it, for example:

- Default short tasks.
- External integrations.
- Resource-intensive reports or exports.
- Sensitive or tightly controlled finance/payroll tasks where operational isolation is justified.

Queue names are operational routing, not business authorization.

### 4.8 Scheduling

Use one authoritative scheduler deployment for periodic tasks. Each schedule must define timezone, overlap policy, missed-run behavior, idempotency, tenant enumeration, and recovery.

Tenant-local business dates must be calculated from approved tenant and legal-entity configuration; scheduler host time is not authoritative.

### 4.9 Results and status

Celery result storage is not the authoritative user-visible operation state. Important operations require PostgreSQL records with controlled states, timestamps, attempts, errors safe for retention, and recovery metadata.

### 4.10 Serialization and security

Use safe serializers such as JSON for task messages. Unsafe deserialization formats are prohibited. Broker credentials, network access, and administrative interfaces must follow least privilege and secrets-management requirements.

## 5. Rationale

Celery and Redis fit the modular Django deployment while allowing web and worker capacity to scale separately. Keeping durable intent and status in PostgreSQL addresses broker loss, duplicate delivery, and operational recovery without treating Redis as a financial or regulatory system of record.

## 6. Consequences

### Positive consequences

- Responsive requests and supported scheduled work.
- Shared Django domain services across web and workers.
- Recoverable duplicate delivery and durable operation visibility.
- Targeted worker and queue scaling.

### Negative consequences and trade-offs

- Additional infrastructure, deployment, monitoring, and security surface.
- Every side-effecting task needs idempotency and failure design.
- Redis outages and worker backlog require operational procedures.
- Correct local development does not prove production broker behavior.

### Risks and mitigations

- **Duplicate effects:** durable idempotency and reconciliation.
- **Lost required work:** transactional outbox under ADR-010.
- **Tenant-context leakage:** transaction-local context and worker tests.
- **Retry storms:** bounded backoff, jitter, circuit breaking, and rate limits.
- **Sensitive message exposure:** minimal JSON payloads and secured broker access.

## 7. Security and Tenant-Isolation Implications

- Workers use restricted database and broker credentials.
- Every tenant task validates ownership from durable state.
- Logs and failure records exclude unnecessary secrets and sensitive payloads.
- Manual retry, revoke, replay, and recovery operations require authorization and audit.
- A shared queue does not permit cross-tenant data access.

## 8. Data Integrity and Migration

- Critical tasks require durable operation and idempotency schemas.
- Migrations must support deployment overlap between old and new workers.
- Tasks must tolerate compatible payload versions during rolling deployment.
- Destructive changes to queued contract fields require drain, translation, or compatibility plans.

## 9. Operational Impact

Monitor queue depth, oldest task age, task latency, failures, retries, runtime, worker health, scheduler health, Redis capacity, operation-state age, and reconciliation failures. Runbooks must cover broker outage, poison messages, stuck tasks, worker termination, manual recovery, and safe replay.

## 10. Implementation Requirements

1. Pin Celery and Redis client versions and document compatibility.
2. Define task naming, payload versioning, and base logging conventions.
3. Establish restricted web, worker, broker, and database credentials.
4. Implement durable operation records for critical workflows.
5. Define retry and timeout profiles by workload category.
6. Establish one scheduler and overlap-safe schedules.
7. Add health checks, metrics, alerts, and recovery runbooks.
8. Test duplicate delivery, worker termination, retries, context isolation, and deployment overlap.

## 11. Validation and Acceptance Criteria

- [ ] Duplicate task delivery does not duplicate business effects.
- [ ] Worker termination at critical points results in safe retry or reconciliation.
- [ ] Missing or invalid tenant context fails closed.
- [ ] Authorization and operation state are revalidated according to policy.
- [ ] Permanent failures do not retry indefinitely.
- [ ] Uncertain provider outcomes do not trigger blind duplicate requests.
- [ ] Scheduled jobs are overlap-safe and timezone-correct.
- [ ] Redis loss does not erase authoritative business state.
- [ ] Manual recovery is authorized, bounded, and audited.
- [ ] Monitoring detects backlog, stale work, and repeated failure.

## 12. Alternatives Rejected

- Synchronous processing for all work is rejected.
- Redis as the authoritative operation record is rejected.
- Exactly-once delivery assumptions are rejected.
- Unsafe serialized Python objects are rejected.
- Unbounded automatic retries are rejected.

## 13. References

- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- Celery documentation: https://docs.celeryq.dev/en/stable/
- Redis documentation: https://redis.io/docs/latest/
- Django transactions: https://docs.djangoproject.com/en/stable/topics/db/transactions/

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Celery with Redis broker and PostgreSQL durable operation state.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; broker topology, capacity, and retry values remain deployment/implementation decisions.

This accepted decision governs future worker and scheduler implementation, which remains phase-authorized work.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial background task execution decision accepted after standards review. |
