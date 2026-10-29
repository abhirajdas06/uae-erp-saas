# ENTERPRISE_ADMINISTRATION — SaaS Administration and Support-Control Specification

| Property | Value |
|---|---|
| Document ID | MOD-ENTERPRISE-ADMIN-001 |
| Status | APPROVED CONTRACT BASELINE; EXPANDED IMPLEMENTATION DETAIL PROPOSED — SUPPORT AND DATA-GOVERNANCE POLICY REQUIRED |
| Owning phase | P11; cross-cutting administration services |
| Django app | `administration` |
| Domain owner | Platform Operations |
| Commercial module | No; provider-domain capability |
| Tenant-owned data | Operates on tenant data under explicit authorization; owns provider-domain control records |
| Readiness | Expanded under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`; sections 3–14 are PROPOSED and unapproved |

## 1. Purpose and Boundary

Define controlled operator workflows for tenant, subscription and entitlement lifecycle, support access, privileged audit, export, retention, legal hold, deletion and offboarding, under [P11-SPEC-001](../02-phases/P11_ENTERPRISE_READINESS/P11_PHASE_SPECIFICATION.md). Owning domains remain authoritative; this capability orchestrates approved actions through their services.

Governing sources: P11-SPEC-001, ADR-004–ADR-006, ADR-011, ADR-017–ADR-019, `QUAL-PRIV-001`, `QUAL-THREAT-001`, `QUAL-SEC-001`, `ARCH-MIGRATION-001`, `ARCH-NOTIFY-001`, `PROD-REPORTS-001`.

It does not create unrestricted cross-tenant access, silently delete records or override legal or financial controls. It is a provider-domain capability and is never exposed to a tenant user.

## 2. Actors and Separation

| Actor | Permitted scope |
|---|---|
| Platform operator | Request and execute approved lifecycle operations |
| Tenant administrator | Request tenant-side actions such as export; no provider authority |
| Support agent | Operate within a granted, time-bounded support session |
| Support approver | Approve a support access request |
| Security responder | Break-glass request and incident action |
| Privacy / data-governance operator | Manage inventory, retention rules, holds and disposition |
| Auditor | Read-only privileged review |
| Break-glass reviewer | Independent post-hoc review of exceptional access |

Concrete permission codenames, satisfying `RDY-004`:

`administration.view_tenant`, `administration.change_tenant_lifecycle`, `administration.change_entitlement`, `administration.request_support_access`, `administration.approve_support_access`, `administration.use_support_session`, `administration.impersonate_user`, `administration.request_break_glass`, `administration.review_break_glass`, `administration.manage_data_inventory`, `administration.manage_retention_rule`, `administration.place_legal_hold`, `administration.release_legal_hold`, `administration.request_tenant_export`, `administration.execute_tenant_export`, `administration.preview_disposition`, `administration.execute_disposition`, `administration.execute_offboarding`, `administration.view_privileged_audit`.

Request, approve, execute, review and evidence access are separated for every sensitive action. No actor may both approve and execute the same privileged operation.

## 3. Domain Ownership

| Record / capability | Owner | Scope | Mutation interface |
|---|---|---|---|
| Administrative operation record | `administration` | Provider domain | Operation service |
| Support grant, session, impersonation, break-glass | `administration` | Provider domain, targets one tenant | Access-control services |
| Data inventory, retention rule, legal hold | `administration` | Provider domain, references tenant scopes | Governance services |
| Export, disposition, offboarding operation | `administration` | Targets one tenant | Orchestration services calling domain services |
| Tenant, subscription, entitlement | `tenants`, `subscriptions`, `entitlements` | Same-tenant | Owning domain services only |
| Business records of any domain | Owning module | Same-tenant | Owning module services only |
| Audit events | `audit` | Append-only | Audit service |

This capability never writes a business record directly and never bypasses a domain service, a permission check or row-level security.

## 4. Data Model Requirements

Conceptual records: `AdministrativeOperation`, `SupportAccessGrant`, `SupportSession`, `ImpersonationSession` where approved, `BreakGlassEvent`, `DataInventoryEntry`, `RetentionRule`, `LegalHold`, `TenantExportOperation`, `DataDispositionOperation`, `TenantOffboardingOperation`, `PrivilegedReviewFinding`.

Field-level requirements satisfying `RDY-001`:

| Entity | Required attributes |
|---|---|
| `AdministrativeOperation` | UUID id; operation type; target tenant reference; declared purpose; requesting actor; approving actor; `status`; idempotency key; requested-at, approved-at, executed-at; parameters; outcome; immutable audit reference |
| `SupportAccessGrant` | Target tenant reference; grantee actor; scope limited to named domains or records; declared purpose; granted-by; granted-at; expires-at; step-up authentication evidence; `status`; revoked-at and revoking actor |
| `SupportSession` | Grant FK; started-at; ended-at; accessed-record log reference; action log reference; auto-revocation trigger |
| `ImpersonationSession` | Grant FK; real actor; represented user; started-at; ended-at; prohibited-action list; every action attributed to both identities |
| `BreakGlassEvent` | Target scope; requesting actor; justification; alert reference; evidence bundle reference; independent reviewer; review outcome; reviewed-at |
| `DataInventoryEntry` | Data element; owning module; classification; data-subject category; purpose; retention class; deletion mechanism; cross-border flag |
| `RetentionRule` | Retention class; scope; period source decision reference; disposal action; approval reference; effective dates |
| `LegalHold` | Scope of tenant, domain, period or records; reason; placed-by; placed-at; review date; `status`; released-by and released-at |
| `TenantExportOperation` | Target tenant; requested scope; schema version; manifest reference; artifact reference; SHA-256 checksum; expiry; authorization snapshot; `status` |
| `DataDispositionOperation` | Target scope; retention class; dry-run flag; preview manifest; executed manifest; authorizing actor; `status`; verification evidence |
| `TenantOffboardingOperation` | Target tenant; grace-period dates; export window; disposition reference; `status`; resumable checkpoint state |
| `PrivilegedReviewFinding` | Subject operation or session; reviewer; finding; severity; resolution state |

Constraints: UUID primary keys; append-only operation, session, grant, hold and review history; unique idempotency key per operation; mandatory declared purpose and expiry on every grant; check constraints preventing an approver equal to the executing actor; mandatory target tenant on every tenant-affecting operation; no hard deletion of any operation, session, grant, hold or review record. Support grant expiry is enforced server-side and cannot be extended by the grantee.

## 5. Workflows and States

| Record | States |
|---|---|
| `AdministrativeOperation` | `REQUESTED`, `PENDING_APPROVAL`, `APPROVED`, `EXECUTING`, `COMPLETED`, `FAILED`, `CANCELLED`, `REJECTED` |
| `SupportAccessGrant` | `REQUESTED`, `APPROVED`, `ACTIVE`, `EXPIRED`, `REVOKED`, `DENIED` |
| `DataDispositionOperation` | `PREVIEW`, `PENDING_AUTHORIZATION`, `AUTHORIZED`, `EXECUTING`, `COMPLETED`, `BLOCKED_BY_HOLD`, `FAILED` |
| `TenantOffboardingOperation` | `INITIATED`, `GRACE_PERIOD`, `EXPORT_AVAILABLE`, `PENDING_DISPOSITION`, `DISPOSED`, `CANCELLED` |
| `LegalHold` | `ACTIVE`, `UNDER_REVIEW`, `RELEASED` |

Every privileged operation follows request, approve, execute, review. Support access additionally requires step-up authentication, minimum scope, an expiry and automatic revocation. Disposition always runs a dry-run preview first, and execution is blocked where a legal hold intersects the scope; the block is recorded, never bypassed.

Lifecycle actions are idempotent and resumable, and never delete tenant data merely because a subscription expired. Offboarding provides a grace period and an export window before any disposition, per `MIG-075` and `PRIV-012`.

## 6. Business Rules

| ID | Rule / verification |
|---|---|
| EAM-001 | Every privileged operation has purpose, target, actor, authority, approval and immutable audit |
| EAM-002 | Support access is minimum scope/time, step-up authenticated, auto-revoked and tenant-safe |
| EAM-003 | Impersonation, if enabled, preserves real/represented identity and blocks prohibited actions |
| EAM-004 | Break-glass is exceptional, alerted, evidence-rich and independently reviewed |
| EAM-005 | Tenant lifecycle actions are idempotent/resumable and never delete data merely for expiry |
| EAM-006 | Export reuses domain authorization, records inventory/manifest/hash and uses private expiry |
| EAM-007 | Retention/hold/disposal conflicts fail closed and preserve financial/audit evidence |
| EAM-008 | Delete/anonymize preview and execution reconcile all domain/file/event/search/cache copies |
| EAM-009 | Bulk/admin/API/task/direct-database paths preserve permission, RLS and audit controls |
| EAM-010 | Migration/restore preserves grants, holds, operations, evidence and review history |
| EAM-011 | An approver and the executing actor are distinct for every sensitive operation; separation tests |
| EAM-012 | A support session cannot read a tenant or record outside its granted scope, and expiry is enforced server-side; scope and expiry tests |
| EAM-013 | Disposition of a financial, tax or audit retention class requires explicit human authorization and is never automated unattended; authorization tests |
| EAM-014 | Tenant-visible audit of support access is produced where the support model requires it; transparency tests |
| EAM-015 | No operator surface exposes data from two tenants in one view or export unless an explicitly approved business requirement authorizes it; aggregation tests |

## 7. Tenant Isolation, Security and Sensitive Data

This capability is the single most dangerous surface in the platform, because it legitimately crosses the operator-to-tenant boundary `TB-04` and `TB-11`. Every path derives trusted context, validates the target tenant explicitly, and preserves row-level security; no path uses a superuser or `BYPASSRLS` database role.

Applicable threats from `QUAL-THREAT-001`, satisfying `RDY-010`: `THR-020` tenant user reaching a platform function, `THR-021` self-granting authority, `THR-023` unattributed administrative action, `THR-024` support access beyond purpose or duration, `THR-025` administrative interface exposed in production, `THR-053` standing production access, `THR-054` destructive operation without authorization, `THR-056` backup or export artifact exposure, `THR-057` automated agent performing an unauthorized action, `THR-058` audit trail alteration, `ABU-07` bulk extraction, `ABU-10` suppressing audit to hide an action. Residual risk `THR-RES-02` for insider access is accepted or further mitigated only under `DEC-SEC-005`.

Data classification and retention, satisfying `RDY-009`: operation and grant metadata is `C2`; accessed-record logs may reference `C4` data by identifier and are themselves `C4` in effect. Retention classes are `RET-09` for privileged audit and review evidence, `RET-16` for support and diagnostic data, and `RET-12` for export artifacts, under `QUAL-PRIV-001`. Audit records are append-only and their disposal requires approval under `DEC-PRIV-008`.

Support sessions never copy tenant data out of the platform, and support extracts are purpose-bound, time-bounded, audited and disposed of on a recorded schedule per `PRIV-065`.

## 8. Entitlements and Degraded Access

This capability is provider-domain and is not subject to tenant entitlement; it is gated solely by platform-operator permissions and approval workflows. A tenant's suspension or expiry never widens operator authority. Tenant-initiated actions that this capability orchestrates, such as export, remain subject to the tenant's own permissions.

## 9. Integrations and Events

- `tenants`, `subscriptions`, `entitlements`: execute lifecycle changes through owning domain services only.
- Every business domain: export and disposition call the domain's own authorized services, which apply their own validation and audit.
- `audit`: every privileged action writes an append-only audit event under ADR-018.
- Monitoring and incident response: break-glass and privileged denials raise alerts per `DEP-OBS-001` and feed `DEP-IR-001`.
- Notifications: mandatory security-category messages for support grant, break-glass and disposition.

Material administrative facts are published through the transactional outbox per ADR-010. Reconciliation detects orphaned tenant data, expired grants still active, holds without review, and disposition manifests that do not match executed effects.

## 10. UI, API, Reports, Imports and Exports

Operator surfaces are served from the separated platform-administration shell defined in `ARCH-UI-001` `UIX-002`, never from the tenant shell, and are restricted in production per `ARCH-API-001` section 26.7. Surfaces cover tenant search and lifecycle, entitlement adjustment, support access request and approval, active session monitoring with revoke, break-glass request and review, data inventory, retention rules, legal holds, export request and artifact access, disposition preview and authorization, offboarding progress and privileged review findings. Destructive and disposition actions require the explicit confirmation of `UIX-036` naming the tenant and effect.

Reports registered in `PROD-REPORTS-001`: `RPT-801` tenant and subscription status, `RPT-803` module adoption and usage, `RPT-805` security and access review. These are provider-domain reports and are never visible to a tenant.

Export follows `ARCH-MIGRATION-001` section 9 and reuses tenant export; this capability adds the operator-side authorization, manifest and checksum. Import of business data is out of scope.

Document types registered in `ARCH-SEQ-001`, satisfying `RDY-007`: administrative operation reference and tenant code, both provider-domain identifiers strictly separate from tenant ERP document numbering per `SEQ-005`.

Notifications registered in `ARCH-NOTIFY-001`, satisfying `RDY-008`: support access requested, approved, denied and revoked; break-glass invoked; disposition authorized and completed; legal hold placed and released; offboarding initiated and grace period ending. All are security category, mandatory and never digested or opt-out. Where the approved support model requires tenant visibility, the tenant administrator is notified of support access to their data.

## 11. Regulatory and Financial Readiness

This capability asserts no regulatory position. It enforces the retention and erasure framework in `QUAL-PRIV-001`, whose periods remain unresolved pending `DEC-PRIV-005`, `DEC-PRIV-006` and the parent `DEC-DATA-002`; no period is configured or asserted here, per `RDY-012`. Data-subject request handling is routed to the tenant as the controlling party per `PRIV-031`. Disposal of a financial, tax or audit record always requires explicit human authorization.

## 12. Operations, Migration and Recovery

Monitor active and expired support grants, break-glass use, privileged denials, approval-to-execution separation violations, bulk export and disposition volume, orphaned tenant data, holds past review date and audit gaps. Runbooks cover a support grant requiring emergency revocation, a break-glass review, a disposition blocked by a legal hold, a failed or partially completed offboarding requiring resumption, an export artifact exposure concern and restore reconciliation.

Migration preserves grants, sessions, holds, operations, manifests, evidence and review history. Restore verifies operation and grant counts, that no expired grant is active, hold coverage, audit continuity and that disposition manifests reconcile to executed effects.

## 13. Acceptance Criteria, Tests and Evidence

Acceptance criteria are `EAM-001`–`EAM-015` and the applicable criteria in `P11-AC-001`–`P11-AC-018`. Required tests are the administration scenarios within `P11-TST-001`–`P11-TST-151`, including `P11-TST-001`–`P11-TST-012` for policy readiness. Evidence records are `P11-EV-001`–`P11-EV-015` in the [P11 matrix](../02-phases/P11_ENTERPRISE_READINESS/P11_TRACEABILITY_AND_TEST_MATRIX.md).

All scenarios are `NOT_RUN` and additionally require an implemented candidate platform, since this capability can only be tested against real domain services.

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| DEC-SEC-005 | Support-access model, impersonation availability, tenant visibility of support access, and acceptance of the insider residual risk | Product Owner / Security reviewer | Any support access implementation | Purpose-bound, time-bounded, step-up authenticated, tenant-visible and audited; keep impersonation disabled until justified |
| DEC-DATA-002 | Retention, legal hold, export, deletion and anonymization and offboarding policy | Product / Privacy / Legal / Security / Finance | Data lifecycle implementation | Fail closed on conflicting retention; preserve financial and audit evidence |
| DEC-PRIV-011 | Terminated-tenant grace period, export window and disposal authority | Product Owner | Offboarding implementation | Provide a grace period and export window before any disposal |
| DEC-PRIV-008 | Audit and privileged-evidence retention and disposal authority | Security and privacy reviewers | Audit disposal | Append-only retention; approval required for disposal |
| DEC-GOV-007 | Phase-entry specification gate covering this expansion | Product Owner / Architecture | P11 implementation authorization | Approve the gate and this expanded specification together |

### 14.1 Identifier defect

The previous revision of this document cited `DEC-ENT-001` as governing support and lifecycle behavior. `DEC-ENT-001` is the approved module entitlement enforcement decision recorded against ADR-006 and does not govern support access. That reference is recorded as `ISSUE-009` and is not reused here; `DEC-SEC-005` and `DEC-DATA-002` are the governing records. Per `../08-requirements-traceability/REQUIREMENT_ID_CONVENTIONS.md` section 4, no agent reassigns an existing identifier, so the correction is registered rather than applied by renaming.

## 15. Implementation Prompt

Use the [P11 orchestration prompt](../04-agents/phase-prompts/P11_ENTERPRISE_READINESS.md) and the administration tasks in the [P11 bounded task prompts](../04-agents/phase-prompts/P11_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest; no implementation is authorized by this document.
