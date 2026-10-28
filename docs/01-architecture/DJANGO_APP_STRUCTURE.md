# UAE ERP SaaS — Django Application Structure

| Property | Value |
|---|---|
| Document ID | ARCH-002 |
| Version | 1.0 |
| Status | APPROVED — Architecture Baseline |
| Product | UAE ERP SaaS |
| Framework | Django |
| API Framework | Django REST Framework, where required |
| Architecture | Modular Monolith |
| Database | PostgreSQL |
| Frontend | Django Templates, HTMX, Tailwind CSS |
| Background Processing | Celery and Redis |
| Parent Documents | SYSTEM_ARCHITECTURE.md, DATABASE_DESIGN.md, MULTI_TENANCY.md, AUTHENTICATION_AND_PERMISSIONS.md, MODULE_DEPENDENCIES.md, ENTITLEMENT_ENGINE.md |

---

# 1. Purpose

This document defines the implementation-level Django application structure for the UAE ERP SaaS platform.

It establishes:

- The Django project layout.
- The responsibility of each Django application.
- Model ownership.
- Service-layer conventions.
- Query and data-access patterns.
- Cross-application communication rules.
- URL and API organization.
- Forms, serializers, templates, and static asset conventions.
- Background-task organization.
- Testing conventions.
- Database migration rules.
- Module activation and entitlement integration.
- Architectural constraints for OpenAI Codex.

The purpose is to prevent the project from becoming a tightly coupled collection of Django apps with duplicated business logic and unclear ownership.

**All implementation agents must follow this document unless an approved architecture decision explicitly changes it.**

---

# 2. Core Structural Decisions

The initial application structure follows these decisions.

| Decision | Standard |
|---|---|
| Django project | One project |
| Deployment model | Modular monolith |
| Django applications | Separate apps for platform and business domains |
| Database | Shared PostgreSQL database and schema initially |
| Tenant isolation | Explicit tenant ownership and authorization |
| Business logic | Application services and domain rules |
| Database writes | Through approved domain services for significant business operations |
| Frontend | Django Templates, HTMX, Tailwind CSS |
| API | Django REST Framework where required |
| Background jobs | Celery tasks calling application services |
| External integrations | Provider adapters |
| Financial transactions | Explicit transactional services and database constraints |
| Tests | Domain-specific tests plus cross-domain integration tests |
| App dependencies | Explicit, documented, and acyclic wherever practical |

## 2.1 Structural principles

1. Each app must have a clearly defined responsibility.
2. Each business record must have an authoritative owning domain.
3. A domain must not bypass another domain's business rules.
4. Shared utilities must remain small and generic.
5. Business logic must not be implemented exclusively in views, templates, or serializers.
6. Background tasks must reuse the same application services as synchronous workflows.
7. Tenant isolation must be enforced server-side.
8. Module entitlements must be checked through the approved entitlement interface.
9. Database migrations must be reviewed and tested.
10. New apps must be introduced only when their responsibilities are sufficiently clear.

---

# 3. Recommended Repository Structure

The following is the target structure for the application.

Not every directory or application needs to exist in Phase 0. Apps should be created progressively according to the approved development roadmap.

```text
uae-erp-saas/
│
├── AGENTS.md
├── README.md
├── manage.py
├── pyproject.toml
├── uv.lock                         # If uv is selected as dependency manager
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .env.example
│
├── config/
│   ├── __init__.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   ├── celery.py
│   │
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── test.py
│       └── production.py
│
├── apps/
│   ├── __init__.py
│   │
│   ├── core/
│   ├── tenants/
│   ├── users/
│   ├── audit/
│   │
│   ├── subscriptions/
│   ├── billing/
│   │
│   ├── crm/
│   ├── sales/
│   ├── invoicing/
│   ├── e_invoicing/
│   │
│   ├── accounting/
│   ├── vat/
│   │
│   ├── procurement/
│   ├── inventory/
│   │
│   ├── hrms/
│   ├── payroll/
│   │
│   ├── projects/
│   ├── expenses/
│   ├── fixed_assets/
│   │
│   ├── banking/
│   ├── reporting/
│   └── integrations/
│
├── templates/
│   ├── base.html
│   ├── layouts/
│   ├── components/
│   ├── errors/
│   └── registration/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── vendor/
│
├── tests/
│   ├── architecture/
│   ├── integration/
│   ├── security/
│   └── end_to_end/
│
├── scripts/
│   ├── development/
│   ├── deployment/
│   └── maintenance/
│
├── docs/
│   ├── 00-product/
│   ├── 01-architecture/
│   ├── 02-phases/
│   ├── 03-modules/
│   ├── 04-agents/
│   ├── 05-quality/
│   ├── 06-deployment/
│   └── 07-project-management/
│
├── orchestration/
│   ├── phase-manifest.yml
│   ├── task-manifest.yml
│   └── notification-config.example.yml
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── security-checks.yml
        └── phase-validation.yml
```

## 3.1 Naming conventions

Use the following conventions consistently:

- Django project package: `config`.
- Django application package: `apps.<app_name>`.
- Python modules: lowercase with underscores.
- Django model classes: singular PascalCase names.
- Service modules: descriptive nouns or business operations.
- Test files: `test_<subject>.py`.
- Architecture documents: uppercase or descriptive filenames matching the repository's established convention.
- Module identifiers: stable uppercase codes such as `INVOICING` and `ACCOUNTING`.

Do not rename applications or change Django app labels casually after migrations have been deployed.

---

# 4. Standard Django Application Layout

