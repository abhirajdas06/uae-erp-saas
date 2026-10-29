# P03 — CRM, Sales, and ERP Customer Invoicing Phase Specification

| Property | Value |
|---|---|
| Document ID | P03-SPEC-001 |
| Status | READY FOR REVIEW |
| Phase | P3-CRM-SALES-INVOICING |
| Implementation Authorization | Not granted by this document |
| Owners | Product, Architecture, Revenue Operations, Finance |
| Required predecessors | P01 approved and implemented; P02 entitlement contracts available |

## 1. Objective

Deliver the first coherent tenant business workflow from customer relationship through quotation and sales order to a tenant-issued customer invoice, credit note, and customer-payment allocation foundation. P03 must preserve tenant isolation, server-side permissions and entitlements, immutable issued financial documents, exact monetary calculations, and explicit domain ownership.

## 2. Governing Sources

- [Product Requirements](../../00-product/PRODUCT_REQUIREMENTS.md): `CRM-001`–`CRM-003` and `INV-001`–`INV-005`.
- [Module Catalogue](../../00-product/MODULE_CATALOGUE.md): CRM, Sales, and Invoicing.
- [Development Roadmap](../../00-product/DEVELOPMENT_ROADMAP.md), Phase 3.
- [Database Design](../../01-architecture/DATABASE_DESIGN.md), [Module Dependencies](../../01-architecture/MODULE_DEPENDENCIES.md), [Authentication and Permissions](../../01-architecture/AUTHENTICATION_AND_PERMISSIONS.md), and [Entitlement Engine](../../01-architecture/ENTITLEMENT_ENGINE.md).
- ADR-003 through ADR-008, ADR-010, ADR-011, ADR-013 through ADR-015, and ADR-018 through ADR-020.
- [Security Requirements](../../05-quality/SECURITY_REQUIREMENTS.md) and [Testing Strategy](../../05-quality/TESTING_STRATEGY.md).
- [CRM](../../03-modules/CRM.md), [Sales](../../03-modules/SALES.md), and [ERP Customer Invoicing](../../03-modules/ERP_CUSTOMER_INVOICING.md).

No source in this batch is evidence of UAE tax, e-invoicing, accounting, or legal compliance.

## 3. Entry Gate

Implementation requires:

1. Verified P01 tenant, identity, permission, audit, database, migration, file, and CI foundations.
2. A stable P02 entitlement-evaluation contract for `CRM`, `SALES`, and `INVOICING`; P02 need not be commercially live if test fixtures provide the approved contract.
3. Explicit authorization of a bounded P03 task.
4. Resolution of schema-affecting P03 decisions: customer master, sellable-item ownership, invoice numbering scope, supported currency/tax behavior, and initial sales workflow.
5. Approved test-only policy fixtures where commercial, finance, or regulatory policy remains unresolved.

Documentation and test design may proceed before these gates close. Undecided workflows must remain disabled rather than guessed.

## 4. Bounded Scope and Non-Goals

### 4.1 Included

- Tenant customer/account and contact management, duplicate review, search, lifecycle, and audit.
- Leads, opportunities, configurable pipeline stages, activities, ownership, and assignment.
- Bounded sellable-item/commercial-reference contract needed for quotations and invoice lines.
- Quotation creation, calculation, revision, approval, sending/acceptance recording, expiry, and conversion.
- Sales order creation, approval, revision/cancellation rules, fulfillment-status placeholders, and invoice-request interface.
- Customer invoice drafts, server calculation, numbering, issue/finalization, documents, credit notes/corrections, payments, allocations, balances, and statements where approved.
- Controlled cross-domain snapshots, idempotent conversion, audit, outbox events, tenant-safe files, reports, imports/exports, migrations, tests, and runbooks.

### 4.2 Excluded

