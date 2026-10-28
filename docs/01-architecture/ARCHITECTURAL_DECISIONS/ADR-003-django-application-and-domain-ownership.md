# ADR-003: Django Application and Domain Ownership

| Field | Details |
|---|---|
| ADR ID | ADR-003 |
| Title | Django Application and Domain Ownership |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / Technical Lead |
| Reviewers | Architecture, Security, Development, Data, Product |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-001, ADR-002, ADR-004, ADR-005, ADR-006 |
| Related Requirements | PRD-001–PRD-003, TEN-001–TEN-005, IAM-002–IAM-004, SUB-001–SUB-005, BILL-001 |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DJANGO_APP_STRUCTURE.md`, `DATABASE_DESIGN.md`, `MULTI_TENANCY.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `MODULE_DEPENDENCIES.md`, `ENTITLEMENT_ENGINE.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The platform is designed as a modular Django monolith containing platform capabilities and ERP business domains. The current documents describe many of the same concepts, but some assign ownership differently. The most immediate conflict is tenant membership: some documents assign it to `users`, while the tenancy and authorization documents use `tenants.TenantMembership`.

Unclear ownership creates material risks:

- Competing authoritative models for the same concept.
- Circular imports and migrations.
- Business rules duplicated in views, tasks, serializers, and signals.
- Cross-domain writes that bypass invariants.
- Entitlement or authorization logic implemented differently by each module.
- Schema changes that are difficult to migrate or extract later.

This ADR defines the ownership rule and the initial domain map. It does not require every listed Django app to be created before its approved phase.

## 2. Decision Drivers

- One authoritative owner for each business concept and state transition.
- Explicit dependency direction and no circular application dependencies.
- Tenant isolation and authorization at every boundary.
- Transactional integrity for financial and inventory operations.
- Independent testability without network boundaries inside the monolith.
- Incremental implementation aligned with approved phases.
- Clear future extraction seams without premature microservices.

## 3. Options Considered

### Option A: Domain-owned Django apps with explicit service contracts

Each domain owns its models, migrations, write rules, and public application services. Other apps may hold references where approved but may not modify protected state directly.

**Advantages:** clear accountability, testable boundaries, local transactions, controlled dependencies, and practical Django implementation.

**Disadvantages:** requires dependency discipline, interface review, and occasional coordination for cross-domain transactions.

### Option B: Technical-layer applications

Organize models, services, APIs, and tasks into separate technical apps.

**Advantages:** superficially uniform layers.

**Disadvantages:** business concepts span many apps, ownership is obscured, and changes create broad coupling.

### Option C: Shared models and unrestricted cross-app access

Allow apps to import and write any model directly.

**Advantages:** low initial ceremony.

**Disadvantages:** hidden coupling, duplicated rules, unsafe writes, difficult testing, and poor modularity.

### Option D: Independently deployed service per domain

**Advantages:** process and deployment isolation.

**Disadvantages:** distributed consistency, operational, security, and observability costs are not justified for the initial product.

## 4. Decision

Adopt domain-owned Django applications within the modular monolith.

Every authoritative model, business invariant, and state-changing operation must have exactly one owning application. Cross-domain behavior must use an explicit public service, selector, query contract, or durable event appropriate to the consistency requirement.

An app boundary is a code and ownership boundary, not a network boundary. Django applications remain part of one deployable system under ADR-001.

### 4.1 Initial ownership map

| App | Authoritative ownership |
|---|---|
| `core` | Small technical primitives, shared exceptions, health checks, and genuinely generic utilities |
| `tenants` | Tenant, tenant settings, tenant lifecycle, `TenantMembership`, legal entity, branch, and organizational ownership relationships |
| `users` | User identity, credentials, authentication lifecycle, roles, permissions, role-permission mappings, and membership-role assignments |
| `audit` | Audit-event records and protected audit retrieval |
| `subscriptions` | Module definitions, dependency policy, subscriptions, subscription module selections, and effective entitlement records |
| `billing` | SaaS subscription charges, billing documents, provider payment records, and SaaS payment reconciliation |
| `crm` | Leads, CRM activities, and the approved customer/contact master scope |
| `sales` | Quotations, sales orders, and sales workflow state |
| `invoicing` | ERP customer invoices, credit notes, numbering, issuance, and document lifecycle |
| `e_invoicing` | Provider adapters, submission operations, acknowledgements, and reconciliation |
| `accounting` | Chart of accounts, journals, ledger entries, fiscal periods, and posting controls |
| `vat` | VAT configuration, effective-dated tax rules, calculation policy, and VAT reporting artifacts |
| `procurement` | Supplier purchasing workflow and purchase orders |
| `inventory` | Products where assigned by the module specification, warehouses, stock movements, balances, and valuation |
| `hrms` | Employee master and HR records |
| `payroll` | Payroll rules, runs, results, and payslips |
| `projects` | Projects, tasks, milestones, and project allocation |
| `expenses` | Expense claims, approval state, and reimbursement requests |
| `fixed_assets` | Asset register, lifecycle, and depreciation records |
| `banking` | Bank accounts, imported transactions, matching, and reconciliation records |
| `reporting` | Report definitions and execution metadata; it does not own copied business truth |
| `integrations` | Shared integration configuration and generic delivery infrastructure that does not belong to a provider-specific domain |

The owner of products, shared parties/contacts, generic attachments, notifications, and payment allocation must be finalized in the applicable module or later ADR before those models are created.

### 4.2 Tenant membership correction

`TenantMembership` belongs to `tenants` because it represents the relationship between an identity and an organization and is part of tenant access establishment. `users` owns identities and authorization definitions. `users.MembershipRoleAssignment` may reference `tenants.TenantMembership` through an explicit contract.

This choice prevents the identity app from owning tenant lifecycle while keeping authentication and role semantics in the identity domain.

### 4.3 Public interfaces

An owning app must expose only the interfaces needed by consumers. Accepted interface forms are:

- Application services for commands and state changes.
- Selectors or query services for intentional read access.
- Permission and policy functions for domain decisions.
- Stable value objects or data-transfer structures where model exposure would create coupling.
- Durable events for asynchronous follow-up when immediate atomic consistency is not required.

Direct model reads may be permitted for simple, documented relationships. Direct cross-domain writes to protected state are prohibited.

### 4.4 Dependency direction

Platform apps may be depended on by business apps through their public interfaces. Business apps must not introduce reverse dependencies into platform apps.

Cross-business-domain dependencies must be explicit and reviewed. Shared behavior does not automatically belong in `core`; it should remain in the domain that owns the rule unless it is genuinely domain-neutral.

Imports, migration dependencies, task calls, template tags, and signal registrations all count as dependencies and must not form cycles.

### 4.5 Cross-domain transactions

One application service must coordinate a synchronous operation that requires atomic updates across domains. Participating domains retain their invariants through callable services or validated operations.

When an external system or asynchronous boundary is involved, commit authoritative local state first and use the approved durable operation/outbox pattern. Do not hold a database transaction open across network calls.

### 4.6 Signals

Django signals may support low-risk technical hooks. They must not conceal critical financial posting, entitlement activation, tenant provisioning, inventory movement, or external-provider workflows.

## 5. Rationale

Domain ownership provides enforceable modularity without the cost of distributed services. Assigning tenant membership to `tenants` aligns the organizational relationship with tenant lifecycle and allows the identity domain to remain focused on users and authorization primitives.

Explicit service contracts make security checks, transaction boundaries, and tests visible. They also provide seams that can support future extraction if operational evidence justifies it.

## 6. Consequences

### Positive consequences

- One authoritative model and workflow owner.
- Clearer migrations, reviews, and test ownership.
- Reduced circular dependencies and duplicated rules.
- Consistent entry points for views, APIs, tasks, and integrations.
- Safer future service extraction.

### Negative consequences and trade-offs

- Public interfaces require design and maintenance.
- Cross-domain changes require coordination.
- Some Django foreign keys will cross app boundaries.
- Strict ownership may feel slower than direct model writes for small changes.

### Risks and mitigations

- **God services:** split services by business operation and keep domain rules cohesive.
- **Overgrown `core`:** require a domain-neutral justification for every shared abstraction.
- **Anemic models or services:** place invariants where they are most enforceable; do not impose one style universally.
- **Hidden cycles:** add architecture tests for imports and declared module dependencies.

## 7. Security and Tenant Isolation

- Every public service must receive or establish trusted actor and tenant context where applicable.
- Model ownership does not grant access; authorization and entitlements remain separate controls.
- Cross-domain selectors must preserve tenant and legal-entity scope.
- Platform-wide operations require explicit privileged services and audit evidence.
- Sensitive HR, payroll, banking, tax, and audit interfaces must expose only necessary fields.

## 8. Data Integrity and Migration

- The owning app owns migrations for its tables and constraints.
- Cross-app foreign-key changes require review by both owners.
- Cross-tenant references must be prevented according to ADR-002 and ADR-004.
- Ownership changes after data exists require a migration and compatibility plan; moving a model between apps is not a routine refactor.
- Posted financial data must not be duplicated into another domain as a competing source of truth.

## 9. Operational Impact

The monolith remains one release unit. Ownership must nevertheless appear in logging, metrics, runbooks, support procedures, and incident escalation. A domain owner must be identifiable when a migration, task, or integration fails.

## 10. Implementation Requirements

1. Reconcile `MODULE_CATALOGUE.md` and `DJANGO_APP_STRUCTURE.md` so tenant membership ownership is consistent after approval.
2. Maintain an authoritative model-ownership inventory as module specifications are created.
3. Document each app's public services and prohibited dependencies.
4. Add architecture tests for dependency cycles and prohibited imports where practical.
5. Require services for protected state changes.
6. Record unresolved shared-entity ownership before model creation.
7. Keep SaaS billing separate from ERP customer invoicing.

## 11. Validation and Acceptance Criteria

- [ ] Every implemented model has one documented owning app.
- [ ] `TenantMembership` has one model and one owner.
- [ ] No circular Django app dependency exists.
- [ ] Protected cross-domain writes use reviewed services.
- [ ] Views, APIs, and tasks reuse the same business operations.
- [ ] Tenant and actor context are explicit at service boundaries.
- [ ] Cross-app migrations and foreign keys have integrity tests.
- [ ] Shared concepts do not have competing authoritative models.
- [ ] Architecture tests enforce selected dependency rules.
- [ ] Module specifications link back to this ADR.

## 12. Alternatives Rejected

- Technical-layer applications are rejected because they fragment business ownership.
- Unrestricted cross-app access is rejected because it defeats the modular-monolith boundary.
- Immediate service-per-domain decomposition is rejected under ADR-001.
- Assigning tenant membership to `users` is not recommended because membership is an organizational relationship governed by tenant lifecycle.

## 13. References

- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/00-product/MODULE_CATALOGUE.md`
- `docs/01-architecture/DJANGO_APP_STRUCTURE.md`
- `docs/01-architecture/MODULE_DEPENDENCIES.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/07-project-management/DECISIONS_PENDING.md`
- Django applications: https://docs.djangoproject.com/en/stable/ref/applications/

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Domain-owned Django apps with explicit service contracts and `tenants.TenantMembership`.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; source documents must be reconciled to `tenants.TenantMembership` before model implementation.

This accepted decision governs P01 domain ownership. P01 implementation remains unauthorized until the phase gate is approved.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial domain ownership and service-boundary decision accepted after standards review. |
