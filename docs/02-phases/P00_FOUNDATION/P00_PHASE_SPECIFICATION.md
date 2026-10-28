# P00 — Foundation and Architecture Phase Specification

| Property | Value |
|---|---|
| Phase ID | P00 |
| Legacy roadmap alias | P0 / `P0-FOUNDATION` |
| Document ID | P00-SPEC-001 |
| Version | 1.0 |
| Status | APPROVED SPECIFICATION |
| Date | 28 October 2026 |
| Phase Owner | Product Owner |
| Coordinators | Architecture / Project Governance |
| Required Reviewers | Product, Architecture, Security, QA, DevOps; Finance/UAE specialists where applicable |
| Current Authorization | Documentation and governance only |
| Implementation Authorization | Not granted |

## 1. Purpose

P00 establishes the approved, traceable foundation required before application implementation begins. It turns the product baseline, accepted ADRs, approved quality baselines, decisions, risks, and phase gates into a bounded evidence package.

This specification does not authorize Django project creation, application models, migrations, CI workflow files, production infrastructure, paid providers, or ERP feature implementation. Those activities require the task and phase authorization described below.

The canonical P00 traceability record is [P00_TRACEABILITY_MATRIX.md](P00_TRACEABILITY_MATRIX.md).

## 2. Authority and Source Documents

P00 is governed by:

- [Repository instructions](../../../AGENTS.md).
- [Master Product Specification](../../00-product/MASTER_PRODUCT_SPECIFICATION.md).
- [Product Requirements](../../00-product/PRODUCT_REQUIREMENTS.md).
- [Development Roadmap](../../00-product/DEVELOPMENT_ROADMAP.md).
- [System Architecture](../../01-architecture/SYSTEM_ARCHITECTURE.md).
- [ADR Register](../../01-architecture/ARCHITECTURAL_DECISIONS/README.md) and accepted ADR-001 through ADR-020.
- [ADR Standards Review](../../07-project-management/ADR_STANDARDS_REVIEW.md).
- [Security Requirements](../../05-quality/SECURITY_REQUIREMENTS.md), approved baseline.
- [Testing Strategy](../../05-quality/TESTING_STRATEGY.md), approved baseline.
- [Pending Decisions](../../07-project-management/DECISIONS_PENDING.md).
- [Risks and Issues](../../07-project-management/RISKS_AND_ISSUES.md).
- [Phase Status](../../07-project-management/PHASE_STATUS.md).

Accepted ADRs are authoritative where other architecture prose conflicts with them. Approved quality baselines govern applicable controls, while execution evidence and residual-risk decisions remain separate.

## 3. Objective

Establish a consistent, reviewable, secure, testable, and implementation-ready foundation for a bounded P01 increment while preserving explicit human approval for phase transition and implementation.

P00 succeeds when reviewers can answer, with linked evidence:

1. What product increment is being built first and what is excluded?
2. Which architecture decisions govern it?
3. Which unresolved decisions block it?
4. Which security and testing controls apply?
5. What evidence is required before implementation and before phase exit?
6. Who may approve the transition to P01?

## 4. Scope

### 4.1 Currently authorized documentation scope

- Maintain the product, module, commercial, and roadmap baselines.
- Maintain accepted ADRs and reconcile affected architecture narratives.
- Define and review security and testing standards.
- Establish requirement-to-control-to-test-to-evidence traceability.
- Maintain project, phase, decision, and risk registers.
- Define P00 and a bounded P01 specification.
- Define phase/task manifest schemas and CI requirements as documentation.
- Define review, approval, exception, and evidence-package procedures.
- Identify unresolved product, finance, UAE regulatory, provider, privacy, retention, and operational decisions.

### 4.2 Planned P00 engineering scope requiring separate authorization

The following may be authorized later as bounded P00 engineering tasks but are not authorized by this document:

- Create validated phase/task manifest schemas and initial manifest files.
- Create documentation validation scripts.
- Create the initial GitHub Actions documentation/quality workflow.
- Configure branch protection or repository settings.
- Select and pin initial developer tooling.
- Create safe, non-functional environment templates needed for an approved P01 bootstrap.

### 4.3 Explicit non-goals

P00 does not:

- Implement ERP business features or commercial modules.
- Create speculative Django apps, models, migrations, views, APIs, tasks, or templates.
- Select paid hosting, e-invoicing, payment, secret, storage, monitoring, or security providers.
- Establish UAE legal, tax, employment, privacy, retention, or compliance conclusions.
- Deploy to any production environment.
- Approve P01 implementation merely by completing documentation.
- Claim that architecture controls have been implemented or tested.