- SaaS subscription billing owned by P02 `billing`.
- UAE e-invoicing submission, provider selection, accreditation, or compliance claims (P04).
- Authoritative VAT rules/returns and general-ledger posting (P05).
- Inventory reservation, stock movement, delivery, and cost/valuation (P06).
- Bank feeds and bank reconciliation (P09).
- Payment gateway processing unless separately approved; P03 records customer payment evidence only.
- Revenue recognition, collections automation, advanced pricing/promotions, full CPQ, marketing automation, and production deployment.
- Hardcoded UAE tax rates, statutory fields, retention periods, or invoice wording.

## 5. Domain Ownership and Integration Boundaries

| Capability/record | Authoritative owner | Boundary |
|---|---|---|
| Customer account, contact, lead, opportunity, CRM activity | `crm` | Other domains reference stable IDs and snapshot required facts |
| Sellable commercial item, quotation, sales order, revisions/approvals | `sales` | Inventory mapping is a future explicit interface; no stock ownership |
| Customer invoice, credit note, customer payment record, allocation, balance, rendered invoice artifact | `invoicing` | No SaaS billing, ledger, bank reconciliation, or e-invoice provider state |
| Tenant entitlement | `subscriptions` | Required independently from user permission |
| Tenant/user/role/audit foundation | P01 domains | P03 cannot redefine tenant or identity models |

An accepted quotation or order may request an invoice through an idempotent invoicing service. Sales must not create or mutate invoice rows directly. Invoicing snapshots the authoritative commercial facts required to preserve issued history.

## 6. Cross-Cutting Invariants

1. Every tenant-owned object has one enforceable tenant path; cross-tenant references fail in services and the database.
2. Entitlement, user permission, object scope, lifecycle state, and approval are independent checks.
3. Clients may propose quantities, prices, discounts, tax classifications, and totals but the server validates or calculates authoritative values.
4. Authoritative money uses `Decimal`, explicit currency, versioned calculation policy, and named rounding stages under ADR-013.
5. Drafts may be edited under authorization. Issued/finalized invoices and credit notes freeze protected meaning and cannot be silently edited or hard-deleted.
6. Corrections preserve original and corrective records through an approved credit, cancellation, or replacement workflow.
7. Conversion, numbering, issue, credit, payment, and allocation commands are transactional, idempotent, concurrency-safe, and audited.
8. Current customer/item changes never rewrite issued-document snapshots.
9. Subscription expiry or module disablement does not delete CRM, sales, invoice, payment, document, or audit records.
10. Missing tax, numbering, currency, correction, or legal policy blocks affected issuance; it does not trigger a default assumption.

## 7. Bounded Task Packages

| Task | Objective | Depends on | Primary evidence |
|---|---|---|---|
| P03-T01 | Approve/reconcile P03 ownership, policies, permissions, and reference contracts | Entry gate | Decision and contract review |
| P03-T02 | Implement CRM customer/account and contact foundation | T01 | Schema, isolation, duplicate/search tests |
| P03-T03 | Implement leads, opportunities, pipeline, activities, and assignment | T02 | Workflow and permission tests |
| P03-T04 | Implement sellable-item contract and quotation calculation/revision | T01–T02 | Calculation and snapshot tests |
| P03-T05 | Implement quotation approval/acceptance and sales-order lifecycle | T04 | State, approval, concurrency tests |
| P03-T06 | Implement invoice draft and calculation service | T01–T02, T04 | Financial and tenant tests |
| P03-T07 | Implement invoice numbering, issue/finalization, and immutable snapshots | T06 | Concurrency and immutability tests |
| P03-T08 | Implement credit-note and correction workflows | T07 | Linked-correction and balance tests |
| P03-T09 | Implement customer payment records, allocations, and reconciliation foundation | T07–T08 | Allocation/idempotency tests |
| P03-T10 | Implement document rendering, files, UI, approved APIs, reports, imports/exports | T02–T09 | Boundary, visual, accessibility, file tests |
| P03-T11 | Implement outbox integrations and complete migration/security/operational verification | T03–T10 | Resilience, migration, recovery reports |
| P03-T12 | Assemble evidence and independent exit review | T11 | P03 evidence index and approvals |

