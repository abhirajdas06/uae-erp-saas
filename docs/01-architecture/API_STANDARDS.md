# API Standards — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | ARCH-API-001 |
| Document | `docs/01-architecture/API_STANDARDS.md` |
| Version | 1.0 |
| Status | Draft — Requires Architecture and Security Review |
| Last Reviewed | 27 October 2026 |
| Applies To | Django application, REST APIs, external integrations, webhooks, and API consumers |
| Primary Stack | Django, Django REST Framework where appropriate, PostgreSQL, Celery, Redis |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DJANGO_APP_STRUCTURE.md`, `DATABASE_DESIGN.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `ENTITLEMENT_ENGINE.md`, `MODULE_DEPENDENCIES.md`, `MULTI_TENANCY.md`, `MODULE_CATALOGUE.md`, `PRODUCT_REQUIREMENTS.md` |

---

# 1. Purpose

This document establishes the API design, implementation, security, and maintenance standards for the UAE ERP SaaS platform.

It defines how application interfaces should be designed so that:

- Internal application components interact through clearly defined service contracts.
- Browser-facing pages and HTMX interactions remain consistent with Django's server-rendered architecture.
- REST APIs provide stable interfaces for external clients and approved integrations.
- Tenant data remains isolated across all request paths.
- Module entitlements and user permissions are enforced consistently.
- Financial operations preserve accounting integrity.
- API errors are predictable and actionable.
- External integrations can recover safely from timeouts, retries, and partial failures.
- Codex-generated code follows the same conventions throughout the project.

This document is an implementation standard, not merely a recommendation list. Requirements marked **MUST** are mandatory unless an approved architectural decision explicitly states otherwise.

## 1.1 Normative language

The following terms have specific meanings:

- **MUST / MUST NOT:** Mandatory requirement.
- **SHOULD / SHOULD NOT:** Strong recommendation that may be overridden with documented justification.
- **MAY:** Optional behavior.
- **TBD:** Decision that must be resolved before the relevant production feature is implemented.

## 1.2 Scope

This document covers:

1. Internal application service interfaces.
2. Django page requests and HTMX endpoints.
3. Versioned REST APIs.
4. Authentication and authorization.
5. Tenant context propagation.
6. Request validation and response formatting.
7. Pagination, filtering, sorting, and searching.
8. API versioning and backward compatibility.
9. Idempotency and concurrency control.
10. Rate limiting and abuse prevention.
11. External integrations and webhooks.
12. API documentation and automated testing.
13. Observability, error handling, and operational requirements.

---

# 2. API Architecture Principles

## 2.1 Modular monolith

The application will initially use a Django modular monolith.

A single deployment may expose multiple interfaces, but business logic must remain within the Django application and its domain-owned modules.

The project MUST NOT introduce microservices solely to create an API boundary.

REST APIs should be introduced when there is a genuine requirement, such as:

- Third-party integrations.
- Mobile or desktop clients.
- External customer integrations.
- Machine-to-machine communication.
- A stable public interface.
- Integration with an approved e-invoicing service provider.

## 2.2 API interaction types

The platform distinguishes five interface types.

| Interface | Primary purpose | Recommended implementation |
|---|---|---|
| Internal application services | Reuse domain operations across modules | Python service functions/classes |
| Server-rendered pages | Standard browser navigation | Django views and templates |
| HTMX endpoints | Partial page updates and interactive forms | Django views returning HTML fragments |
| REST APIs | Structured machine-readable communication | Django REST Framework where justified |
| External callbacks/webhooks | Receive asynchronous events | Dedicated, authenticated Django endpoints |

These interfaces may share domain services, but they MUST NOT duplicate business rules.

### Example

An invoice creation operation may be invoked from:

- A Django form.
- An HTMX request.
- A REST endpoint.
- An approved integration.

All four entry points must ultimately use the same invoice application service.

The service must enforce tenant ownership, module entitlement, user or integration authorization, validation, transaction boundaries, and invoice state rules.

A REST API MUST NOT become the only location where critical business validation occurs.

## 2.3 Architectural flow

The preferred request flow is:

```text
Client
  |
  v
HTTP Request
  |
  v
Request Middleware
  |
  +--> Request ID / Correlation ID
  |
  +--> Authentication
  |
  +--> Active Tenant Context
  |
  v
Endpoint / View / API View
  |
  +--> Input Validation
  |
  +--> Authorization
  |      |
  |      +--> Tenant Membership
  |      +--> Module Entitlement
  |      +--> User or Integration Permissions
  |      +--> Object-Level Access
  |
  v
Application Service
  |
  +--> Domain Validation
  +--> Transaction Management
  +--> Domain State Transitions
  +--> Audit Events
  |
  v
Tenant-Aware Data Access
  |
  v
PostgreSQL
  |
  v
Response Serialization / Template Rendering
  |
  v
HTTP Response
```

The exact order of framework components may differ, but no request may reach protected business operations without the required authorization and validation.

## 2.4 Separation of responsibilities

API views and controllers MUST remain thin.

They are responsible for:

- Reading and validating request input.
- Establishing the appropriate request context.
- Invoking authorization services.
- Calling application services.
- Mapping results and exceptions to HTTP responses.
- Serializing output.

They SHOULD NOT contain:

- Complex accounting calculations.
- Invoice posting logic.
- Stock valuation algorithms.
- Payroll calculations.
- Subscription provisioning workflows.
- Cross-module orchestration that belongs in application services.
- Direct SQL that bypasses established tenant-aware access patterns.
- Repeated copies of domain validation logic.

---

# 3. API Exposure Policy

Not every application operation needs to be exposed as a REST endpoint.

## 3.1 API categories

Every API endpoint MUST be classified as one of the following.

### A. Internal browser interface

Used by the Django frontend.

Examples:

- Customer creation form.
- Invoice editing page.
- Inventory search.
- Dashboard filters.

Implementation:

- Django views and templates.
- HTMX responses where useful.
- Standard Django form validation.
- Django authentication and CSRF protection.

These endpoints do not need to return JSON unless the interaction requires it.

### B. Internal application service

Used by other Django modules.

Examples:

- Creating an accounting journal from a posted invoice.
- Checking whether a module is entitled for a tenant.
- Creating stock movements from a goods receipt.

Implementation:

- Explicit Python service interfaces.
- Typed inputs and predictable return values.
- Transactional boundaries.
- Domain-specific exceptions.

Internal service calls SHOULD NOT make HTTP requests back to the same application merely to invoke another module.

### C. Authenticated REST API

Used by approved clients or integrations.

Examples:

- Customer synchronization.
- External sales order submission.
- Approved reporting integrations.
- Mobile application access if introduced later.

These endpoints MUST use the established authentication, tenant, permission, validation, and API response standards.

### D. Public endpoint

Used for operations that intentionally do not require an authenticated user session.

Examples:

- Public health checks with limited information.
- Public registration initiation.
- Email verification links.
- Password reset initiation.
- Public payment-provider callbacks where the provider has an authenticated callback mechanism.

Public endpoints MUST be explicitly allowlisted.

They MUST NOT expose tenant business data or internal system details.

### E. Provider webhook endpoint

Used to receive events from external systems.

Examples:

- Payment status updates.
- E-invoicing submission results.
- Integration synchronization notifications.

These endpoints MUST use provider-specific authentication or signature verification where supported.

They MUST also enforce replay protection, payload validation, and idempotent processing.

## 3.2 Endpoint exposure register

Before introducing an endpoint, the implementing agent MUST document:

- Endpoint purpose.
- Owning Django app.
- Interface category.
- Intended consumers.
- Authentication method.
- Tenant context requirements.
- Required permissions.
- Module entitlement requirements.
- Request and response schema.
- Data sensitivity.
- Rate limits where applicable.
- Idempotency requirements.
- Audit requirements.
- Relevant tests.

Endpoints MUST NOT be exposed publicly simply because they are technically easy to implement.

---

# 4. REST API Conventions

## 4.1 Base URL

The initial versioned REST API base path is:

```text
/api/v1/
```

Example:

```text
GET /api/v1/customers/
POST /api/v1/customers/
GET /api/v1/customers/{customer_id}/
PATCH /api/v1/customers/{customer_id}/
```

The production hostname is deployment-specific and MUST be configurable.

## 4.2 Versioning strategy

The API will use major-version path versioning.

Example:

```text
/api/v1/
/api/v2/
```

Rules:

1. New public REST APIs MUST use an explicit version.
2. Breaking changes MUST introduce a new major API version or follow an approved deprecation strategy.
3. Existing clients MUST NOT silently receive incompatible response schemas.
4. Security fixes and nonbreaking bug fixes MAY be released without a new major version.
5. Additive response fields are generally nonbreaking, but clients MUST be designed to tolerate unknown fields.
6. Removing fields, changing field meanings, changing authentication requirements, or changing established error semantics may be breaking.
7. Each version MUST have a documented support and deprecation policy.
8. Internal Python service interfaces do not need HTTP-style version prefixes.

The initial policy for API deprecation duration is **TBD**.

Do not invent a fixed support period until the commercial and operational requirements have been approved.

## 4.3 Resource naming

Use plural nouns for collections.

Preferred:

```text
/api/v1/customers/
/api/v1/suppliers/
/api/v1/invoices/
/api/v1/credit-notes/
/api/v1/stock-movements/
```

Avoid:

```text
/api/v1/getCustomers/
/api/v1/createInvoice/
/api/v1/doStockUpdate/
```

Resource paths SHOULD use lowercase, hyphen-separated names where needed.

Examples:

