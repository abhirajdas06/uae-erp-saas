# Security Requirements — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | QUAL-SEC-001 |
| Version | 1.0 |
| Status | APPROVED BASELINE |
| Date | 28 October 2026 |
| Owner | Security Lead / Architecture |
| Reviewers | Product, Security, Privacy, Architecture, DevOps, QA, Domain Owners |
| Applies To | P00–P12 and every production-bound change |

## 1. Purpose

This document defines the minimum security requirements for the modular, multi-tenant ERP SaaS platform. It converts the approved architecture controls into implementation and verification obligations without claiming UAE legal, regulatory, or privacy compliance.

The baseline is risk-based. It uses OWASP ASVS 5.0.0 Level 2 as the default application-security target and requires additional Level 3-style assurance where threat modelling identifies high-impact privileged administration, financial posting, payroll, banking, identity, regulatory evidence, bulk export, secrets, or cross-tenant operations. Exact ASVS identifiers must include the standard version when added to the traceability matrix.

NIST SP 800-218 SSDF 1.1 provides the secure-development lifecycle structure. Framework and infrastructure controls must also follow supported-version vendor guidance.

## 2. Authority and Interpretation

Normative terms `MUST`, `MUST NOT`, `SHOULD`, and `MAY` have their ordinary requirements meaning.

Authority order:

1. Explicit current human-approved requirements and ADRs.
2. This document after approval.
3. Approved phase, module, and task specifications.
4. Current supported-version vendor guidance.
5. Informative security guidance and implementation recommendations.

When a standard conflicts with an accepted ADR or validated legal requirement, stop the affected work and record the conflict. Passing a scanner does not establish security, privacy, or regulatory compliance.

## 3. Security Assurance Model

Every feature or material change MUST identify:

- Assets and data classifications affected.
- Tenant, legal-entity, branch, actor, and support boundaries.
- Trust boundaries and untrusted inputs.
- Abuse cases and failure impact.
- Applicable requirements from this document.
- Required automated and manual evidence.
- Residual risks, owner, and disposition.

Threat modelling is mandatory before implementing authentication, tenant context, privileged administration, financial posting, payroll, banking, e-invoicing, file handling, external APIs, provider callbacks, bulk import/export, cross-tenant support, cryptographic key handling, or production infrastructure.

## 4. Security Requirements

### SEC-001 — Secure development lifecycle

Security requirements MUST be traced from product and architecture decisions through design, implementation, tests, review, release evidence, vulnerability response, and lessons learned.

**Acceptance criteria:**

1. Each authorized task identifies applicable security requirements and risks.
2. High-risk designs receive security review before implementation is committed.
3. Findings have severity, owner, due date, and disposition.
4. Release evidence identifies unresolved security exceptions.
5. Recurring defects produce root-cause and prevention actions.

**Verification:** Traceability review, design review, CI/release evidence, and finding register inspection.

### SEC-002 — Tenant isolation and trusted context

Tenant isolation MUST be enforced across requests, services, ORM queries, raw SQL, tasks, caches, files, reports, exports, search, logs, administration, backups, and integrations according to [ADR-002](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-002-shared-postgresql-database-and-schema.md), [ADR-004](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-004-tenant-isolation-and-postgresql-rls.md), and [ADR-014](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-014-uuid-primary-keys-and-tenant-aware-references.md).

**Acceptance criteria:**

1. Tenant context originates from authenticated and authorized server-side state, never an unvalidated client identifier.
2. Tenant-owned records have an authoritative ownership path and critical relationships enforce same-tenant integrity.
3. RLS-covered transactions use `app.current_tenant_id` transaction-locally under a non-owner, non-superuser, non-`BYPASSRLS` runtime role.
4. Missing or invalid tenant context fails closed.
5. Negative tests cover cross-tenant IDs, parent references, tasks, caches, files, reports, and privileged paths.

**Verification:** Architecture tests, restricted-role PostgreSQL tests, service/API tests, and security review.

