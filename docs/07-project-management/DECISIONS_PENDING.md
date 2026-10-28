# Pending Decisions Register — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | PM-DEC-001 |
| Version | 1.0 |
| Status | Active |
| Last Updated | 28 October 2026 |
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
- `RESOLVED`: A non-semantic governance inconsistency was corrected without making a product or architecture decision.

## 3. Foundational Decisions

| ID | Decision | Recommendation | Status | Owner | Blocks | Authoritative record |
|---|---|---|---|---|---|---|
| DEC-ARCH-001 | Initial architecture style | Use a disciplined Django modular monolith; do not introduce microservices without a later evidence-based ADR | APPROVED | Product Owner / Architecture | — | ADR-001 |
| DEC-DATA-001 | Initial database tenancy topology | Use one PostgreSQL database and shared schema with explicit tenant ownership and layered isolation | APPROVED | Product Owner / Architecture / Security | — | ADR-002 |
| DEC-ARCH-002 | Django domain and model ownership | Assign each authoritative model and write operation to one Django app; use explicit service contracts across boundaries | APPROVED | Architecture | — | ADR-003 |
| DEC-SEC-001 | Tenant isolation and RLS | Require application-level isolation for all paths and phased PostgreSQL RLS defense-in-depth for approved tenant-owned tables | APPROVED | Architecture / Security / Database | — | ADR-004 |
| DEC-IAM-001 | Authentication and authorization model | Use a custom Django user model, tenant memberships, tenant-scoped RBAC, object checks, and separately controlled platform access | APPROVED | Architecture / Security | — | ADR-005 |
| DEC-ENT-001 | Module entitlement enforcement | Centralize effective-entitlement evaluation and dependency validation; keep it independent from user authorization | APPROVED | Product / Architecture / Security | — | ADR-006 |
| DEC-UI-001 | Primary web-interface architecture | Use Django Templates, HTMX, and Tailwind CSS; require a new ADR before adopting a material SPA surface | APPROVED | Product / Architecture / UX | — | ADR-007 |
| DEC-API-001 | Application API strategy | Use Django REST Framework selectively for approved machine consumers; do not make ordinary internal Django calls over HTTP | APPROVED | Product / Architecture / Security | — | ADR-008 |
| DEC-TASK-001 | Background task execution | Use Celery with Redis as broker while PostgreSQL remains authoritative for operation state and idempotency | APPROVED | Architecture / DevOps / Security | — | ADR-009 |
| DEC-EVT-001 | Reliable event and follow-up delivery | Use a PostgreSQL transactional outbox for material post-commit work, with at-least-once publication and idempotent consumers | APPROVED | Architecture / Database / Operations | — | ADR-010 |
| DEC-FIN-002 | Financial posting and correction integrity | Use controlled posting, freeze protected financial fields, and correct through linked reversals, credit notes, adjustments, or cancellations | APPROVED | Finance / Architecture / Product | — | ADR-011 |
| DEC-EIN-001 | UAE e-invoicing integration boundary | Use a dedicated `e_invoicing` domain with versioned provider adapters, durable operations, immutable snapshots, and reconciliation | APPROVED | Product / Architecture / UAE Tax and Compliance / Security | — | ADR-012 |
| DEC-FIN-003 | Monetary representation and calculation policy | Require decimal arithmetic, explicit currencies, typed numeric classes, and named versioned rounding stages | APPROVED | Finance / UAE Tax / Architecture | — | ADR-013 |
| DEC-DATA-003 | Primary-key and tenant-reference strategy | Use UUIDv4 for foundational and major entities, reviewed bigint exceptions, and database-enforced same-tenant references | APPROVED | Architecture / Database / Security | — | ADR-014 |
| DEC-QA-001 | Automated testing and CI gates | Use layered risk-based gates, PostgreSQL-backed critical tests, and GitHub Actions as the initial CI service | APPROVED | QA / Architecture / Security / DevOps | — | ADR-015 |
| DEC-QA-002 | Security requirements baseline | Use `docs/05-quality/SECURITY_REQUIREMENTS.md` as the risk-based security baseline | APPROVED | Security / Product / Architecture / Privacy | — | QUAL-SEC-001; legal interpretation and residual-risk acceptance excluded |
| DEC-QA-003 | Testing strategy baseline | Use `docs/05-quality/TESTING_STRATEGY.md` as the layered verification baseline | APPROVED | QA / Security / DevOps / Product | — | QUAL-TST-001; execution evidence remains required |
| DEC-PHASE-001 | Bounded P00 phase specification | Approve `P00_PHASE_SPECIFICATION.md` as the documentation/governance boundary without approving P00 exit | APPROVED | Product Owner / Architecture / Security / QA / DevOps | P00 exit still requires evidence | P00-SPEC-001 |
| DEC-GOV-005 | P00 traceability and evidence model | Use `P00_TRACEABILITY_MATRIX.md` as the P00 verification contract | APPROVED | QA / Project Governance / Architecture | P00 evidence execution | P00-TRACE-001 |
| DEC-PHASE-002 | Bounded P01 Core Platform and Multi-Tenancy specification | Approve the specification boundary; require P00 exit and separate authorization before implementation | APPROVED | Product Owner / Architecture / Security / QA / Database / DevOps | P01 implementation authorization | P01-SPEC-001 |
| DEC-QA-004 | P01 tenant-isolation verification contract | Use all mandatory and applicable conditional rules before P01 implementation/exit | APPROVED | Security / QA / Architecture / Database | Test execution remains `NOT_RUN` | P01-TEN-TEST-001 |
| DEC-GOV-006 | Phase/task manifest schema | Use canonical P00–P12 IDs, guarded statuses, explicit authorization, evidence, permission, and exception contracts | APPROVED | Project Governance / Architecture / QA / DevOps | Validator implementation/evidence | P00-MANIFEST-001 |
| DEC-QA-005 | Initial CI quality-gate specification | Use reproducible commands, read-only defaults, evidence-bound gates, and expiring/non-weakening exceptions | APPROVED | QA / Security / DevOps / Architecture | Workflow implementation/evidence | QUAL-CI-001 |
| DEC-DEP-001 | Container deployment architecture | Use one immutable Docker application image with explicit web, worker, scheduler, and migration roles; defer production topology selection | APPROVED | Architecture / DevOps / Security | — | ADR-016 |
| DEC-SEC-003 | Secrets and environment configuration | Use typed environment configuration plus a narrow approved production secrets backend; prohibit production secrets in source, images, and ordinary tables | APPROVED | Security / DevOps / Architecture | — | ADR-017 |
| DEC-AUD-001 | Audit, logging, and sensitive-data boundary | Separate append-oriented audit events, structured application logs, and operational/security telemetry with shared correlation and minimization | APPROVED | Security / Compliance / Architecture / Operations | — | ADR-018 |
| DEC-FILE-001 | File and document storage architecture | Use private production object storage with authoritative PostgreSQL metadata, staged safe uploads, authorization-checked delivery, versioned evidence, and governed lifecycle/recovery | APPROVED | Architecture / Security / Privacy / Operations | — | ADR-019 |
| DEC-API-002 | API versioning and external contract evolution | Use `/api/v{major}/` for approved REST APIs, version-controlled OpenAPI contracts, independently versioned provider/webhook/event/file schemas, and compatibility/deprecation gates | APPROVED | Product / Architecture / Security / Integration / QA | — | ADR-020 |

