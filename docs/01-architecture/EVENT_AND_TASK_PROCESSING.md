# Event and Task Processing — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | ARCH-EVT-001 |
| Document | `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md` |
| Version | 1.0 |
| Status | APPROVED — Event and Task Architecture Baseline |
| Last Reviewed | 27 October 2026 |
| Applies To | Django application, Celery workers, scheduled jobs, internal events, external integrations |
| Primary Stack | Django, PostgreSQL, Celery, Redis |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DJANGO_APP_STRUCTURE.md`, `DATABASE_DESIGN.md`, `MULTI_TENANCY.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `MODULE_DEPENDENCIES.md`, `ENTITLEMENT_ENGINE.md`, `API_STANDARDS.md`, `SECURITY_REQUIREMENTS.md`, `TESTING_STRATEGY.md` |

---

# 1. Purpose

This document establishes the architecture and implementation standards for asynchronous processing and event-driven workflows in the UAE ERP SaaS platform.

It defines how the application processes work that should not be performed entirely within an HTTP request or a single database transaction.

The objectives are to ensure that:

- Background tasks execute reliably.
- Business transactions remain consistent.
- Tasks can be retried without duplicating business effects.
- Events are not silently lost between database commits and message publication.
- Tenant context is propagated explicitly and securely.
- Financial operations remain auditable.
- External integrations tolerate timeouts, retries, and uncertain outcomes.
- Scheduled jobs execute predictably.
- Failures can be detected, investigated, and recovered.
- Codex-generated implementations follow consistent patterns.

This document applies to internal asynchronous workflows and external integration processing. It does not require every operation to become an event-driven workflow.

## 1.1 Normative language

- **MUST / MUST NOT:** Mandatory.
- **SHOULD / SHOULD NOT:** Strong recommendation unless a documented exception exists.
- **MAY:** Optional.
- **TBD:** A decision that must be resolved before the affected feature is production-ready.

## 1.2 Scope

This document covers:

1. Synchronous versus asynchronous execution.
2. Celery task architecture.
3. Redis broker and infrastructure considerations.
4. Domain events and integration events.
5. Transactional outbox and inbox patterns.
6. Task idempotency and duplicate delivery.
7. Retry policies and failure classification.
8. Dead-letter and failed-task recovery.
9. Scheduled and periodic tasks.
10. Tenant context propagation.
11. Authorization and entitlement checks.
12. External provider integration.
13. Task status and operational visibility.
14. Logging, monitoring, alerting, and reconciliation.
15. Automated testing and release requirements.

---

# 2. Architectural Principles

## 2.1 Modular monolith first

The application will remain a Django modular monolith unless an approved architectural decision establishes a concrete reason to introduce separately deployed services.

Django modules may publish internal events and execute asynchronous tasks, but these mechanisms do not imply that each module must become a microservice.

The preferred architecture is:

```text
Django Modular Monolith
        |
        +--> Core / Tenants / Users
        |
        +--> Subscriptions / Billing
        |
        +--> CRM / Sales / Invoicing
        |
        +--> Accounting / VAT
        |
        +--> Procurement / Inventory
        |
        +--> HRMS / Payroll
        |
        +--> E-Invoicing / Integrations
        |
        v
PostgreSQL
        |
        +--> Business Records
        +--> Transactional Outbox
        +--> Task and Operation Records
        |
        v
Outbox Dispatcher / Task Publisher
        |
        v
Redis Message Broker
        |
        v
Celery Workers
        |
        +--> Internal Processing
        +--> Scheduled Work
        +--> External Provider Calls
        +--> Reconciliation
```

PostgreSQL is the authoritative source for business state.

Redis is a task-broker and supporting infrastructure component. It MUST NOT become the only durable record of a financial operation or integration submission.

The exact broker and result-backend configuration remains subject to infrastructure and reliability requirements.

## 2.2 Separate business state from processing state

The system MUST distinguish the state of a business resource from the state of a task processing that resource.

For example:

| Business state | Processing state |
|---|---|
| Invoice issued | E-invoicing submission queued |
| Invoice issued | E-invoicing submission running |
| Invoice issued | Provider response pending |
| Invoice issued | Submission accepted |
| Invoice issued | Submission rejected |
| Invoice issued | Submission outcome uncertain |

The invoice's business state and the provider submission's processing state are related but not interchangeable.

A failed task MUST NOT automatically reverse a valid business transaction.

Likewise, a task marked successful MUST NOT imply regulatory acceptance unless the provider's verified response establishes that outcome.

## 2.3 At-least-once processing assumption

The architecture MUST assume that tasks and events may be delivered more than once.

Duplicate delivery can occur because of:

- Worker crashes.
- Broker redelivery.
- Visibility timeouts.
- Network interruptions.
- Publisher retries.
- Outbox dispatcher retries.
- Operator-initiated replay.
- Provider webhook redelivery.
- Deployment interruptions.

Therefore, tasks MUST be idempotent where duplicate execution could create duplicate business effects.

The system MUST NOT rely on an assumption of exactly-once message delivery.

## 2.4 Durable intent

If a committed business transaction requires follow-up work, the application MUST preserve enough durable information to identify and recover that work.

For important workflows, the database transaction SHOULD record both:

1. The business change.
2. The intent to perform the follow-up operation.

The transactional outbox is the preferred mechanism for reliable event publication.

## 2.5 Explicit failure semantics

Every asynchronous workflow MUST define:

- What constitutes success.
- Which failures are retryable.
- Which failures are permanent.
- Whether duplicate execution is safe.
- How an ambiguous external result is reconciled.
- When human intervention is required.
- What the user sees while processing is pending.
- How the workflow is audited.

A generic retry decorator is not sufficient for a financial or regulatory integration workflow.

---

# 3. Processing Model

## 3.1 Synchronous execution

Use synchronous execution when an operation is:

- Short-running.
- Predictable in duration.
- Required to determine the immediate HTTP response.
- Limited to work that can safely complete within the request lifecycle.

Examples include:

- Validating a customer form.
- Checking a user's permission.
- Evaluating module entitlement.
- Reading a single resource.
- Performing a small database update.
- Validating whether an invoice can be issued.

Synchronous execution MUST NOT be used for long-running operations merely because the initial implementation is simpler.

## 3.2 Asynchronous execution

Use asynchronous processing when an operation:

- May take a substantial or unpredictable amount of time.
- Depends on an external provider.
- Processes a large number of records.
- Can be safely resumed or retried.
- Does not need to complete before the user receives an acknowledgement.
- Requires scheduled or repeated execution.

Examples:

- E-invoicing submission.
- Bulk customer import.
- Large report generation.
- Large data exports.
- Email delivery.
- Payment-provider reconciliation.
- Inventory synchronization.
- Subscription provisioning.
- Integration event delivery.
- Scheduled expiry processing.

## 3.3 Processing decision table

| Operation | Preferred approach | Reason |
|---|---|---|
| Validate invoice fields | Synchronous | Immediate validation feedback |
| Save an invoice draft | Synchronous | User expects the saved resource |
| Issue an invoice | Synchronous domain transaction, with asynchronous follow-up where required | Preserve a clear business commit boundary |
| Submit an invoice to an external e-invoicing provider | Usually asynchronous | Provider latency, retries, and uncertain outcomes |
| Generate a small dashboard summary | Synchronous, subject to performance | Immediate user interaction |
| Generate a large report | Asynchronous | Long-running query and file generation |
| Send an email | Asynchronous | External delivery is not part of the core database commit |
| Process a large import | Asynchronous | Chunking, progress tracking, and recovery |
| Update a stock balance from a posted movement | Synchronous within the business transaction where required | Inventory consistency |
| Rebuild an analytical projection | Asynchronous | Derived data can be recomputed |
| Reconcile provider submission statuses | Scheduled asynchronous job | External state may change independently |

The preferred approach may change when the module's consistency requirements demand it. Each exception MUST be documented.

## 3.4 Do not queue work unnecessarily

Not every internal function should be a Celery task.

The application MUST NOT enqueue a separate task for every small internal method.

Avoid asynchronous processing when it introduces:

- Unnecessary eventual consistency.
- More complex failure recovery.
- Extra database queries.
- Difficult-to-debug state transitions.
- Duplicate processing risks without a corresponding benefit.

---

# 4. Celery Architecture

## 4.1 Role of Celery