### SEC-003 — Identity and authentication

Identity and authentication MUST follow [ADR-005](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-005-authentication-and-authorization-model.md) and supported Django security mechanisms.

**Acceptance criteria:**

1. A custom Django user model is established before initial production migrations.
2. Password storage uses a supported adaptive password hasher; custom cryptography is prohibited.
3. Login, recovery, verification, MFA, and credential-change flows resist enumeration, replay, brute force, and session fixation.
4. Platform-privileged access requires MFA; sensitive tenant roles receive a risk-based MFA policy.
5. Authentication events are rate-limited, monitored, and audited where material.

**Verification:** Authentication tests, abuse tests, configuration review, and audit inspection.

### SEC-004 — Session and browser security

Production browser sessions MUST use HTTPS-only secure cookies, appropriate `HttpOnly` and `SameSite` behavior, CSRF protection, host validation, origin controls, and security headers. `DEBUG` MUST be false in production.

**Acceptance criteria:**

1. HTTP is redirected to HTTPS and HSTS is enabled only after deployment validation.
2. Proxy trust is explicit; forwarded headers are not trusted from arbitrary sources.
3. Unsafe browser operations require CSRF protection unless a documented non-cookie boundary replaces it.
4. Clickjacking, MIME sniffing, referrer leakage, and unsafe cross-origin behavior are controlled.
5. Session rotation, expiry, logout, and revocation behavior are tested.

**Verification:** Configuration tests, browser security tests, deployment inspection, and supported Django checks.

### SEC-005 — Authorization, object scope, and separation of duties

Authorization MUST be deny-by-default and independently evaluate tenant membership, role/permission, organizational scope, object ownership, sensitive fields, workflow state, separation of duties, and entitlement under [ADR-005](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-005-authentication-and-authorization-model.md) and [ADR-006](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-006-module-entitlement-and-dependency-enforcement.md).

**Acceptance criteria:**

1. Hiding navigation or guessing-resistant identifiers never substitutes for authorization.
2. List, detail, create, update, delete, export, task, and bulk operations enforce consistent scope.
3. Protected fields are server-owned or explicitly allowlisted; mass assignment is prevented.
4. Support, impersonation, emergency, and cross-tenant access are purpose-bound, time-bounded where appropriate, monitored, and audited.
5. Denied, revoked, disabled, expired, and conflicting-role scenarios are tested.

**Verification:** Permission matrix review and negative service/view/API/task tests.

### SEC-006 — Input, output, template, and query safety

All untrusted input MUST be validated at the trust boundary and all output encoded for its context. ORM and parameterized database operations are required; dynamic SQL, commands, templates, URLs, redirects, and serialized data require explicit safe construction.

**Acceptance criteria:**

1. Server-side schemas define type, length, format, range, allowed values, and ownership.
2. Django template autoescaping remains enabled; approved sanitization is required for stored rich content.
3. SQL, command, template, header, path, spreadsheet-formula, and log injection are addressed where applicable.
4. Server-side request forgery controls restrict destinations, schemes, DNS/IP behavior, redirects, and credentials.
5. Errors return safe stable codes without secrets, stack traces, or cross-tenant existence disclosure.

**Verification:** Unit/property tests, injection tests, code review, and security testing.

### SEC-007 — API, webhook, and integration security

External interfaces MUST follow [ADR-008](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-008-selective-use-of-django-rest-framework.md), [ADR-012](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-012-uae-e-invoicing-provider-integration-boundary.md), and [ADR-020](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-020-api-versioning-and-external-integration-contracts.md).

**Acceptance criteria:**

1. Every interface has an owner, consumer, version, authentication, authorization, tenant, entitlement, rate-limit, audit, and data-classification policy.
2. Webhooks verify the strongest provider-supported authenticity mechanism, exact signed bytes, timestamp/replay rules, and connection/tenant mapping.
3. State-changing APIs define idempotency, concurrency, timeout, duplicate, and ambiguous-outcome behavior.
4. Provider credentials and tokens are least-privileged, rotatable, and never logged.
5. Contract tests include invalid authentication, cross-tenant references, replay, over-posting, and unknown versions.

