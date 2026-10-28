# ADR-011: Financial Data Integrity and Immutable Posted Entries

| Field | Details |
|---|---|
| ADR ID | ADR-011 |
| Title | Financial Data Integrity and Immutable Posted Entries |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / Finance Domain Owner |
| Reviewers | Architecture, Finance, Accounting, Security, Database, Product |
| Affected Phases | P03–P12 |
| Related ADRs | ADR-002, ADR-003, ADR-004, ADR-005, ADR-010, ADR-012, ADR-013, ADR-014, ADR-018 |
| Related Requirements | INV-001–INV-005, ACC-001–ACC-005, REP-002, AUD-001, NFR-006–NFR-007, NFR-009 |
| Related Documents | `MASTER_PRODUCT_SPECIFICATION.md`, `PRODUCT_REQUIREMENTS.md`, `DATABASE_DESIGN.md`, `SYSTEM_ARCHITECTURE.md`, `API_STANDARDS.md`, `EVENT_AND_TASK_PROCESSING.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

Invoices, credit notes, journal entries, payments, inventory valuation, payroll postings, bank reconciliation, and tax records become financially authoritative at defined lifecycle points. Ordinary CRUD behavior is unsafe after that point: changing or deleting a posted entry can alter historical balances without leaving an adequate correction trail.

The platform needs a common integrity contract while leaving accounting policy, tax treatment, document correction rules, and statutory requirements to approved domain specifications and qualified review.

## 2. Decision Drivers

- Reproducible ledgers and financial reports.
- Balanced, atomic, tenant-scoped posting.
- Traceable corrections rather than silent history rewrites.
- Duplicate-posting and concurrency protection.
- Period controls and separation of duties.
- Reliable links from source documents to accounting consequences.
- Auditable failure, reversal, reconciliation, and migration behavior.

## 3. Options Considered

### Option A: Controlled posting with append-oriented posted records

Drafts may be edited. Posting validates and commits an immutable financial snapshot. Corrections use linked reversal, credit-note, adjustment, or cancellation workflows.

**Advantages:** strong traceability, reproducible reporting, and explicit correction semantics.

**Disadvantages:** more workflow states, storage, services, and user training.

### Option B: Editable posted records with audit history

**Advantages:** operational convenience.

**Disadvantages:** audit history does not guarantee balances were never silently changed; downstream reports and external submissions can diverge.

### Option C: Database append-only ledger for every business document

**Advantages:** strongest uniform immutability.

**Disadvantages:** unnecessary complexity for drafts and non-financial metadata; difficult business workflows.

### Option D: Event sourcing for all financial domains

**Advantages:** complete state reconstruction in theory.

**Disadvantages:** substantial modelling, projection, migration, and operational complexity not justified for the initial platform.

## 4. Decision

Use controlled lifecycle transitions and append-oriented financial history. Draft records may change under authorization. Once a record becomes issued, posted, finalized, reconciled, or otherwise financially authoritative under its domain policy, protected financial fields must not be silently edited or deleted.

Corrections must use an approved linked transaction such as a reversal, credit note, adjustment, cancellation record, or reopening workflow. “Immutable” means protected business meaning and evidence are preserved; it does not prohibit tightly controlled updates to non-financial operational metadata when those updates cannot change the historical accounting interpretation.

### 4.1 Authoritative lifecycle

Each financial document type must define:

- Draft and review states.
- Required approvals.
- The transition that makes it authoritative.
- Fields frozen by that transition.
- Permitted post-finalization metadata changes.
- Correction and reversal mechanisms.
- Effects on accounting, tax, e-invoicing, inventory, payments, and reports.
- Cancellation and void semantics.

Status names may differ by domain, but their meaning must be explicit and testable.

### 4.2 Posting service

Financial posting must occur through an owning application service inside an explicit PostgreSQL transaction. The service must validate, as applicable:

1. Tenant and legal-entity ownership.
2. Actor permission, approval, and separation of duties.
3. Source-document state and entitlement policy.
4. Accounting period eligibility.
5. Account, dimension, and currency validity.
6. Debit-credit balance under ADR-013.
7. Required numbering and source references.
8. Duplicate and idempotency protection.
9. Concurrency preconditions.
10. Required audit and outbox records.

The record is not posted until the transaction commits successfully.

### 4.3 Double-entry integrity

Every posted journal entry must balance according to the approved base-currency and rounding policy. A row-level check alone cannot validate an aggregate across lines; the posting service must calculate and lock the relevant entry state, while database constraints protect line validity and prohibited lifecycle changes.

Unbalanced entries must fail without partial posting.

### 4.4 Source and ledger relationship

Source domains own their business documents. `accounting` owns posted journal entries. Source modules request posting through an explicit accounting contract and store stable references to the result.

The accounting ledger must not depend on mutable source fields to reproduce a posted entry. Required descriptions, currency, amounts, tax classification, exchange-rate references, and source identity must be snapshotted or otherwise historically resolvable.

### 4.5 Corrections and reversals

A reversal must:

- Reference the original posted record.
- Carry equal and opposite financial effect under the approved policy.
- Record reason, actor, time, and approval evidence.
- Use an eligible posting date and open period.
- Preserve both original and corrective entries.
- Be idempotent and protected from duplicate execution.

A correction requiring new values must normally create a new adjusted transaction in addition to the reversal. Whether an issued invoice requires a credit note, cancellation, replacement, or another legal document remains a domain and regulatory decision.

### 4.6 Period controls

Posting into a closed period is denied. Closing and reopening are controlled operations with permission, approval, audit, and reconciliation evidence. A UI flag alone is insufficient; posting services must enforce period state transactionally.

Backdated corrections and exceptional reopening require an approved accounting policy.

### 4.7 Deletion and retention

Posted entries, issued documents, approved payroll results, completed reconciliations, and their audit relationships must not be hard-deleted through ordinary product workflows. Subscription expiry or module disablement does not delete them.

Retention and legally required erasure or anonymization must use approved record-category policies that preserve financial integrity and required evidence.

### 4.8 Concurrency and idempotency

Posting, invoice numbering, payment allocation, period closing, reversal, and reconciliation require explicit locking or optimistic concurrency plus database constraints. Stable business idempotency keys must prevent repeated requests, task retries, or provider callbacks from posting twice.

### 4.9 Audit and evidence

Record the actor or system identity, tenant, legal entity, source, approvals, posting time, policy/rule versions, correlation identifiers, and correction relationships required to explain the financial outcome. Audit evidence must not contain unnecessary secrets or full sensitive payloads.

## 5. Rationale

Controlled posting separates editable work-in-progress from authoritative financial history. Linked corrections preserve the truth that an original transaction occurred while allowing the business to correct it transparently. Local PostgreSQL transactions and constraints provide a strong integrity boundary within the modular monolith.

## 6. Consequences

### Positive consequences

- Reproducible ledgers and reports.
- Traceable corrections and approvals.
- Safer retries and concurrent workflows.
- Clear integration point for source modules.

### Negative consequences and trade-offs

- More states, records, and workflow complexity.
- Corrections require domain-specific user experiences.
- Historical snapshots increase storage.
- Some exceptional regulatory corrections need specialist decisions.

### Risks and mitigations

- **Hidden mutation:** service restrictions, database permissions, triggers or constraints where justified, and integrity tests.
- **Duplicate posting:** idempotency keys, unique source references, and transaction locks.
- **Incorrect reversal date:** period validation and finance approval.
- **Ledger/source divergence:** reconciliation and stable source references.
- **Migration damage:** staged migrations, immutable-field checks, backups, and financial reconciliation.

## 7. Security and Tenant-Isolation Implications

- Posting and reversal require explicit permissions and tenant/legal-entity scope.
- Approval and posting may require separate actors where the approved control model demands it.
- Cross-tenant source or account references must be rejected at service and database levels.
- Privileged support access must not silently mutate posted data.
- Sensitive payroll, bank, and tax details require field-level access controls.

## 8. Data Integrity and Migration

- Protect authoritative status transitions and frozen fields.
- Use constraints for non-negative or mutually exclusive debit/credit values where the approved design requires them.
- Preserve source, reversal, and correction references.
- Backfills affecting posted data require before/after reconciliation totals and rollback evidence.
- Migration scripts must not regenerate historical values from current mutable configuration.

## 9. Operational Impact

Operations require monitoring for failed postings, duplicate-source conflicts, unbalanced drafts, stale approvals, closed-period attempts, reconciliation differences, and unauthorized mutation attempts. Recovery must restore consistent financial and audit state, not merely make the application start.

## 10. Implementation Requirements

1. Define lifecycle and frozen fields for every financial record type.
2. Implement one controlled posting service per owning domain or approved accounting interface.
3. Define reversal, adjustment, cancellation, and credit-note behavior in module specifications.
4. Add idempotency, concurrency, and unique source constraints.
5. Enforce period state and legal-entity scope.
6. Snapshot historically required values and rule versions.
7. Add financial reconciliation and immutable-field tests.
8. Protect posted records from ordinary admin and bulk-edit paths.

## 11. Validation and Acceptance Criteria

- [ ] Failed posting commits no partial financial state.
- [ ] Posted journal entries balance under ADR-013.
- [ ] Posted protected fields cannot be edited or hard-deleted through ordinary paths.
- [ ] Repeated posting and reversal requests are idempotent.
- [ ] Corrections preserve original and corrective records.
- [ ] Closed-period restrictions are enforced outside the UI.
- [ ] Cross-tenant and cross-legal-entity references are rejected.
- [ ] Ledger totals reconcile to authoritative posted entries.
- [ ] Historical reports do not change when current master data changes.
- [ ] Financial migrations include reconciliation and recovery evidence.

## 12. Alternatives Rejected

- Editable posted rows with audit history are rejected as insufficient integrity.
- Hard deletion as a correction mechanism is rejected.
- UI-only period and lifecycle controls are rejected.
- Event sourcing for all financial domains is rejected absent a justified requirement.
- Treating the source document as the accounting ledger is rejected.

## 13. References

- `docs/00-product/MASTER_PRODUCT_SPECIFICATION.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/API_STANDARDS.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Controlled posting with immutable protected fields and linked corrective transactions.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`. Specific accounting, tax, valuation, period-reopening, and correction policies still require finance/specialist approval.

This ADR does not approve specific accounting, tax, valuation, period-reopening, or document-correction policies. Those decisions block implementation of the affected financial workflows but do not block independent documentation.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial financial integrity and posted-entry decision accepted after standards review. |
