# Entitlement Engine

| Property | Value |
|---|---|
| Document ID | ARCH-007 |
| Document Path | `docs/01-architecture/ENTITLEMENT_ENGINE.md` |
| Product | UAE ERP SaaS |
| Version | 1.0 |
| Status | Draft — Requires Architecture and Security Review |
| Review Date | 27 October 2026 |
| Target Phase | P2 — Module Catalogue, Subscription and Billing |
| Framework | Django |
| Database | PostgreSQL |
| Related Documents | `MODULE_CATALOGUE.md`, `COMMERCIAL_MODEL.md`, `MODULE_DEPENDENCIES.md`, `DATABASE_DESIGN.md`, `DJANGO_APP_STRUCTURE.md`, `MULTI_TENANCY.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `PRODUCT_REQUIREMENTS.md` |

---

# 1. Purpose

The Entitlement Engine determines which product modules and capabilities a tenant is authorized to use under the SaaS commercial model.

It provides a centralized mechanism for:

- Resolving the tenant's current module entitlements.
- Evaluating subscription status and effective dates.
- Enforcing hard, optional and conditional module dependencies.
- Separating commercial entitlement from user authorization.
- Supporting configurable module selection and pricing.
- Activating and deactivating modules safely.
- Handling subscription expiry, suspension, renewal and cancellation.
- Applying feature-level restrictions where required.
- Providing consistent results to Django views, APIs, services, background tasks and integrations.
- Auditing all entitlement-changing operations.
- Preventing unauthorized access when caches are stale or background jobs are delayed.

The engine must support the product's modular commercial model without requiring separate application deployments for every module.

## 1.1 Primary design rule

**Every protected operation must evaluate current authorization and the applicable entitlement policy through a trusted server-side path.**

Frontend visibility, hidden navigation items, JavaScript checks and client-submitted module codes must never be treated as proof of entitlement.

## 1.2 Scope

This document covers module and feature entitlements.

It does not replace:

- Authentication.
- Role-based access control.
- Object-level permissions.
- Tenant isolation.
- Subscription billing.
- Payment processing.
- Regulatory compliance validation.
- Domain-specific business rules.

These systems must work together through defined interfaces.

---

# 2. Core Concepts

## 2.1 Tenant

A tenant is a customer organization using the SaaS platform.

A tenant may contain multiple legal entities, branches, users and business records.

The entitlement engine evaluates access in the context of the authenticated tenant and the tenant's subscription.

The final product model must explicitly decide whether subscriptions apply to:

- The tenant as a whole.
- Individual legal entities.
- Individual branches.
- A combination of tenant-level subscriptions and scoped add-ons.

The initial implementation should use tenant-level subscriptions unless the approved commercial model requires otherwise.

## 2.2 Module definition

A module definition describes a product capability available in the platform.

Examples:

- CRM.
- Sales.
- Invoicing.
- Accounting.
- VAT.
- Inventory.
- HRMS.
- Payroll.
- Reporting.

A module definition is catalogue data, not a tenant entitlement.

## 2.3 Subscription

A subscription records the commercial relationship between a tenant and the SaaS provider.

It defines the applicable commercial terms, status and billing period.

A subscription does not, by itself, mean every module is accessible.

## 2.4 Subscription module selection

A subscription module selection records which modules are included in a subscription and the applicable commercial terms.

For example:

```text
Tenant A
    Subscription: Active
    Selected Modules:
        CRM
        INVOICING
        ACCOUNTING
```

The selection must satisfy the approved dependency policy.

## 2.5 Entitlement

An entitlement is the effective authorization for a tenant to use a module or capability.

It is derived from the approved subscription configuration, subscription state, effective dates, module lifecycle, dependency rules and platform restrictions.

An entitlement must not be inferred solely from the existence of a row in a module-selection table.

## 2.6 User permission

A user permission controls what an individual user may do within an entitled module.

For example:

- A tenant may have Accounting.
- One user may view reports.
- Another user may create draft journals.
- Only an appropriately authorized user may post journals.

Module entitlement does not override role-based or object-level authorization.

## 2.7 Capability

A capability is a specific operation or feature that a module can expose.

Examples:

```text
accounting.journal.view
accounting.journal.create
accounting.journal.post
inventory.stock.view
inventory.stock.adjust
invoicing.invoice.issue
e_invoicing.invoice.submit
```

The engine may use module-level entitlements as the initial authorization boundary and support feature-level entitlements where the commercial model requires them.

Do not introduce a large feature-entitlement system before the product requires it.

---

# 3. Authorization Model

## 3.1 Required checks

A protected operation must satisfy the applicable checks:

```text
REQUEST AUTHORIZATION
    |
    +-- User is authenticated
    |
    +-- Account is active
    |
    +-- Tenant membership is active
    |
    +-- Request tenant is valid and authorized
    |
    +-- Required module entitlement is active
    |
    +-- Required module dependencies are satisfied
    |
    +-- User has the required permission
    |
    +-- Object belongs to the authorized tenant
    |
    +-- Organizational scope is permitted
    |
    +-- Business state permits the requested operation
    |
    +-- Operation is not blocked by a security or platform control
```

The exact order may vary according to the request, but every applicable check must be enforced.

## 3.2 Formal rule

Let:

- `T` = tenant context is valid.
- `S` = subscription policy permits access.
- `M` = module is implemented and permitted by its lifecycle state.
- `D` = required dependencies are satisfied.
- `P` = platform policy permits access.
- `U` = user is authorized for the action.
- `O` = object and organizational scope are valid.
- `B` = business rules permit the operation.

Then:

```text
ALLOW =
    T AND S AND M AND D AND P AND U AND O AND B
