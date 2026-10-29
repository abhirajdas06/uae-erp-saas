# P10 — Reporting, Analytics and Integration Hub Phase Specification

| Property | Value |
|---|---|
| Document ID | P10-SPEC-001 |
| Status | READY FOR REVIEW — REPORT CATALOGUE AND INTEGRATION SCOPE APPROVAL REQUIRED |
| Implementation authorization | NOT GRANTED |

## 1. Objective and Authority

Deliver tenant-safe, reproducible reporting and shared provider-neutral integration infrastructure without creating a parallel source of business truth. Implements `REP-001`–`REP-003`, `INT-001`–`INT-002`, ADR-003–010, ADR-013–015 and ADR-017–020.

Domain-specific regulated adapters remain owned by their domains. P10 may supply shared transport, credential-reference, webhook, operation and health capabilities but cannot reinterpret domain outcomes.

## 2. Entry Gates

- P01 tenancy/IAM/audit, P02 entitlement and applicable source-domain contracts are verified.
- Each report has an owner, authoritative sources, metric definition, access policy, as-of behavior and reconciliation rule.
- Each integration has a provider/activity owner, exact contract/version, credential and data policy, failure semantics and activation approval.
- Product Owner approves bounded P10 scope (`APPR-P10-001`).

## 3. Included Scope

- Versioned report catalogue; standard operational/financial reports and dashboards for explicitly available domains.
- Filters, date/as-of semantics, locale/timezone/currency presentation, controlled exports and optional approved background generation.
- Shared integration registry, tenant configuration, secrets references, operation/evidence records, inbox/outbox, authenticated webhooks, retries, reconciliation and health.
- Report/integration UI and approved APIs, authorization, entitlements, isolation/RLS, audit, observability, migration and recovery.

## 4. Excluded Scope

- A warehouse, data lake, BI platform, arbitrary cross-tenant analytics, machine learning, unrestricted report builder or executive metric without approved definition.
- Recalculation of ledger, tax, inventory valuation, payroll or provider status outside owning domains.
- Provider selection, paid commitments, production credentials or activation of a regulated integration.
- Exactly-once delivery claims, silent retries of uncertain operations or storage of secrets in ordinary tables.

## 5. Ownership and Boundaries

`reporting` owns report definitions, authorized execution/snapshots, generated artifacts and delivery evidence. Source domains own business facts and semantic calculations. Accounting owns financial truth.

`integrations` owns shared connection metadata, secrets references, transport operations, webhook/inbox/outbox evidence, scheduling and health. Domain modules own provider-specific business mapping, validation, state transitions and reconciliation. No generic adapter may bypass domain authorization.

## 6. Reporting Controls

- A report definition pins ID/version, owner, sources, joins, filters, time/as-of and timezone rules, currency/rounding, dimensions, authorization, entitlement, sensitivity, freshness and reconciliation.
- Server-side access is applied before aggregation. Saved filters, scheduled runs, caches and artifacts carry tenant/user/service scope and are reauthorized at access.
- Financial reports reconcile to Accounting. Other reports publish metric semantics and source coverage; missing/late/uncertain data is visible.
- Expensive work is bounded by row/time/memory/concurrency quotas and uses approved asynchronous snapshots where appropriate.
- Exports follow ADR-019, mitigate spreadsheet injection, record requester/scope/version/hash/expiry and never expand access.

## 7. Integration Controls

- Registry entries declare owner, purpose, provider/legal entity, mode, environments, schemas, authentication, scopes, endpoints, limits, timeout/retry/idempotency, callback verification, data/retention and disable/exit behavior.
- Secrets are backend references under ADR-017. Configuration never exposes secret values.
- Durable operations distinguish intent, transport, provider receipt, business acceptance, rejection, uncertainty and reconciliation.
- Incoming webhooks authenticate provider/body, bind trusted tenant/connection context, reject replay/oversize/invalid schemas and use inbox deduplication.
- Outbound events use transactional outbox where required. Retries are classified, bounded and jittered; uncertain side effects are reconciled before retry.
- Health summarizes evidence without leaking data or implying business success.

## 8. Migration, Recovery and Operations

Migrations preserve definition/contract versions, report snapshots/artifacts, connection identities, operation/idempotency/inbox/outbox records and audit. Restore reconciles report catalogue/results where retained, artifacts, integrations, operation states, inbox/outbox and source-domain links.

Monitor report latency/failure/queue/exports, cache/artifact leakage, provider availability/rate limits, callback authentication/replay, retry/dead-letter/uncertainty, credential/certificate expiry and reconciliation age.

## 9. Acceptance Criteria

| ID | Criterion |
|---|---|
| P10-AC-001 | Approved report catalogue and integration inventory identify owners, exact scopes, contracts and disabled behavior |
| P10-AC-002 | Report definitions are versioned and reproduce documented source, filter, time, currency and metric semantics |
| P10-AC-003 | Every report/dashboard/export enforces tenant, role, object, field and entitlement controls before aggregation |
| P10-AC-004 | Financial reports reconcile to Accounting and other metrics reconcile to named authoritative domains |
| P10-AC-005 | Large report execution is bounded, observable and cannot exhaust shared resources |
| P10-AC-006 | Generated exports/artifacts are private, safe, checksummed, expiring and audited |
| P10-AC-007 | Integration registry/configuration is tenant-safe and stores only secrets references |
| P10-AC-008 | Outbound operations/events are durable, versioned, idempotent and preserve uncertain outcomes |
| P10-AC-009 | Incoming callbacks are authenticated, schema-validated, replay-safe and tenant-routed from trusted context |
| P10-AC-010 | Retry, rate-limit, dead-letter, replay and reconciliation behavior is bounded and operable |
| P10-AC-011 | Shared integration infrastructure cannot bypass domain validation or fabricate provider/business success |
| P10-AC-012 | Logs, audit, telemetry and health indicators are useful, minimized and redacted |
| P10-AC-013 | UI/API/task/cache/file/report paths pass authorization, isolation and security tests |
| P10-AC-014 | Migration and restore reconcile reports, artifacts, connections, operations, events and audit |
| P10-AC-015 | Performance, monitoring, incident/runbook and accessibility evidence meets approved targets |
| P10-AC-016 | Domain, Finance, Security, Integration, Database, Operations and independent findings are dispositioned |
| P10-AC-017 | Product Owner records bounded exit and each production integration activation separately |

## 10. Evidence and Approval Gates

Evidence `P10-EV-001`–`P10-EV-014` is defined by P10-TRACE-001. `APPR-P10-001` governs phase scope, `APPR-P10-002` report catalogue/semantics, `APPR-P10-003` shared integration contract, `APPR-P10-004` each provider activation and `APPR-P10-005` exit.
