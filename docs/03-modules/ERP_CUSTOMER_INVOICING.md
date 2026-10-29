# INVOICING — ERP Customer Invoicing Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-INVOICING-001 |
| Status | READY FOR REVIEW |
| Owning Phase | P03 |
| Django App | `invoicing` |
| Domain Owner | ERP Customer Invoicing |
| Commercial Module | Yes |
| Tenant-Owned Data | Yes |

## 1. Purpose and Sources

Own invoices a tenant issues to its customers, related credit notes, customer-payment evidence, allocations, balances, statements, and rendered document artifacts. This specification implements `INV-001`–`INV-005` under the [P03 phase specification](../02-phases/P03_CRM_SALES_INVOICING/P03_PHASE_SPECIFICATION.md), Module Catalogue Invoicing boundary, ADR-003 through ADR-006, ADR-010, ADR-011, ADR-013 through ADR-015, and ADR-018 through ADR-020.

This module is categorically separate from P02 SaaS subscription billing.

## 2. Scope

### 2.1 Included

- Manual and source-driven invoice drafts and lines.
- Server-side amount calculation, currency, dates, terms, numbering, issue/finalization, and immutable snapshots.
- Credit notes and approved cancellation/replacement workflows.
- Customer-payment records, allocations, outstanding balances, and bounded statements.
- Invoice/credit-note rendering, private storage, authorized download, audit, events, reports, imports/exports, reconciliation, and recovery.

### 2.2 Excluded

- SaaS subscription invoices/payments (`billing`).
- UAE e-invoice provider submission/status (`e_invoicing`, P04).
- Authoritative VAT policy/returns (`vat`, P05).
- General ledger, revenue recognition, accounting periods, or journal entries (`accounting`, P05).
- Bank transactions/reconciliation (`banking`, P09).
- Card/payment-gateway collection and claims of legal/tax compliance.

## 3. Actors and Authorization

| Actor | Permitted scope |
|---|---|
| Invoice preparer | Create and edit drafts within organizational/object scope |
| Invoice issuer/approver | Approve and issue eligible drafts under amount/entity policy |
| Credit/correction approver | Create/approve linked corrections within remaining limits |
| Receivables user | Record customer payment evidence and allocate within authorized scope |
| Finance manager | Configure approved sequences/terms, reconcile, review exceptions, report |
| Customer/portal user | View/download only their documents through a separately approved identity contract |
| Support/auditor | Purpose-bound privileged access or read-only evidence review |

Create, update, issue, cancel, credit, record payment, allocate, reverse, export, and configure sequence are distinct permissions. Entitlement is additionally required and never substitutes for permission.

## 4. Domain Ownership

| Record/capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Customer invoice and line | `invoicing` | Direct/inherited tenant | Draft/issue services |
| Invoice sequence/reservation | `invoicing` | Tenant/legal entity/document type | Numbering service |
| Credit note and line | `invoicing` | Original invoice/tenant | Correction service |
| Customer payment evidence | `invoicing` | Direct tenant/customer | Payment-recording service |
| Payment allocation | `invoicing` | Payment and invoice/credit same tenant | Allocation service |
| Outstanding balance/statement | `invoicing` | Derived from authoritative records | Query/reconciliation service |
| Rendered invoice artifact | `invoicing` | Invoice/credit tenant | Document service |
| Customer/contact master | `crm` | Same-tenant reference | Snapshot service only |
| Sales source | `sales` | Same-tenant source reference | Idempotent invoice-request contract |

Accounting, E-Invoicing, Banking, and VAT consume versioned facts through explicit contracts; they do not mutate invoice records.

## 5. Data Model and Financial Requirements

Conceptual entities: `CustomerInvoice`, `CustomerInvoiceLine`, `InvoiceSequence`, `InvoiceNumberReservation`, `CreditNote`, `CreditNoteLine`, `CustomerPayment`, `PaymentAllocation`, `InvoiceDocument`, and durable issue/correction/reconciliation operations.

- UUID public IDs plus explicit tenant and approved legal-entity ownership.
- Same-tenant customer, contact, source, invoice, credit, payment, allocation, user, and file relationships.
- Draft version, status, source/idempotency reference, document number, issue/due dates, currency, calculation/policy version, terms, totals, balance, timestamps, and correction relationships.
- Lines snapshot description, quantity, unit, unit price, discount, tax classification/result if approved, subtotal, tax, total, source item ID, and calculation inputs.
- Issuance snapshots issuer/customer names, addresses, identifiers, currency, terms, lines, totals, and applicable policy references. Current master data never changes the snapshot.
- Monetary fields use PostgreSQL `NUMERIC`/Python `Decimal`; precision, scale, ranges, rounding stages, and currency registry are approved before migration.
- Database constraints protect status combinations, amount ranges, allocation/currency consistency, tenant relationships, unique numbering scope, idempotency/source uniqueness, and correction limits where enforceable.
- Hard deletion of issued/finalized invoices, credit notes, allocated payments, or their audit/document relationships is prohibited through ordinary workflows.

