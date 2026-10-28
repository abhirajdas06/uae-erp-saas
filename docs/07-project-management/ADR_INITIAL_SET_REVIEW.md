# Initial ADR Set — Consistency Review and Human-Approval Summary

| Property | Value |
|---|---|
| Document ID | PM-ADR-REVIEW-001 |
| Version | 1.0 |
| Status | Superseded as current approval summary by `ADR_STANDARDS_REVIEW.md` |
| Review Date | 28 October 2026 |
| Scope | ADR-001 through ADR-020 |
| Decision Authority | Product Owner and designated specialist reviewers |

## 1. Purpose and Authority

> **Historical review snapshot:** The pending-approval position in this document was superseded on 28 October 2026 by `ADR_STANDARDS_REVIEW.md`, which records the standards review and explicit acceptance of ADR-001 through ADR-020. This file is retained as the pre-approval consistency and grouping record.

This document records the cross-ADR review of the initial architecture decision set and organizes the twenty proposed decisions into dependency-aware human-approval packets.

It is a review snapshot, not a second ADR register and not an approval record. The canonical identifier, file, and status register is `../01-architecture/ARCHITECTURAL_DECISIONS/README.md`. Unresolved decision ownership and disposition remain canonical in `DECISIONS_PENDING.md`.

Every ADR remains `PROPOSED`. Detailed text, mandatory language, a recommendation in this summary, or approval of a related ADR does not implicitly approve another decision.

## 2. Review Scope and Method

The review covered:

- All ADR files from ADR-001 through ADR-020.
- The ADR register and template.
- Cross-references among architecture, product, and project-governance documents.
- Architecture style, domain ownership, tenancy, authorization, entitlement, UI/API, task/event, financial, integration, identifier, quality, deployment, secret, audit, storage, and contract boundaries.
- Security, tenant isolation, financial integrity, migrations, operations, testability, unresolved questions, and approval status.

Automated checks covered file count, identifier uniqueness, ADR status declarations, local Markdown link targets, and references to unknown ADR identifiers. Semantic review covered dependencies, overlapping responsibility, incompatible recommendations, and source-document drift.

## 3. Review Result

### 3.1 Confirmed findings

- The initial set contains exactly twenty uniquely numbered ADR files, ADR-001 through ADR-020.
- All twenty decisions are `PROPOSED`; none is recorded as `ACCEPTED`, `REJECTED`, `SUPERSEDED`, or `DEPRECATED`.
- The ADR register uses one canonical topic for each identifier and links to every record.
- Each ADR contains the governance content applicable to the decision: context, drivers, alternatives, decision, rationale, consequences, risks, security/tenancy, data/migration, operations, implementation requirements, testable criteria, references, approval, and supersession history. ADR-001 and ADR-002 use expanded section numbering but cover the required subjects.
- No broken local Markdown link or reference to an unknown ADR identifier was found in the repository review.
- No direct contradiction was found between the recommendations in ADR-001 through ADR-020 when they are read as one proposed architecture.
- Provider selection, regulatory interpretation, legal retention, commercial API support promises, hosting topology, and other specialist choices remain explicitly unresolved rather than being invented.

### 3.2 Coherent dependency chains

The following relationships are mutually consistent and should be preserved during review:

1. ADR-001's modular monolith is decomposed by ADR-003 domain ownership; ADR-008 keeps ordinary internal calls in-process.
2. ADR-002's shared schema relies on ADR-004 layered tenant isolation and ADR-014 tenant-aware references; none treats UUIDs or RLS as a substitute for application authorization.
3. ADR-005 user authorization and ADR-006 commercial entitlement are separate required checks.
4. ADR-007's server-rendered UI and ADR-008's selective DRF use are compatible with ADR-020's versioned external contracts.
5. ADR-009 treats Redis as transient infrastructure; ADR-010 keeps material delivery intent in PostgreSQL and assumes at-least-once processing.
6. ADR-011 protected posting uses ADR-013 monetary semantics and ADR-014 stable tenant-aware references.
7. ADR-012 isolates UAE e-invoicing providers and depends on ADR-009/010 for durable asynchronous work, ADR-019 for evidence storage, and ADR-020 for versioned provider contracts.
8. ADR-015 supplies the verification gates for the other decisions; ADR-016 deployment depends on ADR-017 secrets, ADR-018 logging/audit, and ADR-019 durable files.
9. ADR-018 keeps audit events distinct from diagnostic logs; ADR-019 keeps file content distinct from file metadata and audit evidence.
10. ADR-020 versions external presentation/integration contracts without duplicating authoritative domain state.

### 3.3 Remaining source-document reconciliation

These are not contradictions between the ADR recommendations, but they must be corrected after the relevant ADRs are approved:

