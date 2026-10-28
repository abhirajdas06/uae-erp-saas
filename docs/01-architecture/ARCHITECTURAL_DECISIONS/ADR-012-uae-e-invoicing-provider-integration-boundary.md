# ADR-012: UAE E-Invoicing Provider Integration Boundary

| Field | Details |
|---|---|
| ADR ID | ADR-012 |
| Title | UAE E-Invoicing Provider Integration Boundary |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / E-Invoicing Domain Owner |
| Reviewers | Product, Architecture, Security, Integration, Finance, UAE Tax and Compliance, Legal, Operations |
| Affected Phases | P03–P12 |
| Related ADRs | ADR-003, ADR-004, ADR-005, ADR-008, ADR-009, ADR-010, ADR-011, ADR-013, ADR-017, ADR-018, ADR-019, ADR-020 |
| Related Requirements | INV-001–INV-004, EIN-001–EIN-005, INT-001–INT-002, NFR-006–NFR-007 |
| Related Documents | `PRODUCT_REQUIREMENTS.md`, `DATABASE_DESIGN.md`, `SYSTEM_ARCHITECTURE.md`, `API_STANDARDS.md`, `EVENT_AND_TASK_PROCESSING.md` |
| Regulatory Review Date | 27 October 2026 |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The ERP must support UAE e-invoicing through the applicable regulatory framework and an appropriately validated provider route. The Ministry of Finance maintains the official UAE e-invoicing portal and an evolving list of Accredited Service Providers (ASPs). Provider status, legislative material, technical schemas, mandatory fields, dates, and guidance can change.

The ERP invoice remains a business document owned by `invoicing`. Provider submission, exchange, reporting, acknowledgements, and reconciliation are external workflows owned by `e_invoicing`. Coupling provider-specific fields and statuses directly into the invoice model would make financial history, retries, and provider changes unsafe.

This ADR defines the integration boundary. It does not select a provider, approve commercial terms, determine customer applicability, or claim regulatory compliance.

## 2. Decision Drivers

- Preserve the authoritative invoice independently of provider availability.
- Implement only current, verified UAE and provider requirements.
- Isolate provider-specific APIs, credentials, statuses, and payloads.
- Prevent duplicate submissions and incorrect success claims.
- Support versioned validation, evidence, reconciliation, and provider change.
- Enforce tenant, legal-entity, authorization, and sensitive-data boundaries.
- Keep network operations outside long-running database transactions.

## 3. Options Considered

### Option A: Dedicated `e_invoicing` domain with provider adapters

The invoice domain publishes an eligible immutable snapshot to a durable submission workflow. Provider adapters translate the canonical submission contract into verified provider contracts.

**Advantages:** clear ownership, provider isolation, reliable retries, evidence retention, and reduced impact of provider change.

**Disadvantages:** canonical mapping, adapter tests, operation records, and reconciliation add complexity.

### Option B: Provider calls inside `invoicing`

**Advantages:** fewer components initially.

**Disadvantages:** couples invoice lifecycle to network availability, spreads provider logic, and complicates retries and provider replacement.

### Option C: Direct government integration by default

**Advantages:** may appear to remove an intermediary.

**Disadvantages:** must not be assumed where the official framework requires or expects an accredited-provider route; it risks implementing a nonexistent or unsupported contract.

### Option D: Generic interchangeable provider API

**Advantages:** simple conceptual abstraction.

**Disadvantages:** providers differ in authentication, onboarding, schemas, statuses, idempotency, callbacks, limits, retention, and support obligations. False interchangeability is unsafe.

## 4. Decision

Create a dedicated `e_invoicing` application boundary. It owns provider configuration references, canonical submission snapshots, validation outcomes, submission operations and attempts, provider-status mapping, acknowledgements, callbacks, and reconciliation.

`invoicing` owns invoices and credit notes. `e_invoicing` must not silently rewrite an issued invoice in response to a provider result. Corrections use the approved invoice/credit-note lifecycle under ADR-011 and then create the appropriate new or linked e-invoicing operation.

### 4.1 Regulatory source control

Before implementing or changing regulated behavior, record:

