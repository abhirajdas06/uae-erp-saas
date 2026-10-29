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