```

A failed mandatory check results in denial.

## 3.3 Deny by default

Unknown modules, unknown capabilities, missing configuration, invalid tenant context and unresolved dependencies must not result in permissive access.

If the engine cannot establish that access is allowed, it must deny the protected operation.

Operational failures must be logged and surfaced to the appropriate monitoring systems.

## 3.4 Separate authentication, entitlement and permissions

The implementation must not combine these concerns into a single `is_active` flag.

For example:

```python
# Incorrect: a Django user being active does not grant
# access to every module.
if request.user.is_active:
    allow_module_access()
```

Instead, use the approved authorization service, which evaluates tenant membership, permissions and the required module entitlement.

---

# 4. Module Lifecycle and Entitlement States

These states represent different concepts and must remain separate.

## 4.1 Module lifecycle states

Use the approved module catalogue lifecycle:

- `PLANNED`
- `IN_DEVELOPMENT`
- `INTERNAL_ONLY`
- `PILOT`
- `AVAILABLE`
- `DEPRECATED`
- `RETIRED`

Only approved lifecycle states may permit commercial activation.

For example, a planned module must not become purchasable simply because a database row exists.

## 4.2 Subscription states

The subscription domain should define its own lifecycle.

The initial proposal is:

- `DRAFT`
- `PENDING_PAYMENT`
- `TRIALING`
- `ACTIVE`
- `PAST_DUE`
- `SUSPENDED`
- `CANCELLED`
- `EXPIRED`

The final set must match the approved billing provider and commercial policies.

Do not reuse module-entitlement statuses as subscription statuses.

## 4.3 Module entitlement states

Suggested effective states:

- `PENDING`
- `ACTIVE`
- `GRACE`
- `SUSPENDED`
- `EXPIRED`
- `REVOKED`
- `DISABLED`

These states describe the tenant's access to a module.

The system must define which states allow which operations.

Example:

| Entitlement State | Normal Reads | New Business Operations | Subscription Management |
|---|---|---|---|
| `PENDING` | No | No | According to authorized setup flow |
| `ACTIVE` | Yes, subject to permissions | Yes, subject to permissions and business rules | Yes, if authorized |
| `GRACE` | According to approved grace policy | According to approved grace policy | Yes, if authorized |
| `SUSPENDED` | According to suspension policy | Normally no | Yes, if authorized |
| `EXPIRED` | According to historical-access policy | No | Yes, if authorized |
| `REVOKED` | According to historical-access policy | No | Yes, if authorized |
| `DISABLED` | According to platform policy | No | According to platform policy |

The exact policy for historical reads, exports and grace periods requires product approval.

Do not assume that every suspension or cancellation has the same behavior.

## 4.4 Effective dates

Entitlements must support effective start and end dates where required.

Use timezone-aware timestamps.

The engine must define how it evaluates:

```text
effective_from <= current_time < effective_until
```

When `effective_until` is absent, the entitlement may have no scheduled end date, subject to its subscription and lifecycle state.

The database and application must use consistent UTC storage and comparison rules.

---

# 5. Central Entitlement Architecture

## 5.1 Proposed Django application ownership

The `subscriptions` application should own the subscription and entitlement domain unless a separately approved architecture assigns it elsewhere.

Suggested structure:

```text
apps/
└── subscriptions/
    ├── models/
    │   ├── module_definition.py
    │   ├── module_dependency.py
    │   ├── subscription.py
    │   ├── subscription_module.py
    │   ├── module_entitlement.py
    │   └── entitlement_change.py
    ├── services/
    │   ├── entitlement_service.py
    │   ├── dependency_service.py
    │   ├── activation_service.py
    │   ├── deactivation_service.py
    │   └── subscription_change_service.py
    ├── selectors/
    │   ├── entitlement_selectors.py
    │   └── subscription_selectors.py
    ├── policies/
    │   ├── subscription_access_policy.py
    │   └── entitlement_policy.py
    ├── tasks.py
    ├── admin.py
    ├── apps.py
    └── tests/
        ├── test_entitlement_service.py
        ├── test_dependency_service.py
        ├── test_activation_service.py
        ├── test_deactivation_service.py
        ├── test_entitlement_security.py
        └── test_entitlement_concurrency.py
