# Pending Decisions Register — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | PM-DEC-001 |
| Version | 1.0 |
| Status | Active |
| Last Updated | 29 October 2026 |
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
| DEC-REG-002 | P04 supported document/applicability ruleset, PINT AE and mandatory-field/status-map versions | OPEN | Product / qualified UAE Tax and Legal / Integration | P04 schema, adapter mapping and submission activation |
| DEC-INT-002 | UAE e-invoicing ASP and exact contracted technical/operational capabilities | OPEN | Product / Security / Legal / Finance / Operations | Provider-dependent P04 implementation and activation |
| DEC-FIN-005 | P05 legal-entity, chart, functional/multi-currency, posting, reversal, close/reopen and opening-balance policy | OPEN | Product / Finance / Architecture | P05 accounting schema and posting implementation |
| DEC-TAX-001 | P05 supported UAE VAT treatments, evidence, calculations, rounding, corrections, periods and workpaper mappings | OPEN | Product / Finance / qualified UAE Tax reviewer | P05 VAT schema, calculation and reporting activation |
| DEC-OPS-001 | Hosting region and data-residency requirements | OPEN | Product / Legal / Security / DevOps | Production infrastructure selection |
| DEC-OPS-002 | Availability, backup RPO, and recovery RTO | OPEN | Product / DevOps | Production architecture approval |
| DEC-DATA-002 | Retention, deletion, legal hold, and tenant-level recovery policy | OPEN | Legal / Compliance / Security | Production handling of customer data |
| DEC-OPS-003 | Production object-storage provider, region, scanning, encryption, quota, and lifecycle configuration | OPEN | Product / Security / Privacy / DevOps | Production file storage and customer document handling |
| DEC-API-003 | External API consumers, support/deprecation duration, and contractual exposure | OPEN | Product / Commercial / Architecture / Operations | Public or partner API commitment |
| DEC-P03-001 | P03 customer/party and sellable-item ownership | RECOMMENDED | Product / Architecture / CRM and Sales Owners | P03 schema implementation |
| DEC-P03-002 | P03 quotation, acceptance, order, and fulfillment scope | RECOMMENDED | Product / Sales Operations / Security / Legal | P03 Sales workflow implementation |
| DEC-FIN-004 | ERP invoice/credit numbering, currency, rounding, tax, correction, payment-allocation, document, and retention policies | OPEN | Product / Finance / UAE Tax and Legal / Operations | P03 invoice migrations and issue activation |

## 6. Actionable P03 Approvals

| Approval | Exact decision required | Authorized approver/reviewer | Evidence and alternatives | Recommendation and consequences | Recording action | Blocks |
|---|---|---|---|---|---|---|
| APPR-P03-001 | Approve or revise the bounded P03 implementation scope and P03-T01–T12 sequence | Product Owner, after Architecture/Security/Finance review | `P03_PHASE_SPECIFICATION.md`, matrix, three module specifications; alternative is a smaller CRM-only or CRM/Sales increment | Approve the bounded specification; this enables later task authorization but does not itself start implementation | Add dated approval to this register and use: “I approve P03-SPEC-001 as the bounded P03 implementation scope.” | P03 implementation only; not documentation |
| APPR-P03-002 / DEC-P03-001 | Select authoritative customer/party and sellable-item ownership | Product Owner and Architecture | CRM-owner/Sales-minimal-item recommendation; alternatives are a shared party/product domain or hard CRM/Inventory dependencies, each adding scope and migration coupling | CRM owns customer/contact; Sales initially owns a minimal non-stock commercial item with explicit future Inventory mapping | Record selected option/date/approver, then reconcile Module Catalogue, dependencies, P03 specs, and task manifests | P03 customer/item schema; not P04/P05 documentation |
| APPR-P03-003 / DEC-FIN-004 | Approve concrete invoice/credit financial and document policies and effective dates | Product Owner plus Finance and qualified UAE Tax/Legal reviewers | `ERP_CUSTOMER_INVOICING.md`, ADR-011/013, current authoritative UAE source register when prepared; alternatives include restricting P03 to drafts or enabling only explicitly reviewed document types/currencies | Enable only reviewed policies; keep issue/correction/payment behaviors disabled otherwise, avoiding incorrect financial or legal behavior | Record versioned policy decisions and reviewer/date/source evidence in this register and the owning specifications | Invoice migrations/issuance and commercial pilot; not CRM documentation |
| APPR-P03-004 | Approve P03 exit and, separately, any controlled pilot scope | Product Owner after independent QA/Security/Privacy/Database/Finance/UX/Operations review | P03-EV-001–014 and open-risk disposition; alternatives are reject, conditional exit with only waivable exceptions, or no pilot | Separate phase exit from pilot authorization; define enabled modules, tenants, dates, limitations, monitoring, and rollback authority | Add the exact exit/pilot statement, date, approver, evidence commit/artifacts, conditions, and expiry to `PHASE_STATUS.md` and this register | P03 exit/pilot and P04 implementation transition |

