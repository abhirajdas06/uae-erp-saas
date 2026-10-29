# Platform Threat Model

| Property | Value |
|---|---|
| Document ID | QUAL-THREAT-001 |
| Status | PROPOSED BASELINE — SECURITY REVIEW APPROVAL REQUIRED |
| Owner | Security Review Agent / Product Architect |
| Method | STRIDE applied per trust boundary, with multi-tenant and financial abuse cases |
| Related documents | `SECURITY_REQUIREMENTS.md`, `../01-architecture/MULTI_TENANCY.md`, `../01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`, `../01-architecture/API_STANDARDS.md`, `DATA_PROTECTION_AND_RETENTION.md` |

## 1. Purpose and Boundary

`SECURITY_REQUIREMENTS.md` SEC-001 requires threat modelling within the secure development lifecycle, and ADR-016 and `../01-architecture/API_STANDARDS.md` reference a threat model as an input, but no document contains one. This document owns the system-level threat model.

This document owns assets, trust boundaries, threat actors, enumerated threats with their mitigating controls, abuse cases, residual risk and the per-task threat-modelling obligation. It does not restate the control requirements themselves, which remain with `SECURITY_REQUIREMENTS.md`, and it does not grant any security assurance. It is a design-analysis record, not evidence of a tested control.

No penetration test, security assessment or control verification has been performed. Every mitigation is `PLANNED` until the owning phase implements and evidences it.

## 2. Assets

| ID | Asset | Impact of compromise |
|---|---|---|
| AST-01 | Tenant financial records: ledgers, invoices, payments, tax positions | Financial loss, misstated statutory filings, loss of audit integrity, irrecoverable trust damage |
| AST-02 | Tenant master data: customers, suppliers, pricing, contracts | Commercial harm, competitive disclosure |
| AST-03 | Employee personal and payroll data: identity documents, salaries, bank details, end-of-service entitlements | Personal-data breach, legal exposure, payroll fraud |
| AST-04 | Banking data: account details, IBANs, payment instructions, wage protection files | Direct monetary theft, payment diversion |
| AST-05 | Authentication and authorization state: credentials, sessions, multi-factor factors, role and permission assignments | Full account or tenant takeover |
| AST-06 | Tenant isolation boundary itself | Catastrophic multi-tenant breach affecting every customer |
| AST-07 | Subscription and entitlement state | Revenue loss, unauthorized module access |
| AST-08 | E-invoicing submission data and provider credentials | Regulatory exposure, fraudulent submission under the tenant identity |
| AST-09 | Audit trail and evidence records | Undetectable fraud, loss of defensibility |
| AST-10 | Platform secrets, signing material and infrastructure credentials | Total platform compromise |
| AST-11 | Backups, exports, generated documents and report artifacts | Mass data disclosure through a secondary path |
| AST-12 | Platform availability | Business interruption for every tenant, missed statutory deadlines |

## 3. Trust Boundaries

| ID | Boundary | Crossing traffic |
|---|---|---|
| TB-01 | Public internet to edge and web tier | Unauthenticated and authenticated browser requests, provider webhooks |
| TB-02 | Authenticated user to tenant data scope | Every tenant-scoped read and write |
| TB-03 | Tenant to tenant | Must never be crossed by data, cache, file, task, sequence or report |
| TB-04 | Tenant user to platform administration | Provider-domain operations and support access |
| TB-05 | Application tier to database | Queries executed under a tenant context |
| TB-06 | Application tier to background workers, queue and cache | Serialized task payloads and tenant context propagation |
| TB-07 | Application tier to external providers: e-invoicing, banking, email, storage | Outbound business-significant requests and inbound callbacks |
| TB-08 | Application tier to object and file storage | Uploaded and generated tenant documents |
| TB-09 | Runtime to secrets and configuration source | Credential and configuration retrieval |
| TB-10 | Build and deployment pipeline to runtime | Code, dependencies, images and migrations |
| TB-11 | Production to operator, developer and agent access paths | Administrative and diagnostic access |
| TB-12 | Production to non-production environments | Data and configuration flow that must remain one-directional and sanitized |

## 4. Threat Actors