**Verification:** OpenAPI/schema review, integration tests, replay tests, and provider-contract evidence.

### SEC-008 — File, document, import, and export safety

Files MUST follow [ADR-019](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-019-file-and-document-storage.md).

**Acceptance criteria:**

1. Production objects are private; metadata establishes tenant, owner, classification, state, checksum, and lifecycle.
2. Uploads use generated keys, size/type limits, content inspection, quarantine, and risk-based malware scanning.
3. Files cannot be downloaded before authorization of identity, tenant, parent, scope, and state.
4. Signed URLs are short-lived and narrowly scoped; active content uses safe disposition and isolation.
5. Exports are tenant-scoped at query time, audited where required, expire, and are cleaned up.
6. Orphan, missing, corrupt, and failed-deletion conditions are reconciled and observable.

**Verification:** File security tests, malicious fixtures, cross-tenant tests, lifecycle tests, and restore/reconciliation exercises.

### SEC-009 — Data classification, minimization, and privacy engineering

Every domain MUST classify personal, employee, payroll, identity, banking, tax, financial, credential, regulatory, and confidential customer data. Collection, access, display, export, telemetry, lower-environment use, retention, and deletion MUST follow the approved purpose and least-data principle.

**Acceptance criteria:**

1. Sensitive fields and files have owner, purpose, audience, and retention category.
2. Production data is not copied to lower environments without explicit authorization and effective de-identification controls.
3. Support and analytics access are bounded and audited.
4. Legal hold and deletion operations are authorized, observable, and do not silently destroy protected evidence.
5. UAE privacy, residency, and retention obligations remain subject to authoritative legal validation.

**Verification:** Data-flow review, access review, fixture inspection, retention tests, and specialist review.

### SEC-010 — Cryptography and transport protection

Approved, maintained platform cryptography MUST be used. Custom cryptographic algorithms or protocols are prohibited.

**Acceptance criteria:**

1. External and administrative traffic uses currently approved TLS configuration.
2. Passwords use supported password hashing, not reversible encryption.
3. Encryption keys have owners, scope, rotation, backup/recovery, and revocation procedures.
4. Random tokens and identifiers use cryptographically secure generation where unpredictability is required.
5. Certificate and key expiry are monitored.

**Verification:** Configuration review, dependency review, key-management runbook, and transport tests.

### SEC-011 — Secrets and configuration

Secrets MUST follow [ADR-017](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-017-secrets-and-environment-configuration.md).

**Acceptance criteria:**

1. Secrets are absent from source, images, ordinary database tables, logs, fixtures, build arguments, and documentation.
2. Production secrets are injected at runtime through an approved backend and scoped identity.
3. Critical configuration is typed, validated, and fails closed at startup.
4. Rotation and compromise procedures are tested for material credentials.
5. CI and untrusted workflows cannot read deployment or production secrets.

**Verification:** Secret scanning, image inspection, configuration tests, access review, and rotation exercise.

### SEC-012 — Audit, logging, monitoring, and alerting

Audit events, diagnostic logs, and telemetry MUST remain distinct under [ADR-018](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-018-audit-logging-and-sensitive-data-handling.md).

**Acceptance criteria:**

1. Material security, authorization, support, financial, export, retention, and administrative events have defined audit triggers.
2. Critical audit evidence commits with the protected state or through an equally durable design.
3. Passwords, tokens, keys, cookies, and prohibited sensitive payloads never enter logs.
4. Audit access, export, retention, and deletion are restricted and themselves audited.
5. Alerts exist for cross-tenant attempts, privileged access, repeated denials, secret anomalies, audit failures, bulk export, and critical integration failures.

**Verification:** Audit coverage tests, redaction tests, tamper attempts, access review, and alert exercises.

