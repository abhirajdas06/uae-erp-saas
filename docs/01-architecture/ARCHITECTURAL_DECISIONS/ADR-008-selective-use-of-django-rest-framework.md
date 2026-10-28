# ADR-008: Selective Use of Django REST Framework

| Field | Details |
|---|---|
| ADR ID | ADR-008 |
| Title | Selective Use of Django REST Framework |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / API Lead |
| Reviewers | Architecture, Security, Product, Integration, Development |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-001, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-010, ADR-020 |
| Related Requirements | INT-001–INT-002, IAM-001–IAM-005, TEN-002–TEN-003, NFR-001–NFR-007 |
| Related Documents | `API_STANDARDS.md`, `SYSTEM_ARCHITECTURE.md`, `DJANGO_APP_STRUCTURE.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `EVENT_AND_TASK_PROCESSING.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The primary product interface is proposed as server-rendered Django under ADR-007. The platform will nevertheless need machine interfaces for approved external integrations, provider callbacks, automation, mobile or partner use cases, and selected internal boundaries.

Making every browser interaction a REST API would create unnecessary contracts and duplicate presentation workflows. Avoiding an API framework entirely would lead to inconsistent authentication, serialization, validation, errors, pagination, and schema documentation when machine APIs are required.

## 2. Decision Drivers

- Use APIs only for validated consumers and integration requirements.
- Consistent tenant isolation, authorization, entitlement, and validation.
- Stable contracts and versioning for external consumers.
- Reuse of domain application services across HTML, API, and tasks.
- Safe idempotency, concurrency, webhook, and asynchronous-operation behavior.
- Bounded maintenance and support commitments.

## 3. Options Considered

### Option A: Selective Django REST Framework use

Use DRF for approved REST endpoints and machine contracts; keep ordinary browser UI server-rendered.

**Advantages:** mature authentication and serialization hooks, schema ecosystem, consistent API controls, and no requirement to expose every workflow.

**Disadvantages:** two transport styles require shared service discipline and contract governance.

### Option B: API-first for all functionality

**Advantages:** uniform transport and potential client flexibility.

**Disadvantages:** unnecessary API surface, duplicated browser concerns, larger compatibility burden, and premature client architecture.

### Option C: Ad hoc Django JSON views

**Advantages:** minimal dependency for very small endpoints.

**Disadvantages:** inconsistent errors, validation, authentication, pagination, and documentation at scale.

### Option D: No application APIs

**Advantages:** smallest initial surface.

**Disadvantages:** incompatible with required integrations and future approved consumers.

## 4. Decision

Use Django REST Framework selectively for approved REST APIs where a documented machine consumer or integration requirement exists. Do not create REST endpoints solely because a model or server-rendered page exists.

HTML views, HTMX endpoints, REST APIs, background tasks, and integrations must invoke the same owning application services. Transport code must not implement a competing version of business logic.

### 4.1 Approved API categories

- External customer or partner APIs explicitly included in product scope.
- Provider integration endpoints where REST semantics are appropriate.
- Authenticated machine-to-machine interfaces.
- Mobile or alternate-client APIs after product approval.
- Internal operational APIs with a defined consumer and security boundary.
- Webhook receivers, although provider-specific verification may require specialized views or adapters.

An internal Python call inside the modular monolith should normally use a service interface, not an HTTP API.

### 4.2 Endpoint ownership

The domain owning the operation owns its API endpoint, serializer/schema, permission integration, tests, and documentation. Cross-domain orchestration belongs to an explicit coordinating service.

Serializers are transport schemas, not authoritative business services. Writable fields require explicit allowlists; ownership, tenant, totals, approval status, and other protected fields must not be mass-assigned from client input.

### 4.3 Security sequence

Every protected request must establish, as applicable:

1. API audience and version.
2. Authenticated user or service identity.
3. Authorized tenant context.
4. Tenant membership or service scope.
5. User permission and object scope.
6. Effective module entitlement.
7. Valid business state and input.

Querysets must be tenant-scoped before object lookup so identifiers do not become authorization proof.

### 4.4 Authentication

Authentication is selected per API audience under ADR-005 and ADR-020. Browser session authentication may be used for same-origin application endpoints with CSRF protection. External integrations require separately managed credentials and must not reuse human browser sessions.

The final external authentication methods, token lifetimes, scopes, and rotation policy remain pending security review.

### 4.5 Contracts and errors

Public and integration endpoints require explicit request and response schemas, stable machine-readable error codes, documented validation behavior, and OpenAPI representation where appropriate.

Status codes must distinguish authentication, authorization, not-found, validation, conflict, rate-limit, and server failures without leaking cross-tenant object existence. The final error envelope remains a documented API decision.

### 4.6 Versioning and compatibility

Externally consumed APIs require an approved versioning and deprecation policy under ADR-020. Internal endpoint changes still require consumer analysis; an `internal` label is not permission for uncoordinated breaking changes.

