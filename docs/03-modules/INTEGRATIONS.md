# INTEGRATIONS — Shared Integration Hub Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-INTEGRATIONS-001 |
| Status | APPROVED CONTRACT BASELINE; EXPANDED IMPLEMENTATION DETAIL PROPOSED — SHARED CONTRACT AND PROVIDER ACTIVATION REQUIRED |
| Owning phase / app | P10 / `integrations` |
| Domain owner | Platform Integration |
| Commercial module | Yes |
| Tenant-owned data | Yes, for tenant connections and evidence |
| Readiness | Expanded under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`; sections 3–14 are PROPOSED and unapproved |

## 1. Purpose and Boundary

Own shared provider-neutral connection metadata, secret references, transport operations, inbox, outbox and webhook evidence, scheduling and health under `INT-001`–`INT-002` and [P10-SPEC-001](../02-phases/P10_REPORTING_INTEGRATIONS/P10_PHASE_SPECIFICATION.md). Domain modules retain provider-specific business mapping, validation, authoritative state and reconciliation.

Governing sources: `INT-001`–`INT-002`, P10-SPEC-001, ADR-009, ADR-010, ADR-017, ADR-018, ADR-020, [UAE e-invoicing provider contract](../01-architecture/UAE_EINVOICING_PROVIDER_CONTRACT.md), [banking provider contract](../01-architecture/BANKING_PROVIDER_CONTRACT.md), `ARCH-API-001`, `ARCH-NOTIFY-001`, `QUAL-PRIV-001`, `QUAL-THREAT-001`.

This module is not a universal business-logic layer and does not authorize a provider, a regulated activity or a production credential.

## 2. Actors and Authorization

| Actor | Permitted scope |
|---|---|
| Integration administrator | Define and configure integrations within approved contracts |
| Credential provisioner | Register secret references; never handles business data |
| Integration operator | Invoke, monitor and replay within bounds |
| Domain owner | Owns the business effect of any operation its module requests |
| Replay / reconciliation approver | Authorize a bounded replay or reconciliation action |
| Auditor | Read-only evidence review |
| Purpose-bound support | Time-bounded, audited payload evidence inspection under ADR-018 |

Concrete permission codenames, satisfying `RDY-004`:

`integrations.view_integration`, `integrations.configure_integration`, `integrations.configure_tenant_integration`, `integrations.register_credential_reference`, `integrations.rotate_credential_reference`, `integrations.enable_integration`, `integrations.disable_integration`, `integrations.invoke_operation`, `integrations.view_operation_evidence`, `integrations.view_payload_evidence`, `integrations.replay_operation`, `integrations.approve_replay`, `integrations.reconcile_integration`, `integrations.view_health`, `integrations.export_diagnostics`.

Configure, reference and rotate a credential, enable, invoke, replay, reconcile, inspect payload evidence and export diagnostics are separate, with maker-checker wherever side effects warrant it. A replay requester cannot approve their own replay.

## 3. Domain Ownership

| Record / capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Integration definition and contract version | `integrations` | Platform-owned catalogue | Definition service |
| Tenant integration configuration | `integrations` | Direct tenant | Configuration service |
| Credential reference | `integrations` | Direct tenant | Reference only; material lives in the secrets backend per ADR-017 |
| Operation, attempt, evidence | `integrations` | Direct tenant | Transport services |
| Webhook inbox record | `integrations` | Resolved tenant | Inbox service, fail-closed routing |
| Outbox message | `integrations` | Direct tenant | Outbox service per ADR-010 |
| Schedule and health | `integrations` | Direct tenant | Scheduling and health services |
| Business effect of any operation | Owning domain module | Same-tenant | Domain service only |
| Authoritative provider status interpretation | Owning domain module | Same-tenant | Domain service only |

Transport never applies a business effect. The owning domain service authorizes and validates every effect, and transport cannot bypass it.

## 4. Data Model Requirements

Conceptual entities: `IntegrationDefinition`, `IntegrationContractVersion`, `TenantIntegration`, `CredentialReference`, `IntegrationOperation`, `IntegrationAttempt`, `IntegrationEvidence`, `WebhookInbox`, `OutboxMessage`, `IntegrationSchedule`, `IntegrationHealth`, `IntegrationReconciliationFinding`.

Field-level requirements satisfying `RDY-001`:

| Entity | Required attributes |
|---|---|
| `IntegrationDefinition` | UUID id; code; provider; purpose; capability set; environment classes; owning domain module; contract owner; approval reference |
| `IntegrationContractVersion` | Definition FK; version; effective dates; endpoint set; authentication mechanism; request and response schema references; timeout, retry and rate-limit parameters; idempotency requirement; deprecation date |
| `TenantIntegration` | Tenant FK; definition FK; pinned contract version; environment; `status`; enabled-by and enabled-at; configuration values excluding secrets |
| `CredentialReference` | Tenant integration FK; secret-backend reference; credential type; scope; rotation due date; `status`; never the credential value |
| `IntegrationOperation` | Tenant FK; tenant integration FK; operation type; requesting domain reference; immutable payload hash; idempotency key; `status` including an explicit uncertain state; created-at; terminal-at |
| `IntegrationAttempt` | Operation FK; attempt number; started-at; finished-at; outcome classification of permanent, transient or uncertain; transport status; error classification |
| `IntegrationEvidence` | Operation or inbox FK; native request and response reference; checksum; received-at; redaction applied; retention class |
| `WebhookInbox` | Received-at; raw payload reference; signature verification result; resolved tenant reference or unresolved marker; replay-detection key; `status`; routed-to domain reference |
| `OutboxMessage` | Tenant FK; aggregate reference; event type; payload version; created-at; dispatched-at; attempt history; `status` |
| `IntegrationSchedule` | Tenant integration FK; cadence; window; next-run-at; last-run reference; `status` |
| `IntegrationHealth` | Tenant integration FK; observed-at; availability; latency percentiles; error rate; credential expiry warning; contract-drift indicator |
| `IntegrationReconciliationFinding` | Tenant FK; scope; detected-at; finding type; resolution state |

Constraints: UUID primary keys; mandatory tenant ownership on every tenant-owned row; unique idempotency key per tenant and operation type; unique replay-detection key per inbox source; immutable payload hash and native evidence; append-only attempt and evidence history; same-tenant foreign keys throughout; credential values never stored in an ordinary column; no hard deletion of operations, evidence or inbox records required for reconciliation or audit within their retention class.

## 5. Workflows and States

| Record | States |
|---|---|
| `TenantIntegration` | `CONFIGURED`, `PENDING_CREDENTIAL`, `ENABLED`, `DISABLED`, `SUSPENDED`, `DEPRECATED_CONTRACT` |
| `IntegrationOperation` | `PENDING`, `IN_FLIGHT`, `SUCCEEDED`, `PERMANENTLY_FAILED`, `UNCERTAIN`, `CANCELLED` |
| `WebhookInbox` | `RECEIVED`, `VERIFIED`, `REJECTED`, `ROUTED`, `PROCESSED`, `DUPLICATE`, `UNRESOLVED` |
| `OutboxMessage` | `PENDING`, `DISPATCHED`, `FAILED`, `DEAD_LETTERED` |

Outbound sequence: a domain service records durable intent inside its business transaction, the outbox dispatches asynchronously per ADR-010, transport applies timeout, retry with backoff, rate limiting and circuit behavior, each attempt is classified, and native evidence is retained. An `UNCERTAIN` outcome is never resolved to success without evidence or an authorized reconciliation decision.

Inbound sequence: authenticate and verify the signature, enforce size and schema limits, detect replay, resolve the tenant from trusted data only, route to the owning domain service, and record evidence. Any failure in authentication, verification, schema, size, replay detection or tenant resolution fails closed; an unresolved payload is quarantined and never guessed into a tenant.

A contract version is pinned per tenant integration. Provider drift against the pinned version raises a health finding and may suspend the integration rather than silently adapting.

## 6. Business Rules

| ID | Rule / verification |
|---|---|
| INTM-001 | Exact purpose/provider/capability/environment/contract owner is declared and approved |
| INTM-002 | Tenant configuration is scoped; credentials are secret-backend references only |
| INTM-003 | Domain service authorizes and validates every business effect; transport cannot bypass it |
| INTM-004 | Durable intent/outbox and stable idempotency prevent duplicate effects |
| INTM-005 | Incoming webhook authentication, schema, size, replay and trusted routing fail closed |
| INTM-006 | Timeouts/retries/rate limits/circuit behavior classify permanent/transient/uncertain outcomes |
| INTM-007 | Provider-native evidence and normalized internal status remain separately traceable |
| INTM-008 | Replay/reconciliation is authorized, bounded and cannot duplicate business effects |
| INTM-009 | Logs/health/audit redact secrets and sensitive payloads while preserving correlation |
| INTM-010 | Migration/restore reconciles connections, operations, inbox/outbox and domain references |
| INTM-011 | Outbound requests enforce egress allowlisting and address validation against server-side request forgery; SSRF tests |
| INTM-012 | An unapproved provider, contract version or environment is unreachable rather than partially enabled; negative tests |
| INTM-013 | A credential is never written to a log, error, export, fixture or health record; secret-scan and redaction tests |
| INTM-014 | Entitlement, permission and tenant isolation apply to configuration, invocation, evidence and diagnostics; security tests |
| INTM-015 | A provider acknowledgement is never represented as regulatory compliance or business settlement; disclosure tests |

## 7. Tenant Isolation, Security and Sensitive Data

Every path, including inbound callbacks and scheduled tasks, derives trusted tenant context and validates same-tenant relationships, with row-level security as defence in depth. Background and scheduled execution carries explicit tenant context and never inherits it ambiently from a worker process, per `MULTI_TENANCY.md` and `NTF-046`.

Applicable threats from `QUAL-THREAT-001`, satisfying `RDY-010`: `THR-040` forged provider webhook, `THR-041` replayed callback duplicating a financial effect, `THR-042` compromised provider credential, `THR-043` server-side request forgery, `THR-046` provider outage cascading, `THR-047` loss of acknowledgement evidence, `THR-013` task without tenant context, `THR-031` unsafe deserialization of a payload, `THR-035` sensitive data in logs, `THR-050` committed secret, `ABU-09` duplicate effect through retry.

Data classification and retention, satisfying `RDY-009`: definitions and health are `C1`; tenant configuration is `C2`; payload evidence inherits the classification of the business data it carries and is treated as `C4` where it may contain financial, banking, payroll or personal data; credentials are `C5` and exist only as references. Retention classes are `RET-12` for payload evidence, `RET-10` for transport logs and health, and `RET-09` where evidence forms part of the audit trail, under `QUAL-PRIV-001`. A provider receiving `C3` or higher data requires a recorded purpose, a data-processing arrangement and a named approver before activation, per `PRIV-023`.

Payload evidence is redacted according to the declared rules of its contract version, stored privately, and inspectable only with `integrations.view_payload_evidence` under purpose and audit.

## 8. Entitlements and Degraded Access

`INTEGRATIONS` entitlement and the relevant user permission are both required, and each integration additionally requires the entitlement of the domain module it serves. Suspension or expiry disables new invocation and scheduling by default while preserving evidence and allowing approved read, export and reconciliation. Deactivation never deletes operation evidence, inbox records or audit history, and never prevents required retention or recovery.

## 9. Integrations and Events

- E-invoicing: provide transport for the approved service provider under the e-invoicing provider contract; `MOD-EINVOICING-001` owns mapping, validation and submission status truth.
- Banking: provide transport for the approved connectivity or payment mode under the banking provider contract; `MOD-BANKING-001` owns reconciliation truth.
- Notifications: provide transport for the approved email or message provider; `ARCH-NOTIFY-001` owns the catalogue, recipients and suppression.
- Every domain module: expose the durable intent, idempotency and evidence contracts.
- Monitoring: publish health, latency, error rate, dead-letter age and credential expiry signals to `DEP-OBS-001`.

Reconciliation detects intent-without-dispatch, dispatch-without-evidence, uncertain operations past their window, unresolved inbox records, dead-letter growth and contract drift.

## 10. UI, API, Reports, Imports and Exports

Django and HTMX surfaces cover the integration catalogue, tenant configuration, credential reference registration and rotation status, enable and disable confirmation, operation browser with status and attempt history, evidence inspection under purpose capture, inbox browser including unresolved and duplicate records, outbox and dead-letter monitoring, schedule management, health dashboard and reconciliation findings. Surfaces use the data table, status badge, asynchronous operation status, confirmation dialog and empty-state components in `ARCH-UI-001`. Enable, disable, rotation and replay require explicit confirmation naming the integration and effect per `UIX-036`.

Reports registered in `PROD-REPORTS-001`: this module contributes integration health and operation status to `RPT-804` platform operational health; it owns no business report.

Diagnostics export is bounded, redacted, private, checksummed and audited, and never contains a credential. Business data import is out of scope; this module is transport only.

This module allocates no business document number, so it registers no document type in `ARCH-SEQ-001` beyond operation references, which are internal identifiers and not statutory document numbers.

Notifications registered in `ARCH-NOTIFY-001`, satisfying `RDY-008`: integration enabled and disabled, credential expiring and expired, authentication failure, circuit opened, dead-letter threshold exceeded, contract drift detected, unresolved inbound payload and uncertain operation past its window. Security and regulatory-status categories are mandatory and never digested.

## 11. Regulatory and Financial Readiness

This module asserts no provider accreditation, availability, pricing, capability or regulatory standing. A successful transport exchange is never evidence of regulatory compliance, provider acceptance or business settlement, per `AGENTS.md` section 11 and `INTM-015`. Every concrete provider requires its own domain and provider approval before activation, and production credentials are never provisioned by this specification. No regulatory fact is asserted here, per `RDY-012`.

## 12. Operations, Migration and Recovery

Monitor availability, latency, rate-limit and cut-off behavior, authentication failures, callback success, retry and dead-letter age, uncertain operations, contract drift, credential expiry, unresolved inbox volume and diagnostics export. Runbooks cover a provider outage, an authentication or credential rotation failure, a signature verification failure spike, an unresolved inbound payload, a dead-letter backlog, an uncertain operation requiring provider confirmation, an authorized bounded replay and restore reconciliation.

Migration preserves definitions, pinned contract versions, tenant configuration, credential references, operations, evidence, inbox and outbox state. Restore reconciles connections, operation idempotency keys, inbox replay keys, outbox state and domain references, and verifies that no credential material was captured in a backup artifact.

## 13. Acceptance Criteria, Tests and Evidence

Acceptance criteria are `INTM-001`–`INTM-015` and the applicable criteria in `P10-AC-001`–`P10-AC-017`. Required tests are the integration scenarios within `P10-TST-001`–`P10-TST-171`. Evidence records are `P10-EV-009`–`P10-EV-014` in the [P10 matrix](../02-phases/P10_REPORTING_INTEGRATIONS/P10_TRACEABILITY_AND_TEST_MATRIX.md).

All scenarios are `NOT_RUN`. Tests stub providers at the adapter boundary with recorded contract fixtures per `QUAL-TESTDATA-001` TD-044 and TD-045, perform no live external call in the default suite, and use no real credential.

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| DEC-INT-001 | Which integrations are in launch scope and their owning domains | Product Owner | Integration implementation | Begin with the transport needed by approved e-invoicing, banking Mode A and transactional email only |
| DEC-INT-002 | Credential handling, rotation cadence and secrets backend for each environment | DevOps / Security | Any credential registration | Secret-backend references only, with recorded rotation |
| DEC-INT-003 | Shared infrastructure behavior for retries, rate limits, circuit thresholds, evidence retention and replay authority | Architecture / Operations | Transport implementation | Conservative bounded retries with explicit uncertain classification and authorized replay |
| DEC-NTF-002 | Transactional email provider and sending domain | Product Owner / DevOps | Email transport activation | Select only with a recorded data-processing arrangement |
| DEC-PRIV-009 | Retention for payload evidence and diagnostics exports | Product Owner | Evidence disposal | Short, redacted retention with checksum records |
| DEC-GOV-007 | Phase-entry specification gate covering this expansion | Product Owner / Architecture | P10 implementation authorization | Approve the gate and this expanded specification together |

Every concrete provider still requires its own domain and provider approval; this module's approval does not confer it.

## 15. Implementation Prompt

Use the [P10 orchestration prompt](../04-agents/phase-prompts/P10_REPORTING_INTEGRATIONS.md) and the integration tasks in the [P10 bounded task prompts](../04-agents/phase-prompts/P10_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest; no implementation is authorized by this document.