| ID | Actor | Capability and motive |
|---|---|---|
| ACT-01 | Unauthenticated internet attacker | Automated scanning, credential stuffing, exploitation of exposed surfaces |
| ACT-02 | Authenticated tenant user acting maliciously | Valid session seeking cross-tenant data, privilege escalation or entitlement bypass |
| ACT-03 | Authenticated tenant user acting in error | Accidental destructive or disclosing action |
| ACT-04 | Malicious tenant administrator | Full tenant authority used to attack the platform or other tenants |
| ACT-05 | Insider: platform operator, developer or support agent | Legitimate elevated access used beyond purpose |
| ACT-06 | Compromised external provider or provider impersonator | Forged callbacks, malicious responses, credential abuse |
| ACT-07 | Supply-chain attacker | Malicious dependency, image or build-pipeline compromise |
| ACT-08 | Automated agent acting outside authorized scope | Unsafe destructive or production-affecting operation |
| ACT-09 | Fraudulent business party | Payment diversion, forged document, fictitious transaction |

## 5. Threat Enumeration

Mitigation references name the controls in `SECURITY_REQUIREMENTS.md` and the governing ADRs. Every mitigation state is `PLANNED`.

### 5.1 TB-01 — Edge and Web Tier

| ID | STRIDE | Threat | Primary mitigations |
|---|---|---|---|
| THR-001 | Spoofing | Credential stuffing or password spraying against sign-in | SEC-003, rate limiting per `API_STANDARDS.md` section 17, multi-factor policy, lockout and alerting |
| THR-002 | Spoofing | Session token theft through transport or script injection | SEC-004, SEC-010, secure cookie attributes, content security policy, output escaping |
| THR-003 | Tampering | Cross-site request forgery on a state-changing operation | SEC-006, CSRF on all unsafe methods including HTMX fragments, no state change via GET |
| THR-004 | Information disclosure | Verbose errors, stack traces or debug surfaces exposing internals | SEC-006, SEC-012, correlation-identifier-only user messaging |
| THR-005 | Denial of service | Expensive query, report or export abuse exhausting shared capacity | Pagination and resource limits per `API_STANDARDS.md` sections 11 and 24, report resource classes, rate limiting |
| THR-006 | Elevation of privilege | Exploitation of an unauthenticated or misconfigured endpoint | SEC-001, endpoint exposure register, fail-closed defaults |

### 5.2 TB-02 and TB-03 — Tenant Isolation

| ID | STRIDE | Threat | Primary mitigations |
|---|---|---|---|
| THR-010 | Information disclosure | Insecure direct object reference to another tenant's record by identifier | SEC-002, SEC-005, ADR-004, ADR-014, tenant-scoped querysets, object-level authorization, neutral not-found responses |
| THR-011 | Information disclosure | Missing tenant filter in a new query, report, aggregate or export | ADR-004 database-level isolation as defense in depth, mandatory cross-tenant tests in `../02-phases/P01_CORE_PLATFORM/P01_TENANT_ISOLATION_TEST_MATRIX.md` |
| THR-012 | Information disclosure | Cache, session or fragment-cache key omitting tenant scope | SEC-002, tenant-inclusive cache keys, authorization-aware cache invalidation |
| THR-013 | Information disclosure | Background task, scheduled job or webhook handler executing without correct tenant context | SEC-013, ADR-009, explicit context propagation, prohibition on ambient worker context |
| THR-014 | Information disclosure | Generated file, report artifact or export served from a path lacking tenant authorization | SEC-008, ADR-019, private storage, authorized time-bounded access |
| THR-015 | Tampering | Client-supplied tenant identifier accepted as authoritative | `API_STANDARDS.md` section 6.2, server-side context resolution only |
| THR-016 | Information disclosure | Cross-tenant inference through error differences, timing, numbering or search results | Neutral responses, tenant-scoped lookup per `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md` SEQ-052 |
| THR-017 | Elevation of privilege | Database connection or migration path operating without isolation enforcement | ADR-004, ADR-002, least-privilege database roles, migration review |

### 5.3 TB-04 — Platform Administration and Entitlements