| Item | Current drift | Proposed authority | Required action after approval |
|---|---|---|---|
| Tenant membership owner | Architecture documents alternate between `users` and `tenants` | ADR-003 proposes `tenants.TenantMembership`; ADR-005 is aligned | Update `DJANGO_APP_STRUCTURE.md` and related model tables |
| RLS tenant-context key | `MULTI_TENANCY.md` uses `app.tenant_id`; ADR-002/004 use `app.current_tenant_id` | ADR-004 proposes `app.current_tenant_id` | Align all policy and transaction examples before implementation |
| Phase identifiers | Documents mix P00/P01, P0/P1, and descriptive machine IDs | `PHASE_STATUS.md` and DEC-GOV-002 propose P00–P12 | Approve convention and update references/manifests |
| Draft authority | Several architecture documents use mandatory wording although decisions are not approved | ADR status register | Add or retain draft/proposal notices; do not implement solely from prose |
| Quality specifications | ADR-015/017/018 define direction, but security and testing standards are absent | P00 governance backlog | Draft `SECURITY_REQUIREMENTS.md` and `TESTING_STRATEGY.md` |
| Operations specifications | Topology, RPO/RTO, backup, recovery, retention, and provider choices are open | DEC-OPS-001/002 and DEC-DATA-002 | Resolve before production infrastructure commitment |
| Traceability | Requirements, ADR controls, tests, and evidence have no unified matrix | P00 governance backlog | Define traceability rules and initial matrix |

### 3.4 Decisions deliberately left open

The ADR set establishes boundaries without deciding:

- Launch segment, module scope, pricing, billing provider, or paid vendors.
- UAE regulatory applicability, dates, provider accreditation, or claims of compliance.
- Financial precision/scale matrices, VAT rounding policy, exchange-rate sources, and residual allocation.
- Production region, data residency, availability, RPO/RTO, and tenant-level recovery method.
- Secret-management, observability, object-storage, malware-scanning, or hosting provider.
- Legal retention periods, deletion rules, legal-hold details, or data-processing terms.
- API support/deprecation duration, initial external consumers, or contractual service levels.

These open choices do not invalidate the proposed boundaries. They block the dependent production or migration commitment identified in `DECISIONS_PENDING.md`.

## 4. Grouped Human-Approval Plan

Human reviewers should record an explicit disposition for every ADR in a packet. A packet may be approved, rejected, returned for revision, or split, but approval of the packet must not be inferred from silence.

### Group 1 — Core structure, tenancy, and identifiers

**ADRs:** ADR-001, ADR-002, ADR-003, ADR-004, ADR-014  
**Recommendation:** Approve together after architecture, security, and database review.

This group establishes the modular monolith, shared database/schema, authoritative domain ownership, layered tenant isolation/RLS, and UUID/tenant-aware reference strategy. Together they define the shape of the P01 data model and the controls preventing cross-tenant relationships.

**Alternatives and practical consequences:** Microservices or per-tenant databases/schemas add deployment and migration complexity now; omitting RLS reduces defense-in-depth; application-only same-tenant checks leave database integrity gaps; universal bigint identifiers make external references more enumerable and migration seams less stable. The proposed option instead increases query, constraint, RLS, and test discipline in one shared schema.

**Principal risks/costs:** RLS context leakage, shared-database blast radius, composite constraints, UUID index locality, and migration rigor.

**Blocking effect:** Blocks foundational model creation, tenant-owned migrations, production database-role design, and P01 implementation. Documentation that does not assume incompatible topology can continue.

**Approval conditions:** Resolve DEC-ARCH-003 and DEC-SEC-002 as part of the group; require negative cross-tenant tests and restricted runtime roles.

### Group 2 — Identity, authorization, and commercial access

**ADRs:** ADR-005, ADR-006  
**Recommendation:** Approve after security and product/commercial review, following Group 1.

This group separates identity and tenant-scoped RBAC/object authorization from module entitlement and dependency enforcement.

**Alternatives and practical consequences:** Conflating entitlements with permissions can let a subscribed tenant bypass user authorization or let an authorized user access an unsubscribed module. Client-side-only controls are insecure. The proposal adds a consistent server-side decision sequence and lifecycle behavior.

**Principal risks/costs:** Permission sprawl, stale entitlement caches, support-access abuse, complex object scope, and dependency-transition rules.

**Blocking effect:** Blocks authentication/membership/role implementation and P02 entitlement services. UI copy, permission catalog drafts, and test specifications can continue.

**Approval conditions:** Confirm membership ownership from Group 1 and assign product ownership for entitlement lifecycle rules.

### Group 3 — User interface, REST exposure, and contract evolution

**ADRs:** ADR-007, ADR-008, ADR-020  
**Recommendation:** Approve the server-rendered default, selective DRF boundary, and `/api/v{major}/` contract policy together.

The group keeps the primary product interface in Django Templates/HTMX/Tailwind, limits APIs to justified machine consumers, and governs those APIs and external contracts through explicit versions and compatibility evidence.

**Alternatives and practical consequences:** A default SPA or API-first architecture increases frontend/authentication/contract surface before a requirement justifies it. Unversioned APIs create silent consumer breakage. The proposal favors a smaller surface while accepting parallel-version maintenance when external contracts exist.

**Principal risks/costs:** HTMX interaction consistency, DRF exceptions becoming the default, concurrent API support, consumer inventory, and deprecation overhead.

**Blocking effect:** Blocks frontend/API scaffolding and external contract commitments, but not domain/service documentation.

