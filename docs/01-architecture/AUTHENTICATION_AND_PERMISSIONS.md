# Authentication and Permissions Architecture

| Property | Value |
|---|---|
| Document ID | ARCH-005 |
| Document Path | `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md` |
| Product | UAE ERP SaaS |
| Version | 1.0 |
| Status | Draft — Requires Architecture and Security Review |
| Review Date | 27 October 2026 |
| Framework | Django |
| Database | PostgreSQL |
| API Framework | Django REST Framework, where required |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DJANGO_APP_STRUCTURE.md`, `DATABASE_DESIGN.md`, `MULTI_TENANCY.md`, `MODULE_CATALOGUE.md`, `PRODUCT_REQUIREMENTS.md`, `ENTITLEMENT_ENGINE.md` |

---

# 1. Purpose

This document defines the authentication and authorization architecture for the UAE ERP SaaS platform.

It establishes how the platform will:

- Authenticate users securely.
- Manage user accounts and account lifecycle.
- Support users who belong to multiple tenants.
- Enforce tenant membership and organizational access.
- Implement role-based access control.
- Support legal-entity and branch-level restrictions.
- Control access to individual records and sensitive operations.
- Integrate permissions with subscription-based module entitlements.
- Secure browser sessions and API access.
- Manage invitations, password recovery and account verification.
- Support multi-factor authentication.
- Restrict privileged platform-operator access.
- Audit security-sensitive actions.
- Prevent unauthorized access to financial, tax, payroll and other sensitive records.

The design must be implemented consistently across Django views, application services, APIs, background tasks, exports, integrations and administrative interfaces.

## 1.1 Primary security objective

**Authentication establishes identity. Authorization determines access. Module entitlements determine commercial availability. Tenant isolation restricts data ownership. These controls must operate independently and collectively.**

A successful login must never be interpreted as permission to access every organization, module, record or administrative function.

# 2. Architectural Decisions

## 2.1 Authentication approach

Use Django's built-in authentication framework as the foundation for user identity and password management.

Use Django sessions for the primary server-rendered browser application.

Use Django REST Framework authentication and permission mechanisms for API endpoints. Select the API authentication method according to the actual client type and deployment requirements.

For a first-party browser application, prefer secure, server-managed sessions over introducing long-lived browser-held bearer tokens without a specific requirement.

For external integrations, mobile applications or third-party API clients, use an explicitly designed token or credential mechanism with appropriate expiry, revocation and scope restrictions.

Do not introduce a custom password-storage or authentication protocol.

## 2.2 Authorization approach

Use a layered authorization model:

1. Authentication.
2. Account-status validation.
3. Tenant membership.
4. Tenant and organizational scope.
5. Role-based permissions.
6. Object-level authorization.
7. Module entitlement.
8. Module dependency validation.
9. Business-state validation.
10. Database-level tenant isolation.

Every applicable layer must be evaluated before a protected operation is completed.

## 2.3 Selected authorization model

The initial platform will use **role-based access control (RBAC) with tenant, legal-entity, branch and object-level restrictions**.

The permission system must support configurable roles and permissions without requiring code changes every time a customer needs a new role.

However, a tenant administrator must not be able to create permissions that exceed the capabilities granted by the platform.

## 2.4 Design principles

The implementation must follow these principles:

- Deny by default.
- Least privilege.
- Explicit tenant membership.
- Explicit permission checks.
- Server-side enforcement.
- Separation of authentication from authorization.
- Separation of permissions from subscription entitlements.
- Separation of tenant administration from platform administration.
- Additional restrictions for sensitive financial and personal data.
- Auditable privileged operations.
- Short-lived authorization decisions where access can change.
- No reliance on frontend visibility for security.

# 3. Identity and Access Terminology

The following concepts must remain separate.

## 3.1 User identity

A user is an authenticated identity in the platform.

Suggested model:

`users.User`

A user may belong to multiple tenants.

A user account does not automatically grant access to any tenant.

## 3.2 Tenant

A tenant represents a customer organization using the SaaS platform.

Suggested model:

`tenants.Tenant`

A tenant has its own users, subscriptions, module entitlements, business data and organizational permissions.

## 3.3 Tenant membership

Membership links a user to a tenant.

Suggested model:

`tenants.TenantMembership`

Membership determines whether the user is authorized to participate in that organization.

A user with no active membership must not access tenant-owned business data.

## 3.4 Role

A role is a named collection of permissions.

Examples:

- Tenant Administrator.
- Finance Manager.
- Accountant.
- Sales Manager.
- Sales Representative.
- Inventory Manager.
- HR Manager.
- Employee.
- Read-Only Auditor.

A role is not a tenant and must not be treated as an authenticated identity.

## 3.5 Permission

A permission represents an explicitly defined action that an authorized user may perform.

Examples:

- `crm.customer.view`
- `crm.customer.create`
- `sales.invoice.view`
- `sales.invoice.approve`
- `accounting.journal.post`
- `hrms.employee.view_sensitive`
- `subscriptions.manage`

Permissions must be defined in a central, documented permission catalogue.

## 3.6 Scope

Scope determines the organizational area within which a permission applies.

Examples:

- Entire tenant.
- Selected legal entities.
- Selected branches.
- Records assigned to the user.
- Records created by the user, where appropriate.

A permission without an applicable scope must not automatically grant unrestricted access.

## 3.7 Module entitlement

A module entitlement determines whether a tenant's subscription permits the use of a commercial module.

For example, a tenant may have permission to use an accounting function according to its role but may not be entitled to the Accounting module.

In that case, access must be denied.

## 3.8 Platform operator

A platform operator is an authorized person or service that operates the SaaS platform.

Platform privileges are separate from tenant roles.

A platform operator must not automatically receive unrestricted access to customer financial records or personal data.

# 4. User Account Model

## 4.1 User model requirements

The user model should include the minimum fields necessary to support identity and account lifecycle management.

Recommended fields:

| Field | Purpose |
|---|---|
| `id` | Internal user identifier, preferably UUID |
| `email` | Login identifier if email-based login is selected |
| `email_normalized` | Canonical representation for case-insensitive identity matching |
| `is_active` | Whether the account may authenticate |
| `is_staff` | Django administrative capability, not a tenant role |
| `is_superuser` | Django-level administrative flag, subject to strict controls |
| `date_joined` | Account creation timestamp |
| `last_login` | Last successful login, where supported |
| `created_at` | Record creation timestamp |
| `updated_at` | Record update timestamp |

Additional profile fields may be stored in a separate profile model.

Examples include:

- Display name.
- Preferred language.
- Time zone.
- Contact information.
- Profile preferences.

Do not add unnecessary personal data to the core identity model.

## 4.2 Custom user model

Create and configure a custom Django user model before the first production migration.

Set:

```python
AUTH_USER_MODEL = "users.User"
```

The actual app label and model name must match the project implementation.

Do not begin with Django's default user model and plan to replace it casually after tenant memberships, foreign keys and migrations have been created.

Changing the user model late in the project can require substantial schema and data migration work.

## 4.3 Email identity

If email is the primary login identifier:

- Normalize email addresses consistently.
- Define case-insensitive uniqueness.
- Verify email ownership before treating an address as verified.
- Prevent duplicate identities caused by inconsistent normalization.
- Avoid exposing whether an email address belongs to an existing account.
- Define how email-address changes are verified and audited.

Email normalization must not alter provider-specific email semantics in a way that incorrectly merges distinct accounts.

Do not assume that removing periods or plus-addressing suffixes is universally safe.

## 4.4 Account status

An account should support a clearly defined lifecycle.

Suggested statuses:

- PENDING_VERIFICATION
- ACTIVE
- SUSPENDED
- DEACTIVATED

The implementation may use Django's `is_active` field alongside an explicit status field if that separation is useful.

The rules must be unambiguous.

For example:

| Status | Authentication |
|---|---|
| Pending verification | Restricted according to verification policy |
| Active | Permitted when all authentication checks succeed |
| Suspended | Denied |
| Deactivated | Denied |

Account status must be checked on protected requests where the authentication mechanism requires it. A session must not indefinitely preserve access after the underlying account has been suspended.

# 5. Tenant Membership and Organizational Access

## 5.1 Membership model

Membership should represent the user's relationship with a tenant.

Recommended fields:

| Field | Purpose |
|---|---|
| `id` | Membership identifier |
| `tenant_id` | Tenant to which the membership belongs |
| `user_id` | Associated user |
| `status` | Invitation and membership lifecycle |
| `joined_at` | Membership activation timestamp |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |
| `revoked_at` | Revocation timestamp, when applicable |

Additional fields may track the inviter or membership-management metadata.

## 5.2 Membership uniqueness

A user should not have multiple conflicting active memberships for the same tenant unless the product has an explicitly documented reason to support them.

Use appropriate database constraints to prevent unintended duplicates.

A revoked membership may remain in the database for audit purposes.

Reinviting a previously removed user should follow an explicit reactivation or new-invitation workflow.

## 5.3 Multi-tenant users

A single user may belong to multiple tenants.

Example:

```text
User: accountant@example.com

