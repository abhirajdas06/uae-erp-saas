# AUDIT — Audit and Sensitive-Event Foundation Specification

| Property | Value |
|---|---|
| Document ID | MOD-AUDIT-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
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

## 10. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved.

| Gate | Disposition for `audit` |
|---|---|
| RDY-001 attributes | Satisfied by the audit event contract in section 4, which is this module's data model: event UUID, occurred and recorded timestamps, tenant reference, actor type and safe reference, action code, outcome, resource type and safe reference, source channel, correlation identifier, reason code, allowlisted metadata, schema version and sensitivity and retention category. Prohibited content is enumerated in the same section |
| RDY-002 states | An audit event has no mutable business state; its lifecycle is recorded, then optionally corrected by a linked append, then disposed of only under an approved retention action. `AUD-MOD-003` prohibits ordinary modification or deletion, and section 6 defines controlled append and correction semantics rather than claiming tamper-proof storage |
| RDY-003 testable rules | Satisfied by `AUD-MOD-001`–`AUD-MOD-012`, each with a named verification method |
| RDY-004 permissions | `audit.view_tenant_audit`, `audit.export_tenant_audit`, `audit.view_platform_audit`, `audit.export_platform_audit`, `audit.view_event_payload`, `audit.manage_retention_category`. Tenant audit access and platform audit access are separate capabilities, and payload inspection is separate from event listing |
| RDY-005 interface surfaces | Audit trail list and event detail components in `../01-architecture/UI_DESIGN_SYSTEM.md`, used by owning domains to display record history; customer-facing audit search remains later work under `AUD-DEC-002` |
| RDY-006 reports and imports | Supplies `RPT-109` audit trail extract and `RPT-805` security and access review in `../00-product/REPORT_CATALOGUE.md`. Import is prohibited: an audit event is only ever generated by the platform, never imported, and `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` `MIG-044` requires imports to produce their own audit entries rather than supplying them |
| RDY-007 document numbering | Not applicable. Event identifiers are UUIDs and are not business document numbers |
| RDY-008 notifications | Registered in `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md`: audit write failure and unusual privileged audit access. Both are security category, mandatory and never digested. `NTF-062` prohibits event payload content in any notification |
| RDY-009 classification and retention | Event metadata is `C2`; an event referencing payroll, banking or identity data is `C4` in effect. Retention class is `RET-09` in `../05-quality/DATA_PROTECTION_AND_RETENTION.md`, which is append-only and whose disposal requires approval under `DEC-PRIV-008`. `AUD-MOD-010` already prohibits inventing legal durations, and `PRIV-043` prohibits unattended automated disposal of this class |
| RDY-010 threats | `THR-058` audit trail alteration or deletion concealing activity, `THR-023` unattributed administrative action, `THR-024` support access beyond purpose, `THR-035` sensitive data in logs, `THR-010` cross-tenant event access, `ABU-01` altering a posted record, `ABU-10` suppressing audit to hide an action |
| RDY-011 decision dependencies | `AUD-DEC-001`, `AUD-DEC-002` and `AUD-DEC-003` remain open, alongside `DEC-PRIV-008`. Retention categories exist without durations until approved, and tenant-visible search and external export stay disabled |
| RDY-012 regulatory assertions | None. Section 6 explicitly refuses to claim tamper-proof storage without independent controls and evidence |

## 11. Entitlements and Degraded Access

`audit` is a platform foundation and is not a commercial module, so no tenant entitlement gates the recording of events; recording must never be disabled by a subscription state, because audit evidence is required precisely when a tenant is suspended or offboarding. Tenant-facing audit viewing, where later approved under `AUD-DEC-002`, is gated by permission and by the entitlement of the domain whose records are shown. Suspension or expiry never reduces recording completeness.

## 12. Migration, Compatibility and Recovery

Event schemas are versioned per `AUD-MOD-001`, and a schema change is additive: a new version is introduced and historical events remain readable under their recorded version, because reinterpreting a historical event would falsify evidence. Field removal is a deprecation with a replacement recorded, never a rewrite of stored events.

Audit tables grow monotonically, so partitioning or archival requires an approved plan that preserves queryability and chain continuity under `DEC-PRIV-008`. Restore verification confirms event counts by category and period, timestamp continuity with no unexplained gap, correlation linkage to application logs and durable operations, that no prohibited value is present in restored payloads, and that restricted database access prevents ordinary mutation after restore.
