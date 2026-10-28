# Module Dependencies and Entitlement Rules

| Property | Value |
|---|---|
| Document ID | ARCH-006 |
| Document Path | `docs/01-architecture/MODULE_DEPENDENCIES.md` |
| Product | UAE ERP SaaS |
| Version | 1.0 |
| Status | APPROVED — Module Dependency Baseline; Commercial Rules Pending |
| Review Date | 27 October 2026 |
| Architecture | Django Modular Monolith |
| Database | PostgreSQL |
| Related Documents | `MODULE_CATALOGUE.md`, `COMMERCIAL_MODEL.md`, `DATABASE_DESIGN.md`, `DJANGO_APP_STRUCTURE.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `MULTI_TENANCY.md`, `ENTITLEMENT_ENGINE.md`, `PRODUCT_REQUIREMENTS.md` |

---

# 1. Purpose

This document defines the dependency model for commercial and platform modules within the UAE ERP SaaS.

It establishes:

- Which modules depend on other modules.
- Which dependencies are mandatory.
- Which integrations are optional.
- Which modules are foundational and cannot be purchased independently.
- How module combinations are validated.
- How module dependencies interact with subscriptions and user permissions.
- How module activation and deactivation affect existing business data.
- How the system handles subscription expiry, suspension and cancellation.
- How Django applications communicate without creating circular dependencies.
- How module dependencies are configured, tested and changed.
- How Codex development agents must implement and maintain dependency rules.

The dependency system must support customers selecting individual modules or combinations according to the approved commercial model.

## 1.1 Primary objective

A customer must be able to purchase a supported combination of modules, receive access to the functionality included in that combination, and retain appropriate access to existing business records when subscription entitlements change.

The platform must never activate an invalid module combination silently.

It must also never delete business records merely because a module is disabled or a subscription expires.

## 1.2 Architectural principle

**Module dependencies are configuration-driven business rules enforced by a central entitlement engine and supported by an acyclic application dependency graph.**

These are related but distinct concerns:

1. **Commercial dependencies:** Which modules must a tenant be entitled to use together?
2. **Runtime dependencies:** Which application capabilities must exist for a feature to execute?
3. **Data dependencies:** Which data structures or services does a module require?
4. **Operational dependencies:** Which external services, workers or infrastructure components are required?
5. **Optional integrations:** Which capabilities can be connected without making another commercial module mandatory?

A single dependency declaration must not be used to represent all five concerns indiscriminately.

---

# 2. Dependency Terminology

## 2.1 Platform module

A platform module provides capabilities required to operate the SaaS itself.

Examples:

- Core platform.
- Tenant management.
- User identity.
- Subscription management.
- SaaS billing.

These modules are not necessarily independently purchasable.

## 2.2 Commercial module

A commercial module is a product capability that customers can purchase according to the approved pricing and subscription model.

Examples:

- CRM.
- Sales.
- Invoicing.
- Accounting.
- VAT.
- Inventory.
- HRMS.
- Payroll.

A commercial module must not be exposed as purchasable merely because its Django application exists.

## 2.3 Hard dependency

A hard dependency is a mandatory requirement for a module to operate as designed.

Example:

```text
Payroll -> HRMS
```

If Payroll genuinely requires HRMS in the approved product design, the tenant must have both entitlements before Payroll functionality can be activated.

The final dependency must be confirmed against the actual Payroll scope. If payroll can operate using a standalone employee and compensation master, the dependency may instead be a shared platform capability rather than the commercial HRMS module.

## 2.4 Optional dependency

An optional dependency represents a capability that enhances a module but is not required for its core operation.

Example:

```text
CRM -> Integrations [optional]
```

CRM can operate without the commercial Integrations module, while advanced external synchronization may require it.

Optional dependencies must not prevent activation of the parent module.

## 2.5 Alternative dependency

An alternative dependency allows a module to operate through one of several supported implementations.

Example:

```text
Bank feeds:
    Provider A OR Provider B OR manual import
```

Alternative dependencies must be represented explicitly.

The system must not interpret multiple alternatives as a requirement to subscribe to every option.

## 2.6 Conditional dependency

A conditional dependency applies only when a particular feature or workflow is enabled.

Example:

```text
Inventory
    -> Accounting integration [conditional]
```

Inventory may operate independently, while automatic accounting postings require Accounting.

The condition must be evaluated by a documented capability or feature rule.

## 2.7 Infrastructure dependency

An infrastructure dependency describes a technical service needed to execute a feature.

Examples:

- PostgreSQL.
- Redis.
- Celery workers.
- Email delivery.
- Object storage.
- External payment provider.

Infrastructure dependencies are not automatically commercial module dependencies.

For example, a CRM application may require Redis for a particular asynchronous workflow, but customers should not need to purchase a separate Redis module.

## 2.8 Shared platform capability

A shared platform capability is a technical or business primitive used by multiple modules.

Examples:

- Organization and legal-entity context.
- Currency and locale.
- Audit events.
- Document storage.
- Numbering services.
- Notification delivery.
- Permission evaluation.
- Entitlement evaluation.

A shared capability should be provided by an appropriate platform or domain service instead of making one commercial module a mandatory dependency for every other module.

---

# 3. Module Registry

The following registry reflects the planned product catalogue. It is a proposed architecture baseline, not a declaration that every module is implemented or ready for sale.

| Module Code | Django App | Category | Commercial | Initial State |
|---|---|---|---|---|
| CORE | `core` | Platform | No | Foundational |
| TENANTS | `tenants` | Platform | No | Foundational |
| USERS | `users` | Platform | No | Foundational |
| SUBSCRIPTIONS | `subscriptions` | Platform | No | Planned |
| BILLING | `billing` | Platform | No | Planned |
| CRM | `crm` | Business | Yes | Planned |
| SALES | `sales` | Business | Yes | Planned |
| INVOICING | `invoicing` | Business | Yes | Planned |
| E_INVOICING | `e_invoicing` | Business | Yes | Planned |
| ACCOUNTING | `accounting` | Business | Yes | Planned |
| VAT | `vat` | Business | Yes | Planned |
| PROCUREMENT | `procurement` | Business | Yes | Planned |
| INVENTORY | `inventory` | Business | Yes | Planned |
| HRMS | `hrms` | Business | Yes | Planned |
| PAYROLL | `payroll` | Business | Yes | Planned |
| PROJECTS | `projects` | Business | Yes | Planned |
| EXPENSES | `expenses` | Business | Yes | Planned |
| FIXED_ASSETS | `fixed_assets` | Business | Yes | Planned |
| BANKING | `banking` | Business | Yes | Planned |
| REPORTING | `reporting` | Business | Yes | Planned |
| INTEGRATIONS | `integrations` | Business | Yes | Planned |

The initial lifecycle states must be reconciled with `MODULE_CATALOGUE.md`.

A module may be sold only when its lifecycle state, implementation readiness, dependency configuration, pricing configuration and release approvals all permit commercial activation.

---

# 4. Dependency Design Rules

## 4.1 Platform dependencies are implicit prerequisites

Every commercial module relies on the relevant shared platform capabilities.

Conceptually:

```text
Commercial Modules
       |
       +-- Core Platform
       +-- Tenant Context
       +-- Identity and Authorization
       +-- Audit Infrastructure
       +-- Configuration
       +-- Database Integrity