Tenant A
  Membership: ACTIVE
  Role: Accountant

Tenant B
  Membership: ACTIVE
  Role: Finance Manager

Tenant C
  Membership: REVOKED
```

This user may access Tenant A and Tenant B according to the permissions granted by each organization.

Access to Tenant C must be denied.

Roles and permissions must be evaluated independently for each membership.

A role assigned in Tenant A must not grant privileges in Tenant B.

## 5.4 Active tenant selection

After authentication, the user may select an organization from their authorized tenant list.

The application must validate the selected tenant against active membership records.

A previously selected tenant must not remain authorized after:

- Membership revocation.
- Membership suspension.
- Tenant suspension.
- Account suspension.
- Other relevant authorization changes.

Do not treat the tenant stored in a browser session as permanent proof of membership.

## 5.5 Legal-entity access

Where a tenant contains multiple legal entities, the permission model must support users who can access:

- All legal entities.
- Selected legal entities.
- Specific branches.
- Read-only financial information.
- Particular operational functions.

Legal-entity and branch restrictions must be applied after tenant authorization and before returning protected data.

## 5.6 Membership revocation

When a membership is revoked:

- New protected requests must be denied.
- Active sessions must no longer authorize access to that tenant.
- Cached authorization decisions must be invalidated or revalidated.
- Relevant active tenant contexts must be rejected.
- Sensitive ongoing operations must revalidate authorization before committing.
- The revocation must be audited.

If the user belongs to other tenants, their unrelated memberships may remain active.

# 6. Authentication Flows

## 6.1 Login

The login workflow should:

1. Accept the supported login identifier and credentials.
2. Validate input.
3. Apply rate limiting and abuse protections.
4. Authenticate through Django's configured authentication system.
5. Check account status.
6. Enforce required MFA or additional authentication checks.
7. Establish a secure session or issue the appropriate API credentials.
8. Record the authentication outcome.
9. Redirect to an authorized landing page or tenant-selection screen.

The application must not automatically authorize a tenant merely because the user authenticated successfully.

## 6.2 Login error handling

Error messages must not unnecessarily reveal whether an account exists.

For example, prefer a generic message such as:

"Unable to sign in with the provided credentials."

Do not expose:

- Password correctness details.
- Internal authentication exceptions.
- Database errors.
- Account lookup traces.
- Session identifiers.
- Authentication tokens.

Detailed failure reasons may be recorded in protected logs, subject to appropriate data-minimization rules.

## 6.3 Registration

Registration must follow an explicit product decision.

Possible models include:

- Public self-registration.
- Registration followed by tenant creation.
- Invitation-only registration.
- Platform-approved onboarding.
- A combination of these flows.

The initial implementation should support the selected onboarding model without allowing registration to bypass tenant provisioning controls.

Creating a user account must not automatically create privileged tenant membership unless the registration workflow explicitly authorizes that action.

## 6.4 Email verification

If email is used as the account identity or for security-sensitive recovery:

- Require verification according to the selected policy.
- Use cryptographically secure, single-use verification tokens.
- Give tokens an expiry.
- Invalidate tokens after successful use.
- Avoid including secrets in application logs.
- Rate-limit verification requests.
- Prevent account enumeration where practical.

Verification tokens should be stored or represented in a way that limits the impact of database disclosure.

## 6.5 Logout

Logout must invalidate the active session or applicable authentication credential.

For browser sessions:

- Use Django's logout mechanism.
- Invalidate the session.
- Ensure the session cookie is no longer accepted.
- Apply appropriate CSRF protection to state-changing logout requests.

For token-based APIs, define how tokens are revoked, expired or invalidated.

Do not assume that deleting a browser token invalidates a still-valid server-side credential.

## 6.6 Password recovery

The password-recovery workflow must:

- Accept a supported recovery identifier.
- Return a response that does not reveal account existence.
- Rate-limit requests.
- Generate secure, single-use tokens.
- Enforce token expiry.
- Prevent token reuse.
- Apply password validation.
- Invalidate or rotate relevant sessions and credentials according to policy.
- Notify the user of successful password changes.
- Record security-relevant events.

Use Django's established password-reset mechanisms where possible.

Do not create a custom recovery protocol without a clear technical requirement and security review.

## 6.7 Password changes

When a user changes their password:

- Verify the existing credential or require an appropriate reauthentication mechanism.
- Validate the new password.
- Update the credential securely.
- Record the event.
- Notify the user where appropriate.
- Invalidate other sessions or credentials according to the documented session-revocation policy.

Password changes and administrative password resets must not expose the new password to administrators.

# 7. Password Security

## 7.1 Password storage

Use Django's password-hashing framework.

Do not store passwords in plaintext, reversible encryption or custom hash formats.

Use a supported password hasher appropriate to the production environment.

Review password-hasher settings periodically as computing costs and framework recommendations evolve.

## 7.2 Password policy

The password policy must be defined in configuration and validated server-side.

It should:

- Require sufficient password length.
- Reject commonly used or compromised passwords where practical.
- Avoid unnecessary complexity rules that encourage predictable patterns.
- Support password managers.
- Support pasting and generated passwords.
- Avoid arbitrary periodic password changes unless required by a specific security or regulatory policy.
- Prevent reuse where a documented risk-based policy requires it.

Use Django's password validators as a foundation and add suitable controls for the product's risk profile.

## 7.3 Rate limiting

Authentication endpoints must have abuse protection.

Consider limits for:

- Login attempts.
- Password-reset requests.
- Email-verification requests.
- MFA verification attempts.
- Invitation acceptance.
- Token issuance.
- Account recovery.

Rate limits should consider both source-based and account-based abuse.

Avoid permanent account lockouts that attackers can use to deny service to legitimate users.

## 7.4 Credential compromise

The platform must have a documented response to suspected account compromise.

Potential actions include:

- Session invalidation.
- Credential reset.
- MFA reset through a verified process.
- Revocation of API credentials.
- Temporary account suspension.
- Review of recent tenant access.
- Review of privileged actions.
- Notification and incident handling.

# 8. Multi-Factor Authentication

MFA adds a second authentication factor beyond the primary credential.

Because the ERP processes financial, tax, employee and potentially payroll data, MFA should be part of the initial security design.

## 8.1 Recommended policy

Require MFA for:

- Platform operators.
- Privileged support personnel.
- Users with highly privileged administrative access.
- Other accounts designated as high risk.

For ordinary tenant users, make MFA available and define a configurable tenant-level policy.

The product may later require MFA for all users, depending on customer requirements and risk assessment.

## 8.2 Supported methods

Potential methods include:

- Time-based one-time passwords (TOTP).
- WebAuthn or passkeys.
- Approved identity-provider MFA through SSO.

The initial implementation should choose a supported, maintained implementation rather than inventing a custom MFA protocol.

SMS should not be the preferred primary MFA method where stronger methods are practical.

## 8.3 MFA enrollment

Enrollment must:

- Require an authenticated session.
- Verify control of the new factor.
- Avoid activating a factor before successful verification.
- Record the enrollment event.
- Provide recovery procedures.
- Prevent unauthorized removal of an existing factor.

## 8.4 Recovery codes

If recovery codes are supported:

- Generate them securely.
- Display them only when appropriate.
- Store only protected representations.
- Make each code single-use.
- Audit their use.
- Provide a secure regeneration process.

## 8.5 MFA reset

MFA reset is a sensitive operation.

It must require an approved identity-verification process, particularly for privileged accounts.

Support staff must not be able to disable MFA casually or impersonate users without a controlled, auditable workflow.

# 9. Session Management

## 9.1 Browser session configuration

Use Django's session framework with secure production settings.

Recommended baseline:

```python
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
```

These settings assume HTTPS in production.

The final configuration must account for the selected frontend architecture, authentication flows and any legitimate cross-site requirements.

Do not set `SameSite=None` or weaken cookie security without a documented reason.

## 9.2 Session expiry

Define:

- Idle session timeout.
- Absolute session lifetime.
- Reauthentication requirements for sensitive operations.
- Session revocation behavior.
- Concurrent-session policy, if applicable.

Timeout values must be configurable and based on the platform's risk profile.

Sensitive actions may require recent authentication even if the general session remains valid.

Examples include:

- Changing authentication settings.
- Changing payment-provider credentials.
- Exporting large amounts of sensitive data.
- Changing privileged roles.
- Initiating sensitive financial or administrative operations.

## 9.3 Session fixation

The application must rotate or replace session identifiers appropriately after authentication and other relevant privilege transitions.

Use Django's authentication and session mechanisms rather than custom session-ID handling.

## 9.4 Session revocation

Define a reliable method for revoking active sessions when:

- A user is suspended.
- A password is reset.
- MFA recovery indicates possible compromise.
- A membership is revoked.
- A privileged session must be terminated.
- An account is deactivated.

Where a user has memberships in multiple tenants, the system must distinguish tenant-specific access revocation from global account revocation.

## 9.5 Tenant switching

Switching tenants must trigger a fresh tenant authorization check.

The application must not carry over permissions from the previous tenant.

Tenant switching must clear or revalidate:

- Tenant-specific cached data.
- Active legal-entity and branch selections.
- Tenant-scoped permissions.
- Module-entitlement state.
- Tenant-specific navigation state.
- Sensitive tenant-specific form or workflow context.

A tenant switch must not change the ownership of records already created.

# 10. API Authentication and Security

## 10.1 API authentication selection

The authentication mechanism must be selected according to the client.

| Client | Preferred starting point |
|---|---|
| First-party server-rendered browser application | Django session authentication |
| Same-origin browser application using DRF | Session authentication with CSRF protection |
| External integration | Scoped API credentials or an appropriate token-based mechanism |
| Mobile application | A properly designed token or identity-provider flow |
| Enterprise SSO client | Approved OIDC or SAML integration, according to requirements |

Do not enable multiple authentication schemes indiscriminately.

Each enabled mechanism must have a defined purpose, credential lifecycle and threat model.

## 10.2 API tokens

If bearer tokens are introduced, define:

- Token format.
- Issuance process.
- Expiry.
- Rotation.
- Revocation.
- Audience and scope.
- Tenant association.
- Storage requirements.
- Leakage response.
- Audit events.

Long-lived tokens must not be issued without a clear operational requirement.

Never place access tokens in URLs.

## 10.3 API request authorization

Every protected API endpoint must enforce the relevant controls.

Example:

```text
Request
  |
  v
