# P07 — HRMS and Payroll Phase Specification

| Property | Value |
|---|---|
| Document ID | P07-SPEC-001 |
| Status | READY FOR REVIEW — REGULATORY POLICY APPROVAL REQUIRED |
| Regulatory cut-off | 29 October 2026 |
| Implementation authorization | NOT GRANTED |

## 1. Objective and Authority

Deliver secure employee administration, leave foundations and deterministic payroll for explicitly approved UAE employer/employee scenarios. Implements `HR-001`–`HR-002`, `PAY-001`–`PAY-003`, ADR-003–006, ADR-010–011, ADR-013–015, ADR-017–020 and [REG-HR-001](../../00-product/UAE_EMPLOYMENT_PAYROLL_WPS_SOURCE_REGISTER.md).

The initial candidate ruleset is MoHRE-regulated private-sector employment only. This phase does not certify labour-law, pension, WPS, privacy or payroll compliance.

## 2. Entry Gates

- P01 tenancy/IAM/audit, P02 entitlement, P05 accounting posting and ADR file/security controls are verified for the enabled scope.
- Employer jurisdiction/category, employee/work-pattern categories, employment/leave/payroll/WPS/pension/privacy policies are approved; unresolved scenarios fail closed.
- Product Owner approves bounded P07 scope (`APPR-P07-001`).

## 3. Included Scope

- Tenant/legal-entity employee identity, employment records, departments/designations, lifecycle and effective-dated contract/compensation references.
- Private employee documents, field-level sensitivity, self-service and purpose-bound privileged access.
- Effective-dated leave types/policies, requests, approvals, balances and payroll-effect interface for approved scenarios.
- Payroll calendars/periods, component/rule definitions, approved employee inputs/snapshots, draft calculation, review, approval, finalization, corrections and payslips.
- Approved WPS/agent export or adapter boundary with preparation, approval, evidence and reconciliation; no unsupported settlement claim.
- Versioned Accounting posting requests and reconciliation.
- Audit, reports/exports, migrations, recovery, monitoring and specialist evidence.

## 4. Excluded Scope

- Government/domestic-worker/free-zone-specific employment, multiple-country payroll or unsupported worker categories.
- Recruitment/ATS, performance, training, benefits, time-clock hardware, medical diagnosis, immigration/work-permit automation, Emiratisation/Nafis, pension authority filing, unemployment insurance or end-of-service calculations unless separately approved.
- Direct bank payment, WPS-agent behavior, general-ledger writes, universal statutory rates or legal advice.
- Biometric/special-category data without a separate privacy/security decision.

## 5. Ownership and Data Boundaries

`hrms` owns employee/employment lifecycle, organization placement, employment documents and leave records. `users` owns login identity; employee-user linkage is optional, same-tenant and explicitly provisioned. `payroll` owns payroll rules/configuration, input snapshots, runs/results/adjustments, payslips and payment/WPS preparation evidence. Accounting owns postings; banks/WPS agents own settlement; government/pension systems own regulatory acceptance.

Sensitive fields are classified and minimized: identity/contact, contract, compensation, bank/WPS, pension/nationality, leave/medical evidence and payroll results have purpose/role/field/export-specific access. Ordinary HR read does not imply salary, bank, medical or payroll access.

## 6. HRMS Controls

- Employment status, contract, compensation and policy assignments are effective-dated; overlapping/retroactive changes follow approved rules and preserve history.
- Employee identifiers are scoped; duplicate candidates are reviewed, never silently merged.
- Documents are private, scanned/validated, checksum/versioned, authorized at download and retained/disposed per category policy.
- Leave uses approved eligibility, accrual, calendar/day, proration, carryover, negative balance, evidence, approval and payroll-effect rules. Missing policy blocks action.
- Employee termination/deactivation does not delete payroll, leave, document or audit history.

## 7. Payroll and WPS Controls

- Rules are effective-dated by employer/entity, employee category/work pattern, contract, component and governing scheme.
- A payroll run snapshots employee eligibility, compensation, time/leave/input, component/rule versions, currency and calculation evidence. `Decimal` only; server is authoritative.
- Drafts can be recalculated under controlled versioning; approval rejects stale inputs. Finalization commits one immutable result or none. Corrections use linked adjustment/off-cycle/reversal flows.
- Maker/checker and restricted payroll permissions are enforced; employees see only authorized self-service records.
- Payroll-to-Accounting is versioned/idempotent and reconciled. Payroll never writes ledger lines.
- WPS/payment preparation uses an approved current agent/SIF contract, secure approval, encrypted/private artefact, stable operation, responses/reconciliation and restricted export. Prepared/uploaded/accepted/disbursed/settled meanings remain distinct.

## 8. Migration, Recovery and Operations