Celery is the initial task-execution framework for the application.

It is responsible for executing background work, including:

- Asynchronous business workflows.
- Integration requests.
- Scheduled tasks.
- Bulk processing.
- Retryable operations.
- Reconciliation jobs.
- Notifications.

Celery does not replace:

- PostgreSQL business records.
- The transactional outbox.
- Domain services.
- Audit records.
- Business state machines.
- The central entitlement engine.

## 4.2 Broker

Redis is the initial recommended Celery broker.

The broker configuration MUST be environment-specific and must not be hardcoded into source files.

Production broker configuration MUST include appropriate:

- Authentication.
- Network restrictions.
- TLS where required by the deployment architecture.
- Connection timeouts.
- Resource limits.
- Monitoring.
- Persistence and recovery settings appropriate to the workload.

Redis persistence and replication alone MUST NOT be treated as proof that a task has been durably completed.

The application MUST retain durable business intent for critical workflows.

## 4.3 Result backend

The result backend MUST be selected according to actual operational requirements.

Not every task requires a full serialized result to be stored in Redis.

For business-critical operations, a dedicated application-level operation record or domain record SHOULD hold the authoritative processing state.

Celery result records MAY support diagnostics, but they MUST NOT be the only source of truth for:

- Invoice submission outcomes.
- Payment status.
- Subscription provisioning.
- Payroll processing.
- Accounting operations.
- Regulatory evidence.

## 4.4 Worker responsibilities

Celery workers MUST:

- Execute the approved task.
- Validate task input.
- Establish explicit tenant context where required.
- Revalidate relevant resource ownership.
- Invoke application services.
- Use appropriate transaction boundaries.
- Apply retry policies.
- Record processing outcomes.
- Emit structured logs.
- Avoid exposing sensitive information.
- Support safe recovery after process interruption.

Workers MUST NOT directly manipulate business state in ways that bypass domain services.

## 4.5 Worker isolation

The production deployment SHOULD use separate worker queues or worker pools for workloads with materially different resource or reliability requirements.

For example:

```text
celery queue: critical
celery queue: integrations
celery queue: notifications
celery queue: reports
celery queue: maintenance
```

These are proposed queue names, not mandatory names.

The final queue layout MUST reflect measured workloads, task criticality, and infrastructure capacity.

A large report SHOULD NOT be allowed to starve time-sensitive invoice submissions simply because both tasks use the same unconstrained worker pool.

## 4.6 Task registration

Tasks MUST be registered using the project's established Celery configuration.

The project SHOULD use explicit task names that are stable and meaningful.

Example:

```python
@app.task(name="invoicing.process_submission")
def process_submission(submission_id: str) -> None:
    ...
```

The example illustrates naming only. The actual implementation MUST follow the project's installed Celery version and task conventions.

Renaming or removing a task that may already be queued requires compatibility planning.

During rolling deployments, queued tasks may have been created by an older application version. Task contracts MUST be managed accordingly.

---

# 5. Task Design Standards

## 5.1 One task, one clear responsibility

A task SHOULD perform one clearly defined processing responsibility.

Examples:

- Dispatch pending outbox events.
- Submit one e-invoice.
- Generate one export.
- Process one import batch.
- Reconcile one provider transaction.
- Send one notification.

Tasks MAY coordinate multiple application services when the workflow requires it, but complex workflows SHOULD have explicit orchestration and state tracking.

## 5.2 Pass identifiers, not full model objects

Tasks SHOULD receive stable identifiers rather than serialized Django model instances.

Preferred:

```python
process_invoice_submission.delay(
    submission_id=str(submission.id),
    tenant_id=str(tenant.id),
)
```

Avoid:

```python
process_invoice_submission.delay(invoice_model)
```

Passing model instances creates serialization problems and can accidentally include stale or sensitive state.

Task inputs SHOULD contain the minimum required information.

## 5.3 Task arguments

Task arguments MUST be:

- Serializable by the approved serializer.
- Explicitly documented.
- Version-compatible where necessary.
- Free of passwords, access tokens, private keys, and other secrets.
- Limited to the minimum required data.

Do not place full customer, employee, payroll, or financial documents into broker messages unless a documented requirement justifies it.

Prefer durable record identifiers and retrieve authorized data when processing begins.

## 5.4 Task contracts

Every nontrivial task MUST document:

- Task name.
- Owning module.
- Purpose.
- Input parameters.
- Tenant context requirements.
- Authorization requirements.
- Idempotency strategy.
- Retry policy.
- Expected duration.
- Side effects.
- Failure states.
- Observability requirements.
- Recovery mechanism.
- Compatibility requirements.

## 5.5 Task versioning

Queued tasks may survive application deployments.

Changes to task signatures or message semantics MUST account for messages already in the broker.

For incompatible changes, the team SHOULD:

- Introduce a new task name.
- Support both formats during a transition.
- Drain or migrate queued work through an approved procedure.
- Include a payload version where appropriate.
- Remove legacy support only after the compatibility window has closed.

The implementation MUST NOT assume that deploying new code removes all old messages.

---

# 6. Transactional Outbox Pattern

## 6.1 Problem

A common failure occurs when the application commits a database transaction and then publishes a message to Redis.

Example:

```text
1. Invoice is issued in PostgreSQL.
2. Database transaction commits.
3. Application attempts to publish an e-invoicing task.
4. Redis is unavailable.
5. The invoice exists, but the submission task was never queued.
```

A different failure can occur if the message is published before the database transaction commits.

The worker may then receive a message referring to a resource that does not yet exist or whose transaction later rolls back.

## 6.2 Required approach

For critical workflows, the business change and the intent to publish follow-up work MUST be recorded in the same PostgreSQL transaction.

The recommended pattern is:

```text
Application Service
        |
        v
BEGIN DATABASE TRANSACTION
        |
        +--> Validate business operation
        |
        +--> Update business records
        |
        +--> Insert audit records where required
        |
        +--> Insert outbox event
        |
        v
COMMIT
        |
        v
Outbox Dispatcher
        |
        v
Publish Task / Event
        |
        v
Mark Outbox Event as Published
```

The dispatcher may crash after publishing but before recording the publication. Therefore, duplicate publication MUST be expected.

Consumers MUST be idempotent.

## 6.3 When the outbox is required

The transactional outbox SHOULD be mandatory when a committed transaction creates a durable obligation to initiate external or asynchronous work.

Examples include:

- Issuing an invoice and initiating e-invoicing submission.
- Committing a subscription change and provisioning entitlements.
- Recording a payment initiation and dispatching the provider request.
- Committing an integration synchronization change.
- Recording a business event that must be delivered to another subsystem.
- Scheduling a required notification whose omission would violate the approved workflow.

Not every internal task needs an outbox.

Simple noncritical work MAY use Django's `transaction.on_commit()` to avoid dispatching a task before a transaction commits.

However, `transaction.on_commit()` alone does not provide durable publication if the process crashes after the database commit and before the callback successfully publishes the task.

It MUST NOT be treated as equivalent to a transactional outbox.

## 6.4 Conceptual outbox model

The outbox model SHOULD include fields equivalent to:

| Field | Purpose |
|---|---|
| `id` | Unique event identifier |
| `tenant_id` | Tenant context where applicable |
| `event_type` | Stable event type |
| `event_version` | Event schema version |
| `aggregate_type` | Related business resource type |
| `aggregate_id` | Related business resource identifier |
| `payload` | Minimal event data |
| `correlation_id` | Workflow correlation identifier |
| `causation_id` | Identifier of the event or command that caused this event |
| `occurred_at` | Event creation timestamp |
| `available_at` | Earliest dispatch time |
| `published_at` | Successful publication timestamp, where known |
| `attempt_count` | Publication attempt count |
| `status` | Dispatch state |
| `last_error_code` | Sanitized last error classification |
| `created_at` | Record creation timestamp |

The final model MUST follow the approved database design.

The payload MUST NOT contain secrets or unnecessary sensitive personal information.

## 6.5 Outbox state machine

A possible state machine is:

```text
PENDING
   |
   v
PROCESSING
   |
   +--> PUBLISHED
   |
   +--> PENDING (retry scheduled)
   |
   +--> FAILED (manual intervention or terminal failure)
```

An expired processing lease may return the event to a retryable state.

The exact states and lease strategy MUST be defined in the implementation.