```

These dependencies do not require customers to purchase separate commercial modules.

They must be enforced by the platform architecture.

## 4.2 Avoid false commercial dependencies

Do not make a commercial module depend on another commercial module solely because:

- Both modules are commonly purchased together.
- One module links to the other in the navigation.
- One module can optionally synchronize data with the other.
- One module provides a convenient screen for data owned elsewhere.
- One module can consume another module's events.

A mandatory dependency must reflect a real, approved requirement.

## 4.3 Shared capabilities must have clear ownership

If multiple modules need a shared capability, define its owner.

Examples:

| Capability | Suggested Owner |
|---|---|
| User identity | `users` |
| Tenant and membership | `tenants` |
| Subscription state | `subscriptions` |
| SaaS subscription charges | `billing` |
| Customer and lead records | `crm` |
| Sales quotation workflow | `sales` |
| Commercial invoice records | `invoicing` |
| Posted journal entries | `accounting` |
| VAT calculation and reporting | `vat`, coordinated with Accounting |
| Stock movements | `inventory` |
| Employee master | `hrms` |
| Payroll calculations | `payroll` |
| Fixed-asset lifecycle | `fixed_assets` |
| Expense claims | `expenses` |
| Bank reconciliation | `banking` |
| Cross-module reports | `reporting` |

Ownership must be reconciled with `DATABASE_DESIGN.md` and `DJANGO_APP_STRUCTURE.md`.

One module must not silently become the owner of another module's domain records.

## 4.4 Dependencies must be explicit

Each dependency must specify:

- Parent module.
- Required capability or dependent module.
- Dependency type.
- Activation condition.
- Enforcement behavior.
- User-facing explanation.
- Deactivation behavior.
- Version or compatibility constraints, where needed.
- Whether the dependency affects commercial pricing.
- Whether it affects existing data access.

Do not infer dependencies from application imports, installed packages or menu structure.

---

# 5. Proposed Initial Commercial Dependency Graph

The following is a starting proposal for product review.

It must be validated against the actual scope and pricing model before being treated as final.

## 5.1 Dependency matrix

| Module | Proposed Dependency | Type | Reason |
|---|---|---|---|
| CRM | None beyond platform | None | Can manage customer and lead records independently |
| SALES | CRM | Optional/conditional | CRM-linked leads and customer relationships may be optional |
| INVOICING | None beyond platform | None | Standalone invoice creation may be supported |
| E_INVOICING | INVOICING | Hard | Electronic submission requires an invoice representation |
| ACCOUNTING | None beyond platform | None | May operate independently with its own chart of accounts |
| VAT | ACCOUNTING | Conditional | Tax reporting and postings may require accounting integration |
| PROCUREMENT | None beyond platform | None | Purchase orders can operate independently |
| INVENTORY | None beyond platform | None | Stock tracking can operate independently |
| HRMS | None beyond platform | None | Employee administration can operate independently |
| PAYROLL | HRMS | Proposed hard dependency | Depends on employee records if HRMS owns the employee master |
| PROJECTS | None beyond platform | None | Project tracking can operate independently |
| EXPENSES | None beyond platform | None | Expense claims may operate independently |
| FIXED_ASSETS | ACCOUNTING | Conditional | Automated depreciation postings require accounting integration |
| BANKING | ACCOUNTING | Conditional | Reconciliation and automated postings require accounting integration |
| REPORTING | None beyond platform | None | Can provide reports over entitled modules |
| INTEGRATIONS | None beyond platform | None | Provides integration infrastructure and configurable connectors |

### Important qualification

This matrix distinguishes a commercial module dependency from a functional integration requirement.

For example, VAT reporting may require accounting data for a particular workflow. That does not automatically mean every VAT-related function must be commercially unavailable unless Accounting is purchased.

The product owner must decide whether to:

1. Make Accounting a mandatory commercial dependency.
2. Offer a standalone VAT capability with limited functionality.
3. Offer different VAT features depending on the subscribed modules.

The chosen policy must be documented before implementation.

## 5.2 Sales and CRM

Sales should support two operating modes if the product requirements require them:

- Standalone sales workflow using its own customer and contact references or shared customer primitives.
- CRM-integrated workflow using CRM leads, opportunities and relationship history.

The implementation must not duplicate the entire CRM domain inside Sales.

If the commercial product requires CRM for Sales, change the dependency to hard and update the pricing, onboarding and entitlement rules.

## 5.3 Invoicing and Accounting

Invoicing and Accounting should remain distinct domains.

Invoicing owns the commercial invoice lifecycle.

Accounting owns the general ledger and posted accounting entries.

When Accounting is enabled, invoices may produce accounting events or journal entries through an explicit integration.

When Accounting is not enabled, invoice creation and issuance must follow the approved standalone invoicing design.

Do not create an incomplete general ledger in the Invoicing module merely to simulate accounting functionality.

## 5.4 E-invoicing

The electronic invoicing module depends on an implemented invoice workflow and a validated provider integration.

The module must not be commercially activated until:

- Its invoice data contract is defined.
- Provider integration requirements are validated.
- Required credentials and tenant configuration are supported.
- Submission and response handling are implemented.
- Idempotency and retry behavior are tested.
- Required evidence and audit records are retained.
- Applicable regulatory requirements are reviewed.

The platform must not claim UAE regulatory compliance solely because the E-Invoicing module exists.

## 5.5 Payroll and HRMS

The proposed default is for Payroll to depend on HRMS if HRMS owns the authoritative employee records required by payroll processing.

If a standalone payroll product is desired, introduce an explicit shared employee-master capability or a separate product design.

Do not bypass ownership boundaries by copying employee records into Payroll without a defined synchronization and data-integrity policy.

## 5.6 Fixed Assets and Accounting

Fixed Assets may support:

- Asset registration.
- Asset classification.
- Custody and location.
- Depreciation schedules.
- Disposal records.

Accounting integration may be required for journal generation, depreciation posting and disposal accounting.

The dependency can therefore be conditional if the asset-register functionality is intentionally sold separately.

## 5.7 Banking and Accounting

Banking may support imported transactions and reconciliation without the Accounting module, depending on the final scope.

Automatic journal posting, ledger reconciliation and accounting-period controls may require Accounting.

These capabilities must be individually specified rather than treating all banking features as universally dependent on Accounting.

## 5.8 Procurement and Inventory

Procurement and Inventory may integrate through:

- Purchase orders.
- Goods receipts.
- Supplier returns.
- Stock movements.
- Inventory valuation.

A purchase order can exist without Inventory if the product supports service purchases or non-stock purchasing.

Inventory integration must be explicit and must not create circular application dependencies.

---

# 6. Platform Module Dependencies

Platform modules have different rules from commercial modules.

## 6.1 CORE

`CORE` provides shared infrastructure and application primitives.

It is a prerequisite for the rest of the platform.

It is not independently purchasable.

## 6.2 TENANTS

`TENANTS` provides tenant identity, tenant lifecycle and membership context.

Commercial modules must use the shared tenant-context mechanisms.

They must not implement their own conflicting tenant-resolution logic.

## 6.3 USERS

`USERS` provides identity, roles, permissions and account-security capabilities.

A module must use the shared authorization model rather than implementing a separate user-role system.

## 6.4 SUBSCRIPTIONS

`SUBSCRIPTIONS` manages the commercial relationship between a tenant and its selected modules.

It owns or coordinates:

- Subscription lifecycle.
- Selected modules.
- Subscription periods.
- Entitlement changes.
- Suspension and cancellation state.
- Subscription-related commercial rules.

Business modules must not modify subscription entitlements directly.

## 6.5 BILLING

`BILLING` manages charges associated with the SaaS subscription.

It must remain separate from customer invoices created through the ERP's Invoicing module.

For example:

```text
SaaS Subscription Billing
    Customer pays the ERP SaaS provider.