## 6. Workflows and States

### 6.1 Invoice draft and calculation

Conceptual states: `DRAFT`, `PENDING_APPROVAL`, `APPROVED`, `ISSUING`, `ISSUED`, `PARTIALLY_PAID`, `PAID`, `CANCELLATION_PENDING`, `CANCELLED`, `CREDITED_PARTIALLY`, and `CREDITED_FULLY`, subject to policy. Payment/credit condition may be derived rather than conflated with issuance state.

Draft mutation validates tenant/customer/source/lines, parses decimals safely, resolves approved policy, calculates on the server, and stores reproducible inputs/results. Missing tax, currency, numbering, or calculation policy blocks issue.

### 6.2 Numbering and issue

The numbering service owns a documented tenant/legal-entity/document-type/series scope. Under a transaction and concurrency control it validates approval, recalculates, assigns/reserves a unique number according to approved gap policy, freezes the snapshot, changes authoritative state, writes audit/outbox intent, and commits atomically. A rollback cannot leave an issued partial document; number gaps are handled by explicit policy and evidence, never hidden reuse.

Repeated issue with the same idempotency key returns the original result; different payload reuse conflicts. Concurrency yields one authoritative issue.

### 6.3 Credit notes and corrections

A credit note references an eligible issued invoice and snapshots its own reason, lines, amounts, policy, issue number/date, and approval. Total credits cannot exceed eligible remaining amounts unless a specifically approved exception exists. Original issued values remain unchanged. Cancellation/replacement and credit behavior, including downstream tax/accounting/e-invoicing consequences, must be approved before activation.

### 6.4 Customer payments and allocations

P03 records payment evidence such as method category, tenant/customer, date, amount/currency, external reference, safe metadata, and status. It is not authoritative bank settlement. Allocation applies an available payment amount to eligible invoice balances within the same tenant/customer/currency and approved date policy. Repetition/concurrency cannot over-allocate. Reversal/unallocation preserves original evidence and reason.

Balances equal issued eligible amounts less valid credits and allocations under a documented equation. Stored accelerators, if used, reconcile to authoritative records and are not independent truth.

### 6.5 Document generation

Generate from the immutable authoritative snapshot, not current CRM/configuration. Rendering is idempotent and may be asynchronous; failure does not reverse issuance. Artifacts are private, content-typed, integrity-hashed where approved, access-checked at download, replaceable only by a versioned regeneration record, and retained under approved policy.

## 7. Business Rules

| ID | Requirement | Verification |
|---|---|---|
| INVM-001 | ERP invoices and P02 SaaS billing share no models, sequences, permissions, services, or balances | Boundary tests |
| INVM-002 | Server is authoritative for invoice/credit/payment/allocation calculations and state | Tamper tests |
| INVM-003 | Decimal, currency, precision, tax-source, discount, rounding, and residual policies are explicit and versioned | Financial tests |
| INVM-004 | Invoice numbering is unique in approved scope and safe under concurrency/retry/rollback | Database/concurrency tests |
| INVM-005 | Issue commits one immutable snapshot or no authoritative document | Transaction tests |
| INVM-006 | Issued protected fields cannot be silently edited or deleted through any ordinary path | Immutability tests |
| INVM-007 | Corrections preserve original and linked corrective records and cannot exceed policy limits | Credit tests |
| INVM-008 | Payment evidence and allocations are tenant/customer/currency valid, idempotent, and reconcilable | Allocation tests |
| INVM-009 | Current master/configuration changes do not rewrite historical documents or totals | Historical tests |
| INVM-010 | Rendered artifacts exactly represent the stored snapshot and remain private/authorized | Document/file tests |
| INVM-011 | Missing or unverified tax, legal, e-invoicing, accounting, or retention rules fail closed for affected behavior | Negative/readiness tests |
| INVM-012 | Material lifecycle, correction, payment, allocation, export, and privileged access is audited | Audit tests |

## 8. Tenant Isolation, Security, and Sensitive Data

All request, service, task, report, statement, export, cache, file, admin, and reconciliation paths derive trusted tenant context and validate same-tenant relationships. Use RLS defense where approved. Error/search behavior must not confirm another tenant’s object existence. Protect against IDOR, mass assignment of totals/status/tenant, stored XSS, template injection, CSV/formula injection, unsafe uploads, SSRF in document assets, and unbounded report generation.