## 6.6 Concurrent dispatchers

Multiple outbox dispatchers may run concurrently.

The dispatcher MUST prevent unsafe concurrent claiming of the same event.

Suitable approaches include:

- PostgreSQL row locking.
- `SELECT ... FOR UPDATE SKIP LOCKED`, where appropriate.
- A lease or claim token.
- A database-backed state transition with conditional updates.

The implementation MUST account for process crashes while an event is claimed.

A permanently stuck processing record MUST be recoverable after its lease expires or through a controlled operational procedure.

## 6.7 Publication semantics

An outbox event marked as published means that the configured publication mechanism accepted the event according to the application's publication contract.

It does not necessarily mean that:

- A consumer completed processing.
- An external provider accepted a transaction.
- An invoice was accepted by a regulatory network.
- A notification was delivered to its recipient.

The system MUST distinguish publication from downstream completion.

## 6.8 Event ordering

The system MUST NOT assume global ordering across all outbox events.

Where ordering matters for a particular business resource, the implementation MUST define and enforce an appropriate ordering strategy.

For example, a sequence of financial state transitions for one invoice may need ordered processing even though unrelated invoices can be processed concurrently.

The team SHOULD prefer explicit aggregate versions, sequence numbers, or conditional state transitions over relying solely on task arrival order.

---

# 7. Internal Events and Integration Events

## 7.1 Event definitions

An event records that something happened.

Examples:

- `invoice.issued`
- `invoice.voided`
- `journal.posted`
- `stock.receipt.completed`
- `subscription.activated`
- `subscription.expired`
- `einvoicing.submission.accepted`
- `payment.reconciled`

Event names MUST reflect established domain terminology.

The final event catalogue MUST be maintained with the relevant modules.

## 7.2 Commands versus events

A command requests an action.

An event records an outcome or occurrence.

Examples:

| Command | Event |
|---|---|
| Issue invoice | Invoice issued |
| Submit e-invoice | E-invoice submission requested |
| Post journal | Journal posted |
| Activate module | Module entitlement activated |
| Reconcile payment | Payment reconciled |

The system MUST NOT label an uncompleted request as a completed event.

## 7.3 Domain events

Domain events describe significant occurrences within the application domain.

They MAY be handled synchronously within the same transaction when immediate consistency is required.

They MAY also produce outbox records for reliable asynchronous follow-up.

The team MUST NOT use events to avoid defining ownership of a business operation.

## 7.4 Integration events

Integration events are intended for delivery outside the immediate application boundary or to a separate integration component.

They SHOULD have explicit, versioned payload contracts.

Internal Django model structures MUST NOT be exposed directly as integration event schemas.

Integration event payloads MUST contain only the data required by the consumer.

## 7.5 Event schema

A standard event envelope SHOULD contain:

```json
{
  "event_id": "a3e7e57b-3b70-4db4-9f19-0a8a0c43c6a0",
  "event_type": "invoice.issued",
  "event_version": 1,
  "occurred_at": "2026-10-27T10:30:00Z",
  "tenant_id": "tenant-uuid",
  "aggregate_type": "invoice",
  "aggregate_id": "invoice-uuid",
  "correlation_id": "correlation-uuid",
  "causation_id": null,
  "data": {
    "invoice_id": "invoice-uuid"
  }
}
```

All identifiers and values are illustrative.

Rules:

- `event_id` MUST be unique.
- `event_type` MUST be stable and documented.
- `event_version` MUST identify the event payload schema.
- `occurred_at` MUST contain an explicit timezone.
- Tenant context MUST be included where relevant.
- `aggregate_id` MUST identify the affected resource without exposing unnecessary internal data.
- `correlation_id` SHOULD connect related processing steps.
- `causation_id` SHOULD identify the preceding command or event where applicable.
- `data` MUST be validated against the event contract.

The envelope MUST NOT include authentication credentials or unnecessary personal data.

## 7.6 Event compatibility

Changes to published event schemas MUST consider consumers that may still be processing older messages.

Adding an optional field is generally compatible.

Removing a field, changing its type, or changing its meaning may be breaking.

Breaking event changes MUST use an approved versioning or migration strategy.

The consumer MUST NOT assume every event was produced by the latest application version.

## 7.7 Avoid event proliferation

The application MUST NOT generate events for every model save without a defined business purpose.

Events SHOULD represent meaningful domain occurrences rather than low-level implementation details.

Unnecessary events increase operational complexity, storage usage, and debugging difficulty.

---

# 8. Consumer Inbox and Duplicate Protection

## 8.1 Purpose

An outbox protects reliable publication of work.

An inbox or equivalent idempotency record protects reliable processing of received events.

The application SHOULD use a durable inbox for critical inbound events when duplicate processing could create incorrect business effects.

Examples include:

- Payment-provider callbacks.
- E-invoicing provider callbacks.
- External order synchronization.
- Integration event consumption.
- External financial transaction notifications.

## 8.2 Conceptual inbox model

An inbox record SHOULD include:

- Provider or source identifier.
- External event identifier.
- Tenant or integration scope.
- Event type.
- Payload fingerprint where appropriate.
- Receipt timestamp.
- Processing status.
- Processing attempt count.
- Completion timestamp.
- Correlation identifier.
- Sanitized error classification.

A database uniqueness constraint MUST prevent the same external event from being processed as a new event within the same defined scope.

## 8.3 Duplicate delivery

When the same event is received more than once:

1. Authenticate the sender.
2. Validate the payload.
3. Identify the event using the approved deduplication key.
4. Determine whether the event has already been processed or is in progress.
5. Avoid repeating the completed business effect.
6. Return the appropriate acknowledgement according to the integration contract.

The application MUST distinguish a duplicate delivery from a different event that happens to contain similar data.

## 8.4 Inbox processing states

Possible states include:

```text
RECEIVED
PROCESSING
PROCESSED
RETRY_PENDING
FAILED
```

The exact states may differ according to the provider and business workflow.

The implementation MUST define recovery for interrupted processing.

A record left in `PROCESSING` MUST NOT remain stuck indefinitely without detection or recovery.

## 8.5 Provider event versus business state

A provider event is evidence from an external system. It is not automatically authoritative for every internal field.

The integration adapter MUST validate the event and map it to an approved internal state transition.

Unexpected, stale, contradictory, or out-of-order provider events MUST be handled according to a documented policy.

The application MUST NOT blindly overwrite business state based only on the latest-arriving webhook.

---

# 9. Task Idempotency

## 9.1 Mandatory principle

A task that can be retried or delivered more than once MUST be designed so that duplicate execution does not create duplicate business effects.

Idempotency MUST be implemented at the appropriate business-operation boundary, not merely by checking a boolean task flag.

## 9.2 Common strategies

Depending on the operation, idempotency may use:

- A unique business-operation identifier.
- A database uniqueness constraint.
- An outbox event identifier.
- An inbox event identifier.
- A provider idempotency key.
- A durable operation record.
- A conditional state transition.
- A transaction that records both the result and the deduplication key.

A task SHOULD use the strongest practical combination for its failure model.

## 9.3 Example: invoice submission

Consider an invoice that must be submitted to an external e-invoicing provider.

The implementation SHOULD:

1. Create a durable submission record.
2. Associate it with the tenant and invoice.
3. Record the intended provider and operation.
4. Generate or retrieve the stable provider idempotency key, where supported.
5. Queue processing through the approved outbox mechanism.
6. Before sending, inspect the current submission state.
7. Prevent concurrent workers from initiating the same logical submission.
8. Send the request using the provider's documented idempotency mechanism where available.
9. Persist the response or an uncertain-outcome state.
10. Reconcile ambiguous outcomes before attempting another non-idempotent submission.

If the provider does not support idempotency, the adapter MUST define a safe reconciliation strategy before production use.

## 9.4 Do not rely on Celery task IDs alone

A Celery task ID is not a sufficient business idempotency mechanism.

The same logical operation may be queued under different task IDs.

The application MUST use a durable business identifier or deduplication key that survives task rescheduling and replay.

## 9.5 Idempotency scope

Idempotency keys MUST be scoped to the appropriate combination of:

- Tenant.
- Business operation.
- Resource or transaction.
- External provider or integration, where relevant.

The same key used by two unrelated tenants MUST NOT cause one tenant's operation to suppress another tenant's legitimate operation.

---

# 10. Retry Policies