Every implementation task must instantiate the repository task prompt template with exact files, source requirements, permissions, tests, evidence, migration/recovery behavior, reviewers, and prohibited scope.

## 8. Phase Acceptance Criteria

| ID | Criterion |
|---|---|
| P03-AC-001 | Customer and contact records have validated tenant ownership, lifecycle, duplicate handling, search, permissions, and audit. |
| P03-AC-002 | Leads, opportunities, stages, ownership, assignment, and activities follow configurable validated workflows. |
| P03-AC-003 | Customer/account ownership is not duplicated across CRM, Sales, and Invoicing. |
| P03-AC-004 | Sellable-item references and line snapshots preserve ownership boundaries and do not simulate inventory. |
| P03-AC-005 | Quotations calculate server-side, preserve revisions, enforce approvals, and record acceptance without silent mutation. |
| P03-AC-006 | Sales orders derive from approved sources, preserve history, and cannot bypass approval or duplicate conversion. |
| P03-AC-007 | Invoice drafts validate tenant, customer, lines, dates, currency, calculation policy, and permissions. |
| P03-AC-008 | Invoice and credit-note amounts are reproducible under explicit precision, currency, discount, tax, and rounding policies. |
| P03-AC-009 | Number assignment is unique within the approved scope and safe under concurrent issuance, retry, rollback, and failure. |
| P03-AC-010 | Invoice issue/finalization freezes protected snapshots and commits no partial authoritative state. |
| P03-AC-011 | Issued invoices cannot be silently edited/deleted through UI, API, service, task, import, admin, or bulk paths. |
| P03-AC-012 | Credit notes/corrections reference originals, obey limits and policy, preserve both records, and update balances once. |
| P03-AC-013 | Customer payments and allocations are tenant-safe, idempotent, currency-valid, bounded by available amounts, and reconcilable. |
| P03-AC-014 | Invoice balances/statements reconcile to authoritative invoices, credits, and allocations without becoming an accounting ledger. |
| P03-AC-015 | Rendered documents reproduce authoritative snapshots, are private and authorized, and retry safely without duplicate issuance. |
| P03-AC-016 | Entitlement and user/object permission are enforced independently at UI, direct URL, service, API, task, report, export, file, and admin boundaries. |
| P03-AC-017 | Tenant A cannot discover, reference, mutate, convert, render, download, report, or allocate against Tenant B data. |
| P03-AC-018 | Cross-domain events/commands are versioned, durable where required, idempotent, and reconcilable. |
| P03-AC-019 | Material changes and privileged access produce durable, redacted, tenant-attributed audit evidence. |
| P03-AC-020 | Clean/upgrade migrations, deployment overlap, backup/restore reconciliation, monitoring, and runbooks are verified. |
| P03-AC-021 | Required CI, security, finance, UX/accessibility, database, and operations reviews meet approved thresholds. |
| P03-AC-022 | Exit evidence is complete, reproducible, independently reviewed, and explicitly approved by the Product Owner. |

## 9. Security, Tenant Isolation, and Privacy

- Use only trusted P01 tenant context, scoped managers/services, same-tenant constraints, and approved RLS defense.
- Define distinct permissions for view, create, update, assign, approve, accept, convert, issue, credit, cancel, record payment, allocate, export, and privileged support.
- Treat customer/contact details, notes, communications, prices, margins, invoices, payments, and exports according to data classification and least privilege.
- Sanitize rich text and imported fields; protect against CSV/formula injection, stored XSS, IDOR, mass assignment, unsafe filters, and file-content attacks.
- Never log unnecessary contact data, invoice payloads, documents, payment evidence, access tokens, or secrets.
- Critical cross-tenant access, unauthorized issue/correction/payment, financial mutation, or sensitive-data exposure is a no-waiver exit blocker.

## 10. Financial, Regulatory, and Data-Integrity Requirements