- Official source and stable reference.
- Date reviewed.
- Applicable decision, guideline, schema, or mandatory-field version.
- Effective date and applicability conditions.
- Reviewer and approval evidence.
- Provider contract version and environment.

The Ministry of Finance portal is the authoritative starting point for UAE e-invoicing programme material. Provider marketing content is not sufficient regulatory evidence.

### 4.2 Provider selection

Provider selection is a separate product, security, legal, commercial, and operational decision. At selection and before production activation, verify the provider's current status against the Ministry of Finance's official ASP information and validate the exact contracted capabilities.

The platform must not hardcode a provider named in a time-sensitive list merely because it appeared there during drafting.

### 4.3 Canonical submission contract

The `e_invoicing` domain maintains a versioned canonical submission representation containing only approved required data, including stable source references, tenant and legal entity, document type, parties, line and tax snapshots, totals, currency, correction references, schema/rule versions, and payload hash as applicable.

The canonical representation is not claimed to be identical to every provider payload. Each adapter maps it to a selected, verified provider contract and records mapping limitations.

### 4.4 Eligibility and preparation

An owning service determines whether an issued document is eligible using an approved, effective-dated rule set. Preparation must validate required fields and create an immutable submission snapshot before network delivery.

Missing regulatory, tenant, legal-entity, party, tax, or provider configuration must fail before submission and remain visible to authorized users.

### 4.5 Durable workflow

Submission uses a durable operation and transactional outbox under ADR-010:

1. Validate source state and eligibility.
2. Create the versioned snapshot and operation record.
3. Record durable delivery intent in the same transaction.
4. Commit.
5. Dispatch through the provider adapter outside the transaction.
6. Record request evidence, response, mapped status, and attempt.
7. Reconcile uncertain or asynchronous outcomes.

Celery task state is not the authoritative submission status.

### 4.6 Idempotency and uncertain outcomes

Each submission operation has a stable internal idempotency key. Use provider idempotency or duplicate controls where the verified contract supports them.

A timeout, connection failure, or worker crash after sending is an uncertain outcome, not proof of rejection or non-receipt. Query provider status or reconcile through the documented route before resubmitting.

### 4.7 Status mapping

Keep provider-native status and evidence separately from the controlled internal status. The mapping must be versioned and tested. Internal status must distinguish at least prepared, validation failed, queued, in progress, submitted, acknowledged where applicable, accepted where evidenced, rejected, retryable failure, permanent failure, uncertain, and reconciliation required as supported by the actual contract.

Do not represent “sent,” “HTTP 200,” task success, or provider receipt as government acceptance unless authoritative evidence establishes that meaning.

### 4.8 Inbound callbacks

Callbacks must verify provider authenticity using the contracted method, enforce replay controls, retain safe evidence, tolerate duplicates and reordering, and resolve tenant and provider account through trusted configuration rather than an untrusted tenant identifier in the payload.

Unknown, invalid, or conflicting callbacks must be quarantined or rejected safely and remain operationally discoverable.

### 4.9 Credentials and connectivity

Credentials belong in an approved secrets system and are referenced, not stored in ordinary business tables. Separate test and production environments, endpoints, credentials, certificates, and data. Rotation and revocation must not require changing invoice records.

### 4.10 Provider change and portability

Provider adapters implement a common internal interface, but portability is not assumed. A provider change requires capability mapping, historical access planning, credential and onboarding changes, contract tests, cutover/reconciliation, rollback, and review of data-retention responsibilities.

Historical submissions retain their original provider, contract, schema, rule, external reference, and evidence.

### 4.11 Data retention and payloads

Retain the authoritative snapshot, hashes, statuses, identifiers, and evidence required by approved legal and operational policy. Avoid duplicating full sensitive payloads in every attempt. Encrypt and restrict payloads when storage is required.

Exact retention periods remain subject to verified requirements and legal review.

## 5. Rationale

The dedicated boundary protects invoices and accounting from provider volatility and network failure. Durable operations and immutable snapshots make retries and audits explainable. Versioned adapters accommodate real provider differences without claiming that all providers are interchangeable.

## 6. Consequences

### Positive consequences

- Provider failures do not corrupt invoice state.
- Regulatory and provider versions remain traceable.
- Duplicate and uncertain outcomes can be reconciled.
- Provider changes are bounded to adapters and migration workflows.