```text
/api/v1/fixed-assets/
/api/v1/e-invoices/
```

## 4.4 HTTP methods

| Method | Intended use | Expected behavior |
|---|---|---|
| GET | Retrieve a resource or collection | Must not change business state |
| POST | Create a resource or execute an explicitly defined action | May change business state |
| PUT | Replace a resource representation | Full replacement semantics |
| PATCH | Partially update a resource | Only permitted fields are updated |
| DELETE | Delete a resource where deletion is allowed | Must enforce lifecycle and retention rules |

### Important restrictions

- GET MUST NOT perform financial or other business mutations.
- DELETE MUST NOT be used to reverse posted accounting entries or erase issued invoices.
- PATCH MUST reject unauthorized fields rather than silently accepting protected changes.
- PUT SHOULD NOT be exposed when its replacement semantics are unnecessary or unsafe.
- Business actions that are not ordinary CRUD operations SHOULD have explicit action endpoints.

Examples:

```text
POST /api/v1/invoices/{invoice_id}/issue/
POST /api/v1/invoices/{invoice_id}/send/
POST /api/v1/invoices/{invoice_id}/void/
POST /api/v1/journals/{journal_id}/post/
POST /api/v1/stock-transfers/{transfer_id}/complete/
```

These actions MUST invoke domain services that enforce valid state transitions.

The exact action set depends on the owning module's approved specification.

## 4.5 Trailing slashes

The project SHOULD use trailing slashes for collection and resource endpoints.

Examples:

```text
/api/v1/customers/
/api/v1/customers/{customer_id}/
```

The convention MUST be applied consistently.

API clients SHOULD NOT depend on redirects for authenticated or state-changing requests.

---

# 5. Request Standards

## 5.1 Content types

JSON REST endpoints SHOULD accept:

```http
Content-Type: application/json
```

Responses SHOULD use:

```http
Content-Type: application/json
```

File upload endpoints MUST explicitly document their accepted content types, file-size limits, and validation rules.

Django HTML and HTMX endpoints MAY accept form-encoded or multipart requests according to their interface requirements.

The API MUST reject unsupported content types with an appropriate HTTP status.

## 5.2 Character encoding

JSON payloads MUST use UTF-8.

The application MUST correctly support English and Arabic text.

Input validation MUST NOT accidentally remove valid Unicode characters or assume that all user-provided text is ASCII.

## 5.3 Input validation

Validation MUST occur at multiple appropriate layers:

1. Request schema or serializer.
2. Application service.
3. Domain model or database constraint where applicable.

The API serializer MUST validate the external representation.

The application service MUST enforce business rules even if it is called without an HTTP request.

The database MUST enforce applicable uniqueness, referential integrity, and other invariants that must survive concurrent requests.

Examples:

- Invoice dates must comply with the applicable document lifecycle.
- A credit note must reference an eligible source transaction where required.
- A journal must balance before posting.
- A stock transfer must have sufficient eligible stock according to the approved inventory policy.
- A user cannot assign themselves a privileged role without the required authorization.
- A tenant cannot activate a module if mandatory dependencies are unsatisfied.

## 5.4 Unknown and protected fields

Input serializers MUST use explicit field allowlists.

The API MUST NOT accept unrestricted model updates from arbitrary client JSON.

Clients MUST NOT directly control protected fields such as:

```text
tenant
tenant_id
created_by
posted_by
approved_by
created_at
updated_at
is_platform_admin
subscription_status
module_entitlement_status
is_system_generated
```

The actual protected field list depends on the resource.

Where a client is permitted to set a field with a similar name, that permission MUST be explicit and validated.

Attempts to update protected fields SHOULD return a clear validation error.

## 5.5 Server-controlled fields

Fields such as the following SHOULD be generated or assigned by the server:

- Primary identifiers.
- Tenant association.
- Creation timestamps.
- Audit metadata.
- Posting timestamps.
- Approval metadata.
- Authoritative financial totals.
- Subscription and entitlement status.
- Integration processing status.

A client may submit proposed values for business inputs, such as quantities, unit prices, discounts, or tax selections, but the server MUST validate and calculate authoritative results.

For example, a client-submitted invoice total MUST NOT be trusted as the authoritative amount.

---

# 6. Tenant Context and Data Isolation

Tenant isolation is a mandatory security boundary.

## 6.1 Establishing tenant context

Tenant context MUST be established through the approved tenant-resolution mechanism.

For authenticated browser users, this may be based on the active tenant selected from their authorized memberships.

For integrations, it may be established through an authenticated integration identity explicitly associated with a tenant.

A request's tenant context MUST be validated against the authenticated principal.

## 6.2 Client-supplied tenant identifiers

A request parameter such as:

```json
{
  "tenant_id": "another-tenant-id"
}
```

MUST NOT grant access to that tenant.

The server MUST reject unauthorized tenant selection.

Where the API uses tenant-scoped URLs, the tenant identifier MUST be checked against the authenticated principal's permitted tenant scope.

The URL itself is not an authorization mechanism.

## 6.3 Tenant-aware querysets

Every tenant-owned resource endpoint MUST restrict data access to the active authorized tenant.

Conceptual example:

```python
def get_queryset(self):
    tenant = self.request.tenant

    return Customer.objects.filter(
        tenant=tenant,
    )
```

This example is illustrative. The implementation MUST use the project's approved tenant-resolution and data-access patterns.

The application MUST NOT rely on developers remembering to add tenant filters manually in every unrelated code path without architectural safeguards.

## 6.4 Cross-tenant object access

For an endpoint such as:

```text
GET /api/v1/invoices/{invoice_id}/
```

the server MUST verify that the requested invoice belongs to the active tenant and that the user is authorized to access it.

The same rule applies to:

- Nested resources.
- Related-object selectors.
- Bulk operations.
- Export endpoints.
- File downloads.
- Background tasks.
- Search and autocomplete endpoints.
- Report generation.
- Administrative actions.

A guessed UUID MUST NOT bypass tenant isolation.

The application SHOULD return a consistent not-found response for inaccessible cross-tenant objects when revealing their existence would create an information leak.

## 6.5 Tenant context in background processing

Celery tasks MUST receive explicit tenant context where required.

A task MUST NOT infer its tenant from a global mutable variable or the current HTTP request.

Conceptual task input:

```python
{
    "tenant_id": "...",
    "resource_id": "...",
    "correlation_id": "..."
}
```

Before processing, the task MUST validate that the resource belongs to the expected tenant.

The tenant identifier is processing context, not proof of authorization.

The same rule applies to scheduled tasks and integration jobs.

## 6.6 Database-level defense in depth

PostgreSQL Row Level Security (RLS), where implemented, MUST complement application-level authorization.

RLS MUST NOT replace:

- Authentication.
- Tenant membership validation.
- Module entitlement checks.
- User permissions.
- Object-level authorization.

If RLS is enabled, request and task processing MUST establish tenant context safely and reset it at the end of the relevant transaction or connection lifecycle.

The application database role MUST NOT have privileges that unintentionally bypass the intended RLS controls.

RLS implementation details belong in `MULTI_TENANCY.md` and `DATABASE_DESIGN.md`.

---

# 7. Authentication and Authorization

The authoritative authentication and permissions requirements are defined in:

`docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`

This document specifies how those requirements apply to API interfaces.

## 7.1 Authentication

Every protected endpoint MUST authenticate the calling principal.

Supported authentication mechanisms must be selected according to the client type.

| Client type | Preferred approach |
|---|---|
| Browser using Django sessions | Django session authentication |
| Browser using unsafe methods | Session authentication plus CSRF protection |
| Approved machine-to-machine integration | Explicitly configured integration authentication |
| Future mobile or external API client | Approved token or OAuth-based mechanism |
| Payment/e-invoicing provider callback | Provider-supported signature or authenticated callback mechanism |

The project MUST NOT introduce JWT, OAuth, API keys, or another authentication mechanism merely because it is common in other applications.

The mechanism must match the actual client, threat model, credential lifecycle, and operational requirements.

## 7.2 Session authentication and CSRF

For browser sessions:

- Session cookies MUST use appropriate `Secure`, `HttpOnly`, and `SameSite` settings.
- Unsafe browser requests MUST be protected against CSRF.
- State-changing requests MUST NOT be performed through GET.
- Allowed origins and CORS policies MUST be explicit.
- Cross-origin credential use MUST NOT be enabled indiscriminately.

Disabling CSRF protection globally to resolve an API integration issue is prohibited.

## 7.3 Machine authentication

Machine credentials MUST:

- Be associated with an identifiable integration or service principal.
- Have a documented scope and purpose.
- Be stored securely.
- Support revocation and rotation.
- Be limited to the minimum required permissions.
- Be restricted to the appropriate tenant or explicitly approved platform-level scope.

Long-lived credentials MUST NOT be embedded in frontend JavaScript or mobile application source code.

## 7.4 Authorization layers

A protected operation must pass all applicable checks:

```text
Authenticated Principal
        AND
Valid Tenant Context
        AND
Active Tenant / Applicable Account Policy
        AND
Required Module Entitlement
        AND
Satisfied Module Dependencies
        AND
Required User or Integration Permission
        AND
Object-Level Access
        AND
Business Rules
        =
Operation Allowed
```

Not every endpoint requires every check. Public endpoints, platform-only operations, and noncommercial platform functions have different applicable policies.

However, omitting a check MUST be deliberate and documented.

## 7.5 Centralized authorization

Authorization logic MUST use the project's approved permission and entitlement services.

The API MUST NOT implement separate entitlement logic from the rest of the application.

A view MUST NOT assume that a user can access a module simply because:

- The route exists.
- The Django app is installed.
- The user is authenticated.
- The user has a generic staff flag.
- A frontend button is visible.
- The client submits a valid resource ID.

## 7.6 Platform administrator access

Platform-level permissions MUST be distinct from tenant-level roles.

Tenant APIs MUST NOT automatically grant platform administrators unrestricted access to tenant business records.

Support access, impersonation, emergency access, and cross-tenant troubleshooting MUST follow the controls defined in `AUTHENTICATION_AND_PERMISSIONS.md`.

Sensitive access MUST be auditable.

---

# 8. Module Entitlements and API Availability

The platform sells modules according to a configurable commercial model.

An endpoint belonging to a commercial module MUST respect the central entitlement engine.

## 8.1 Endpoint-to-module mapping

Each commercial endpoint MUST declare its owning module.

Example:

| Endpoint | Owning module |
|---|---|
| `/api/v1/customers/` | CRM, according to the approved catalogue |
| `/api/v1/sales-orders/` | SALES |
| `/api/v1/invoices/` | INVOICING |
| `/api/v1/e-invoices/` | E_INVOICING |
| `/api/v1/journals/` | ACCOUNTING |
| `/api/v1/vat-returns/` | VAT |
| `/api/v1/stock-movements/` | INVENTORY |
| `/api/v1/employees/` | HRMS |
| `/api/v1/payroll-runs/` | PAYROLL |

These mappings are illustrative and MUST be reconciled with the approved module ownership and dependency registry.

If an endpoint spans several modules, the implementation MUST define the required entitlements explicitly.

## 8.2 Entitlement evaluation

Before executing a protected commercial operation, the application MUST evaluate the applicable entitlement through the central service.

Conceptual example:

```python
result = evaluate_module_entitlement(
    tenant=tenant,
    module_code="INVOICING",
)

if not result.allowed:
    raise ModuleEntitlementRequired(
        module_code="INVOICING",
        reason_code=result.reason_code,
    )
```

The function and exception names above are illustrative. Codex MUST reuse the interfaces actually defined by `ENTITLEMENT_ENGINE.md` and the implemented application.

## 8.3 Entitlement changes during processing

Long-running tasks MUST NOT assume that an entitlement remains valid indefinitely.

For example, an e-invoicing task queued while a subscription is active may execute after the entitlement has changed.

The application MUST define whether the operation is permitted to continue, be suspended, or enter a recoverable state.

Already-issued invoices and posted accounting records MUST NOT be silently deleted because a subscription expires.

The entitlement engine controls future access; it does not automatically invalidate historical business records.

## 8.4 Error behavior

If a required module is not entitled, the API MUST return the approved error representation with an appropriate status.

The default recommendation is:

```http
HTTP/1.1 403 Forbidden
Content-Type: application/json
```

The error should include a stable code, such as:

```text
MODULE_ENTITLEMENT_REQUIRED
```

The response MAY identify the required module when doing so is safe and useful.

The API MUST NOT expose internal subscription rules, confidential pricing logic, or implementation details unnecessarily.

---

# 9. Standard Response Formats

## 9.1 General response rules

Successful REST responses MUST use consistent JSON structures.

The exact response shape depends on the operation.

A successful response MUST NOT contain a complete Django model object serialized without an explicit field policy.

The API MUST expose only fields required by the intended client.

## 9.2 Resource response

Example:

```json
{
  "data": {
    "id": "8b56d22c-ff52-48f5-a45b-12d9b51b8f75",
    "customer_code": "CUS-000123",
    "name": "Example Trading LLC",
    "status": "active",
    "created_at": "2026-10-27T10:30:00Z"
  },
  "meta": {
    "request_id": "req_example123"
  }
}
```

The identifiers and values are illustrative.

The API SHOULD use UUIDs for public resource identifiers where consistent with the database design.

Resource responses MUST NOT expose internal implementation details such as database table names or unapproved internal identifiers.

## 9.3 Collection response

Example:

```json
{
  "data": [
    {
      "id": "8b56d22c-ff52-48f5-a45b-12d9b51b8f75",
      "customer_code": "CUS-000123",
      "name": "Example Trading LLC"
    }
  ],
  "pagination": {
    "count": 1,
    "next": null,
    "previous": null,
    "page": 1,
    "page_size": 25
  },
  "meta": {
    "request_id": "req_example123"
  }
}
```

The pagination contract must be consistent within a given API version.

The project MUST select and document one implementation rather than mixing unrelated pagination conventions.

## 9.4 Single-object versus list metadata

Metadata MAY be omitted when it adds no meaningful value, but response consistency takes precedence.

If `data`, `pagination`, and `meta` envelopes are adopted, they MUST be implemented consistently across the relevant API version.

The team MUST NOT introduce a new response envelope for each Django app.

## 9.5 Empty results

An empty collection MUST return a successful response with an empty array.

Example:

```json
{
  "data": [],
  "pagination": {
    "count": 0,
    "next": null,
    "previous": null,
    "page": 1,
    "page_size": 25
  },
  "meta": {
    "request_id": "req_example123"
  }
}
```

A valid request with no matching resources MUST NOT be treated as a server error.

---

# 10. Standard Error Format

## 10.1 Error envelope

Errors MUST use a consistent machine-readable structure.

The recommended structure is:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid fields.",
    "details": {
      "customer_code": [
        "A customer with this code already exists."
      ]
    }
  },
  "meta": {
    "request_id": "req_example123"
  }
}
```

The format may be implemented using Django REST Framework's exception handling and validation mechanisms, but the final external contract MUST remain consistent.

## 10.2 Required error fields

An API error SHOULD include:

- `error.code`: stable machine-readable code.
- `error.message`: safe human-readable explanation.
- `error.details`: optional field-level or operation-level details.
- `meta.request_id`: correlation identifier for troubleshooting.

Stack traces, SQL errors, filesystem paths, secret values, internal tokens, and raw exception messages MUST NOT be returned to clients in production.

## 10.3 Error codes

Error codes MUST be stable and independent of human-readable wording.

Recommended initial codes include:

| Error code | Meaning |
|---|---|
| `VALIDATION_ERROR` | Request data failed validation |
| `AUTHENTICATION_REQUIRED` | Valid authentication is required |
| `PERMISSION_DENIED` | The principal lacks required permission |
| `RESOURCE_NOT_FOUND` | Resource does not exist or is not accessible |
| `MODULE_ENTITLEMENT_REQUIRED` | Required module access is unavailable |
| `MODULE_DEPENDENCY_UNSATISFIED` | Required module dependency is unavailable |
| `TENANT_CONTEXT_REQUIRED` | Required tenant context is missing |
| `INVALID_STATE_TRANSITION` | Requested business operation is not permitted in the current state |
| `IDEMPOTENCY_KEY_REUSED` | An idempotency key was reused with a different request |
| `CONCURRENCY_CONFLICT` | Resource changed concurrently |
| `RATE_LIMIT_EXCEEDED` | Request limit exceeded |
| `RESOURCE_CONFLICT` | Request conflicts with the current resource state |
| `SERVICE_UNAVAILABLE` | Required service is temporarily unavailable |
| `INTERNAL_ERROR` | Unexpected internal error |

The list may expand as modules are implemented.

Error codes MUST NOT encode sensitive internal information.

## 10.4 HTTP status codes

| Status | Usage |
|---|---|
| `200 OK` | Successful retrieval or update returning a representation |
| `201 Created` | Resource successfully created |
| `202 Accepted` | Operation accepted for asynchronous processing |
| `204 No Content` | Successful operation with no response body |
| `400 Bad Request` | Malformed request or general client request error |
| `401 Unauthorized` | Authentication is missing or invalid |
| `403 Forbidden` | Authenticated principal lacks permission or entitlement |
| `404 Not Found` | Resource does not exist or is not accessible |
| `405 Method Not Allowed` | HTTP method is unsupported |
| `406 Not Acceptable` | Requested response representation is unsupported |
| `409 Conflict` | State conflict, duplicate business operation, or concurrency conflict |
| `412 Precondition Failed` | Conditional request precondition failed |
| `413 Content Too Large` | Request or uploaded content exceeds the allowed limit |
| `415 Unsupported Media Type` | Unsupported request content type |
| `422 Unprocessable Content` | Optional use for syntactically valid but semantically invalid requests |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Unexpected server failure |
| `502 Bad Gateway` | Invalid response from an upstream gateway or provider |
| `503 Service Unavailable` | Temporary service unavailability |
| `504 Gateway Timeout` | Upstream dependency timeout |

The implementation MUST use a consistent policy for validation failures, including whether they return `400` or `422`.

For the initial Django REST Framework implementation, `400` is a reasonable default for serializer validation errors. Do not mix the two statuses arbitrarily.

An HTTP `401` response is an authentication challenge; `403` indicates that the request is understood but not permitted. The actual response must follow the selected authentication scheme.

## 10.5 Error handling by domain

Domain errors MUST be translated into safe API responses.

Example:

```text
Application service:
    InvoiceCannotBePosted

API exception handler:
    HTTP 409
    code: INVALID_STATE_TRANSITION