Authentication
  |
  v
Account Status
  |
  v
Tenant Membership
  |
  v
Permission and Scope
  |
  v
Module Entitlement
  |
  v
Object Ownership
  |
  v
Business Validation
  |
  v
Database Transaction and RLS
  |
  v
Response
```

The exact execution order may vary where an endpoint needs limited public access or an integration-specific authentication flow.

The security outcome must remain the same.

## 10.4 API object-level security

List endpoints must use tenant-scoped querysets.

Detail endpoints must retrieve records through the authorized scope.

Update and delete operations must validate ownership and permission before applying the change.

Do not assume that a UUID or other unguessable identifier prevents insecure direct object reference vulnerabilities.

## 10.5 API error responses

Error responses must not expose:

- Internal model details.
- SQL statements.
- Stack traces.
- Passwords or tokens.
- Database connection details.
- Secrets.
- Protected records outside the caller's scope.

Use consistent API error structures as defined in `API_STANDARDS.md`.

## 10.6 CORS and CSRF

Configure CORS and CSRF according to the actual client architecture.

CORS is not an authorization mechanism.

A restrictive CORS configuration does not replace tenant, object or permission checks.

For cookie-authenticated state-changing requests, implement appropriate CSRF protection.

For bearer-token clients, validate the token and request authorization independently.

# 11. Role-Based Access Control

## 11.1 Permission naming convention

Use a consistent, machine-readable permission namespace.

Recommended pattern:

```text
<module>.<resource>.<action>
```

Examples:

```text
crm.customer.view
crm.customer.create
crm.customer.update
crm.customer.delete

sales.quotation.view
sales.quotation.create
sales.quotation.approve

sales.invoice.view
sales.invoice.create
sales.invoice.approve
sales.invoice.issue
sales.invoice.void

accounting.journal.view
accounting.journal.create
accounting.journal.approve
accounting.journal.post

inventory.stock.view
inventory.stock.adjust

hrms.employee.view
hrms.employee.view_sensitive
hrms.employee.update
```

Permission identifiers must remain stable.

Changing permission names may affect role assignments, tests, APIs and authorization rules.

Permission changes must be version-controlled and reviewed.

## 11.2 Standard actions

Typical actions include:

- `view`
- `create`
- `update`
- `delete`
- `approve`
- `reject`
- `submit`
- `issue`
- `post`
- `reverse`
- `export`
- `manage`
- `view_sensitive`

Not every resource needs every action.

Avoid granting a broad `manage` permission when individual actions need separate controls.

## 11.3 Role and permission model

A configurable role system may use the following conceptual models:

```text
Tenant
  |
  +-- TenantMembership
         |
         +-- RoleAssignment
                  |
                  +-- Role
                        |
                        +-- RolePermission
                                  |
                                  +-- Permission