```

This is a proposed organization. It must be reconciled with the final Django application structure.

## 5.2 Service responsibilities

### `entitlement_service.py`

Responsible for:

- Evaluating effective module access.
- Evaluating capability access where supported.
- Combining subscription, module lifecycle and dependency policies.
- Returning structured results.
- Providing a trusted application-level authorization interface.

It must not directly charge payment methods or delete business data.

### `dependency_service.py`

Responsible for:

- Resolving hard dependencies.
- Evaluating optional dependencies.
- Evaluating conditional dependencies.
- Evaluating alternative dependency groups.
- Detecting invalid dependency configuration.
- Calculating dependency impact.

### `activation_service.py`

Responsible for:

- Validating requested activation.
- Coordinating subscription changes.
- Recording entitlement transitions.
- Scheduling required provisioning.
- Handling retries and idempotency.

### `deactivation_service.py`

Responsible for:

- Calculating affected dependent modules.
- Validating deactivation requests.
- Applying the approved deactivation policy.
- Preserving business records.
- Scheduling cleanup of non-business operational resources where appropriate.

### `subscription_change_service.py`

Responsible for:

- Coordinating subscription module changes.
- Revalidating dependencies.
- Applying approved pricing and billing rules.
- Coordinating payment workflow state.
- Recording the resulting subscription and entitlement changes.

The final boundaries must be kept explicit to prevent circular service calls.

---

# 6. Database Model Requirements

The following models are conceptual requirements, not final Django model code.

Their exact fields and relationships must be reconciled with `DATABASE_DESIGN.md` and `MODULE_DEPENDENCIES.md`.

## 6.1 ModuleDefinition

Represents a module in the product catalogue.

Suggested fields:

| Field | Purpose |
|---|---|
| `id` | Internal primary key |
| `code` | Unique stable module code |
| `name` | Display name |
| `description` | Customer-facing description |
| `lifecycle_state` | Current release state |
| `is_commercial` | Whether the module is commercially purchasable |
| `is_sellable` | Whether commercial activation is currently permitted |
| `configuration_version` | Version of relevant catalogue configuration |
| `created_at` | Creation timestamp |
| `updated_at` | Update timestamp |

The stable module code must not be derived from a user-editable name.

A module must not be deleted if subscriptions, entitlements, audit records or historical business references depend on it.

Use lifecycle transitions and controlled retirement.

## 6.2 Subscription

Represents a tenant's subscription.

Suggested fields:

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `tenant_id` | Subscribing tenant |
| `status` | Subscription lifecycle state |
| `starts_at` | Subscription start |
| `current_period_starts_at` | Current period start |
| `current_period_ends_at` | Current period end |
| `trial_ends_at` | Optional trial end |
| `grace_ends_at` | Optional grace-period end |
| `cancel_at_period_end` | Whether cancellation is scheduled |
| `cancelled_at` | Cancellation timestamp |
| `billing_reference` | External billing identifier, if applicable |
| `created_at` | Creation timestamp |
| `updated_at` | Update timestamp |

Commercial prices, currencies, billing intervals and tax treatment must be modeled according to the approved billing design.

Do not store payment card secrets in this model.

## 6.3 SubscriptionModule

Represents a module selected under a subscription.

Suggested fields:

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `subscription_id` | Associated subscription |
| `module_definition_id` | Selected module |
| `status` | Selection or activation state |
| `effective_from` | Start of selection |
| `effective_until` | End of selection |
| `price_snapshot` | Agreed price information, if required |
| `configuration_version` | Applicable commercial configuration |
| `created_at` | Creation timestamp |
| `updated_at` | Update timestamp |

A suitable uniqueness constraint must prevent duplicate active selections for the same module within the same subscription, unless the commercial model explicitly supports multiple separately scoped instances.

If the platform later supports module quantities or entity-specific subscriptions, the uniqueness rules must be revisited.

## 6.4 ModuleEntitlement

Represents a tenant's effective entitlement to a module.

Suggested fields:

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `tenant_id` | Entitled tenant |
| `module_definition_id` | Entitled module |
| `subscription_id` | Source subscription, where applicable |
| `status` | Effective entitlement state |
| `effective_from` | Entitlement start |
| `effective_until` | Entitlement end |
| `reason_code` | Reason for current state |
| `source_configuration_version` | Dependency or policy version |
| `last_evaluated_at` | Last evaluation time |
| `created_at` | Creation timestamp |
| `updated_at` | Update timestamp |

The model may be persisted as a materialized effective state for operational convenience.

However, the persisted state must remain derived from authoritative subscription and dependency records.

It must not become an independent source of commercial truth.

If multiple subscriptions or add-ons can grant the same module, the entitlement resolution policy must explicitly account for those sources.

## 6.5 EntitlementChange

Records entitlement transitions and their causes.

Suggested fields:

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `tenant_id` | Affected tenant |
| `module_code` | Affected module |
| `previous_status` | Previous effective state |
| `new_status` | New effective state |
| `reason_code` | Change reason |
| `source_type` | Subscription, administrative action, policy change or other approved source |
| `source_reference` | Related record reference |
| `actor_user_id` | Initiating user, where applicable |
| `correlation_id` | Related workflow identifier |
| `created_at` | Change timestamp |

Records should be append-only through ordinary application workflows.

Corrections must be represented by additional audit events rather than silently rewriting historical transitions.

## 6.6 Dependency records

Use the dependency model defined by `MODULE_DEPENDENCIES.md`.

Do not create a second independent dependency registry inside the entitlement engine.

---

# 7. Entitlement Evaluation Contract

## 7.1 Required interface

Provide a central service interface similar to:

```python
evaluate_module_entitlement(
    *,
    tenant,
    module_code,
    at=None,
    use_cache=True,
)
```

The service returns a structured result describing whether the module is available and why.

The interface is illustrative; the final implementation must follow project coding standards.

## 7.2 Structured result

A successful result may contain:

```json
{
  "allowed": true,
  "tenant_id": "tenant-reference",
  "module_code": "INVOICING",
  "status": "ACTIVE",
  "reason_code": "ENTITLED",
  "configuration_version": 1
}
```

A denied result may contain:

```json
{
  "allowed": false,
  "tenant_id": "tenant-reference",
  "module_code": "E_INVOICING",
  "status": "DISABLED",
  "reason_code": "MISSING_DEPENDENCY",
  "missing_dependencies": [
    {
      "module_code": "INVOICING",
      "dependency_type": "HARD"
    }
  ],
  "configuration_version": 1
}
```

These are illustrative payloads.

The implementation must not expose internal identifiers or sensitive configuration to unauthorized callers.

The public API response may contain less detail than the internal service result.

## 7.3 Result semantics

The service must distinguish at least:

- Module not found.
- Module not yet available.
- Module not sellable.
- No matching subscription.
- Subscription not active.
- Subscription outside its effective period.
- Module not selected.
- Entitlement expired.
- Entitlement suspended.
- Missing hard dependency.
- Failed conditional dependency.
- No valid alternative dependency.
- Platform policy denial.
- Configuration invalid.

The internal reason code must be stable enough for tests, monitoring and customer-support workflows.

Do not make application behavior depend on parsing human-readable error messages.

## 7.4 Evaluation sequence

The service should follow a documented evaluation sequence:

1. Resolve the trusted tenant context.
2. Resolve the module definition.
3. Validate module lifecycle and availability.
4. Resolve the applicable subscription.
5. Evaluate subscription state and effective dates.
6. Resolve the tenant's selected modules.
7. Evaluate direct and transitive hard dependencies.
8. Evaluate applicable conditional dependencies.
9. Evaluate alternative dependency groups.
10. Apply platform restrictions.
11. Return the effective result and reason codes.

The implementation may optimize this sequence, but it must preserve the semantics.

## 7.5 Unknown module codes

Unknown module codes must not default to access granted.

They should produce a controlled denial and an operationally appropriate diagnostic.

## 7.6 Missing configuration

If a required dependency rule or module configuration is invalid, the affected activation or protected operation must fail closed.

The system must alert operators when a configuration error prevents normal operation.

---

# 8. Capability-Level Entitlements

Module-level access is the baseline.

Feature-level entitlements should be introduced only where the product or commercial model needs them.

## 8.1 Example

A tenant subscribes to Invoicing.

Its subscription may include:

- Draft invoice creation.
- Invoice issuance.
- Credit notes.
- Invoice exports.

Advanced automation or integrations may require separate entitlements.

The product must not hardcode pricing or feature access in individual templates.

## 8.2 Suggested interface

```python
evaluate_capability_entitlement(
    *,
    tenant,
    capability_code,
    at=None,
)
```

A capability must map to:

- An owning module.
- A defined commercial or operational policy.
- Required dependencies, if any.
- The appropriate authorization checks.

## 8.3 Capability ownership

Every capability code must have a unique owner.

For example:

```text
invoicing.invoice.create
    Owner: INVOICING