```

The API MUST NOT require clients to parse Python exception names or framework-specific traceback messages.

---

# 11. Pagination, Filtering, Sorting, and Search

## 11.1 Pagination is mandatory for large collections

Collection endpoints MUST implement pagination unless the resource is explicitly bounded and the exception is documented.

The API MUST NOT return unlimited customer, invoice, inventory, employee, or accounting collections by default.

## 11.2 Default and maximum page size

Recommended initial policy:

```text
Default page size: 25
Maximum page size: 100
```

These values are initial defaults and MAY be adjusted through configuration and performance testing.

The server MUST enforce the maximum even if a client requests a larger page.

## 11.3 Pagination strategy

Page-number pagination is appropriate for ordinary administrative screens and collections where count queries are acceptable.

Cursor pagination SHOULD be considered for large or frequently changing datasets, including event feeds and high-volume transaction histories.

The pagination strategy MUST be documented for each endpoint.

Clients MUST NOT assume that all collections support the same pagination parameters unless the contract explicitly guarantees it.

## 11.4 Filtering

Filtering MUST use an explicit allowlist.

Example:

```text
GET /api/v1/invoices/?status=issued&customer_id=<uuid>
```

Supported filters SHOULD be documented per endpoint.

The API MUST NOT expose arbitrary database field lookup expressions directly to clients.

For example, unrestricted client-controlled ORM lookups such as:

```text
?field__icontains=value
```

MUST NOT be accepted as a generic filtering mechanism.

## 11.5 Sorting

Sorting MUST use an allowlist of supported fields.

Example:

```text
GET /api/v1/invoices/?ordering=-issue_date
```

The API MUST reject unsupported ordering fields or handle them according to a documented validation policy.

Sensitive internal fields and expensive joins MUST NOT be exposed for unrestricted sorting.

## 11.6 Search

Search MUST be scoped to the active tenant and the user's authorized data.

Search endpoints MUST enforce appropriate limits and avoid exposing cross-tenant records through autocomplete or partial-match behavior.

Search implementations SHOULD use indexed fields or appropriate PostgreSQL search facilities.

## 11.7 Query performance

Collection endpoints MUST avoid uncontrolled database access.

The implementation SHOULD use:

- `select_related()` for appropriate foreign-key relationships.
- `prefetch_related()` for appropriate reverse and many-to-many relationships.
- Query annotations where useful.
- Indexes based on actual query patterns.
- Explicit response serializers.
- Query-count tests for high-value endpoints.

Serializers MUST NOT trigger uncontrolled per-object database queries.

---

# 12. Data Representation Standards

## 12.1 Identifiers

Public resource identifiers SHOULD use UUIDs, consistent with the database design.

Identifiers MUST be validated before being used to retrieve resources.

The server MUST NOT treat an identifier as proof of authorization.

## 12.2 Dates and timestamps

API timestamps MUST use ISO 8601 representations with explicit timezone information.

Example:

```text
2026-10-27T10:30:00Z
```

Naive timestamps MUST NOT be used in external API responses.

The application SHOULD store event timestamps in UTC and render local times according to the relevant user or organization settings.

## 12.3 Business dates

Business dates and timestamps MUST be distinguished.

Examples:

- Invoice issue date: a business date.
- Payment processing timestamp: an event timestamp.
- VAT tax period: a reporting period.
- Stock movement effective date: a business date subject to the approved inventory rules.

A business date MUST NOT be converted to UTC as though it were a timestamp.

## 12.4 Monetary values

Monetary values MUST be represented as decimal strings in JSON.

Example:

```json
{
  "currency": "AED",
  "subtotal": "1000.00",
  "tax_amount": "50.00",
  "total_amount": "1050.00"
}
```

This avoids binary floating-point representation errors in client applications.

Rules:

- Monetary calculations MUST use decimal arithmetic.
- Binary floating-point types MUST NOT be used for authoritative monetary calculations.
- Currency codes MUST use the approved ISO 4217 representation.
- Currency precision and rounding rules MUST follow the applicable currency and approved accounting policy.
- Tax rounding MUST follow the approved UAE VAT and e-invoicing rules where applicable.
- Clients MUST NOT be trusted to supply authoritative calculated totals.
- Historical transaction amounts MUST preserve the approved transaction snapshot.

## 12.5 Quantities and rates

Quantities, unit prices, percentages, and exchange rates MUST use suitable decimal representations when precision is required.

The precision and scale MUST be defined by the relevant domain model and calculation policy.

## 12.6 Booleans, null values, and enums

The API MUST define whether each field is:

- Required.
- Optional.
- Nullable.
- Read-only.
- Write-only.
- Computed.
- Immutable after a lifecycle transition.

Enums MUST use documented stable machine-readable values.

Example:

```json
{
  "status": "partially_paid"
}
```

Human-readable labels may change independently of the machine-readable values.

Clients MUST NOT rely on display labels as stable identifiers.

## 12.7 Arabic and English

API contracts MUST support Unicode text.

The API MAY return Arabic or English labels according to the documented localization strategy.

Machine-readable identifiers, error codes, and enum values SHOULD remain language-neutral.

The API MUST NOT translate stable codes differently for different locales.

---

# 13. Create, Update, and Delete Semantics

## 13.1 Creation

Create endpoints MUST:

- Validate the request.
- Establish tenant ownership server-side.
- Enforce authorization and module entitlements.
- Apply domain validation.
- Use database constraints for critical invariants.
- Record required audit events.
- Return the created resource or a documented asynchronous-operation response.

## 13.2 Partial updates

PATCH endpoints MUST:

- Accept only approved fields.
- Validate field combinations.
- Reject attempts to modify immutable fields.
- Enforce the current resource lifecycle.
- Prevent unauthorized changes to related objects.
- Use transactions when multiple records must change together.

## 13.3 Deletion policy

Deletion behavior MUST be defined by the resource's lifecycle and retention requirements.

Possible policies include:

- Hard deletion for eligible temporary records.
- Soft deletion where reversible removal is appropriate.
- Archiving for historical records.
- Cancellation or voiding for business documents.
- Reversal entries for posted financial transactions.
- Retention under legal or regulatory obligations.

These policies MUST NOT be applied uniformly without regard to domain requirements.

## 13.4 Financial resources

Issued invoices, posted accounting entries, completed stock movements, and finalized payroll records MUST NOT be silently rewritten or deleted.

Corrections MUST use the applicable business process, such as:

- Credit notes.
- Reversal journals.
- Corrective stock movements.
- Payroll adjustments.
- Approved amendment workflows.

The exact correction process belongs to the owning module specification.

---

# 14. Idempotency and Duplicate Prevention

Idempotency is essential for financial operations and external integrations.

## 14.1 When idempotency is required

Idempotency MUST be implemented for operations where a retry could otherwise create duplicate business effects.

Examples include:

- Invoice issuance.
- Payment initiation.
- External invoice submission.
- Webhook processing.
- Subscription provisioning.
- Stock receipt creation from an external order.
- Integration synchronization.
- Other externally retried financial or provisioning operations.

The owning module specification MUST identify which operations require it.

## 14.2 Idempotency key

For applicable REST POST operations, the API SHOULD accept:

```http
Idempotency-Key: <unique-client-generated-value>
```

The key MUST be scoped appropriately, including the authenticated principal or integration, tenant, and operation.

The storage design MUST prevent concurrent requests from successfully creating duplicate effects for the same idempotency scope.

## 14.3 Request fingerprint

The server SHOULD store a fingerprint of the semantically relevant request input.

If the same idempotency key is reused with a different request, the API MUST reject the request with a stable conflict error.

Example:

```json
{
  "error": {
    "code": "IDEMPOTENCY_KEY_REUSED",
    "message": "The idempotency key was previously used for a different request."
  }
}
```

## 14.4 Idempotency record

An idempotency record SHOULD contain:

- Scope identifier.
- Tenant identifier where applicable.
- Idempotency key.
- Operation identifier.
- Request fingerprint.
- Processing status.
- Resulting resource identifier where available.
- Stored response or sufficient information to reproduce it.
- Creation and expiration timestamps.
- Correlation identifier.

Retention duration is TBD and MUST be defined according to the operation's retry window and operational requirements.

## 14.5 Concurrent requests

The implementation MUST handle two concurrent requests using the same idempotency key.

A process-local Python lock is insufficient for multi-worker production deployments.

Use an appropriate database constraint, transaction strategy, or other shared coordination mechanism.

## 14.6 Idempotency versus business uniqueness

Idempotency keys do not replace domain-level uniqueness constraints.

For example, an invoice may also require a tenant-scoped unique invoice number.

The database and application must enforce the applicable business uniqueness independently.

---

# 15. Concurrency and Conditional Updates

## 15.1 Financial and inventory operations

Operations that affect financial balances, stock quantities, or resource lifecycle transitions MUST be safe under concurrent requests.

The implementation MUST use appropriate combinations of:

- Database transactions.
- Row-level locking.
- Unique constraints.
- Optimistic concurrency controls.
- Conditional updates.
- Idempotency.
- Domain-level conflict detection.

The selected approach MUST match the consistency requirements of the operation.

## 15.2 Optimistic concurrency

Where concurrent edits are likely, the API SHOULD support an explicit concurrency mechanism.

Possible approaches include:

- A resource version field.
- A version number or last-modified value.
- ETags and conditional requests.

Example:

```http
If-Match: "<etag-value>"
```

If the resource has changed since the client retrieved it, the API SHOULD reject the stale update with an appropriate precondition or conflict status.

The API MUST NOT silently overwrite a more recent update when that could cause data loss or violate a business invariant.

## 15.3 Locking

Database locks MUST be acquired within an appropriate transaction.

Lock ordering SHOULD be consistent to reduce deadlock risk.

The implementation MUST NOT hold database locks while making slow network requests to external providers.

## 15.4 State transitions

Financial and operational resources MUST use explicit state-transition services.

For example:

```text
Draft Invoice
    |
    v
Validated Invoice
    |
    v
Issued Invoice
    |
    v
