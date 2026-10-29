# SALES — Sales Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-SALES-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Owning Phase | P03 |
| Django App | `sales` |
| Domain Owner | Sales Management |
| Commercial Module | Yes |
| Tenant-Owned Data | Yes |

## 1. Purpose and Sources

Own sellable commercial references, quotations, revisions, approvals, acceptances, and sales orders between CRM interest and downstream invoicing/fulfillment. This specification follows the [P03 phase specification](../02-phases/P03_CRM_SALES_INVOICING/P03_PHASE_SPECIFICATION.md), Module Catalogue Sales boundary, ADR-003 through ADR-006, ADR-010, ADR-013 through ADR-015, and ADR-018 through ADR-020.

The stable product requirements are `SALES-001` through `SALES-005`. The `SALESM-*` rules below are module-level control identifiers that refine, but do not replace, those product requirements.

## 2. Scope

Included: minimal non-stock commercial item/reference, quotation and line calculation, revision/history, approval, send/acceptance evidence, expiry, sales order and lines, status/approval/cancellation, idempotent quote-to-order and order-to-invoice request, documents, reports, imports/exports, audit, and events.

Excluded: CRM master duplication, invoice ownership, tax authority, stock/reservation/delivery, procurement, accounting entries, revenue recognition, advanced CPQ/configurators, commissions, and provider communications.

## 3. Actors and Authorization

Sales users create/edit drafts within organizational/object scope. Approvers require distinct approval permissions and thresholds; self-approval is configurable and denied where separation is required. Managers control approved configuration and reports. Customers/portal identities may accept only through a separately approved authenticated contract. Support/auditors receive purpose-bound access.

Every action requires Sales entitlement plus user/object permission. Quotation approval, acceptance recording, order approval, cancellation, price/discount override, export, and conversion are distinct permissions.

## 4. Domain Ownership

| Record/capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Commercial item/service reference | `sales` initially | Direct tenant | Commercial catalogue service |
| Quotation, line, revision, approval, acceptance | `sales` | Direct/inherited tenant | Quotation services |
| Sales order, line, approval, status history | `sales` | Direct/inherited tenant | Order services |
| Customer/contact master | `crm` | Referenced same tenant | CRM snapshot contract |
| Customer invoice/credit/payment | `invoicing` | Created via command/service | Invoicing contract |
| Inventory item/availability/movement | Future `inventory` | Explicit mapping | Inventory contract only |

## 5. Data Model and Snapshot Requirements

Conceptual entities: `CommercialItem`, `Quotation`, `QuotationLine`, `QuotationRevision`, `SalesApproval`, `QuotationAcceptance`, `SalesOrder`, `SalesOrderLine`, `SalesOrderStatusHistory`, and `InvoiceRequest`.

- UUIDs and explicit tenant ownership; same-tenant customer/contact/item/user references.
- Document numbers unique in approved tenant/legal-entity/type/sequence scope.
- Header/line currency, quantity, unit-of-measure, description, price, discount, tax classification/result where approved, subtotals, total, policy version, and validity dates.
- Accepted/approved revisions and orders snapshot customer/contact/address/item descriptions and financial inputs needed for history.
- One active revision and explicit optimistic version; published/accepted revisions are immutable.
- Commercial item does not own stock quantity, valuation, warehouse, or movement. A future Inventory mapping is explicit and optional.
- No binary floating point; concrete precision/scale/range is approved before migration.

## 6. Workflows and States

### 6.1 Quotation

Conceptual states: `DRAFT`, `PENDING_APPROVAL`, `APPROVED`, `SENT`, `ACCEPTED`, `REJECTED`, `EXPIRED`, `WITHDRAWN`, and `SUPERSEDED`. Revision creates an append-oriented version. Server calculation runs on every material draft change and again under lock before approval/acceptance/conversion.

Acceptance records the specific revision, actor/channel/evidence, time, and terms version. It is not legal proof beyond the approved acceptance method. Stale, expired, superseded, unapproved, or cross-tenant revisions cannot be accepted.

### 6.2 Sales order

Conceptual states: `DRAFT`, `PENDING_APPROVAL`, `CONFIRMED`, `PARTIALLY_FULFILLED`, `FULFILLED`, `CANCELLATION_PENDING`, `CANCELLED`, and `CLOSED` as supported. P03 may leave fulfillment as an externally updated status contract; it must not fake stock or delivery.

Quote-to-order and order-to-invoice request use stable source IDs/idempotency keys and preserve source snapshots. Repeated/concurrent commands yield one order/request. Cancellation considers downstream invoice/fulfillment state and may require compensating workflows.

## 7. Calculation and Business Rules