invoicing.invoice.issue
    Owner: INVOICING

accounting.journal.post
    Owner: ACCOUNTING

e_invoicing.invoice.submit
    Owner: E_INVOICING
```

A capability code must not be reassigned silently to a different module.

Changes must be versioned and tested.

## 8.4 Avoid premature complexity

Do not introduce per-user module subscriptions or arbitrary user-specific feature entitlements unless the commercial model requires them.

Tenant-level module entitlements and user-level permissions should remain separate.

---

# 9. Dependency Resolution

The engine must use the rules defined in `MODULE_DEPENDENCIES.md`.

## 9.1 Hard dependencies

All required hard dependencies must be satisfied before the module is considered available.

Hard dependencies must be resolved transitively.

Example:

```text
MODULE_A -> MODULE_B
MODULE_B -> MODULE_C
```

If all edges represent hard dependencies, activating `MODULE_A` requires valid entitlement to both `MODULE_B` and `MODULE_C`.

## 9.2 Optional dependencies

An optional dependency must not block the parent module.

The engine may report that the optional capability is unavailable so the frontend can adjust its presentation.

## 9.3 Conditional dependencies

Conditional rules must use registered, reviewed condition codes.

Do not evaluate arbitrary Python code or database-supplied expressions.

## 9.4 Alternative dependencies

Alternative groups must have explicit semantics.

For example, the condition may require at least one supported integration path.

The engine must not treat every alternative as mandatory.

## 9.5 Dependency graph validation

Validate the graph when configuration changes.

Reject:

- Direct cycles.
- Indirect cycles.
- Self-dependencies.
- Missing module references.
- Invalid dependency types.
- Invalid alternative groups.
- Dependencies that violate approved lifecycle rules.

Dependency graph validation must be automated and covered by tests.

---

# 10. Subscription Activation Workflow

Module activation must be coordinated through the subscription domain.

## 10.1 Workflow

```text
Customer Selects Module
        |
        v
Authenticate and Authorize
        |
        v
Validate Module Sellability
        |
        v
Resolve Required Dependencies
        |
        v
Calculate Proposed Commercial Changes
        |
        v
Present Required Modules and Pricing
        |
        v
Obtain Required Customer Confirmation
        |
        v
Execute Approved Billing Workflow
        |
        v
Commit Subscription Change
        |
        v
Record Entitlement Transition
        |
        v
Provision Required Resources
        |
        v
Verify Activation
        |
        v