Each business app should use a consistent structure appropriate to its complexity.

Example: `apps/invoicing/`

```text
apps/
└── invoicing/
    ├── __init__.py
    ├── apps.py
    ├── admin.py
    ├── models.py
    ├── managers.py
    ├── querysets.py
    ├── selectors.py
    ├── services.py
    ├── permissions.py
    ├── validators.py
    ├── forms.py
    ├── serializers.py
    ├── views.py
    ├── api_views.py
    ├── urls.py
    ├── api_urls.py
    ├── tasks.py
    ├── signals.py
    ├── constants.py
    │
    ├── migrations/
    │   └── __init__.py
    │
    ├── templates/
    │   └── invoicing/
    │       ├── invoice_list.html
    │       ├── invoice_detail.html
    │       ├── invoice_form.html
    │       └── components/
    │
    ├── static/
    │   └── invoicing/
    │
    └── tests/
        ├── __init__.py
        ├── factories.py
        ├── test_models.py
        ├── test_services.py
        ├── test_selectors.py
        ├── test_permissions.py
        ├── test_views.py
        ├── test_api.py
        └── test_tasks.py
```

This structure is a reference, not a requirement to create empty files in every app.

## 4.1 Keep simple apps simple

A small app may begin with:

```text
apps/example/
├── __init__.py
├── apps.py
├── models.py
├── services.py
├── urls.py
├── views.py
├── migrations/
└── tests/
```

Add additional modules when actual complexity justifies them.

Do not create empty directories and placeholder files merely to make the repository look complete.

## 4.2 Split large modules deliberately

If a domain grows beyond a manageable `models.py` or `services.py`, split it by meaningful responsibility.

For example:

```text
apps/invoicing/
├── models/
│   ├── __init__.py
│   ├── invoice.py
│   ├── invoice_line.py
│   └── credit_note.py
│
├── services/
│   ├── __init__.py
│   ├── creation.py
│   ├── issuance.py
│   ├── cancellation.py
│   └── payment_allocation.py
│
└── tests/
```

When models are split into a package, import them through the package's public `models` interface so Django discovers them consistently.

Do not split files merely because they exceed an arbitrary line count. Split them when distinct responsibilities or maintainability concerns justify the change.

---

# 5. Application Responsibility Matrix

The following table establishes initial domain ownership.

> **Accepted decision:** ADR-003 assigns `TenantMembership` to `tenants`. The `users` application owns identity, roles, permissions, and membership-role assignments, but not the membership record itself.

| Application | Primary Responsibility | Owns Primary Records | Commercial Module |
|---|---|---|---|
| `core` | Shared technical foundations | Generic shared infrastructure records, if required | No |
| `tenants` | Organization, tenant lifecycle, and membership relationships | Tenant, tenant configuration, `TenantMembership`, legal entity, branch | No |
| `users` | User identity, authentication, roles, and permissions | User, roles, permissions, membership-role assignments | No |
| `audit` | Business and security audit records | Audit events | No |
| `subscriptions` | Plans, subscriptions, and entitlements | Subscription, subscription lines, entitlement state | Platform |
| `billing` | SaaS charges and payment processing records | SaaS billing documents and payment records | Platform |
| `crm` | Leads, contacts, and CRM activity | Lead, CRM activity, contact records if owned here | Yes |
| `sales` | Quotations and sales workflow | Quotation and quotation lines | Yes |
| `invoicing` | Customer invoices and credit notes | Invoice, invoice lines, credit notes | Yes |
| `e_invoicing` | External e-invoicing submissions | Submission records and provider references | Yes |
| `accounting` | Ledger and accounting operations | Accounts, journals, ledger entries, fiscal periods | Yes |
| `vat` | Tax configuration and calculation | VAT codes, tax rules, tax configuration | Yes |
| `procurement` | Purchasing workflow | Purchase orders and related purchasing records | Yes |
| `inventory` | Stock control and valuation | Stock locations, stock movements, valuation records | Yes |
| `hrms` | Employee and HR workflows | Employee and HR records | Yes |
| `payroll` | Payroll calculations and processing | Payroll runs, payroll results, payslips | Yes |
| `projects` | Project and task management | Projects, tasks, milestones | Yes |
| `expenses` | Expense claims and approvals | Expense claims and related records | Yes |
| `fixed_assets` | Asset register and depreciation | Fixed assets and depreciation records | Yes |
| `banking` | Bank statements and reconciliation | Bank statements and reconciliation records | Yes |
| `reporting` | Reporting and dashboard execution | Report definitions and execution records, where needed | Yes |
| `integrations` | Generic integration infrastructure | Integration configurations and delivery records | Platform or shared capability |

**Ownership clarification:** The table identifies the initial default owner. Before implementation, the module specifications must settle shared entities such as contacts, products, payments, and document attachments. Codex must not independently create competing authoritative models for the same business concept.

---

# 6. `core` Application

**Path:** `apps/core/`

## 6.1 Responsibilities

The `core` app contains small, reusable platform primitives that do not belong to a particular business domain.

Possible responsibilities include:

- Shared abstract model mixins.
- Generic timestamp fields.
- Common exception types.
- Generic health-check support.
- Shared low-level utilities.
- Approved common validation helpers.

## 6.2 What does not belong here

Do not place the following in `core` merely because several apps use them:

- Invoice business rules.
- Accounting logic.
- Tenant subscription policies.
- Payroll calculations.
- Inventory valuation.
- Generic models representing unrelated business documents.
- A central service that performs every business operation.

Shared code must be genuinely generic.