ERP Customer Invoicing
    Tenant issues invoices to its own customers.
```

These are separate financial domains.

Do not create a commercial dependency from ERP Invoicing to SaaS Billing.

---

# 7. Dependency Types and Evaluation

## 7.1 Required dependency types

The implementation must support at least:

```text
HARD
OPTIONAL
CONDITIONAL
ALTERNATIVE
```

Additional types may be introduced if they solve a documented requirement.

A dependency record should include:

| Field | Purpose |
|---|---|
| `id` | Dependency identifier |
| `module_code` | Module whose activation or feature is being evaluated |
| `dependency_type` | Hard, optional, conditional or alternative |
| `target_module_code` | Required or optional target module, if applicable |
| `target_capability_code` | Shared capability, if applicable |
| `condition_code` | Named condition for conditional dependencies |
| `is_active` | Whether the rule is active |
| `effective_from` | Effective date, if required |
| `effective_until` | End date, if required |
| `configuration_version` | Version of the dependency policy |
| `created_at` | Creation timestamp |
| `updated_at` | Update timestamp |

The exact schema must be reconciled with the subscription and entitlement models.

Do not duplicate the same dependency definition in multiple tables without a clear ownership rule.

## 7.2 Hard dependencies

A module is eligible for activation only if all hard dependencies are satisfied.

Example:

```text
E_INVOICING
    requires INVOICING
```

If Invoicing is not entitled, the entitlement engine must reject E-Invoicing activation.

## 7.3 Optional dependencies

Optional dependencies must not block activation.

If an optional module is unavailable:

- Hide or disable the dependent integration feature.
- Explain the missing capability where useful.
- Preserve the core module's operation.
- Do not fabricate data that would otherwise come from the optional module.

## 7.4 Conditional dependencies

Conditional dependencies must use named, testable conditions.

Example:

```text
Condition:
    automatic_accounting_posting_enabled

Requirement:
    ACCOUNTING must be entitled and operational.
```

Avoid arbitrary Python expressions stored in the database.

Use registered condition codes that map to reviewed application logic.

## 7.5 Alternative dependencies

Alternative dependencies should support an explicit policy such as:

```text
Any one of:
    supported_bank_provider
    manual_bank_import