```

Recommended models:

- `tenants.TenantMembership`
- `users.Role`
- `users.Permission`
- `users.RolePermission`
- `users.MembershipRoleAssignment`

The exact app ownership and model names must be aligned with `DJANGO_APP_STRUCTURE.md`.

A Django implementation may use built-in permission primitives or custom models. The selected approach must support tenant-scoped roles without confusing Django's global permission system with customer-specific role assignments.

## 11.4 Role scope

A role assignment must identify its applicable scope.

Possible scope values:

- TENANT
- LEGAL_ENTITY
- BRANCH
- RECORD_ASSIGNMENT, if supported by the resource

For example, a Finance Manager role may apply to all legal entities, while a Sales Representative role may apply only to selected branches or assigned records.

Scope must be validated server-side.

Do not treat a role name as proof that the user has tenant-wide access.

## 11.5 Built-in roles

Provide useful default roles for onboarding.

Illustrative roles include:

| Role | Purpose |
|---|---|
| Tenant Owner | Manage organization ownership and authorized tenant settings |
| Tenant Administrator | Manage permitted users, roles and tenant configuration |
| Finance Manager | Manage authorized financial processes |
| Accountant | Perform authorized accounting tasks |
| Sales Manager | Manage sales operations and approvals |
| Sales Representative | Manage permitted sales records |
| Procurement Manager | Manage purchasing operations |
| Inventory Manager | Manage authorized stock operations |
| HR Manager | Manage permitted HR operations |
| Employee | Access authorized self-service functions |
| Read-Only Auditor | Review authorized information without modifying it |

These are default role templates, not a universal permission grant.

The final permission set for each role must be defined in the implementation and tested.

## 11.6 Role customization

Tenant administrators may be allowed to create custom roles from a controlled set of available permissions.

The implementation must:

- Prevent assignment of unknown permissions.
- Prevent granting platform-only permissions to tenant roles.
- Prevent escalation beyond the administrator's permitted authority.
- Preserve a secure recovery path for tenant administration.
- Record role creation and modification.
- Audit sensitive permission changes.
- Revalidate affected sessions or authorization caches.

A custom role must not be able to bypass tenant isolation, database security or module entitlements.

## 11.7 Role assignment

Role assignment must verify:

- The actor has permission to manage roles.
- The target user has an active membership in the relevant tenant.
- The requested role belongs to the permitted role catalogue.
- The role scope is valid.
- The requested permissions are assignable.
- The assignment does not violate platform-defined privilege restrictions.

The assignment must be recorded in the audit system.

# 12. Permission Evaluation

## 12.1 Standard authorization sequence

For a tenant-scoped business operation, evaluate:

1. Is the identity authenticated?
2. Is the account active?
3. Is the active tenant valid?
4. Is the user's membership active?
5. Does the user have the required permission?
6. Does the permission apply to the requested scope?
7. Is the required commercial module enabled for the tenant?
8. Are all required module dependencies satisfied?
9. Does the target object belong to the active tenant?
10. Does the target object fall within the user's legal-entity and branch scope?
11. Is the requested business-state transition permitted?
12. Does the database permit the operation under RLS and integrity constraints?

If a required condition fails, the operation must be denied.

## 12.2 Permission checks must be server-side

Do not use frontend-only controls to authorize operations.

Hiding a button does not prevent a user from calling the endpoint directly.

The backend must enforce every protected action regardless of whether the frontend displays it.

## 12.3 Reusable authorization services

Centralize permission evaluation through a documented service or policy interface.

For example:

```python
def authorize_action(
    *,
    user,
    tenant,
    permission_code,
    legal_entity=None,
    branch=None,
    resource=None,
):
    """
    Authorize an action within a validated organizational scope.

    The production implementation must evaluate account status,
    active membership, role assignments, permission scope,
    object ownership and any applicable organizational restrictions.
    """
    raise NotImplementedError
```

This is an interface example, not production-ready authorization code.

Codex must implement the function according to the actual permission model and tests.

Do not leave security decisions in unimplemented placeholder functions.

## 12.4 Avoid inconsistent permission implementations

Do not implement separate, conflicting authorization rules in:

- Views.
- Serializers.
- Templates.
- Celery tasks.
- Management commands.
- Django admin.
- External API endpoints.

Shared application services and permission policies should provide consistent behavior.

Entry points may have additional authentication requirements, but they must not weaken the underlying authorization rules.

# 13. Object-Level and Record-Level Permissions

## 13.1 Object ownership

Before accessing a tenant-owned object, verify that it belongs to the authorized tenant.

For example, an invoice must belong to the active tenant and an accessible legal entity.

A user must not gain access by supplying a valid invoice UUID from another organization.

## 13.2 Record assignment

Some modules may require record-assignment restrictions.

Examples include:

- Sales representatives accessing assigned leads.
- Project members accessing authorized project records.
- Employees accessing their own profile or payslips.
- Managers accessing employees within their permitted organizational scope.

Assignment-based access must be explicitly defined.

Do not assume that every tenant member can view every tenant-owned record.

## 13.3 Sensitive fields

Some records may be accessible while certain fields remain restricted.

Examples include:

- Employee salary.
- Payroll bank details.
- Personal identification information.
- Banking credentials.
- Sensitive customer information.
- Tax registration details.
- Integration secrets.

Use field-level controls where justified.

A read permission for an employee record must not automatically authorize access to every sensitive field.

## 13.4 Bulk operations

Bulk updates, deletes, exports and approval actions must enforce permissions for every affected record.

Do not authorize a bulk operation based solely on the first record in the request.

The operation must fail safely if the requested scope contains unauthorized records.

Where appropriate, use a transaction to prevent partial execution.

If partial success is supported, it must be explicitly documented and audited.

# 14. Separation of Duties

The ERP must support separation of duties for financial and other high-risk operations.

Examples include:

- Creating an invoice versus approving it.
- Preparing a journal versus posting it.
- Creating a supplier versus approving supplier changes.
- Creating a payment versus releasing it.
- Preparing payroll versus approving payroll.
- Creating a stock adjustment versus approving it.

Not every deployment requires strict maker-checker approval for every operation. However, the permission architecture must support it.

## 14.1 Approval requirements

Approval workflows must define:

- Required permissions.
- Eligible approvers.
- Organizational scope.
- Minimum approval count, where relevant.
- Separation-of-duties rules.
- Permitted state transitions.
- Delegation rules, if supported.
- Rejection and resubmission behavior.
- Audit requirements.

## 14.2 Self-approval restrictions

For designated sensitive workflows, the person who created a transaction must not be allowed to approve it if the applicable policy requires separation of duties.

This restriction must be enforced by the backend, not only the interface.

## 14.3 Financial state transitions

Permission to edit a draft invoice must not imply permission to issue, void or reverse it.

Similarly, permission to create a journal must not imply permission to post it.

State transitions must be validated by the domain service and protected by transactionally safe rules.

Posted financial records must follow the accounting module's correction and reversal policies rather than being silently edited.

# 15. Module Entitlements and Permissions

## 15.1 Independent controls

Module entitlement and user permission are separate.

A tenant may subscribe to Accounting, but an ordinary Sales Representative must not automatically gain accounting access.

A Finance Manager may have an accounting permission defined in the role catalogue, but if the tenant has not subscribed to Accounting, the operation must still be denied.

## 15.2 Effective access rule

Use the following conceptual rule:

```text
EFFECTIVE ACCESS =
    Authenticated
    AND Account Active
    AND Tenant Active
    AND Membership Active
    AND Required Permission Granted
    AND Permission Scope Valid
    AND Module Entitled
    AND Dependencies Satisfied
    AND Object Authorized
    AND Business Rules Satisfied
    AND Database Isolation Enforced