Submitted for E-Invoicing
    |
    v
Accepted / Rejected / Pending / Failed
```

This is an illustrative lifecycle, not a claim that every invoice or provider uses these exact states.

The actual state machine MUST be defined by the relevant module specification and applicable provider or regulatory requirements.

The API MUST reject invalid transitions and return a stable error code.

---

# 16. Asynchronous Operations

## 16.1 When to use asynchronous processing

Long-running or externally dependent operations SHOULD use background processing when synchronous execution would create unreliable response times or poor failure recovery.

Examples:

- E-invoicing submission.
- Bulk imports.
- Large exports.
- Report generation.
- Large synchronization jobs.
- Email delivery.
- High-volume integration processing.

The decision MUST consider the operation's business requirements and user experience.

## 16.2 HTTP response

When an operation is accepted for asynchronous processing, return:

```http
HTTP/1.1 202 Accepted
```

Example:

```json
{
  "data": {
    "operation_id": "5dfc8bc5-20d4-4d1a-9f58-3f0b3b7f81b7",
    "status": "queued",
    "status_url": "/api/v1/operations/5dfc8bc5-20d4-4d1a-9f58-3f0b3b7f81b7/"
  },
  "meta": {
    "request_id": "req_example123"
  }
}
```

An operation-status endpoint SHOULD expose only information the caller is authorized to access.

The response MUST NOT imply that an operation has completed merely because it was queued.

## 16.3 Operation status

Where a generic operation resource is implemented, its lifecycle SHOULD use documented stable values, for example:

```text
queued
running
succeeded
failed
cancelled
```

Additional states MAY be introduced where necessary.

The operation model MUST distinguish transient infrastructure failures from permanent business failures where useful.

## 16.4 Task execution

Celery tasks MUST:

- Be safe to retry where retries are enabled.
- Carry sufficient context to identify the operation and tenant.
- Validate resource ownership.
- Enforce appropriate business and authorization policies.
- Use idempotency for externally observable side effects.
- Record processing outcomes.
- Apply bounded retry policies.
- Avoid logging secrets or sensitive payloads.
- Support failure diagnosis.

The task MUST NOT rely on request-local state from the original HTTP request.

## 16.5 Transactional outbox

For operations that must reliably publish an event after a database transaction, the platform SHOULD use the transactional outbox pattern.

The business change and outbox record SHOULD be committed atomically.

A separate worker can publish or process the event.

This avoids relying on an unreliable sequence such as:

1. Commit a business transaction.
2. Publish a message.
3. Assume both operations succeeded.

The outbox implementation MUST account for duplicate delivery.

Consumers MUST be idempotent.

---

# 17. Rate Limiting and Abuse Prevention

## 17.1 Rate limiting policy

Rate limits MUST be defined according to endpoint sensitivity and expected usage.

The policy SHOULD distinguish:

- Anonymous requests.
- Authenticated user requests.
- Integration requests.
- Login and password-reset requests.
- Expensive reports and exports.
- File uploads.
- Sensitive financial operations.
- Provider callbacks.

The final numeric limits are TBD and MUST be established using security requirements and performance testing.

## 17.2 Rate limit scope

Rate limits SHOULD be enforceable by appropriate combinations of:

- Authenticated principal.
- Integration credential.
- Tenant.
- Endpoint category.
- Source IP where appropriate.
- Resource or operation type.

IP-only rate limiting is insufficient for authenticated, multi-tenant workloads.

## 17.3 Rate limit responses

When a request exceeds the applicable limit, the API SHOULD return:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

The response may include a safe retry interval.

The API MUST NOT expose internal rate-limiter implementation details.

## 17.4 Sensitive operations

Login, password reset, verification, authentication-token issuance, and public registration initiation MUST have appropriate abuse-prevention controls.

Bulk exports and expensive report endpoints MUST have controls against resource exhaustion.

Rate limiting MUST NOT be used as a substitute for authorization or input validation.

---

# 18. File Uploads and Downloads

## 18.1 Upload validation

Upload endpoints MUST validate:

- Allowed file types.
- File size.
- File content where applicable.
- Authorization.
- Tenant ownership.
- Storage location and access policy.
- Required malware scanning or security inspection.
- Filename handling.

The application MUST NOT trust the supplied filename or MIME type alone.

## 18.2 Storage

Uploaded business documents SHOULD be stored using the platform's approved file-storage architecture.

The database SHOULD store metadata and references rather than large binary documents unless a documented exception exists.

Private documents MUST NOT be served through publicly accessible URLs without an approved access model.

## 18.3 Downloads

Every protected download MUST validate tenant ownership and permissions.

A user must not gain access to another tenant's attachment by changing a URL or guessing a storage key.

Signed URLs, if used, MUST have appropriate expiry and scope.

## 18.4 Sensitive files

HR, payroll, banking, tax, identity, and financial documents MUST receive the appropriate access controls and retention policy.

Export endpoints MUST be treated as potentially high-risk data-access operations.

---

# 19. Webhooks and External Integrations

## 19.1 Integration boundaries

External integrations MUST be implemented through the approved integration layer or an explicitly designated domain-owned adapter.

Domain services MUST NOT be tightly coupled to provider-specific request formats.

For example, the invoicing domain should not directly depend on a particular e-invoicing provider's HTTP response schema.

A provider adapter should translate between the provider contract and the application's internal model.

## 19.2 Provider adapters

A provider adapter SHOULD define explicit interfaces for:

- Authentication.
- Request serialization.
- Response parsing.
- Error classification.
- Timeout handling.
- Retry eligibility.
- Idempotency.
- Webhook verification.
- Provider status mapping.
- Observability.

Provider-specific logic MUST remain isolated from general business rules.

## 19.3 E-invoicing integration

The UAE e-invoicing integration MUST follow the approved provider integration architecture and validated regulatory requirements.

The application MUST NOT assume:

- Every provider exposes the same API.
- Every invoice follows the same submission lifecycle.
- A successful HTTP response means regulatory acceptance.
- A provider timeout means that submission failed.
- A single provider status maps directly to the final business state.
- Direct communication with a government system is available for every integration flow.

Provider accreditation, applicable dates, technical schemas, submission rules, error handling, and status semantics MUST be verified before production implementation.

The adapter MUST preserve the evidence required by the approved regulatory and operational design.

## 19.4 Webhook authentication

Webhook endpoints MUST verify the strongest supported provider authentication mechanism.

Where the provider supports signed payloads, the implementation MUST validate signatures using the provider's documented method.

It MUST NOT invent a custom signature algorithm and assume the provider supports it.

Verification MUST account for:

- Correct secret or public-key selection.
- Exact bytes used for signature verification.
- Timestamp validation where supported.
- Replay prevention.
- Key rotation.
- Constant-time comparison where applicable.
- Provider-specific request requirements.

Unsigned callbacks MUST NOT be trusted merely because they contain a plausible resource identifier.

If a provider does not support signed callbacks, the integration MUST use another documented verification mechanism, such as authenticated polling or independent status verification.

## 19.5 Webhook idempotency

Webhook processing MUST tolerate duplicate deliveries.

The application SHOULD persist provider event identifiers and enforce uniqueness within the correct provider or integration scope.

If the provider does not supply a unique event identifier, the adapter MUST define a documented duplicate-detection strategy.

The implementation MUST distinguish:

- Receipt of the event.
- Successful authentication.
- Successful validation.
- Acceptance into the processing queue.
- Completion of business processing.

## 19.6 Webhook acknowledgement

The application SHOULD acknowledge a verified and durably accepted event promptly, then process complex business logic asynchronously where appropriate.

It MUST NOT acknowledge an event as successfully accepted before the required durable persistence or queueing operation has succeeded.

If durable acceptance fails, the endpoint MUST return an appropriate failure response so the provider can retry according to its documented policy.

## 19.7 Outbound HTTP requests

Outbound provider requests MUST use:

- Explicit connection and read timeouts.
- Bounded retries.
- Exponential backoff with jitter where appropriate.
- Idempotency for retryable state-changing operations where supported.
- Safe error classification.
- Credential redaction.
- Correlation identifiers.
- TLS certificate verification.
- Response schema validation.

The application MUST NOT retry a non-idempotent financial operation blindly after an ambiguous timeout.

It should first use the provider's idempotency mechanism or status-reconciliation process.

## 19.8 SSRF protection

If users can configure external callback URLs or integration endpoints, the implementation MUST consider server-side request forgery.

Controls SHOULD include:

- Restricting supported schemes.
- Rejecting loopback, link-local, private, and otherwise prohibited destinations where appropriate.
- Validating resolved IP addresses.
- Revalidating redirects.
- Restricting outbound network access where feasible.
- Preventing access to cloud metadata endpoints.
- Avoiding arbitrary user-controlled URL fetching.

The exact policy MUST match the integration configuration model and deployment environment.

---

# 20. API Security Requirements

## 20.1 Security baseline

All REST APIs MUST follow the security controls defined in:

`docs/05-quality/SECURITY_REQUIREMENTS.md`

The API implementation MUST also follow:

- `AUTHENTICATION_AND_PERMISSIONS.md`
- `ENTITLEMENT_ENGINE.md`
- `MULTI_TENANCY.md`
- `DATABASE_DESIGN.md`

## 20.2 Required controls

Protected endpoints MUST enforce applicable controls for:

- Authentication.
- Tenant isolation.
- Authorization.
- Module entitlements.
- Input validation.
- Output field restrictions.
- CSRF protection where session authentication is used.
- Rate limiting.
- Audit logging.
- Secure error handling.
- Secret management.
- File access.
- Concurrency.
- Abuse prevention.

## 20.3 Mass assignment

The API MUST NOT permit clients to update arbitrary model fields through unrestricted deserialization.

Writable fields MUST be explicitly defined.

## 20.4 Object-level authorization

Every endpoint receiving a resource identifier MUST evaluate authorization for that specific resource.

Collection-level permission does not automatically imply permission to access every object in the collection.

Nested resources MUST be validated against their parent resource and tenant.

## 20.5 Injection protection

The application MUST use safe ORM operations or appropriately parameterized queries.

Raw SQL MUST NOT concatenate untrusted input into executable SQL.

Dynamic sort expressions, filters, table names, and identifiers MUST be validated against explicit allowlists.

## 20.6 CORS

CORS MUST be configured for known, approved origins only.

The application MUST NOT use a wildcard origin with credentials.

CORS is a browser security mechanism and MUST NOT be treated as API authentication.

## 20.7 Security headers and transport

Production APIs MUST be served over HTTPS.

The deployment MUST configure appropriate transport security and response headers.

Sensitive responses SHOULD use appropriate cache-control directives, including `Cache-Control: no-store` where required.

## 20.8 API schema exposure

API documentation and schema endpoints MUST follow the approved access policy.

Internal-only endpoints MUST NOT become public merely because automatic schema generation includes them.

Production debugging and interactive schema tools MUST be secured or disabled according to the deployment policy.

---

# 21. Auditability and Financial Integrity

## 21.1 Auditable operations

The API MUST generate appropriate audit events for sensitive business actions.

Examples include:

- Invoice issuance.
- Credit-note issuance.
- Journal posting.
- Period closing.
- Payroll finalization.
- E-invoicing submission.
- Payment initiation.
- Stock adjustments.
- Permission changes.
- Module activation or deactivation.
- Data exports.
- Privileged support access.

The audit design MUST follow the platform's audit requirements.

## 21.2 Audit event contents

Where appropriate, audit events SHOULD capture:

- Tenant.
- Actor or integration identity.
- Action.
- Resource type and identifier.
- Timestamp.
- Correlation ID.
- Outcome.
- Relevant before-and-after values or a controlled change summary.
- Source context.
- Related business operation identifier.

Audit logs MUST NOT contain passwords, access tokens, secrets, or unnecessary sensitive payloads.

## 21.3 Financial transaction boundaries

Financial API operations MUST use appropriate database transactions.

A posted financial transaction MUST NOT be treated as successful until the required durable database changes have committed.

If the operation also requires external processing, the API MUST distinguish the committed local business state from the external provider state.

## 21.4 External side effects

External network requests MUST NOT occur inside long-running database transactions without a documented justification.

The preferred pattern is:

1. Validate the request.
2. Commit the required local state and durable work record.
3. Execute the external operation asynchronously where appropriate.
4. Record the provider result.
5. Reconcile ambiguous or failed outcomes.
6. Expose the resulting status to authorized clients.

The exact pattern depends on the business operation and must preserve its consistency requirements.

---

# 22. API Documentation

## 22.1 OpenAPI

Versioned REST APIs SHOULD be documented using OpenAPI.

The implementation SHOULD use the OpenAPI tooling approved for the project's Django REST Framework setup.

The selected library and version MUST be pinned in project dependencies.

## 22.2 Required endpoint documentation

Each endpoint MUST document:

- Purpose.
- HTTP method and path.
- Owning module.
- Authentication requirements.
- Tenant context.
- Permissions.
- Module entitlements.
- Path parameters.
- Query parameters.
- Request body.
- Response schema.
- Error responses.
- Pagination behavior.
- Idempotency behavior.
- Rate limits where relevant.
- Side effects.
- Audit behavior.
- Asynchronous processing behavior.
- Deprecation status where applicable.

## 22.3 Examples

Important endpoints SHOULD include representative examples for:

- Successful responses.
- Validation failures.
- Authorization failures.
- State conflicts.
- Asynchronous operations.
- Retryable integration errors.

Examples MUST use synthetic data and MUST NOT include real credentials or customer information.

## 22.4 Schema validation

The API schema MUST be generated from or validated against the actual implementation.

The project SHOULD include CI checks for schema generation and validation.

Changes that unintentionally break the documented API contract MUST fail the relevant checks.

## 22.5 Internal services

Internal Python services MUST have clear signatures, type annotations where practical, docstrings for nontrivial behavior, and explicit exception contracts.

They do not need to be published as OpenAPI endpoints.

---

# 23. API Testing Strategy

Every API implementation MUST include appropriate automated tests.

The testing strategy is defined in `docs/05-quality/TESTING_STRATEGY.md`.

## 23.1 Unit tests

Unit tests SHOULD cover:

- Request validation rules where independently testable.
- Response mapping.
- Domain exception mapping.
- Serialization behavior.
- Permission decision helpers.
- Provider response parsing.
- Idempotency key validation.
- Status mapping.

## 23.2 Integration tests

Integration tests MUST cover:

- Authentication.
- Tenant resolution.
- Tenant-scoped queryset behavior.
- Module entitlements.
- User permissions.
- Database constraints.
- Transaction behavior.
- Idempotency.
- Concurrency-sensitive operations.
- Background-task integration.
- Webhook verification.
- API error formatting.

## 23.3 Cross-tenant tests

For every tenant-owned resource category, tests MUST verify that a user in Tenant A cannot:

- Retrieve Tenant B's resource.
- Modify Tenant B's resource.
- Delete or cancel Tenant B's resource.
- Access its attachments.
- Access it through nested resources.
- Discover it through search.
- Export it through reports.
- Trigger unauthorized operations against it.
- Access it through an asynchronous operation.

Where appropriate, tests SHOULD cover both direct resource identifiers and related-object references.

## 23.4 Permission and entitlement tests

Tests MUST verify that:

- An unauthenticated principal cannot access protected endpoints.
- A user without the required permission is denied.
- A user with the permission but without the required module entitlement is denied.
- A user with entitlement but without object-level access is denied.
- A valid authorized user can perform the operation.
- Expired or suspended subscription behavior follows the approved policy.
- Changes in module dependencies are reflected in entitlement evaluation.
- Platform-only permissions do not leak into tenant-level permissions.

## 23.5 Financial tests

Financial endpoints MUST test:

- Decimal precision.
- Tax calculation and rounding.
- Transaction rollback.
- Duplicate submissions.
- Concurrent posting attempts.
- Invalid state transitions.
- Immutability of posted records.
- Audit event creation.
- Failure handling for external dependencies.
- Recovery after ambiguous provider responses.

## 23.6 Contract tests

The project SHOULD include tests that verify response schemas and compatibility with the published OpenAPI contract.

External provider adapters SHOULD have contract tests based on official provider documentation and approved test environments.

Mocks MAY be used for unit tests, but they MUST NOT be the only evidence that an external integration works.

## 23.7 Test isolation

Tests MUST NOT use production data or real production credentials.

External API calls MUST be isolated from ordinary automated tests unless an explicitly controlled integration-test environment is used.

---

# 24. Performance and Reliability

## 24.1 Response-time targets

The project MUST establish measurable performance targets before production launch.

The targets SHOULD distinguish:

- Ordinary CRUD operations.
- Complex reporting queries.
- Large exports.
- External provider operations.
- Asynchronous job submission.
- Background processing completion.

Initial numeric targets remain TBD pending expected user counts, traffic patterns, infrastructure sizing, and load testing.

## 24.2 Database efficiency

API endpoints MUST avoid:

- Unbounded result sets.
- Uncontrolled N+1 queries.
- Unnecessary full-table scans.
- Excessive serialization.
- Expensive synchronous exports.
- Long-running transactions.
- Unindexed tenant-scoped lookups.

Performance-sensitive queries SHOULD be measured with realistic data volumes.

## 24.3 Timeouts

HTTP clients, database operations, background jobs, and upstream integrations MUST have appropriate timeout policies.

A request timeout MUST NOT automatically be interpreted as proof that a business transaction failed.

The application MUST provide a reconciliation path for operations whose completion is uncertain.

## 24.4 Caching

Caching MUST respect tenant and authorization boundaries.

Sensitive tenant-specific responses MUST NOT be cached under a key that allows reuse by another tenant or principal.

Authorization and entitlement caches MUST follow the invalidation and freshness requirements in the entitlement and authentication architecture documents.

Caching MUST NOT bypass current permissions for sensitive financial operations.

## 24.5 Availability and graceful degradation

The API SHOULD distinguish required dependencies from optional dependencies.

If a noncritical analytics integration is unavailable, unrelated core invoice operations SHOULD remain available where architecturally safe.

If an operation requires a provider that is unavailable, the API MUST return a clear, recoverable error or accept the operation asynchronously according to its business contract.

The API MUST NOT report false success merely to hide dependency failures.

---

# 25. Logging and Observability

## 25.1 Correlation identifiers

Every API request SHOULD receive a server-generated request ID.

If a client supplies a correlation ID, the application MAY accept it after validating its length and format.

Client-supplied identifiers MUST NOT be trusted as authorization data.

The server-generated request ID MUST be included in logs and SHOULD be returned in response metadata.

Example:

```json
{
  "meta": {
    "request_id": "req_example123"
  }
}
```

## 25.2 Structured logs

Production API logs SHOULD be structured and include relevant fields such as:

- Timestamp.
- Request ID.
- Correlation ID.
- HTTP method.
- Normalized route.
- Status code.
- Duration.
- Tenant identifier where permitted.
- Authenticated principal identifier where permitted.
- Error code.
- Integration or operation identifier where applicable.

## 25.3 Sensitive information

Logs MUST NOT include:

- Passwords.
- Session cookies.
- Access tokens.
- API secrets.
- Full payment credentials.
- Private signing keys.
- Unnecessary personal data.
- Unredacted sensitive financial or payroll payloads.

The logging policy MUST support applicable retention and access controls.

## 25.4 Metrics

The platform SHOULD monitor:

- Request volume.
- Response latency.
- Error rates.
- Authentication failures.
- Authorization denials.
- Rate-limit events.
- Database query latency.
- Background job failures.
- Integration timeouts.
- Webhook processing failures.
- Idempotency conflicts.
- Entitlement-related denials.

Metrics MUST NOT expose sensitive tenant information unnecessarily.

---

# 26. Django and Django REST Framework Implementation Standards

## 26.1 Framework policy

Django REST Framework SHOULD be used for endpoints that require structured REST behavior.

Django views and forms SHOULD remain the default for server-rendered browser workflows where a REST API provides no material benefit.

The project MUST NOT introduce a separate API framework without an approved architectural decision.

## 26.2 Serializers

Serializers MUST:

- Declare explicit readable and writable fields.
- Validate external input.
- Avoid unrestricted model-field exposure.
- Avoid hidden database queries where possible.
- Use appropriate decimal and date representations.
- Respect the API's nullability and enum contracts.
- Avoid implementing complex business workflows inside serializer methods.

Complex domain behavior belongs in application services.

## 26.3 Views and viewsets

Views and viewsets MUST:

- Enforce authentication and permissions.
- Establish or validate tenant context.
- Scope querysets correctly.
- Validate request input.
- Invoke application services.
- Map domain outcomes to documented HTTP responses.
- Avoid duplicated business rules.

Generic viewsets MAY be used where their behavior matches the resource's lifecycle.

Custom application services MUST be used for complex state transitions.

## 26.4 Permissions

DRF permission classes MUST be used where appropriate, but framework-level permission checks do not replace domain-level authorization.

The implementation MUST enforce object-level access for individual resources.

The application MUST NOT assume that a list permission automatically provides correct detail-object authorization.

## 26.5 Exception handling

The project SHOULD use a centralized API exception handler to normalize error responses.

The handler MUST preserve safe field-validation details and map known application exceptions to stable error codes.

Unexpected exceptions MUST be logged securely and returned as a generic internal error.

The handler MUST NOT expose stack traces in production.

## 26.6 Transactions

Use `transaction.atomic()` where multiple database changes must succeed or fail together.

The transaction boundary SHOULD be defined by the application service for the business operation.

Do not assume that every HTTP request needs one large database transaction.

External network calls MUST be kept outside long-running transactions where possible.

## 26.7 Django admin

Django admin is an operational interface, not a substitute for the public API.

Admin actions MUST respect tenant and permission safeguards.

A custom API endpoint MUST NOT be introduced merely to reproduce an internal admin action unless there is a genuine client requirement.

## 26.8 Signals

Signals MUST NOT be used as the primary mechanism for complex business workflows that require explicit transaction control or predictable error handling.

Critical financial and provisioning operations SHOULD use explicit application services.

Signals MAY be used for appropriate decoupled side effects when their execution order, transaction behavior, and failure semantics are documented.

## 26.9 Dependency direction

The API layer may depend on application services.

Domain-owned services MUST NOT depend on HTTP request or response objects.

A domain service SHOULD accept explicit arguments rather than reaching into global request state.

---

# 27. Suggested API App Structure

The API structure MUST fit the existing Django app architecture.

A possible implementation is:

```text
apps/
├── core/
├── tenants/
├── users/
├── subscriptions/
├── billing/
├── crm/
├── sales/
├── invoicing/
├── e_invoicing/
├── accounting/
├── vat/
├── inventory/
├── integrations/
└── ...
```

Within an app that exposes REST APIs:

```text
apps/
└── invoicing/
    ├── api/
    │   ├── __init__.py
    │   ├── urls.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── permissions.py
    │   ├── filters.py
    │   └── tests/
    ├── services/
    ├── selectors.py
    ├── models.py
    ├── forms.py
    ├── tasks.py
    ├── admin.py
    ├── urls.py
    └── tests/