| ID | Requirement | Verification |
|---|---|---|
| SALESM-001 | Server calculates all authoritative quotation/order totals using Decimal and explicit currency/policy | Financial tests |
| SALESM-002 | Client-submitted totals, approval status, discounts, and tax results are untrusted | Tamper tests |
| SALESM-003 | Approved/sent/accepted revisions are immutable; changes create a new revision | State/DB tests |
| SALESM-004 | Approval thresholds, price/discount overrides, and self-approval follow approved policy | Permission tests |
| SALESM-005 | Acceptance binds one eligible revision and preserves evidence | Workflow tests |
| SALESM-006 | Quote-to-order and order-to-invoice requests are tenant-safe, idempotent, and concurrency-safe | Integration tests |
| SALESM-007 | Sales never mutates CRM, invoice, inventory, or accounting tables directly | Boundary tests |
| SALESM-008 | Master-data changes do not rewrite accepted quotation/order snapshots | Historical tests |
| SALESM-009 | Missing pricing/tax/currency/approval policy blocks affected transition | Negative tests |
| SALESM-010 | Cancellation preserves history and coordinates downstream consequences | State/reconciliation tests |

Calculation order—quantity, unit price, discount, tax base, tax where approved, rounding, line total, document total, residual—must be versioned and explicit. P03 does not approve UAE VAT rates or treatment.

## 8. Tenant Isolation, Security, Entitlements, and Audit

All documents, revisions, approvals, acceptance tokens/evidence, files, tasks, reports, imports, exports, caches, and admin paths use trusted tenant context. Same-tenant customer/item/user references are enforced. Public acceptance links, if ever approved, use high-entropy single-purpose expiring tokens, safe responses, replay protection, and no tenant enumeration.

Entitlement and permission are separately required. Suspension denies new sales operations by default while approved read/export/integrity operations may remain. Material changes, overrides, approvals, acceptance, conversion, and cancellation are audited with tenant, actor, before/after state, version, reason, and correlation—without secrets or full sensitive content.

## 9. Integrations and Events

CRM supplies validated customer/contact snapshots. Invoicing accepts an idempotent invoice request referencing a confirmed eligible order/quotation and revalidates authoritative facts. Future Inventory supplies availability/reservation and owns fulfillment movements. Accounting receives only approved downstream invoice/posting facts, not mutable sales drafts.

Durable facts/commands use ADR-010 where loss matters, with versioned minimal payloads, aggregate version, tenant ID, correlation/causation, and idempotent consumers. Reconciliation compares source document, conversion operation, and downstream result.

## 10. UI, API, Documents, Reports, Imports, and Exports

Use Django/HTMX for list/detail, calculator-backed draft editing, revision comparison, approval inbox, acceptance status, order lifecycle, conversion, and audit history. Server returns calculation/validation results; client JavaScript is not authority. Approved APIs follow ADR-020.

Rendered quotation/order documents use immutable revision snapshots, private storage, authorized download, safe templates, and retry without new business effect. Imports are previewed, bounded, idempotent, and cannot import approved/accepted states. Reports define date/status/currency semantics and avoid unapproved cross-currency aggregation.

## 11. Operations, Migration, and Recovery

Monitor calculation failures, approval backlog, stale/expired quotations, sequence conflicts, duplicate conversion, downstream reconciliation, document failure, and entitlement denial anomalies. Migrations preserve revisions/source links and document precision. Restore tests reconcile quotation/order counts/totals, active revisions, conversion links, files, outbox, and audit.

## 12. Acceptance Criteria, Tests, and Evidence

Source requirements are `SALES-001`–`SALES-005`. Module controls are `SALESM-001`–`SALESM-010`; phase acceptance is P03-AC-004–006 and 016–020. Required tests are P03-TST-019–040 and 102–152 as applicable. Evidence is P03-EV-002, 005, and 009–012 in the [P03 matrix](../02-phases/P03_CRM_SALES_INVOICING/P03_TRACEABILITY_AND_TEST_MATRIX.md).

## 13. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| P03-DEC-002 | Sellable item/product ownership before Inventory | Product/Architecture | Sales schema | Sales owns minimal commercial item/service; Inventory later maps without taking historical ownership |
| SALES-DEC-001 | Standalone Sales vs hard CRM dependency | Product/Commercial | Entitlement configuration | Allow explicit CRM integration; do not duplicate CRM; decide commercial dependency before sale |
| SALES-DEC-002 | Approval thresholds/self-approval and customer acceptance method | Product/Sales Ops/Security/Legal | Approval/acceptance activation | Configurable thresholds; deny self-approval where material; validate acceptance evidence/legal effect |
| SALES-DEC-003 | Initial order/fulfillment scope | Product | P03-T05 | Treat fulfillment as bounded status/interface until Inventory/operations workflow is specified |

## 14. Implementation Prompt

Use [P03 orchestration](../04-agents/phase-prompts/P03_CRM_SALES_INVOICING.md) and P03-T04/T05 in [P03 bounded tasks](../04-agents/phase-prompts/P03_BOUNDED_TASK_PROMPTS.md).
