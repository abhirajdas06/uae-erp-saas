# Pending Decisions Register — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | PM-DEC-001 |
| Version | 1.0 |
| Status | Active |
| Last Updated | 27 October 2026 |
| Decision Authority | Product Owner and designated reviewers |

## 1. Purpose and Authority

This is the canonical register for unresolved project decisions and human approvals. Domain documents may contain detailed candidate-decision lists, but the current owner, priority, blocking effect, recommendation, and disposition must be recorded here.

An entry marked `RECOMMENDED` or linked to a `PROPOSED` ADR is not approved. Approval requires an explicit human decision, date, and approver.

## 2. Status Vocabulary

- `OPEN`: Analysis or recommendation is incomplete.
- `RECOMMENDED`: A proposed option is documented and awaits review.
- `AWAITING_APPROVAL`: Review material is complete enough for an authorized decision.
- `APPROVED`: Explicit human approval is recorded.
- `REJECTED`: Explicitly declined.
- `DEFERRED`: Intentionally postponed with a stated trigger.
- `SUPERSEDED`: Replaced by another decision entry.

## 3. Foundational Decisions

| ID | Decision | Recommendation | Status | Owner | Blocks | Authoritative record |
|---|---|---|---|---|---|---|
| DEC-ARCH-001 | Initial architecture style | Use a disciplined Django modular monolith; do not introduce microservices without a later evidence-based ADR | AWAITING_APPROVAL | Product Owner / Architecture | P01 implementation | ADR-001 |
| DEC-DATA-001 | Initial database tenancy topology | Use one PostgreSQL database and shared schema with explicit tenant ownership and layered isolation | AWAITING_APPROVAL | Product Owner / Architecture / Security | P01 data model | ADR-002 |
| DEC-ARCH-002 | Django domain and model ownership | Assign each authoritative model and write operation to one Django app; use explicit service contracts across boundaries | RECOMMENDED | Architecture | P01 model creation | ADR-003 planned |
| DEC-SEC-001 | Tenant isolation and RLS | Require application-level isolation for all paths and phased PostgreSQL RLS defense-in-depth for approved tenant-owned tables | RECOMMENDED | Architecture / Security / Database | P01 tenant data access | ADR-004 planned |
| DEC-IAM-001 | Authentication and authorization model | Use a custom Django user model, tenant memberships, tenant-scoped RBAC, object checks, and separately controlled platform access | RECOMMENDED | Architecture / Security | P01 identity and permissions | ADR-005 planned |
| DEC-ENT-001 | Module entitlement enforcement | Centralize effective-entitlement evaluation and dependency validation; keep it independent from user authorization | RECOMMENDED | Product / Architecture / Security | P02 and commercial modules | ADR-006 planned |

## 4. Audit Reconciliation Decisions

| ID | Decision | Recommendation | Status | Owner | Blocks | Notes |
|---|---|---|---|---|---|---|
| DEC-GOV-001 | Canonical ADR numbering | Use the ADR-001 through ADR-020 sequence in the ADR register | RECOMMENDED | Architecture | New ADR creation | Register and `SYSTEM_ARCHITECTURE.md` have been reconciled; approval is needed only if the roadmap itself changes |
| DEC-GOV-002 | Canonical phase identifiers | Standardize on zero-padded P00–P12 identifiers and define machine-readable IDs separately | RECOMMENDED | Product / Project Governance | Phase manifests and folders | Existing documents mix P00/P01 with P0/P1 and P0-FOUNDATION |
| DEC-GOV-003 | Requirement and test identifier namespaces | Preserve IAM-001–IAM-005 for product requirements and rename architecture test scenarios to IAM-TST-NNN | RECOMMENDED | Architecture / QA | Traceability matrix | Current identifiers have different meanings in two documents |
| DEC-SEC-002 | Canonical PostgreSQL tenant-context key | Use `app.current_tenant_id` consistently | RECOMMENDED | Security / Database | RLS policy implementation | `MULTI_TENANCY.md` currently uses `app.tenant_id` |
| DEC-ARCH-003 | Tenant-membership model owner | Assign `TenantMembership` to `tenants`; keep user identity, roles, permissions, and role assignments in `users` | RECOMMENDED | Architecture / Security | ADR-003 and P01 models | Existing documents alternate between `users` and `tenants` ownership |
| DEC-GOV-004 | Git repository governance | Initialize or attach the intended Git repository before implementation work | OPEN | Product Owner / Repository Maintainer | Diff-based review and implementation governance | Current directory has no discoverable Git metadata |

## 5. High-Priority Product and Operational Decisions

| ID | Decision | Status | Owner | Required before |
|---|---|---|---|---|
| DEC-PROD-001 | Initial launch segment and module scope | OPEN | Product Owner | Commercial pilot planning |
| DEC-COM-001 | Pricing, trials, grace periods, and subscription-change policy | OPEN | Product / Commercial / Finance | P02 acceptance |
| DEC-INT-001 | SaaS payment provider | OPEN | Product / Finance / Security | Payment integration implementation |
| DEC-REG-001 | Current UAE e-invoicing applicability and provider selection | OPEN | Product / Compliance / Architecture | P04 implementation |
| DEC-FIN-001 | Monetary precision, currency, and rounding policy | OPEN | Finance / Product / Architecture | Financial model implementation |
| DEC-OPS-001 | Hosting region and data-residency requirements | OPEN | Product / Legal / Security / DevOps | Production infrastructure selection |
| DEC-OPS-002 | Availability, backup RPO, and recovery RTO | OPEN | Product / DevOps | Production architecture approval |
| DEC-DATA-002 | Retention, deletion, legal hold, and tenant-level recovery policy | OPEN | Legal / Compliance / Security | Production handling of customer data |

## 6. Decision Recording Requirements

Every resolved entry must record:

- Selected option and scope.
- Approver and approval date.
- Related ADR or product record.
- Documents requiring reconciliation.
- Implementation and test implications.
- Any deferred follow-up decision.

Detailed decision inventories currently embedded in product and architecture documents will be mapped into this register incrementally as their owning documentation unit is reviewed. Their presence does not constitute approval.

## 7. Decision Log

| Date | Decision ID | Outcome | Approved by | Notes |
|---|---|---|---|---|
| — | — | No human approvals recorded | — | — |
