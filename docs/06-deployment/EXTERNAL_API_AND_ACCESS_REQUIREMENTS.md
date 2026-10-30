# External API, Service and Access Requirements

| Property | Value |
|---|---|
| Document ID | DEP-API-001 |
| Status | APPROVED DOCUMENTATION BASELINE — PROVIDER SELECTION AND SPEND NOT AUTHORIZED |
| Owner | DevOps / Product Owner |
| Related documents | `../03-modules/INTEGRATIONS.md`, `../01-architecture/UAE_EINVOICING_PROVIDER_CONTRACT.md`, `../01-architecture/BANKING_PROVIDER_CONTRACT.md`, `ENVIRONMENT_VARIABLES.md`, `../05-quality/DATA_PROTECTION_AND_RETENTION.md` |

## 1. Purpose and Boundary

Development repeatedly stalls on access rather than on code: a credential nobody requested, an accreditation with a lead time, a sandbox that needs a contract first. This document lists every external API, service and account the platform needs, what is blocked without each, and how to obtain it.

It does not select a provider, authorize spend, or assert any provider's pricing, availability or capability. Those remain the decisions named in section 10. Technical integration behavior stays with `../03-modules/INTEGRATIONS.md` and the two provider contracts; this document covers acquisition and access only.

Every cost and lead time below is `REQUIRES_VERIFICATION`. None was obtained from a provider, and no quotation exists. Treat each as a question to ask, not a figure to plan with.

## 2. The Most Important Fact First

**P01 requires no external API at all.** The authorized phase covers the toolchain, settings, PostgreSQL roles, the custom user model, authentication, tenancy, membership, entitlement scaffolding and audit. Every dependency is local: PostgreSQL, Redis, Python packages and the existing GitHub repository.

A developer can therefore start today with no account to open and no credential to request. The first external dependency appears in P02 if a SaaS payment provider is in scope, and the first regulated one in P04.

## 3. Dependency Register

Classes: `DEV` is development tooling, `INFRA` is hosted infrastructure, `COMMERCIAL` is a paid business service, `REGULATED` requires an authorization, accreditation or licensed counterparty.

| ID | Dependency | Class | Needed from | Blocked without it |
|---|---|---|---|---|
| EXT-001 | GitHub repository and Actions | `DEV` | Now, in use | CI gates, evidence artifacts |
| EXT-002 | Python package index | `DEV` | P01 | Dependency installation |
| EXT-003 | Container image registry for PostgreSQL, Redis and base images | `DEV` | P01 | Local stack and CI containers |
| EXT-004 | Node package registry for the Tailwind build | `DEV` | First interface task | Asset pipeline |
| EXT-005 | Object storage, S3-compatible | `INFRA` | First file-handling task | Document and artifact storage under ADR-019 |
| EXT-006 | Secrets management backend | `INFRA` | First hosted environment | ADR-017 compliance; no production secret may sit in source or an ordinary table |
| EXT-007 | Hosting platform and managed PostgreSQL | `INFRA` | First hosted environment | Any deployment |
| EXT-008 | Domain registration, DNS and TLS certificates | `INFRA` | First hosted environment | Public access, secure cookies |
| EXT-009 | Transactional email provider and verified sending domain | `COMMERCIAL` | First notification task | Account invitation, credential reset, billing and regulatory notices |
| EXT-010 | Error tracking, metrics and log aggregation | `INFRA` | First hosted environment | `DEP-OBS-001` monitoring obligations |
| EXT-011 | SaaS subscription payment provider | `COMMERCIAL` | P02, if collection is in launch scope | Provider-domain billing collection |
| EXT-012 | SMS provider and sender identity | `COMMERCIAL` | Only if `DEC-NTF-001` puts SMS in scope | SMS channel; out of initial scope |
| EXT-013 | E-invoicing Accredited Service Provider | `REGULATED` | P04 | Structured e-invoice transmission and tax data reporting |
| EXT-014 | FTA taxpayer portal access for the tenant | `REGULATED` | P05 operationally | Nothing in the product; see section 5.2 |
| EXT-015 | Wage protection agent or bank channel | `REGULATED` | P07, if wage protection is in scope | Salary file submission |
| EXT-016 | Bank account data or payment connectivity | `REGULATED` | P09, only for Modes B, C or D | Nothing in Mode A; manual statement import needs no API |
| EXT-017 | Independent security testing supplier | `COMMERCIAL` | Before production launch | `DEC-SEC-006` release gate |

## 4. Development Tooling

| ID | Requirement |
|---|---|
| API-ACQ-001 | `EXT-001` is already available. Branch protection and required reviewers are configured under `DEC-DWF-002`; no new account is needed |
| API-ACQ-002 | `EXT-002` to `EXT-004` are public registries. Dependencies are pinned and vulnerability-scanned per `QUAL-SEC-001` SEC-015, and a private mirror is adopted only if an approved decision records the reason |
| API-ACQ-003 | Container registry pull limits apply to unauthenticated use and can fail CI unpredictably. Authenticate CI pulls, or mirror the images, before the first containerized pipeline |
| API-ACQ-004 | No development tooling account may hold a production credential, and no CI secret is readable by a pull request from a fork |