## 10.1 Retry principle

Retries MUST be bounded, observable, and based on failure classification.

The application MUST NOT retry every exception indiscriminately.

Retries are appropriate when the failure is transient and the operation is safe to repeat or can be reconciled before retrying.

## 10.2 Failure classification

Failures SHOULD be classified into the following categories.

### A. Transient infrastructure failure

Examples:

- Temporary database connectivity issue.
- Redis connection interruption.
- Network timeout.
- Temporary provider unavailability.
- HTTP 429 response where the provider's contract allows retry.

Action:

- Retry with bounded backoff.
- Respect `Retry-After` where applicable.
- Preserve the operation's idempotency guarantees.
- Record the attempt.

### B. Permanent validation failure

Examples:

- Invalid payload.
- Missing mandatory business field.
- Unsupported document type.
- Invalid configuration.
- Business rule violation.

Action:

- Do not retry automatically without changing the input or configuration.
- Record a clear failure reason.
- Expose the error to the appropriate user or operator.
- Allow correction and controlled reprocessing where appropriate.

### C. Authorization or entitlement failure

Examples:

- Required permission no longer exists.
- Required module entitlement is unavailable.
- Tenant is suspended under the applicable policy.

Action:

- Do not blindly retry.
- Apply the approved policy for the affected workflow.
- Preserve business records and evidence.
- Re-evaluate authorization or entitlement when the operation is resumed.
- Escalate when business obligations cannot be safely deferred.

### D. External outcome uncertain

Examples:

- Provider accepts a request but the response is lost.
- Network timeout occurs after request transmission.
- Worker crashes after an external side effect but before persisting its result.

Action:

- Do not assume failure.
- Mark the operation as uncertain or reconciliation-required.
- Query the provider or use its idempotency mechanism.
- Resume processing only when duplicate effects can be prevented.

### E. Permanent provider rejection

Examples:

- Provider rejects a structurally invalid document.
- Provider returns a terminal business rejection.
- A document cannot be processed under the provider's validated rules.

Action:

- Persist the rejection evidence.
- Map the response to the approved internal state.
- Do not retry unchanged input indefinitely.
- Allow correction and resubmission only through the approved workflow.

## 10.3 Backoff

Retry policies SHOULD use exponential backoff with jitter for transient failures.

A conceptual schedule might be:

```text
Attempt 1: immediate
Attempt 2: short delay
Attempt 3: longer delay
Attempt 4: progressively longer delay
Final automatic attempt: bounded by task policy
```

Actual delays and attempt limits MUST be configured per task category.

The system MUST NOT use unlimited automatic retries for business-critical tasks.

## 10.4 Example policy

The following is an initial proposal, not a universal requirement.

| Task category | Retry policy | Terminal handling |
|---|---|---|
| Critical outbox dispatch | Bounded exponential backoff; continue monitoring pending events | Alert and retain pending event |
| E-invoicing submission | Provider-specific bounded retry plus reconciliation | Persist rejection or uncertain state |
| Payment-provider request | Provider-specific retry and status lookup | Reconcile before any repeat financial action |
| Email delivery | Bounded retry for transient failures | Mark failed and allow controlled resend |
| Bulk import | Retry eligible chunks independently | Record row-level and batch-level failures |
| Report generation | Limited retry for transient infrastructure failures | Mark operation failed with safe diagnostics |
| Subscription provisioning | Idempotent retry | Reconcile desired and actual entitlement state |
| Scheduled maintenance | Task-specific retry | Alert if critical maintenance remains incomplete |

## 10.5 Retry configuration

Retry settings MUST be centralized or explicitly declared by task category.

Each retryable task MUST define:

- Maximum attempts or bounded retry duration.
- Initial delay.
- Maximum delay.
- Backoff strategy.
- Retryable exception categories.
- Terminal failure behavior.
- Alerting threshold.
- Manual recovery procedure.

Do not copy arbitrary retry values into unrelated tasks.

## 10.6 Retry storms

The application MUST avoid uncontrolled retry storms during a prolonged outage.

Appropriate safeguards include:

- Exponential backoff.
- Jitter.
- Maximum retry limits.
- Queue isolation.
- Provider-level concurrency limits.
- Circuit breakers where justified.
- Pausing nonessential work during a severe dependency outage.

The system SHOULD preserve critical business work while reducing pressure on a failing dependency.

---

# 11. Dead-Letter Handling and Failed Tasks

## 11.1 Purpose

Tasks that exhaust automatic retries MUST remain discoverable and recoverable.

A failed task MUST NOT simply disappear from the system without an operational record.

## 11.2 Durable failure records

For business-critical workflows, the application SHOULD maintain a durable failure or operation record containing:

- Operation identifier.
- Tenant identifier where applicable.
- Business resource reference.
- Task or event type.
- Current processing state.
- Attempt count.
- Last attempt timestamp.
- Next retry timestamp where applicable.
- Sanitized error code.
- Safe error summary.
- Correlation identifier.
- Recovery status.

The exact model may be a task-operation table, outbox record, inbox record, provider-submission record, or a combination of domain-owned records.

The application SHOULD avoid creating a separate generic failure table when existing durable records already provide the required operational visibility.

## 11.3 Dead-letter queue versus durable failure state

A dedicated dead-letter queue MAY be introduced if supported and justified by the chosen infrastructure.

However, the presence of a broker dead-letter queue does not replace durable application-level failure tracking.

A broker may lose, expire, or purge messages under some operational conditions.

The application MUST be able to identify business operations that remain incomplete independently of transient broker state.

## 11.4 Manual retry

Manual retry MUST be a controlled operation.

Before retrying, the operator or authorized application workflow MUST determine:

- Whether the business operation is still valid.
- Whether the tenant is still eligible.
- Whether required module entitlements are satisfied.
- Whether the resource is in a retryable state.
- Whether an external side effect may already have occurred.
- Whether reconciliation is required first.
- Whether the retry could duplicate a financial or regulatory effect.

Manual retry MUST use the same application services and idempotency mechanisms as automatic execution.

It MUST NOT create a bypass around normal authorization or validation.

## 11.5 Manual recovery permissions

Recovery actions MUST be restricted to authorized operational roles.

Tenant users MAY be allowed to retry certain business operations, but only where the module specification explicitly permits it.

Platform operators MUST NOT automatically gain unrestricted access to tenant financial data merely because they can manage task execution.

Sensitive recovery actions MUST be audited.

## 11.6 Recovery runbooks

Critical workflows MUST have documented procedures for:

- Identifying failed work.
- Determining whether the operation completed externally.
- Correcting invalid configuration or data.
- Requeueing work safely.
- Reconciling the resulting state.
- Recording the operator action.
- Confirming that the backlog has cleared.

---

# 12. Scheduled and Periodic Tasks

## 12.1 Scheduling mechanism

The platform SHOULD use Celery Beat or another explicitly approved scheduling mechanism for recurring tasks.

Only one authoritative scheduler SHOULD control a given schedule unless duplicate execution is intentionally supported.

Running multiple unsynchronized schedulers MUST NOT cause critical financial or provisioning operations to execute multiple times unintentionally.

## 12.2 Scheduled task registry

Every scheduled task MUST have a documented registry entry.

The registry SHOULD include:

| Field | Description |
|---|---|
| Task name | Stable task identifier |
| Owning module | Responsible module |
| Purpose | Business or operational objective |
| Schedule | Cron or interval definition |
| Timezone | Timezone used to interpret the schedule |
| Tenant scope | Global, tenant-specific, or explicitly bounded |
| Idempotency | Duplicate-execution strategy |
| Retry policy | Failure and retry behavior |
| Expected duration | Operational expectation |
| Overlap policy | Whether concurrent runs are allowed |
| Failure alert | How missed or failed runs are detected |
| Recovery procedure | How incomplete work is repaired |

## 12.3 Timezone handling

The application MUST distinguish between:

- UTC timestamps.
- Tenant-local business dates.
- Tenant-local schedules.
- Provider-defined timezones.

A task that is intended to run at a tenant-local time MUST use the approved timezone policy.

The application MUST NOT assume that all tenants use the same timezone.

For schedules tied to business dates, the task MUST define how daylight-saving changes are handled where applicable.

## 12.4 Scheduled task examples

Potential scheduled tasks include:

- Subscription expiry evaluation.
- Entitlement reconciliation.
- Outbox dispatch.
- Provider status reconciliation.
- Payment reconciliation.
- Pending import recovery.
- Stale-operation detection.
- Report cleanup.
- Backup verification.
- Operational health checks.

The exact schedule MUST be approved according to business and operational requirements.

## 12.5 Missed schedules

The system MUST define behavior when a scheduled task is missed because of downtime.

Possible strategies include:

- Run once after recovery.
- Process each missed period.
- Skip obsolete periods.
- Reconstruct work from durable business records.

The correct strategy depends on the task.

A missed report-cleanup run and a missed subscription-expiry evaluation do not necessarily require the same behavior.

## 12.6 Overlapping executions

Scheduled tasks MUST define whether overlapping runs are allowed.

If overlap is unsafe, the implementation MUST use a shared coordination mechanism or database-backed claim strategy.

A process-local lock is insufficient when multiple workers or application instances can execute the task.

The lock or lease MUST have a recovery strategy if the worker crashes.

## 12.7 Tenant fan-out

A global scheduled task that processes many tenants MUST:

- Enumerate eligible tenants through an approved query.
- Process tenants in bounded batches.
- Establish explicit tenant context for each unit of work.
- Isolate failures between tenants where possible.
- Avoid a single tenant failure aborting all unrelated tenant processing.
- Record progress and outcomes.
- Support safe resumption.

A tenant-specific task MUST NOT silently switch to another tenant during processing.

---

# 13. Tenant Context and Authorization

## 13.1 Explicit context

Every tenant-scoped task MUST receive or derive its tenant context through an approved, verifiable mechanism.

The preferred approach is to pass stable tenant and resource identifiers, then validate their relationship when the task begins.

Example:

```python
process_subscription_change(
    tenant_id=tenant_id,
    subscription_id=subscription_id,
)
```

The values are identifiers, not proof of authorization.

## 13.2 Context lifecycle

Tenant context MUST be established for the task's execution scope and cleared afterward.

The implementation MUST NOT rely on an HTTP request being present.

It MUST NOT leave tenant-specific context in thread-local, task-local, connection-local, or other reusable execution state where a subsequent task could inherit it incorrectly.

If PostgreSQL RLS is used, tenant context MUST be set and reset according to the approved database connection and transaction strategy.

## 13.3 Ownership validation

Before processing a resource, the task MUST verify that the resource belongs to the expected tenant.

For example:

```python
submission = InvoiceSubmission.objects.get(
    id=submission_id,
    tenant_id=tenant_id,
)
```

This is illustrative. The actual query MUST follow the established tenant-aware data-access pattern.

A task MUST NOT retrieve a resource globally by ID and assume that the caller supplied the correct tenant.

## 13.4 Authorization re-evaluation

Authorization and entitlement may change between task scheduling and execution.

The task MUST determine which policy applies at execution time.

For example, the application may need to revalidate:

- Tenant status.
- Subscription state.
- Module entitlement.
- Integration credential status.
- Required user or service permissions.
- Resource lifecycle.
- Approval state.

The exact rule depends on the business obligation.

A previously authorized task MUST NOT automatically bypass current controls.

## 13.5 Platform-level tasks

Some tasks legitimately operate across tenants, such as:

- Subscription reconciliation.
- Global outbox maintenance.
- Platform health checks.
- Expired temporary-file cleanup.

Such tasks MUST use explicit platform-level authorization and scope.

They MUST NOT obtain cross-tenant access by disabling tenant filtering indiscriminately.

---

# 14. Entitlements and Module Dependencies

## 14.1 Central entitlement engine

All relevant tasks MUST use the central entitlement engine defined in:

`docs/01-architecture/ENTITLEMENT_ENGINE.md`

A task MUST NOT implement an independent subscription or entitlement calculation.

## 14.2 Scheduling versus execution

The system MUST distinguish between a task being scheduled and a task being permitted to execute.

A task may be queued while the module is entitled, then execute after the entitlement changes.

The task MUST evaluate the approved policy before performing protected work.

## 14.3 In-flight operations

Entitlement changes MUST NOT cause the system to discard important business evidence or corrupt an operation already in progress.

For each module, the specification MUST define how entitlement changes affect:

- New operations.
- Queued operations.
- Running operations.
- External submissions.
- Reconciliation.
- Access to historical records.
- Recovery of previously failed work.

For example, an issued invoice may need to retain a durable e-invoicing submission record even if the tenant's subscription later changes.

Whether the submission may proceed must follow the approved contractual, legal, and operational policy.

## 14.4 Dependency failures

If a task depends on another module or integration, the task MUST handle missing dependencies explicitly.

Examples:

- A payroll task requires an eligible HRMS configuration.
- An e-invoicing submission requires the relevant invoicing capability and provider configuration.
- A stock valuation task requires valid inventory records.
- A reporting job requires permission to access its source modules.

The task MUST NOT assume that dependency configuration remains valid indefinitely.

---

# 15. Financial and Regulatory Workflows

This section establishes additional safeguards for financial and regulatory tasks.

## 15.1 Invoice issuance

Issuing an invoice MUST use an explicit application service and database transaction.

The transaction MUST preserve the required invoice state, numbering rules, audit evidence, and related accounting obligations according to the approved invoicing and accounting design.

If follow-up asynchronous processing is required, the durable intent MUST be recorded as part of the business transaction.

## 15.2 E-invoicing submission

An e-invoicing submission workflow SHOULD distinguish at least these concepts:

- Submission intent recorded.
- Submission queued.
- Submission in progress.
- Provider request sent.
- Provider response received.
- Provider acceptance or rejection.
- Submission outcome uncertain.
- Reconciliation required.
- Retry or correction required.

The final states MUST follow the validated provider contract and regulatory requirements.

The application MUST preserve the evidence required by the approved compliance design.

A timeout MUST NOT be interpreted automatically as a rejection.

A generic task failure MUST NOT be treated as proof that the provider did not receive the document.

## 15.3 Accounting

Tasks affecting accounting MUST preserve double-entry integrity and the approved posting rules.

The application MUST NOT allow an asynchronous task to bypass journal validation, period restrictions, or posting controls.

Posted entries MUST NOT be silently overwritten during retry or replay.

If a task generates accounting entries, the operation MUST be protected against duplicate posting.

## 15.4 Inventory

Inventory tasks MUST distinguish between:

- A request to move stock.
- A committed stock movement.
- A derived stock balance update.
- An external inventory synchronization.

The authoritative stock movement and its required quantity effects MUST follow the approved inventory transaction model.

Repeated execution MUST NOT duplicate a receipt, issue, transfer, or adjustment.

## 15.5 Payroll

Payroll tasks MUST follow the approved payroll lifecycle and access policy.

Examples include payroll calculation, payslip generation, payment-file generation, and payroll reconciliation.

The system MUST protect employee data and payroll amounts.

A retry MUST NOT create duplicate payroll runs, duplicate payment instructions, or duplicate finalized accounting entries.

## 15.6 Payments

Payment initiation and reconciliation MUST use durable operation identifiers and provider-specific idempotency or reconciliation controls.

A network timeout after a payment request MUST be treated as an uncertain outcome unless the provider's documented behavior proves otherwise.

The system MUST NOT initiate a second payment solely because the first HTTP request timed out.

## 15.7 Regulatory assumptions

The implementation MUST NOT invent provider behavior, regulatory deadlines, government APIs, or acceptance semantics.

Provider-specific and UAE regulatory requirements MUST be validated against authoritative documentation before production release.

---

# 16. Task Operations and Status Tracking

## 16.1 Business operation records

For user-visible or business-critical asynchronous workflows, the platform SHOULD maintain an application-level operation record.

This record allows the system to track the workflow independently of a Celery task ID.

Potential fields include:

| Field | Purpose |
|---|---|
| `id` | Stable operation identifier |
| `tenant_id` | Tenant scope where applicable |
| `operation_type` | Business operation type |
| `resource_type` | Related resource type |
| `resource_id` | Related resource identifier |
| `status` | Current operation state |
| `progress_current` | Completed work units where meaningful |
| `progress_total` | Expected work units where meaningful |
| `attempt_count` | Processing attempts |
| `started_at` | Execution start |
| `completed_at` | Completion timestamp |
| `correlation_id` | Workflow correlation |
| `error_code` | Safe failure classification |
| `created_by` | Initiating user or integration where applicable |

