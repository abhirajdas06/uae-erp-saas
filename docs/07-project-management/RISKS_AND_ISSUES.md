# Risks and Issues Register — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | PM-RISK-001 |
| Version | 1.0 |
| Status | Active |
| Last Updated | 28 October 2026 |

## 1. Purpose

This register tracks material technical, security, product, commercial, regulatory, and operational uncertainty. Detailed controls remain in their owning specifications and ADRs.

Severity values are `CRITICAL`, `HIGH`, `MEDIUM`, and `LOW`. Status values are `OPEN`, `MITIGATING`, `ACCEPTED`, `RESOLVED`, and `CLOSED`.

## 2. Active Risks

| ID | Risk | Severity | Status | Owner | Current mitigation / next evidence |
|---|---|---|---|---|---|
| RISK-001 | Tenant data can be exposed through inconsistent request, service, task, report, cache, file, or database scoping | CRITICAL | MITIGATING | Architecture / Security | Accepted ADR-002/004/014 and approved SEC-002/TST-004 define controls; implementation evidence remains required |
| RISK-002 | Draft architecture language may be treated as approved implementation direction | HIGH | MITIGATING | Architecture / Governance | ADR register separates record state from decision status; approval remains explicit |
| RISK-003 | Conflicting ownership of tenant membership may create competing models, migrations, or authorization paths | HIGH | RESOLVED | Architecture / Security | ADR-003 accepted and `DJANGO_APP_STRUCTURE.md` reconciled to `tenants.TenantMembership` on 28 October 2026 |
| RISK-004 | Inconsistent RLS context keys may produce denied operations, untested policies, or false isolation confidence | CRITICAL | RESOLVED | Security / Database | ADR-004 accepted and `MULTI_TENANCY.md` reconciled to `app.current_tenant_id` on 28 October 2026 |
| RISK-005 | Duplicated registries and scattered pending decisions may drift | HIGH | MITIGATING | Documentation / Governance | Canonical ADR, decision, risk, project, and phase registers established |
| RISK-006 | Reused or unmapped requirement and test identifiers may break traceability and acceptance reporting | HIGH | MITIGATING | QA / Documentation | P00 traceability baseline created; validate remaining namespaces, completeness, and executed evidence as phases progress |
| RISK-007 | Approved security/testing/CI standards may not be enforced consistently in implementation | HIGH | MITIGATING | Security / QA / DevOps | Initial validators/workflow are implemented and pass locally; hosted enforcement and later application gates remain required |
| RISK-008 | Unverified UAE regulatory assumptions may produce incorrect product behavior or compliance claims | HIGH | MITIGATING | Product / Compliance | ADR-012 establishes official-source and evidence gates; applicability, provider, schemas, dates, and specialist approval remain open |
| RISK-009 | Shared-database restore may have a multi-tenant blast radius and no validated tenant-level recovery path | CRITICAL | OPEN | DevOps / Database | Define RPO/RTO, backup architecture, restore tests, and tenant recovery procedure |
| RISK-010 | Financial rules may be implemented before precision, rounding, posting, reversal, and valuation policies are approved | CRITICAL | MITIGATING | Finance / Architecture | ADR-011 and ADR-013 are accepted; concrete finance and tax policies still require approval before implementation |
| RISK-011 | External retries may duplicate payments, e-invoices, or business effects | CRITICAL | MITIGATING | Architecture / Integration | Accepted ADR-009/010/012 require operation records, idempotency, outbox, and reconciliation; implementation tests remain required |
| RISK-012 | Missing Git metadata prevents reliable history, diff review, and change attribution | MEDIUM | RESOLVED | Repository Maintainer | Git repository root and working-tree visibility verified at `D:/Project/uae-erp-saas` on 28 October 2026 |
| RISK-013 | Scope expansion across the full ERP catalogue may bypass phase gates | HIGH | MITIGATING | Product / Orchestrator | Keep documentation-only mode; authorize bounded phases and tasks only |
| RISK-014 | Sensitive payroll, banking, tax, and employee data may receive insufficient access controls | CRITICAL | OPEN | Security / Domain Owners | Define data classification, least privilege, audit, export, retention, and security tests |
| RISK-015 | UUIDs may be mistaken for authorization or cross-tenant references may rely only on application validation | CRITICAL | MITIGATING | Architecture / Database / Security | ADR-014 requires tenant-scoped lookup, direct ownership, and composite constraints for critical relationships |
| RISK-016 | Provider integration may misrepresent timeout, transport success, or provider receipt as regulatory acceptance | CRITICAL | MITIGATING | Integration / Compliance | ADR-012 requires evidence-based statuses, uncertain-outcome reconciliation, and no unsupported compliance claims |
| RISK-017 | Containerization may be mistaken for production availability, backup, or recovery readiness | HIGH | MITIGATING | DevOps / Architecture | ADR-016 separates image/runtime design from topology, persistent data, RPO/RTO, and production approval |
| RISK-018 | Secrets may leak through source, images, CI, logs, task payloads, or shared credentials | CRITICAL | MITIGATING | Security / DevOps | ADR-017 requires runtime secret injection, scoped identities, redaction, scanning, rotation, and compromise response |
| RISK-019 | Audit records or logs may omit critical evidence or become an uncontrolled sensitive-data repository | CRITICAL | MITIGATING | Security / Compliance / Audit Owner | ADR-018 separates audit/log/telemetry purposes and requires minimization, append controls, access, and category retention |
| RISK-020 | CI may report false confidence through SQLite-only tests, skipped failures, unsafe secrets, or weak release gates | HIGH | MITIGATING | QA / DevOps / Security | Initial P00 gates fail closed and use no secrets; hosted evidence and later PostgreSQL/application gates remain required |
| RISK-021 | File metadata and object content may diverge, expose another tenant, preserve malicious content, or lose regulated evidence | CRITICAL | MITIGATING | Architecture / Security / Privacy / Operations | ADR-019 requires private storage, trusted metadata authorization, quarantine/scanning, checksums, immutable versions, reconciliation, and recovery tests |
| RISK-022 | External API, webhook, event, or provider contracts may drift silently and create incompatible or duplicate business effects | HIGH | MITIGATING | Architecture / Integration / QA / Product | ADR-020 requires explicit versions, machine-readable contracts, compatibility gates, idempotency, consumer inventory, and governed deprecation |
| RISK-023 | Documentation traceability may be mistaken for implemented or executed control evidence | HIGH | MITIGATING | QA / Governance | P00 matrix distinguishes documentation status from `NOT_RUN` application verification and requires evidence-linked status changes |
| RISK-024 | An approved P01 specification or test matrix may be mistaken for authorization or proof that tenant isolation is implemented | CRITICAL | MITIGATING | Product / Governance / Security | Approval is explicitly specification-only, all 53 tests are `NOT_RUN`, and entry requires P00 exit plus separate P01 authorization |
| RISK-025 | The dependency-free P00 secret scanner may miss novel, encoded, high-entropy, or history-only credentials | HIGH | MITIGATING | Security / DevOps | Initial patterns fail closed on recognized credentials; retain Git hygiene, review findings, and select a specialist history-aware scanner before application secrets or deployment workflows are introduced |