Database models must not be exposed as implicit public contracts.

### 4.7 Collections and performance

Collection endpoints require bounded pagination, explicit filtering and sorting allowlists, query-count review, and protection against unbounded nested serialization. Tenant-aware rate limits and quotas must be defined where abuse or cost risk exists.

### 4.8 Idempotency and concurrency

Retry-sensitive write operations require idempotency keys or an equivalent durable duplicate-protection mechanism. Mutable resources require a documented concurrency strategy when lost updates are material.

Long-running operations should return a durable operation reference and accurate status rather than keeping requests open or claiming success before completion.

### 4.9 Webhooks

Inbound webhooks must verify provider authenticity, retain sufficient evidence, tolerate duplicates and reordering, resolve tenant scope from trusted configuration, and acknowledge only according to the provider contract. Processing should be durably recorded before asynchronous follow-up.

## 5. Rationale

Selective DRF use provides consistent machine interfaces without forcing the entire server-rendered product through REST. Shared domain services keep behavior aligned, while explicit approval of API categories prevents accidental long-term support obligations.

## 6. Consequences

### Positive consequences

- Bounded and intentional API surface.
- Consistent validation, permissions, errors, and documentation.
- Reusable business logic across transports.
- Easier future integration without an API-only product architecture.

### Negative consequences and trade-offs

- Teams must maintain both HTML and API transport conventions.
- Public contracts add compatibility and support obligations.
- Authentication, rate limits, and versioning need later detailed decisions.
- DRF remains a material dependency even if used selectively.

### Risks and mitigations

- **API logic drift:** require application-service reuse and contract tests.
- **Mass assignment:** explicit writable-field allowlists.
- **Cross-tenant lookup:** scope querysets before lookup and add negative tests.
- **Unbounded API growth:** require a named consumer and product owner.
- **Breaking integrations:** OpenAPI diffs, version policy, and compatibility review.

## 7. Security and Tenant-Isolation Implications

- Authentication is not authorization.
- Tenant identifiers and resource UUIDs are not credentials.
- Rate limits, payload limits, input validation, output filtering, and safe error messages are mandatory where applicable.
- Secrets and tokens must not appear in URLs, logs, schemas, or error responses.
- API caches must include tenant, identity or scope, permissions, and representation where relevant.

## 8. Data Integrity and Migration

- API contracts must tolerate staged database migrations and deployment overlap.
- Financial and state-changing endpoints use transactions and domain constraints.
- Idempotency records require defined uniqueness, expiry, and response-replay behavior.
- Schema changes do not automatically justify API breaking changes.

## 9. Operational Impact

Production operations require API metrics, structured logs, tracing or correlation IDs, rate-limit visibility, schema publication controls, credential revocation, deprecation monitoring, and runbooks for failed asynchronous operations and webhook replay.

## 10. Implementation Requirements

1. Approve each API category and consumer before endpoint implementation.
2. Pin DRF and selected OpenAPI tooling through the dependency process.
3. Establish shared authentication, permission, error, pagination, and schema conventions.
4. Require explicit serializer fields and tenant-scoped object lookup.
5. Reuse domain services for state changes.
6. Add idempotency and concurrency controls to applicable writes.
7. Add contract, authorization, tenant-isolation, and performance tests.
8. Maintain an endpoint catalogue with ownership and version status.

## 11. Validation and Acceptance Criteria

- [ ] Every endpoint has a named owner and consumer.
- [ ] No endpoint exists solely because a model exists.
- [ ] Tenant A cannot discover or access Tenant B resources by identifier.
- [ ] Writable fields are explicitly allowlisted.
- [ ] Permission and entitlement failures are tested.
- [ ] Business rules match equivalent HTML and task workflows.
- [ ] Collections are bounded and query behavior is reviewed.
- [ ] Retry-sensitive operations are idempotent.
- [ ] External contracts have schema and compatibility evidence.
- [ ] Webhook authenticity, duplicate delivery, and recovery are tested.

## 12. Alternatives Rejected

- API-first for every product workflow is rejected because it is not required by the primary UI architecture.
- Ad hoc JSON views are rejected for material API surfaces.
- Model serializers with unrestricted fields are rejected.
- Internal HTTP calls between Django apps are rejected as the default modular-monolith interface.
- Browser session credentials are rejected as the default machine-integration mechanism.

## 13. References

- `docs/01-architecture/API_STANDARDS.md`
- `docs/01-architecture/DJANGO_APP_STRUCTURE.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- Django REST Framework: https://www.django-rest-framework.org/
- OpenAPI Specification: https://spec.openapis.org/oas/latest.html
- OWASP API Security: https://owasp.org/www-project-api-security/

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Selective DRF use for approved machine interfaces; server-rendered UI remains primary.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; each API still requires an approved consumer, contract, and security boundary.

This accepted decision governs API scaffolding and dependency use; endpoint implementation remains bounded phase work.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial selective DRF decision accepted after standards review. |