This is a conceptual model. The final implementation MUST avoid duplicating state already owned by domain-specific records.

## 16.2 Status accuracy

The application MUST distinguish:

- Queued.
- Running.
- Completed.
- Failed.
- Cancelled.
- Awaiting external response.
- Awaiting reconciliation.
- Requires manual intervention.

Not every workflow requires every state.

The operation's status MUST reflect its actual business and processing condition.

## 16.3 Progress reporting

Progress SHOULD be provided for large imports, exports, and batch operations where it is useful to the user.

Progress values MUST be meaningful.

The application MUST NOT report 100% completion before all required work has completed successfully.

## 16.4 Cancellation

Cancellation behavior MUST be defined per task type.

A cancellation request may stop future processing, but it cannot necessarily undo an external side effect that has already occurred.

For example, cancelling a task after a payment provider has accepted a payment request does not cancel the payment itself.

Cancellation MUST be implemented through a controlled state transition, not by assuming that deleting a Celery message reverses the operation.

## 16.5 Retention

Task operation records, outbox events, inbox events, and processing evidence MUST follow an approved retention policy.

Retention MUST distinguish ordinary technical logs from business and regulatory records.

Critical financial or regulatory evidence MUST NOT be deleted merely because a task has completed.

---

# 17. Observability and Monitoring

## 17.1 Required observability

The production environment MUST provide visibility into:

- Queue depth.
- Oldest pending task age.
- Task execution duration.
- Task success and failure rates.
- Retry counts.
- Outbox backlog.
- Outbox publication failures.
- Stale processing leases.
- Dead-letter or terminal-failure counts.
- Integration timeouts.
- Provider rejection rates.
- Inbox processing failures.
- Reconciliation backlog.
- Scheduled-task execution status.
- Worker availability.
- Broker availability.

The final monitoring system is an infrastructure decision.

## 17.2 Correlation identifiers

Every important asynchronous workflow SHOULD have a correlation identifier.

The identifier SHOULD propagate through:

```text
HTTP Request
    |
    v
Application Service
    |
    v
Database Transaction
    |
    v
Outbox Event
    |
    v
Celery Task
    |
    v
Provider Request
    |
    v
Provider Callback
    |
    v
Reconciliation
```

Where a provider supports a reference or correlation field, the integration MAY propagate a suitable identifier.

Do not send internal identifiers to a provider unless the provider contract and security policy permit it.

## 17.3 Structured logging

Task logs SHOULD include:

- Task name.
- Celery task ID.
- Business operation ID.
- Correlation ID.
- Tenant identifier where permitted.
- Resource type and identifier.
- Attempt number.
- Duration.
- Outcome.
- Error classification.

Logs MUST NOT contain passwords, API secrets, private keys, access tokens, or unnecessary sensitive payloads.

## 17.4 Alerting

Alerts SHOULD be based on operational impact rather than individual transient failures alone.

Examples of useful alert conditions:

- Critical outbox backlog exceeds the approved threshold.
- A required scheduled task has not completed within its expected window.
- Provider submissions remain uncertain beyond the allowed period.
- A payment reconciliation backlog is growing.
- A worker queue remains saturated.
- Failed task rates exceed the approved threshold.
- A critical integration is unavailable.
- Repeated database or broker connection failures occur.
- Tenant entitlement reconciliation is incomplete.

Thresholds MUST be established during deployment planning and adjusted using production observations.

## 17.5 Tenant-aware diagnostics

Operators MUST be able to identify which tenant and business operation are affected, subject to access controls.

Monitoring interfaces MUST NOT expose sensitive tenant information to unauthorized users.

Operational dashboards SHOULD aggregate data where detailed tenant records are unnecessary.

---

# 18. Security Requirements

## 18.1 Task messages are untrusted inputs

Even if task messages are produced internally, the worker MUST validate identifiers and inputs.

A task MUST NOT treat a message payload as proof of authorization.

## 18.2 Broker security

The production broker MUST be protected through appropriate:

- Network isolation.
- Authentication.
- Access controls.
- TLS where required.
- Secret management.
- Monitoring.
- Resource limits.

Broker access MUST NOT be publicly exposed without an explicitly approved architecture and appropriate controls.

## 18.3 Serialization

The application SHOULD use JSON serialization for task messages.

It MUST NOT enable unsafe deserialization of arbitrary Python objects from an untrusted or insufficiently protected broker.

Pickle-based task serialization MUST NOT be enabled merely for convenience.

## 18.4 Secrets

Secrets MUST be retrieved through the approved configuration or secret-management mechanism.

Tasks MUST NOT contain credentials in:

- Source code.
- Hardcoded constants.
- Persistent message payloads.
- Logs.
- Error messages.
- Unprotected task results.

## 18.5 Data minimization

Task messages MUST contain only the data needed to identify and process the operation.

Sensitive data SHOULD be loaded from the authoritative data store after authorization and tenant validation.

## 18.6 Least privilege

Workers SHOULD have only the database and external-system permissions required for their assigned workload.

If separate worker pools are used, access to sensitive tasks and credentials SHOULD be restricted accordingly.

## 18.7 Replay protection

Externally triggered operations MUST have appropriate replay protection.

Replay handling MUST be compatible with legitimate provider retries.

The application MUST NOT reject all duplicate callbacks indiscriminately if a provider legitimately retries delivery.

Instead, it MUST acknowledge already-processed events without repeating their business effects.

---

# 19. Performance and Capacity Planning

## 19.1 Queue isolation

Tasks with different latency and resource characteristics SHOULD be separated when they interfere with one another.

Examples:

- Short operational tasks.
- External provider calls.
- Large report generation.
- Bulk data imports.
- Scheduled maintenance.

The final number of queues and worker pools MUST be justified by measured workload requirements.

## 19.2 Bounded batches

Large jobs MUST process records in bounded batches.

A bulk import SHOULD NOT load an unlimited number of records into memory.

A global reconciliation task SHOULD NOT query and lock all tenant records at once.

## 19.3 Database connection management

Worker concurrency MUST be sized with regard to:

- Available PostgreSQL connections.
- Query duration.
- Lock contention.
- Memory usage.
- External provider rate limits.
- Celery worker concurrency.
- Web application workload.

Increasing worker concurrency without evaluating database capacity is prohibited for production tuning.

## 19.4 Long-running tasks

Long-running tasks SHOULD record progress and checkpoints where appropriate.

A task MUST define whether a worker interruption requires:

- Restarting the entire operation.
- Resuming from the last committed checkpoint.
- Retrying only failed items.
- Reconciling partially completed work.

The selected approach MUST preserve idempotency and data integrity.

## 19.5 Backpressure

The system SHOULD apply backpressure when downstream systems cannot process incoming work at the required rate.

Possible controls include:

- Queue prioritization.
- Bounded concurrency.
- Per-provider concurrency limits.
- Rate-limited dispatch.
- Batch sizing.
- Delayed retries.
- Pausing noncritical work.

The platform MUST NOT allow an integration outage to create an unbounded retry storm or uncontrolled resource exhaustion.

---

# 20. Testing Strategy

All event and task processing implementations MUST have automated tests appropriate to their failure modes.

## 20.1 Unit tests

Unit tests SHOULD cover:

- Task input validation.
- Failure classification.
- Retry eligibility.
- Event serialization.
- Event schema validation.
- Provider status mapping.
- Idempotency decision logic.
- Operation state transitions.
- Error classification.
- Scheduled task business rules.

## 20.2 Transactional outbox tests

Tests MUST verify:

1. The business transaction creates the required outbox event.
2. The business transaction and outbox record commit together.
3. A rollback does not leave an event for a transaction that never committed.
4. The dispatcher publishes pending events.
5. Publication failures leave events recoverable.
6. Concurrent dispatchers do not corrupt event state.
7. Dispatcher crashes do not permanently strand events.
8. Duplicate publication does not create duplicate business effects.
9. Stale processing claims can be recovered.

## 20.3 Idempotency tests

Tests MUST verify:

- Duplicate task delivery.
- Duplicate provider callback delivery.
- Reuse of the same business-operation identifier.
- Concurrent execution of the same logical operation.
- Retry after an ambiguous external outcome.
- Safe replay of failed operations.
- Correct handling of duplicate business requests.

## 20.4 Tenant isolation tests

