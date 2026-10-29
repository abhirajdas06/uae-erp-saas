# P03 CRM, Sales, and ERP Customer Invoicing — Orchestration Prompt

Use this prompt only after the P03 implementation entry gate is satisfied and a bounded P03 task is explicitly authorized.

## Role

Act as P03 orchestrator for the UAE ERP SaaS modular monolith. Coordinate Product, Architecture, CRM/Sales Operations, Finance, Development, Database, Security/Privacy, QA, UX/Accessibility, DevOps, Operations, and Documentation. Agent completion messages are not evidence; require reproducible results and independent review.

## Authoritative Inputs

Read completely before dispatch:

- `AGENTS.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md` (`CRM-001`–`CRM-003`, `INV-001`–`INV-005`)
- `docs/00-product/MODULE_CATALOGUE.md`
- `docs/00-product/DEVELOPMENT_ROADMAP.md`, Phase 3
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/MODULE_DEPENDENCIES.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/01-architecture/ENTITLEMENT_ENGINE.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- ADR-003 through ADR-008, ADR-010, ADR-011, ADR-013 through ADR-015, and ADR-018 through ADR-020
- `docs/02-phases/P03_CRM_SALES_INVOICING/P03_PHASE_SPECIFICATION.md`
- `docs/02-phases/P03_CRM_SALES_INVOICING/P03_TRACEABILITY_AND_TEST_MATRIX.md`
- `docs/03-modules/CRM.md`, `SALES.md`, and `ERP_CUSTOMER_INVOICING.md`
- `docs/05-quality/SECURITY_REQUIREMENTS.md` and `TESTING_STRATEGY.md`
- P01/P02 contracts and exit evidence applicable to the task
- Current decision, risk, phase-status, and evidence registers.

## Objective

Deliver only the approved P03 customer-to-cash foundation: CRM customers/contacts/leads/opportunities; Sales commercial items/quotations/orders; tenant-issued invoice/credit/payment-allocation records; calculations; immutable issued snapshots; documents; integrations; tests; runbooks; and evidence.

Do not implement P02 SaaS billing, UAE e-invoicing submission, authoritative VAT/ledger, inventory/fulfillment, bank reconciliation, live payment gateways, production deployment, or unverified regulatory policy.

## Required Task Order

1. P03-T01 — decision and contract baseline.
2. P03-T02 — CRM customer/account/contact foundation.
3. P03-T03 — lead/opportunity/activity workflow.
4. P03-T04 — commercial-item and quotation foundation.
5. P03-T05 — quotation approval/acceptance and sales orders.
6. P03-T06 — invoice draft/calculation.
7. P03-T07 — numbering, issue, and immutable snapshot.
8. P03-T08 — credit/correction.
9. P03-T09 — customer payment/allocation/balance.
10. P03-T10 — documents, UI/API, reports, imports/exports.
11. P03-T11 — durable integrations and full verification.
12. P03-T12 — evidence and independent exit review.

T02 and bounded T04 technical preparation may proceed in parallel only after T01 fixes customer/item ownership. Models, migrations, tenant context, calculation primitives, numbering, invoice state, audit, files, and shared service contracts are high-coordination areas with one integration owner.

## Task Generation Rule

Instantiate `docs/04-agents/IMPLEMENTATION_TASK_PROMPT_TEMPLATE.md` using the applicable bounded prompt. Include authorization, exact file scope, source/acceptance/test/evidence IDs, permitted models/services, tenant/permission/entitlement paths, migration and recovery, transaction/idempotency/concurrency behavior, reviewers, reproducible commands, and explicit exclusions.

## Mandatory Controls

- CRM owns customer/contact master; Sales and Invoicing reference and snapshot it.
- Sales owns quotation/order; Invoicing owns tenant-issued invoice/credit/payment allocation.
- P02 `billing` remains wholly separate from P03 `invoicing`.
- Client values are proposals; the server validates authoritative totals and state.
- Use Decimal, explicit currency, approved precision/ranges/rounding, and immutable calculation snapshots.
- Issue/credit/payment/allocation/conversion are transactional, idempotent, concurrency-safe, tenant-safe, and audited.
- Issued protected fields cannot be edited/deleted through admin, import, API, task, or bulk paths.
- Entitlement and permission are independently enforced at every boundary.
- Required follow-up uses outbox/operation records and reconciliation.
- Unresolved tax/legal/accounting/e-invoicing/banking behavior stays disabled.
- Tests use synthetic data; never send real documents, submissions, or payments.

## Stop Conditions

Stop the affected dependent task and record an actionable decision when:

- accepted architecture conflicts with proposed ownership/schema;
- customer/item/legal-entity/numbering/currency/tax/correction ownership remains ambiguous for the task;
- tenant/same-tenant integrity, financial immutability, exact calculations, or duplicate prevention cannot be enforced;
- work would require a compliance claim, provider, real customer data, production secret, destructive migration, or production operation;
- a critical/high isolation, authorization, privacy, financial-integrity, file, audit, or migration finding remains.

Continue independent documentation, contracts, tests, and disabled-path work where safe.

## Completion Report

After each task report changed files; acceptance/test IDs; commands actually executed; evidence/digest; tenant/security/privacy/financial/migration review; defects and disabled features; status/decision/risk updates; next dependency-ready task; and every approval with ID, approver, evidence/alternatives, recommendation/consequences, exact recording statement/action, and blocked scope.

P03 exit requires independent QA, Security/Privacy, Database, Finance, UX/Accessibility, and Operations dispositions plus explicit Product Owner approval. Exit does not itself authorize pilot, P04, production, or compliance claims.
