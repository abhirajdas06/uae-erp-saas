# PAYROLL — Payroll Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-PAYROLL-001 |
| Status | APPROVED CONTRACT BASELINE; EXPANDED IMPLEMENTATION DETAIL PROPOSED — PAYROLL/WPS POLICY REQUIRED |
| Owning phase / app | P07 / `payroll` |
| Domain owner | Payroll |
| Commercial module | Yes |
| Tenant-owned data | Yes |
| Readiness | Expanded under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`; sections 3–14 are PROPOSED and unapproved |

## 1. Purpose and Boundaries

Own effective-dated payroll configuration, input snapshots, calculations, approvals, finalized results, adjustments, payslips and approved wage-protection and payment-preparation evidence under `PAY-001`–`PAY-003`, [P07-SPEC-001](../02-phases/P07_HRMS_PAYROLL/P07_PHASE_SPECIFICATION.md) and `REG-HR-001`.

Governing sources: `PAY-001`–`PAY-003`, P07-SPEC-001, `REG-HR-001`, [UAE employment, payroll and WPS source register](../00-product/UAE_EMPLOYMENT_PAYROLL_WPS_SOURCE_REGISTER.md), ADR-003–ADR-006, ADR-010, ADR-011, ADR-013–ADR-015, ADR-017–ADR-019, `ARCH-SEQ-001`, `ARCH-NOTIFY-001`, `ARCH-MIGRATION-001`, `QUAL-PRIV-001`, `QUAL-THREAT-001`, `PROD-REPORTS-001`.

HRMS owns employment and leave; Accounting owns ledger entries; banks and wage-protection agents own payment and settlement; pension and government systems own acceptance. Excluded until approved: universal end-of-service, pension, Emiratisation and Nafis obligations, government filing, direct bank payment initiation, and unsupported jurisdictions or worker categories.

## 2. Actors and Authorization

| Actor | Permitted scope |
|---|---|
| Payroll configurator | Maintain calendars, rule sets and components |
| Input preparer | Enter and validate period inputs |
| Calculator | Run and recalculate draft calculations |
| Reviewer | Review exceptions and variance before approval |
| Approver / finalizer | Approve and finalize a run |
| Payment / WPS preparer | Prepare the approved payment or wage-protection artifact |
| Payment / WPS approver | Authorize release of the prepared artifact |
| Accounting reconciler | Reconcile posted payroll to the ledger |
| Employee self-service | View own payslip only |
| Auditor | Read-only evidence review |
| Purpose-bound support | Time-bounded, audited privileged access under ADR-018 |

Concrete permission codenames, satisfying `RDY-004`:

`payroll.configure_calendar`, `payroll.configure_ruleset`, `payroll.configure_component`, `payroll.assign_employee_payroll`, `payroll.enter_input`, `payroll.calculate_run`, `payroll.review_run`, `payroll.approve_run`, `payroll.finalize_run`, `payroll.correct_result`, `payroll.view_sensitive_pay`, `payroll.view_own_payslip`, `payroll.generate_payslip`, `payroll.prepare_wps`, `payroll.approve_wps`, `payroll.export_wps`, `payroll.prepare_posting`, `payroll.reconcile_payroll`, `payroll.export_payroll_data`, `payroll.view_all_payroll`.

Configure, input, calculate, approve, finalize, correct, view sensitive, generate payslip, prepare and export wage-protection artifacts, post, reconcile and bulk export are separate permissions with maker-checker. A preparer or calculator cannot approve or finalize the same run, and a wage-protection preparer cannot approve its release.

## 3. Domain Ownership

| Record / capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Payroll calendar, period, rule set, component | `payroll` | Direct tenant and legal entity | Configuration services |
| Employee payroll assignment | `payroll` | Employee tenant | Assignment service |
| Input, run, result, result line | `payroll` | Period tenant | Calculation and finalization services |
| Adjustment and off-cycle result | `payroll` | Result tenant | Correction service |
| Payslip artifact | `payroll` | Result tenant | Document service under ADR-019 |
| Posting operation | `payroll` | Run tenant | Durable operation service |
| Wage-protection operation and artifact | `payroll` | Run tenant | Approved agent contract service |
| Employment, contract, compensation, leave | `hrms` | Same-tenant reference | Versioned snapshot read only |
| Journal entry, period, ledger balance | `accounting` | Same-tenant reference | Accounting contract |
| Bank account and settlement | `banking` | Same-tenant reference | Banking contract |

## 4. Data Model Requirements

Conceptual records: `PayrollCalendar`, `PayrollPeriod`, `PayrollRuleSet`, `PayrollComponent`, `EmployeePayrollAssignment`, `PayrollInput`, `PayrollRun`, `PayrollResult`, `PayrollResultLine`, `PayrollAdjustment`, `PayslipArtifact`, `PayrollPostingOperation`, `WPSOperation`, `WPSArtifact`, `PayrollReconciliationFinding`.

Field-level requirements satisfying `RDY-001`:

| Entity | Required attributes |
|---|---|
| `PayrollCalendar` | UUID id; tenant FK; legal-entity FK; frequency; period definition rules; active flag |
| `PayrollPeriod` | Calendar FK; period start and end dates; pay date; `status`; unique per calendar and period |
| `PayrollRuleSet` | Tenant FK; version; effective from and to dates; jurisdiction and worker-category applicability; rounding and proration stage definitions; immutable once referenced by a finalized run |
| `PayrollComponent` | Rule set FK; code; name; type of earning, deduction, employer cost or informational; calculation basis; taxability and wage-protection inclusion flags where approved; ordering |
| `EmployeePayrollAssignment` | Employee FK; rule set version; effective dates; non-overlapping; bank-account reference restricted to authorized readers |
| `PayrollInput` | Period FK; employee FK; input type; `NUMERIC` quantity or amount; source reference; entered-by; validated flag |
| `PayrollRun` | Period FK; `status`; snapshot hash; prepared-by, approved-by and finalized-by actors with timestamps; totals by component; stale-guard token |
| `PayrollResult` | Run FK; employee FK; `NUMERIC` gross, total deductions and net; currency; snapshot version references; immutable once finalized; unique per run and employee |
| `PayrollResultLine` | Result FK; component FK; `NUMERIC` amount; calculation inputs; immutable once finalized |
| `PayrollAdjustment` | Original result FK; adjustment type; `NUMERIC` amounts; reason; approver; linked corrective result |
| `PayslipArtifact` | Result FK; private storage reference; content type; SHA-256 checksum; version; generated-at |
| `PayrollPostingOperation` | Run FK; idempotency key; payload version; status including an explicit uncertain state; attempt history; ledger reference where returned |
| `WPSOperation` | Run FK; agent contract version; idempotency key; `status`; attempt and response history |
| `WPSArtifact` | Operation FK; private encrypted storage reference; SHA-256 checksum; format version; generated-at; approver |
| `PayrollReconciliationFinding` | Tenant FK; scope; detected-at; finding type; amounts; resolution state |

Constraints: UUID primary keys; mandatory tenant and legal-entity ownership; `NUMERIC`/`Decimal` for every monetary value with precision, scale and named rounding stages approved before migration per ADR-013; check constraints proving gross less total deductions equals net per result and that run totals equal the sum of result lines; exclusion constraints preventing overlapping effective-dated rule-set assignments; unique result per run and employee; unique idempotency key per operation type; append-only adjustment and audit history; no hard deletion of a finalized run, result, line, payslip, posting or wage-protection artifact through any ordinary path.

## 5. Workflows and States

| Record | States |
|---|---|
| `PayrollPeriod` | `OPEN`, `INPUT_LOCKED`, `CALCULATED`, `CLOSED` |
| `PayrollRun` | `DRAFT`, `CALCULATING`, `CALCULATED`, `PENDING_APPROVAL`, `APPROVED`, `FINALIZING`, `FINALIZED`, `FAILED` |
| `PayrollPostingOperation` | `PENDING`, `SENT`, `CONFIRMED`, `FAILED`, `UNCERTAIN` |
| `WPSOperation` | `PREPARED`, `EXPORTED`, `UPLOADED`, `ACCEPTED`, `DISBURSED`, `REJECTED`, `UNCERTAIN`, `SETTLED` |

Sequence: open period, collect and validate inputs, calculate and recalculate a draft, review exceptions, approve, finalize, generate payslips, request accounting posting, prepare the approved payment or wage-protection artifact, reconcile evidence, close. A changed input, rule set or employee snapshot invalidates an existing approval through the stale-guard token and forces recalculation.

Finalization locks and revalidates the run, proves the gross, deduction and net equations and component constraints, and writes immutable results, audit entries and outbox intent atomically, or commits nothing. Negative net, deduction ordering, retroactivity, proration, unpaid leave, overtime, end-of-service and pension behavior exist only where explicitly approved, and otherwise fail closed.

Wage-protection preparation uses an exact versioned agent contract, a private encrypted and checksummed artifact, explicit approval, a stable operation identity and recorded response reconciliation. A `WPSOperation` state is set only from evidence; local state never fabricates settlement, and an `UNCERTAIN` outcome is never reported as disbursed or settled.

## 6. Business Rules

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
| PAYM-013 | A closed period rejects a new run, posting or wage-protection preparation; period tests |
| PAYM-014 | A bank-account change on an employee assignment requires maker-checker and is audited before any payment preparation uses it; change-control tests |
| PAYM-015 | Payroll run numbering and payslip references are unique, concurrency-safe and rollback-safe per `ARCH-SEQ-001`; numbering tests |
| PAYM-016 | Excluded treatments remain unreachable rather than partially implemented; negative tests |

## 7. Tenant Isolation, Security and Sensitive Data

Every request, service, task, report, export, cache, file, self-service and administrative path derives trusted tenant context and validates same-tenant relationships, with row-level security as defence in depth. Self-service exposes only the requesting employee's own payslip, evaluated server-side.

Applicable threats from `QUAL-THREAT-001`, satisfying `RDY-010`: `THR-010`, `THR-011`, `THR-012`, `THR-013` background calculation without tenant context, `THR-014` payslip and artifact authorization, `THR-034` race producing duplicate payment effects, `THR-035` sensitive data in logs, `THR-042` compromised agent credential, `THR-045` storage authorization, `THR-055` production payroll data in lower environments, `ABU-03` payment diversion through altered bank details, `ABU-04` unauthorized salary change, `ABU-05` self-approval, `ABU-07` bulk extraction, `ABU-09` duplicate payment through retry.

Data classification and retention, satisfying `RDY-009`: payroll configuration is `C2`; salary amounts, result lines, payslips, bank details and wage-protection artifacts are `C4`. Retention classes are `RET-05` for payroll records and wage-protection evidence, `RET-07` for bank details, and `RET-12` for generated artifacts, under `QUAL-PRIV-001`. Periods remain unresolved pending `DEC-PRIV-006`; none is asserted here.

Wage-protection artifacts are encrypted at rest, access-controlled, checksummed and never retained beyond the approved period. Agent credentials are secret-backend references only per ADR-017. Logs, metrics, traces, notifications and support exports exclude every `C4` value.

## 8. Entitlements and Degraded Access

`PAYROLL` entitlement and the relevant user permission are both required on every path. Suspension or expiry denies new calculation, approval, finalization, posting and wage-protection preparation by default. Because withheld pay has employment consequences, approved read, payslip access, export and legally required correction may be explicitly allowed and audited under `DEC-PAY-001`. Deactivation never deletes finalized results, payslips or wage-protection evidence, and never prevents required retention or recovery.

## 9. Integrations and Events

- HRMS: consume versioned employment, contract, compensation and leave-impact snapshots; a later HRMS change never rewrites a finalized result.
- Accounting: publish versioned, balanced payroll facts per component, entity, period and currency; Accounting owns journal entries and periods, and the reconciliation required by `RPT-504`.
- Banking: hand the approved payment or wage-protection artifact to the approved route; Payroll records evidence and never initiates a bank payment directly.
- Wage-protection agent: exchange only through the versioned contract behind the integration boundary per `MOD-INTEGRATIONS-001`; provider-native evidence is retained separately from internal status.
- Expenses: accept reimbursement-through-payroll requests only where that route is approved.
- Reporting: expose payroll facts for `RPT-501`–`RPT-506`.

Durable intent and the transactional outbox per ADR-010 protect finalization, posting and wage-protection preparation. Reconciliation detects run-to-result, result-to-posting, posting-to-ledger, run-to-wage-protection and artifact-to-response mismatches.

## 10. UI, API, Reports, Imports and Exports

Django and HTMX surfaces cover calendar and rule-set configuration, component configuration, employee assignment, input entry and validation, run preparation with variance and exception review, approval and finalization confirmation, payslip generation status, posting status, wage-protection preparation and approval, settlement evidence, reconciliation review and employee self-service payslip access. Surfaces use the data table, monetary cell, form error summary, destructive confirmation dialog, asynchronous operation status and attachment list components in `ARCH-UI-001`. Finalization, wage-protection release and correction require explicit confirmation naming the run and effect per `UIX-036`. Sensitive columns are hidden unless the reader holds `payroll.view_sensitive_pay`.

Reports registered in `PROD-REPORTS-001`: `RPT-501` payroll run summary, `RPT-502` payroll register, `RPT-503` payslip, `RPT-504` payroll journal reconciliation, `RPT-505` wage-protection submission status, `RPT-506` end-of-service provision and settlement. All except `RPT-504` are `C4` and restricted to explicitly authorized payroll roles by default.

Imports follow `ARCH-MIGRATION-001` domains 4 and 6: payroll configuration and opening payroll balances through previewed, bounded, idempotent staged services. Import cannot create a finalized run, cannot bypass approval or numbering, and opening balances are all-or-nothing and must reconcile. Exports are private, encrypted where `C4`, authorized, formula-safe, checksummed and audited as a disclosure.

Document types registered in `ARCH-SEQ-001`, satisfying `RDY-007`: payroll run reference, allocated at run creation and scoped to tenant, entity and period; payslip reference, allocated at generation; and wage-protection file reference, allocated at preparation. Gapless requirements follow `DEC-SEQ-002`, with conservative gapless defaults until confirmed.

Notifications registered in `ARCH-NOTIFY-001`, satisfying `RDY-008`: run awaiting approval, run finalized, payslip available, posting failed or uncertain, wage-protection rejected or uncertain, bank-detail change recorded, and reconciliation variance detected. Payslip availability notifies the employee without including any amount in the subject, preview or body, per `NTF-034`. Financial and security categories are mandatory and are never digested.

## 11. Regulatory and Financial Readiness

This module establishes no UAE wage, overtime, leave-pay, end-of-service, pension, Emiratisation or wage-protection obligation, and no file format is assumed correct. Applicability, the exact salary-information-file format, agent onboarding and submission acceptance are unresolved and governed by `APPR-P07-003` and `APPR-P07-004`, with dated sources recorded in the employment, payroll and wage-protection source register.

A successful file generation or agent acknowledgement is never evidence of regulatory compliance, per `AGENTS.md` section 11. Where applicability or format is unapproved, wage-protection preparation is disabled and visibly unavailable. No regulatory fact or period is asserted here, per `RDY-012`.

## 12. Operations, Migration and Recovery

Monitor missing or stale inputs, calculation exceptions, anomalous or negative net results, duplicate and conflicting runs, failed finalization, posting and wage-protection mismatches, rejected and uncertain payment evidence, payslip generation failures, privileged reads, bank-detail changes and export volume. Runbooks cover a failed finalization transaction, an uncertain posting or wage-protection outcome requiring manual confirmation, a rejected wage-protection file, an incorrect finalized result requiring a linked adjustment or off-cycle run, a suspected payment diversion, and restore reconciliation.

Migration preserves finalized results, component detail, payslips, posting and wage-protection evidence and audit; a precision change requires before-and-after gross, deduction and net totals plus recovery evidence. Restore verifies employee and result counts, gross, deduction and net totals by period and currency, component totals, posting idempotency keys, wage-protection artifact checksums, outbox age and audit completeness.

## 13. Acceptance Criteria, Tests and Evidence

Acceptance criteria are `PAYM-001`–`PAYM-016` and the applicable criteria in `P07-AC-001`–`P07-AC-021`. Required tests are the payroll scenarios within `P07-TST-001`–`P07-TST-192`. Evidence records are `P07-EV-007`–`P07-EV-015` in the [P07 matrix](../02-phases/P07_HRMS_PAYROLL/P07_TRACEABILITY_AND_TEST_MATRIX.md).

All scenarios are `NOT_RUN`. Calculation arithmetic is tested against golden fixtures covering proration, mid-period joiners and leavers, unpaid leave, retroactive adjustment, rounding-sensitive values and negative-net guards, per `QUAL-TESTDATA-001` TD-014 and TD-035. Tests use synthetic employees and documented invalid bank-detail patterns, and never transmit to a real agent endpoint.

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| DEC-PAY-001 | Payroll scope, component model, rounding and proration stages, retroactivity, negative-net policy and degraded-access behavior | Product / Finance / HR | Any calculation or schema work | Approve a minimal earning and deduction set with explicit rounding stages; keep end-of-service and pension excluded |
| DEC-PAY-002 | Wage-protection applicability, exact file format version, agent selection and submission route | Product / Payroll specialist / DevOps | Any wage-protection generation or transmission | Keep disabled until the format and agent are confirmed with dated evidence |
| DEC-PRIV-001 | Employee and payroll data classification, lawful basis, access, retention, transfer and deletion policy | Privacy / Legal / Security / Product | Production payroll data handling | Apply purpose-bound field access and minimization |
| DEC-PRIV-006 | Retention periods for payroll and wage-protection records | Employment specialist | Automated disposal | Confirm with dated sources; retain under obligation until then |
| DEC-GOV-007 | Phase-entry specification gate covering this expansion | Product Owner / Architecture | P07 implementation authorization | Approve the gate and this expanded specification together |

`APPR-P07-003`, `APPR-P07-004` and `APPR-P07-005` remain the governing approvals for payroll, wage protection and privacy.

## 15. Implementation Prompt

Use the [P07 orchestration prompt](../04-agents/phase-prompts/P07_HRMS_PAYROLL.md) and the payroll tasks in the [P07 bounded task prompts](../04-agents/phase-prompts/P07_BOUNDED_TASK_PROMPTS.md), with `P07-TRACE-001` as the verification baseline. Every coding task requires an authorized manifest; no implementation is authorized by this document.