```

This is a suggested layout, not a requirement to create empty files in every app.

The team SHOULD avoid unnecessary directory complexity in small modules.

The following separation MUST remain clear:

- API transport logic.
- Domain/application services.
- Data-access patterns.
- Background processing.
- Tests.

---

# 28. Recommended URL Registration

The project MAY register versioned API routes centrally.

Illustrative example:

```python
# config/urls.py

from django.urls import include, path

urlpatterns = [
    path("api/v1/crm/", include("apps.crm.api.urls")),
    path("api/v1/sales/", include("apps.sales.api.urls")),
    path("api/v1/invoicing/", include("apps.invoicing.api.urls")),
    path("api/v1/accounting/", include("apps.accounting.api.urls")),
]
```

Alternatively, resource routes MAY be registered directly under the versioned API namespace.

The project MUST select a consistent URL ownership strategy.

Do not mix multiple routing approaches arbitrarily.

For a central resource-oriented API, the preferred public paths are:

```text
/api/v1/customers/
/api/v1/sales-orders/
/api/v1/invoices/
/api/v1/credit-notes/
/api/v1/journals/
```

The owning Django app can remain an internal implementation detail.

The final route structure MUST be reconciled with the approved module and API catalogue before production clients depend on it.

---

# 29. Example API Contract

The following example illustrates the expected design for a customer creation endpoint.

It is a contract example, not a complete production implementation.

## 29.1 Endpoint

```http
POST /api/v1/customers/
```

## 29.2 Authentication

An authenticated user or integration with appropriate access.

## 29.3 Authorization

The endpoint must verify:

- Valid tenant context.
- Access to the CRM module, if required by the approved module mapping.
- Required customer-creation permission.
- Any applicable object or legal-entity restrictions.

## 29.4 Request

```json
{
  "customer_code": "CUS-000123",
  "name": "Example Trading LLC",
  "email": "accounts@example.invalid",
  "phone": "+971500000000",
  "currency": "AED"
}
```

The example uses a reserved `.invalid` domain and illustrative contact details.

## 29.5 Successful response

```http
HTTP/1.1 201 Created
```

```json
{
  "data": {
    "id": "8b56d22c-ff52-48f5-a45b-12d9b51b8f75",
    "customer_code": "CUS-000123",
    "name": "Example Trading LLC",
    "email": "accounts@example.invalid",
    "phone": "+971500000000",
    "currency": "AED",
    "status": "active",
    "created_at": "2026-10-27T10:30:00Z"
  },
  "meta": {
    "request_id": "req_example123"
  }
}
```

## 29.6 Validation failure

```http
HTTP/1.1 400 Bad Request
```

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid fields.",
    "details": {
      "customer_code": [
        "A customer with this code already exists."
      ]
    }
  },
  "meta": {
    "request_id": "req_example123"
  }
}
```