## 7. Actionable P04 and P05 Approvals

| Approval | Exact decision required | Authorized approver/reviewer | Evidence and alternatives | Recommendation and consequences | Recording action | Blocks |
|---|---|---|---|---|---|---|
| APPR-P04-001 | Approve or revise bounded P04 provider-neutral implementation scope | Product Owner after Architecture/Security/Finance review | P04-SPEC-001, P04-TRACE-001, module/contract specs; alternative is research/contracts only | Approve bounded scope with all unverified/provider-dependent flows disabled; enables later task authorization only | “I approve P04-SPEC-001 as the bounded P04 implementation scope, subject to its named gates.” Record date/approver | P04 implementation; not further documentation |
| APPR-P04-002 / DEC-INT-002 | Select ASP and approve exact contract/capabilities | Product, Security, Legal, Finance, Operations | Current MoF listing snapshot; contract, privacy/security/data/SLA/exit and technical artefacts; alternatives are defer or assess another listed ASP | Select only after complete due diligence; provider-neutral work avoids premature lock-in | Create dated provider-selection record naming legal entity, services, versions, environments, limitations, evidence and approvers | Provider adapter, credentials, sandbox/production activation |
| APPR-P04-003 / DEC-REG-001/002 | Approve applicability, dates, document types, fields/schema, statuses and retention policy | Qualified UAE Tax/Legal reviewers plus Product | REG-SRC-001, operative texts and checksummed PINT AE/mandatory-field/provider artefacts; alternative is disable affected flows | Approve an effective-dated bounded ruleset; never generalize beyond reviewed scope | Sign/version P04 policy record with source IDs/checksums, facts, exclusions, effective date, reviewer/date | P04 schema/mapping/submission activation |
| APPR-P04-004 | Approve P04 exit and separately any production provider traffic | Product Owner after independent QA/Security/Privacy/Finance/Operations/regulatory review | P04-EV-001–014 and open risks; alternatives are reject, conditional exit, or sandbox-only | Separate exit from production activation and name tenants/documents/environment/rollback | Add exact exit and separate activation statements, evidence commit/artifacts, conditions and expiry | P04 exit / production traffic |
| APPR-P05-001 | Approve or revise bounded P05 accounting/VAT implementation scope | Product Owner after Architecture/Finance/Security review | P05-SPEC-001, P05-TRACE-001 and module specs; alternative is accounting-only foundation | Approve ledger plus validated VAT-workpaper scope; keep filing/advanced finance excluded | “I approve P05-SPEC-001 as the bounded P05 implementation scope, subject to its named gates.” Record date/approver | P05 implementation |
| APPR-P05-002 / DEC-FIN-001/005 | Approve concrete accounting/currency/period policy | Product Owner, Finance and Architecture | ADR-011/013, ACCOUNTING spec; alternatives include AED-only/no FX and narrower chart/dimensions | Start with explicitly approved functional currency and minimal policy; disable advanced FX/opening behavior until reviewed | Create versioned finance-policy record covering precision, chart, dimensions, source/posting/reversal, close/reopen, opening and FX scope | Accounting migrations/posting |
| APPR-P05-003 / DEC-TAX-001 | Approve bounded UAE VAT policy | Qualified UAE Tax reviewer plus Finance/Product | REG-SRC-001 and operative legislation/guidance; alternatives are disabled VAT or fewer supported treatments | Enable only reviewed transaction types/treatments with exact calculation/rounding/evidence/workpaper versions | Sign/version VAT policy with source IDs/checksums, effective date, examples, exclusions and reviewer/date | VAT schema/calculation/report activation |
| APPR-P05-004 | Approve P05 exit and separately production accounting/VAT scope | Product Owner after Finance/Tax/Security/Database/Operations/independent QA review | P05-EV-001–015, reconciliations and risks; alternatives are conditional or accounting-only exit | Approve exact enabled scope; keep filing/payment outside unless separately authorized | Add exact exit/production statement, evidence commit/artifacts, limitations, monitoring and rollback | P05 exit / production scope |

