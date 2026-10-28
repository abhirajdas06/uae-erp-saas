# ADR-017: Secrets and Environment Configuration

| Field | Details |
|---|---|
| ADR ID | ADR-017 |
| Title | Secrets and Environment Configuration |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 28 October 2026 |
| Decision Owner | Security Lead / DevOps Lead |
| Reviewers | Architecture, Security, Development, DevOps, Operations, Privacy |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-004, ADR-005, ADR-009, ADR-012, ADR-015, ADR-016, ADR-018, ADR-019, ADR-020 |
| Related Requirements | IAM-001, INT-001–INT-002, OPS-001, NFR-001–NFR-003, DEP-001–DEP-003 |
| Related Documents | `AGENTS.md`, `SYSTEM_ARCHITECTURE.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `DATABASE_DESIGN.md`, `EVENT_AND_TASK_PROCESSING.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The platform requires Django signing keys, database and Redis credentials, email credentials, API tokens, webhook secrets, provider certificates, encryption keys, object-storage credentials, monitoring credentials, and deployment identities. It also needs non-secret environment configuration such as hostnames, feature availability, timeouts, limits, and service endpoints.

Embedding these values in source code, images, ordinary database tables, documentation, CI logs, or copied `.env` files creates material compromise and configuration-drift risks. Treating every configuration value as a secret also makes change control and diagnostics unnecessarily difficult.

## 2. Decision Drivers

- No production secrets in source control, images, logs, or ordinary artifacts.
- Typed, validated, fail-safe configuration.
- Strong separation between development, test, staging, and production.
- Least-privilege credentials by service role and tenant/provider scope.
- Rotation, revocation, compromise response, and auditability.
- Replaceable secrets backend without spreading provider APIs through the application.
- Clear distinction between deploy-time, runtime, tenant, and business configuration.

## 3. Options Considered

### Option A: Typed environment configuration with an approved secrets backend

Non-secret deployment settings enter through environment/runtime configuration; secrets are injected from a managed or otherwise approved protected store through a narrow settings boundary.

**Advantages:** source separation, deployment portability, startup validation, rotation, and limited application coupling.

**Disadvantages:** secret-store integration, permissions, bootstrap, and outage behavior require design.

### Option B: `.env` files for all environments

**Advantages:** simple local workflow.

**Disadvantages:** easy copying, weak rotation and audit, accidental commits, and unsafe production distribution.

### Option C: Encrypted secrets committed to the repository

**Advantages:** versioned configuration and disaster recovery if key management is sound.

**Disadvantages:** decryption-key bootstrap, broad repository exposure, rotation complexity, and risk of plaintext leakage in CI or local tools.

### Option D: Secrets stored in ordinary application tables

**Advantages:** tenant administration convenience.

**Disadvantages:** database readers gain credentials, encryption-key circularity, unsafe ORM/log exposure, and difficult least privilege.

## 4. Decision

Use typed Django settings with explicit configuration sources. Non-secret deployment configuration may be supplied through environment variables or approved mounted configuration. Production secrets must be supplied at runtime through an approved secrets-management mechanism and exposed to the application only through the settings/integration boundary that needs them.

Local development may use an ignored `.env` file generated from a secret-free `.env.example`. Production must not depend on manually distributed plaintext `.env` files as the normal secrets system.

The specific production secrets product is deferred until hosting and operational requirements are approved.

### 4.1 Configuration classification

Classify each setting as:

- Public build configuration.
- Non-secret deployment configuration.
- Secret credential or key.
- Tenant or legal-entity business configuration.
- Provider/integration configuration.
- Effective-dated regulated or financial policy.

Environment variables are appropriate for deployment configuration, not for modelling mutable business policy or large structured tenant configuration.

### 4.2 Settings structure

Maintain a shared base settings module plus explicit environment-specific composition. Parse settings through typed validation that defines required status, format, range, safe default, and secret classification.

Production startup must fail closed for missing or unsafe critical settings, including secret keys, allowed hosts, database connectivity, security flags, or mandatory integration references. Development defaults must not silently become production defaults.

### 4.3 Secret references

Ordinary business tables may store a secret reference, version, provider/account association, status, and safe metadata, but not the raw secret unless an approved encrypted-secret design explicitly requires it.

Application code accesses secrets through a narrow adapter and must not expose the value to templates, serializers, task payloads, audit metadata, or routine logs.

### 4.4 Least privilege and separation

Use distinct credentials where practical for:

- Web runtime.
- Celery workers and specialized queues.
- Database migrations.
- Database backup and restore.
- Monitoring.
- CI build and test.
- Deployment.
- Each external provider environment/account.

Production, staging, test, and local environments use separate credentials and cryptographic material. Tenant-scoped provider secrets must not be usable for another tenant.

### 4.5 Secret delivery and bootstrap

Secret delivery may use an approved runtime identity, mounted secret file, protected environment injection, or secrets API. The mechanism must avoid placing values in image layers, command-line arguments, build logs, process listings, or world-readable files.

The bootstrap identity must be narrowly scoped and recoverable. Failure to retrieve a required secret must produce a safe unavailable state, not a hardcoded fallback.

### 4.6 Rotation and versioning

Every long-lived secret type must define owner, rotation trigger, maximum approved lifetime where applicable, version, activation, overlap, revocation, and rollback behavior.

Systems using signing or encryption keys may need controlled multi-key verification/decryption during rotation. Rotation must not silently make historical encrypted data or signed messages unreadable.