## 6.3 Abstract model example

```python
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

This model may be used by domain models that need these fields.

Do not introduce abstract base classes containing many optional fields that unrelated models inherit without needing them.

---

# 7. `tenants` Application

**Path:** `apps/tenants/`

## 7.1 Responsibilities

- Tenant creation and lifecycle.
- Organization-level configuration.
- Tenant activation and suspension.
- Tenant context resolution support.
- Tenant-specific settings.
- Tenant onboarding state.

## 7.2 Primary records

The initial specification should define records such as:

- `Tenant`
- `TenantSettings`, if separate configuration is justified.

The exact model design belongs in `DATABASE_DESIGN.md`.

## 7.3 Rules

- Tenant identity must be stable.
- Tenant status transitions must be validated.
- Tenant-owned business records must have a consistent ownership strategy.
- Tenant selection must not be treated as proof of authorization.
- Deactivation must follow a defined access and data-retention policy.
- Tenant deletion must not silently destroy records subject to retention requirements.

---

# 8. `users` Application

**Path:** `apps/users/`

## 8.1 Responsibilities

- User identity.
- Authentication integration.
- Role and permission definitions and assignments for tenant memberships owned by `tenants`.
- Role assignment.
- User activation and deactivation.
- Organization-level access configuration.
- Permission-related user workflows.

## 8.2 Custom user model

A custom Django user model should be selected and configured before the first production migration.

The initial implementation should use a custom user model derived from Django's supported user abstractions unless a documented decision establishes a different approach.

Configure `AUTH_USER_MODEL` before creating the initial migration history.

Changing the user model after production data exists can be difficult and must not be treated as an ordinary refactor.

## 8.3 Membership and roles

User identity and tenant membership are different concepts.

A single user may belong to more than one tenant if that capability is approved.

`tenants.TenantMembership` records determine which organizations the user can access. The `users` application may own role assignments that reference an active membership through the approved domain contract.

Role assignment must not be inferred solely from a user having a particular email address or being the first user created.

---

# 9. `audit` Application

**Path:** `apps/audit/`

## 9.1 Responsibilities

- Record significant business actions.
- Record security-sensitive changes.
- Record privileged administrative operations.
- Provide controlled audit-event retrieval.
- Support investigation of business and security incidents.

## 9.2 Audit design principles

Audit records should be append-oriented and protected against unauthorized modification.

Where stronger tamper resistance is required, additional controls must be designed and documented; an ordinary database table alone does not guarantee immutable evidence.

Audit events must not contain unnecessary secrets or sensitive document contents.

## 9.3 Integration

Domains should use an approved audit service or event-recording interface.

Do not duplicate audit formatting and sensitive-data filtering in every view.

Audit events required for a critical business operation should be recorded with appropriate transaction semantics so that the business action and its audit evidence do not become unintentionally inconsistent.

---

# 10. `subscriptions` Application

**Path:** `apps/subscriptions/`

## 10.1 Responsibilities

- Module catalogue integration.
- Subscription plans or configurable commercial arrangements.
- Subscription line items.
- Subscription lifecycle.
- Module entitlement evaluation.
- Module dependency validation.
- Trials, renewal, suspension, and cancellation rules where approved.

## 10.2 Boundaries

The app determines whether a tenant's subscription permits access to a module.

It must not take over the accounting or invoicing rules of a tenant's ERP business.

The SaaS billing domain owns the platform's billing records and payment-related financial records.

## 10.3 Required interfaces

Provide explicit service interfaces for:

- Evaluating module entitlements.
- Validating module dependencies.
- Activating or changing a subscription.
- Suspending or cancelling a subscription.
- Resolving effective subscription state.

The exact function signatures must be defined in `ENTITLEMENT_ENGINE.md`.

---

# 11. `billing` Application

**Path:** `apps/billing/`

## 11.1 Responsibilities

- SaaS subscription charges.
- SaaS billing documents.
- Payment-provider integration.
- Payment attempts and results.
- Subscription billing history.
- Payment-provider webhook processing.
- Refund or credit workflows where approved.

## 11.2 Critical boundary

SaaS billing is not the same as ERP customer invoicing.

Do not use the `invoicing.Invoice` model to represent charges that the platform operator makes to SaaS subscribers unless an explicit and justified design establishes that relationship.

The platform's commercial relationship with its subscribers and each tenant's commercial relationship with its own customers are separate domains.

---

# 12. `crm` Application

**Path:** `apps/crm/`

## 12.1 Responsibilities

- Lead management.
- CRM activity tracking.
- Lead assignment.
- Lead qualification.
- Customer relationship history.
- CRM search and filtering.

## 12.2 Contact and customer ownership

Before implementation, explicitly decide whether the authoritative customer and contact records belong to CRM or a separate shared customer master-data domain.

Do not create independent, conflicting customer records in CRM, sales, and invoicing.

If CRM owns the customer record, other domains should reference that record through a documented interface.

If a separate customer domain is later justified, the migration must preserve identity, references, and historical relationships.

---

# 13. `sales` Application

**Path:** `apps/sales/`

## 13.1 Responsibilities

- Quotations.
- Quotation line items.
- Quotation status transitions.
- Sales document numbering.
- Quotation approval where required.
- Conversion of an approved quotation into an invoice through the invoicing service.

## 13.2 Boundaries

Sales owns the quotation lifecycle.

Invoicing owns the invoice lifecycle.

The sales app must not directly create a partially initialized invoice by writing arbitrary fields into the invoicing app's models.

Instead, it should invoke an approved invoicing application service.

---

# 14. `invoicing` Application

**Path:** `apps/invoicing/`

## 14.1 Responsibilities

- Customer invoices.
- Invoice line items.
- Invoice numbering.
- Invoice issuance.
- Invoice lifecycle and status transitions.
- Credit notes and correction workflows.
- Payment allocation interfaces where approved.
- Printable invoice documents.

## 14.2 Business rules

- Invoice totals are calculated on the server.
- Issued invoices cannot be silently overwritten.
- Financial corrections follow approved workflows.
- Document numbers follow an approved uniqueness and sequencing strategy.
- Tax calculations use the approved tax interface.
- Tenant ownership is validated for related customer and product records.
- Invoice state transitions are enforced by application services.

## 14.3 Required service boundaries

The app should expose controlled operations for:

- Creating a draft invoice.
- Updating an eligible draft.
- Validating an invoice.
- Issuing an invoice.
- Cancelling or correcting an invoice where permitted.
- Retrieving an authorized invoice representation.

The exact operations depend on the approved invoicing specification.

---

# 15. `e_invoicing` Application

**Path:** `apps/e_invoicing/`

## 15.1 Responsibilities

- Provider configuration references.
- Submission records.
- Provider request and response metadata.
- Submission status tracking.
- Retry coordination.
- Reconciliation.
- Provider-specific adapters.

## 15.2 Boundaries

The app must not become the authoritative owner of the internal invoice.

It owns the integration workflow and provider-facing state.

The internal invoice remains owned by `invoicing`.

## 15.3 Implementation rules

- Use provider adapters.
- Preserve provider identifiers separately from internal identifiers.
- Apply idempotency controls.
- Handle uncertain submission outcomes explicitly.
- Do not assume a timeout means the provider rejected the invoice.
- Keep credentials out of source control.
- Do not claim regulatory compliance without validated requirements and appropriate review.

---

# 16. `accounting` Application

**Path:** `apps/accounting/`

## 16.1 Responsibilities

- Chart of accounts.
- Fiscal periods.
- Journal entries.
- Journal entry lines.
- Posting and reversal.
- General ledger.
- Trial balance.
- Accounting period closure.
- Financial reporting foundations.

## 16.2 Ownership

The accounting domain owns the authoritative accounting ledger and posting rules.

Other apps must request posting through the approved accounting service rather than directly inserting ledger entries.

## 16.3 Required invariants

- Posted journal entries must balance.
- Posting must be transactional.
- Duplicate posting must be prevented.
- Posted records must preserve their audit history.
- Closed periods must enforce approved restrictions.
- Corrections must use controlled reversal or adjustment operations.

---

# 17. `vat` Application

**Path:** `apps/vat/`

## 17.1 Responsibilities

- VAT codes.
- Tax rule configuration.
- Tax calculation.
- Tax treatment validation.
- Supported tax reporting logic.
- Effective dates or versioning where required.

## 17.2 Boundaries

VAT calculation is a tax-domain responsibility.

Invoicing, procurement, and accounting may invoke the VAT service through documented interfaces.

The VAT app must not own the full lifecycle of invoices, purchase orders, or journal entries.

Tax rules must be validated against the requirements applicable to the product's supported scenarios.

---

# 18. `procurement` Application

**Path:** `apps/procurement/`

## 18.1 Responsibilities

- Purchase requisitions where approved.
- Purchase orders.
- Purchase order lines.
- Supplier purchasing workflows.
- Goods receipt coordination.
- Supplier invoice references.
- Purchase workflow approvals.

## 18.2 Boundaries

Procurement owns purchasing workflow records.

Inventory owns the stock movement records created when goods are received or transferred.

Accounting owns the resulting ledger entries where accounting integration is enabled.

The workflow between these domains must be explicit and must handle partial failures.

---

# 19. `inventory` Application

**Path:** `apps/inventory/`

## 19.1 Responsibilities

- Products or inventory-item references, depending on the approved master-data ownership decision.
- Warehouses.
- Stock locations.
- Stock movements.
- Transfers.
- Stock adjustments.
- Stock availability.
- Stock valuation.

## 19.2 Invariants

- Every stock change must have an identifiable source or approved adjustment.
- Concurrent transactions must preserve stock consistency.
- Stock movements must be auditable.
- Negative stock behavior must follow an approved policy.
- Inventory valuation must follow an approved method.
- Financial integration must use the accounting service.

---

# 20. `hrms` Application

**Path:** `apps/hrms/`

## 20.1 Responsibilities

- Employee records.
- Departments and designations.
- Employment status.
- HR documents.
- Leave requests.
- Leave policies and balances.
- Employee-related workflows.

## 20.2 Security

Employee information must have appropriate access controls.

Sensitive employee documents must not be exposed through unrestricted media URLs or unprotected exports.

HRMS must not assume that every authenticated tenant user can access all employee information.

---

# 21. `payroll` Application

**Path:** `apps/payroll/`

## 21.1 Responsibilities

- Payroll periods.
- Payroll runs.
- Earnings and deductions.
- Payroll calculations.
- Payroll review and approval.
- Payslip generation.
- Payroll history.
- Accounting integration where approved.

## 21.2 Boundaries

HRMS owns employee and employment records.

Payroll owns payroll runs and calculation results.

Payroll may read approved employee information through documented interfaces, but it must not take ownership of the HRMS employee lifecycle.

## 21.3 Controls

- Payroll calculations must be deterministic for fixed inputs and rule versions.
- Finalized payroll must not be silently overwritten.
- Sensitive payroll data must be access-controlled.
- Corrections must preserve historical evidence.
- Applicable statutory rules must be validated for the supported scope.

---

# 22. `projects` Application

**Path:** `apps/projects/`

## Responsibilities

- Projects.
- Tasks.
- Milestones.
- Project status.
- Project ownership.
- Project-related operational reporting.
- References to relevant customers and commercial records.

Project cost and revenue calculations must use approved financial integration contracts rather than inventing separate authoritative financial balances.

---

# 23. `expenses` Application

**Path:** `apps/expenses/`

## Responsibilities

- Expense claims.
- Expense categories.
- Receipt references.
- Approval workflows.
- Reimbursement status.
- Accounting integration.

The app must validate the submitter, tenant, approval authority, and current expense state.

Where expense posting is enabled, the accounting service must own the ledger operation.

---

# 24. `fixed_assets` Application

**Path:** `apps/fixed_assets/`

## Responsibilities

- Asset register.
- Asset categories.
- Acquisition records.
- In-service dates.
- Depreciation configuration.
- Depreciation schedules.
- Asset disposal and retirement.
- Accounting integration.

The asset register and depreciation schedule belong to this domain.

The accounting ledger remains authoritative for posted accounting balances.

---

# 25. `banking` Application

**Path:** `apps/banking/`

## Responsibilities

- Bank account references.
- Statement imports.
- Imported bank transactions.
- Matching and reconciliation.
- Unmatched transaction review.
- Reconciliation status.
- Optional bank-provider integration.

Statement imports must be protected against unintended duplicate processing.

Reconciliation must preserve an audit trail and must not silently modify posted accounting records.

---

# 26. `reporting` Application

**Path:** `apps/reporting/`

## Responsibilities

- Report definitions.
- Dashboard configuration where required.
- Report execution.
- Export generation.
- Report status and history where needed.
- Approved read-only aggregation interfaces.

## 26.1 Boundaries

Reporting must not become a second source of truth for financial records.

Financial reports must derive from the approved accounting records or another explicitly authoritative source.

Report queries must respect tenant isolation, permissions, and module entitlements.

Large exports should use background tasks where appropriate.

---

# 27. `integrations` Application

**Path:** `apps/integrations/`

## Responsibilities

- Generic integration configuration.
- Integration status.
- Webhook delivery records.
- Generic retry coordination.
- External event tracking.
- Integration health metadata.

## 27.1 Boundaries

This app provides shared integration infrastructure.

Provider-specific business behavior should remain with the relevant domain adapter.

Examples:

- E-invoicing submission logic belongs to `e_invoicing`.
- SaaS payment logic belongs to `billing`.
- Bank reconciliation logic belongs to `banking`.

The generic integration app must not become a universal place for unrelated provider business rules.

---

# 28. Standard Application Layers

Each substantial domain should use a consistent division of responsibility.

## 28.1 Models

Models represent persisted domain state and enforce local invariants where appropriate.

They may contain:

- Field definitions.
- Relationships.
- Database constraints.
- Local validation methods where suitable.
- Simple derived properties.
- Model metadata.

Models should not become the sole location for large multi-step business workflows.

## 28.2 Services

Services implement application use cases and controlled business state transitions.

Examples:

- `issue_invoice()`
- `post_journal_entry()`
- `receive_goods()`
- `finalize_payroll_run()`
- `evaluate_module_entitlement()`

Service operations should define their transaction boundaries, authorization assumptions, idempotency requirements, and expected failure modes.

## 28.3 Selectors and queries

Selectors encapsulate complex or reusable read operations.

Examples:

- `get_invoice_detail()`
- `list_open_invoices()`
- `get_trial_balance()`
- `get_available_stock()`

A selector must not bypass tenant scoping or permissions.

A selector is not required for every simple ORM lookup. Use one where it improves clarity, reuse, or testability.

## 28.4 Views

Views handle HTTP concerns:

- Request parsing.
- Authentication and permission checks.
- Form or serializer validation.
- Calling application services.
- Selecting templates or response formats.
- Translating expected application errors into HTTP responses.

Views should not contain complex financial calculations or large multi-step business workflows.

## 28.5 Forms and serializers

Forms and serializers validate incoming presentation-layer data.

They must not be treated as the only enforcement point for business invariants, because application services may also be invoked by tasks, management commands, or other apps.

## 28.6 Tasks

Celery tasks orchestrate asynchronous execution.

They should load current records, establish tenant context, and call application services.

They should not reimplement the same business workflow independently.

---

# 29. Service-Layer Standards

For significant business operations, use explicit service functions.

Illustrative example:

```python
# apps/invoicing/services.py