Tests MUST verify that:

- A task cannot access another tenant's resource by changing its identifier.
- Tenant context is established and cleared correctly.
- RLS context, where enabled, does not leak between tasks.
- A global task uses its approved platform-level scope.
- One tenant's failure does not cause another tenant's records to be processed incorrectly.
- Tenant-specific credentials cannot be used outside their approved scope.

## 20.5 Retry tests

Tests MUST verify that:

- Transient failures are retried according to policy.
- Permanent validation failures are not retried indefinitely.
- Maximum retry limits are respected.
- Retry delays and provider `Retry-After` behavior are handled where required.
- Terminal failures are recorded.
- Retried operations preserve idempotency.
- A timeout after an external side effect triggers reconciliation when required.

## 20.6 Financial tests

Financial task tests MUST verify:

- No duplicate invoice issuance.
- No duplicate accounting posting.
- No duplicate payment initiation.
- No duplicate stock movements.
- No duplicate payroll finalization.
- Correct handling of transaction rollback.
- Correct handling of provider timeouts.
- Correct handling of stale and out-of-order provider events.
- Correct preservation of audit evidence.

## 20.7 Integration tests

Where feasible, tests SHOULD use the real PostgreSQL transaction and locking behavior required by the workflow.

Mocks MAY be used for external providers in unit tests.

However, mocks MUST NOT be the only evidence for critical transaction, concurrency, or integration behavior.

## 20.8 Test execution

Tests SHOULD be separated into appropriate categories, such as:

- Unit tests.
- Database integration tests.
- Task processing tests.
- Provider contract tests.
- Concurrency tests.
- End-to-end workflow tests.

The CI pipeline MUST run the required test categories for the changes being merged.

Tests MUST NOT silently disable transaction, locking, or tenant-isolation behavior merely to simplify execution.

---

# 21. Failure Scenarios and Required Behavior

The following scenarios define minimum expected behavior.

## 21.1 Redis unavailable after invoice issuance

**Scenario:** The invoice transaction commits, but Redis is unavailable.

Required behavior:

- The invoice remains committed according to the approved business transaction.
- The outbox event remains stored in PostgreSQL.
- The dispatcher retries publication when the broker becomes available.
- Monitoring identifies the growing outbox backlog.
- No duplicate invoice is created during recovery.

## 21.2 Worker crashes after publishing to a provider

**Scenario:** The provider receives the request, but the worker crashes before saving the response.

Required behavior:

- The operation is not automatically treated as a definitive failure.
- The durable operation record remains available.
- Recovery checks the provider's status or uses its idempotency mechanism.
- The application avoids duplicate external effects.
- The final result is reconciled and audited.

## 21.3 Duplicate webhook delivery

**Scenario:** A provider delivers the same event more than once.

Required behavior:

- The callback is authenticated.
- The event is identified through the approved deduplication mechanism.
- Completed business effects are not repeated.
- The provider receives the acknowledgement required by its contract.
- Duplicate delivery is observable without generating misleading business failures.

## 21.4 Tenant entitlement changes while a task is queued

**Scenario:** A task is queued while a module is available, but the tenant's entitlement changes before execution.

Required behavior:

- The task evaluates the approved execution policy.
- Unauthorized new operations are prevented.
- Historical business records are preserved.
- Regulatory or financial obligations are handled according to the approved policy.
- The operation's final state is visible and recoverable.

## 21.5 Provider outage creates a large backlog

**Scenario:** An external provider is unavailable for an extended period.

Required behavior:

- Retries are bounded and delayed.
- Worker capacity is not consumed indefinitely by immediate retries.
- Critical and noncritical workloads are isolated where necessary.
- The backlog remains durable.
- Operators receive appropriate alerts.
- Recovery occurs gradually when the provider becomes available.

## 21.6 A scheduled task runs twice

**Scenario:** Two scheduler instances initiate the same scheduled workflow.

Required behavior:

- The task's idempotency mechanism prevents duplicate business effects.
- Any shared lock or claim is handled safely.
- The system records the outcome.
- Duplicate scheduling does not create duplicate financial or subscription operations.

## 21.7 Worker crashes while holding a processing claim

**Scenario:** A worker claims an outbox event and crashes.

Required behavior:

- The event does not remain permanently stuck.
- A lease or equivalent recovery mechanism makes the event eligible for safe recovery.
- Another worker can resume processing.
- Duplicate publication remains safe.

## 21.8 A payment request times out

**Scenario:** The payment provider may have accepted a payment, but the application receives no response.

Required behavior:

- The system records an uncertain outcome.
- It does not blindly initiate another payment.
- It uses the provider's documented lookup, idempotency, or reconciliation mechanism.
- The final payment state is recorded with appropriate evidence.

---

# 22. Implementation Roadmap

The following roadmap identifies when the processing architecture should be implemented.

| Phase | Required processing capabilities |
|---|---|
| P0 — Foundation | Establish Celery configuration strategy, task conventions, logging, and test infrastructure |
| P1 — Core Platform | Establish tenant-safe task execution patterns and shared operational controls |
| P2 — Subscription Engine | Implement idempotent provisioning, expiry processing, and entitlement reconciliation |
| P3 — CRM, Sales & Invoicing | Implement required invoice-related events and durable follow-up processing |
| P4 — UAE E-Invoicing | Implement provider submission records, retries, inbox/outbox integration, and reconciliation |
| P5 — Accounting & VAT | Protect posting workflows and reporting jobs with transaction and idempotency controls |
| P6 — Procurement & Inventory | Protect receipt, transfer, adjustment, and synchronization workflows |
| P7 — HRMS & Payroll | Protect payroll processing, payslip generation, and finalization workflows |
| P8 — Projects, Expenses & Fixed Assets | Implement appropriate asynchronous imports, processing, and reporting |
| P9 — Banking & Advanced Finance | Implement payment and banking reconciliation with uncertain-outcome handling |
| P10 — Reporting & Integrations | Expand event delivery, import/export jobs, and integration operations |
| P11 — Enterprise Readiness | Strengthen operational recovery, monitoring, capacity planning, and resilience |
| P12 — Production Launch | Validate queue recovery, backup and restore, alerts, failure runbooks, and production readiness |

A phase MUST implement the processing capabilities required by its own features.

It MUST NOT defer a critical idempotency or transaction-safety requirement merely because the full shared processing architecture is scheduled for a later phase.

---

# 23. Requirements Traceability

The following requirement IDs are introduced by this document and SHOULD be added to the project's requirements traceability matrix.

| Requirement ID | Requirement | Priority |
|---|---|---|
| EVT-001 | Asynchronous processing MUST use the approved task execution architecture. | MUST |
| EVT-002 | PostgreSQL MUST remain authoritative for business state. | MUST |
| EVT-003 | Critical follow-up work MUST have durable processing intent. | MUST |
| EVT-004 | Critical business changes and their outbox events MUST commit atomically. | MUST |
| EVT-005 | Task execution MUST tolerate duplicate delivery where retries or redelivery are possible. | MUST |
| EVT-006 | Tenant-scoped tasks MUST establish and validate explicit tenant context. | MUST |
| EVT-007 | Tasks MUST revalidate applicable resource ownership and execution policy. | MUST |
| EVT-008 | Retry policies MUST be bounded and based on failure classification. | MUST |
| EVT-009 | Permanent failures MUST NOT be retried indefinitely. | MUST |
| EVT-010 | Ambiguous external outcomes MUST be reconciled before unsafe repeated side effects. | MUST |
| EVT-011 | Critical failed operations MUST remain discoverable and recoverable. | MUST |
| EVT-012 | Scheduled tasks MUST define timezone, overlap, and missed-run behavior. | MUST |
| EVT-013 | Financial operations MUST preserve transaction integrity and domain state transitions. | MUST |
| EVT-014 | Provider webhooks MUST be authenticated and processed idempotently. | MUST |
| EVT-015 | Event schemas MUST be documented and versioned where needed. | MUST |
| EVT-016 | Critical asynchronous workflows MUST provide sufficient operational visibility. | MUST |
| EVT-017 | Task messages MUST NOT contain unnecessary secrets or sensitive data. | MUST |
| EVT-018 | Worker concurrency MUST be planned against database and provider capacity. | MUST |
| EVT-019 | Automated tests MUST cover retries, duplicate delivery, tenant isolation, and recovery. | MUST |
| EVT-020 | Manual recovery MUST follow authorization and audit requirements. | MUST |
| EVT-021 | The system SHOULD use queue isolation for workloads with materially different resource requirements. | SHOULD |
| EVT-022 | Critical inbound integration events SHOULD use a durable inbox or equivalent deduplication mechanism. | SHOULD |
| EVT-023 | The system SHOULD use correlation identifiers across asynchronous workflows. | SHOULD |
| EVT-024 | The system SHOULD provide operation-status tracking for important user-visible jobs. | SHOULD |
| EVT-025 | Event consumers MUST tolerate compatible schema evolution and deployment overlap. | MUST |