| ID | STRIDE | Threat | Primary mitigations |
|---|---|---|---|
| THR-020 | Elevation of privilege | Tenant user reaching a platform-administration function | SEC-005, `API_STANDARDS.md` section 7.6, separated administrative surface and roles |
| THR-021 | Elevation of privilege | Self-granting a role or permission beyond current authority | SEC-005, separation of duties, maker-checker on authority changes, full audit |
| THR-022 | Tampering | Direct manipulation of subscription or entitlement state to obtain unpaid modules | ADR-006, server-side entitlement evaluation, provider-domain ownership of subscription state |
| THR-023 | Repudiation | Administrative action taken without attributable record | SEC-012, ADR-018, immutable audit of authority and configuration change |
| THR-024 | Information disclosure | Support access to tenant data beyond purpose or duration | ADR-018, purpose-bound and time-bounded support access with tenant-visible audit |
| THR-025 | Elevation of privilege | Django administrative interface exposed in production | `API_STANDARDS.md` section 26.7, restricted or disabled administrative surface |

### 5.4 TB-05 and TB-06 — Data and Processing Tier

| ID | STRIDE | Threat | Primary mitigations |
|---|---|---|---|
| THR-030 | Tampering | SQL injection through raw query or unsafe construction | SEC-006, parameterized access, prohibition on unreviewed raw SQL |
| THR-031 | Tampering | Deserialization of an untrusted task payload executing code | SEC-013, safe serialization formats, schema-validated payloads |
| THR-032 | Tampering | Queue or cache reachable without authentication, allowing task injection | SEC-016, network isolation, authenticated broker and cache |
| THR-033 | Denial of service | Unbounded task retry, poison message or queue exhaustion | SEC-013, bounded retries, dead-letter handling, alerting |
| THR-034 | Tampering | Race condition producing double posting, double payment or duplicate numbering | ADR-011, `API_STANDARDS.md` sections 14 and 15, database constraints, locking, idempotency |
| THR-035 | Information disclosure | Sensitive data written to logs, traces, metrics or error trackers | SEC-012, ADR-018, redaction rules and log review |

### 5.5 TB-07 and TB-08 — External Providers and Storage

| ID | STRIDE | Threat | Primary mitigations |
|---|---|---|---|
| THR-040 | Spoofing | Forged provider webhook creating a false business or regulatory state | SEC-007, `API_STANDARDS.md` section 19.4, signature verification, fail-closed routing, replay protection |
| THR-041 | Tampering | Replayed provider callback duplicating a financial effect | `API_STANDARDS.md` section 19.5, inbox idempotency, durable intent records |
| THR-042 | Spoofing | Compromised provider credential used to submit under a tenant identity | SEC-011, secret-backend references only, rotation, scoped credentials, submission audit |
| THR-043 | Information disclosure | Server-side request forgery through a provider or callback URL | `API_STANDARDS.md` section 19.8, egress allowlisting, address validation |
| THR-044 | Tampering | Malicious uploaded file executed or served as active content | SEC-008, type and size validation, content scanning, non-executing private storage |
| THR-045 | Information disclosure | Object storage or generated document accessible without authorization | ADR-019, private buckets, no public URLs, signed time-bounded access |
| THR-046 | Denial of service | Provider outage or latency cascading into platform unavailability | Timeouts, circuit behavior, graceful degradation per `API_STANDARDS.md` section 24.5 |
| THR-047 | Repudiation | Loss of provider-native acknowledgement evidence for a regulatory submission | `../03-modules/INTEGRATIONS.md` INTM-007, retained provider evidence separate from internal status |

### 5.6 TB-09 to TB-12 — Supply Chain, Secrets and Operations

| ID | STRIDE | Threat | Primary mitigations |
|---|---|---|---|
| THR-050 | Information disclosure | Secret committed to the repository, image, log or documentation | SEC-011, ADR-017, secret scanning in CI, example-only configuration templates |
| THR-051 | Tampering | Malicious or compromised dependency reaching production | SEC-015, pinned dependencies, vulnerability scanning, review of new dependencies |
| THR-052 | Tampering | Build pipeline or image registry compromise | SEC-015, SEC-016, least-privilege pipeline credentials, reproducible builds |
| THR-053 | Elevation of privilege | Standing production access or shared administrative credentials | SEC-016, least privilege, individually attributable access, approval for elevation |
| THR-054 | Tampering | Destructive migration, reset or data operation executed without authorization | `AGENTS.md` sections 13 and 18, migration review, explicit authorization gates |
| THR-055 | Information disclosure | Production data copied into a development or test environment | SEC-009, `TEST_DATA_AND_FIXTURES.md`, prohibition with sanitization requirements |
| THR-056 | Information disclosure | Backup or export artifact exposed or retained beyond policy | SEC-017, encryption, access control, retention classes in `DATA_PROTECTION_AND_RETENTION.md` |
| THR-057 | Tampering | Automated agent performing an unauthorized production or destructive action | `AGENTS.md` sections 7 and 13, authorization gates, no agent-recorded approvals |
| THR-058 | Repudiation | Audit trail alteration or deletion concealing activity | ADR-018, append-only audit design, restricted and monitored access |