### SEC-013 — Background jobs, queues, and durable events

Background work MUST follow [ADR-009](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-009-celery-redis-and-background-task-execution.md) and [ADR-010](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-010-transactional-outbox-and-event-delivery.md).

**Acceptance criteria:**

1. Messages contain minimal identifiers, not secrets or unbounded sensitive payloads.
2. Workers reload authoritative tenant and operation state and establish trusted tenant context.
3. Material tasks are idempotent and safe under duplicate, late, concurrent, and reordered delivery.
4. Deserialization is restricted to approved safe formats and task names/queues are controlled.
5. Poison messages, retry exhaustion, stuck operations, and outbox lag are observable and recoverable.

**Verification:** Task tests, duplicate/concurrency tests, queue configuration review, and failure simulation.

### SEC-014 — Financial and regulated workflow security

Financial controls MUST preserve [ADR-011](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-011-financial-data-integrity-and-immutable-posted-entries.md) and [ADR-013](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-013-monetary-precision-currency-and-rounding.md).

**Acceptance criteria:**

1. Posting/finalization validates permission, separation of duties, tenant/legal entity, period, balance, currency, idempotency, and concurrency.
2. Protected posted values cannot be silently updated or deleted.
3. Corrections use linked reversal, credit, adjustment, cancellation, or approved reopening workflows.
4. Regulatory state is not inferred from transport success or provider marketing claims.
5. Financial and UAE-specific rules require finance/tax/legal validation before implementation acceptance.

**Verification:** Transaction, authorization, immutability, reconciliation, provider-failure, and specialist-review evidence.

### SEC-015 — Dependency and software-supply-chain security

Dependencies, actions, images, and build inputs MUST be inventoried, pinned or constrained through an approved policy, scanned, and updated within risk-based service targets.

**Acceptance criteria:**

1. Python and frontend dependency manifests are locked and reviewed.
2. CI actions are pinned to immutable revisions and receive minimum permissions.
3. Builds produce provenance and software-component evidence where the release process requires it.
4. Unsupported runtime/framework versions block production release.
5. Critical exploitable findings block release unless an authorized, expiring exception documents compensating controls.

**Verification:** Dependency/secret/image scans, CI configuration review, SBOM/provenance evidence where adopted, and vulnerability register.

### SEC-016 — Container, host, and deployment security

Deployment MUST follow [ADR-016](../01-architecture/ARCHITECTURAL_DECISIONS/ADR-016-docker-based-deployment-architecture.md).

**Acceptance criteria:**

1. Images use supported pinned bases, locked dependencies, non-root processes, minimal content, and no embedded secrets.
2. Runtime filesystems, Linux capabilities, networks, service identities, and administrative access are least-privileged where the platform permits.
3. Web, worker, scheduler, and migration roles have explicit commands and permissions.
4. Database migrations run as a controlled release operation, not concurrently from every replica.
5. Image and configuration promotion preserves traceable immutable artifacts.

**Verification:** Image scan, runtime configuration inspection, deployment test, and release evidence.

### SEC-017 — Backup, recovery, retention, and secure disposal

Backups and recovery MUST protect confidentiality and integrity while meeting approved RPO/RTO targets.

**Acceptance criteria:**

1. Database, object, configuration-reference, and required audit data are within documented backup scope.
2. Backup credentials and storage are segregated and access-controlled.
3. Restore tests verify completeness, tenant isolation, object/metadata consistency, and application usability.
4. Retention, legal hold, deletion, and media disposal are approved and auditable.
5. A shared restore cannot be used casually for one tenant; tenant-level recovery has a reviewed procedure.

**Verification:** Restore exercise, access review, reconciliation evidence, and operational approval.

### SEC-018 — Vulnerability and incident management

The project MUST define coordinated vulnerability intake, triage, remediation, disclosure, emergency release, incident response, evidence preservation, and post-incident improvement.

**Acceptance criteria:**

