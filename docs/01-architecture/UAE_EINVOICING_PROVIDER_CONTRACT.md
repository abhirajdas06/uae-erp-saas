# UAE E-Invoicing Provider Contract Boundary

| Property | Value |
|---|---|
| Document ID | ARCH-EINV-CONTRACT-001 |
| Status | READY FOR REVIEW — PROVIDER NEUTRAL |
| Governing ADR | ADR-012 |
| Regulatory baseline | REG-SRC-001, cut-off 29 October 2026 |

## 1. Boundary

`invoicing` owns immutable issued invoice/credit-note facts. `e_invoicing` owns applicability evaluation, canonical submission snapshots, validation, provider accounts/adapters, operations, attempts, native and internal statuses, callbacks, acknowledgements and reconciliation. An adapter may translate; it cannot mutate the source document or decide accounting/VAT policy.

The contract is an internal architecture contract, not a provider selection or claim of conformance to PINT AE. `ARCH-PINT-AE-001` governs the pinned 2025-Q2 artefact structure and mapping strategy; the provider contract must name the exact profile/resource versions it accepts.

## 2. Versioned Commands and Facts

| Contract | Producer → consumer | Required semantics |
|---|---|---|
| `PrepareElectronicDocument.v1` | Invoicing → E-Invoicing | Stable tenant/legal-entity/source/version, type, immutable party/line/tax/total/currency/correction snapshots, policy versions and source hash |
| `SubmitElectronicDocument.v1` | Authorized service → E-Invoicing | Prepared operation ID, provider account/environment and stable idempotency key; no client-supplied success state |
| `ElectronicDocumentStatusChanged.v1` | E-Invoicing → authorized consumers | Source/operation, controlled internal status, native status/reference, evidence time, mapping version and correlation; no unsupported acceptance claim |
| `ElectronicDocumentReconciliationRequired.v1` | E-Invoicing → Operations | Reason, last evidence, uncertainty class, safe next action and ownership |

Schema compatibility follows ADR-020. Decimals are strings; timestamps include timezone; identifiers are opaque UUIDs; payloads carry schema and ruleset versions.

## 3. Canonical Snapshot

The snapshot records document and correction identity, supplier and buyer identifiers/addresses, dates, currency, lines, allowances/charges, tax classifications and amounts, totals, payment/terms references only when approved, source/rule/schema versions, and cryptographic content hash. A separate mapping manifest records the approved Billing/Self-Billing and Invoice/Credit Note profile, `IBT`/`IBG`/`BTAE` mapping, UBL paths/cardinalities, code-list/resource checksums, shared/AE Schematron versions and serialized payload hash. Optional/conditional fields are explicit; missing mandatory data produces a validation finding, not a fabricated value.

Provider payloads and responses are retained minimally according to approved policy. Store hashes, safe metadata and immutable evidence; encrypt restricted payloads and never log credentials or complete invoice data.

## 4. Adapter Interface

Each adapter implements capabilities, provider preflight, submit, query/reconcile, verify callback, normalize evidence/status, and safe health check. The domain mapping layer—not arbitrary provider code—performs the approved semantic-to-UBL serialization and standard validation before provider preflight. The adapter manifest declares provider, environment, accepted PINT AE profiles/resource versions/checksums, API/schema/status-map versions, authentication mode, idempotency semantics, timeouts/rate limits, supported document types, callback rules, data locations/retention responsibilities and known limitations.

An unsupported capability fails closed. A generic interface does not erase provider differences.

## 5. Operation State Machine

Controlled states are `PREPARATION_FAILED`, `PREPARED`, `QUEUED`, `SUBMITTING`, `SUBMITTED`, `ACKNOWLEDGED`, `ACCEPTED_WHERE_EVIDENCED`, `REJECTED`, `RETRYABLE_FAILURE`, `PERMANENT_FAILURE`, `UNCERTAIN`, and `RECONCILIATION_REQUIRED`. Only states supported by approved evidence are enabled.

Transport success, HTTP success, worker completion and provider receipt are never silently mapped to tax-authority acceptance. Native status, raw-safe evidence and mapping version remain separately traceable. Duplicate or reordered evidence cannot regress a terminal state without an approved reconciliation operation.

## 6. Reliability and Security

- Preparation and outbox intent commit atomically; network calls occur after commit.
- One stable business idempotency key identifies an operation. Reuse with a different payload is a conflict.
- Timeout after send is `UNCERTAIN`; query/reconcile before resubmission.
- Callback authenticity, timestamp/nonce or equivalent replay controls, provider-account routing and body integrity are verified before processing.
- Tenant/legal-entity/provider-account mapping derives from trusted configuration, never an untrusted callback tenant field.
- Separate sandbox/production endpoints and secrets; rotation does not rewrite history.
- Least-privilege permissions separate prepare, submit, retry, reconcile, configure and view-payload actions.

## 7. Error Contract and Operations

Normalize errors as validation, authentication/configuration, rate limit, transient provider, permanent provider, duplicate/conflict, callback-invalid and uncertain. Preserve provider codes safely. Retries require bounded exponential backoff/jitter and policy limits; non-retryable errors remain operator-visible.

Reconciliation compares source version/hash, prepared snapshot, operation/attempts, provider reference/status, callback evidence and downstream visibility. Runbooks cover outage, rejected document, uncertain result, invalid callback, expiring credential/certificate, schema change and provider cutover.

## 8. Contract Acceptance Criteria

1. Provider-specific code cannot mutate invoice/VAT/accounting records.
2. Every submission is tenant/legal-entity/source/version traceable.
3. Required fields and schema/ruleset version are validated before network delivery.
4. Duplicate commands/callbacks create no duplicate submission or business effect.
5. Uncertain outcomes reconcile before retry.
6. Status meanings are evidence-based, versioned and tested.
7. Secrets/full payloads are absent from logs and routine errors.
8. Historical operations remain readable after adapter/schema/status-map changes.
9. Contract tests cover success, rejection, timeout, crash, retry, duplicate, reordering, invalid callback and provider outage.
10. Production enablement requires a selected accredited provider, signed contract, current artefacts, sandbox/conformance evidence and human approval.

## 9. Provider Onboarding Evidence

Capture dated MoF accreditation evidence; legal entity and contracted service; security/privacy/data-location review; API and schema artefacts with checksums; authentication/certificate lifecycle; environments; supported flows and status meanings; idempotency/reconciliation; SLAs/support/escalation; portability/export/termination; sandbox tests; operational owner; approved limitations; and production activation/rollback decision.