**Approval conditions:** Define initial approved consumers before exposing endpoints; commercial support/deprecation duration may remain a later decision.

### Group 4 — Background execution, durable events, and e-invoicing boundary

**ADRs:** ADR-009, ADR-010, ADR-012  
**Recommendation:** Approve the reliability model together; approve no provider or compliance claim through this packet.

This group uses Celery/Redis for execution, PostgreSQL operation/outbox records for authoritative intent, at-least-once delivery with idempotency, and a provider-neutral e-invoicing domain/adapter boundary.

**Alternatives and practical consequences:** Broker-only state can lose required work; direct provider calls inside financial transactions create ambiguity and latency; provider schemas in invoicing code create lock-in. The proposed design adds operation records, dispatch, retries, reconciliation, and adapter work.

**Principal risks/costs:** Duplicate delivery, stuck outbox rows, worker isolation, uncertain provider outcomes, and reconciliation workload.

**Blocking effect:** Blocks critical worker workflows, reliable integrations, and P04 implementation. Regulatory research and provider-neutral specifications can continue.

**Approval conditions:** Regulatory applicability, provider selection, schemas, and accreditation remain separate specialist decisions under DEC-REG-001.

### Group 5 — Financial posting and monetary semantics

**ADRs:** ADR-011, ADR-013  
**Recommendation:** Approve the integrity principles after finance, accounting, and UAE tax review; retain concrete numeric policies as separately approved configuration/specification.

This group protects posted entries from in-place mutation, uses explicit reversals/corrections, requires decimal arithmetic and currency, and makes rounding stages named and versioned.

**Alternatives and practical consequences:** Mutable posted entries simplify corrections but destroy audit and reconciliation evidence. Binary floats or ad hoc rounding create irreproducible totals. The proposal requires more workflow states, correction documents, balancing controls, and test fixtures.

**Principal risks/costs:** Incorrect posting boundaries, concurrency, scale overflow, residual allocation, and historical rule reproduction.

**Blocking effect:** Blocks financial schema migrations, posting engines, VAT calculations, and money-bearing API contracts. Non-financial documentation can continue.

**Approval conditions:** DEC-FIN-001 must be resolved before financial implementation acceptance, even if these ADR principles are approved.

### Group 6 — Engineering quality, deployment, secrets, audit, and files

**ADRs:** ADR-015, ADR-016, ADR-017, ADR-018, ADR-019  
**Recommendation:** Approve the control boundaries as the P00 engineering baseline; defer individual infrastructure providers and numerical service objectives.

This group defines risk-based CI gates, one immutable Docker application image with explicit process roles, runtime secret injection, separated audit/log/telemetry records, and private object storage with relational metadata and governed lifecycle.

**Alternatives and practical consequences:** Environment drift, baked secrets, application logs as audit evidence, or container-local files reduce initial setup but fail production security and recoverability needs. The proposal adds CI time, operational tooling, access review, scanning, storage reconciliation, and runbooks.

**Principal risks/costs:** False CI confidence, migration failure, secret leakage, audit data overcollection, object/metadata divergence, vendor/data-residency constraints, and recovery complexity.

**Blocking effect:** Blocks implementation merge gates and any production/release readiness claim. Provider-neutral security/testing/deployment specifications can continue.

**Approval conditions:** Create the detailed testing and security standards; resolve region, residency, RPO/RTO, retention, and provider choices before production commitment.

## 5. Recommended Approval Order

1. Group 1 — core structure, tenancy, and identifiers.
2. Group 2 — identity, authorization, and entitlements.
3. Group 5 — financial posting and monetary semantics, before finance schema work.
4. Group 4 — tasks, outbox, and e-invoicing boundary.
5. Group 3 — UI, REST exposure, and contract evolution.
6. Group 6 — engineering and operational baseline.

Groups 3–6 may be reviewed in parallel after their Group 1 dependencies are understood. Approval order is not implementation authorization. P00 exit evidence and explicit authorization are still required.

## 6. Approval Recording Procedure

For each ADR disposition:

1. Record the decision, approver, date, scope, conditions, and notes in the ADR's Approval section.
2. Change the ADR status and supersession table only to match the explicit disposition.
3. Update the canonical ADR register and corresponding entry in `DECISIONS_PENDING.md`.
4. Reconcile affected architecture documents and mark any intentional exception.
5. Update risks, phase evidence, requirements/test traceability, and implementation backlog.
6. Re-run link, status, identifier, and cross-ADR checks.

Conditional approval must state the condition precisely. A material change to the selected option requires revised review or a superseding ADR, not an undocumented edit.

## 7. Review Conclusion

The initial ADR set is complete enough for grouped human architecture review. It presents one internally coherent proposed direction and preserves meaningful unresolved provider, regulatory, commercial, finance-policy, retention, and operational choices.

The review does **not** establish implementation readiness or regulatory compliance. P00 still requires dispositions for foundational ADRs, a bounded phase specification, security and testing standards, traceability, operational objectives, specialist validation, and explicit authorization.

## 8. Change Log

| Date | Change |
|---|---|
| 28 October 2026 | Completed initial ADR-001 through ADR-020 consistency review and grouped approval plan. |
