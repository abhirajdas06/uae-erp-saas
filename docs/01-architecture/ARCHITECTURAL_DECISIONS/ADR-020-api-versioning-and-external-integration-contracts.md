# ADR-020: API Versioning and External Integration Contracts

| Field | Details |
|---|---|
| ADR ID | ADR-020 |
| Title | API Versioning and External Integration Contracts |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 28 October 2026 |
| Decision Owner | Architecture / Integration Domain Owner |
| Reviewers | Product, Architecture, Security, QA, Operations, Domain Owners, Integration Consumers |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-003–ADR-006, ADR-008–ADR-010, ADR-012, ADR-013–ADR-019 |
| Related Requirements | NFR-002–NFR-004, INT-001–INT-002, EIN-001, REP-003 |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DJANGO_APP_STRUCTURE.md`, `API_STANDARDS.md`, `EVENT_AND_TASK_PROCESSING.md`, `AUTHENTICATION_AND_PERMISSIONS.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The platform needs stable machine contracts for selected external clients, provider integrations, webhooks, exports, and future partner interfaces. ADR-008 limits REST APIs to justified machine consumers; it does not define how those contracts evolve. External consumers deploy independently, provider schemas change outside the platform's release cycle, and silent response or semantic changes can cause financial, tenant-isolation, and regulatory failures.

The existing API standard proposes `/api/v1/` major-version paths, OpenAPI documentation, provider adapters, authenticated webhooks, idempotency, and contract tests. This ADR makes those boundaries a coherent evolution policy while leaving commercial support periods and individual provider contracts to approved specifications.

## 2. Decision Drivers

- Predictable compatibility for independently deployed consumers.
- Explicit breaking-change, support, and deprecation governance.
- Provider-specific change containment.
- Machine-readable contracts and testable conformance.
- Tenant isolation, authorization, entitlements, and audit at every interface.
- Idempotent and recoverable state-changing operations.
- Stable financial, decimal, currency, date/time, error, and status semantics.
- Consumer discovery, migration evidence, and operational observability.
- No unnecessary HTTP boundary inside the modular monolith.

## 3. Options Considered

### Option A: Major-version URI paths plus versioned schemas and adapters

Expose approved external REST APIs under `/api/v{major}/`, publish OpenAPI contracts, version webhook/event/provider schemas independently, and introduce a new major version for incompatible changes.

**Advantages:** visible routing, straightforward concurrent versions, strong documentation and test alignment.

**Disadvantages:** parallel maintenance, migration work, and policy overhead.

### Option B: Header-only API version negotiation

**Advantages:** stable resource URLs and flexible content negotiation.

**Disadvantages:** less visible operational routing and consumer support complexity for the initial platform.

### Option C: Unversioned endpoints with continuous evolution

**Advantages:** simplest implementation.

**Disadvantages:** silent incompatibility, unsafe consumer coupling, and weak deprecation governance.

### Option D: Freeze every contract indefinitely

**Advantages:** maximum theoretical compatibility.

**Disadvantages:** accumulating defects, obsolete security models, and inability to meet changing provider or regulatory requirements.

## 4. Decision

Approved external REST APIs use **major-version URI paths**, beginning with:

```text
/api/v1/
```

Each supported major version has a published OpenAPI contract, documented semantics, compatibility tests, ownership, lifecycle state, and consumer migration path. Internal Python application-service interfaces remain in-process and do not use HTTP version paths.

Provider adapters, inbound webhooks, outbound webhooks, asynchronous integration events, file schemas, and bulk import/export contracts use their own explicit schema or adapter versions because their lifecycle may differ from the public REST API.

### 4.1 Interface catalogue and ownership

Maintain an interface catalogue identifying:

- Contract ID, type, owner, purpose, and data classification.
- Consumers or providers and approved authentication mechanism.
- Tenant, legal-entity, permission, and entitlement requirements.
- Current schema/major version and lifecycle status.
- OpenAPI or schema location and examples.
- Idempotency, ordering, pagination, rate-limit, and retry semantics.
- Support/deprecation dates when approved.
- Monitoring, audit, incident, and contact ownership.