## 8. Decision Recording Requirements

Every resolved entry must record:

- Selected option and scope.
- Approver and approval date.
- Related ADR or product record.
- Documents requiring reconciliation.
- Implementation and test implications.
- Any deferred follow-up decision.

Detailed decision inventories currently embedded in product and architecture documents will be mapped into this register incrementally as their owning documentation unit is reviewed. Their presence does not constitute approval.

## 9. Decision Log

| Date | Decision ID | Outcome | Approved by | Notes |
|---|---|---|---|---|
| 28 October 2026 | DOC-BASELINE-001 | Approved the repository documentation in scoped baseline/specification classes | Product Owner — explicit market-standard review instruction | See `DOCUMENT_STANDARDS_REVIEW.md`; no compliance certification or implementation authorization implied |
| 27 October 2026 | DEC-GOV-003 | Reserved IAM-NNN for product requirements and IAM-TST-NNN for architecture test scenarios | Documentation governance rule | Corrected an identifier collision without changing required behavior |
| 28 October 2026 | DEC-GOV-004 | Verified the existing Git repository rooted at `D:/Project/uae-erp-saas` | Repository state verification | Git status and diff checks are available for documentation governance |
| 28 October 2026 | ADR-001–ADR-020 | Accepted the initial architecture baseline after standards review | Product Owner — explicit project instruction | See `ADR_STANDARDS_REVIEW.md`; deferred product, regulatory, finance, provider, and operational choices remain open |
| 28 October 2026 | DEC-QA-002/003; DEC-PHASE-001/002; DEC-GOV-005/006; DEC-QA-004/005 | Approved the quality, bounded phase, traceability, manifest, tenant-test, and CI specification baselines | Product Owner — explicit market-standard review instruction | P00 exit, P01 implementation, test execution, and workflow implementation remain separate evidence/authorization gates |
| 28 October 2026 | P00-T-001 | Authorized and completed bounded manifest validators and initial read-only CI workflow | Product Owner — explicit implementation instruction | Local gates passed; hosted workflow run remains pending and no ERP/P01 implementation was authorized |
| 28 October 2026 | P00-EV-011 | Verified initial hosted CI execution evidence from run 40647091699 and artifact 12798425785 | Product Owner — explicit workflow execution instruction | Evidence verification does not approve P00 exit or authorize P01 implementation |
| 28 October 2026 | P00-EV-014 | Approved P00 as Product Owner | Product Owner — explicit instruction “i approve p00” | Independent P00-EV-013 review and initial-increment scope disposition remain; P01 implementation is not authorized |
| 28 October 2026 | APPR-P00-002 | Approved bounded P01 Core Platform and Multi-Tenancy as the initial implementation increment | Product Owner — explicit approval statement | DEC-PROD-001 remains open for commercial pilot planning; P01 implementation still requires APPR-P01-001 |