## 6. Financial and Business Abuse Cases

| ID | Abuse case | Primary mitigations |
|---|---|---|
| ABU-01 | Modify or delete a posted financial record to conceal activity | ADR-011 immutability, reversal-only correction, audit history |
| ABU-02 | Issue, then silently alter, a submitted tax invoice | ADR-011, ADR-012, submission evidence retention, credit-note-only correction |
| ABU-03 | Divert a supplier payment by altering bank details before a payment run | Maker-checker on bank-detail change, change audit, pre-payment verification, alerting |
| ABU-04 | Inflate or redirect payroll through unauthorized salary or bank-detail change | Separation of duties, payroll approval gate, change audit |
| ABU-05 | Approve one's own transaction across maker-checker | Separation-of-duties enforcement and tests under SEC-005 |
| ABU-06 | Back-date a document into a closed period to alter a filed position | Period-close enforcement, authorized and audited back-dating |
| ABU-07 | Exfiltrate the customer or employee base through export or report | Export permission, sensitive-column policy, disclosure audit, volume alerting |
| ABU-08 | Use an unsubscribed module through a direct endpoint | Server-side entitlement enforcement under ADR-006 on every endpoint and fragment |
| ABU-09 | Duplicate a payment or submission through retry or replay | Idempotency and duplicate-prevention controls |
| ABU-10 | Suppress a notification or audit entry to hide an action | Mandatory notification categories, append-only audit |

## 7. Residual Risk and Open Questions

| ID | Residual risk | Disposition |
|---|---|---|
| THR-RES-01 | A malicious tenant administrator retains full authority over that tenant's own data by design | Accepted by design; mitigated by audit, maker-checker and notification, not preventable |
| THR-RES-02 | Insider access by platform operators cannot be eliminated | Mitigated by least privilege, purpose binding, time bounding and tenant-visible audit; residual risk requires `DEC-SEC-005` acceptance |
| THR-RES-03 | Provider compromise outside platform control | Mitigated by evidence retention, reconciliation and fail-closed handling; residual risk remains with the provider decision |
| THR-RES-04 | Data residency and cross-border processing exposure | Unresolved pending hosting and privacy decisions in `DATA_PROTECTION_AND_RETENTION.md` |
| THR-RES-05 | Denial-of-service resilience limits | Unresolved pending infrastructure decisions `DEC-OPS-001` to `DEC-OPS-005` |
| THR-RES-06 | Effectiveness of every control above is unverified | No security testing has been performed; all mitigations are `PLANNED` |

## 8. Per-Task Obligation

| ID | Requirement |
|---|---|
| THR-100 | A task that crosses a trust boundary, adds an endpoint or fragment, changes authorization, touches tenant scoping, adds a provider, handles a file, or changes financial posting must identify the applicable threats from this document in its completion report |
| THR-101 | A task introducing a threat not listed here must propose an addition to this document rather than leaving it unrecorded |
| THR-102 | A new trust boundary or external provider requires a security review and may require an ADR |
| THR-103 | This threat model is reviewed at each phase gate and at each release gate, with a dated record |
| THR-104 | No task may report a threat as mitigated without naming the implemented control and its executed test |

## 9. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-SEC-005 | Accept or further mitigate the insider-access residual risk, including the support-access model and its tenant visibility | Product Owner / Security reviewer |
| DEC-SEC-006 | Approve the scope, timing and provider of independent security testing before production launch | Product Owner |
| DEC-SEC-007 | Approve the vulnerability severity, remediation-window and exception policy | Security reviewer |

These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`. This document provides no security assurance and claims no tested control.