```

Not every public or platform operation requires every condition. The rules must be explicit for each endpoint and service.

## 15.3 Module dependency checks

If a module depends on another commercial module, the entitlement engine must evaluate the dependency.

For example, if an implemented invoicing workflow depends on Sales, the system must follow the approved module-dependency configuration rather than hardcoding assumptions across views.

Module dependencies are defined in `MODULE_CATALOGUE.md` and `MODULE_DEPENDENCIES.md`.

## 15.4 Core platform access

Core platform functions must remain accessible where necessary for the tenant to manage its account and subscription.

Examples include:

- Login and account management.
- Tenant selection.
- Subscription overview.
- Billing administration.
- Support access.
- Module catalogue visibility.

The exact behavior during subscription expiry or suspension must be defined in the commercial model.

Do not accidentally lock customers out of the workflows required to resolve subscription or billing issues.

## 15.5 Entitlement cache

If entitlement decisions are cached, the cache must be scoped to the tenant and invalidated or revalidated when:

- A subscription changes.
- A module is enabled or disabled.
- A dependency changes.
- A subscription expires.
- A tenant is suspended.
- An administrative override is applied.

An outdated entitlement cache must not permit access after the underlying entitlement has been revoked.

# 16. Sensitive Module Permissions

Certain modules require additional authorization controls because of their data sensitivity.

## 16.1 Accounting and VAT

Permissions should distinguish between:

- Viewing financial data.
- Creating transactions.
- Approving transactions.
- Posting journals.
- Reversing entries.
- Managing the chart of accounts.
- Managing accounting periods.
- Viewing tax workpapers.
- Preparing tax reports.
- Approving or finalizing tax-related workflows.
- Exporting sensitive financial information.

The actual actions must match the implemented module workflows.

## 16.2 UAE e-invoicing

Permissions should distinguish, where applicable, between:

- Viewing invoice submission status.
- Preparing submissions.
- Initiating submissions.
- Retrying failed submissions.
- Viewing provider responses.
- Managing provider configuration.
- Accessing payload evidence.
- Exporting submission records.

Provider credentials must not be exposed through ordinary configuration screens or API responses.

Regulatory submission permissions must not be inferred solely from ordinary invoice-view permissions.

## 16.3 HRMS and payroll

Separate ordinary employee access from sensitive HR and payroll access.

Examples include:

- Employee self-service.
- Viewing employee profiles.
- Editing employee records.
- Viewing salary information.
- Preparing payroll.
- Approving payroll.
- Accessing payslips.
- Managing payroll configuration.
- Exporting payroll data.

An HR role must not automatically grant access to every salary or payroll operation.

## 16.4 Banking and payments

Permissions must distinguish between:

- Viewing bank accounts.
- Viewing transactions.
- Managing reconciliation.
- Creating payment instructions.
- Approving or releasing payments.
- Managing bank integrations.
- Viewing sensitive integration metadata.

The system must never return banking or payment secrets merely because a user can view the associated configuration record.

## 16.5 Exports

Exporting sensitive information may require a separate permission from viewing it.

Examples include:

- Payroll exports.
- Customer-data exports.
- Financial statements.
- Accounting ledgers.
- Tax records.
- Large-scale contact exports.

Export permission must be checked before the data is retrieved and the file is generated.

# 17. Tenant Administration

## 17.1 Tenant administrator scope

A tenant administrator may manage selected organizational functions, including:

- User invitations.
- Membership status.
- Role assignments.
- Tenant profile settings.
- Authorized legal-entity settings.
- Branch configuration.
- Module access configuration, where commercially permitted.
- Tenant-specific preferences.

The administrator must not automatically be able to:

- Access platform-wide administration.
- Override PostgreSQL RLS.
- Change database security policies.
- Access other tenants.
- Grant platform-only permissions.
- Read every sensitive field without restriction.
- Bypass accounting approval workflows.
- Change subscription prices or platform-wide commercial configuration.

## 17.2 Tenant ownership

If the product supports a Tenant Owner role, its responsibilities and transfer process must be documented.

Ownership transfer must:

- Verify the current actor's authority.
- Verify the incoming owner's identity and membership.
- Record the transfer.
- Preserve an auditable history.
- Avoid leaving the tenant without a valid administrator.
- Follow additional verification requirements for sensitive transfers.

Do not assume the first user to register is permanently entitled to retain ownership.

## 17.3 Preventing privilege escalation

A tenant administrator must not be able to assign a role that grants privileges beyond the administrator's allowed authority.

Role-management services must validate the actual permissions being assigned, not merely the requested role name.

# 18. Platform Administration and Support

## 18.1 Separate platform and tenant administration

Platform administration must use a separate permission namespace.

Examples:

```text
platform.tenant.view
platform.tenant.manage
platform.subscription.manage
platform.support_access.request
platform.support_access.approve
platform.security_audit.view
platform.configuration.manage
```

These are illustrative identifiers.

The final permission catalogue must define each permission's purpose and permitted scope.

Tenant roles must not be able to grant platform permissions.

## 18.2 Support access

Support personnel should have access to operational metadata by default, rather than unrestricted access to customer business records.

Where customer-data access is necessary, use a controlled workflow.

Recommended controls:

1. Authenticate the support operator.
2. Verify the required platform permission.
3. Record the target tenant.
4. Require a stated business reason.
5. Obtain approval for designated sensitive access.
6. Grant time-limited access.
7. Limit the accessible operations.
8. Record relevant reads and changes where technically appropriate.
9. Expire the access automatically.
10. Review privileged-access history.

## 18.3 Impersonation

If customer impersonation is implemented for troubleshooting, it must be treated as a privileged security feature.

It must not be an unrestricted convenience function.

Controls must include:

- Explicit authorization.
- A documented reason.
- A visible impersonation state.
- A time limit.
- Audit events.
- Restricted access to highly sensitive actions.
- A reliable exit mechanism.
- No exposure of the customer's password or authentication secrets.

Where possible, prefer a controlled support-access mode that identifies the support operator explicitly rather than silently pretending the operator is the customer.

## 18.4 Platform superusers

Django superuser privileges must not automatically bypass application-level tenant security.

Production database credentials used by the web application must not be superuser credentials.

Platform administration must use explicit application permissions and controlled database roles.

# 19. Invitations and Membership Onboarding

## 19.1 Invitation flow

The invitation workflow should:

1. Verify that the inviter can manage memberships.
2. Validate the tenant and intended role.
3. Validate the target email address.
4. Create an invitation with a secure, single-use token.
5. Apply an expiry.
6. Send the invitation through the configured delivery system.
7. Verify the invitee's identity.
8. Create or associate the user account.
9. Establish the tenant membership.
10. Apply the approved role assignment.
11. Record the activation event.

The exact sequence may vary depending on whether the user already exists.

## 19.2 Invitation security

Invitation tokens must:

- Be generated securely.
- Be single-use.
- Expire.
- Be invalidated after acceptance or cancellation.
- Be protected from unnecessary logging.
- Be scoped to the intended tenant and invitation.
- Not allow role or tenant substitution through modified request parameters.

## 19.3 Role assignment during invitation

The inviter may assign only roles they are authorized to grant.

The invitee must not be able to modify the role, tenant or permission scope merely by changing a request payload.

## 19.4 Invitation cancellation

Authorized administrators must be able to cancel pending invitations.

Cancellation must invalidate the token and prevent later acceptance.

The action must be auditable.

---

# 20. Authorization in Background Tasks

Background tasks must not assume that a prior HTTP request's permissions remain valid indefinitely.

## 20.1 Task identity

Each task must have an explicit execution identity.

Possible identities include:

- A tenant user initiating an action.
- A tenant-scoped system process.
- A platform maintenance process.
- An approved integration identity.

The identity must be represented in task metadata where relevant.

## 20.2 Authorization revalidation

Before performing a sensitive or delayed operation, the task must revalidate the conditions required by the business process.

For example, an approval task must not rely solely on a permission that existed when the task was queued if the approver's membership has since been revoked.

Depending on the workflow, the task may need to revalidate:

- Tenant status.
- Membership status.
- Role assignment.
- Module entitlement.
- Resource ownership.
- Approval state.
- Integration authorization.
- Idempotency state.

## 20.3 System tasks

A system task may operate without a human actor only when its purpose and authorization are explicitly defined.

System tasks must not receive unrestricted access to all tenants merely for convenience.

Cross-tenant maintenance tasks must follow the controlled platform-processing model defined in `MULTI_TENANCY.md`.

## 20.4 Audit identity

Audit events generated by a task should distinguish:

- The human actor who initiated the operation, if applicable.
- The service or worker that executed it.
- The tenant context.
- The operation performed.
- The result.

Do not record a background worker as though it were the human actor.

# 21. Audit and Security Events

## 21.1 Required event categories

The platform must record relevant authentication and authorization events.

Examples:

- Successful login.
- Failed login.
- Logout.
- Password reset request.
- Password change.
- Email verification.
- MFA enrollment.
- MFA reset.
- Account suspension.
- Membership creation.
- Membership revocation.
- Role assignment.
- Permission changes.
- Tenant switching where security-relevant.
- Privileged support access.
- Sensitive export.
- API credential creation or revocation.
- Repeated authorization failures.
- Administrative access to sensitive records.

## 21.2 Event structure

A security event may include:

| Field | Purpose |
|---|---|
| `id` | Event identifier |
| `tenant_id` | Tenant context, if applicable |
| `actor_user_id` | Human actor, if applicable |
| `actor_type` | User, platform operator or service identity |
| `action` | Event type |
| `resource_type` | Affected resource category |
| `resource_id` | Affected resource identifier, where appropriate |
| `timestamp` | Event time |
| `outcome` | Success or failure |
| `correlation_id` | Request or workflow correlation |
| `source_context` | Relevant execution context |
| `reason` | Business reason, where required |

The actual schema must align with the audit architecture in `DATABASE_DESIGN.md`.

## 21.3 Audit integrity

Audit records must not be casually editable by ordinary tenant users.

Sensitive audit events must be protected from unauthorized modification or deletion.

Where the risk profile requires it, use separate write permissions, restricted storage or tamper-evident mechanisms.

Do not include raw passwords, access tokens, recovery tokens or integration secrets in audit events.

## 21.4 Audit retention

Define retention according to:

- Applicable law.
- Contractual obligations.
- Security requirements.
- Record category.
- Legal holds.
- Data minimization.

Do not assume that every authentication log and every business audit record requires the same retention period.

# 22. Caching and Permission Changes

## 22.1 Permission caching

Permission results may be cached for performance only if the cache is scoped and invalidated correctly.

Cache keys must account for the relevant identity and organizational scope.

For example:

```text
permissions:<user_id>:<tenant_id>:<membership_version>
```

The exact implementation may use a role-assignment version, tenant permission version or another suitable invalidation mechanism.

## 22.2 Invalidation triggers

Permission caches must be invalidated or revalidated after:

- Role changes.
- Permission changes.
- Membership suspension.
- Membership revocation.
- Tenant suspension.
- Legal-entity access changes.
- Branch access changes.
- User deactivation.
- MFA or account-security events where relevant.
- Module entitlement changes.

## 22.3 Sensitive operations

Do not rely on a long-lived cached permission decision for high-risk financial or administrative operations without an appropriate revalidation strategy.

The system must prioritize correctness over cache performance where stale authorization could expose sensitive data or permit unauthorized transactions.

# 23. Database and Tenant-Isolation Integration

This document does not replace `MULTI_TENANCY.md`.

The authentication and permission architecture must integrate with the tenant-isolation controls defined there.

## 23.1 Required sequence

For tenant-owned business operations:

1. Authenticate the user.
2. Validate account status.
3. Resolve the active tenant.
4. Validate active membership.
5. Evaluate the required permission.
6. Validate legal-entity and branch scope.
7. Validate module entitlement and dependencies.
8. Retrieve or modify records within the authorized scope.
9. Establish transaction-local PostgreSQL tenant context.
10. Execute the operation under RLS and database constraints.
11. Record required audit events.

The implementation may use a different internal sequence where necessary, but no required authorization condition may be omitted.

## 23.2 RLS does not replace authorization

PostgreSQL RLS protects tenant-row boundaries.

It does not determine whether a Sales Representative may approve an invoice or whether an employee may access payroll data.

These are application-level authorization decisions.

## 23.3 Application authorization does not replace RLS

Application-level checks are necessary but can be implemented incorrectly.

RLS must provide an independent database-level tenant-isolation safeguard for protected tables.

## 23.4 Administrative exceptions

Administrative and maintenance operations that require exceptional privileges must follow the controlled procedures defined in `MULTI_TENANCY.md`.

Do not introduce a general-purpose permission that silently bypasses tenant isolation.

---

# 24. Django Implementation Standards

## 24.1 Use Django's authentication framework

Use Django's supported authentication mechanisms for:

- Password verification.
- Session handling.
- Password hashing.
- Password reset.
- Authentication backends.
- Authentication middleware.

Extend the framework where necessary, but avoid replacing its security-sensitive behavior without a clear reason.

## 24.2 Django REST Framework permissions

For API endpoints, use explicit authentication and permission classes.

Illustrative structure:

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class CustomerListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # The production implementation must also:
        # - Resolve and validate the active tenant.
        # - Enforce the required CRM permission.
        # - Validate module entitlement.
        # - Use a tenant-scoped queryset.
        # - Apply object-level and organizational restrictions.
        raise NotImplementedError
```