## 4. Audit Reconciliation Decisions

| ID | Decision | Recommendation | Status | Owner | Blocks | Notes |
|---|---|---|---|---|---|---|
| DEC-GOV-001 | Canonical ADR numbering | Use the ADR-001 through ADR-020 sequence in the ADR register | APPROVED | Architecture | — | Register and `SYSTEM_ARCHITECTURE.md` are reconciled |
| DEC-GOV-002 | Canonical phase identifiers | Use zero-padded P00–P12 as primary IDs; retain P0/P0-FOUNDATION only as legacy aliases | APPROVED | Product / Project Governance | — | Defined by P00-MANIFEST-001 |
| DEC-GOV-003 | Requirement and test identifier namespaces | Preserve IAM-001–IAM-005 for product requirements and use IAM-TST-NNN for authentication test scenarios | RESOLVED | Architecture / QA | Traceability matrix | Non-semantic governance correction applied; no product or architecture decision changed |
| DEC-SEC-002 | Canonical PostgreSQL tenant-context key | Use `app.current_tenant_id` consistently | APPROVED | Security / Database | — | Accepted by ADR-004; `MULTI_TENANCY.md` examples reconciled on 28 October 2026 |
| DEC-ARCH-003 | Tenant-membership model owner | Assign `TenantMembership` to `tenants`; keep user identity, roles, permissions, and role assignments in `users` | APPROVED | Architecture / Security | — | Accepted by ADR-003; `DJANGO_APP_STRUCTURE.md` reconciled on 28 October 2026 |
| DEC-GOV-004 | Git repository governance | Use the Git repository rooted at `D:/Project/uae-erp-saas` for diff-based review and implementation governance | RESOLVED | Product Owner / Repository Maintainer | — | Repository metadata and working-tree status were verified on 28 October 2026 |