## 5. Entry Conditions

| ID | Entry condition | Current state | Evidence |
|---|---|---|---|
| P00-ENT-001 | Repository instructions exist | SATISFIED | `AGENTS.md` |
| P00-ENT-002 | Product and roadmap drafts exist | SATISFIED | `docs/00-product/` |
| P00-ENT-003 | Architecture baseline exists | SATISFIED | `docs/01-architecture/` |
| P00-ENT-004 | ADR governance exists | SATISFIED | ADR register/template |
| P00-ENT-005 | Project tracking registers exist | SATISFIED | `docs/07-project-management/` |
| P00-ENT-006 | Documentation-only authorization is explicit | SATISFIED | `AGENTS.md`, project status |

## 6. Work Packages

### P00-WP-01 — Product and requirement baseline

**Owner:** Product / Architecture  
**Authorization:** Documentation only

Deliverables:

- Review product scope, target market, commercial model, module catalogue, and roadmap for consistency.
- Confirm stable requirement identifiers and priorities.
- Separate launch-scope decisions from the complete product catalogue.
- Record unresolved product and commercial decisions with owners and consequences.

Completion evidence:

- Product-document review record.
- No unresolved identifier collision in the P00 scope.
- Launch-scope decision remains explicitly open if not approved.

### P00-WP-02 — Architecture and ADR baseline

**Owner:** Architecture  
**Authorization:** Documentation only

Deliverables:

- Maintain ADR-001 through ADR-020 and canonical status register.
- Reconcile architecture narratives to accepted ADRs.
- Validate domain ownership, tenancy, authorization, entitlement, task/event, financial, deployment, storage, and API boundaries.
- Record deviations through ADR governance.

Completion evidence:

- Accepted ADR register and approval record.
- Cross-ADR consistency checks.
- Reconciliation checklist with no unowned material conflict.

### P00-WP-03 — Security and testing baseline

**Owner:** Security / QA  
**Authorization:** Documentation only

Deliverables:

- Review and disposition `SECURITY_REQUIREMENTS.md`.
- Review and disposition `TESTING_STRATEGY.md`.
- Confirm P00 and P01 control/test applicability.
- Define exception, finding, flaky-test, and evidence rules.

Completion evidence:

- Explicit approval or revision record for both quality documents.
- Security and QA reviewer names/dates.
- No unresolved contradiction with accepted ADRs.

### P00-WP-04 — Traceability and evidence governance

**Owner:** QA / Documentation / Project Governance  
**Authorization:** Documentation only

Deliverables:

- Maintain `P00_TRACEABILITY_MATRIX.md`.
- Link P00 requirements, product requirements, ADRs, SEC/TST controls, verification, owners, and evidence.
- Define status vocabulary and gap handling.
- Define the P00 exit evidence index.

Completion evidence:

- Unique identifiers and valid links.
- Every mandatory P00 exit criterion has an owner and evidence expectation.
- Open items identify blocking effect and next action.

### P00-WP-05 — Decisions, risks, and governance

**Owner:** Product Owner / Project Governance  
**Authorization:** Documentation only

Deliverables:

- Maintain decision, risk, issue, project, and phase status records.
- Resolve phase-identifier governance.
- Identify which open decisions block P01 versus later phases.
- Define architecture/security exception procedures.

Completion evidence:

- No critical P01 blocker lacks an owner and decision route.
- Registers agree with source documents.
- Accepted risks contain explicit human authority, rationale, and review date.

### P00-WP-06 — P01 readiness definition

**Owner:** Product / Architecture / Security / QA  
**Authorization:** Documentation only

Deliverables:

- Create a bounded P01 specification limited to core platform, identity, tenant isolation, and minimum engineering foundation.
- Define P01 tasks, dependencies, non-goals, migrations, tests, and evidence.
- Map P01 requirements to accepted ADRs and quality controls.
- Identify the specific human authorization required to start P01.

Completion evidence:

- P01 scope is small enough for independent review and verification.
- Tenant isolation and authorization test matrix is explicit.
- No commercial ERP module is included prematurely.

### P00-WP-07 — Manifest and CI design

**Owner:** DevOps / QA / Project Governance  
**Authorization:** Documentation design only; files/tooling require separate task authorization

Deliverables:

- Specify phase/task manifest schema, validation rules, and status transitions.
- Specify initial CI jobs, commands, permissions, secrets boundary, evidence, and failure policy.
- Define protected-branch and release-gate recommendations.

Completion evidence:

- Reviewable schemas/workflow specification.
- Every job has a locally reproducible command or documented exception.
- No production/deployment credential is required for ordinary CI.

