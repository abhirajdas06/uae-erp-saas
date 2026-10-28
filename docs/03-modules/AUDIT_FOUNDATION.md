# AUDIT — Audit and Sensitive-Event Foundation Specification

| Property | Value |
|---|---|
| Document ID | MOD-AUDIT-001 |
| Status | READY FOR REVIEW |
| Owning Phase | P01 |
| Django App | `audit` |
| Domain Owner | Security/business audit-event persistence and recording contract |
| Commercial Module | No |
| Tenant-Owned Data | Mixed |

## 1. Purpose

`audit` provides append-oriented, access-controlled evidence of material security and business actions. Audit events are distinct from diagnostic logs and metrics. The foundation must be usable by later modules without becoming an uncontrolled copy of sensitive payloads.

## 2. Governing sources

- ADR-010 and ADR-018
- P01 phase specification
- SEC-012 and TST-013
- Authentication, tenancy, secrets, file, financial-integrity, and event-processing architecture

## 3. P01 scope

Record approved events for:

- authentication success/failure and recovery lifecycle;
- tenant provisioning and lifecycle changes;
- membership creation, activation, suspension, and removal;
- role/permission assignment changes;
- platform/support access attempts and outcomes;
- security-relevant configuration or authorization denials where proportionate.

Customer-facing audit search, SIEM integration, legal hold, long-term archival, and complete ERP event coverage are later work.

## 4. Audit event contract

Minimum fields:

- event UUID and occurred/recorded timestamps;
- tenant reference where applicable;
- actor type and safe actor reference;
- action code and outcome;
- resource type and safe resource reference;
- source channel;
- correlation/operation identifier;
- reason code and approved minimal metadata;
- schema version and sensitivity/retention category.

Events must not contain passwords, secrets, session cookies, reset tokens, full provider payloads, unnecessary personal data, or unbounded before/after snapshots.

## 5. Requirements

| ID | Requirement | Verification |
|---|---|---|
| AUD-MOD-001 | Material P01 actions have stable versioned event codes | Coverage review |
| AUD-MOD-002 | Required audit events are recorded in the protected transaction or an equally durable design | Transaction/rollback tests |
| AUD-MOD-003 | Ordinary users cannot modify or delete audit events | Permission/database tests |
| AUD-MOD-004 | Tenant users can access only explicitly authorized events for their tenant | Cross-tenant tests |
| AUD-MOD-005 | Platform audit access is separate, justified, least-privileged, and audited | Security review |
| AUD-MOD-006 | Payload schemas allowlist fields and enforce size limits | Validation tests |
| AUD-MOD-007 | Sensitive values are redacted or rejected before persistence and logging | Secret/PII tests |
| AUD-MOD-008 | Failed business transactions do not create misleading success evidence | Rollback tests |
| AUD-MOD-009 | Correlation links audit, application logs, tasks, and durable operations without exposing secrets | Integration tests |
| AUD-MOD-010 | Retention categories are defined without inventing legal durations | Documentation review |
| AUD-MOD-011 | Event timestamps use UTC and preserve the business-effective date separately where needed | Unit/database tests |
| AUD-MOD-012 | Audit exports are authorized, tenant-scoped, logged, and protected from spreadsheet injection | Export tests |

## 6. Integrity and failure behavior

Critical security/financial events must fail the associated operation when required audit evidence cannot be recorded, unless an approved durable fallback exists. Non-critical diagnostics may degrade without misrepresenting the business outcome.

Audit immutability means controlled append/correction semantics and restricted database access; it does not justify claiming tamper-proof storage without independent controls and evidence.

## 7. Operations and privacy

Define retention by event category, legal basis, access role, exportability, and deletion/hold behavior after specialist decisions. Monitor audit write failures, unusual privileged access, and backlog/storage growth without exposing event payloads in metrics.

## 8. Acceptance and tests

P01 exit requires an event coverage matrix and executed tests for creation, rollback, forbidden mutation/deletion, tenant isolation, platform access, correlation, redaction, size limits, timestamp behavior, and export authorization.

## 9. Pending decisions

| ID | Decision | Owner | Required before |
|---|---|---|---|
| AUD-DEC-001 | Category-specific retention and legal-hold policy | Legal / Compliance / Security | Production retention |
| AUD-DEC-002 | Tenant-visible audit-search scope | Product / Security | Customer audit feature |
| AUD-DEC-003 | External SIEM/export contract | Security / Operations | Enterprise integration |