```

The system must determine whether at least one supported alternative is available.

The dependency engine must not interpret alternative providers as mandatory commercial modules unless the commercial model explicitly says so.

---

# 8. Dependency Graph Validation

## 8.1 Directed graph

Represent module dependencies as a directed graph.

If Module A requires Module B:

```text
A -> B
```

A dependency path must not create a circular dependency.

Invalid example:

```text
SALES -> INVOICING
INVOICING -> ACCOUNTING
ACCOUNTING -> SALES
```

This graph creates a cycle and must be rejected.

## 8.2 Cycle detection

Dependency configuration must be validated whenever it changes.

Validation must detect:

- Direct self-dependencies.
- Indirect cycles.
- Missing module references.
- References to retired or invalid modules.
- Unsupported dependency types.
- Conflicting conditions.
- Invalid alternative groups.
- Dependencies on modules that cannot be enabled for the tenant.

Use a graph algorithm such as depth-first search or topological sorting.

## 8.3 Dependency resolution

The entitlement engine must calculate the transitive hard-dependency closure of a requested module.

Example:

```text
MODULE_A -> MODULE_B
MODULE_B -> MODULE_C
```

If the dependency types are hard:

```text
MODULE_A requires:
    MODULE_B
    MODULE_C
```

The engine must not evaluate only the direct dependency and ignore the transitive dependency.

## 8.4 Validation errors

Errors must be actionable.

Example:

```text
Cannot activate E_INVOICING.

Required module:
- INVOICING

Action:
Subscribe to Invoicing or select a product configuration
that supports electronic invoicing independently.
```

Do not return raw database errors or internal dependency-graph implementation details to customers.

---

# 9. Entitlement Evaluation

## 9.1 Entitlement is not a permission

The entitlement engine determines whether a tenant has access to a module.

The permission system determines whether a particular user may perform an action.

These checks must remain independent.

## 9.2 Effective module access

For a tenant and module:

```text
MODULE AVAILABLE =
    Module Exists
    AND Module Is Implemented
    AND Module Is Sellable or Otherwise Authorized
    AND Tenant Subscription Permits Access
    AND Subscription State Permits Access
    AND Required Dependencies Are Satisfied
    AND Module Is Not Disabled by Platform Policy
```

For a user performing an operation:

```text
ACTION ALLOWED =
    MODULE AVAILABLE
    AND User Is Authenticated
    AND Account Is Active
    AND Tenant Membership Is Active
    AND Required Permission Is Granted
    AND Organizational Scope Is Valid
    AND Object Access Is Authorized
    AND Business Rules Permit the Action
```

Database tenant isolation and integrity constraints remain mandatory.

## 9.3 Module lifecycle

The module lifecycle must be evaluated separately from subscription state.

Suggested module states:

- `PLANNED`
- `IN_DEVELOPMENT`
- `INTERNAL_ONLY`
- `PILOT`
- `AVAILABLE`
- `DEPRECATED`
- `RETIRED`

Suggested tenant entitlement states:

- `PENDING`
- `ACTIVE`
- `SUSPENDED`
- `EXPIRED`
- `CANCELLED`
- `DISABLED`

These states represent different concerns and must not be combined into one ambiguous field.

## 9.4 Sellability

A module may be purchased only if all required release conditions are satisfied.

At minimum:

- Lifecycle state permits commercial activation.
- Required functionality is implemented.
- Hard dependencies are available.
- Pricing configuration is valid.
- Required tests have passed.
- Required security review is complete.
- Required external integrations are configured.
- Product approval has been recorded.

A module marked `PLANNED` must not appear as an available purchasable module unless the product explicitly supports pre-orders or another approved commercial model.

## 9.5 Dependency enforcement

Dependency checks must be enforced in:

- Subscription changes.
- Module activation.
- Entitlement evaluation.
- Protected views and API endpoints.
- Application services.
- Background tasks.
- Integration workflows.
- Module-specific exports.

The UI may explain dependency requirements, but the server remains authoritative.

---

# 10. Module Activation Workflow

Activating a module must follow a controlled workflow.

## 10.1 Activation steps

1. Authenticate the initiating user.
2. Verify permission to manage the tenant subscription.
3. Load the current module catalogue.
4. Verify that the requested module is eligible for sale.
5. Validate the tenant's subscription state.
6. Evaluate hard dependencies.
7. Evaluate conditional dependencies applicable to the requested features.
8. Validate pricing and billing requirements.
9. Calculate the proposed entitlement changes.
10. Present any additional required modules and charges.
11. Obtain the required customer confirmation.
12. Execute the subscription change transactionally.
13. Record the entitlement changes.
14. Trigger required provisioning tasks.
15. Verify provisioning results.
16. Expose the module only when the required activation conditions are satisfied.

Payment authorization, payment capture and entitlement activation must follow the approved commercial model.

The system must not grant paid access merely because a client submitted a successful-looking request.

## 10.2 Dependency purchase options

If a customer selects a module with a hard dependency, the product may:

- Ask the customer to select the required module.
- Offer to add the required module to the same purchase.
- Reject the selection and explain the requirement.

The platform must not silently add a paid module without the required customer confirmation.

## 10.3 Atomicity

Subscription changes must preserve consistency.

The application must not leave the tenant in a partially committed state where:

- The parent module is active.
- A hard dependency is missing.
- The subscription charge is inconsistent.
- The entitlement record disagrees with the subscription.
- Provisioning status falsely reports completion.

Use database transactions and idempotent processing where appropriate.

External payment operations cannot generally be made atomic with a local database transaction. Use a documented payment workflow, idempotency keys and reconciliation procedures to handle partial failures.

## 10.4 Provisioning

If activation requires initialization, such as creating a default chart of accounts, provisioning must be idempotent.

Repeated task execution must not create duplicate records.

A provisioning failure must be visible and recoverable.

Do not expose a module as fully operational while its mandatory initialization is incomplete.

---

# 11. Module Deactivation and Subscription Changes

## 11.1 Core rule

**Disabling a module must not delete the module's business data.**

A subscription change affects access rights and operational availability, not ownership of historical records.

## 11.2 Dependency impact

Suppose:

```text
E_INVOICING -> INVOICING
```

If the tenant attempts to deactivate Invoicing, the system must evaluate the impact on E-Invoicing.

Possible outcomes:

- Reject deactivation while the dependent module remains active.
- Offer to deactivate dependent modules in the same approved change.
- Apply a documented alternative capability if one exists.

The system must not leave E-Invoicing active with an unsatisfied mandatory dependency.

## 11.3 Deactivation preview

Before deactivation, present a clear summary:

- Modules that will be disabled.
- Dependent modules affected.
- Features that will become unavailable.
- Records that will remain stored.
- Reports that may become unavailable.
- Scheduled tasks that will be stopped or adjusted.
- Integration connections that will be disabled.
- Existing workflows that require resolution.
- Any additional commercial consequences.

The preview must be calculated by the backend using the same dependency rules that will govern the actual change.

## 11.4 Existing records

When a module is disabled:

- Preserve its business records.
- Preserve relevant audit events.
- Preserve financial history.
- Prevent unauthorized creation or modification.
- Apply the approved read-only policy.
- Preserve required regulatory evidence.
- Prevent background tasks from performing unauthorized new actions.

## 11.5 Cross-module data

If Module A references records owned by Module B, deactivating Module B must not silently corrupt Module A.

The design must define whether Module A can:

- Continue displaying a historical snapshot.
- Continue displaying a limited read-only reference.
- Continue processing without the optional integration.
- Require reactivation of Module B for specific operations.

The correct behavior depends on the business meaning of the reference.

## 11.6 Grace periods

If the commercial model provides a grace period after expiry, the entitlement engine must represent it explicitly.

A grace period must define:

- Start and end times.
- Which operations remain available.
- Whether new transactions are permitted.
- Whether exports are permitted.
- Whether module dependencies remain active.
- What happens at the end of the grace period.

Do not implement an undocumented grace period in individual modules.

## 11.7 Data export and termination

The platform must define how tenants can retrieve authorized data after module cancellation or tenant termination.

Export policies must consider:

- Customer contracts.
- Applicable retention requirements.
- Personal data protection.
- Financial and tax record obligations.
- Legal holds.
- Security controls.
- Deletion schedules.

Module cancellation must not automatically trigger irreversible data deletion.

---

# 12. Dependency-Aware User Experience

## 12.1 Module catalogue

The module catalogue should distinguish:

- Available modules.
- Modules already subscribed to.
- Modules requiring additional dependencies.
- Modules unavailable because they are not yet released.
- Modules restricted by tenant or platform policy.
- Modules that require external provider configuration.

Do not show unavailable modules as purchasable merely because they are listed in a static frontend menu.

## 12.2 Dependency explanations

When a module cannot be activated, explain:

- Which requirement is missing.
- Why it is required.
- Whether it is a commercial module or a technical capability.
- What the customer can do next.

Example:

```text
Electronic Invoicing is not available.