from django.db import transaction


@transaction.atomic
def issue_invoice(*, invoice_id, tenant_id, actor):
    """
    Issue a draft invoice after validating ownership,
    permissions, current state, and business rules.

    This is an illustrative signature. The final implementation
    must follow the approved invoice and authorization contracts.
    """
    # 1. Load the invoice within the authorized tenant.
    # 2. Validate the actor's permission.
    # 3. Validate the invoice's current state.
    # 4. Validate totals and required data.
    # 5. Apply the approved issuance transition.
    # 6. Record the required audit event.
    # 7. Return the resulting invoice.
    raise NotImplementedError
```

This example demonstrates the intended structure, not an implementation ready for production.

## 29.1 Service rules

- Use keyword arguments for nontrivial service functions.
- Make transaction boundaries explicit.
- Validate tenant ownership.
- Validate current workflow state.
- Enforce business invariants.
- Apply appropriate authorization checks or require a documented trusted authorization context.
- Use durable idempotency controls where needed.
- Return a documented result or raise a documented application exception.
- Avoid hidden side effects.
- Add tests for success, validation failures, authorization failures, and concurrency-sensitive behavior.

## 29.2 Service authorization

Do not assume that a service is safe merely because it is called from a protected view.

A service may be invoked from an API, a task, a management command, or another app.

The service must either enforce the relevant authorization policy or require an explicit trusted context whose validation is guaranteed by the documented calling contract.

## 29.3 Transaction management

Use `transaction.atomic()` for operations that must commit or roll back together.

Do not keep database transactions open while waiting for slow external network calls.

If a workflow spans PostgreSQL and an external provider, define a durable state machine, idempotency behavior, and reconciliation process.

---

# 30. Cross-App Dependency Rules

Cross-app dependencies must remain explicit.

## 30.1 Preferred dependency direction

```text
Presentation Layer
        |
        v