Each domain owns the meaning of its resources and operations. The integration layer owns provider translation and transport behavior. A shared API layer may enforce conventions but must not become the owner of every domain operation.

### 4.2 Compatibility classification

Changes are classified through contract review.

Generally nonbreaking changes include:

- Adding optional request fields with unchanged defaults.
- Adding response fields when consumers are required to tolerate unknown fields.
- Adding new endpoints or optional capabilities.
- Correcting behavior to match an already precise published contract, after impact review.
- Security and defect fixes that preserve documented semantics.

Generally breaking changes include:

- Removing or renaming fields, endpoints, error codes, or supported values.
- Changing field type, scale, unit, currency meaning, requiredness, or nullability incompatibly.
- Changing authentication, authorization, tenant context, entitlement, idempotency, pagination, ordering, or retry semantics incompatibly.
- Changing a status or error meaning, default, side effect, or state transition.
- Reinterpreting dates, time zones, decimals, identifiers, or financial amounts.
- Adding enum values when the published consumer contract does not require unknown-value tolerance.

Ambiguous changes are treated as breaking until contract tests and consumer review show otherwise. A new major API version is required for incompatible REST changes unless an explicitly approved migration strategy provides equivalent safety.

### 4.3 Contract form and source control

OpenAPI is the machine-readable contract for versioned REST APIs. It documents endpoints, schemas, authentication, tenant context, permissions, entitlements, errors, pagination, idempotency, rate limits, side effects, asynchronous completion, audit behavior, and deprecation.

Provider, webhook, event, and file contracts use an appropriate versioned schema or bounded adapter fixture. Generated documentation may be derived from code, but the reviewed contract diff is release evidence. Implementation models or database schemas are not automatically public contracts.

Contracts, examples, and compatibility fixtures are version-controlled. Documentation and implementation changes are reviewed together.

### 4.4 Representational conventions

External contracts follow `API_STANDARDS.md` and the relevant ADRs:

- UUIDs use canonical string representation under ADR-014.
- Monetary amounts use decimal strings with explicit currency and ADR-013 semantics; binary floating point is not a financial contract.
- Timestamps are timezone-aware ISO 8601 values; business dates remain distinct date fields.
- Stable machine-readable error codes accompany safe human messages and correlation IDs.
- Pagination, filtering, sorting, nullability, and unknown-enum behavior are explicit.
- External identifiers are distinct from internal identifiers and scoped to the provider or connection.

### 4.5 Deprecation and retirement

An API or contract is not removed merely because a newer version exists. Deprecation requires:

1. Named owner and affected-consumer inventory.
2. Replacement contract and migration guidance.
3. Approved notice and support period.
4. Documentation, machine-visible deprecation indicators where practical, and direct consumer communication where applicable.
5. Usage and failure telemetry that does not expose sensitive payloads.
6. Exit evidence showing migration, explicit exception, or authorized retirement.
7. Rollback or incident plan for retirement.

Exact minimum support and notice periods remain a product, contractual, and operational decision. Emergency security retirement requires documented risk authority and consumer communication rather than a silent incompatible change.

### 4.6 Concurrent versions

When major versions overlap, routing and code structure must make their differences explicit. Versions may share domain services when semantics are compatible, but serializers/adapters must not mutate old behavior accidentally. New versions do not duplicate authoritative business state.

Each version has defined monitoring and retirement criteria. Supporting an old version does not permit bypassing current tenant isolation or critical security controls; compatible security enforcement and safe migration are required.

### 4.7 Provider contracts and adapters

Provider-specific payloads and statuses terminate at versioned adapters. Domain services consume canonical internal commands and results. Each adapter declares provider API/schema version, authentication, serialization, error taxonomy, timeouts, retry eligibility, idempotency, webhook verification, status mapping, and evidence retention.