Invoice/customer/payment details are sensitive business data. Never log full documents, addresses, tax identifiers, bank/payment evidence, access links, provider payloads, or secrets. Support and bulk export require purpose, narrow scope, audit, and bounded retention.

## 9. Entitlements and Degraded Access

`INVOICING` entitlement and relevant user permission are both required. Suspension/expiry denies new issue, credit, and payment operations by default. Approved read/export, customer remediation, or legally/integrity-required correction may be explicitly allowed and audited. Deactivation does not delete documents or prevent required retention/recovery.

## 10. Integrations and Events

- CRM: fetch validated customer snapshot; tolerate later merge/retirement without rewriting issued history.
- Sales: consume idempotent invoice request and return stable invoice/operation reference.
- P04 E-Invoicing: publish finalized invoice/credit facts and accept provider status only in its own domain; P03 does not infer provider compliance.
- P05 VAT/Accounting: consume versioned financial facts; Accounting owns postings, periods, and ledger references.
- P09 Banking: reconcile bank transactions to P03 customer-payment evidence through an explicit contract.

Use transactional outbox for issued/corrected/payment-allocation facts whose loss is material. Consumers are idempotent and version-tolerant. Reconciliation detects source-to-invoice, invoice-to-credit/allocation, artifact, outbox, and later downstream mismatches.

## 11. UI, API, Reports, Imports, and Exports

Django/HTMX screens cover draft, calculation review, approval, issue confirmation, history, credits, payments, allocation, balance/statement, document access, and reconciliation. UI clearly distinguishes draft, issued, credited, cancelled, payment, and bank-unreconciled concepts. APIs follow ADR-020 and represent decimals as strings.

Reports/statements define status/date/currency/credit/allocation semantics and never aggregate currencies without approved conversion. Imports may create drafts or payment evidence only through previewed, bounded, idempotent services; they cannot import issued status or bypass numbering/approval. Exports/documents are private, audited, formula-safe, and retention-controlled.

## 12. Regulatory and Financial Readiness

This specification does not establish UAE VAT rates, mandatory invoice/credit-note fields, tax point, numbering/gap rules, language, retention, e-invoicing applicability/deadlines, or legal acceptance of electronic documents. Before commercial issuance, a dated source register and qualified review must approve applicable policy versions. Unsupported rules remain disabled and limitations are visible.

## 13. Operations, Migration, and Recovery

Monitor issue/number contention, calculation exceptions, immutable-field attempts, over-credit/allocation conflicts, document failures, outstanding reconciliation, outbox age, and privileged operations. Runbooks cover failed issuance transaction, artifact regeneration, sequence incident, incorrect draft vs issued correction, duplicate payment, allocation reversal, restore reconciliation, and downstream outage.

Migrations preserve issued snapshots and identifiers; precision changes require before/after totals and recovery evidence. Backup/restore verifies counts and hashes, per-currency totals, balances, sequence high-water marks/reservations, correction/payment links, files, outbox, and audit.

## 14. Acceptance Criteria, Tests, and Evidence

Acceptance criteria are `INVM-001`–`INVM-012` and P03-AC-007–020. Required tests are P03-TST-041–152 as applicable. Evidence is P03-EV-002, 006–013 in the [P03 matrix](../02-phases/P03_CRM_SALES_INVOICING/P03_TRACEABILITY_AND_TEST_MATRIX.md). Automated tests use synthetic data and never create real external payments or regulatory submissions.

## 15. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| INV-DEC-001 | Invoice/credit numbering scope, format, gaps, cancellation, and recovery | Product/Finance/Operations/qualified UAE reviewer | P03-T07 | Separate tenant/legal-entity/type series; never reuse issued numbers; document gaps with evidence |
| INV-DEC-002 | Supported currency, precision, discount/tax calculation, rounding, and residual rules | Product/Finance/Tax specialist | P03-T06 migration/issue | Start with explicitly approved currencies/policies; no implicit UAE tax rule |
| INV-DEC-003 | Mandatory fields, language/layout, delivery, retention, and correction/legal-document policy | Product/Finance/Legal/Tax | Commercial issue/document activation | Validate authoritative current UAE sources and version policy |
| INV-DEC-004 | Customer payment evidence, method, reversal, allocation, and reconciliation scope | Product/Finance/Operations | P03-T09 | Treat as receivables evidence; Banking remains authoritative for bank reconciliation |
| INV-DEC-005 | Initial accounting and e-invoicing handoff contracts | Architecture/Finance | P04/P05 integration | Publish immutable versioned facts; do not couple P03 to provider or ledger internals |

## 16. Implementation Prompt

Use [P03 orchestration](../04-agents/phase-prompts/P03_CRM_SALES_INVOICING.md) and P03-T06–T10 in [P03 bounded tasks](../04-agents/phase-prompts/P03_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest.