## 7. Deliverables Register

| ID | Deliverable | Required for exit | Current state |
|---|---|---|---|
| P00-DEL-001 | Product documentation baseline | Yes | APPROVED BASELINE; launch and specialist decisions remain |
| P00-DEL-002 | Architecture documentation baseline | Yes | APPROVED BASELINE; implementation evidence remains |
| P00-DEL-003 | ADR-001–ADR-020 | Yes | ACCEPTED |
| P00-DEL-004 | Security requirements | Yes | APPROVED BASELINE |
| P00-DEL-005 | Testing strategy | Yes | APPROVED BASELINE |
| P00-DEL-006 | P00 traceability matrix | Yes | APPROVED VERIFICATION BASELINE |
| P00-DEL-007 | Project/phase/decision/risk registers | Yes | ACTIVE |
| P00-DEL-008 | P00 phase specification | Yes | APPROVED SPECIFICATION; exit not approved |
| P00-DEL-009 | Bounded P01 phase specification | Yes | APPROVED SPECIFICATION; implementation not authorized |
| P00-DEL-010 | Phase/task manifest schema | Yes | IMPLEMENTED AND LOCALLY VERIFIED; P00-EV-010 |
| P00-DEL-011 | Initial CI workflow and evidence | Yes under roadmap; requires separate authorization | IMPLEMENTED; local-equivalence evidence passed, hosted run pending; P00-EV-011 |
| P00-DEL-012 | P00 exit evidence index and approval record | Yes | NOT_STARTED |

## 8. P00 Acceptance Criteria

| ID | Acceptance criterion | Required evidence |
|---|---|---|
| P00-AC-001 | Product scope, non-goals, target market, and commercial assumptions are documented without claiming implementation | Reviewed product baseline |
| P00-AC-002 | Requirements use stable unique identifiers and have verification statements | Identifier validation and requirements review |
| P00-AC-003 | Each planned module has a documented purpose, owner, lifecycle, and dependency boundary | Module catalogue and dependency review |
| P00-AC-004 | The initial dependency graph contains no unreviewed circular dependency | Architecture review and dependency evidence |
| P00-AC-005 | Multi-tenancy, domain ownership, identifiers, authorization, and entitlements follow accepted ADRs | ADR/source reconciliation record |
| P00-AC-006 | Financial ownership, immutability, decimal, currency, and correction principles are documented; unresolved policies remain explicit | ADR-011/013 review and DEC-FIN-001 |
| P00-AC-007 | Task, outbox, integration, file, audit, API, secret, and deployment boundaries are documented | ADR-009/010/012/016–020 review |
| P00-AC-008 | Security requirements and testing strategy are explicitly reviewed and approved | Quality approval records |
| P00-AC-009 | P00 traceability links mandatory requirements, controls, tests, owners, status, and evidence | Traceability validation report |
| P00-AC-010 | Material open decisions and risks have owners, consequences, required-by gates, and current status | Decision/risk register review |
| P00-AC-011 | Repository and documentation conventions are defined and internally linked | `AGENTS.md`, README, link/structure checks |
| P00-AC-012 | Phase/task manifest schemas and validation rules are defined | Approved schema specification and validation evidence |
| P00-AC-013 | Initial CI gates are implemented or an explicit approved P00 exception defines when and how they will be implemented before P01 changes merge | CI workflow evidence or approved exception |
| P00-AC-014 | P01 has a bounded specification, task/evidence model, dependencies, and non-goals | Reviewed P01 specification |
| P00-AC-015 | No unresolved critical security, tenant-isolation, financial-integrity, or governance conflict blocks P01 | Security/architecture/decision review |
| P00-AC-016 | P00 evidence package is complete, factual, and free of fabricated results | Evidence index and independent review |
| P00-AC-017 | Product Owner and designated technical reviewers explicitly approve P00 exit and separately authorize P01 implementation | Signed/recorded phase approval |

## 9. Verification Plan

P00 is primarily verified through documentation and governance evidence:

- Markdown link, heading, identifier, and register consistency checks.
- ADR status and approval parity checks.
- Requirement/control/test coverage checks.
- Cross-document terminology and ownership review.
- Security and QA review of approved quality standards and their implementation evidence.
- Product review of scope, non-goals, launch assumptions, and open decisions.
- Architecture review of accepted-ADR reconciliation.
- Git diff and change-attribution review.
- Independent confirmation that no implementation is represented as complete.

If P00 engineering tasks are later authorized, their commands, results, artifacts, and limitations must be added to the evidence package. Unexecuted tests cannot be recorded as passed.