## 5. High-Priority Product and Operational Decisions

| ID | Decision | Status | Owner | Required before |
|---|---|---|---|---|
| DEC-PROD-001 | Initial launch segment and module scope | OPEN | Product Owner | Commercial pilot planning |
| DEC-COM-001 | Pricing, trials, grace periods, and subscription-change policy | OPEN | Product / Commercial / Finance | P02 acceptance |
| DEC-INT-001 | SaaS payment provider | OPEN | Product / Finance / Security | Payment integration implementation |
| DEC-REG-001 | Current UAE e-invoicing applicability, effective requirements, and provider selection | OPEN | Product / Compliance / Architecture / Legal | P04 implementation and production release |
| DEC-FIN-001 | Concrete precision/scale matrix, VAT rounding, exchange-rate source, and residual-allocation policies | OPEN | Finance / UAE Tax / Product / Architecture | Financial model migrations and calculation acceptance |
| DEC-OPS-001 | Hosting region and data-residency requirements | OPEN | Product / Legal / Security / DevOps | Production infrastructure selection |
| DEC-OPS-002 | Availability, backup RPO, and recovery RTO | OPEN | Product / DevOps | Production architecture approval |
| DEC-DATA-002 | Retention, deletion, legal hold, and tenant-level recovery policy | OPEN | Legal / Compliance / Security | Production handling of customer data |
| DEC-OPS-003 | Production object-storage provider, region, scanning, encryption, quota, and lifecycle configuration | OPEN | Product / Security / Privacy / DevOps | Production file storage and customer document handling |
| DEC-API-003 | External API consumers, support/deprecation duration, and contractual exposure | OPEN | Product / Commercial / Architecture / Operations | Public or partner API commitment |

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
| 28 October 2026 | DOC-BASELINE-001 | Approved the repository documentation in scoped baseline/specification classes | Product Owner — explicit market-standard review instruction | See `DOCUMENT_STANDARDS_REVIEW.md`; no compliance certification or implementation authorization implied |
| 27 October 2026 | DEC-GOV-003 | Reserved IAM-NNN for product requirements and IAM-TST-NNN for architecture test scenarios | Documentation governance rule | Corrected an identifier collision without changing required behavior |
| 28 October 2026 | DEC-GOV-004 | Verified the existing Git repository rooted at `D:/Project/uae-erp-saas` | Repository state verification | Git status and diff checks are available for documentation governance |
| 28 October 2026 | ADR-001–ADR-020 | Accepted the initial architecture baseline after standards review | Product Owner — explicit project instruction | See `ADR_STANDARDS_REVIEW.md`; deferred product, regulatory, finance, provider, and operational choices remain open |
| 28 October 2026 | DEC-QA-002/003; DEC-PHASE-001/002; DEC-GOV-005/006; DEC-QA-004/005 | Approved the quality, bounded phase, traceability, manifest, tenant-test, and CI specification baselines | Product Owner — explicit market-standard review instruction | P00 exit, P01 implementation, test execution, and workflow implementation remain separate evidence/authorization gates |
| 28 October 2026 | P00-T-001 | Authorized and completed bounded manifest validators and initial read-only CI workflow | Product Owner — explicit implementation instruction | Local gates passed; hosted workflow run remains pending and no ERP/P01 implementation was authorized |
| 28 October 2026 | P00-EV-011 | Verified initial hosted CI execution evidence from run 40647091699 and artifact 12798425785 | Product Owner — explicit workflow execution instruction | Evidence verification does not approve P00 exit or authorize P01 implementation |