### 4.7 Compromise response

For suspected exposure:

1. Contain and revoke the affected credential.
2. Identify environments, tenants, systems, and data within scope.
3. Rotate dependent credentials or keys.
4. Review logs and audit evidence without revealing the secret further.
5. Restore service safely.
6. Record incident and follow-up controls.

Secret values must never be copied into the incident record.

### 4.8 CI and build controls

Build jobs do not need production runtime secrets. Test jobs use dedicated synthetic credentials. Deployment secrets are available only to protected, authorized workflows and environments.

Secret scanning must cover source, commits where available, images, configuration examples, logs, and relevant generated artifacts. Detection requires revocation; deleting the visible string from the latest file is not sufficient.

### 4.9 Logging, diagnostics, and errors

Mark secret settings and fields for redaction. Avoid dumping environment dictionaries, Django settings, provider requests, headers, connection strings, or exception objects that may embed credentials.

Diagnostic tooling should report presence, version, and safe fingerprint where necessary—not the value.

### 4.10 Configuration change control

Environment configuration changes require review, validation, deployment identity, timestamp, and rollback plan proportional to risk. Changes affecting security, tenant isolation, finance, providers, or retention require the applicable approval.

Tenant business configuration and regulated rules remain in audited application workflows, not ad hoc environment changes.

### 4.11 Encryption keys

Keys used for application-level encryption are separate from ordinary provider credentials and require an approved key-management, access, rotation, recovery, and destruction design. Losing an encryption key can be equivalent to losing data; exposing it can compromise all protected records.

## 5. Rationale

Typed settings catch unsafe configuration before serving traffic. A narrow secrets boundary supports different hosting environments without coupling business domains to a vendor. Separating deployment settings from tenant and regulated configuration preserves auditability and appropriate change workflows.

## 6. Consequences

### Positive consequences

- Lower risk of committed or baked-in credentials.
- Explicit startup validation and environment separation.
- Granular rotation and revocation.
- Replaceable production secrets backend.

### Negative consequences and trade-offs

- Secret-store availability and bootstrap become operational dependencies.
- Rotation-compatible application code adds complexity.
- Local development needs documented onboarding.
- Some third-party libraries may expose secrets unless carefully configured.

### Risks and mitigations

- **Environment leakage:** prefer protected injection, restrict process/host access, and redact diagnostics.
- **Secret-store outage:** bounded caching only where approved and safe failure behavior.
- **Over-broad runtime identity:** per-role policies and regular access review.
- **Rotation outage:** versioned overlap and tested rollback.
- **Accidental commit:** ignored local files, examples without values, and secret scanning.

## 7. Security and Tenant-Isolation Implications

- Tenant/provider credentials are scoped and retrieved only after trusted tenant resolution.
- Client-supplied secret references are not trusted.
- Runtime identities must not list or retrieve unrelated tenant secrets.
- RLS does not protect an external secrets backend; its access policy needs independent review.
- Secret access and administrative changes require protected audit events without values.

## 8. Data Integrity and Migration

- Configuration schema changes are versioned and backwards-compatible during deployment overlap.
- Secret-reference migrations preserve provider/account/environment ownership.
- Encryption-key rotation and data re-encryption require resumable, auditable migrations and recovery.
- Rollback must account for configuration and key versions, not only code.

## 9. Operational Impact

Operations must manage secret inventory, ownership, expiry, access review, rotation, emergency revocation, backup/recovery of key-management metadata, and alerts for failed or unusual secret access. The actual secret manager, availability design, and cost remain deployment decisions.

## 10. Implementation Requirements

1. Create a canonical environment-variable and configuration specification.
2. Implement typed startup validation and production-safe defaults.
3. Maintain `.env.example` without real values and ignore local secret files.
4. Select and integrate an approved production secrets backend.
5. Define per-role credentials and provider/tenant scoping.
6. Add redaction, secret scanning, rotation, and compromise runbooks.
7. Define key-management requirements before application-level encryption.
8. Test missing, malformed, rotated, revoked, and unavailable secret behavior.

## 11. Validation and Acceptance Criteria

- [ ] No real secret exists in source, image layers, examples, or ordinary artifacts.
- [ ] Production rejects missing or unsafe critical configuration.
- [ ] Development defaults cannot silently activate in production.
- [ ] Web, worker, migration, CI, and deployment identities are appropriately separated.
- [ ] Tenant/provider credentials cannot be retrieved across scope.
- [ ] Logs, errors, audit events, and diagnostics redact secret values.
- [ ] Rotation works without unauthorized overlap or unrecoverable data loss.
- [ ] Revoked credentials stop working within the approved window.
- [ ] CI from untrusted changes cannot access protected secrets.
- [ ] Compromise response and recovery are exercised.

## 12. Alternatives Rejected

- Production plaintext `.env` distribution as the primary secrets system is rejected.
- Secrets committed to source or baked into images are rejected.
- Raw provider credentials in ordinary configuration tables are rejected.
- One shared credential for all process roles or tenants is rejected.
- Hardcoded fallback secrets are rejected.

## 13. References

- `AGENTS.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- Django deployment checklist: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
- OWASP Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Typed environment configuration plus a narrow, approved production secrets backend.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; production secret backend, key management, rotation intervals, and emergency access remain unresolved.

The production secrets product, key-management design, rotation intervals, and emergency-access process remain unresolved and block production configuration. Documentation and safe examples may proceed.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial secrets and environment-configuration decision accepted after standards review. |