1. Findings use a documented severity model that includes tenant, financial, privacy, and regulatory impact.
2. Remediation targets and escalation paths are approved.
3. Security contacts and supported-version policy are published internally before production.
4. Incident exercises cover credential compromise, cross-tenant exposure, malicious upload, provider compromise, and data integrity failure.
5. Exceptions require owner, rationale, compensating controls, expiry, and human acceptance.

**Verification:** Process review, issue evidence, incident tabletop, and exception audit.

## 5. Release Security Gates

A production release MUST NOT proceed with:

- A known exploitable critical vulnerability without explicit executive/security risk acceptance.
- A failing tenant-isolation, authorization, secret-exposure, posted-financial-integrity, destructive-migration, or backup/restore gate.
- Unsupported core runtime or framework versions.
- Unresolved production secrets in source, image, logs, or artifacts.
- Missing evidence for applicable high-risk requirements.
- An unreviewed material change to an accepted ADR.

Medium and lower findings follow approved remediation targets. A green scanner does not replace code review, threat modelling, or negative tests.

## 6. Security Evidence and Traceability

Each security requirement maps to:

- Product requirement and ADR.
- Threat or abuse case.
- Implementing control and owner.
- Automated test or manual verification procedure.
- Evidence location and execution date.
- Finding or exception where unmet.

Evidence MUST avoid production secrets and unnecessary personal or financial data.

## 7. ADR Control Map

| Security area | Primary ADR controls |
|---|---|
| Architecture and ownership | ADR-001, ADR-003 |
| Shared data and tenant isolation | ADR-002, ADR-004, ADR-014 |
| Identity, authorization, entitlements | ADR-005, ADR-006 |
| Browser and API boundaries | ADR-007, ADR-008, ADR-020 |
| Tasks and reliable delivery | ADR-009, ADR-010 |
| Financial and regulated workflows | ADR-011, ADR-012, ADR-013 |
| CI, deployment, and supply chain | ADR-015, ADR-016, ADR-017 |
| Audit and sensitive data | ADR-018 |
| Files and documents | ADR-019 |

## 8. Standards and Authoritative References

Verified 28 October 2026:

- [OWASP ASVS 5.0.0](https://asvs.owasp.org/) — application security requirements and verification baseline.
- [NIST SP 800-218 SSDF 1.1](https://csrc.nist.gov/pubs/sp/800/218/final) — secure software development lifecycle practices.
- [Django security guidance](https://docs.djangoproject.com/en/stable/topics/security/) — supported framework security controls and deployment responsibilities.
- [PostgreSQL Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) — RLS behavior, owner/bypass behavior, and policy controls.
- [GitHub Actions security guidance](https://docs.github.com/en/actions/how-tos/secure-your-work) — workflow permissions, immutable action pinning, OIDC, and artifact integrity.
- [Docker build secrets](https://docs.docker.com/build/building/secrets/) — safe build-time secret handling.
- [OpenAPI Specification](https://spec.openapis.org/oas/) — machine-readable external API contracts.
- `docs/00-product/PRODUCT_REQUIREMENTS.md`, especially IAM-001–IAM-005, AUD-001, OPS-001–OPS-004, and NFR-001–NFR-011.

Standards versions and supported vendor versions MUST be reviewed at least annually and before a major production release.

## 9. Approval

**Current Status:** APPROVED BASELINE

- **Recommended option:** Adopt this risk-based security baseline, using ASVS 5.0.0 Level 2 by default and enhanced assurance for high-impact ERP workflows.
- **Approved By:** Product Owner — explicit market-standard review instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** This document does not approve UAE legal interpretations, retention periods, hosting region, providers, cryptographic products, or residual security risks.

## 10. Change Log

| Version | Date | Status | Description |
|---|---|---|---|
| 1.0 | 28 October 2026 | APPROVED BASELINE | Initial security requirements baseline linked to ADR-001 through ADR-020; approval excludes legal interpretations and residual-risk acceptance. |
