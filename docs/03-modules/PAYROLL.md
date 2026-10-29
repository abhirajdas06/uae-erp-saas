# PAYROLL — Payroll Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-PAYROLL-001 |
| Status | APPROVED SPECIFICATION — PAYROLL/WPS POLICY REQUIRED |
| Owning phase / app | P07 / `payroll` |

## 1. Purpose and Boundaries

Own effective-dated payroll configuration, input snapshots, calculations, approvals, finalized results, adjustments, payslips and approved WPS/payment-preparation evidence under `PAY-001`–`PAY-003`, P07-SPEC-001 and REG-HR-001.

HRMS owns employment/leave; Accounting owns ledger entries; banks/WPS agents own payment/settlement; pension/government systems own acceptance. Excluded until approved: universal end-of-service, pension, Emiratisation/Nafis, government filing, direct bank payment and unsupported jurisdictions/categories.

## 2. Actors and Permissions

Payroll configurator, input preparer, calculator, reviewer, approver/finalizer, payment/WPS preparer/approver, accounting reconciler, employee self-service, auditor and purpose-bound support. Configure, input, calculate, approve, finalize, correct, view sensitive, generate payslip, prepare/export WPS, post, reconcile and bulk export are separate with maker-checker.

## 3. Model and Immutable Results

Conceptual records: `PayrollCalendar`, `PayrollPeriod`, `PayrollRuleSet`, `PayrollComponent`, `EmployeePayrollAssignment`, `PayrollInput`, `PayrollRun`, `PayrollResult`, `PayrollResultLine`, `PayrollAdjustment`, `PayslipArtifact`, `PayrollPostingOperation`, `WPSOperation`, `WPSArtifact` and `PayrollReconciliationFinding`.

- Tenant/legal entity, employee/employment and approved ruleset scope is explicit.
- Rule/component assignments are effective-dated and unambiguous.
- Run snapshots employee/contract/compensation/leave/time/input/rule/currency versions and hashes.
- Authoritative amounts use Decimal and named proration/rounding stages.
- Finalized results/lines/payslips are protected; corrections create linked adjustment/off-cycle/reversal results.
- Source/version/purpose idempotency prevents duplicate result, posting or WPS preparation.

## 4. Workflows

Open period → collect/validate inputs → calculate/recalculate draft → review exceptions → approve → finalize → generate payslips → request accounting posting → prepare approved payment/WPS artefact → reconcile evidence → close. Stale changed inputs/rules/employee snapshot invalidate approval.

Finalization locks/revalidates the run, proves gross/deduction/net equations and component constraints, writes immutable results/audit/outbox atomically, or commits nothing. Negative net, deductions, retroactivity, proration, unpaid leave, overtime, end-of-service and pension behavior exist only when explicitly approved.

WPS preparation uses an exact versioned agent contract, private encrypted/checksummed artifact, approval, stable operation and response/reconciliation. `PREPARED`, `EXPORTED`, `UPLOADED`, `ACCEPTED`, `DISBURSED`, `REJECTED`, `UNCERTAIN` and `SETTLED` are enabled only when supported by evidence; local state never fabricates settlement.

## 5. Business Rules

| ID | Rule / verification |
|---|---|
| PAYM-001 | Only approved effective employer/employee/ruleset combinations calculate; applicability tests |
| PAYM-002 | Payroll snapshot is complete/versioned and current changes do not drift result; historical tests |
| PAYM-003 | Decimal component/proration/rounding/gross/deduction/net is deterministic; golden/property tests |
| PAYM-004 | Approval/finalization is transactional, maker-checker and stale-safe; workflow tests |
| PAYM-005 | Finalized pay/payslip cannot be silently edited/deleted; correction remains linked; immutability tests |
| PAYM-006 | Retry/concurrency cannot duplicate payroll/posting/WPS effects; idempotency tests |
| PAYM-007 | Accounting posting is versioned and reconciles per component/entity/period/currency; contract tests |
| PAYM-008 | WPS/provider statuses and artefacts are exact, secure and do not overstate settlement; contract tests |
| PAYM-009 | Sensitive/self-service/export access, entitlement, tenant isolation and RLS cover every path; security tests |
| PAYM-010 | Logs/audit/evidence exclude prohibited salary/bank/identity/secret data; redaction tests |
| PAYM-011 | Reports/payslips/API/files are authorized, accessible, bounded and historically accurate; surface tests |
| PAYM-012 | Migration/restore reconciles gross/deduction/net, components, employees, postings, WPS and files; recovery tests |

## 6. Operations and Decisions

Monitor missing/stale inputs, calculation exceptions, anomalous/negative net, duplicate/conflict, failed finalization, posting/WPS mismatch, rejected/uncertain payment evidence, payslip failures, privileged reads and export volume. APPR-P07-003–005 govern payroll, WPS and privacy. Use P07 prompts and P07-TRACE-001.