`IsAuthenticated` alone is not sufficient for tenant-scoped business endpoints.

The implementation must add the required tenant, permission and entitlement checks.

## 24.3 Serializers

Serializers must not trust client-supplied ownership fields.

For tenant-owned records:

- Derive tenant ownership from validated server-side context.
- Validate relationships against the active tenant.
- Reject attempts to assign records from another tenant.
- Apply object-level permissions where required.
- Avoid exposing sensitive fields to unauthorized users.

Do not rely exclusively on serializer validation for database integrity.

## 24.4 Forms and templates

Django forms and templates must follow the same security model.

A form that hides an unauthorized choice must still validate the submitted value server-side.

Templates may hide unavailable actions for usability, but the backend must independently enforce the permission.

## 24.5 Django admin

Django admin must have explicit access rules.

Requirements include:

- Restricted access to staff-only administration.
- Tenant-aware list and object access for tenant-owned models.
- Validation of tenant ownership on writes.
- Protection against unauthorized bulk actions.
- Appropriate audit logging.
- Separation of tenant administration and platform administration.

The `is_staff` and `is_superuser` flags must not be treated as substitutes for the platform's complete authorization model.

## 24.6 Management commands

Management commands that modify tenant data must require explicit scope or operate through a documented platform-wide workflow.

A command must not accidentally process every tenant because a tenant argument was omitted.

Commands with elevated privileges must be restricted to authorized operational environments.

## 24.7 Signals and model methods

Do not rely on signals or model methods alone to enforce authorization.

Authorization must occur before the operation is executed in the relevant application service.

Signals may support auditing or secondary processing, but must not be the sole security boundary.

# 25. Testing Requirements