## 5. Regulated Dependencies

These have the longest lead times and the most prerequisites. Start them before the phase that needs them, not during it.

### 5.1 EXT-013 — E-Invoicing Accredited Service Provider

| Item | Detail |
|---|---|
| Why | The UAE model requires a structured electronic invoice exchanged through an accredited provider. A PDF or email is not an e-invoice |
| Who contracts | The **tenant** appoints its service provider. The platform integrates with it; the platform is not itself the taxpayer |
| Prerequisites | Tenant trade licence and Tax Registration Number; determination of the tenant's implementation category; the provider's own onboarding requirements |
| How to obtain | Select from the official accredited provider list recorded as `UAE-EINV-006`, complete the provider's commercial and technical onboarding, obtain sandbox credentials first, then production |
| Dated evidence | `UAE-EINV-003` records that for businesses at or above AED 50 million revenue the provider appointment deadline is 30 October 2026 and implementation is 1 January 2027. Applicability per tenant is a specialist determination under `DEC-REG-001` |
| Credentials | Provider-issued client credentials or certificate; held as secret-backend references only, never in a model field |
| Environments | Sandbox and production must be separately configured and separately credentialed. A sandbox acknowledgement is never evidence of a production submission |
| Verification | Conformance against the pinned profile per `ARCH-PINT-AE-002`, plus the provider evidence contract in `../01-architecture/UAE_EINVOICING_PROVIDER_CONTRACT.md` |
| Cost and lead time | `REQUIRES_VERIFICATION`. Obtain a written quotation and an onboarding timeline from at least two accredited providers before `DEC-INT-002` |

### 5.2 EXT-014 — Tax Authority Access

| Item | Detail |
|---|---|
| Why | VAT and corporate tax obligations are discharged by the tenant through the authority's own portal |
| Important | Do not assume a public filing API exists. `../01-architecture/DATABASE_DESIGN.md` section 2.1 requires controlled exports, preparation workpapers or documented manual procedures where no approved integration interface exists, rather than inventing one |
| Platform impact | None for access. The platform produces preparation reports `RPT-301`–`RPT-305`, which are explicitly not filings |
| Action | No credential is requested. If an official filing interface is later confirmed, it becomes a new dependency with its own decision and ADR |

### 5.3 EXT-015 — Wage Protection Channel

| Item | Detail |
|---|---|
| Why | Salary payment through the approved mechanism, where applicable to the tenant |
| Who contracts | The tenant, with its bank or an approved agent |
| Prerequisites | Employer establishment registration; employee records and bank or wage-card details; the exact file format version the receiving channel accepts |
| How to obtain | Through the tenant's bank or approved agent; the platform generates the file and never transmits on the tenant's behalf unless an approved decision says otherwise |
| Blocking unknown | `DEC-PAY-002` must establish applicability, the exact format version and the agent. Generation stays disabled until then, per `MOD-PAYROLL-001` |
| Cost and lead time | `REQUIRES_VERIFICATION` via the tenant's bank |

### 5.4 EXT-016 — Banking Connectivity

| Item | Detail |
|---|---|
| Why | Statement data and, optionally, payment initiation |
| Mode A needs nothing | The default scope is manual statement import and reconciliation. No API, no credential, no provider |
| Modes B, C, D | Account data access, payment preparation and payment initiation are independently gated regulated activities under `DEC-BANK-001` and `DEC-BANK-002`, and remain unreachable in the product until approved |
| Prerequisites if pursued | Bank or aggregator onboarding, consent framework, certificates, possibly a licensed activity assessment |
| Cost and lead time | `REQUIRES_VERIFICATION`. Treat as the longest lead time in the project |

## 6. Commercial and Infrastructure Dependencies

| ID | How to obtain and what to capture |
|---|---|
| EXT-005 | Select an S3-compatible provider in the approved region. Capture bucket policy proving no public access, encryption at rest, and lifecycle rules matching the retention classes in `../05-quality/DATA_PROTECTION_AND_RETENTION.md` |
| EXT-006 | Provision the approved secrets backend before any hosted environment. Capture the access policy, rotation schedule and audit configuration. Required by ADR-017 |
| EXT-007 | Depends on `DEC-PRIV-004` hosting region and residency, and `DEC-OPS-001`. Capture the region, data-at-rest location, backup location and the processing location of every sub-processor, per `PRIV-060` |
| EXT-008 | Register the domain, configure DNS, and automate certificate issuance and renewal. Capture the renewal mechanism; an expired certificate is an avoidable outage |
| EXT-009 | Create the account, verify the sending domain, publish SPF, DKIM and DMARC records, and execute a data-processing arrangement because the provider will handle `C3` personal data per `PRIV-023`. Capture the arrangement and the sub-processor entry before enabling |
| EXT-010 | Select providers for error tracking, metrics and logs. Configure redaction before sending any payload, because `ADR-018` and `PRIV-004` prohibit `C4` and `C5` data leaving in telemetry |
| EXT-011 | Required only if the platform collects subscription payments at launch. Prerequisites typically include a UAE commercial licence, a bank account and underwriting. Capture the settlement terms, the data-processing arrangement and the card-data boundary; the platform must never handle raw card data |
| EXT-012 | Only if `DEC-NTF-001` includes SMS. Sender identity registration is usually required for business messaging and has its own lead time |
| EXT-017 | Scope and engage an independent tester per `DEC-SEC-006`. Capture the scope, dates, findings and remediation evidence as the release gate record |

