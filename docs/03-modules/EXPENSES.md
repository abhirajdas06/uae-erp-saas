# EXPENSES — Expense Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-EXPENSES-001 |
| Status | APPROVED SPECIFICATION — EXPENSE/REIMBURSEMENT POLICY REQUIRED |
| Owning phase / app | P08 / `expenses` |

## 1. Purpose and Boundary

Own business expense claims, lines, private receipt links, policy snapshots, approval and reimbursement evidence under `EXP-001` and P08-SPEC-001. HRMS/Users own claimant identity; Projects owns project references; Accounting owns ledger/VAT posting; Payroll/Banking owns approved settlement routes.

Corporate-card feeds, travel booking, cash advances, authoritative OCR, per-diem tax policy and direct payment initiation are excluded until approved.

## 2. Actors and Permissions

Claimant, delegate, manager, expense reviewer, approver, finance preparer, reimbursement reconciler, auditor and purpose-bound support. Claim preparation, approval, policy override, accounting request, reimbursement preparation, settlement confirmation and bulk export are separate; maker cannot approve their own claim except an explicitly approved exception.

## 3. Model and Workflow

`ExpensePolicy`, `ExpenseCategory`, `ExpenseClaim`, `ExpenseLine`, `ExpenseReceipt`, `ExpenseApproval`, `ExpensePostingOperation`, `ExpenseReimbursementOperation` and `ExpenseReconciliationFinding`.

Draft → submitted → under review → approved/rejected/returned → reimbursement prepared/in progress → settled or exception. Approved records are immutable; correction/cancellation creates a linked version or reversal.

## 4. Rules and Verification

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

## 5. Operations and Decisions

Monitor duplicate candidates, stale approvals, overrides, high-risk amounts/categories, failed postings, uncertain reimbursements, file access and export volume. `DEC-EXP-001` must approve claimant linkage, policy/approval, VAT, reimbursement route, duplicate and retention behavior.
