# Architectural Decision Records (ADRs)

**Project:** UAE ERP SaaS Platform  
**Document Type:** Architecture Governance  
**Status:** Active  
**Version:** 1.1

## 1. Purpose

This directory contains Architecture Decision Records (ADRs) documenting significant technical and architectural decisions made during the development of the platform.

ADRs establish a consistent source of truth for human developers, Codex agents, reviewers, and deployment engineers.

## 2. ADR Principles

1. Each significant architectural decision must have its own ADR.
2. ADRs must explain the context and problem before stating the decision.
3. Alternatives must be considered for material architectural choices.
4. Each decision must document its consequences and trade-offs.
5. Accepted decisions must not be silently overridden by code changes or AI agents.
6. Superseded decisions must remain in the repository for historical traceability.
7. Proposed decisions must not be treated as approved implementation requirements.
8. Regulatory and compliance-related decisions must identify the authoritative sources and validation required.
9. ADRs must remain consistent with the master product specification, system architecture, database design, security requirements, and phase specifications.
10. Material changes to an accepted decision require a new ADR or a documented revision process.

## 3. Naming Convention

Use this naming convention:

`ADR-NNN-short-description.md`

Examples:

- `ADR-001-modular-monolith.md`
- `ADR-002-shared-database-multi-tenancy.md`
- `ADR-003-django-application-structure.md`
- `ADR-004-tenant-isolation-and-rls.md`

Assign each ADR a unique, sequential number. Never reuse a number.

## 4. Status Definitions

- **PROPOSED:** Under discussion; not approved.
- **ACCEPTED:** Approved and authoritative.
- **REJECTED:** Considered and rejected.
- **SUPERSEDED:** Replaced by a newer decision.
- **DEPRECATED:** No longer recommended, but not necessarily replaced.

## 5. Decision-Making Process

1. Identify a significant architectural question.
2. Review existing ADRs and architecture documents.
3. Draft a new ADR with the problem, constraints, alternatives, and recommendation.
4. Identify security, data integrity, tenancy, operational, commercial, and regulatory implications.
5. Obtain the required human approval.
6. Mark the ADR as ACCEPTED only after approval.
7. Update affected architecture documents and implementation tasks.
8. Add tests or architecture checks where the decision can be enforced automatically.
9. Record any superseding decisions without deleting the original ADR.

## 6. Rules for Codex Agents

Codex agents must:

- Read relevant ADRs before implementing architecture-sensitive changes.
- Treat ACCEPTED ADRs as authoritative unless a higher-priority approved requirement supersedes them.
- Never assume a PROPOSED ADR is approved.
- Never silently alter an accepted architectural decision.
- Raise a conflict when implementation requirements contradict an accepted ADR.
- Propose a new ADR when a material architectural change is necessary.
- Update affected documentation and tests after an approved change.
- Avoid creating duplicate ADRs for decisions already documented.
- Record unresolved questions in the appropriate project decision register.

## 7. ADR Register

This register is the canonical ADR numbering sequence. Other documents must reference this sequence and must not assign a different topic to an existing identifier.

`Record state` describes whether an ADR file exists. `Decision status` uses the controlled ADR statuses in Section 4. A not-yet-drafted candidate has no decision status because no decision record exists yet.