Reason:
Your organization does not currently have the Invoicing module.

Next step:
Add Invoicing to your subscription, then configure
a supported electronic invoicing service provider.
```

The exact wording must reflect the real dependency and actual provider-integration status.

## 12.3 Navigation

The application should display only modules and features that are relevant to the tenant's current access.

Navigation visibility is a usability feature, not a security boundary.

A user must still receive an authorization denial if they directly request an unavailable route.

## 12.4 Module status

Where useful, display states such as:

- Active.
- Setup required.
- Temporarily unavailable.
- Subscription action required.
- Dependency missing.
- Read-only.
- Deactivation pending.

Do not expose internal implementation errors or sensitive configuration through status messages.

---

# 13. Django Application Dependency Architecture

Commercial module dependencies must not create circular Python imports or circular application-layer dependencies.

## 13.1 Dependency direction

Use a modular monolith with clear ownership boundaries.

A simplified direction is:

```text
Shared Platform
    |
    +-- Tenant and Identity Services
    +-- Authorization and Entitlement Services
    +-- Audit and Shared Infrastructure
             |
             v
       Business Domains
             |
             v
       Application Services
             |
             v
       External Integrations and Workers
```

This is conceptual. Actual calls should follow the approved application architecture and must not introduce hidden dependencies.

## 13.2 Cross-module calls

Modules should interact through documented application services or domain events.

Examples:

- Sales requests invoice creation through the Invoicing application service.
- Invoicing emits an invoice-issued event.
- Accounting consumes the event and creates the appropriate accounting transaction when entitled and configured.
- Inventory emits stock-movement events.
- Reporting reads approved data sources through explicit reporting interfaces.

A module must not directly modify another module's tables merely because they share PostgreSQL.

## 13.3 Avoid circular imports

Avoid designs such as:

```text
sales imports invoicing
invoicing imports accounting
accounting imports sales
```

Instead:

- Establish clear ownership.
- Use application-service interfaces.
- Use domain events for asynchronous reactions.
- Use explicit integration adapters.
- Use stable identifiers and documented data contracts.
- Keep dependency direction acyclic.

## 13.4 Shared primitives

If multiple domains need the same foundational data, determine whether it belongs to:

- A shared platform capability.
- A dedicated domain module.
- A stable reference-data service.

Do not move business logic into `core` simply to avoid import errors.

`core` must remain small and must not become the owner of all cross-module business behavior.

## 13.5 Django app installation

Django application installation is not the same as tenant entitlement.

A commercial app may be installed in the Django project while unavailable to a tenant.

Conversely, a tenant must not receive access to a module merely because the application is installed.

The module catalogue and entitlement engine determine tenant-level availability.

---

# 14. Data Ownership and Optional Modules

## 14.1 Authoritative ownership

Each business record must have one authoritative owner.

Examples:

- CRM owns lead lifecycle.
- Sales owns quotations and sales workflows.
- Invoicing owns invoice lifecycle.
- Accounting owns posted journal entries.
- Inventory owns stock movements.
- HRMS owns employee records if that is the approved product design.
- Payroll owns payroll calculations and payroll runs.

Other modules may reference these records through defined interfaces.

## 14.2 No implicit data deletion

Disabling a module must not delete records from another module.

Database relationships and deletion policies must reflect domain ownership.

Use deliberate foreign-key deletion behavior and explicit lifecycle transitions.

Do not use cascading deletion for business records unless the behavior is justified, reviewed and compatible with audit and retention requirements.

## 14.3 Historical snapshots

When a transaction requires historical values, store the necessary snapshot in the owning transaction.

Examples include:

- Invoice line descriptions and prices.
- Tax treatment applied at transaction time.
- Supplier or customer identity details required for historical evidence.
- Relevant accounting classifications.
- Submitted electronic-invoice payload evidence.

The snapshot must preserve the historical meaning of the transaction even if the referenced master data later changes.

## 14.4 Optional module references

If a module uses an optional integration, define what happens when that integration is unavailable.

Examples:

- CRM may retain a customer reference while an external CRM connector is disabled.
- Inventory may retain a stock movement after Accounting is disabled.
- Fixed Assets may preserve depreciation schedules even when automatic accounting posting is unavailable.

The business data must remain valid even when optional downstream processing is unavailable.

---

# 15. Database and Configuration Design

## 15.1 Central dependency configuration

Store dependency rules in a central, controlled configuration model or versioned registry.

Do not independently hardcode the same dependency in every view, serializer and task.

The dependency configuration should be the authoritative source for commercial dependency evaluation.

## 15.2 Suggested models

Potential models include:

- `subscriptions.ModuleDefinition`
- `subscriptions.ModuleDependency`
- `subscriptions.Subscription`
- `subscriptions.SubscriptionModule`
- `subscriptions.ModuleEntitlement`
- `subscriptions.EntitlementChange`
- `subscriptions.ModuleActivationJob`

The final names and ownership must align with `DATABASE_DESIGN.md`.

## 15.3 Dependency configuration fields

A dependency configuration may include:

```text
module_code
dependency_type
target_module_code
target_capability_code
condition_code
alternative_group_code
effective_from
effective_until
is_active
configuration_version
created_at
updated_at
```

Not all fields are required for every dependency type.

For example, a hard module dependency may use `target_module_code`, while a shared capability dependency may use `target_capability_code`.

## 15.4 Integrity constraints

Use database constraints where appropriate to enforce:

- Valid module references.
- Valid dependency types.
- Unique active dependency definitions.
- Valid effective date ranges.
- Valid relationship cardinality.
- Valid tenant entitlement references.

Application validation is still required for graph-level rules such as detecting indirect dependency cycles.

## 15.5 Versioning

Dependency configuration changes must be auditable and versioned.

When a dependency changes, record:

- Previous configuration.
- New configuration.
- Actor.
- Change reason.
- Effective date.
- Impact assessment.
- Approval status.

For major commercial changes, preserve the configuration version used to evaluate an existing subscription where required by the commercial model.

---

# 16. Dependency Evaluation Service

The entitlement engine should expose a small, documented service interface.

Illustrative interface:

```python
def validate_module_activation(
    *,
    tenant,
    requested_module_code,
    requested_features=None,
):
    """
    Validate whether a module can be activated for a tenant.

    The production implementation must:
    - Validate the module lifecycle and sellability.
    - Resolve direct and transitive hard dependencies.
    - Evaluate applicable conditional dependencies.
    - Evaluate alternative dependencies.
    - Check tenant subscription state.
    - Check dependency entitlement state.
    - Return structured, actionable validation results.
    - Avoid changing subscription state during validation.
    """
    raise NotImplementedError