Expose Module Access
```

The exact ordering of payment authorization, capture and subscription activation depends on the approved billing provider and commercial policy.

The system must explicitly handle cases where payment succeeds but local activation fails, or local preparation succeeds but payment fails.

## 10.2 No silent paid dependencies

The engine must identify required paid modules before the customer confirms a purchase.

It must not silently add paid modules to the subscription.

Any additional charges must be disclosed and authorized according to the approved commercial model.

## 10.3 Transaction boundaries

Use database transactions for related local state changes.

For example, the local subscription change and its associated module selections should not be committed in an inconsistent combination.

External payment operations cannot generally be included in a PostgreSQL transaction.

Use a documented payment workflow with:

- Idempotency keys.
- Correlation identifiers.
- Explicit workflow states.
- Retry handling.
- Reconciliation.
- Compensating actions where appropriate.

## 10.4 Provisioning

Provisioning may include:

- Creating default configuration records.
- Creating a chart of accounts when required.
- Initializing module-specific settings.
- Registering integration configuration.
- Scheduling background tasks.

Provisioning must be idempotent.

Repeated execution must not create duplicate business records.

A module must not be marked fully operational until mandatory provisioning has succeeded.

---

# 11. Deactivation, Expiry and Suspension

## 11.1 Deactivation

When a tenant removes a module, the engine must calculate the impact on all dependent modules.

For example:

```text
E_INVOICING -> INVOICING
```

If Invoicing is removed, E-Invoicing must not remain fully active with an unsatisfied hard dependency.

The platform must follow the approved policy:

- Reject the change.
- Require dependent modules to be removed in the same confirmed change.
- Apply an explicitly supported alternative.

## 11.2 Deactivation preview

Before execution, provide an impact report containing:

- Modules affected.
- Required dependent changes.
- Features that will become unavailable.
- Background tasks affected.
- Integrations affected.
- Business records retained.
- Historical access implications.
- Billing consequences, if applicable.

The preview must use the same policy rules as the final execution.

## 11.3 Subscription expiry

When a subscription expires:

- Recalculate effective entitlements.
- Apply the approved expiry policy.
- Prevent new protected operations where access is no longer permitted.
- Preserve business records.
- Retain audit evidence.
- Keep subscription-management and support paths available according to their own permissions.
- Cancel or adjust scheduled business operations that are no longer authorized.

Do not assume that an expired subscription must always make every historical record inaccessible.

## 11.4 Grace period

If a grace period is approved, represent it explicitly.

Define:

- Start and end timestamps.
- Allowed read operations.
- Allowed write operations.
- Export permissions.
- Background-task behavior.
- Module dependency behavior.
- Final transition at the end of the grace period.

Do not create an undocumented grace period inside module-specific code.

## 11.5 Suspension

Suspension may result from:

- Payment delinquency.
- Security concerns.
- Administrative action.
- Contractual restrictions.
- Platform abuse controls.

The reason for suspension must be recorded.

Different suspension reasons may require different operational behavior, but no exception may bypass security policy or tenant isolation.

## 11.6 Preserve business data

Disabling a module must not delete its business records.

The platform must define read-only and export policies separately from entitlement status.

Regulatory retention requirements, contractual obligations and legal holds must be considered before any deletion workflow.

---

# 12. User Authorization Integration

## 12.1 Two independent decisions

The entitlement engine answers:

> Does this tenant have access to the module or capability?

The authorization system answers:

> Is this user permitted to perform this action on this record?

Both must succeed.

## 12.2 Example

A tenant has Accounting.

A user may be permitted to:

- View journal entries.
- Create draft journals.

The same user may not be permitted to:

- Post journals.
- Close an accounting period.
- Export sensitive financial data.

The module entitlement does not override those restrictions.

## 12.3 Reusable authorization services

The application should provide a documented authorization interface that combines entitlement and permission checks without merging their domain ownership.

For example:

```python
authorize_action(
    *,
    user,
    tenant,
    action_code,
    resource=None,
)
```

This is an illustrative interface.

The implementation should delegate to the central entitlement and authorization services.

## 12.4 Object-level checks

Every protected record must be checked against the authorized tenant and applicable organizational scope.

A user must not access another tenant's records by changing a URL identifier, API payload, export request or background-task argument.

## 12.5 Administrative access

Platform operators must not automatically receive unrestricted access to customer business records merely because they can manage subscriptions.

Support access must follow the approved privileged-access policy, including auditability and any required approval.

---

# 13. Enforcement Across Django Components

The entitlement engine must be used consistently throughout the application.

## 13.1 Django views

Views must validate module entitlement and user authorization before executing protected operations.

Do not rely only on navigation visibility.

## 13.2 Django REST Framework

DRF permissions and application services must enforce the required entitlement.

A protected endpoint must not become accessible merely because the UI does not display it.

Serializer validation is not a substitute for authorization.

## 13.3 Application services

Application services must enforce the required authorization at the appropriate trust boundary.

This is important because the same service may be called from:

- A web view.
- An API endpoint.
- A management workflow.
- A background task.
- An integration handler.

Avoid relying solely on a check in the view layer.

## 13.4 Background tasks

Celery tasks must not assume that the user who originally triggered the task still has access.

Each task must follow a documented authorization policy.

For delayed business operations, the system must decide whether authorization is evaluated:

- At scheduling time.
- At execution time.
- At both times.

For subscription-sensitive business operations, execution-time entitlement validation is generally required unless an approved workflow explicitly authorizes the operation to complete after a subscription change.

Tasks must use trusted tenant identifiers and must not accept arbitrary tenant context from untrusted callers.

## 13.5 Django admin

Admin actions that affect tenant subscriptions or entitlements must use the same services as the customer-facing application.

Direct database edits that bypass dependency validation should be restricted and audited.

## 13.6 Webhooks and integrations

Webhook handlers must:

- Authenticate and verify the external request.
- Resolve the appropriate tenant through trusted integration configuration.
- Validate the operation.
- Apply the required entitlement policy.
- Enforce idempotency.
- Record the result.

An external provider's successful webhook does not automatically authorize unrelated business operations.

---

# 14. Caching and Freshness

Caching can improve performance, but stale entitlements can create security and commercial inconsistencies.

## 14.1 Cache only derived results

The authoritative subscription, module-selection and dependency configuration records remain the source of truth.

Cached entitlement results are derived data.

## 14.2 Cache key

A cache key must include enough context to prevent cross-tenant or cross-module reuse.

A conceptual key is:

```text
entitlement:
    tenant_id:
    module_code:
    policy_version