Application Services
        |
        v
Domain Models and Rules
        |
        v
Persistence
```

Shared platform services such as tenancy, users, auditing, and entitlements may be used by business domains through documented interfaces.

A domain must not import arbitrary private implementation details from another domain.

## 30.2 Examples

Acceptable:

- Sales calls the invoicing service to create an invoice.
- Invoicing calls the approved VAT service to calculate tax.
- Invoicing requests a journal posting through the accounting service.
- Payroll requests an accounting operation through the approved posting interface.
- Reporting uses approved read-only queries.
- Celery tasks call the owning domain's service functions.

Avoid:

- Sales directly editing issued invoice totals.
- Payroll directly inserting accounting ledger rows.
- Reporting changing source records.
- A task duplicating the invoicing issuance workflow.
- An app importing another app's private helper and treating it as a public contract.

## 30.3 Circular dependencies

If two apps require each other's services, stop and review the design.

Possible solutions include:

- Moving a genuinely shared concept to an appropriately owned domain.
- Introducing a narrower interface.
- Reversing the dependency.
- Using a domain event for an asynchronous workflow.
- Reorganizing responsibilities.

Do not create a generic `common` app as a quick fix for every circular dependency.

---

# 31. URL and API Organization

## 31.1 Project-level URLs

The project URL configuration should compose app-owned routes.

Illustrative example:

```python
# config/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("app/", include("apps.core.urls")),
    path("crm/", include("apps.crm.urls")),
    path("sales/", include("apps.sales.urls")),
    path("invoices/", include("apps.invoicing.urls")),
]
```

The exact URL prefixes and route names must be standardized before the relevant implementation phase.

## 31.2 App-level URLs

Each app owns its page routes.

For example:

```python
# apps/invoicing/urls.py

