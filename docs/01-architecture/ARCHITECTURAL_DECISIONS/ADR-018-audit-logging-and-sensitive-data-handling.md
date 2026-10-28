# ADR-018: Audit Logging and Sensitive-Data Handling

| Field | Details |
|---|---|
| ADR ID | ADR-018 |
| Title | Audit Logging and Sensitive-Data Handling |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 28 October 2026 |
| Decision Owner | Security Lead / Audit Domain Owner |
| Reviewers | Architecture, Security, Privacy, Compliance, Finance, Operations, Product |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-003–ADR-006, ADR-009–ADR-017, ADR-019–ADR-020 |
| Related Requirements | IAM-005, AUD-001, OPS-001, OPS-004, NFR-001–NFR-003, REP-003 |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DATABASE_DESIGN.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `API_STANDARDS.md`, `EVENT_AND_TASK_PROCESSING.md`, `MULTI_TENANCY.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The ERP must explain material business and security actions: tenant and membership changes, privileged access, subscription changes, invoice issuance, financial posting and reversal, payroll finalization, e-invoicing operations, exports, provider changes, retention actions, and support access.

Application logs are also needed for troubleshooting and monitoring. Audit records and diagnostic logs have different purposes, integrity, access, and retention requirements. Recording too little prevents investigation; recording complete payloads, credentials, payroll data, bank details, identity documents, or customer files creates a second sensitive-data repository.

## 2. Decision Drivers

- Traceable business, security, support, and administrative actions.
- Append-oriented audit evidence protected from ordinary modification.
- Useful structured operational logs and correlation.
- Data minimization, redaction, access control, and category-specific retention.
- Tenant and platform-event separation.
- Reproducible evidence without logging entire sensitive records.
- Incident investigation, monitoring, legal hold, and controlled export.

## 3. Options Considered

### Option A: Separate audit events, application logs, and security telemetry

Use a domain audit store for material actions, structured logs for diagnostics, and monitoring/security signals for detection, linked by correlation identifiers.

**Advantages:** purpose-specific controls, minimized sensitive data, stronger audit integrity, and useful operations.

**Disadvantages:** multiple pipelines, schemas, retention policies, and access models.

### Option B: Use application logs as the audit trail

**Advantages:** one pipeline.

**Disadvantages:** logs may be sampled, rotated, redacted, reordered, or unavailable; they usually lack transactional integrity and stable business semantics.

### Option C: Store complete before/after objects for every change

**Advantages:** extensive detail.

**Disadvantages:** excessive personal and financial data, credential risk, large storage, retention conflicts, and difficult access control.

### Option D: Depend only on database logs or change-data capture

**Advantages:** broad technical visibility.

**Disadvantages:** weak actor/business context and possible exposure of raw data; not a substitute for domain audit events.

## 4. Decision

Maintain three distinct but correlated records:

1. **Audit events** for material business, security, authorization, support, and administrative actions.
2. **Application logs** for debugging, request/task/integration operation, and service health.
3. **Security and operational telemetry** for metrics, alerts, traces, and incident detection.

Audit events are owned by the `audit` domain and are append-oriented from the ordinary application perspective. Logs and telemetry are not authoritative business records.

### 4.1 Audit event schema

Audit events include, where applicable:

- Stable event ID and schema version.
- Tenant and legal-entity scope, or explicit platform-global classification.
- Actor type and stable actor reference; system/service identity when no human actor exists.
- Effective or impersonated/support actor distinction.
- Action code and outcome.
- Resource type and stable reference.
- Occurrence and recording timestamps.
- Request, correlation, causation, operation, and source references.
- Approved reason, approval reference, or support purpose where required.
- Minimal structured metadata and changed-field names or safe values where justified.

Do not make display names, email addresses, or mutable descriptions the only actor/resource identity.

### 4.2 Required audit categories

At minimum, specifications must evaluate audit requirements for:

- Authentication, MFA, credential, session, and account events.
- Tenant, membership, role, permission, and entitlement changes.
- Privileged support, impersonation, emergency, and cross-tenant access.
- Invoice issue/cancel/correct and financial post/reverse/period operations.
- VAT, payroll, inventory adjustment, bank reconciliation, and sensitive approvals.
- E-invoicing, payment, and provider configuration/status operations.
- Sensitive views, bulk exports, downloads, and evidence packages where policy requires.
- Retention, deletion, anonymization, legal hold, and restoration.
- Secret-reference, security-policy, deployment, and administrative configuration changes.

Each domain owns the meaning and trigger; the audit domain owns safe persistence and retrieval.

### 4.3 Transactional audit behavior

When an audit event is required to establish a critical business action, write it in the same PostgreSQL transaction as the state change or through an equally durable design. If required audit persistence fails, the protected state change must fail rather than commit without its evidence.

External outcomes and asynchronous follow-up use durable operation and outbox evidence. An audit event must not claim success before the authoritative operation reaches that state.

### 4.4 Audit integrity

- Ordinary application users cannot update or delete audit events.
- Runtime services may append only the event categories they are authorized to create.
- Corrections append a new event; they do not rewrite prior evidence.
- Audit access, export, retention, and deletion actions are themselves audited.
- Database roles, backups, and administrative procedures protect audit tables.

Cryptographic chaining, signed batches, write-once storage, or external archive may be introduced when threat, contractual, or regulatory requirements justify them. A normal append-oriented table is not represented as cryptographically tamper-proof.

### 4.5 Application logging

Use structured logs with timestamp, severity, component, environment, safe tenant reference where useful, request/correlation ID, task/operation/integration ID, error classification, and safe diagnostic context.

Do not log:

- Passwords, reset tokens, session IDs, API tokens, private keys, or connection strings.
- Full payment or bank credentials.
- Full payroll, identity-document, tax-document, provider, or customer payloads by default.
- Sensitive request/response headers or cookies.
- Unredacted environment or Django settings.

Stack traces are restricted to protected operational systems and still require redaction.

### 4.6 Sensitive-data classification

Every domain must classify sensitive fields and files, including personal data, credentials, payroll, bank details, tax identifiers, identity documents, health/leave information, financial margins, and confidential customer data.

Classification drives access, masking, encryption, audit, export, retention, lower-environment use, and incident response. “Tenant-owned” does not mean every tenant user may view the data.

### 4.7 Redaction and safe metadata

Redaction occurs before data reaches logs or third-party telemetry where possible. Use allowlisted structured metadata rather than blacklisting known secret names alone.

Audit metadata should record changed field names, safe categorical values, hashes, references, or approved before/after values only when necessary. Hashing low-entropy secrets or identifiers does not necessarily anonymize them.

### 4.8 Tenant isolation and support access

Tenant users can access only approved audit categories for their tenant and organizational scope. Platform audit access is separate from tenant administration and requires purpose-bound privileged authorization.

Cross-tenant searches, support views, and evidence exports require bounded scope, reason, monitoring, and audit. Query and storage systems must not use tenant context from untrusted log fields as authorization.

### 4.9 Retention, deletion, and legal hold

Define retention by record category, purpose, legal basis, contractual obligation, incident need, and storage location. Audit events, application logs, security telemetry, financial evidence, and temporary debug data must not share one arbitrary duration.

Retention changes are effective-dated and approved. Legal hold suspends eligible deletion. Expired data is deleted or anonymized through authorized, auditable jobs with failure and verification evidence.

Exact UAE and contractual retention periods require authoritative legal/compliance validation and are not set by this ADR.

### 4.10 Time and correlation

Use timezone-aware UTC event timestamps for technical ordering and retain separate legally meaningful business dates where applicable. Systems require reliable time synchronization. Correlation identifiers link requests, tasks, outbox events, provider attempts, and audit events without becoming authorization tokens.

### 4.11 Monitoring and alerting

Define alerts for suspicious authentication, cross-tenant attempts, privileged access, bulk export, audit-write failure, repeated authorization denial, secret-access anomalies, provider callback failures, unexpected audit deletion attempts, and logging/telemetry pipeline failure.

Alert content follows the same minimization and access controls.

### 4.12 Evidence exports

Evidence exports are reproducible, tenant-scoped, permission-controlled, watermarked or integrity-protected where required, and audited. They identify included sources and generation time without claiming legal sufficiency beyond reviewed requirements.

## 5. Rationale

Purpose separation prevents diagnostic logs from becoming an unreliable audit ledger and prevents audit events from becoming a dump of sensitive payloads. Transactional critical events preserve evidence with the business action, while structured correlation supports investigation across synchronous and asynchronous paths.

## 6. Consequences

### Positive consequences

- Reliable explanation of material actions.
- Better incident detection and troubleshooting.
- Reduced secret and sensitive-data exposure.
- Category-specific access and retention.
- Clear evidence boundary for financial and provider workflows.

### Negative consequences and trade-offs

- Multiple storage and operational pipelines.
- Domain teams must define safe audit schemas.
- Retention, export, and privileged access require ongoing governance.
- Stronger tamper evidence may add future cost and infrastructure.

### Risks and mitigations

- **Sensitive-data duplication:** allowlisted metadata, redaction, and classification review.
- **Audit gaps:** transactionally required events and coverage tests.
- **Tampering:** restricted append roles, monitored administration, backups, and optional stronger archive.
- **Excessive access:** separate roles, purpose-bound support, and access review.
- **Unmanageable volume:** event taxonomy, sampling only for diagnostics—not required audit—and category retention.

## 7. Security and Tenant-Isolation Implications

- Audit and log systems are security-sensitive data stores.
- Tenant association is validated from trusted execution context.
- Sensitive audit fields may require additional permissions beyond general audit access.
- Log aggregation, monitoring, backup, and support vendors require data-flow and processor review.
- Security monitoring must not become a cross-tenant data-exposure path.

## 8. Data Integrity and Migration

- Audit schema evolution is versioned and remains readable historically.
- Required audit and business state commit atomically where applicable.
- Backfills must distinguish reconstructed records from contemporaneous events.
- Retention migrations preserve legal holds and required financial evidence.
- Audit identifiers and resource references follow ADR-014.

## 9. Operational Impact

Operations must manage ingestion reliability, storage capacity, access review, retention jobs, legal holds, alert routing, time synchronization, incident preservation, and export procedures. Logging outages and dropped audit events require monitoring and severity rules.

## 10. Implementation Requirements

1. Define audit event taxonomy, schema versions, and domain ownership.
2. Define sensitive-data classification and logging allowlists.
3. Implement append-oriented audit persistence and restricted database roles.
4. Establish structured logging, correlation, redaction, and protected error reporting.
5. Define category-specific access, retention, legal hold, and deletion policies.
6. Add audit coverage, tamper-attempt, redaction, tenant-isolation, and failure tests.
7. Define monitoring, alerting, incident preservation, and evidence-export runbooks.
8. Select operational log/telemetry tooling only after security, residency, cost, and retention review.

## 11. Validation and Acceptance Criteria

- [ ] Material event categories have explicit triggers and owners.
- [ ] Required audit failure prevents the protected state change.
- [ ] Ordinary users cannot edit or delete audit history.
- [ ] Tenant users cannot access another tenant's audit or logs.
- [ ] Credentials and prohibited sensitive values are absent from logs and audit metadata.
- [ ] Privileged access and audit export are themselves audited.
- [ ] Correlation connects requests, tasks, provider operations, and audit events.
- [ ] Retention jobs respect legal holds and produce verification evidence.
- [ ] Historical audit schemas remain interpretable after deployment.
- [ ] Alert and evidence-export paths are access-controlled and tested.

## 12. Alternatives Rejected

- Application logs as the sole audit trail are rejected.
- Full-object before/after logging by default is rejected.
- Mutable audit history is rejected.
- One retention period for all telemetry and evidence is rejected.
- Claims of cryptographic immutability without an implemented mechanism are rejected.

## 13. References

- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- OWASP User Privacy Protection Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Separate append-oriented audit events, structured application logs, and security/operational telemetry with shared correlation and data minimization.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; taxonomy, classification, retention, stronger tamper evidence, and log/telemetry provider remain controlled follow-up decisions.

Exact event taxonomy, retention periods, sensitive-data classes, tamper-evidence mechanism, and log/telemetry provider remain unresolved. They block production audit and monitoring implementation but not further documentation.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial audit logging and sensitive-data handling decision accepted after standards review. |
