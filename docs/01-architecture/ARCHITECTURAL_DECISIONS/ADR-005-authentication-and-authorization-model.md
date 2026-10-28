# ADR-005: Authentication and Authorization Model

| Field | Details |
|---|---|
| ADR ID | ADR-005 |
| Title | Authentication and Authorization Model |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / Security Lead |
| Reviewers | Architecture, Security, Product, Development, Privacy |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-002, ADR-003, ADR-004, ADR-006, ADR-017, ADR-018, ADR-020 |
| Related Requirements | IAM-001–IAM-005, TEN-002–TEN-005, SUB-003, NFR-001–NFR-003 |
| Related Documents | `AUTHENTICATION_AND_PERMISSIONS.md`, `MULTI_TENANCY.md`, `DJANGO_APP_STRUCTURE.md`, `API_STANDARDS.md`, `ENTITLEMENT_ENGINE.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The platform must authenticate human users and approved service identities, support users who belong to multiple tenants, enforce tenant-scoped roles and object access, and separate tenant administration from platform operations.

Django provides authentication, session, group, and permission primitives, but its global permission model does not by itself establish tenant membership, legal-entity scope, branch scope, module entitlement, object ownership, or safe support access.

The user model must be chosen before the first production migration. The authorization model must also remain consistent across server-rendered views, HTMX requests, APIs, application services, tasks, exports, and administrative tools.

## 2. Decision Drivers

- Secure identity and credential lifecycle.
- Explicit multi-tenant membership and active-tenant selection.
- Least privilege and deny-by-default behavior.
- Tenant-, legal-entity-, branch-, and object-level scope.
- Separation of commercial entitlement from user authorization.
- Strong protection for financial, payroll, banking, tax, and administrative operations.
- Auditable privileged access and role changes.
- Consistency across all transport and execution paths.

## 3. Options Considered

### Option A: Django identity plus tenant-scoped authorization services

Use a custom Django user model, Django-supported credential/session facilities, explicit tenant membership, tenant-scoped RBAC, object checks, and separate platform permissions.

**Advantages:** integrates with Django security, supports server-rendered UI, remains testable, and models tenant scope explicitly.

**Disadvantages:** requires custom policy services and cannot rely solely on Django groups.

### Option B: Django groups and model permissions only

**Advantages:** minimal custom code.

**Disadvantages:** groups are global by default and do not safely express tenant, legal-entity, branch, entitlement, or sensitive-field scope.

### Option C: External identity provider as the sole authorization authority

**Advantages:** centralized identity and possible enterprise federation.

**Disadvantages:** external claims become stale, cannot express all business-object rules, and create provider dependency. Product authorization must remain local.

### Option D: Per-tenant user accounts

**Advantages:** simple membership assumptions.

**Disadvantages:** duplicate identities, difficult multi-tenant access, fragmented credential lifecycle, and poor support for partners or accountants.

## 4. Decision

Use one custom Django user model for platform identities and a separate tenant-membership model for organizational access. Authorization will use deny-by-default, tenant-scoped RBAC supplemented by legal-entity, branch, object, state-transition, sensitive-field, and separation-of-duties checks.

Authentication, tenant membership, user authorization, module entitlement, and business-rule validation are independent gates. Passing one gate does not imply passing another.

### 4.1 Identity ownership

`users.User` is the authoritative human-user identity and must be configured through `AUTH_USER_MODEL` before initial production migrations.

`tenants.TenantMembership` establishes whether a user may participate in a tenant. Membership belongs to `tenants` under ADR-003.

`users` owns role and permission definitions and membership-role assignments. A role assignment must reference an active membership and record its scope.

### 4.2 Authentication

- Use Django's supported password hashing, session, CSRF, token, and security facilities rather than custom cryptography.
- Server-rendered browser access uses secure session authentication by default.
- API authentication mechanisms must be selected by API audience under ADR-020; browser sessions are not automatically suitable for machine integrations.
- Account activation, verification, recovery, lockout, and credential change operations must be rate-limited and audited where appropriate.
- Multi-factor authentication is required for platform-privileged access and should be supported for sensitive tenant roles; the exact initial method remains a security decision.
- Federation and social login are deferred until justified by an approved requirement.

### 4.3 Active tenant context

A user with memberships in multiple tenants must explicitly select or address one authorized tenant context. The platform must not infer a privileged tenant from an untrusted identifier or a previous request.

Every protected operation must validate that:

1. The identity is authenticated and active.
2. The tenant exists and is eligible for the operation.
3. The membership is active.
4. The role or direct permission permits the action in the relevant scope.
5. Object ownership and business state permit the action.
6. The applicable module entitlement permits the capability.

### 4.4 Permission model

Permissions use stable, action-oriented codes such as `invoicing.invoice.approve` or `payroll.run.view_sensitive`.

Roles group permissions but do not replace operation-specific checks. Broad `manage` permissions should be avoided when approval, posting, reversal, export, or sensitive viewing require distinct controls.

Role assignments may be scoped to:

- Tenant.
- Legal entity.
- Branch.
- An explicitly supported record-assignment boundary.

The initial implementation must not invent record-level scope for every model. Add it only where a validated workflow requires it.

### 4.5 Object and state-transition authorization

A permission code alone is insufficient. Services must validate tenant ownership, legal-entity and branch scope, current object state, actor relationship, separation of duties, and applicable financial controls.

All state-changing authorization belongs at the application-service boundary. Views and serializers may reject earlier, but they must not be the only enforcement point.

### 4.6 Platform administration

Platform operators are not tenant administrators. Cross-tenant or support access must use dedicated platform permissions, explicit purpose, bounded scope, time-limited elevation where practical, and audit records.

Django superuser status must not be used as the ordinary support-access model. Production runtime paths must not silently bypass tenant isolation because an account is privileged.

### 4.7 Background tasks and service identities

Tasks execute an authorized operation; they do not inherit a user's live session. Task records must capture the initiating actor where relevant, tenant, operation, and authorization-relevant scope. Workers must revalidate ownership and current business state.

Machine integrations require separately managed service credentials with limited scopes, rotation, revocation, and auditability. A service identity must not masquerade as a human user.

### 4.8 Caching and revocation

Authorization caches must be tenant- and identity-scoped, bounded in lifetime, and invalidated on membership, role, permission, or account changes. Sensitive operations must revalidate authoritative state when stale access could cause material harm.

Revocation must affect subsequent protected operations promptly. Long-running jobs must validate current authority at safe checkpoints where required.

## 5. Rationale

The selected model uses mature Django identity facilities while representing the organizational and business scopes Django does not provide automatically. Separating membership and entitlement prevents commercial availability from becoming a security permission and prevents a valid membership from granting every module or action.

## 6. Consequences

### Positive consequences

- Supports one identity across multiple tenants.
- Clear tenant and organizational scope.
- Consistent checks across transports and workers.
- Stronger privileged-access accountability.
- Avoids global Django groups being mistaken for tenant roles.

### Negative consequences and trade-offs

- Requires custom role-assignment and policy services.
- More negative authorization tests are required.
- Revocation and caching need explicit design.
- Enterprise federation and service credentials require later bounded decisions.

### Risks and mitigations

- **Permission drift:** maintain a central permission catalogue and migration process.
- **Over-broad roles:** default deny and separate sensitive actions.
- **Support abuse:** audited, purpose-bound elevation and regular review.
- **Stale authorization:** event-driven invalidation plus authoritative revalidation.
- **Transport inconsistency:** enforce at application-service boundaries.

## 7. Security and Tenant-Isolation Implications

- Passwords, reset tokens, MFA secrets, API credentials, and session identifiers are sensitive secrets.
- Login, recovery, invitation, token, and webhook endpoints require abuse controls.
- Tenant IDs, UUIDs, URLs, and hidden UI elements are not proof of authorization.
- Cross-tenant denial responses must not unnecessarily disclose object existence.
- Permission and membership changes require audit events.
- Sensitive exports require explicit permissions and tenant-safe storage.

## 8. Data Integrity and Migration

- Configure the custom user model before initial migrations.
- Enforce uniqueness and valid lifecycle states for memberships and assignments.
- Prevent roles or assignments from referencing a different tenant than the membership.
- Historical audit evidence must remain intelligible after role names or permissions change.
- Destructive account deletion must respect financial, employment, audit, and retention requirements.

## 9. Operational Impact

Operations require secure session settings, rate-limit monitoring, suspicious-login alerts, privileged-access review, credential rotation, emergency access procedures, and incident response for account compromise.

## 10. Implementation Requirements

1. Define the custom user model before the initial migration chain.
2. Implement `tenants.TenantMembership` and scoped role assignments according to ADR-003.
3. Maintain a stable permission catalogue.
4. Provide shared authorization services and decorators/adapters for views, APIs, and tasks.
5. Keep entitlement evaluation separate and composable.
6. Audit membership, role, privilege, credential, and support-access changes.
7. Establish secure defaults for cookies, sessions, CSRF, password hashing, and recovery.
8. Define MFA, service-identity, and support-elevation details before the affected production feature.

## 11. Validation and Acceptance Criteria

- [ ] A user without active membership cannot access tenant data.
- [ ] A user with multiple memberships accesses only the explicitly authorized tenant.
- [ ] Roles and assignments cannot cross tenant boundaries.
- [ ] Every protected operation checks action, object, scope, state, and entitlement as applicable.
- [ ] Views, APIs, tasks, exports, and admin paths enforce equivalent policy.
- [ ] Revoked memberships and permissions stop subsequent access within the approved window.
- [ ] Platform support access is separate, bounded, and audited.
- [ ] Sensitive permissions and separation-of-duties rules have negative tests.
- [ ] Authentication abuse controls and recovery-token tests pass.
- [ ] Logs and errors do not expose credentials or unnecessary sensitive data.

## 12. Alternatives Rejected

- Django groups alone are rejected as the tenant-authorization model.
- External identity claims alone are rejected as business authorization.
- Per-tenant duplicate user accounts are rejected as the default.
- UI-only permission checks are rejected.
- Ordinary Django superuser access is rejected as the production support workflow.

## 13. References

- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- Django authentication: https://docs.djangoproject.com/en/stable/topics/auth/
- Django password management: https://docs.djangoproject.com/en/stable/topics/auth/passwords/
- OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Custom Django identity plus tenant membership, scoped RBAC, object checks, and separate platform access.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; exact MFA and external machine-authentication mechanisms remain bounded security decisions.

This accepted decision governs the P01 identity and permission schema. Implementation remains subject to the P01 phase gate and security acceptance criteria.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial authentication and authorization decision accepted after standards review. |
