# HRMS — Human Resource Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-HRMS-001 |
| Status | APPROVED CONTRACT BASELINE; EXPANDED IMPLEMENTATION DETAIL PROPOSED — REGULATORY/PRIVACY POLICY REQUIRED |
| Owning phase / app | P07 / `hrms` |
| Domain owner | Human Resources |
| Commercial module | Yes |
| Tenant-owned data | Yes |
| Readiness | Expanded under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`; sections 3–14 are PROPOSED and unapproved |

## 1. Purpose and Scope

Own employee and employment master data, organization placement, effective-dated employment history, private documents and approved leave workflows under `HR-001`–`HR-002`, [P07-SPEC-001](../02-phases/P07_HRMS_PAYROLL/P07_PHASE_SPECIFICATION.md) and `REG-HR-001`.

Governing sources: `HR-001`–`HR-002`, P07-SPEC-001, `REG-HR-001`, [UAE employment source register](../00-product/UAE_EMPLOYMENT_PAYROLL_WPS_SOURCE_REGISTER.md), ADR-003–ADR-006, ADR-011, ADR-013–ADR-015, ADR-018, ADR-019, `ARCH-SEQ-001`, `ARCH-NOTIFY-001`, `ARCH-MIGRATION-001`, `QUAL-PRIV-001`, `QUAL-THREAT-001`, `PROD-REPORTS-001`.

Excluded initially: recruitment, performance, training, benefits, medical case management, immigration and work-permit integration, government, domestic and free-zone specific rules, and unsupported biometric or attendance systems. `users` owns login identities; `payroll` owns pay results.

## 2. Actors and Field-Level Access

| Actor | Permitted scope |
|---|---|
| HR administrator | Configure organization structure, designations, leave types and policies |
| HR manager / approver | Maintain employee and employment records within scope |
| Line manager | View team profile subset and approve team leave |
| Leave approver | Approve leave within approved authority |
| Employee self-service user | View own profile subset, submit own leave, upload own documents |
| Payroll consumer service | Read versioned snapshots only through the published contract |
| Privacy / security reviewer | Review classification, access and retention behavior |
| Auditor | Read-only evidence review |
| Purpose-bound support | Time-bounded, audited privileged access under ADR-018 |

Concrete permission codenames, satisfying `RDY-004`:

`hrms.view_employee_basic`, `hrms.view_employee_sensitive`, `hrms.view_employee_document`, `hrms.add_employee`, `hrms.change_employee`, `hrms.change_employment`, `hrms.terminate_employment`, `hrms.rehire_employee`, `hrms.link_user_account`, `hrms.configure_org_structure`, `hrms.configure_leave_policy`, `hrms.view_own_profile`, `hrms.submit_own_leave`, `hrms.approve_leave`, `hrms.adjust_leave_ledger`, `hrms.merge_employee`, `hrms.export_hr_data`, `hrms.view_all_employees`.

Ordinary profile read excludes compensation, bank, pension and nationality, medical and leave evidence, and restricted documents unless specifically authorized. Bulk export and privileged read have separate permission, declared purpose, expiry and audit.

## 3. Domain Ownership

| Record / capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Employee, employment, history | `hrms` | Direct tenant and legal entity | Employment services |
| Organization unit, designation | `hrms` | Direct tenant | Configuration service |
| Employee identifier and document | `hrms` | Employee tenant | Identifier and document services |
| Leave type, policy, request, ledger | `hrms` | Employee tenant | Leave services |
| Login identity | `users` | Same-tenant reference | Explicit provisioning contract |
| Pay result and payslip | `payroll` | Same-tenant reference | Payroll services only |
| Expense claimant reference | `expenses` | Same-tenant reference | Reference contract |
| Ledger entry | `accounting` | Same-tenant reference | Accounting contract |

## 4. Data Model Requirements

Conceptual records: `Employee`, `Employment`, `OrganizationUnit`, `Designation`, `EmploymentAssignment`, `ContractReference`, `CompensationReference`, `EmployeeIdentifier`, `EmployeeDocument`, `LeaveType`, `LeavePolicyAssignment`, `LeaveRequest`, `LeaveLedgerEntry`, `EmploymentChange`.

Field-level requirements satisfying `RDY-001`:

| Entity | Required attributes |
|---|---|
| `Employee` | UUID id; tenant FK; legal-entity FK; employee number per `ARCH-SEQ-001`; name fields supporting Arabic and Latin script; date of birth; nationality reference; optional and deliberately provisioned user-account link; `status`; created and updated timestamps and actors |
| `Employment` | Employee FK; employment type; start date; optional end date and reason; probation dates where approved; work pattern reference; `status`; effective-dated and non-overlapping |
| `OrganizationUnit` | Tenant FK; code unique per tenant; name; optional parent FK; acyclic, depth-bounded |
| `Designation` | Tenant FK; code; name; optional grade reference |
| `EmploymentAssignment` | Employment FK; organization unit FK; designation FK; manager reference; effective from and to dates; non-overlapping per employment |
| `ContractReference` | Employment FK; contract type; effective dates; document reference; approved-by |
| `CompensationReference` | Employment FK; effective dates; currency; `NUMERIC` amounts by component reference; restricted to authorized readers |
| `EmployeeIdentifier` | Employee FK; identifier type; scoped value; validity dates; uniqueness within approved scope; alias retention after merge |
| `EmployeeDocument` | Employee FK; category; private storage reference; content type; byte size; SHA-256 checksum; scan status; version; expiry date where applicable |
| `LeaveType` | Tenant FK; code; name; paid flag; accrual basis; evidence requirement |
| `LeavePolicyAssignment` | Leave type FK; scope; effective dates; entitlement and carry-forward rules; non-overlapping |
| `LeaveRequest` | Employee FK; leave type FK; from and to dates; day-part handling; `status`; evidence reference; approver; decided-at |
| `LeaveLedgerEntry` | Employee FK; leave type FK; entry type of accrual, use, adjustment, expiry or reversal; `NUMERIC` quantity; effective date; source reference; append-only |
| `EmploymentChange` | Employment FK; change type; before and after values; effective date; actor; reason; append-only |

Constraints: UUID primary keys; mandatory tenant and legal-entity ownership; `NUMERIC`/`Decimal` for leave quantities and all compensation values; exclusion or check constraints preventing overlapping effective-dated rows per employment, assignment and policy scope; unique employee number and scoped identifier uniqueness at database level; same-tenant foreign keys for manager, approver, user link and documents; append-only enforcement on ledger and change history; no hard deletion of an employee, employment, document, ledger entry or change record through any ordinary path.

Leave balance is always derived from ledger entries; a stored balance accelerator reconciles to the ledger and is never independent truth. Direct balance edits are prohibited.

## 5. Workflows and States

| Record | States |
|---|---|
| `Employee` | `CANDIDATE_RECORD`, `ACTIVE`, `SUSPENDED`, `TERMINATED`, `REHIRED`, `MERGED` |
| `Employment` | `DRAFT`, `ACTIVE`, `ON_LEAVE`, `SUSPENDED`, `ENDED` |
| `LeaveRequest` | `DRAFT`, `SUBMITTED`, `APPROVED`, `REJECTED`, `CANCELLED`, `WITHDRAWN` |

Hire and onboard, active change, leave and suspension, termination and rehire transitions require approved facts, the permission named in section 2, an effective date and audit. No transition creates a login automatically; account provisioning is an explicit, separately authorized act under `hrms.link_user_account`.

Retroactive changes identify payroll and leave impact and trigger reconciliation rather than rewriting finalized payroll. Leave approval validates applicable policy, eligibility, service and work pattern, calendar and day rules, overlap, balance and negative-balance policy, evidence and approval authority, then creates ledger effects atomically within one transaction. Cancellation or correction appends a reversal or adjustment entry. Payroll consumes a versioned leave-impact snapshot, never the mutable current balance.

## 6. Business Rules

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
| HRMSM-013 | Effective-dated rows cannot overlap within one scope, enforced at database level; constraint tests |
| HRMSM-014 | Self-service exposes only the approved own-record subset and never another employee's data; self-service tests |
| HRMSM-015 | Arabic and Latin name and address text round-trips without loss through storage, search, export and document generation; localization tests |

## 7. Tenant Isolation, Security and Sensitive Data

Every request, service, task, report, export, cache, file, self-service and administrative path derives trusted tenant context and validates same-tenant relationships, with row-level security as defence in depth. Manager scope and self-service scope are object-level filters evaluated server-side, never client-supplied. Search and error behavior must not confirm the existence of an employee outside the caller's scope.

Applicable threats from `QUAL-THREAT-001`, satisfying `RDY-010`: `THR-010`, `THR-011`, `THR-012` cache key omitting tenant or scope, `THR-014` document authorization, `THR-035` sensitive data in logs, `THR-044` malicious uploaded document, `THR-045` storage authorization, `THR-055` production personal data in lower environments, `ABU-04` unauthorized salary or bank-detail change, `ABU-07` bulk extraction of the employee base.

Data classification and retention, satisfying `RDY-009`: organization structure is `C2`; employee name, contact and organizational placement are `C3`; compensation, bank detail, nationality, identity and residency documents, medical and disciplinary evidence are `C4`. Retention classes are `RET-05` for employment and payroll-relevant records, `RET-06` for identity and residency documents, and `RET-12` for generated artifacts, under `QUAL-PRIV-001`. Periods remain unresolved pending `DEC-PRIV-006`; none is asserted here. Biometric data is out of scope and must not be stored.

Logs, metrics, traces, notifications and support exports exclude `C4` values entirely.

## 8. Entitlements and Degraded Access

`HRMS` entitlement and the relevant user permission are both required on every path, including self-service fragments and exports. Suspension or expiry denies new employee and employment mutation and leave approval by default; approved read, employee self-service continuity where contractually required, export for remediation, and legally required correction may be explicitly allowed and audited. Deactivation never deletes employment history, leave ledger or documents, and never prevents required retention or recovery.

## 9. Integrations and Events

- `users`: provision or revoke a login identity only through the explicit same-tenant contract; an employee record never implies an account.
- `payroll`: publish versioned employment, contract, compensation and leave-impact snapshots; Payroll owns results.
- `expenses`: expose a validated claimant reference.
- `projects`: expose a validated member and assignee reference.
- `accounting`: no direct posting; payroll owns the accounting contract.
- Reporting: expose HR facts for `RPT-507`, `RPT-508` and `RPT-509`.

Material employment lifecycle facts are published through the transactional outbox per ADR-010. Consumers are idempotent and version-tolerant. Reconciliation detects snapshot drift, leave ledger imbalance, document expiry and orphaned user links.

## 10. UI, API, Reports, Imports and Exports

Django and HTMX surfaces cover the employee list with scoped filters, employee profile with progressive disclosure of sensitive sections, employment and assignment history, document management with expiry visibility, organization structure, leave request and approval queues, leave balance detail and reconciliation review. Surfaces use the data table, definition list, form, file upload, status badge, confirmation dialog and attachment list components in `ARCH-UI-001`. A sensitive section is revealed only to an authorized reader and its access is audited.

Reports registered in `PROD-REPORTS-001`: `RPT-507` employee master and headcount, `RPT-508` leave balance and liability, `RPT-509` document expiry exceptions. All are restricted by default and carry field-level restriction on `C4` columns.

Imports follow `ARCH-MIGRATION-001` domain 4: employee, employment and organization import through previewed, bounded, idempotent staged services. Import cannot create a terminated or historical lifecycle state that was not present in the source, cannot bypass identifier uniqueness and cannot write leave balances except as ledger opening entries. Exports are private, authorized, formula-safe, checksummed and audited as a disclosure.

Document types registered in `ARCH-SEQ-001`, satisfying `RDY-007`: employee number, allocated at record creation, tenant and entity scoped, non-gapless master-data code; and leave request reference. Neither is a financial document number.

Notifications registered in `ARCH-NOTIFY-001`, satisfying `RDY-008`: leave submitted, approved, rejected and cancelled; approval pending reminder; document expiring and expired; probation end approaching where approved; employment change recorded. Subject lines and preview text never disclose `C4` data, per `NTF-026` and `NTF-034`.

## 11. Regulatory and Financial Readiness

This module establishes no UAE employment-law entitlement, leave accrual rule, probation rule, termination rule, end-of-service calculation, Emiratisation obligation or immigration requirement. Applicability by jurisdiction, free zone and worker category is unresolved and governed by `APPR-P07-002` and `DEC-HR-001`, with dated sources recorded in the employment source register. Where applicability or policy is unapproved the dependent behavior is disabled and visibly unavailable. No regulatory fact is asserted here, per `RDY-012`.

## 12. Operations, Migration and Recovery

Monitor privileged and bulk access, duplicate identifiers, effective-date overlap attempts, expired documents and policies, leave ledger imbalance, failed payroll snapshot generation, self-service anomalies and retention events. Runbooks cover a duplicate employee merge, an incorrect effective-dated change requiring a linked correction, a leave ledger imbalance, a document scan failure, a retroactive change with payroll impact, and restore reconciliation.

Migration preserves employee identity, effective-dated history, leave ledger, document references and audit; a backfill requires payroll and leave impact reconciliation before acceptance. Restore verifies employee and employment counts, non-overlap of effective-dated rows, leave ledger balance reconciliation, document checksums, outbox age and audit completeness.

## 13. Acceptance Criteria, Tests and Evidence

Acceptance criteria are `HRMSM-001`–`HRMSM-015` and the applicable criteria in `P07-AC-001`–`P07-AC-021`. Required tests are the HR scenarios within `P07-TST-001`–`P07-TST-192`, including `P07-TST-001`–`P07-TST-014` for applicability and policy readiness. Evidence records are `P07-EV-001`–`P07-EV-006` in the [P07 matrix](../02-phases/P07_HRMS_PAYROLL/P07_TRACEABILITY_AND_TEST_MATRIX.md).

All scenarios are `NOT_RUN`. Tests use synthetic employees only, with the documented placeholder identity-document patterns in `QUAL-TESTDATA-001`; no real person's data is used under any circumstances.

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| DEC-HR-001 | Employment and leave policy scope, jurisdiction and worker-category applicability | Product / HR / Legal | Schema and leave calculation work | Support a single approved jurisdiction and worker category first; fail closed elsewhere |
| DEC-PRIV-001 | Employee and payroll data classification, lawful basis, notices, access, retention, transfer and deletion policy | Privacy / Legal / Security / Product | Production employee data handling | Apply purpose-bound field access and minimization; exclude biometrics |
| DEC-PRIV-006 | Retention periods for employment, payroll, wage-protection and identity-document records | Employment specialist | Automated disposal | Confirm with dated sources; retain under obligation until then |
| DEC-GOV-007 | Phase-entry specification gate covering this expansion | Product Owner / Architecture | P07 implementation authorization | Approve the gate and this expanded specification together |

`APPR-P07-002` and `APPR-P07-005` remain the governing approvals for employment, leave and privacy policy.

## 15. Implementation Prompt

Use the [P07 orchestration prompt](../04-agents/phase-prompts/P07_HRMS_PAYROLL.md) and the HR tasks in the [P07 bounded task prompts](../04-agents/phase-prompts/P07_BOUNDED_TASK_PROMPTS.md), with `P07-TRACE-001` as the verification baseline. Every coding task requires an authorized manifest; no implementation is authorized by this document.
