# USERS — Identity and Access-Control Specification

| Property | Value |
|---|---|
| Document ID | MOD-USERS-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Owning Phase | P01 |
| Django App | `users` |
| Domain Owner | User identity, authentication, roles, permissions, and membership-role assignment |
| Commercial Module | No |
| Tenant-Owned Data | Mixed |

## 1. Purpose

`users` provides one custom Django user identity and deny-by-default authorization foundations while keeping tenant membership owned by `tenants`. Authentication, tenant membership, permissions, commercial entitlements, and platform administration are separate decisions.

## 2. Scope and exclusions

Included:

- custom user model from the first migration;
- secure browser session authentication;
- login, logout, password change, and approved recovery;
- role/permission catalogue and membership-role assignments;
- tenant, organizational, object, field, workflow, and separation-of-duties checks;
- distinct platform-administration capabilities;
- MFA extension point and required MFA for privileged production access.

Excluded:

- public self-registration, social login, federation, and SSO;
- commercial entitlements;
- hardcoded ERP-module roles before those modules are specified;
- unrestricted Django-admin bypass;
- production support impersonation without a separate approved design.

## 3. Ownership

| Record | Owner | Tenant behavior |
|---|---|---|
| User | `users` | Platform-global identity; access requires membership |
| TenantMembership | `tenants` | Authoritative tenant association |
| Role | `users` | Tenant-scoped or approved platform template |
| Permission | `users` | Stable capability catalogue |
| RolePermission | `users` | Controlled mapping |
| MembershipRole | `users` | References one membership and same tenant role |

## 4. Authorization decision

A protected operation must independently satisfy:

1. authenticated active user;
2. trusted active tenant context;
3. active tenant membership;
4. required action permission;
5. organizational/object/field scope;
6. workflow and separation-of-duties rules;
7. platform-access rules where applicable;
8. commercial entitlement when the future module requires it.

UI visibility never substitutes for server-side enforcement.

## 5. Requirements

| ID | Requirement | Verification |
|---|---|---|
| IAM-MOD-001 | The configured custom user model exists before dependent migrations | Migration tests |
| IAM-MOD-002 | Authentication responses avoid account-enumeration disclosure | Negative tests |
| IAM-MOD-003 | Production cookies, CSRF, hosts, proxy trust, and sessions fail closed on unsafe configuration | Settings/startup tests |
| IAM-MOD-004 | Password reset/change invalidates applicable sessions/tokens under approved policy | Authentication tests |
| IAM-MOD-005 | Authorization is deny-by-default and evaluated server-side | Permission tests |
| IAM-MOD-006 | A role assignment cannot cross tenant membership boundaries | PostgreSQL constraint/service tests |
| IAM-MOD-007 | Object lookup is tenant-scoped before permission evaluation and does not disclose existence | IDOR tests |
| IAM-MOD-008 | Platform administration is separate from tenant roles and fully audited | Security tests |
| IAM-MOD-009 | Django admin applies the same tenant/permission rules | Admin tests |
| IAM-MOD-010 | Permission changes take effect consistently across requests, tasks, and caches | Cache/revocation tests |
| IAM-MOD-011 | Secrets, passwords, cookies, reset tokens, and authentication factors never enter logs/audit payloads | Log/audit tests |
| IAM-MOD-012 | Privileged production access requires the approved MFA control before launch | Release gate review |

## 6. Sessions and abuse controls

Authentication endpoints require rate/abuse controls, safe generic errors, CSRF protection, secure redirects, and audited material outcomes. Exact lockout and recovery policy requires Product/Security approval; implementations must avoid denial-of-service-prone permanent lockouts.

## 7. Entitlement boundary

P01 permissions cover platform foundation operations. P02 will provide commercial module entitlement decisions. A role never grants an unavailable module, and an entitlement never grants a user permission.

## 8. Acceptance and tests

Required evidence includes authentication lifecycle tests, tenant/role/object negative matrices, admin denial tests, platform separation, session/CSRF/cookie configuration checks, cache revocation, audit redaction, PostgreSQL same-tenant constraints, and security-review disposition.

## 9. Pending decisions

| ID | Decision | Owner | Required before |
|---|---|---|---|
| IAM-DEC-001 | Password, recovery, session lifetime, and abuse-control policy | Product / Security | Authentication task |
| IAM-DEC-002 | MFA mechanism and recovery for privileged production users | Security / Product / DevOps | Production privileged access |
| IAM-DEC-003 | Support access/impersonation business requirement | Product / Security / Privacy | Any support-access implementation |

## 10. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved.