## 3. Active Issues

| ID | Issue | Severity | Status | Required resolution |
|---|---|---|---|---|
| ISSUE-001 | `SYSTEM_ARCHITECTURE.md` used a conflicting ADR-004–ADR-010 sequence | HIGH | RESOLVED | Canonical ADR sequence restored on 27 October 2026 |
| ISSUE-002 | Project status, phase status, decision, and risk registers were absent | HIGH | RESOLVED | Registers established on 27 October 2026 |
| ISSUE-003 | Some intended phase, module, agent, quality, and deployment directories/documents remain absent | MEDIUM | OPEN | `docs/02-phases/P00_FOUNDATION/` and `docs/05-quality/` now exist; create other units only when authorized and required |
| ISSUE-004 | Product and non-ADR architecture narratives required scoped approval/reconciliation | HIGH | RESOLVED | Repository-wide baseline review completed on 28 October 2026; open specialist decisions remain in the canonical register |
| ISSUE-005 | Authentication test IDs collided with product requirement IDs | HIGH | RESOLVED | Test scenarios renamed to IAM-TST-001 through IAM-TST-044 on 27 October 2026 |
| ISSUE-006 | Initial ADR roadmap was incomplete and lacked a set-level consistency/approval review | HIGH | RESOLVED | ADR-001 through ADR-020 are accepted; `ADR_INITIAL_SET_REVIEW.md` and `ADR_STANDARDS_REVIEW.md` preserve review and approval evidence |

## 4. Review Rules

- Review this register after every material ADR, phase transition, security finding, provider decision, or regulatory verification.
- A risk may be marked `ACCEPTED` only by an authorized human with rationale and review date.
- A risk is not `RESOLVED` merely because documentation describes a control; implementation and verification evidence are required where applicable.
- Critical and high risks must appear in phase exit reviews when they affect the phase scope.

## 5. Change Log

| Date | Change |
|---|---|
| 27 October 2026 | Established the canonical risk and issue register from the repository audit. |
| 28 October 2026 | Added file-storage and external-contract risks after ADR-019/020 and closed the initial ADR-set review issue. |
| 28 October 2026 | Recorded ADR acceptance, reconciled membership ownership and RLS context-key conflicts, and updated quality-governance risk status. |
| 28 October 2026 | Added P00 traceability-status risk and updated phase/documentation issues after creating the P00 specification and matrix. |
| 28 October 2026 | Added the P01 authorization/evidence risk after drafting the bounded P01 specification and tenant-isolation matrix. |
| 28 October 2026 | Updated quality, tenant-isolation, and document-state risks after scoped repository approval and the manifest/CI specifications. |
| 28 October 2026 | Recorded local completion evidence and remaining hosted-enforcement limitations for P00-T-001. |
