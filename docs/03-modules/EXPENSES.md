# EXPENSES — Expense Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-EXPENSES-001 |
| Status | APPROVED CONTRACT BASELINE; EXPANDED IMPLEMENTATION DETAIL PROPOSED — EXPENSE/REIMBURSEMENT POLICY REQUIRED |
| Owning phase / app | P08 / `expenses` |
| Domain owner | Expense Management |
| Commercial module | Yes |
| Tenant-owned data | Yes |
| Readiness | Expanded under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`; sections 4–14 are PROPOSED and unapproved |

## 1. Purpose and Boundary

Own business expense claims, lines, private receipt links, policy snapshots, approval and reimbursement evidence under `EXP-001` and [P08-SPEC-001](../02-phases/P08_PROJECTS_EXPENSES_ASSETS/P08_PHASE_SPECIFICATION.md). HRMS and Users own claimant identity; Projects owns project references; Accounting owns ledger and VAT posting; Payroll and Banking own approved settlement routes.

Governing sources: `EXP-001`, P08-SPEC-001, ADR-003–ADR-006, ADR-010, ADR-011, ADR-013–ADR-015, ADR-018, ADR-019, `ARCH-SEQ-001`, `ARCH-NOTIFY-001`, `ARCH-MIGRATION-001`, `QUAL-PRIV-001`, `QUAL-THREAT-001`, `PROD-REPORTS-001`.

Corporate-card feeds, travel booking, cash advances, authoritative OCR, per-diem tax policy and direct payment initiation are excluded until approved.

## 2. Actors and Authorization

| Actor | Permitted scope |
|---|---|
| Claimant | Prepare and submit own claims |
| Delegate | Prepare claims for a named claimant under approved delegation |
| Manager | Review and approve claims within organizational and amount scope |
| Expense reviewer | Policy compliance review before approval |
| Finance preparer | Prepare accounting requests for approved claims |
| Reimbursement reconciler | Confirm settlement evidence and resolve exceptions |
| Auditor | Read-only evidence review |
| Purpose-bound support | Time-bounded, audited privileged access under ADR-018 |

Concrete permission codenames, satisfying `RDY-004`:

`expenses.view_own_claim`, `expenses.add_claim`, `expenses.change_own_draft_claim`, `expenses.submit_claim`, `expenses.view_team_claim`, `expenses.review_claim`, `expenses.approve_claim`, `expenses.reject_claim`, `expenses.return_claim`, `expenses.override_policy`, `expenses.prepare_posting`, `expenses.prepare_reimbursement`, `expenses.confirm_settlement`, `expenses.reverse_claim`, `expenses.view_receipt`, `expenses.configure_policy`, `expenses.export_expense_data`, `expenses.view_all_claims`.

Claim preparation, approval, policy override, accounting request, reimbursement preparation, settlement confirmation and bulk export are separate. A maker cannot approve their own claim except under an explicitly approved and audited exception.

## 3. Domain Ownership

| Record / capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Expense policy and category | `expenses` | Direct tenant | Policy service |
| Claim, line, approval record | `expenses` | Direct tenant and claimant | Claim and approval services |
| Receipt file reference | `expenses` | Claim tenant | Document service under ADR-019 |
| Posting and reimbursement operation | `expenses` | Claim tenant | Durable operation services |
| Claimant identity | `hrms` / `users` | Same-tenant reference | Snapshot read only |
| Project reference | `projects` | Same-tenant reference | Reference contract |
| Ledger entry and VAT treatment | `accounting` / `vat` | Same-tenant reference | Accounting contract |
| Bank settlement | `banking` | Same-tenant reference | Banking contract |

## 4. Data Model Requirements

Conceptual entities: `ExpensePolicy`, `ExpenseCategory`, `ExpenseClaim`, `ExpenseLine`, `ExpenseReceipt`, `ExpenseApproval`, `ExpensePostingOperation`, `ExpenseReimbursementOperation`, `ExpenseReconciliationFinding`.

Field-level requirements satisfying `RDY-001`:

| Entity | Required attributes |
|---|---|
| `ExpensePolicy` | UUID id; tenant FK; version; effective from and to dates; approval rules; limit definitions; required-evidence rules; immutable once referenced by a submitted claim |
| `ExpenseCategory` | Tenant FK; code unique per tenant; name; optional default account reference; optional tax treatment reference; active flag |
| `ExpenseClaim` | UUID id; tenant FK; claimant reference; optional delegate reference; claim number per `ARCH-SEQ-001`; `status`; submission date; period; currency; `NUMERIC` total net, tax and gross; referenced policy version; optional project reference; created and updated timestamps and actors |
| `ExpenseLine` | Claim FK; category FK; expense date; description; `NUMERIC` net, tax and gross amounts; currency; optional original currency, rate basis and base-currency equivalent; optional project reference; receipt reference; policy-evaluation result |
| `ExpenseReceipt` | Claim or line FK; private storage reference; content type; byte size; SHA-256 checksum; uploaded-at and uploader; scan status; version |
| `ExpenseApproval` | Claim FK; approver reference; decision; decided-at; reason; approval level; stale-approval guard token; append-only |
| `ExpensePostingOperation` | Claim FK; idempotency key; requested payload version; status; attempt history; resulting ledger reference where returned |
| `ExpenseReimbursementOperation` | Claim FK; route; idempotency key; status including an explicit uncertain state; attempt history; settlement evidence reference |
| `ExpenseReconciliationFinding` | Tenant FK; scope; detected-at; finding type; amounts; resolution state |

Constraints: UUID primary keys; mandatory tenant ownership; `NUMERIC`/`Decimal` for every monetary value with precision, scale and rounding approved before migration per ADR-013; check constraints so line amounts reconcile to claim totals and gross equals net plus tax; same-tenant foreign keys for claimant, approver, project, receipt and operations; unique claim number in its approved scope; unique idempotency key per operation type; no hard deletion of an approved claim, approval record, receipt or operation through any ordinary path.

## 5. Workflows and States

| Record | States |
|---|---|
| `ExpenseClaim` | `DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`, `RETURNED`, `REIMBURSEMENT_PREPARED`, `REIMBURSEMENT_IN_PROGRESS`, `SETTLED`, `EXCEPTION`, `REVERSED` |
| `ExpensePostingOperation` | `PENDING`, `SENT`, `CONFIRMED`, `FAILED`, `UNCERTAIN` |
| `ExpenseReimbursementOperation` | `PREPARED`, `IN_PROGRESS`, `SETTLED`, `FAILED`, `UNCERTAIN` |

Permitted claim transitions: `DRAFT`→`SUBMITTED`; `SUBMITTED`→`UNDER_REVIEW`/`RETURNED`; `UNDER_REVIEW`→`APPROVED`/`REJECTED`/`RETURNED`; `APPROVED`→`REIMBURSEMENT_PREPARED`; `REIMBURSEMENT_PREPARED`→`REIMBURSEMENT_IN_PROGRESS`; `REIMBURSEMENT_IN_PROGRESS`→`SETTLED`/`EXCEPTION`; `APPROVED` or later→`REVERSED` only by an authorized linked reversal. `REJECTED` and `SETTLED` are terminal except through reversal. Transition authority is the permission named in section 2; each transition writes an append-only approval or operation record.

Approved records are immutable per ADR-011; correction or cancellation creates a linked version or reversal and never edits the approved claim. An `UNCERTAIN` reimbursement outcome is never presented as settled.

## 6. Business Rules

| ID | Rule / verification |
|---|---|
| EXPM-001 | Claimant type/entity/eligibility and policy version are explicit; applicability tests |
| EXPM-002 | Decimal line/tax/gross/currency totals are server-derived and reproducible; golden tests |
| EXPM-003 | Required evidence, limits, dates, categories and exceptions use approved policy; boundary tests |
| EXPM-004 | Duplicate candidates use receipt checksum/vendor/date/amount/reference without unsafe auto-rejection; duplicate tests |
| EXPM-005 | Maker-checker, stale approval and concurrent transition controls prevent unauthorized approval; workflow tests |
| EXPM-006 | Approved claims cannot be silently edited/deleted; corrections remain linked; immutability tests |
| EXPM-007 | Accounting/VAT and reimbursement operations are versioned/idempotent/reconciled; contract tests |
| EXPM-008 | Provider/local statuses never fabricate acceptance or settlement; uncertainty tests |
| EXPM-009 | Receipts are private, scanned, checksummed, versioned and authorized at download; file tests |
| EXPM-010 | Field/object/export/support permission, entitlement, tenant isolation and RLS cover every path; security tests |
| EXPM-011 | Logs/audit exclude receipt content, bank details and excessive personal data; redaction tests |
| EXPM-012 | Migration/restore reconciles claims, approvals, postings, reimbursements, files and audit; recovery tests |
| EXPM-013 | An unapproved policy, VAT treatment or reimbursement route disables the dependent behavior instead of defaulting; fail-closed tests |
| EXPM-014 | Claim numbering is unique, concurrency-safe and rollback-safe per `ARCH-SEQ-001`; numbering tests |
| EXPM-015 | Foreign-currency lines record original currency, rate basis and base-currency equivalent; conversion tests |

## 7. Tenant Isolation, Security and Sensitive Data

Every request, service, task, report, export, cache, file and administrative path derives trusted tenant context and validates same-tenant relationships, with row-level security as defence in depth. Protect against insecure direct object reference to another claimant's claim or receipt, mass assignment of status, totals, approver or tenant, formula injection in exports, unsafe uploads and server-side request forgery in document handling.

Applicable threats from `QUAL-THREAT-001`, satisfying `RDY-010`: `THR-010`, `THR-011`, `THR-014` artifact authorization, `THR-034` race producing duplicate reimbursement, `THR-035` sensitive data in logs, `THR-044` malicious uploaded receipt, `THR-045` storage authorization, `ABU-03` payment diversion through altered bank details, `ABU-05` self-approval, `ABU-07` bulk extraction, `ABU-09` duplicate payment through retry.

Data classification and retention, satisfying `RDY-009`: claim and line data is `C2`; claimant identity is `C3`; receipt images and any reimbursement bank detail are `C4`. Retention classes are `RET-01` for claims forming part of the accounting record, `RET-07` for bank detail, and `RET-12` for generated artifacts, under `QUAL-PRIV-001`. Receipt content, bank details and full personal data never appear in logs, metrics, traces or notifications.

## 8. Entitlements and Degraded Access

`EXPENSES` entitlement and the relevant user permission are both required on every path. Suspension or expiry denies new claims, approvals and reimbursement preparation by default; approved read, export and legally required correction may be explicitly allowed and audited. Deactivation never deletes claims, receipts or settlement evidence, and never prevents required retention or recovery.

## 9. Integrations and Events

- HRMS and Users: read a validated same-tenant claimant snapshot; later employee change must not rewrite submitted claim history.
- Projects: validate a same-tenant project reference and its chargeability under approved policy.
- Accounting and VAT: publish versioned approved-claim facts; Accounting owns postings, periods and ledger references, and VAT owns the authoritative tax treatment.
- Payroll or Banking: request reimbursement through the approved route only; this module records evidence and never initiates a payment directly.
- Reporting: expose claim facts for `RPT-605` and `RPT-606`.

Durable intent and the transactional outbox per ADR-010 protect posting and reimbursement requests. Every outbound request carries a stable idempotency key per `ARCH-API-001` section 14. Reconciliation detects claim-to-posting, claim-to-reimbursement, receipt-to-claim and settlement-to-bank mismatches.

## 10. UI, API, Reports, Imports and Exports

Django and HTMX surfaces cover claim preparation with a line editor, receipt upload, policy warnings, submission, review and approval queues, reimbursement preparation, settlement confirmation, exception handling and reconciliation review. Surfaces use the line-item editor, file upload, form error summary, status badge, confirmation dialog and bulk action bar components in `ARCH-UI-001`. Approval and reversal require explicit confirmation naming the claim and effect per `UIX-036`.

Reports registered in `PROD-REPORTS-001`: `RPT-605` expense claim register and status, `RPT-606` expense analysis by category including policy exceptions.

Imports follow `ARCH-MIGRATION-001`: claim and category master import through previewed, bounded, idempotent staged services. Import cannot create an approved or settled state and cannot bypass numbering or approval. Exports are private, authorized, formula-safe, checksummed and audited as a disclosure where they contain `C3` or higher data.

Document types registered in `ARCH-SEQ-001`, satisfying `RDY-007`: expense claim number, allocated at submission, tenant and period scoped; and expense reimbursement reference where a route requires one. Neither is declared gapless unless `DEC-SEQ-003` requires it.

Notifications registered in `ARCH-NOTIFY-001`, satisfying `RDY-008`: claim submitted, returned for correction, approved, rejected, reimbursement prepared, settled, settlement exception, and approval pending reminder. Approval-workflow notifications are digest-eligible; a settlement exception is not digested.

## 11. Regulatory and Financial Readiness

This module establishes no VAT recoverability rule, per-diem treatment, allowable-expense rule or payroll tax position. Input VAT treatment on expenses is owned by `MOD-UAE-VAT-001` and remains disabled here until `DEC-TAX-001` and `DEC-EXP-001` are approved. Retention periods are configuration taken from `QUAL-PRIV-001` and remain unresolved pending `DEC-PRIV-005`; no period is asserted here, per `RDY-012`.

## 12. Operations, Migration and Recovery

Monitor duplicate candidates, stale approvals, policy overrides, high-risk amounts and categories, failed postings, uncertain reimbursements, receipt access, scan failures and export volume. Runbooks cover a failed posting operation, an uncertain reimbursement requiring manual confirmation, a duplicate claim discovered after approval, an authorized reversal, a receipt scan failure and restore reconciliation.

Migration preserves claims, approvals, receipt references and operation history; a precision change requires before-and-after totals. Restore verifies claim counts and per-currency totals, approval chains, receipt checksums, operation idempotency keys, outbox age and audit completeness.

## 13. Acceptance Criteria, Tests and Evidence

Acceptance criteria are `EXPM-001`–`EXPM-015` and the applicable criteria in `P08-AC-001`–`P08-AC-018`. Required tests are the expense scenarios within `P08-TST-001`–`P08-TST-171`. Evidence records are `P08-EV-004`–`P08-EV-009` in the [P08 matrix](../02-phases/P08_PROJECTS_EXPENSES_ASSETS/P08_TRACEABILITY_AND_TEST_MATRIX.md).

All scenarios are `NOT_RUN`. Tests use synthetic claimants, synthetic receipts and the documented invalid bank-detail patterns in `QUAL-TESTDATA-001`; no test initiates a real payment.

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| DEC-EXP-001 | Claimant linkage, policy and approval model, VAT treatment, reimbursement route, duplicate handling and retention behavior | Product / Finance / Operations / Tax | Schema work and any reimbursement activation | Begin with employee claimants, single approval level and manual reimbursement evidence; keep VAT recovery disabled until the tax position is approved |
| DEC-SEQ-003 | Reset policy for the claim number series | Finance domain owner | Numbering implementation | Annual reset on a new scope key |
| DEC-PRIV-005 | Retention periods applicable to claims, receipts and bank detail | Tax and finance specialists | Automated disposal | Confirm with dated sources; retain under obligation until then |
| DEC-GOV-007 | Phase-entry specification gate covering this expansion | Product Owner / Architecture | P08 implementation authorization | Approve the gate and this expanded specification together |

## 15. Implementation Prompt

Use the [P08 orchestration prompt](../04-agents/phase-prompts/P08_PROJECTS_EXPENSES_ASSETS.md) and the expense tasks in the [P08 bounded task prompts](../04-agents/phase-prompts/P08_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest; no implementation is authorized by this document.
