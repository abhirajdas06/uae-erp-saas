# Risks and Issues Register — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | PM-RISK-001 |
| Version | 1.0 |
| Status | Active |
| Last Updated | 27 October 2026 |

## 1. Purpose

This register tracks material technical, security, product, commercial, regulatory, and operational uncertainty. Detailed controls remain in their owning specifications and ADRs.

Severity values are `CRITICAL`, `HIGH`, `MEDIUM`, and `LOW`. Status values are `OPEN`, `MITIGATING`, `ACCEPTED`, `RESOLVED`, and `CLOSED`.

## 2. Active Risks

| ID | Risk | Severity | Status | Owner | Current mitigation / next evidence |
|---|---|---|---|---|---|
| RISK-001 | Tenant data can be exposed through inconsistent request, service, task, report, cache, file, or database scoping | CRITICAL | MITIGATING | Architecture / Security | ADR-002 and planned ADR-004; require cross-tenant tests under restricted PostgreSQL roles |
| RISK-002 | Draft architecture language may be treated as approved implementation direction | HIGH | MITIGATING | Architecture / Governance | ADR register separates record state from decision status; approval remains explicit |
| RISK-003 | Conflicting ownership of tenant membership may create competing models, migrations, or authorization paths | HIGH | OPEN | Architecture / Security | Resolve through ADR-003 and DEC-ARCH-003 before model creation |
| RISK-004 | Inconsistent RLS context keys may produce denied operations, untested policies, or false isolation confidence | CRITICAL | OPEN | Security / Database | Resolve DEC-SEC-002 and align examples before RLS implementation |
| RISK-005 | Duplicated registries and scattered pending decisions may drift | HIGH | MITIGATING | Documentation / Governance | Canonical ADR, decision, risk, project, and phase registers established |
| RISK-006 | Reused requirement and test identifiers may break traceability and acceptance reporting | HIGH | OPEN | QA / Documentation | Adopt separate test namespace and create traceability matrix |
| RISK-007 | Missing security and testing standards may allow inconsistent implementation gates | HIGH | OPEN | Security / QA | Create `SECURITY_REQUIREMENTS.md` and `TESTING_STRATEGY.md` during P00 documentation |
| RISK-008 | Unverified UAE regulatory assumptions may produce incorrect product behavior or compliance claims | HIGH | OPEN | Product / Compliance | Verify authoritative sources, record dates and applicability, require specialist review |
| RISK-009 | Shared-database restore may have a multi-tenant blast radius and no validated tenant-level recovery path | CRITICAL | OPEN | DevOps / Database | Define RPO/RTO, backup architecture, restore tests, and tenant recovery procedure |
| RISK-010 | Financial rules may be implemented before precision, rounding, posting, reversal, and valuation policies are approved | CRITICAL | OPEN | Finance / Architecture | ADR-011 and ADR-013 plus finance review before financial implementation |
| RISK-011 | External retries may duplicate payments, e-invoices, or business effects | CRITICAL | MITIGATING | Architecture / Integration | Planned ADR-009/010/012; require operation records, idempotency, outbox, and reconciliation |
| RISK-012 | Missing Git metadata prevents reliable history, diff review, and change attribution | MEDIUM | OPEN | Repository Maintainer | Initialize or attach the intended Git repository before implementation |
| RISK-013 | Scope expansion across the full ERP catalogue may bypass phase gates | HIGH | MITIGATING | Product / Orchestrator | Keep documentation-only mode; authorize bounded phases and tasks only |
| RISK-014 | Sensitive payroll, banking, tax, and employee data may receive insufficient access controls | CRITICAL | OPEN | Security / Domain Owners | Define data classification, least privilege, audit, export, retention, and security tests |

## 3. Active Issues

| ID | Issue | Severity | Status | Required resolution |
|---|---|---|---|---|
| ISSUE-001 | `SYSTEM_ARCHITECTURE.md` used a conflicting ADR-004–ADR-010 sequence | HIGH | RESOLVED | Canonical ADR sequence restored on 27 October 2026 |
| ISSUE-002 | Project status, phase status, decision, and risk registers were absent | HIGH | RESOLVED | Registers established on 27 October 2026 |
| ISSUE-003 | `docs/02-phases/` through the required governance and deployment directories are absent | MEDIUM | OPEN | Create only when the next authorized documentation unit requires them |
| ISSUE-004 | Product and architecture documents remain unapproved drafts | HIGH | OPEN | Conduct bounded reviews and record explicit human dispositions |

## 4. Review Rules

- Review this register after every material ADR, phase transition, security finding, provider decision, or regulatory verification.
- A risk may be marked `ACCEPTED` only by an authorized human with rationale and review date.
- A risk is not `RESOLVED` merely because documentation describes a control; implementation and verification evidence are required where applicable.
- Critical and high risks must appear in phase exit reviews when they affect the phase scope.

## 5. Change Log

| Date | Change |
|---|---|
| 27 October 2026 | Established the canonical risk and issue register from the repository audit. |
