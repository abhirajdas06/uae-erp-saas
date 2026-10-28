# ADR-010: Transactional Outbox and Event Delivery

| Field | Details |
|---|---|
| ADR ID | ADR-010 |
| Title | Transactional Outbox and Event Delivery |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / Integration Lead |
| Reviewers | Architecture, Security, Database, Development, DevOps, Operations |
| Affected Phases | P01–P12 |
| Related ADRs | ADR-001, ADR-003, ADR-004, ADR-006, ADR-009, ADR-012, ADR-018, ADR-020 |
| Related Requirements | OPS-002, INT-001–INT-002, NFR-006–NFR-007, EIN-002–EIN-004, BILL-004 |
| Related Documents | `EVENT_AND_TASK_PROCESSING.md`, `API_STANDARDS.md`, `DATABASE_DESIGN.md`, `ENTITLEMENT_ENGINE.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

A business transaction often needs follow-up work after committing PostgreSQL state: publish an internal event, queue a task, notify another domain, send a document, or call an external provider. Writing business state and publishing to a broker are separate operations. If publication happens before commit, consumers may see state that later rolls back. If it happens after commit, a crash can leave committed work unpublished.

`transaction.on_commit()` narrows the timing window but does not durably preserve unpublished intent if the process stops before publication succeeds. Critical workflows need an atomic record that follow-up work is required.

## 2. Decision Drivers

- No silent loss of critical post-commit work.
- Atomicity between business state and delivery intent.
- Safe duplicate publication and consumption.
- Explicit tenant ownership, schema versioning, and event ownership.
- Operational visibility, replay, reconciliation, and retention.
- Compatibility with Celery/Redis without making the broker authoritative.

## 3. Options Considered

### Option A: PostgreSQL transactional outbox

Write business changes and an outbox record in one database transaction. A dispatcher publishes committed records asynchronously.

**Advantages:** durable intent, atomic local commit, observable backlog, replay, and compatibility with the modular monolith.

**Disadvantages:** dispatcher, leasing, retention, idempotent consumers, and monitoring are required.

### Option B: Publish directly after commit

**Advantages:** minimal schema and lower apparent latency.

**Disadvantages:** process failure can lose required work; recovery depends on ad hoc reconciliation.

### Option C: Distributed transaction with broker

**Advantages:** theoretical atomic coordination.

**Disadvantages:** unsupported or operationally disproportionate for the selected stack and external systems.

### Option D: Periodic full-state reconciliation only

**Advantages:** simple event publication path.

**Disadvantages:** delayed action, expensive scans, and poor causal traceability. Reconciliation remains a secondary safety control.

## 4. Decision

Use a PostgreSQL transactional outbox for business events and follow-up commands whose silent loss would materially affect financial integrity, tenant access, regulatory workflows, customer-visible state, or external reconciliation.

The outbox guarantees durable intent and at-least-once publication, not exactly-once processing. Consumers must be idempotent.

### 4.1 When the outbox is required

Use the outbox when committed local state requires reliable follow-up, including approved cases such as:

- Subscription or entitlement activation consequences.
- Financial posting follow-up and reconciliation.
- E-invoicing submission operations.
- Payment-provider processing and reconciliation.
- Inventory or document workflows whose downstream action must not be lost.
- Critical notifications or exports when loss would create a material obligation.

Routine cache invalidation or non-critical telemetry may use simpler mechanisms when loss is acceptable and documented.

### 4.2 Atomic write

The owning application service writes domain state, audit evidence where required, and the outbox record in the same PostgreSQL transaction. A rolled-back business transaction must not leave a publishable outbox record.

The outbox record references committed facts or requested follow-up. It must not claim an external action succeeded.

### 4.3 Outbox record

The schema must include, as applicable:

- Globally unique event or command identifier.
- Tenant identifier or explicit platform-global classification.
- Owning domain.
- Stable event or command name.
- Schema version.
- Aggregate or operation identifier.
- Correlation and causation identifiers.
- Occurrence and creation timestamps.
- Minimal versioned payload.
- Delivery state, attempt count, next-attempt time, and last safe error summary.
- Claim owner and lease expiry where leasing is used.
- Published timestamp and retention metadata.

Payloads must not duplicate unnecessary sensitive records or secrets.

### 4.4 Dispatcher and claims

One or more dispatchers may claim eligible rows using a concurrency-safe database strategy, such as bounded batches with `FOR UPDATE SKIP LOCKED` and expiring leases. Claims must recover after dispatcher failure.

The dispatcher publishes to the approved Celery/Redis path or invokes the appropriate delivery adapter, then records the publication attempt. A crash after publish but before marking completion can republish; this is expected and must be safe.

### 4.5 Event and command semantics

- An event states that a committed fact occurred.
- A command requests an idempotent action by an identified owner.
- An operation record tracks a business workflow and its authoritative status.

These concepts must not be conflated. Event names use stable domain language and versioned schemas. Consumers must not infer undocumented database structure from payloads.

### 4.6 Consumer idempotency

Consumers must durably record or enforce processed identifiers when duplicate execution could create material effects. Database constraints or operation-state transitions should enforce the invariant where possible.

A critical inbound integration may use an inbox or equivalent deduplication record before acknowledging or processing the message.

### 4.7 Ordering

Global ordering is not guaranteed. If a workflow requires ordering, define the boundary—such as one aggregate or operation—and enforce it through sequence numbers, state preconditions, partitioning, or serialization appropriate to that scope.

Consumers must tolerate duplicates and compatible reordering unless a stronger contract is explicitly documented.

### 4.8 Failure and replay

Transient dispatch failures retry with bounded backoff. Permanent schema, configuration, or authorization failures move to a discoverable terminal state or require operator action.

Replay requires authorization, bounded selection, dry-run or preview where practical, idempotency verification, and audit evidence. Operators must not edit payloads casually to force success.

### 4.9 Reconciliation

Critical workflows require reconciliation between authoritative operation state, outbox state, broker/task state, and external-provider state where applicable. Reconciliation detects events that were delivered but not recorded, stuck outbox rows, inconsistent terminal states, and uncertain external outcomes.

### 4.10 Retention

Retention must support replay, incident investigation, audit obligations, and data minimization. The exact duration is pending operational, legal, and compliance decisions. Archival or deletion must not remove the authoritative business or audit record.

## 5. Rationale

The transactional outbox closes the local dual-write gap using the existing PostgreSQL transaction boundary. It avoids distributed transactions while making required work observable and recoverable. At-least-once publication is practical when identifiers, state transitions, and consumer idempotency are designed explicitly.

## 6. Consequences

### Positive consequences

- Critical follow-up intent survives process and broker failure.
- Publication backlog is queryable and monitorable.
- Replay and reconciliation are controlled.
- Domain transactions remain local to PostgreSQL.

### Negative consequences and trade-offs

- Additional tables, dispatcher processes, cleanup, and alerts.
- Duplicate delivery is normal and must be handled everywhere.
- Payload schemas and compatibility become governed contracts.
- Retention can create significant data volume.

### Risks and mitigations

- **Duplicate external effects:** consumer and provider idempotency plus reconciliation.
- **Stuck claims:** expiring leases and stale-claim recovery.
- **Backlog growth:** age/depth alerts, capacity limits, and operational runbooks.
- **Sensitive payloads:** minimal references and data classification review.
- **Breaking schema evolution:** versioned payloads and tolerant consumers.

## 7. Security and Tenant-Isolation Implications

- Outbox and inbox rows are tenant-owned unless explicitly platform-global.
- Dispatchers and consumers validate tenant ownership rather than trusting payload fields.
- Payload access, replay, and operational inspection require least privilege.
- Logs and retained errors must not disclose secrets or full sensitive documents.
- Cross-tenant batch dispatch must not create cross-tenant business access.

## 8. Data Integrity and Migration

- Business state and outbox intent share one transaction.
- Unique identifiers and state constraints prevent ambiguous delivery records.
- Schema changes must support old queued payloads during deployment overlap.
- Indexes must support eligible-row claims and stale/backlog monitoring.
- Cleanup must be bounded and must preserve required audit and operation records.

## 9. Operational Impact

Monitor unpublished count, oldest age, claim age, attempts, terminal failures, dispatch latency, consumer duplicates, inbox conflicts, and reconciliation mismatches. Runbooks must cover paused dispatch, poison records, replay, schema incompatibility, backlog recovery, and external-provider uncertainty.

## 10. Implementation Requirements

1. Define outbox, inbox where required, and operation-state schemas.
2. Define event naming, ownership, and payload-version conventions.
3. Implement concurrency-safe claims with stale-claim recovery.
4. Publish through the approved task infrastructure.
5. Implement consumer idempotency and duplicate tests.
6. Define terminal failure and authorized replay procedures.
7. Add backlog, age, failure, and reconciliation monitoring.
8. Approve retention and sensitive-data rules before production.

## 11. Validation and Acceptance Criteria

- [ ] Rolled-back business transactions publish no event.
- [ ] Committed critical work leaves durable outbox intent.
- [ ] A crash before, during, or after publish does not lose required work.
- [ ] Duplicate publication and consumption produce no duplicate business effect.
- [ ] Multiple dispatchers do not corrupt claim state.
- [ ] Stale claims recover automatically or through an approved procedure.
- [ ] Tenant context is validated by dispatchers and consumers.
- [ ] Old and new payload versions coexist during supported deployment overlap.
- [ ] Backlog and terminal failures trigger actionable monitoring.
- [ ] Replay and reconciliation are authorized and audited.

## 12. Alternatives Rejected

- Direct broker publication as the only reliability mechanism is rejected.
- `transaction.on_commit()` alone is rejected for critical delivery.
- Exactly-once claims are rejected.
- Global event ordering is rejected as an unnecessary and costly default.
- Broker state is rejected as the authoritative business-operation status.

## 13. References

- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/API_STANDARDS.md`
- PostgreSQL explicit locking: https://www.postgresql.org/docs/current/explicit-locking.html
- PostgreSQL transaction isolation: https://www.postgresql.org/docs/current/transaction-iso.html
- Celery task documentation: https://docs.celeryq.dev/en/stable/userguide/tasks.html

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** PostgreSQL transactional outbox with at-least-once publication and idempotent consumers.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; leases, retry thresholds, retention, and monitoring values remain bounded implementation decisions.

This accepted decision governs critical asynchronous workflows; their implementation remains subject to authorized phase tasks.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial transactional outbox and event-delivery decision accepted after standards review. |