Provider upgrades are tested as contract changes. A provider's successful transport response is not reinterpreted as business or regulatory success unless the validated contract says so. ADR-012 governs the UAE e-invoicing boundary.

### 4.8 Webhooks and integration events

Inbound webhook contracts validate provider/connection, exact signed bytes where required, timestamp/replay controls, schema version, event identity, and tenant mapping before business processing. Unknown versions fail safely or are quarantined; they are not guessed.

Outbound webhooks and integration events include a stable event ID, event type, schema version, occurrence time, subject reference, and tenant-safe routing context. They use ADR-010 for durable delivery when material, support duplicate delivery, and document ordering and retry behavior. Consumers must be idempotent.

Webhook endpoint path versioning may differ from payload schema versioning. Both must be explicit.

### 4.9 State-changing operations and asynchronous completion

Contracts for material writes define idempotency key scope, request fingerprint behavior, duplicate response semantics, concurrency/precondition rules, and final-state retrieval. Long-running operations return a durable operation reference rather than holding an HTTP connection or claiming premature success.

Timeout or unknown response does not prove failure. Reconciliation and status APIs must allow safe recovery for payments, e-invoicing, imports, exports, and other ambiguous external operations.

### 4.10 Security and exposure governance

No endpoint is public merely because it exists. Each interface has approved authentication, tenant resolution, authorization, entitlement, validation, abuse controls, and audit behavior. API version selection never weakens these controls.

Unversioned business endpoints are prohibited. Narrow operational endpoints such as health probes may be exempt when they disclose no tenant or business data and are governed by deployment security. Provider callback paths may follow provider constraints but still carry an explicit internal contract version and validation policy.

### 4.11 Contract verification

CI under ADR-015 validates:

- OpenAPI/schema validity and deterministic generation.
- Implementation conformance to published request, response, and error schemas.
- Backward-compatibility diffs within a supported major version.
- Consumer/provider fixtures and negative security cases.
- Decimal, date/time, identifier, pagination, idempotency, and unknown-value behavior.
- Webhook signature/replay handling and duplicate delivery.

Mocks are appropriate for unit tests but are not the only evidence for external compatibility. Approved sandbox, certification, recorded-contract, or controlled integration tests are required according to provider risk.

## 5. Rationale

Path-based major versions are explicit for clients, routing, monitoring, and overlapping support. Machine-readable contracts, compatibility review, and adapters constrain accidental coupling. Independent schema versions recognize that REST, providers, webhooks, events, and files change on different schedules while sharing security and domain rules.

## 6. Consequences

### Positive consequences

- Consumers receive predictable compatibility and migration signals.
- Breaking changes are visible and reviewable.
- Provider churn is contained in adapters.
- Contract tests become enforceable release evidence.
- Security, tenant, financial, and error semantics are explicit.
- Multiple consumers can migrate without duplicating business data.

### Negative consequences and trade-offs

- Concurrent versions increase maintenance and test cost.
- Consumer inventory and communication require operational ownership.
- Strict compatibility may delay otherwise simple changes.
- Provider sandboxes and certification can be incomplete or costly.
- Support periods and emergency retirement require product judgment.

### Risks and mitigations

- **Silent contract drift:** schema diffs, conformance tests, and required contract review.
- **Old-version security weakness:** compatible controls, migration, monitored exceptions, and authorized retirement.
- **Provider schema surprise:** adapter version pinning, quarantine, sandbox/contract tests, and reconciliation.
- **Enum or semantic incompatibility:** documented unknown-value policy and breaking-change classification.
- **Duplicate side effects:** scoped idempotency, durable operations, ADR-010, and reconciliation.
- **Consumer abandonment:** catalogue, usage telemetry, notices, migration guidance, and retirement evidence.

## 7. Security and Tenant-Isolation Implications

