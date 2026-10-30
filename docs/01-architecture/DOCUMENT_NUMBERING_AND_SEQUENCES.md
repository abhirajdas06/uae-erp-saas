# Document Numbering and Sequence Allocation

| Property | Value |
|---|---|
| Document ID | ARCH-SEQ-001 |
| Status | APPROVED DOCUMENTATION BASELINE — NUMBERING POLICY AND STATUTORY CONFIRMATION REQUIRED |
| Owner | Product Architect / Finance domain owner |
| Governing decisions | ADR-011, ADR-014, ADR-002, ADR-004 |
| Related documents | `DATABASE_DESIGN.md`, `API_STANDARDS.md`, `../03-modules/UAE_VAT.md`, `../03-modules/UAE_EINVOICING.md`, `../03-modules/ACCOUNTING.md` |

## 1. Purpose and Boundary

Business document identifiers are externally visible, legally significant and frequently subject to tax-audit expectations. No existing document owns how they are allocated, formatted, made gapless, reset or protected under concurrency. This document owns that definition.

This document owns sequence definition, allocation semantics, concurrency behavior, formatting, reset policy, gap handling and the related tests. It does not own primary-key strategy, which remains with ADR-014; posted-record immutability, which remains with ADR-011; or statutory invoice content, which remains with the UAE VAT and e-invoicing module specifications.

A business document number is a distinct concept from a database primary key. Internal references always use the UUID primary key under ADR-014; the business number is a human- and audit-facing attribute and is never used as a foreign key.

## 2. Sequence Model

| ID | Requirement |
|---|---|
| SEQ-001 | A `NumberSequence` is defined per tenant, per document type, and per additional scope dimension the document type declares |
| SEQ-002 | A sequence definition records tenant, document type, scope key, prefix and suffix pattern, numeric width, current value, reset policy, gapless requirement, active period and approval provenance |
| SEQ-003 | Scope dimensions are limited to the declared set: tenant, document type, branch or establishment, fiscal year, period and series; an undeclared scope dimension requires an approved change |
| SEQ-004 | Every sequence is tenant-owned and tenant-scoped; no sequence, counter or cache is shared across tenants under any circumstances |
| SEQ-005 | Platform-level identifiers such as SaaS subscription invoice numbers are owned by the provider domain and are strictly separate from tenant ERP document numbers, per the mandatory separation in `../00-product/MASTER_PRODUCT_SPECIFICATION.md` section 6.3 |
| SEQ-006 | A document type declares whether its number is allocated at draft creation or at posting, confirmation or issue; the choice is recorded, not left to implementation convenience |
| SEQ-007 | Changing an active sequence definition requires an authorized change record and may never retroactively renumber an existing document |

## 3. Document Types Requiring Managed Sequences

| Family | Document types |
|---|---|
| Sales and invoicing | Quotation, sales order, proforma invoice, tax invoice, simplified tax invoice, credit note, debit note, delivery note, receipt |
| Procurement and inventory | Purchase requisition, purchase order, goods receipt, supplier invoice reference, stock movement, stock adjustment, stock transfer, stock count |
| Accounting | Journal entry, recurring journal, payment voucher, receipt voucher, contra entry, period-close record, revaluation entry |
| Banking and finance | Bank transaction batch, payment instruction, payment file, reconciliation statement |
| Payroll and HR | Payroll run, payslip, end-of-service settlement, wage protection file submission, leave record |
| Projects, expenses, assets | Project code, timesheet, expense report, expense claim, asset tag, asset disposal record |
| Platform | Tenant code, SaaS subscription invoice, SaaS credit note, dunning notice |

Each document type must appear in exactly one owning module specification with its declared allocation point, scope dimensions and gapless requirement before implementation of that module.

## 4. Allocation Semantics

| ID | Requirement |
|---|---|
| SEQ-010 | Allocation occurs inside the database transaction that persists the owning record, so a committed document always holds its allocated number and an allocation is never visible without its document |
| SEQ-011 | Allocation serializes concurrent requests for the same sequence scope using a database-level lock or an equivalent atomic primitive; application-level locking alone is insufficient |
| SEQ-012 | A uniqueness constraint on tenant, document type, scope key and number enforces non-duplication at the database level; application checks are defense in depth, not the control |
| SEQ-013 | An allocated number is never reused after commit, including after cancellation, reversal or void |
| SEQ-014 | Allocation is idempotent with respect to a retried request: a retry carrying the same idempotency key under `API_STANDARDS.md` section 14 returns the originally allocated number and never consumes a second value |
| SEQ-015 | A background task, import, migration or integration callback that creates a numbered document uses the same allocation service as interactive requests; no alternative numbering path exists |
| SEQ-016 | Allocation performance under concurrency is bounded and measured; a sequence hot spot is an operational defect, not an accepted behavior |
| SEQ-017 | Pre-allocating or caching unused numbers in application memory is prohibited for any sequence declared gapless |

## 5. Gapless Numbering

| ID | Requirement |
|---|---|
| SEQ-020 | A sequence declared gapless must produce an unbroken ascending series within its scope; a rolled-back transaction must not consume a value |
| SEQ-021 | A gapless sequence therefore allocates at the point of commit of the authoritative record and never at the point of draft creation |
| SEQ-022 | A document type whose statutory treatment is unconfirmed defaults to gapless and conservative behavior until `DEC-SEQ-002` records the confirmed requirement. For tax invoices specifically, `UAE-NUM-001` records that the evidenced obligation read on 29 October 2026 is a sequential number, or a unique number enabling identification and determinable order in a sequence, so the gapless default is conservative rather than minimal and already satisfies that wording |
| SEQ-023 | A cancelled or voided document in a gapless series retains its number and a cancellation status; the number is never freed, deleted or reassigned |
| SEQ-024 | Any detected gap in a gapless series raises an operational alert and produces an audit-reviewable record with cause analysis |
| SEQ-025 | A non-gapless sequence must explicitly record that gaps are acceptable, and the reason, in its owning module specification |