- P03 may store tax classification and calculated tax snapshots only under a reviewed policy; P05 owns authoritative VAT configuration/reporting.
- P03 documents must expose readiness fields for P04 without implementing provider submission or claiming compliance.
- Invoice/credit-note numbering, mandatory fields, language/layout, retention, tax treatment, and correction rules require current authoritative review before commercial use.
- Payment records represent tenant-recorded customer receipts/evidence. They are not bank transactions or proof of bank settlement until reconciled through an approved later integration.
- Accounting postings are future explicit events/contracts. P03 must not create an incomplete ledger.

## 11. Migration, Operations, and Recovery

- Prove clean install and supported upgrade under restricted runtime roles and approved RLS policies.
- Migrations define UUIDs, tenant keys, uniqueness scope, precision/scale/range, snapshot/backfill rules, and forward-fix boundaries.
- Deployment must preserve old/new code and queued schema compatibility or use an approved maintenance boundary.
- Monitor duplicate candidates, invalid transitions, stale approvals, numbering contention/gaps, calculation failure, document generation, outbox backlog, allocation mismatch, cross-domain reconciliation, and unauthorized mutation attempts.
- Restore validation reconciles document counts/totals/balances, sequences, correction links, file artifacts, outbox state, and audit—not just row presence.

## 12. Test and Evidence Plan

The [P03 Traceability and Test Matrix](P03_TRACEABILITY_AND_TEST_MATRIX.md) is authoritative. Evidence identifiers are:

- P03-EV-001: entry gate and approved/disabled policy snapshot.
- P03-EV-002: domain ownership, schema, constraints, and migration review.
- P03-EV-003: CRM customer/contact/duplicate/search test report.
- P03-EV-004: lead/opportunity/activity workflow report.
- P03-EV-005: quotation/order calculation, revision, approval, and conversion report.
- P03-EV-006: invoice calculation, numbering, issue, and immutability report.
- P03-EV-007: credit/correction/payment/allocation/balance report.
- P03-EV-008: document rendering/file/visual/accessibility report.
- P03-EV-009: entitlement, authorization, and tenant-isolation report.
- P03-EV-010: event/task/idempotency/reconciliation resilience report.
- P03-EV-011: security/privacy/audit review.
- P03-EV-012: migration/deployment/backup/recovery/operations review.
- P03-EV-013: finance/regulatory-readiness review and limitations.
- P03-EV-014: independent completion report and Product Owner decision.

Evidence records commit SHA, commands, environment, result, artifact/digest, reviewer, limitations, and retention location.

## 13. Exit Gate

P03 may become `APPROVED` only when P03-AC-001–022 are verified; no critical/high isolation, authorization, privacy, financial-integrity, issued-record, secret, or migration finding remains; every enabled tax/numbering/correction/payment policy is approved; specialist and independent reviews are recorded; and the Product Owner approves P03 exit.

P03 exit does not authorize commercial pilot, P04, compliance claims, customer data import, or production deployment unless separately stated.

## 14. Pending Approvals

| ID | Approval | Owner | Required before | Recommendation | Approval form |
|---|---|---|---|---|---|
| APPR-P03-001 | Bounded P03 implementation scope | Product Owner | P03-T01 implementation | Approve this specification/task order | “I approve P03-SPEC-001 as the bounded P03 implementation scope.” |
| APPR-P03-002 | Customer and sellable-item ownership | Product/Architecture | P03 schema | CRM owns customer/contact; Sales owns a minimal non-stock commercial item, with future Inventory mapping | Record P03-DEC-001/002 choices explicitly |
| APPR-P03-003 | Invoice financial and document policies | Product/Finance/qualified UAE reviewer | Issuance/correction activation | Approve numbering, currencies, rounding, tax behavior, fields, correction, retention, and language; disable unresolved behavior | Reference policy versions/effective dates |
| APPR-P03-004 | P03 exit and any controlled pilot | Product Owner | Phase transition/pilot | Approve exit evidence and pilot scope separately | State exact enabled modules, limitations, tenants, dates, and rollback authority |