Security tests must cover authentication, membership, permission evaluation, tenant scope, module entitlements and privileged operations.

## 25.1 Authentication tests

| ID | Scenario | Expected result |
|---|---|---|
| IAM-001 | Valid credentials for active account | Authentication succeeds |
| IAM-002 | Invalid credentials | Authentication fails |
| IAM-003 | Suspended account attempts login | Authentication denied |
| IAM-004 | Unverified account follows protected flow | Verification policy enforced |
| IAM-005 | Password-reset token is expired | Reset denied |
| IAM-006 | Password-reset token is reused | Reset denied |
| IAM-007 | Login endpoint receives repeated abusive attempts | Rate limiting applies |
| IAM-008 | Logout is completed | Session is invalidated |
| IAM-009 | Password changes | Session-revocation policy is applied |
| IAM-010 | MFA is required but not satisfied | Protected access denied |

## 25.2 Membership tests

| ID | Scenario | Expected result |
|---|---|---|
| IAM-011 | User has active membership in Tenant A | Tenant A access may proceed |
| IAM-012 | User has no membership in Tenant B | Tenant B access denied |
| IAM-013 | User has active memberships in A and B | Permissions evaluated independently |
| IAM-014 | Membership is revoked | Tenant access denied |
| IAM-015 | Membership is suspended | Tenant access denied |
| IAM-016 | Tenant is suspended | Access follows the suspension policy |
| IAM-017 | Client submits an unauthorized tenant UUID | Access denied |
| IAM-018 | User switches from Tenant A to Tenant B | Tenant B permissions are revalidated |

## 25.3 Permission tests

| ID | Scenario | Expected result |
|---|---|---|
| IAM-019 | User has required permission and valid scope | Operation allowed |
| IAM-020 | User lacks required permission | Operation denied |
| IAM-021 | User has view permission but attempts update | Operation denied |
| IAM-022 | User has update permission but attempts approval | Operation denied |
| IAM-023 | User has role in Tenant A only | Role does not grant privileges in Tenant B |
| IAM-024 | Tenant administrator attempts to grant prohibited permission | Assignment rejected |
| IAM-025 | User attempts unauthorized legal-entity access | Access denied |
| IAM-026 | User attempts unauthorized branch access | Access denied |
| IAM-027 | Unauthorized user attempts sensitive-field access | Sensitive data withheld or access denied |
| IAM-028 | User attempts unauthorized bulk action | Operation denied |

## 25.4 Entitlement tests

| ID | Scenario | Expected result |
|---|---|---|
| IAM-029 | User has permission and tenant has module entitlement | Access allowed if all other checks pass |
| IAM-030 | User has permission but tenant lacks entitlement | Access denied |
| IAM-031 | Tenant has entitlement but user lacks permission | Access denied |
| IAM-032 | Required module dependency is absent | Access denied according to dependency rules |
| IAM-033 | Module entitlement is revoked | Subsequent access is denied |
| IAM-034 | Cached entitlement is stale | Revocation is enforced according to policy |

## 25.5 Administrative and operational tests

| ID | Scenario | Expected result |
|---|---|---|
| IAM-035 | Tenant administrator attempts platform administration | Denied |
| IAM-036 | Platform support operator requests restricted customer-data access | Approved workflow required |
| IAM-037 | Support access expires | Further access denied |
| IAM-038 | Role is changed during an active session | Authorization reflects the new policy |
| IAM-039 | User is deactivated | Protected access denied |
| IAM-040 | Background task executes after membership revocation | Required authorization revalidation occurs |
| IAM-041 | Django admin accesses an out-of-scope record | Access denied |
| IAM-042 | API client submits modified ownership fields | Request rejected |
| IAM-043 | Permission cache contains stale access | Revoked access is not improperly retained |
| IAM-044 | Privileged role change occurs | Audit event is recorded |

## 25.6 Test execution requirements

Tests must exercise the real authorization code paths.

Use production-equivalent configuration where relevant.

Do not report a test as passing if it was not executed.

Tests must cover both allowed and denied cases. Testing only successful access does not establish that authorization is secure.

---

# 26. Operational Security Requirements

## 26.1 Secret management

Store production credentials and secrets outside source control.

This includes:

- Django secret key.
- Database credentials.
- Email-provider credentials.
- API signing keys.
- Integration credentials.
- Token-signing keys, if applicable.
- Encryption keys.
- MFA-related secrets.

Use an appropriate secret-management mechanism for the deployment environment.

## 26.2 Environment configuration

Security-sensitive settings must differ appropriately between development, test and production.

Production must enforce HTTPS and secure cookie settings.

Debug mode must be disabled.

Authentication and recovery endpoints must not expose stack traces or internal configuration.

## 26.3 Dependency management

Authentication and authorization dependencies must be maintained and reviewed for security issues.

Use supported versions and apply security updates through a controlled release process.

Do not introduce an unmaintained authentication or MFA package without a documented review.

## 26.4 Monitoring

Monitor relevant events, including:

- Authentication failures.
- MFA failures.
- Password-reset abuse.
- Repeated authorization denials.
- Privilege changes.
- Membership revocation.
- Suspicious API credential activity.
- Unexpected platform support access.
- Changes to authentication configuration.

Monitoring must avoid logging credentials or unnecessary sensitive data.

## 26.5 Incident response

If unauthorized access is suspected:

1. Preserve relevant audit and security logs.
2. Determine the affected accounts and tenants.
3. Revoke affected sessions and credentials where appropriate.
4. Contain the affected access path.
5. Assess data exposure and business impact.
6. Follow applicable legal and contractual notification requirements.
7. Correct the underlying defect.
8. Add regression tests.
9. Verify the remediation.
10. Document the incident and corrective actions.

---

# 27. Implementation Roadmap

| Phase | Scope | Expected output |
|---|---|---|
| P0 — Foundation | Custom user model, password hashing, configuration and test conventions | Secure identity foundation |
| P1 — Core Platform | Tenant membership, account lifecycle, tenant selection and authorization primitives | Users can access only authorized organizations |
| P2 — Subscription Engine | Permission and module-entitlement integration | Commercial availability and user permissions operate independently |
| P3 — CRM, Sales and Invoicing | Resource-level permissions, role assignments and approval actions | Core business permissions are enforced |
| P4 — UAE E-Invoicing | Provider configuration, submission and evidence permissions | E-invoicing access is appropriately restricted |
| P5 — Accounting and VAT | Financial permissions, sensitive exports and approval workflows | Financial operations follow explicit authorization rules |
| P6 — Procurement and Inventory | Purchasing, stock adjustment and operational permissions | Inventory operations are appropriately scoped |
| P7 — HRMS and Payroll | Sensitive employee data, payroll permissions and self-service access | HR and payroll access is restricted |
| P8 — Projects, Expenses and Assets | Project membership, expenses and asset permissions | Operational scope is enforced |
| P9 — Banking and Advanced Finance | Payment, banking and reconciliation permissions | High-risk financial operations are controlled |
| P10 — Reporting and Integrations | Export controls, API credentials and integration authorization | Derived data and external access are protected |
| P11 — Enterprise Readiness | MFA enforcement, privileged-access workflows and security hardening | Enterprise security controls are validated |
| P12 — Production Launch | Security verification, monitoring and incident readiness | Production authentication and authorization acceptance |

Core authentication and authorization must be implemented before business modules rely on them.

A later phase may add more specialized permissions, but it must not introduce a weaker security model.

---

# 28. Pending Decisions

The following decisions require explicit approval and documentation.