## 6. Format and Presentation

| ID | Requirement |
|---|---|
| SEQ-030 | A number format is composed from a bounded pattern of literal text, tenant or branch code, fiscal-year or period token and a zero-padded counter |
| SEQ-031 | The rendered number is stored as the authoritative displayed value alongside its numeric component; display is never recomputed from parts at read time |
| SEQ-032 | Numbers contain only characters from an explicit allowed set and are unambiguous in both left-to-right and right-to-left presentation, per `LOCALIZATION_AND_BILINGUAL_UI.md` L10N-024 |
| SEQ-033 | A number is language-independent and is never translated, transliterated or localized |
| SEQ-034 | Numeric width is sufficient for projected volume; exhaustion of a width is an alerted condition handled before it occurs, not by silent overflow |
| SEQ-035 | A number presented to an external party or regulator matches exactly the stored authoritative value and the value in any structured payload |

## 7. Reset and Period Behavior

| ID | Requirement |
|---|---|
| SEQ-040 | Reset policy is one of never, annual on fiscal-year change, or an approved alternative; the policy is a recorded property of the sequence |
| SEQ-041 | A reset creates a new scope key rather than resetting a counter in place, so historical series remain intact and queryable |
| SEQ-042 | Documents dated in a prior open period continue to draw from that period scope where the policy requires it; back-dating behavior is explicit, authorized and audited |
| SEQ-043 | A closed period cannot accept a newly numbered document; the period-close rules in `../03-modules/ACCOUNTING.md` govern |
| SEQ-044 | Fiscal-year configuration changes do not retroactively alter existing scope keys or numbers |

## 8. Security, Audit and Tenant Isolation

| ID | Requirement |
|---|---|
| SEQ-050 | Every sequence read, allocation and definition change is tenant-scoped at the query level and protected by database-level isolation under ADR-004 |
| SEQ-051 | A document number is not a secret, but it must not be a predictable key to another tenant's data; authorization is by object and tenant, never by number |
| SEQ-052 | A lookup by document number is scoped to the requesting tenant and returns a neutral not-found response for any number outside that tenant |
| SEQ-053 | Sequence definition changes, manual interventions and gap findings are written to the audit trail under `../03-modules/AUDIT_FOUNDATION.md` with actor, time, before and after values and reason |
| SEQ-054 | Manual assignment or override of a document number requires an explicit permission, a recorded reason and maker-checker approval where the document is financial |
| SEQ-055 | A restored or migrated tenant has its sequence current values reconciled against the maximum existing document number before write operations resume |

## 9. Acceptance and Tests

| ID | Verification |
|---|---|
| SEQ-TST-001 | Concurrent allocation requests for one scope produce no duplicate number under sustained parallel load |
| SEQ-TST-002 | A uniqueness violation is prevented by the database constraint when the application layer is bypassed |
| SEQ-TST-003 | A rolled-back transaction consumes no value in a gapless sequence |
| SEQ-TST-004 | A retried request with the same idempotency key returns the original number and consumes no second value |
| SEQ-TST-005 | Cancellation, reversal and void retain the original number and never free it |
| SEQ-TST-006 | Two tenants allocate identical numeric values independently with no interference or cross-tenant visibility |
| SEQ-TST-007 | A document-number lookup across a tenant boundary returns a neutral not-found response |
| SEQ-TST-008 | Annual reset produces a new scope key while preserving the prior series |
| SEQ-TST-009 | Back-dated and closed-period behavior matches the declared policy |
| SEQ-TST-010 | Format rendering, padding, width exhaustion alerting and bidirectional presentation behave as specified |
| SEQ-TST-011 | Background, import and integration creation paths use the same allocation service |
| SEQ-TST-012 | Restore and migration reconcile current values against existing maxima before resuming writes |
| SEQ-TST-013 | Manual override requires permission, reason and approval, and is fully audited |

All scenarios are `NOT_RUN` until the owning phase implements the capability.

## 10. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-SEQ-001 | Approve the number format pattern per document family, including branch and fiscal-year tokens | Product Owner / Finance |
| DEC-SEQ-002 | Confirm which document types carry a statutory sequential or gapless numbering expectation. Evidence is prepared: `UAE-NUM-001` to `UAE-NUM-003` in the regulatory source register record the article-level particulars read on 29 October 2026 for tax invoices, simplified tax invoices and tax credit notes. The specialist must confirm the complete particulars and decide whether gapless allocation is required, or whether identifiability with determinable order suffices per document family | Tax specialist |
| DEC-SEQ-003 | Approve the reset policy per document family | Finance domain owner |
| DEC-SEQ-004 | Approve whether manual number override is permitted at all, and for which document types | Product Owner / Finance |
| DEC-SEQ-005 | Approve branch or establishment scoping, including its interaction with multiple tax registration numbers | Tax specialist / Product Owner |

`DEC-SEQ-002` and `DEC-SEQ-005` are regulatory dependencies. This document asserts no statutory numbering requirement of its own. The article-level wording located for tax invoices is recorded as `UAE-NUM-001` to `UAE-NUM-003` in `../00-product/UAE_REGULATORY_SOURCE_REGISTER.md` section 5.2, with its extraction caveats; the conservative defaults in section 5 continue to apply until the named specialist records a dated confirmation. These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`.