---

# 24. Pending Architectural Decisions

The following decisions require review before the affected capabilities are finalized.

| Decision ID | Decision | Proposed Owner |
|---|---|---|
| EVT-DEC-001 | Confirm Celery broker configuration and Redis deployment topology. | Architecture and DevOps |
| EVT-DEC-002 | Select the authoritative application-level operation-status model. | Architecture |
| EVT-DEC-003 | Finalize the transactional outbox schema and dispatch strategy. | Architecture |
| EVT-DEC-004 | Define outbox claim leases and stale-claim recovery. | Architecture |
| EVT-DEC-005 | Define event naming, schema versioning, and ownership conventions. | Architecture |
| EVT-DEC-006 | Decide which internal workflows require outbox publication. | Architecture and Module Owners |
| EVT-DEC-007 | Finalize idempotency storage and uniqueness constraints. | Architecture |
| EVT-DEC-008 | Define default retry profiles by task category. | Architecture and Operations |
| EVT-DEC-009 | Define terminal failure and dead-letter handling. | DevOps and Operations |
| EVT-DEC-010 | Finalize Celery queue and worker-pool topology. | DevOps |
| EVT-DEC-011 | Define task concurrency, timeouts, and resource limits. | DevOps |
| EVT-DEC-012 | Select the periodic scheduling implementation and deployment model. | Architecture and DevOps |
| EVT-DEC-013 | Define missed-schedule and overlapping-task policies. | Architecture and Module Owners |
| EVT-DEC-014 | Define task and event retention periods. | Security, Compliance, and Operations |
| EVT-DEC-015 | Define the monitoring and alerting stack. | DevOps |
| EVT-DEC-016 | Finalize provider-specific retry, idempotency, and reconciliation rules. | Integration Owner |
| EVT-DEC-017 | Define worker database roles and PostgreSQL RLS context handling. | Security and Architecture |
| EVT-DEC-018 | Define outbox backlog and task-age alert thresholds. | Operations |
| EVT-DEC-019 | Define operational recovery permissions and approval requirements. | Security and Product |
| EVT-DEC-020 | Define event replay tooling and operator procedures. | Architecture and Operations |

These decisions MUST be documented in the project's architectural decision records when resolved.

Critical security, financial-integrity, and regulatory decisions MUST be resolved before production release of the affected workflows.

---

# 25. Instructions for Codex and Development Agents

Every agent implementing asynchronous processing MUST follow this document.

## 25.1 Before implementation

The agent MUST read:

1. `AGENTS.md`
2. `SYSTEM_ARCHITECTURE.md`
3. `DJANGO_APP_STRUCTURE.md`
4. `DATABASE_DESIGN.md`
5. `MULTI_TENANCY.md`
6. `AUTHENTICATION_AND_PERMISSIONS.md`
7. `MODULE_DEPENDENCIES.md`
8. `ENTITLEMENT_ENGINE.md`
9. `API_STANDARDS.md`
10. The owning module's specification.
11. The relevant testing and security standards.

The agent MUST inspect the existing implementation before introducing a new task framework, event bus, scheduler, or operational model.

It MUST NOT assume that a conceptual model described in this document already exists in the codebase.

## 25.2 During implementation

The agent MUST:

- Use explicit task contracts.
- Pass stable identifiers rather than model instances.
- Establish tenant context safely.
- Revalidate resource ownership.
- Reuse application services.
- Define transaction boundaries.
- Implement idempotency where required.
- Apply bounded retry policies.
- Distinguish permanent failures from transient failures.
- Preserve uncertain external outcomes.
- Record critical work durably.
- Use the outbox where required.
- Implement appropriate duplicate-delivery protection.
- Protect secrets and sensitive data.
- Add failure and recovery tests.
- Update documentation and operational runbooks.

The agent MUST NOT:

- Assume Celery delivers every message exactly once.
- Treat Redis as the sole record of a critical operation.
- Rely on `transaction.on_commit()` as a complete durable-publication solution.
- Retry every exception indiscriminately.
- Assume a timeout means an external operation failed.
- Perform a second payment or submission without appropriate duplicate protection.
- Bypass tenant or permission checks inside workers.
- Use unsafe task-message deserialization.
- Use unbounded retries.
- Delete failed business operations merely to clear a queue.
- Claim regulatory acceptance based solely on successful task execution.
- Introduce microservices without an approved decision.

## 25.3 After implementation

The agent MUST report:

- Files changed.
- Tasks and event types introduced.
- Transaction and outbox behavior.
- Idempotency mechanism.
- Retry and failure policies.
- Tenant-isolation controls.
- External side effects.
- Recovery procedure.
- Tests executed and results.
- Database migration impact.
- Monitoring requirements.
- Known limitations.
- Outstanding decisions.

The agent MUST NOT claim that a workflow is reliable, exactly-once, production-ready, or compliant without evidence supporting the claim.

---

# 26. Definition of Done

The shared event and task processing architecture is considered established when:

- [ ] Celery configuration follows the approved architecture.
- [ ] Broker credentials and network access are secured.
- [ ] Task naming and contract conventions are documented.
- [ ] Tenant context is explicit and validated.
- [ ] Critical work has durable processing records.
- [ ] The transactional outbox is implemented for applicable workflows.
- [ ] Duplicate publication and task delivery are safe.
- [ ] Retry policies are bounded and documented.
- [ ] Permanent failures are distinguishable from transient failures.
- [ ] Failed operations remain discoverable.
- [ ] Manual recovery follows authorization and audit requirements.
- [ ] Scheduled tasks have explicit overlap and missed-run policies.
- [ ] Critical external operations support reconciliation.
- [ ] Operation status is available where required.
- [ ] Monitoring covers queues, failures, backlogs, and stale operations.
- [ ] Automated tests cover transaction rollback, retries, duplicates, and recovery.
- [ ] Relevant Codex agent instructions reference this standard.
- [ ] Outstanding architectural decisions are tracked.
- [ ] Production deployment and recovery procedures are documented.

Completion of this document does not prove that these mechanisms have been implemented. Implementation and verification evidence are required.

---

# 27. Official Technical References

The following references should be used to validate framework-specific implementation details against the versions pinned in the project.

- **Celery documentation:** https://docs.celeryq.dev/en/stable/
- **Celery tasks:** https://docs.celeryq.dev/en/stable/userguide/tasks.html
- **Celery periodic tasks:** https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
- **Celery worker configuration:** https://docs.celeryq.dev/en/stable/userguide/workers.html
- **Django transactions:** https://docs.djangoproject.com/en/5.2/topics/db/transactions/
- **Django signals and transaction behavior:** https://docs.djangoproject.com/en/5.2/topics/signals/
- **PostgreSQL explicit locking:** https://www.postgresql.org/docs/current/explicit-locking.html
- **PostgreSQL transaction isolation:** https://www.postgresql.org/docs/current/transaction-iso.html
- **Redis documentation:** https://redis.io/docs/latest/

The project MUST verify these references against the actual versions installed and supported in the production environment. Do not assume that every configuration option or behavior is identical across versions.

---

# 28. Final Architectural Rule

**A task queue is a mechanism for executing work, not the authoritative record that the work must happen or that it has succeeded.**

PostgreSQL must preserve critical business state and the durable intent to perform required follow-up work. Tasks and events must tolerate duplicate delivery, workers must validate tenant context and business state, and retries must respect idempotency and external-system behavior.

When a workflow crosses a database boundary and an external provider boundary, the implementation must explicitly address partial failure, uncertain outcomes, reconciliation, and audit evidence.

These rules apply consistently to invoices, accounting, VAT, e-invoicing, inventory, payroll, payments, subscriptions, and every other module that introduces asynchronous business processing.