| ID | Decision | Required outcome |
|---|---|---|
| IAM-DEC-001 | Login identifier | Confirm email-based login or an alternative |
| IAM-DEC-002 | User registration | Select self-registration, invitation-only or controlled onboarding |
| IAM-DEC-003 | Email verification | Define when verification is mandatory |
| IAM-DEC-004 | MFA | Define mandatory roles and tenant-level policy |
| IAM-DEC-005 | Browser sessions | Define idle timeout, absolute lifetime and revocation |
| IAM-DEC-006 | API authentication | Define mechanisms for browser, mobile and external clients |
| IAM-DEC-007 | Role storage | Select Django permissions, custom models or a documented hybrid |
| IAM-DEC-008 | Permission scopes | Define tenant, legal-entity, branch and record-assignment behavior |
| IAM-DEC-009 | Custom roles | Define tenant-administrator customization boundaries |
| IAM-DEC-010 | Support access | Define approvals, duration, scope and audit requirements |
| IAM-DEC-011 | Impersonation | Decide whether it is required and define safeguards |
| IAM-DEC-012 | Separation of duties | Define required maker-checker workflows |
| IAM-DEC-013 | Session revocation | Define revocation behavior after security and membership changes |
| IAM-DEC-014 | SSO | Determine whether enterprise OIDC or SAML support is required |
| IAM-DEC-015 | Audit retention | Define event categories, retention and access policy |
| IAM-DEC-016 | Rate limiting | Define limits and abuse-response behavior |
| IAM-DEC-017 | Sensitive exports | Define which permissions are required for each data category |

Record approved decisions in:

`docs/01-architecture/ARCHITECTURAL_DECISIONS/`

Do not treat an unresolved decision as approved merely because a developer selected an implementation.

---

# 29. Instructions for Codex and Development Agents

All development agents must follow this document.

## 29.1 Before implementing a protected feature

The agent must identify:

- Required authentication.
- Account-status requirements.
- Tenant membership requirements.
- Required permissions.
- Legal-entity and branch scope.
- Object-level restrictions.
- Module entitlements.
- Sensitive-field restrictions.
- Approval and state-transition requirements.
- Audit requirements.
- Background-task implications.
- API or integration exposure.

## 29.2 During implementation

The agent must:

- Use the configured Django authentication framework.
- Use explicit tenant-aware authorization.
- Keep tenant membership separate from role assignment.
- Keep permissions separate from commercial entitlements.
- Validate ownership server-side.
- Apply object-level authorization.
- Protect sensitive fields and exports.
- Use established authentication and recovery mechanisms.
- Apply CSRF protection where cookie-based authentication requires it.
- Add positive and negative tests.
- Record relevant security events.
- Follow the established application-service architecture.

## 29.3 Prohibited shortcuts

Agents must not:

- Treat login as authorization.
- Trust a tenant ID from request data.
- Rely on frontend button visibility.
- Assume a UUID makes a record inaccessible.
- Use `is_staff` as a tenant role.
- Use `is_superuser` as a substitute for explicit platform authorization.
- Grant all permissions to a tenant administrator.
- Treat a module entitlement as a user permission.
- Treat a user permission as a module entitlement.
- Store plaintext passwords or recovery tokens.
- Implement custom password hashing.
- Log access tokens, passwords or secrets.
- Create tenant-scoped APIs without authorization tests.
- Bypass RLS to simplify a feature.
- Report unexecuted tests as passing.

## 29.4 Required evidence

For each protected feature, the agent must report:

1. Authentication requirements.
2. Required permissions.
3. Tenant and organizational scope.
4. Module-entitlement behavior.
5. Object-level authorization behavior.
6. Security-sensitive changes.
7. Audit events added.
8. Tests executed and actual results.
9. Known limitations.
10. Any unresolved authorization decisions.

---

# 30. Definition of Done

The authentication and permissions foundation is ready for production consideration only when all applicable requirements are satisfied.

## Identity and authentication

- [ ] Custom Django user model is configured before production migrations.
- [ ] Passwords are handled by Django's supported password-hashing framework.
- [ ] Login and recovery endpoints have abuse protection.
- [ ] Account status is enforced.
- [ ] Email verification behavior is defined.
- [ ] Session security settings are configured.
- [ ] Logout and session revocation are tested.
- [ ] MFA policy is defined and implemented for required accounts.

## Tenant membership

- [ ] Users can belong to multiple tenants where authorized.
- [ ] Membership is validated server-side.
- [ ] Roles are assigned independently for each tenant.
- [ ] Revoked and suspended memberships are denied.
- [ ] Tenant switching revalidates authorization.
- [ ] Legal-entity and branch restrictions are enforced.

## Authorization

- [ ] A central permission catalogue exists.
- [ ] Role assignments are scoped and auditable.
- [ ] Object-level access is enforced.
- [ ] Sensitive fields and exports have appropriate restrictions.
- [ ] Approval and state-transition permissions are explicit.
- [ ] Tenant administrators cannot grant prohibited privileges.
- [ ] Platform and tenant administration are separated.

## Module entitlements

- [ ] Permissions and module entitlements are separate controls.
- [ ] Required module dependencies are evaluated.
- [ ] Entitlement revocation takes effect according to the defined policy.
- [ ] Cached authorization decisions are invalidated or revalidated.

## Database and operational security

- [ ] Tenant isolation follows `MULTI_TENANCY.md`.
- [ ] PostgreSQL RLS protects tenant-owned records.
- [ ] Runtime database credentials cannot bypass RLS.
- [ ] Background tasks use explicit execution context.
- [ ] Django admin follows the same authorization principles.
- [ ] Audit events cover relevant security-sensitive actions.
- [ ] Security tests cover both allowed and denied access.
- [ ] Monitoring and incident-response procedures are documented.

**Release rule:** No feature may be released if it allows an authenticated user to perform an operation outside their authorized tenant, role, scope or module entitlement.

---

# 31. Official Technical References

Use the documentation matching the project's pinned versions.

- Django authentication: https://docs.djangoproject.com/en/5.2/topics/auth/
- Django custom user models: https://docs.djangoproject.com/en/5.2/topics/auth/customizing/
- Django password management: https://docs.djangoproject.com/en/5.2/topics/auth/passwords/
- Django sessions: https://docs.djangoproject.com/en/5.2/topics/http/sessions/
- Django security: https://docs.djangoproject.com/en/5.2/topics/security/
- Django CSRF protection: https://docs.djangoproject.com/en/5.2/ref/csrf/
- Django REST Framework authentication: https://www.django-rest-framework.org/api-guide/authentication/
- Django REST Framework permissions: https://www.django-rest-framework.org/api-guide/permissions/
- PostgreSQL Row Security Policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html

These references provide implementation guidance. They do not replace the project's threat model, code review, security testing or production configuration review.

---

# 32. Final Architectural Rule

Authentication and authorization must be consistent across every entry point.

```text
Identity
   |
   v
Account Status
   |
   v
Tenant Membership
   |
   v
Permission Assignment
   |
   v
Organizational Scope
   |
   v
Module Entitlement
   |
   v
Object-Level Authorization
   |
   v
Business-State Validation
   |
   v
PostgreSQL RLS and Integrity Constraints
   |
   v
Authorized Operation
```

This is the common security foundation for CRM, sales, invoicing, UAE e-invoicing, accounting, VAT, procurement, inventory, HRMS, payroll, projects, expenses, fixed assets, banking and reporting.

No module may introduce a weaker authorization path.

The architecture provides a framework for secure implementation; production readiness must be established through working code, reviewed configuration, database-role verification, automated security tests and operational evidence.