## 29.7 Authorization failure

```http
HTTP/1.1 403 Forbidden
```

```json
{
  "error": {
    "code": "PERMISSION_DENIED",
    "message": "You do not have permission to perform this operation."
  },
  "meta": {
    "request_id": "req_example123"
  }
}
```

## 29.8 Implementation notes

The server MUST:

- Assign the tenant association.
- Validate customer-code uniqueness within the correct scope.
- Validate allowed currency codes.
- Apply business validation.
- Record required audit events.
- Avoid accepting protected fields from the request.
- Return only authorized fields.
- Enforce the applicable module entitlement and user permission.

The endpoint MUST NOT trust the client to establish tenant ownership.

---

# 30. API Change Management

## 30.1 Change classification

Every API change MUST be classified as one of the following.

### Nonbreaking change

Examples may include:

- Adding an optional request field.
- Adding a response field.
- Adding an endpoint.
- Adding an optional query parameter.

The team MUST still assess whether existing clients, generated SDKs, serializers, or schema validators could be affected.

### Potentially breaking change

Examples include:

- Changing field types.
- Changing field meanings.
- Changing validation rules.
- Changing status codes relied upon by clients.
- Changing pagination behavior.
- Changing default sorting.
- Changing authentication or authorization requirements.
- Tightening an existing request contract.

These changes require compatibility analysis.

### Breaking change

Examples include:

- Removing fields.
- Renaming fields.
- Removing endpoints.
- Changing established response structures.
- Changing required fields in a way that breaks existing clients.
- Changing a resource's identity or lifecycle contract.

Breaking changes MUST follow the approved versioning and deprecation strategy.

## 30.2 Database migrations

An API change that requires a database migration MUST consider compatibility between the existing code, the migration, background workers, and concurrent requests.

Production deployment SHOULD favor expand-and-contract migrations when a direct change would break running code.

## 30.3 API contract review

Pull requests affecting public or integration APIs MUST document:

- Contract changes.
- Compatibility impact.
- Security impact.
- Tenant-isolation impact.
- Entitlement impact.
- Database migration requirements.
- Test evidence.
- Documentation changes.

## 30.4 Deprecation

Deprecated endpoints MUST have a documented replacement and retirement plan.

Deprecation metadata or response headers MAY be used where appropriate.

The deprecation period MUST be consistent with the approved client support policy.

---

# 31. API Implementation Acceptance Criteria

An API feature MUST NOT be considered complete until all applicable criteria are satisfied.

## 31.1 Functional acceptance