- Every version independently enforces trusted tenant context, authorization, entitlements, and object ownership.
- Version selection, external IDs, signed payload fields, or client-supplied tenant IDs cannot establish authorization.
- Contracts minimize sensitive fields and define field-level permissions, safe errors, and redaction.
- Provider credentials and webhook secrets follow ADR-017; logs and audit follow ADR-018.
- Contract and negative tests cover cross-tenant identifiers, disabled memberships, revoked entitlements, replay, over-posting, and mass assignment.

## 8. Data Integrity and Migration

- API versions are presentation/integration boundaries, not separate ledgers or duplicated domain models.
- Migrations preserve stable identifiers, money semantics, idempotency records, and operation status.
- Breaking financial or provider changes require reconciliation and explicit cutover/rollback evidence.
- Backfills distinguish historical interpretation from new semantics and do not rewrite protected evidence.
- Contract retirement occurs only after data and in-flight operation compatibility are addressed.

## 9. Operational Impact

Operations must monitor traffic, failures, latency, rate limits, authentication, provider-version errors, deprecated-version use, webhook verification, delivery retries, and migration progress by safe interface identifiers. Runbooks cover provider outage, incompatible payload, leaked credential, replay attack, rate-limit exhaustion, version rollback, and consumer migration failure.

## 10. Implementation Requirements

1. Create the interface catalogue and assign owners.
2. Configure `/api/v1/` routing only for approved ADR-008 consumers.
3. Establish version-controlled OpenAPI and schema generation/validation.
4. Define compatibility-diff rules and CI gates.
5. Define shared error, decimal, currency, date/time, identifier, pagination, and idempotency conventions.
6. Implement versioned provider adapters and webhook/event schema handling.
7. Establish deprecation, consumer communication, telemetry, and retirement procedures.
8. Add conformance, backward-compatibility, security, idempotency, replay, and controlled provider contract tests.
9. Record each material external contract and version in the interface catalogue before production exposure.

## 11. Validation and Acceptance Criteria

- [ ] Every exposed business API has an owner, approved consumer, explicit major version, and contract.
- [ ] Supported REST contracts have valid OpenAPI documents and implementation conformance tests.
- [ ] CI detects incompatible changes inside a supported major version.
- [ ] Money, dates, identifiers, errors, pagination, idempotency, and asynchronous outcomes are unambiguous.
- [ ] Provider schemas and statuses do not leak into unrelated domain services.
- [ ] Unknown webhook or event versions fail safely and are observable.
- [ ] Every version passes tenant-isolation, authorization, entitlement, replay, and mass-assignment tests.
- [ ] Deprecation identifies consumers, replacement, notice, telemetry, support period, and retirement evidence.
- [ ] Duplicate requests and deliveries cannot create duplicate protected business effects.
- [ ] Provider compatibility uses controlled contract or integration evidence in addition to unit-test mocks.

## 12. Alternatives Rejected

- Unversioned external business APIs are rejected.
- Silent incompatible changes within a supported major version are rejected.
- Provider payloads as internal domain models are rejected.
- Database models as the automatic public contract are rejected.
- Indefinite support without ownership, telemetry, or retirement criteria is rejected.
- A single global version number for REST, providers, webhooks, events, and files is rejected.

## 13. References

- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- `docs/01-architecture/DJANGO_APP_STRUCTURE.md`
- `docs/01-architecture/API_STANDARDS.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Major-version URI paths for approved REST APIs, version-controlled OpenAPI contracts, independently versioned provider/webhook/event/file schemas, compatibility gates, and governed deprecation.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; consumer scope, support/deprecation windows, rate limits, and provider-specific policies remain product/contract decisions.

Minimum support and deprecation periods, initial consumer inventory, public/partner exposure scope, rate-limit products, and provider-specific version policies remain unresolved. They block production contract commitments, not further contract templates, catalogue design, or compatibility-test documentation.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial API versioning and external integration contract decision accepted after standards review. |