## 7. Credential Handling

| ID | Requirement |
|---|---|
| API-ACQ-010 | Every external credential is stored only as a reference to the approved secrets backend, per ADR-017 and `INTM-002`. A credential never appears in a model field, a repository file, a container image, a log, an export, a fixture or a support extract |
| API-ACQ-011 | Sandbox and production credentials are separate, separately scoped, and never share a secret name or environment variable value |
| API-ACQ-012 | Every credential records its owner, scope, environment, rotation due date and rotation procedure. An expiring credential raises an operational alert before expiry, per the `ARCH-NOTIFY-001` catalogue |
| API-ACQ-013 | Production credentials are never copied into a development, test, demonstration or CI environment, per `PRIV-063` and `TD-004` |
| API-ACQ-014 | A credential-like value in the repository fails the secret-scan gate. A deliberate placeholder is allowlisted explicitly with a recorded reason, per `TD-071` |
| API-ACQ-015 | Credential rotation is rehearsed before production launch, because an unrehearsed rotation during an incident is an outage |

## 8. Sandbox, Stubbing and Non-Production Policy

| ID | Requirement |
|---|---|
| API-ACQ-020 | Every external provider is stubbed at the adapter boundary by default. No test in the default suite performs a live external call, per `TD-044` |
| API-ACQ-021 | A test requiring a real sandbox credential is marked and excluded from the default suite, with its manual execution requirements recorded, per `TD-074` |
| API-ACQ-022 | Non-production environments never transmit to a real recipient, a real bank, a real tax authority or a real accredited provider. Outbound delivery is disabled, redirected to an approved sink, or allowlisted, and the active mode is visible at startup, per `NTF-053` |
| API-ACQ-023 | Contract fixtures captured from a sandbox record the capture date, endpoint, contract version and redaction applied, and contain no credential, per `TD-045` |
| API-ACQ-024 | A provider's sandbox behavior is never assumed to match production. Differences are recorded in the integration's contract version |

## 9. Acquisition Sequence

| When | Obtain | Why then |
|---|---|---|
| Now, for P01 | Nothing external | P01 is fully local |
| Before the first hosted environment | `EXT-006` secrets backend, `EXT-007` hosting and database, `EXT-008` domain and TLS, `EXT-010` observability | A hosted environment without a secrets backend forces a bad pattern that is expensive to undo |
| Before the first file feature | `EXT-005` object storage | Private storage must exist before documents are generated |
| Before the first notification | `EXT-009` email, with its data-processing arrangement | Security and billing notices are mandatory categories |
| P02, if collecting payment | `EXT-011` | Underwriting has a lead time |
| Start early, use at P04 | `EXT-013` accredited provider | Accreditation, contracting and onboarding are the dominant lead time, and a dated appointment deadline already exists |
| P07, if applicable | `EXT-015` wage protection channel | Format and agent must be confirmed first |
| P09, only if approved | `EXT-016` banking connectivity | Regulated; Mode A ships without it |
| Before launch | `EXT-017` security testing | A release gate, not an afterthought |

## 10. Pending Decisions

| ID | Decision | Owner |
|---|---|---|
| `DEC-INT-002` | E-invoicing accredited service provider and contracted capabilities | Product Owner with Legal, Security, Finance |
| `DEC-INT-001` | SaaS payment provider | Product Owner with Finance and Security |
| `DEC-BANK-002` | Banking provider, consent model and environments | Product Owner with Legal |
| `DEC-NTF-002` | Email provider, sending domain and data-processing terms | Product Owner with DevOps |
| `DEC-PAY-002` | Wage protection applicability, format version and agent | Payroll specialist |
| `DEC-PRIV-004` | Hosting region, data-at-rest location and residency | Product Owner with Legal |
| `DEC-OPS-001`–`DEC-OPS-005` | Provider, topology, service targets, recovery objectives and thresholds | Product Owner with DevOps |
| `DEC-SEC-006` | Independent security testing scope, timing and supplier | Product Owner |
| `DEC-NTF-001` | Whether SMS is in launch scope | Product Owner |

No provider is selected, no spend is authorized, no account is opened and no credential is provisioned by this document. Every cost and lead time stated as `REQUIRES_VERIFICATION` must be replaced with a written quotation before it informs a plan or a price.