- [ ] Endpoint purpose and ownership are documented.
- [ ] HTTP method and URL follow the established conventions.
- [ ] Request schema is defined.
- [ ] Response schema is defined.
- [ ] Validation rules are implemented.
- [ ] Error codes and HTTP statuses are consistent.
- [ ] Pagination is implemented where required.
- [ ] Filtering and sorting are explicitly allowlisted.
- [ ] Business logic is implemented in the appropriate service layer.
- [ ] The endpoint respects the resource lifecycle.

## 31.2 Security acceptance

- [ ] Authentication is configured correctly.
- [ ] Tenant context is validated.
- [ ] Cross-tenant access is prevented.
- [ ] Module entitlement is enforced where required.
- [ ] User or integration permissions are enforced.
- [ ] Object-level access is enforced.
- [ ] Protected fields cannot be modified through mass assignment.
- [ ] Sensitive data is not exposed in responses.
- [ ] Rate limiting is applied where required.
- [ ] Errors and logs do not expose secrets.
- [ ] File access and exports are authorized.
- [ ] CSRF and CORS policies are appropriate to the client type.

## 31.3 Data-integrity acceptance

- [ ] Database constraints protect critical invariants.
- [ ] Transactions cover related changes where required.
- [ ] Concurrency-sensitive operations are safe.
- [ ] Idempotency is implemented where required.
- [ ] Financial calculations use appropriate decimal arithmetic.
- [ ] Posted or finalized records follow immutable lifecycle rules.
- [ ] Audit events are generated where required.
- [ ] External side effects have appropriate failure and recovery behavior.

## 31.4 Quality acceptance

- [ ] Unit tests pass.
- [ ] Integration tests pass.
- [ ] Cross-tenant tests pass.
- [ ] Authorization and entitlement tests pass.
- [ ] Contract documentation is updated.
- [ ] API schema generation and validation pass.
- [ ] Performance risks are assessed.
- [ ] Logs and metrics are sufficient for troubleshooting.
- [ ] Relevant quality and security checks pass in CI.

---

# 32. API Requirement Traceability

The following IDs are introduced by this document.

They MUST be added to the project's requirements traceability matrix when that matrix is established.

| Requirement ID | Requirement | Priority |
|---|---|---|
| API-001 | API endpoints MUST follow the approved interface classification and ownership model. | MUST |
| API-002 | Protected endpoints MUST enforce authentication and applicable authorization. | MUST |
| API-003 | Tenant-owned resources MUST enforce tenant isolation. | MUST |
| API-004 | Commercial module endpoints MUST respect the central entitlement engine. | MUST |
| API-005 | REST endpoints MUST use consistent request, response, and error contracts. | MUST |
| API-006 | Public resource identifiers MUST NOT be treated as authorization proof. | MUST |
| API-007 | Request validation MUST use explicit writable-field allowlists. | MUST |
| API-008 | Monetary values MUST use appropriate decimal representations. | MUST |
| API-009 | Financial operations MUST preserve transaction integrity and valid state transitions. | MUST |
| API-010 | Retry-sensitive operations MUST implement appropriate idempotency controls. | MUST |
| API-011 | Collection endpoints MUST use appropriate pagination or a documented exception. | MUST |
| API-012 | Filtering and sorting MUST use explicit allowlists. | MUST |
| API-013 | External integrations MUST handle authentication, timeouts, errors, and retries safely. | MUST |
| API-014 | Webhook processing MUST verify authenticity and tolerate duplicate delivery. | MUST |
| API-015 | API errors MUST use stable machine-readable codes. | MUST |
| API-016 | API implementations MUST include automated authorization and tenant-isolation tests. | MUST |
| API-017 | Public and integration APIs MUST be documented using the approved contract format. | SHOULD |
| API-018 | API changes MUST be assessed for backward compatibility. | MUST |
| API-019 | API logging MUST support troubleshooting without exposing secrets. | MUST |
| API-020 | Long-running operations MUST expose an accurate processing status where asynchronous execution is used. | MUST |
| API-021 | Sensitive endpoints MUST have appropriate rate limits and abuse controls. | MUST |
| API-022 | API performance MUST be measured against approved operational targets. | MUST |
| API-023 | API caching MUST preserve tenant and authorization boundaries. | MUST |
| API-024 | Cross-module business operations MUST use explicit application services rather than duplicated transport-layer logic. | MUST |

---

# 33. Pending Decisions

The following decisions require explicit resolution before the affected behavior is finalized.

| Decision ID | Decision | Proposed Owner |
|---|---|---|
| API-DEC-001 | Select and pin the OpenAPI documentation library. | Architecture |
| API-DEC-002 | Confirm the standard JSON success and error envelope. | Architecture |
| API-DEC-003 | Confirm whether validation failures use `400`, `422`, or a documented combination. | Architecture |
| API-DEC-004 | Finalize the pagination implementation and maximum page size. | Architecture |
| API-DEC-005 | Define API deprecation and version support periods. | Product and Architecture |
| API-DEC-006 | Select authentication mechanisms for external integrations. | Security and Architecture |
| API-DEC-007 | Define initial rate limits and per-tenant quotas. | Security and Operations |
| API-DEC-008 | Define idempotency storage, scope, and retention periods. | Architecture |
| API-DEC-009 | Define API performance and availability targets. | Product and Operations |
| API-DEC-010 | Confirm the public API exposure policy and endpoint catalogue. | Product and Architecture |
| API-DEC-011 | Define provider-specific webhook verification requirements. | Integration Owner |
| API-DEC-012 | Finalize API schema publication and access controls. | Security and Architecture |
| API-DEC-013 | Confirm the approved concurrency mechanism for mutable resources. | Architecture |
| API-DEC-014 | Define the operation-status resource and asynchronous API contract. | Architecture |
| API-DEC-015 | Finalize response localization and error-message language policy. | Product and Architecture |

These decisions MUST NOT block unrelated implementation where a safe, documented default is available.

However, unresolved security, financial-integrity, or regulatory decisions MUST block production release of affected features.

---

# 34. Instructions for Codex and Development Agents

All agents modifying API-related code MUST follow this document.

## 34.1 Before implementation

The agent MUST:

1. Read `AGENTS.md`.
2. Read `DJANGO_APP_STRUCTURE.md`.
3. Read `AUTHENTICATION_AND_PERMISSIONS.md`.
4. Read `ENTITLEMENT_ENGINE.md`.
5. Read `MULTI_TENANCY.md`.
6. Read `MODULE_DEPENDENCIES.md`.
7. Read the owning module specification.
8. Identify the endpoint's tenant, permission, entitlement, and data-integrity requirements.
9. Inspect existing API patterns before creating new ones.
10. Document unresolved decisions that materially affect implementation.

The agent MUST NOT assume that an endpoint, helper, model, serializer, or permission service exists merely because it is described conceptually in this document.

## 34.2 During implementation

The agent MUST:

- Follow established URL and naming conventions.
- Reuse existing application services.
- Avoid duplicating domain logic.
- Apply explicit request and response schemas.
- Scope tenant-owned queries correctly.
- Use the central authorization and entitlement mechanisms.
- Protect sensitive fields.
- Use appropriate transactions and database constraints.
- Implement idempotency where required.
- Document external side effects and retry behavior.
- Add automated tests.
- Update OpenAPI documentation where applicable.
- Avoid introducing new dependencies without justification.

The agent MUST NOT:

- Trust client-supplied tenant identifiers.
- Trust client-submitted calculated financial totals.
- Expose unrestricted model serializers.
- Bypass permission checks in background tasks.
- Suppress errors to make tests pass.
- Disable CSRF globally.
- Return stack traces in production.
- Implement unverified regulatory or provider assumptions.
- Create a separate business rule implementation for the REST API.
- Mark a feature complete when its acceptance criteria remain unmet.

## 34.3 After implementation

The agent MUST provide evidence of:

- Files changed.
- Endpoint contract changes.
- Authorization and tenant-isolation behavior.
- Tests executed and results.
- Schema or documentation changes.
- Database migration impact.
- Known limitations.
- Outstanding decisions.
- Any security or regulatory assumptions requiring review.

An agent MUST report incomplete work honestly.

It MUST NOT claim that tests, security reviews, integration tests, or production validation passed unless the relevant checks were actually performed.

---

# 35. Definition of Done

`API_STANDARDS.md` and the API implementation process are considered operationally established when:

1. The architecture review approves the standard.
2. The response and error contracts are finalized.
3. The selected OpenAPI tooling is configured.
4. A representative endpoint demonstrates the standard.
5. Authentication and tenant-isolation tests are in place.
6. Module entitlement enforcement is integrated.
7. Error mapping is centralized.
8. Pagination and filtering conventions are implemented.
9. Idempotency and concurrency patterns are documented and tested for applicable operations.
10. Webhook and provider integration requirements are documented.
11. CI validates tests and the API schema.
12. Codex follows the standard for new endpoints.
13. The requirements traceability matrix references the API requirement IDs.
14. Production-readiness checks cover security, performance, logging, and failure recovery.

Approval of this document does not itself mean that any API endpoint is implemented or production-ready.

---

# 36. Final Architectural Rule

**An API endpoint is a transport interface, not an independent implementation of business logic.**

Every protected operation must enforce the applicable tenant, subscription, module entitlement, permission, object-access, and business rules.

Every financial operation must preserve transactional integrity, valid lifecycle transitions, and required audit evidence.

Every external integration must handle retries, duplicate delivery, timeouts, and uncertain outcomes without assuming that a network response proves the final business result.

All interfaces must follow the same domain rules, regardless of whether the operation originated from a Django page, an HTMX interaction, a REST API, a background task, or an external provider.