from django.urls import path

from apps.invoicing import views

app_name = "invoicing"

urlpatterns = [
    path("", views.invoice_list, name="list"),
    path("<uuid:invoice_id>/", views.invoice_detail, name="detail"),
]
```

This is an example. The final path converters must match the chosen primary-key strategy.

## 31.3 API routes

Where APIs are required, maintain a clear API route structure.

For example:

```text
/api/v1/crm/
/api/v1/sales/
/api/v1/invoices/
/api/v1/accounting/
/api/v1/integrations/
```

API versioning and error-response standards belong in `API_STANDARDS.md`.

Do not expose internal model fields simply because they exist in the database.

---

# 32. Templates and Static Files

## 32.1 Template organization

Use shared project-level templates for common layouts and reusable interface elements.

Use app-specific templates for domain pages.

Example:

```text
templates/
├── base.html
├── layouts/
│   ├── app_shell.html
│   └── auth_layout.html
├── components/
│   ├── pagination.html
│   ├── form_errors.html
│   ├── status_badge.html
│   └── confirmation_dialog.html
└── errors/
    ├── 403.html
    ├── 404.html
    └── 500.html
```

## 32.2 App templates

Store app templates under an app-specific namespace:

```text
apps/invoicing/templates/invoicing/
apps/crm/templates/crm/
apps/accounting/templates/accounting/
```

This reduces accidental template-name collisions.

## 32.3 Static assets

App-specific static assets should use an app namespace.

Shared design-system assets should live in the approved shared static structure.

Do not duplicate the same CSS or JavaScript across multiple apps when a shared component is appropriate.

## 32.4 Security

Templates must not be treated as an authorization layer.

A page hidden from navigation must still enforce permissions when accessed directly.

Use Django's normal output-escaping behavior and apply safe handling to any intentionally rendered HTML.

---

# 33. Background Tasks

## 33.1 Task location

Place domain-specific tasks in the owning app.

Examples:

```text
apps/billing/tasks.py
apps/e_invoicing/tasks.py
apps/reporting/tasks.py
apps/integrations/tasks.py
```

## 33.2 Task structure

A task should:

1. Receive stable identifiers.
2. Validate its input.
3. Establish the tenant context.
4. Reload relevant records.
5. Check current state.
6. Call the application service.
7. Record the outcome.
8. Apply a bounded retry policy where appropriate.
9. Preserve idempotency.

## 33.3 Retry rules

Do not retry every exception indiscriminately.

Distinguish between transient failures and permanent validation or authorization errors.

For externally visible operations, retries must account for the possibility that the remote system already processed the original request.

## 33.4 Task tests

Test:

- Successful execution.
- Invalid or missing records.
- Wrong-tenant references.
- Duplicate execution.
- Retry behavior.
- Permanent failures.
- Unexpected provider responses.

---

# 34. Signals

Django signals may be used sparingly for simple, decoupled framework-level behavior.

They must not become the default mechanism for important business workflows.

## 34.1 Appropriate uses

Potential uses include:

- Registering framework handlers.
- Simple ancillary behavior where execution order is not business-critical.
- Certain lifecycle integrations that are explicitly documented.

## 34.2 Avoid

Do not use signals as the hidden mechanism for:

- Issuing invoices.
- Posting journals.
- Finalizing payroll.
- Updating inventory balances.
- Charging subscriptions.
- Performing external provider submissions.

These workflows should use explicit services with visible transaction boundaries and tests.

If a durable follow-up action must occur after a transaction commits, design the behavior explicitly. A simple `transaction.on_commit()` callback can prevent execution before commit, but it does not guarantee durable delivery if the process crashes after commit. Use a transactional outbox when durable event publication is required.

---

# 35. Exception Handling

Define a small, consistent application exception hierarchy.

Illustrative structure:

```text
ApplicationError
├── ValidationError
├── PermissionDeniedError
├── ResourceNotFoundError
├── InvalidStateTransitionError
├── ConflictError
├── DependencyUnavailableError
└── IntegrationError
```

These are proposed application-level categories. Django and Django REST Framework already provide exceptions for many HTTP concerns; do not duplicate their behavior unnecessarily.

## 35.1 Rules

- Use exceptions that communicate meaningful failure categories.
- Do not catch and silently ignore exceptions.
- Do not expose internal tracebacks to users.
- Preserve diagnostic context in protected logs.
- Translate expected application errors into consistent responses.
- Roll back transactions when an operation cannot safely complete.
- Distinguish between a failed operation and an operation with an uncertain external outcome.

---

# 36. Database Migrations

## 36.1 Migration ownership

Each Django app owns its migrations.

```text
apps/invoicing/migrations/
apps/accounting/migrations/
apps/inventory/migrations/
```

## 36.2 Migration rules

- Commit migrations with the corresponding code.
- Review generated migration operations.
- Avoid unrelated schema changes in one migration.
- Test migrations on a clean database.
- Test important upgrade paths where prior versions may exist.
- Assess destructive changes.
- Preserve financial and audit history.
- Avoid modifying already-applied migration files.
- Document data migrations and rollback limitations.

## 36.3 Cross-app migration dependencies

Django migration dependencies between apps are permitted where required.

However, excessive circular migration dependencies often indicate a problem with model ownership or app boundaries.

Review the design before introducing complex dependency cycles.

---

# 37. Testing Structure

Use app-level tests for domain behavior and project-level tests for cross-domain behavior.

## 37.1 App-level tests

Example:

```text
apps/invoicing/tests/
├── __init__.py
├── factories.py
├── test_models.py
├── test_services.py
├── test_selectors.py
├── test_permissions.py
├── test_views.py
├── test_api.py
└── test_tasks.py
```

The app may instead use fewer test files if its scope is small.

## 37.2 Project-level tests

```text
tests/
├── architecture/
├── integration/
├── security/
└── end_to_end/
```

Use project-level tests for behavior spanning multiple apps.

Examples include:

- Quotation-to-invoice conversion.
- Invoice-to-accounting posting.
- Purchase receipt-to-inventory movement.
- Payroll-to-accounting integration.
- Subscription change-to-entitlement enforcement.
- E-invoicing submission and reconciliation.

## 37.3 Tenant-isolation testing

Tests must cover attempts to access another tenant's data through:

- Views.
- APIs.
- Service functions.
- Selectors.
- Background tasks.
- File downloads.
- Exports.
- Administrative operations.

Tenant isolation must not be considered adequately tested solely because one protected view rejects an unauthorized request.

---

# 38. Django Admin

Django Admin is an internal administrative interface, not a substitute for the product's customer-facing application.

## 38.1 Appropriate uses

- Controlled internal configuration.
- Authorized operational inspection.
- Selected support workflows.
- Reference data management.
- Development and test administration.

## 38.2 Restrictions

- Tenant-owned data must not be globally exposed to unauthorized administrators.
- Admin querysets and actions must enforce the intended access model.
- Destructive bulk actions require careful review.
- Sensitive payroll and financial information must have appropriate restrictions.
- Important business transitions must use the same domain services as the main application.
- Production admin access must be restricted and monitored.

Do not assume Django Admin automatically provides the correct multi-tenant authorization model.

---

# 39. Management Commands

Management commands may be used for approved operational tasks such as:

- Initial reference-data loading.
- Controlled tenant provisioning.
- Data reconciliation.
- Maintenance operations.
- Administrative reports.
- Carefully designed data migrations or repair procedures.

Commands that modify production data must validate their target scope and must not bypass critical business invariants.

Destructive commands should require explicit confirmation or an approved noninteractive authorization mechanism.

Commands must not embed production credentials.

---

# 40. Configuration and Environment Variables

Application configuration belongs in the settings and deployment configuration layers.

## 40.1 Rules

- Keep secrets outside source control.
- Validate required production settings during startup or deployment.
- Use separate settings for development, test, and production.
- Avoid silently defaulting missing production secrets to insecure values.
- Document every required environment variable.
- Do not read environment variables throughout business logic when a settings interface is appropriate.

## 40.2 Configuration ownership

Django settings define application-level configuration.

Tenant-specific business settings belong to the tenant or owning domain.

Subscription and module configuration belongs to the subscription platform.

Provider-specific configuration belongs to the appropriate integration domain.

Do not confuse environment configuration with tenant-level business configuration.

---

# 41. File and Document Storage

If the platform supports uploaded documents, use an explicit storage abstraction.

Potential storage targets include local storage for development and an approved private object-storage service for production.

## 41.1 Rules

- Store file metadata in the owning domain.
- Keep sensitive files private by default.
- Validate access before issuing downloads.
- Avoid relying on unpredictable filenames as an access-control mechanism.
- Define retention and deletion behavior.
- Apply upload size and type restrictions.
- Keep storage credentials outside source control.
- Document backup and recovery responsibilities.
- Do not store large file contents directly in PostgreSQL unless an approved requirement justifies it.

The actual storage provider and production configuration must be selected during deployment planning.

---

# 42. Module Activation and Application Registration

Not every planned module needs to be active in the first release.

## 42.1 Django registration

An implemented app may be registered in Django even if its commercial functionality is not yet sellable.

These are different states:

- Installed in the codebase.
- Registered in Django.
- Enabled for internal testing.
- Available for pilot use.
- Approved for commercial sale.
- Entitled for a particular tenant.

## 42.2 Safe rollout

A module must not become accessible merely because its Django app is installed.

Its protected views, APIs, services, tasks, and relevant data-access paths must enforce the required authorization and entitlement rules.

Do not depend exclusively on removing a navigation link or omitting a URL from the user interface.

## 42.3 Schema implications

Database migrations for implemented modules may create tables even if a module is not commercially available.

If a future requirement calls for strict separation of data storage or schema by module, that requirement needs a separate architecture decision. Commercial module entitlement alone does not imply separate physical storage.

---

# 43. Code Review Checklist

Every substantial code review should evaluate the following.

## Structure

- [ ] The change belongs to the correct owning app.
- [ ] Cross-app dependencies are explicit.
- [ ] No circular dependency has been introduced.
- [ ] Business logic is placed in an appropriate layer.
- [ ] Public service interfaces are documented.

## Security

- [ ] Authentication and authorization are enforced.
- [ ] Tenant ownership is validated.
- [ ] Entitlement checks are applied where required.
- [ ] Sensitive information is protected.
- [ ] External input is validated.
- [ ] Logs do not expose secrets or unnecessary sensitive data.

## Data integrity

- [ ] Database constraints are appropriate.
- [ ] Transactions are used where required.
- [ ] Financial calculations use decimal arithmetic.
- [ ] State transitions are validated.
- [ ] Idempotency and concurrency are addressed.
- [ ] Migrations have been reviewed.

## Quality

- [ ] Tests cover changed behavior.
- [ ] Relevant regression tests pass.
- [ ] Documentation is updated.
- [ ] No unrelated refactoring was introduced without justification.
- [ ] Known limitations are documented.
- [ ] The implementation follows the approved phase scope.

---

# 44. Rules for OpenAI Codex

Codex must follow these implementation rules.

1. Read `AGENTS.md` before making changes.
2. Read this document and the relevant domain specifications.
3. Create only the apps required for the approved phase.
4. Do not create all planned business models in one giant initial implementation.
5. Do not generate empty placeholder apps merely to make the repository match the final structure.
6. Keep each app responsible for its own business records.
7. Use explicit service interfaces for significant business operations.
8. Keep views thin.
9. Keep financial calculations out of templates and client-side JavaScript.
10. Do not bypass tenant scoping.
11. Do not bypass centralized entitlement evaluation.
12. Do not use Django signals as hidden business workflow engines.
13. Do not call external providers inside long-running database transactions.
14. Do not introduce new dependencies without justification.
15. Add migrations and tests alongside implementation changes.
16. Report test results accurately.
17. Update architecture and module documentation when contracts change.
18. Request approval when model ownership or dependency boundaries are unclear.
19. Never silently alter an approved financial, legal, or regulatory rule.
20. Never claim production readiness based only on successful code generation.

---

# 45. Initial Implementation Scope

The first implementation phase must remain deliberately small.

## Phase P0

Establish:

- Project and repository conventions.
- Approved settings structure.
- Dependency management.
- Testing configuration.
- CI configuration.
- Architecture documentation.
- Initial health-check and application-startup conventions.
- Development environment instructions.

Do not implement the full ERP.

## Phase P1

Implement the approved foundation:

- `core`
- `tenants`
- `users`
- `audit`

The exact initial scope of `audit` must be agreed with the phase specification. If the full audit subsystem is not needed immediately, implement only the approved audit foundation.

Validate:

- Database migrations.
- Authentication.
- Tenant membership.
- Tenant context.
- Tenant isolation.
- Server-side permissions.
- Basic audit events.
- CI and automated tests.

## Phase P2

Introduce:

- `subscriptions`
- `billing`

Implement the module registry and entitlement interfaces before enabling commercial business modules.

## Subsequent phases

Add business apps according to the approved roadmap and dependencies.

Do not implement future modules ahead of schedule merely because their names already appear in the target repository structure.

---

# 46. Final Architectural Rule

The authoritative implementation pattern is:

**Domain-owned Django apps → explicit application services → tenant-aware data access → validated business state transitions → database constraints and transactions → automated tests.**

Presentation code, APIs, and background tasks must call the same approved business services instead of implementing competing versions of the same workflow.

When model ownership, service boundaries, or tenant isolation requirements are unclear, Codex must document the uncertainty and request a decision before implementing a potentially incompatible design.

The objective is a modular Django codebase that can support a growing ERP product without sacrificing security, financial integrity, or maintainability.