## 10. Security and Data-Integrity Considerations

- P00 contains specifications, not production secrets or customer data.
- Regulatory sources, provider contracts, and evidence may be sensitive and require controlled storage.
- Architecture examples must not introduce insecure copy-ready patterns.
- Tenant isolation, runtime database roles, RLS pooling behavior, financial policies, secret handling, and recovery claims require implementation evidence in later phases.
- Acceptance of an ADR does not waive its security or test criteria.

## 11. Dependencies and Blocking Decisions

### Required before P00 exit

- Approval of the security and testing baselines.
- Resolution of canonical phase identifiers or an explicit approved alias policy.
- Approved initial launch/P01 scope.
- Bounded P01 phase specification.
- Phase/task manifest design and validation approach.
- Initial CI evidence or an explicit approved exception that cannot weaken P01 merge gates.
- No unowned critical issue affecting P01.

### May remain open after P00 when not required by P01

- Paid provider selections.
- UAE e-invoicing applicability and provider details.
- Detailed finance/tax policies for later financial phases.
- Production hosting region/topology, final RPO/RTO, retention periods, and API commercial support windows.

These decisions must retain owners and required-by gates; deferral is not implicit approval.

## 12. Evidence Package

The P00 evidence index must include:

1. Approved phase specification and scope changes.
2. Product-document review outcomes.
3. Accepted ADR register and standards approval record.
4. Architecture reconciliation report.
5. Approved security/testing documents or explicit unresolved review findings.
6. Traceability matrix and automated validation results.
7. Decision, risk, issue, project, and phase register snapshots.
8. Manifest/CI design and any executed validation results.
9. Bounded P01 specification.
10. Open exceptions with owner, risk, expiry, and approval.
11. P00 completion report and reviewer dispositions.
12. Explicit Product Owner P00 exit approval and separate P01 implementation authorization.

Evidence status values are `NOT_STARTED`, `DRAFTED`, `READY_FOR_REVIEW`, `VERIFIED`, `APPROVED`, `BLOCKED`, and `NOT_APPLICABLE`.

## 13. Exit Gate

**Gate name:** Architecture, Quality, and Product Foundation Approved

P00 may be marked `APPROVED` only when:

- P00-AC-001 through P00-AC-017 are satisfied or have an explicitly authorized exception where permitted.
- P00-AC-005, P00-AC-008, P00-AC-009, P00-AC-014, P00-AC-015, P00-AC-016, and P00-AC-017 have no routine waiver.
- No critical unresolved finding affects tenant isolation, authorization, secrets, financial integrity, destructive migration safety, or evidence truthfulness.
- The evidence package is reviewed by Product, Architecture, Security, and QA; DevOps reviews applicable CI/operations items.
- Product Owner approval and P01 implementation authorization are recorded separately.

P00 approval does not make the platform production-ready.

## 14. Change Control

- Material scope changes require an updated specification, traceability impact assessment, and Product Owner approval.
- A change conflicting with an accepted ADR requires an amended or superseding ADR.
- New P00 requirements receive stable identifiers; existing identifiers are not reused.
- Deferred items must identify their required-by phase and consequence.
- Status changes require evidence links; prose assertions alone are insufficient.

## 15. Current Phase Assessment

| Area | Assessment |
|---|---|
| ADR baseline | ACCEPTED |
| Product baseline | APPROVED PLANNING BASELINE; launch scope and specialist decisions pending |
| Architecture reconciliation | APPROVED BASELINE; implementation validation pending |
| Security requirements | APPROVED BASELINE |
| Testing strategy | APPROVED BASELINE |
| Traceability baseline | APPROVED VERIFICATION BASELINE |
| P01 specification | APPROVED SPECIFICATION; tenant-isolation matrix approved but all tests `NOT_RUN` |
| Manifest/CI foundation | IMPLEMENTED; local gates pass, hosted Actions run pending |
| P00 exit evidence | IN_PROGRESS; P00-EV-010 verified and P00-EV-011 partial |
| P00 status | SPECIFICATION_IN_PROGRESS |

## 16. Approval

**Current Status:** APPROVED SPECIFICATION

- **Recommended disposition:** Approve this bounded P00 specification after Product, Architecture, Security, QA, and applicable DevOps review.
- **Approved By:** Product Owner — explicit market-standard review instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Approval of this specification alone does not approve the P00 exit gate or authorize P01 implementation.

## 17. Change Log

| Version | Date | Status | Description |
|---|---|---|---|
| 1.0 | 28 October 2026 | APPROVED SPECIFICATION | Bounded P00 documentation and governance phase specification approved; P00 exit remains open. |