```

If results vary by legal entity, branch, subscription scope or other context, the key must include that context.

Never use a global cache entry that allows one tenant's entitlement result to be reused for another tenant.

## 14.3 Invalidation events

Invalidate relevant cache entries after:

- Subscription activation.
- Module selection changes.
- Subscription suspension.
- Subscription expiry.
- Subscription cancellation.
- Entitlement revocation.
- Dependency configuration changes.
- Module lifecycle changes.
- Platform-level access restrictions.

The invalidation process must cover all affected dependent modules.

## 14.4 Invalidation reliability

Do not rely on an in-memory callback alone for a security-critical entitlement change.

Use a reliable invalidation strategy, such as:

- Database transaction followed by an after-commit action.
- Transactional outbox for durable event delivery.
- Versioned cache namespaces.
- A bounded cache TTL as a fallback.

The final design must define the maximum permitted staleness for security-sensitive entitlement checks.

## 14.5 Security-sensitive operations

For operations such as posting financial entries, issuing invoices, submitting electronic invoices or exporting sensitive records, the system must use an authorization path that meets the approved freshness requirement.

A stale cache must not permit a prohibited financial or administrative operation.

## 14.6 Cache failure

The application must define behavior when the cache is unavailable.

The safe fallback is to evaluate authorization through the authoritative database-backed service or deny the operation when authorization cannot be established.

Do not treat a cache failure as an automatic entitlement grant.

---

# 15. Concurrency and Consistency

## 15.1 Concurrent subscription changes

Two administrators may attempt conflicting operations at the same time.

Example:

- Administrator A activates E-Invoicing.
- Administrator B removes Invoicing.

The platform must not commit a final state where E-Invoicing remains active without its required dependency.

## 15.2 Concurrency controls

Use appropriate combinations of:

- Database transactions.
- Row-level locks.
- Optimistic concurrency checks.
- Unique constraints.
- Version numbers.
- Idempotency keys.
- Post-change consistency validation.

The specific strategy must be tested against the selected PostgreSQL isolation level and actual data model.

## 15.3 Final-state validation

Validate the proposed subscription state before committing it.

If a change affects dependent modules, calculate the resulting state of the entire affected dependency closure.

Do not validate only the module directly changed by the request.

## 15.4 Reconciliation

Provide a management command or operational job that identifies inconsistencies between:

- Subscription records.
- Selected module records.
- Effective entitlements.
- Dependency configuration.
- Provisioning state.

The reconciliation process must report inconsistencies and apply only approved, deterministic repairs.

It must not silently rewrite commercial records or charge customers.

---

# 16. Audit and Observability

## 16.1 Required audit events

Record relevant entitlement changes, including:

- Module activated.
- Module deactivated.
- Entitlement granted.
- Entitlement suspended.
- Entitlement restored.
- Entitlement expired.
- Subscription module selection changed.
- Dependency configuration changed.
- Administrative override applied.
- Activation failed.
- Provisioning failed.
- Reconciliation detected inconsistency.

## 16.2 Required event context

Where applicable, record:

- Tenant.
- Module.
- Previous state.
- New state.
- Reason code.
- Actor.
- Source workflow.
- Correlation identifier.
- Timestamp.
- Configuration version.
- Outcome.

Avoid storing passwords, payment secrets, unnecessary personal data or sensitive business payloads in audit logs.

## 16.3 Metrics

Recommended metrics include:

- Entitlement evaluations.
- Allowed and denied decisions.
- Denial reasons.
- Dependency validation failures.
- Activation failures.
- Deactivation failures.
- Provisioning failures.
- Cache hit and miss rates.
- Cache invalidation delays.
- Entitlement reconciliation discrepancies.
- Authorization evaluation latency.

Use bounded labels such as module codes and reason codes.

Do not use tenant IDs, user IDs or other unbounded identifiers as unrestricted metric labels.

## 16.4 Alerts

Alert operators when:

- Entitlement configuration is invalid.
- Dependency cycles are detected.
- A provisioning workflow repeatedly fails.
- Cache invalidation exceeds the approved limit.
- Reconciliation finds unexplained inconsistencies.
- A privileged override is used.
- Subscription changes repeatedly fail after payment confirmation.

Alerts must not contain unnecessary customer data or secrets.

---

# 17. API and Error Semantics

## 17.1 Authorization denial

For an authenticated request to a valid resource that the user is not authorized to access, return the appropriate authorization response according to the project's API standards.

## 17.2 Missing module entitlement

A stable API error may use:

```json
{
  "error": {
    "code": "MODULE_NOT_ENTITLED",
    "message": "This feature is not available under the current subscription.",
    "module_code": "ACCOUNTING",
    "request_id": "request-correlation-id"
  }
}
```

Do not expose sensitive subscription, dependency or tenant configuration to unauthorized callers.

## 17.3 Unknown module

An unknown module code should produce a controlled error and a diagnostic event.

It must never be treated as an unrestricted module.

## 17.4 Avoid overloading HTTP status codes

The API must distinguish:

- Authentication failures.
- Authorization failures.
- Invalid business requests.
- Missing or unavailable resources.
- Subscription configuration errors.
- Temporary infrastructure failures.

Follow the approved `API_STANDARDS.md` contract.

---

# 18. Security Requirements

The entitlement engine is security-sensitive infrastructure.

## 18.1 Mandatory controls

- Deny by default.
- Resolve tenant context through trusted server-side logic.
- Validate tenant membership independently of module entitlement.
- Validate module entitlement independently of user permissions.
- Validate object-level tenant ownership.
- Enforce permissions in application services and other relevant trust boundaries.
- Use consistent authorization logic for web, API and background execution.
- Prevent cache entries from crossing tenant boundaries.
- Audit privileged entitlement changes.
- Restrict administrative overrides.
- Avoid exposing sensitive dependency configuration.
- Validate effective dates and subscription states.
- Prevent direct unvalidated subscription mutations.
- Protect against concurrent state changes.
- Apply database tenant isolation as defined by `MULTI_TENANCY.md`.
- Test authorization-denial paths as well as successful paths.

## 18.2 Platform superusers

A Django superuser must not automatically bypass every tenant and business-domain control in ordinary application workflows.

Any privileged bypass must be explicit, narrowly scoped, documented and audited.

## 18.3 Database security

The entitlement engine does not replace PostgreSQL tenant isolation.

Use the approved tenant-aware data-access patterns and database security controls.

If PostgreSQL Row-Level Security is enabled, application database roles and tenant-context handling must be configured so that RLS is enforced as intended.

The application must not assume that setting a tenant ID in a request parameter establishes trusted database context.

---

# 19. Testing Strategy

The entitlement engine must have comprehensive automated tests.

## 19.1 Core evaluation tests

| ID | Scenario | Expected Result |
|---|---|---|
| ENT-001 | Tenant has an active subscription and selected module | Entitlement allowed if all other checks pass |
| ENT-002 | Tenant has no applicable subscription | Denied |
| ENT-003 | Subscription is pending payment | Follows approved pending-payment policy |
| ENT-004 | Subscription is active within its effective period | Evaluated according to subscription configuration |
| ENT-005 | Subscription has expired | Expiry policy applied |
| ENT-006 | Subscription is suspended | Suspension policy applied |
| ENT-007 | Module is planned | Commercial activation denied |
| ENT-008 | Module is not sellable | New commercial activation denied |
| ENT-009 | Module code is unknown | Denied |
| ENT-010 | Module has a missing hard dependency | Denied |
| ENT-011 | Transitive hard dependency is missing | Denied |
| ENT-012 | Optional dependency is missing | Core module remains available |
| ENT-013 | Conditional dependency is applicable but unsatisfied | Dependent capability denied |
| ENT-014 | Conditional dependency does not apply | Conditional requirement not enforced |
| ENT-015 | One valid alternative is available | Alternative requirement satisfied |
| ENT-016 | No valid alternative is available | Dependent capability denied |
| ENT-017 | Platform policy disables a module | Denied |

## 19.2 User authorization tests

| ID | Scenario | Expected Result |
|---|---|---|
| ENT-018 | Tenant has module and user has permission | Operation may proceed |
| ENT-019 | Tenant has module but user lacks permission | Denied |
| ENT-020 | User has permission but tenant lacks module | Denied |
| ENT-021 | User is not an active tenant member | Denied |
| ENT-022 | User attempts cross-tenant access | Denied |
| ENT-023 | User attempts unauthorized branch access | Denied |
| ENT-024 | User changes a resource identifier | Object authorization remains enforced |
| ENT-025 | User invokes a protected service outside a view | Authorization remains enforced |

## 19.3 Lifecycle tests

| ID | Scenario | Expected Result |
|---|---|---|
| ENT-026 | Module activation succeeds | State and audit record are consistent |
| ENT-027 | Activation is retried | No duplicate side effects |
| ENT-028 | Provisioning fails | Failure is visible and recoverable |
| ENT-029 | Module is deactivated | Business records are retained |
| ENT-030 | Hard dependency is removed | Dependent modules are handled through the approved policy |
| ENT-031 | Module is reactivated | Existing records remain consistent |
| ENT-032 | Subscription cancellation is scheduled for period end | Access follows the approved policy until the effective transition |
| ENT-033 | Grace period begins or ends | Correct state transition occurs |
| ENT-034 | Entitlement is revoked by an administrator | Access is recalculated and audited |

## 19.4 Cache tests

| ID | Scenario | Expected Result |
|---|---|---|
| ENT-035 | Entitlement result is cached | Result remains tenant-specific |
| ENT-036 | Entitlement is revoked | Cached access is invalidated within the approved limit |
| ENT-037 | Dependency configuration changes | Affected cache entries are invalidated |
| ENT-038 | Cache is unavailable | Safe database-backed evaluation or denial |
| ENT-039 | Cache entries exist for two tenants | No cross-tenant result reuse |
| ENT-040 | Financial operation uses cached authorization | Freshness policy is enforced |

## 19.5 Concurrency and reliability tests

| ID | Scenario | Expected Result |
|---|---|---|
| ENT-041 | Concurrent activation requests | No duplicate or inconsistent entitlement |
| ENT-042 | Conflicting activation and deactivation requests | Invalid final state is rejected |
| ENT-043 | Payment succeeds but activation fails | Recoverable reconciliation workflow exists |
| ENT-044 | Database transaction rolls back | No partially committed local entitlement state |
| ENT-045 | Event delivery is repeated | Idempotent processing |
| ENT-046 | Reconciliation detects inconsistency | Reported and handled through approved policy |
| ENT-047 | Invalid dependency configuration is introduced | Configuration is rejected |
| ENT-048 | Administrative override is used | Authorized and audited |

Tests must run against the actual implementation and relevant infrastructure.

---

# 20. Performance and Reliability

## 20.1 Performance objective

Entitlement evaluation must not require expensive dependency-graph reconstruction or unrestricted database queries on every request.

The initial implementation should prioritize correctness and observability, then optimize based on measured workloads.

## 20.2 Performance practices

- Index tenant, subscription and module-reference fields.
- Avoid N+1 queries.
- Cache appropriate derived results.
- Version dependency configuration.
- Avoid recomputing an unchanged dependency closure unnecessarily.
- Use bulk evaluation where reporting workflows need multiple module checks.
- Keep entitlement evaluation separate from expensive provisioning operations.
- Measure database queries and response latency.

## 20.3 Availability

The entitlement service must fail safely when critical configuration or authorization data cannot be established.

For a protected financial operation, uncertainty must not be converted into permission.

## 20.4 Recovery

The platform must be able to reconstruct effective entitlements from authoritative subscription, module-selection and dependency records.

Cached results and derived entitlement rows must be recoverable.

A recovery procedure must not issue duplicate charges or delete business records.

---

# 21. Implementation Roadmap

| Phase | Deliverables |
|---|---|
| P0 — Foundation | Establish module identifiers, configuration conventions and security boundaries |
| P1 — Core Platform | Implement tenant context, identity and authorization foundations |
| P2 — Subscription Engine | Implement module registry, dependency resolution, subscription selections, effective entitlements and lifecycle transitions |
| P3 — CRM, Sales and Invoicing | Integrate initial business modules with central entitlement checks |
| P4 — UAE E-Invoicing | Enforce invoice dependency, provider readiness and submission authorization |
| P5 — Accounting and VAT | Enforce financial-module entitlements and sensitive operation permissions |
| P6 — Procurement and Inventory | Apply module access rules to stock and purchasing workflows |
| P7 — HRMS and Payroll | Enforce sensitive employee and payroll access |
| P8 — Projects, Expenses and Assets | Implement conditional module integrations |
| P9 — Banking and Advanced Finance | Enforce banking and financial-operation entitlements |
| P10 — Reporting and Integrations | Enforce entitlements for reports, exports and external integrations |
| P11 — Enterprise Readiness | Validate administrative controls, reconciliation and operational monitoring |
| P12 — Production Launch | Validate recovery, consistency and release controls |

---

# 22. Pending Decisions

| ID | Decision | Required Clarification |
|---|---|---|
| ENT-DEC-001 | Subscription scope | Tenant-wide, legal-entity-level or another model? |
| ENT-DEC-002 | Trial policy | Which modules and operations are available during a trial? |
| ENT-DEC-003 | Payment failure | When does access change after failed payment? |
| ENT-DEC-004 | Grace period | Is a grace period offered, and which operations remain available? |
| ENT-DEC-005 | Cancellation | Immediate or end-of-period access termination? |
| ENT-DEC-006 | Historical access | What read-only access remains after expiry or cancellation? |
| ENT-DEC-007 | Data export | Which exports are available after cancellation? |
| ENT-DEC-008 | Module pricing | Are dependencies separately charged, bundled or included in plans? |
| ENT-DEC-009 | Dependency changes | How are new mandatory dependencies applied to existing tenants? |
| ENT-DEC-010 | Feature entitlements | Which capabilities require separate commercial entitlements? |
| ENT-DEC-011 | Entitlement caching | What is the maximum acceptable staleness for different operation classes? |
| ENT-DEC-012 | Administrative override | Which roles may grant temporary access, under what approval process? |
| ENT-DEC-013 | Subscription concurrency | What transaction and locking strategy will be used? |
| ENT-DEC-014 | Billing integration | Which payment provider and billing workflow are approved? |
| ENT-DEC-015 | Tenant termination | What retention, export and deletion policies apply? |
| ENT-DEC-016 | Multiple subscriptions | Can multiple subscriptions grant the same module to one tenant? |
| ENT-DEC-017 | Scoped add-ons | Can a module be purchased for only selected legal entities or branches? |

Approved decisions must be recorded in the architectural decision log and reflected in the implementation.

---

# 23. Instructions for Codex Agents

Before implementing the entitlement engine, Codex must read:

1. `MODULE_CATALOGUE.md`
2. `COMMERCIAL_MODEL.md`
3. `MODULE_DEPENDENCIES.md`
4. `DATABASE_DESIGN.md`
5. `MULTI_TENANCY.md`
6. `AUTHENTICATION_AND_PERMISSIONS.md`
7. `DJANGO_APP_STRUCTURE.md`
8. `PRODUCT_REQUIREMENTS.md`

If any referenced document is missing, Codex must identify the gap rather than inventing a conflicting specification.

## 23.1 Required implementation sequence

1. Inspect the current repository and existing models.
2. Reconcile the entitlement model with the subscription schema.
3. Confirm approved subscription and entitlement state transitions.
4. Implement module registry and dependency validation.
5. Implement the central entitlement evaluation service.
6. Implement activation and deactivation workflows.
7. Integrate entitlement checks with authorization services.
8. Implement reliable cache invalidation if caching is introduced.
9. Add audit events and operational metrics.
10. Add automated tests.
11. Run the tests and record actual results.
12. Update architecture and project-status documentation.

## 23.2 Prohibited shortcuts

Codex must not:

- Hardcode subscription eligibility separately in every module.
- Grant access based solely on a frontend flag.
- Treat a Django superuser as automatically authorized for every tenant operation.
- Treat module entitlement as a substitute for user permissions.
- Allow unknown modules by default.
- Bypass the entitlement engine in background tasks.
- Silently add paid dependencies.
- Delete business data when entitlements are revoked.
- Trust client-submitted tenant identifiers without server-side validation.
- Use stale cache entries for sensitive operations beyond the approved freshness policy.
- Modify commercial subscription records through unvalidated direct writes.
- Introduce dependency cycles.
- Claim tests passed without executing them.

## 23.3 Required change report

Every implementation change must report:

- Files changed.
- Models and migrations added or modified.
- Entitlement rules implemented.
- Dependency behavior implemented.
- Authorization integration.
- Cache and concurrency behavior.
- Audit and monitoring changes.
- Tests executed and actual results.
- Known limitations.
- Unresolved product decisions.

---

# 24. Definition of Done

The entitlement engine is ready for production consideration when:

- [ ] The module registry is centralized.
- [ ] Module lifecycle and sellability are enforced.
- [ ] Subscription state and effective dates are evaluated correctly.
- [ ] Module selection is distinguished from effective entitlement.
- [ ] Hard dependencies are resolved transitively.
- [ ] Optional, conditional and alternative dependencies behave correctly.
- [ ] Invalid dependency configurations are rejected.
- [ ] Entitlement evaluation returns structured results.
- [ ] Unknown modules are denied by default.
- [ ] Tenant context is resolved through trusted server-side logic.
- [ ] Module entitlement and user authorization remain separate.
- [ ] Object-level and organizational authorization remain enforced.
- [ ] Activation and deactivation workflows are idempotent.
- [ ] Subscription changes cannot commit invalid dependency states.
- [ ] Payment and activation failures are recoverable.
- [ ] Background tasks follow the approved entitlement policy.
- [ ] Cache invalidation meets the approved freshness requirements.
- [ ] Entitlement changes are audited.
- [ ] Existing business data is preserved after module deactivation.
- [ ] Reconciliation detects inconsistent effective states.
- [ ] Automated tests cover authorization, lifecycle, dependencies and concurrency.
- [ ] Production operational procedures are documented.

---

# 25. Final Architectural Rule

The Entitlement Engine is the authoritative application service for deciding whether a tenant is entitled to use a module or capability.

It must work with, but remain distinct from:

```text
MODULE CATALOGUE
Defines available product modules and lifecycle states.

SUBSCRIPTION ENGINE
Defines the tenant's commercial subscription and module selections.

DEPENDENCY ENGINE
Determines whether the selected module combination is valid.

ENTITLEMENT ENGINE
Determines the tenant's effective access to modules and capabilities.

AUTHORIZATION ENGINE
Determines whether the user may perform a particular operation.

TENANT ISOLATION
Ensures that data access remains confined to the authorized tenant.

BUSINESS DOMAIN SERVICES
Enforce transaction-specific rules and state transitions.
```

No individual Django application may independently redefine these rules.

**Production release requirement:** Every protected business operation must use a trusted server-side authorization path that evaluates the applicable tenant context, effective entitlement, user permissions and business constraints. The system must deny access when a mandatory authorization check fails or cannot be established.