Migrations preserve effective dates, ruleset/input/result versions, immutable finalized history, sensitivity/retention categories and source/correction/posting/WPS links. Backfills affecting pay require before/after employee/component/entity totals and review. Restore validates employees, contracts, leave balances/history, payroll gross/deduction/net totals, payslip hashes, postings, payment/WPS evidence, files, outbox and audit.

Monitor unauthorized/privileged reads, bulk exports, policy expiry, overlap, calculation failure, stale approval, duplicate/conflicting run, net anomalies, posting/WPS mismatch, payslip/file failure and retention events.

## 9. Acceptance Criteria

| ID | Criterion |
|---|---|
| P07-AC-001 | Current official sources, supported employer/worker scenarios and approved/disabled rulesets are recorded |
| P07-AC-002 | Employees/employments are tenant/entity scoped, effective-dated, duplicate-controlled and historically preserved |
| P07-AC-003 | Login identity and employee record remain separate with secure explicit linkage |
| P07-AC-004 | Sensitive fields/documents use purpose/role/field/export controls, private storage and audit |
| P07-AC-005 | Employment lifecycle/contract/compensation changes preserve effective history and authorization |
| P07-AC-006 | Leave policies, requests, approvals, balances and payroll effects reproduce approved rules |
| P07-AC-007 | Payroll rules/components/calendars are effective-dated, approved and unambiguous |
| P07-AC-008 | Payroll snapshots validate and preserve exact employee/input/rule/currency versions |
| P07-AC-009 | Calculation is deterministic with Decimal, approved proration/rounding and golden fixtures |
| P07-AC-010 | Approval/finalization is transactional, maker-checker controlled and stale-input safe |
| P07-AC-011 | Finalized payroll/payslips cannot be silently changed/deleted; corrections are linked/audited |
| P07-AC-012 | Repeated/concurrent processing cannot duplicate payroll, payment preparation or posting |
| P07-AC-013 | Payroll/accounting totals reconcile by entity/period/component/currency/source |
| P07-AC-014 | WPS artefacts/operations follow exact approved agent contract and never overstate acceptance/settlement |
| P07-AC-015 | Pension/statutory behavior is enabled only for approved authority/law cohort/ruleset |
| P07-AC-016 | Permission, entitlement, field-level/self-service/tenant isolation and RLS tests pass |
| P07-AC-017 | Privacy, retention, legal-hold, export, audit and support-access controls pass |
| P07-AC-018 | UI/API/reports/payslips/files are authorized, accessible, bounded and non-misleading |
| P07-AC-019 | Migration/backup/restore/reconciliation and operational runbooks pass |
| P07-AC-020 | Security/performance/full quality gates and qualified specialist reviews are dispositioned |
| P07-AC-021 | Product Owner approves exit and separately production payroll/WPS scope |

## 10. Task/Evidence Plan

P07-T01 regulatory/privacy/policy baseline (`P07-EV-001–002`); P07-T02 employee/employment/document foundation (`P07-EV-003–004`); P07-T03 leave (`P07-EV-005`); P07-T04 payroll rules/inputs (`P07-EV-006`); P07-T05 calculation/approval/finalization (`P07-EV-007–008`); P07-T06 corrections/payslips/accounting (`P07-EV-009`); P07-T07 WPS boundary (`P07-EV-010`); P07-T08 security/surfaces (`P07-EV-011–012`); P07-T09 migration/recovery/operations (`P07-EV-013–014`); P07-T10 independent exit (`P07-EV-015`).

## 11. Pending Approvals

| ID | Decision / approver | Recommendation and recording method | Blocks |
|---|---|---|---|
| APPR-P07-001 | Bounded scope — Product Owner | “I approve P07-SPEC-001 as the bounded P07 implementation scope, subject to its named gates.” | P07 implementation |
| APPR-P07-002 | Employer/employee jurisdiction and HR/leave rules — Product/HR/qualified UAE Legal | Start MoHRE-private-sector only; approve versioned applicability/rules using REG-HR sources and checksums | HR/leave schema/activation |
| APPR-P07-003 | Payroll/end-of-service/pension policy — Product/Finance/HR/qualified UAE Payroll/Legal | Approve enabled components, categories, proration, rounding, retroactivity, corrections, final settlement and pension cohorts; disable remainder | Payroll schema/calculation |
| APPR-P07-004 | WPS provider/agent and technical contract — Product/Finance/Security/Legal/Operations | Approve applicability, bank/agent, current SIF/responses, statuses, credentials, encryption, support and reconciliation in dated record | WPS export/integration |
| APPR-P07-005 | Employee privacy/retention — Privacy/Legal/Security/Product | Approve classification, lawful basis/notices, field access, self-service, exports, residency/transfers, retention/legal hold/deletion | Sensitive data production use |
| APPR-P07-006 | Exit/production — Product Owner after specialist/independent reviews | Record exact employers/categories/rules/WPS environment/evidence/limitations/rollback separately from phase exit | Exit/production |