| Gate | Disposition for `users` |
|---|---|
| RDY-001 attributes | Section 3 names the owned records. Field detail is pinned to `../01-architecture/DATABASE_DESIGN.md` section 5.5 and the identity model in `../01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`; this module does not restate them and must not diverge |
| RDY-002 states | User account states of invited, active, suspended and deactivated, and membership-role assignment lifecycle, are owned here; transitions require the permissions below and are audited. A deactivated account cannot authenticate and retains its audit history |
| RDY-003 testable rules | Satisfied by `IAM-MOD-001`–`IAM-MOD-012`, each with a named verification method, plus the authentication scenarios referenced as `IAM-TST-001`–`IAM-TST-044` |
| RDY-004 permissions | `users.view_user`, `users.add_user`, `users.change_user`, `users.deactivate_user`, `users.reset_user_credential`, `users.view_role`, `users.add_role`, `users.change_role`, `users.assign_role`, `users.revoke_role`, `users.view_permission_catalogue`, `users.manage_platform_admin` as a platform-only capability. Role assignment is separated from role definition, and both are separated from platform administration |
| RDY-005 interface surfaces | Sign-in, password change and recovery, session list, user list and detail, role management, role assignment and platform administration, mapped to the identity shell and platform shell in `../01-architecture/UI_DESIGN_SYSTEM.md` `UIX-002`, with the accessible error association required by `UIX-031` and `QUAL-A11Y-001` `A11Y-015` |
| RDY-006 reports and imports | Contributes to `RPT-805` security and access review, a provider-domain report. User and role import is operator-driven and bounded; it may never import an authentication credential, and `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` `MIG-003` requires import permission distinct from ordinary create permission |
| RDY-007 document numbering | Not applicable. No business document number is allocated |
| RDY-008 notifications | Registered in `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md`: account invited, credential changed, credential reset requested and completed, multi-factor enrolment changed, suspicious sign-in detected, account locked, role assignment changed and platform access granted. All are security category, mandatory, never digested and never opt-out, per `NTF-011`. One-time material follows `NTF-035` with bounded lifetime and single use |
| RDY-009 classification and retention | User name and contact data are `C3`; authentication credentials, recovery tokens and multi-factor secrets are `C5` and never retained in recoverable form where avoidable. Retention follows `RET-08` for account data and `RET-09` for authentication audit, under `../05-quality/DATA_PROTECTION_AND_RETENTION.md`; `PRIV-004` prohibits any `C5` value in logs, metrics or notifications |
| RDY-010 threats | `THR-001` credential stuffing, `THR-002` session token theft, `THR-003` cross-site request forgery, `THR-010`, `THR-020`, `THR-021` self-granting authority, `THR-023` unattributed administrative action, `THR-025` administrative interface exposed in production, `THR-050` committed secret, `ABU-05` self-approval across separation of duties |
| RDY-011 decision dependencies | `IAM-DEC-001` remains open for password, recovery, session lifetime and abuse-control policy. `IAM-MOD-012` requires the approved multi-factor control for privileged production access before launch; absent approved policy the stricter default applies and the behavior fails closed |
| RDY-012 regulatory assertions | None. Identity data handling is governed by `DEC-PRIV-002`, which is unresolved and not asserted here |

## 11. Integrations, Events and Operations

- `tenants`: membership is authoritative there; this module assigns roles to an existing membership and never creates a tenant association itself.
- `hrms`: an employee record never implies a login; provisioning is an explicit, separately authorized act under `hrms.link_user_account`.
- `entitlements`: authorization and entitlement remain independent evaluations per ADR-006; a permission never implies a subscription.
- `audit`: every authentication outcome, credential change, role assignment and platform access attempt is recorded under ADR-018.
- Notifications: security-category messages are dispatched through the approved transport only.

Monitor authentication failure rate and lockouts, credential reset volume, role assignment changes, privileged access attempts and denials, session anomalies and permission-cache revocation lag. Runbooks cover a suspected account compromise, an emergency privileged access revocation, a locked-out administrator, and a permission change that did not propagate within the expected window.

## 12. Migration, Compatibility and Recovery

The custom user model must exist before dependent migrations, per `IAM-MOD-001`; this ordering is irreversible once initial migrations are applied and is therefore a P01 blocking constraint. Changes to the permission catalogue are additive, and a removed permission is deprecated with its replacement recorded rather than deleted, per `../08-requirements-traceability/REQUIREMENT_ID_CONVENTIONS.md`.

Restore verification confirms user and role counts, role-to-membership tenant consistency, that no credential material was captured in a backup artifact in recoverable form, platform-administration separation, and authentication audit continuity.