```

This is an interface illustration, not production-ready code.

The implemented service must use the approved dependency configuration and actual subscription models.

## 16.1 Separate validation from execution

Dependency validation should not itself:

- Charge a payment method.
- Activate a subscription.
- Delete records.
- Disable dependent modules.
- Modify a tenant's permissions.

Validation should produce a result that can be reviewed and then executed through the appropriate subscription workflow.

## 16.2 Structured result

A validation result should provide machine-readable information.

Example:

```json
{
  "allowed": false,
  "module_code": "E_INVOICING",
  "missing_dependencies": [
    {
      "type": "HARD",
      "module_code": "INVOICING"
    }
  ],
  "warnings": [],
  "configuration_version": 1
}
```

The exact response schema must follow the project's API standards.

The frontend must not be treated as authoritative for the validation result.

## 16.3 Idempotency

Repeated evaluation of the same dependency configuration and tenant state should produce a consistent result.

Activation and deactivation operations must use appropriate idempotency controls so retries do not create duplicate subscription changes or conflicting entitlements.

## 16.4 Concurrency

The implementation must consider concurrent subscription changes.

For example, two administrators may attempt to enable and disable related modules at the same time.

Use appropriate transaction boundaries, row locking or concurrency controls to prevent inconsistent entitlement states.

---

# 17. Dependency Changes and Existing Customers

## 17.1 Changing a hard dependency

Adding a new mandatory dependency to an already sellable module can affect existing customers.

Before applying the change:

1. Identify affected subscriptions.
2. Calculate newly required modules.
3. Assess pricing and contractual implications.
4. Determine whether existing customers can retain the previous behavior.
5. Define migration and communication requirements.
6. Test the transition.
7. Obtain product approval.
8. Apply the change through a controlled rollout.

Do not automatically add paid dependencies to existing subscriptions without the required authorization.

## 17.2 Dependency removal

Removing a dependency may permit new module combinations.

The change must still be reviewed for:

- Data ownership.
- Application imports.
- Service calls.
- Integration workflows.
- API contracts.
- Background tasks.
- Existing records.
- Test coverage.

A dependency should not be removed solely to make activation succeed.

## 17.3 Versioned policies

Where commercial or operational requirements justify it, dependency policies may be versioned.

A subscription may record the relevant policy version or follow a migration to the current policy.

The implementation must define which policy applies to:

- New subscriptions.
- Renewals.
- Existing subscriptions.
- Subscription changes.
- Previously activated modules.

Avoid indefinite version branching unless a real contractual or technical requirement justifies it.

## 17.4 Backward compatibility

Dependency configuration changes must not silently invalidate existing tenants.

If an existing subscription becomes inconsistent under a new policy, the system must follow an approved migration or exception policy.

Any temporary exception must be explicit, auditable and time-bounded where appropriate.

---

# 18. Testing Strategy

Dependency tests must cover graph validation, activation, deactivation, entitlement evaluation and cross-module integration.

## 18.1 Graph validation tests

| ID | Scenario | Expected result |
|---|---|---|
| DEP-001 | Valid acyclic dependency graph | Accepted |
| DEP-002 | Module depends on itself | Rejected |
| DEP-003 | Two modules form a cycle | Rejected |
| DEP-004 | Three or more modules form an indirect cycle | Rejected |
| DEP-005 | Dependency references unknown module | Rejected |
| DEP-006 | Dependency references retired module | Rejected unless explicitly permitted |
| DEP-007 | Unsupported dependency type | Rejected |
| DEP-008 | Alternative group is invalid | Rejected |
| DEP-009 | Hard dependency has a missing transitive dependency | Activation rejected |
| DEP-010 | Conditional dependency is not applicable | Conditional requirement not enforced |
| DEP-011 | Conditional dependency is applicable | Requirement enforced |
| DEP-012 | Dependency configuration changes | Validation and audit rules apply |

## 18.2 Entitlement tests

| ID | Scenario | Expected result |
|---|---|---|
| DEP-013 | Module is implemented and sellable | Eligible for subscription evaluation |
| DEP-014 | Module is still planned | Commercial activation denied |
| DEP-015 | Hard dependency is not entitled | Activation denied |
| DEP-016 | All hard dependencies are satisfied | Activation may proceed |
| DEP-017 | Optional dependency is missing | Core module remains usable |
| DEP-018 | One valid alternative is available | Alternative requirement satisfied |
| DEP-019 | No valid alternative is available | Dependent capability unavailable |
| DEP-020 | Tenant subscription is expired | Access follows the approved expiry policy |
| DEP-021 | Dependency entitlement is revoked | Dependent access is recalculated |
| DEP-022 | Module is disabled by platform policy | Access denied |

## 18.3 Activation and deactivation tests

| ID | Scenario | Expected result |
|---|---|---|
| DEP-023 | Valid module activation | Entitlement transition is recorded |
| DEP-024 | Activation has a missing hard dependency | No invalid entitlement is created |
| DEP-025 | Activation is retried | No duplicate activation side effects |
| DEP-026 | Provisioning fails | Failure is visible and recoverable |
| DEP-027 | Parent module is deactivated while dependent module is active | Deactivation is blocked or dependents are handled through the approved workflow |
| DEP-028 | Module is disabled | Business records are retained |
| DEP-029 | Module is reactivated | Existing records remain consistent |
| DEP-030 | Concurrent subscription changes occur | No inconsistent dependency state is committed |

## 18.4 Cross-module tests

| ID | Scenario | Expected result |
|---|---|---|
| DEP-031 | Sales creates an invoice through the supported service | Ownership and validation rules are respected |
| DEP-032 | Accounting consumes an invoice event | Duplicate processing is prevented |
| DEP-033 | Accounting is unavailable or not entitled | Invoice behavior follows the approved integration policy |
| DEP-034 | Inventory generates a stock movement | Inventory remains authoritative for the movement |
| DEP-035 | Optional integration is disabled | Core domain data remains intact |
| DEP-036 | Tenant has one module but lacks another module's entitlement | Unauthorized cross-module operation is denied |
| DEP-037 | Background event is delivered more than once | Processing remains idempotent |
| DEP-038 | Dependency configuration changes | Existing tenant behavior follows the approved migration policy |

Tests must be executed against the actual implementation.

A test plan or a passing static check is not evidence that the behavior works unless the relevant tests were run.

---

# 19. Implementation Roadmap

| Phase | Dependency Work |
|---|---|
| P0 — Foundation | Establish module identifiers, configuration standards and architectural boundaries |
| P1 — Core Platform | Establish tenant context, identity and authorization interfaces |
| P2 — Subscription Engine | Implement module registry, dependency graph, subscription selection and entitlement evaluation |
| P3 — CRM, Sales and Invoicing | Implement initial commercial dependencies and invoice integration contracts |
| P4 — UAE E-Invoicing | Enforce invoice dependency and provider-readiness checks |
| P5 — Accounting and VAT | Implement accounting and tax integration requirements |
| P6 — Procurement and Inventory | Implement purchasing and stock integration rules |
| P7 — HRMS and Payroll | Implement employee-master and payroll dependencies |
| P8 — Projects, Expenses and Assets | Implement conditional accounting and project integrations |
| P9 — Banking and Advanced Finance | Implement banking and accounting integration requirements |
| P10 — Reporting and Integrations | Implement dependency-aware reports, exports and external connectors |
| P11 — Enterprise Readiness | Review dependency migrations, compatibility and administrative controls |
| P12 — Production Launch | Validate dependency changes, recovery procedures and production entitlement consistency |

The dependency engine must be implemented early enough that subsequent commercial modules can use it rather than introducing local, inconsistent dependency checks.

---

# 20. Pending Product Decisions

The following decisions require product approval.

| ID | Decision | Question |
|---|---|---|
| MOD-DEC-001 | Sales and CRM | Can Sales operate independently of CRM? |
| MOD-DEC-002 | Invoicing and Accounting | Is standalone invoicing a supported product configuration? |
| MOD-DEC-003 | VAT and Accounting | Is Accounting mandatory for all VAT functionality, or only selected features? |
| MOD-DEC-004 | Payroll and HRMS | Must Payroll require the commercial HRMS module, or can it use a shared employee master? |
| MOD-DEC-005 | Fixed Assets | Can asset-register functionality be sold without Accounting? |
| MOD-DEC-006 | Banking | Which banking features can operate without Accounting? |
| MOD-DEC-007 | Procurement and Inventory | Which purchasing workflows require Inventory? |
| MOD-DEC-008 | Reporting | Can Reporting be purchased independently, and which data sources are included? |
| MOD-DEC-009 | Integrations | Is Integrations a commercial module, a shared platform capability, or a combination? |
| MOD-DEC-010 | Dependency pricing | Are required modules always billed separately, bundled or included in selected plans? |
| MOD-DEC-011 | Subscription expiry | Which operations remain available during grace periods? |
| MOD-DEC-012 | Deactivation | Should dependent modules be automatically deactivated, or should customer confirmation be required? |
| MOD-DEC-013 | Historical access | What read-only access remains after module cancellation? |
| MOD-DEC-014 | Existing customers | How are new dependencies applied to existing subscriptions? |
| MOD-DEC-015 | Provider integrations | Which external providers require a commercial Integrations entitlement? |
| MOD-DEC-016 | Module release | What evidence is required before a module becomes sellable? |

Approved decisions must be recorded in:

`docs/01-architecture/ARCHITECTURAL_DECISIONS/`

Commercial dependencies must also be reflected in `COMMERCIAL_MODEL.md` and `MODULE_CATALOGUE.md`.

---

# 21. Instructions for Codex and Development Agents

All development agents must follow this document.

## 21.1 Before changing dependencies

The agent must:

1. Read the module catalogue.
2. Read the subscription and entitlement design.
3. Identify the authoritative owner of each affected data domain.
4. Review the current dependency graph.
5. Check for direct and indirect cycles.
6. Identify affected tenants and subscriptions.
7. Assess pricing and commercial implications.
8. Assess data migration and backward-compatibility implications.
9. Define required tests.
10. Request approval for unresolved product decisions.

## 21.2 During implementation

The agent must:

- Use the central module registry.
- Use the central dependency configuration.
- Use the entitlement engine.
- Preserve application ownership boundaries.
- Use documented cross-module interfaces.
- Keep subscription changes transactional where possible.
- Make background processing idempotent.
- Preserve existing business data.
- Add dependency and regression tests.
- Update affected architecture and commercial documents.

## 21.3 Prohibited shortcuts

Agents must not:

- Hardcode dependency rules independently in multiple modules.
- Treat every integration as a mandatory commercial dependency.
- Create circular application imports.
- Activate a module with unsatisfied hard dependencies.
- Automatically charge for a dependency without approved customer authorization.
- Delete business data when a module is disabled.
- Assume that application installation grants tenant entitlement.
- Assume that a tenant entitlement grants every user permission.
- Bypass the entitlement engine in background tasks.
- Change the dependency graph without validation and tests.
- Claim that unexecuted tests have passed.

## 21.4 Required implementation report

For each dependency-engine change, report:

- Modules affected.
- Dependencies added, removed or modified.
- Graph-validation result.
- Entitlement changes.
- Existing-customer impact.
- Data migration impact.
- Tests executed.
- Actual test results.
- Known limitations.
- Decisions requiring product approval.

---

# 22. Definition of Done

The module dependency architecture is ready for production consideration when:

- [ ] Every module has a unique, stable module code.
- [ ] Commercial and platform modules are distinguished.
- [ ] Every approved dependency has a defined type and purpose.
- [ ] Hard dependencies are resolved transitively.
- [ ] Optional dependencies do not block core functionality.
- [ ] Conditional dependencies use explicit, testable conditions.
- [ ] Alternative dependencies are evaluated correctly.
- [ ] Dependency cycles are rejected.
- [ ] Module sellability is separate from application installation.
- [ ] Module entitlement is separate from user permission.
- [ ] Subscription changes are validated centrally.
- [ ] Activation and deactivation workflows are idempotent.
- [ ] Concurrent subscription changes cannot commit inconsistent states.
- [ ] Dependent modules are handled correctly during deactivation.
- [ ] Business records are preserved when modules are disabled.
- [ ] Cross-module data ownership is documented.
- [ ] Django applications use approved integration interfaces.
- [ ] Dependency changes are versioned and auditable.
- [ ] Existing-customer impact is assessed before dependency changes.
- [ ] Automated tests cover graph validation and entitlement behavior.
- [ ] Commercial documentation reflects approved dependencies.
- [ ] Production release criteria are satisfied.

**Release rule:** No commercial module may be activated unless its sellability, subscription state and applicable dependency requirements have been validated by the central entitlement system.

---

# 23. Final Architectural Rule

The module dependency system must preserve three independent boundaries:

```text
COMMERCIAL BOUNDARY
Can this tenant access the module under its subscription?

APPLICATION BOUNDARY
Can the module execute using the required capabilities
and supported cross-module interfaces?

SECURITY BOUNDARY
Can this user perform this operation on this record
within the authorized tenant and organizational scope?
```

All three boundaries must be satisfied before a protected operation proceeds.

The result is a modular SaaS product that supports configurable module selection without coupling commercial packaging, Django application imports and user authorization into a single fragile mechanism.