### Negative consequences and trade-offs

- Requires canonical schemas, adapters, mapping tests, and operational tooling.
- Provider changes still require substantial validation.
- Regulatory monitoring and specialist review are ongoing obligations.
- Secure evidence retention increases storage and governance needs.

### Risks and mitigations

- **Outdated requirements:** dated official-source register and release gate.
- **False success:** evidence-based statuses and reconciliation.
- **Duplicate submissions:** stable idempotency and provider inquiry before retry.
- **Provider lock-in:** adapter boundary, canonical snapshots, and export obligations.
- **Sensitive data exposure:** minimal payloads, encryption, access control, and retention policy.

## 7. Security and Tenant-Isolation Implications

- Provider accounts and credentials are tenant/legal-entity scoped where applicable.
- Submission records, snapshots, callbacks, and exports follow ADR-004.
- Only authorized roles may submit, retry, correct, reconcile, or view sensitive payloads.
- Callback authenticity and tenant mapping are mandatory trust boundaries.
- Support and manual recovery actions are audited.

## 8. Data Integrity and Migration

- Source documents and submission snapshots have stable references and hashes.
- Status transitions follow a controlled state machine.
- Attempts append evidence rather than overwrite history.
- Provider/schema changes require backward-compatible reads of historical records.
- A migration must not reinterpret an old submission using a new rule version.

## 9. Operational Impact

Monitor validation failures, submission latency, uncertain outcomes, provider availability, callback verification failures, duplicate events, reconciliation backlog, expiring credentials/certificates, schema deprecations, and regulatory-source changes. Runbooks must cover provider outage, rejected documents, uncertain delivery, manual reconciliation, and provider cutover.

## 10. Implementation Requirements

1. Select and approve an eligible provider through a separate decision.
2. Maintain a dated regulatory and provider-contract source register.
3. Define canonical submission, snapshot, operation, attempt, and status models.
4. Implement a versioned provider adapter and contract tests.
5. Use outbox delivery, idempotency, callbacks, and reconciliation.
6. Define credential, certificate, environment, retention, and support procedures.
7. Validate document and credit-note behavior with finance and UAE tax reviewers.
8. Prevent compliance or acceptance claims without evidence.

## 11. Validation and Acceptance Criteria

- [ ] Applicable rules, versions, dates, and official sources are recorded.
- [ ] The selected provider's current status and contracted capability are verified.
- [ ] Issued invoice data cannot be silently changed by provider processing.
- [ ] Required fields are validated before network submission.
- [ ] Duplicate delivery and callbacks do not duplicate business effects.
- [ ] Timeouts and uncertain outcomes reconcile before resubmission.
- [ ] Provider and internal statuses remain distinguishable and traceable.
- [ ] Callback authenticity, replay, tenant mapping, and ordering are tested.
- [ ] Historical submissions remain readable after schema or provider change.
- [ ] No test result or network response is misrepresented as regulatory compliance.

## 12. Alternatives Rejected

- Provider logic inside `invoicing` is rejected.
- Direct government API assumptions are rejected without an official contract.
- A provider-neutral façade that hides material differences is rejected.
- Regenerating historical payloads solely from mutable current data is rejected.
- Blind retries after timeout are rejected.

## 13. References

- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- UAE Ministry of Finance e-invoicing portal, reviewed 27 October 2026: https://mof.gov.ae/en/about-us/initiatives/einvoicing/
- UAE Ministry of Finance ASP list, reviewed 27 October 2026: https://mof.gov.ae/en/about-us/initiatives/einvoicing/einvoicing-accredited-service-providers-asps/

Official material must be rechecked at provider selection, implementation, and production release.

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Dedicated `e_invoicing` domain with versioned provider adapters, durable operations, snapshots, and reconciliation.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** The provider-neutral integration boundary is accepted following `ADR_STANDARDS_REVIEW.md`. This does not approve regulatory applicability, dates, schemas, provider accreditation/selection, retention, or compliance claims.

Provider selection, applicability, effective dates, schemas, status meanings, retention, and commercial terms remain unresolved and block production implementation. They do not block adapter-interface and test-specification drafting.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial UAE e-invoicing provider-boundary decision accepted after standards review. |
