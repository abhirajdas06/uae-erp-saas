# HRMS — Human Resource Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-HRMS-001 |
| Status | APPROVED SPECIFICATION — REGULATORY/PRIVACY POLICY REQUIRED |
| Owning phase / app | P07 / `hrms` |

## 1. Purpose and Scope

Own employee/employment master data, organization placement, effective-dated employment history, private documents and approved leave workflows under `HR-001`–`HR-002`, P07-SPEC-001 and REG-HR-001.

Excluded initially: recruitment, performance, training, benefits, medical case management, immigration/work-permit integration, government/domestic/free-zone rules and unsupported biometric/attendance systems. `users` owns login identities; `payroll` owns pay results.

## 2. Actors and Field-Level Access

HR administrator, HR manager/approver, line manager, leave approver, employee self-service user, payroll consumer service, privacy/security reviewer, auditor and purpose-bound support. Ordinary profile read excludes compensation, bank, pension/nationality, medical/leave evidence and restricted documents unless specifically authorized. Bulk export and privileged read have separate permission, purpose, expiry and audit.

## 3. Data Model and History

Conceptual records: `Employee`, `Employment`, `OrganizationUnit`, `Designation`, `EmploymentAssignment`, `ContractReference`, `CompensationReference`, `EmployeeIdentifier`, `EmployeeDocument`, `LeaveType`, `LeavePolicyAssignment`, `LeaveRequest`, `LeaveLedgerEntry` and `EmploymentChange`.

- UUIDs and explicit tenant/legal entity; employee-user link is optional, same-tenant and deliberately provisioned/revoked.
- Employee identifiers are scoped and protected; duplicate review/merge preserves aliases/history.
- Employment, assignment, contract/compensation and policy changes are effective-dated and non-overlapping under approved rules.
- Documents are private, type/size/scan checked, checksummed/versioned and category-retained.
- Leave balance derives from append-oriented accrual/use/adjustment/expiry entries; direct balance edits are prohibited.

## 4. Workflows

Hire/onboard, active/change, leave/suspension, termination and rehire transitions require approved facts, permissions, effective dates and audit. No transition creates a login automatically. Retroactive changes identify payroll/leave impact and trigger reconciliation rather than rewriting finalized payroll.

Leave validates applicable policy, eligibility, service/work pattern, calendar/day rules, overlap, balance/negative policy, evidence and approval. Approval creates ledger effects atomically. Cancellation/correction appends reversal/adjustment. Payroll consumes a versioned leave-impact snapshot, not mutable current balance.

## 5. Business Rules

| ID | Rule / verification |
|---|---|
| HRMSM-001 | Employee/employment identity and lifecycle are tenant/entity scoped and effective-dated; model tests |
| HRMSM-002 | Employee and login identities remain separate with explicit secure linkage; boundary tests |
| HRMSM-003 | Sensitive field/document/self-service/export access is purpose/role/object specific; security tests |
| HRMSM-004 | History cannot be silently overwritten/deleted; correction is linked/audited; immutability tests |
| HRMSM-005 | Leave rules/balance ledger reproduce approved policy and payroll effects; workflow/property tests |
| HRMSM-006 | Missing/ambiguous jurisdiction/worker/policy fails closed; negative tests |
| HRMSM-007 | Payroll consumes approved versioned snapshots; current changes do not rewrite finalized results; contract tests |
| HRMSM-008 | Tenant isolation/RLS covers search, manager scope, self-service, file, task, report/cache/admin; IDOR tests |
| HRMSM-009 | Privacy/retention/legal hold/deletion and privileged access are governed/audited; privacy tests |
| HRMSM-010 | Imports create reviewed records without trusting lifecycle/status; exports are bounded/safe; surface tests |
| HRMSM-011 | Migration/backfill protects history and requires payroll/leave impact reconciliation; migration tests |
| HRMSM-012 | Backup/restore verifies records, effective history, leave ledger, documents and audit; recovery tests |

## 6. Operations and Decisions

Monitor privileged/bulk access, duplicate identifiers, overlap, expired documents/policies, leave imbalance, failed payroll snapshot and retention events. APPR-P07-002/005 govern employment/leave and privacy policy. Use P07 prompts and P07-TRACE-001.