| ADR | Topic | Record state | Decision status | Record |
|---|---|---|---|---|
| ADR-001 | Modular monolith architecture | DRAFTED | ACCEPTED | [ADR-001](ADR-001-modular-monolith-architecture.md) |
| ADR-002 | Shared PostgreSQL database and schema | DRAFTED | ACCEPTED | [ADR-002](ADR-002-shared-postgresql-database-and-schema.md) |
| ADR-003 | Django application and domain ownership | DRAFTED | ACCEPTED | [ADR-003](ADR-003-django-application-and-domain-ownership.md) |
| ADR-004 | Tenant isolation and PostgreSQL RLS | DRAFTED | ACCEPTED | [ADR-004](ADR-004-tenant-isolation-and-postgresql-rls.md) |
| ADR-005 | Authentication and authorization model | DRAFTED | ACCEPTED | [ADR-005](ADR-005-authentication-and-authorization-model.md) |
| ADR-006 | Module entitlement and dependency enforcement | DRAFTED | ACCEPTED | [ADR-006](ADR-006-module-entitlement-and-dependency-enforcement.md) |
| ADR-007 | Server-rendered UI with HTMX and Tailwind CSS | DRAFTED | ACCEPTED | [ADR-007](ADR-007-server-rendered-ui-with-htmx-and-tailwind.md) |
| ADR-008 | Selective use of Django REST Framework | DRAFTED | ACCEPTED | [ADR-008](ADR-008-selective-use-of-django-rest-framework.md) |
| ADR-009 | Celery, Redis, and background task execution | DRAFTED | ACCEPTED | [ADR-009](ADR-009-celery-redis-and-background-task-execution.md) |
| ADR-010 | Transactional outbox and event delivery | DRAFTED | ACCEPTED | [ADR-010](ADR-010-transactional-outbox-and-event-delivery.md) |
| ADR-011 | Financial data integrity and immutable posted entries | DRAFTED | ACCEPTED | [ADR-011](ADR-011-financial-data-integrity-and-immutable-posted-entries.md) |
| ADR-012 | UAE e-invoicing provider integration boundary | DRAFTED | ACCEPTED | [ADR-012](ADR-012-uae-e-invoicing-provider-integration-boundary.md) |
| ADR-013 | Monetary precision, currency, and rounding | DRAFTED | ACCEPTED | [ADR-013](ADR-013-monetary-precision-currency-and-rounding.md) |
| ADR-014 | UUID primary keys and tenant-aware references | DRAFTED | ACCEPTED | [ADR-014](ADR-014-uuid-primary-keys-and-tenant-aware-references.md) |
| ADR-015 | Automated testing and CI quality gates | DRAFTED | ACCEPTED | [ADR-015](ADR-015-automated-testing-and-ci-quality-gates.md) |
| ADR-016 | Docker-based deployment architecture | DRAFTED | ACCEPTED | [ADR-016](ADR-016-docker-based-deployment-architecture.md) |
| ADR-017 | Secrets and environment configuration | DRAFTED | ACCEPTED | [ADR-017](ADR-017-secrets-and-environment-configuration.md) |
| ADR-018 | Audit logging and sensitive-data handling | DRAFTED | ACCEPTED | [ADR-018](ADR-018-audit-logging-and-sensitive-data-handling.md) |
| ADR-019 | File and document storage | DRAFTED | ACCEPTED | [ADR-019](ADR-019-file-and-document-storage.md) |
| ADR-020 | API versioning and external integration contracts | DRAFTED | ACCEPTED | [ADR-020](ADR-020-api-versioning-and-external-integration-contracts.md) |

The sequence is a documentation roadmap, not a requirement to create unnecessary ADRs. Before drafting a candidate, verify that it represents a material decision and is not adequately governed by an existing accepted ADR. Retired candidates remain listed with an explanatory note so identifiers are not silently reused.

## 8. Register Maintenance

1. Reserve the next identifier in this register before creating a new ADR.
2. Change `Record state` to `DRAFTED` only when the corresponding file exists and passes the ADR format check.
3. Copy the status from the ADR file; never infer approval from detailed or mandatory language in another document.
4. Link unresolved approval requests from `docs/07-project-management/DECISIONS_PENDING.md`.
5. Record supersession in both the old and replacement ADRs and in this register.
6. Do not renumber existing ADR files. Correct conflicting references in the referring document.

## 9. Definition of Done

An ADR is complete when:

- Its identifier is unique.
- Its context and problem are explicit.
- Alternatives and trade-offs are documented.
- Its decision and status are clear.
- Security, tenancy, data integrity, operations, and compliance implications are addressed where relevant.
- A human approval is recorded when required.
- Related documentation and implementation tasks are identified.
- Conflicts with existing accepted ADRs have been resolved.
