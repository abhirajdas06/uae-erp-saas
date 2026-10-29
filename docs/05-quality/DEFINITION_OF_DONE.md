# Definition of Done

| Property | Value |
|---|---|
| Document ID | QUAL-DOD-001 |
| Status | READY FOR REVIEW |
| Owner | Engineering / QA |

## 1. Rule

“Done” means the authorized scope and acceptance criteria are satisfied with reproducible evidence. It never means only that drafting or coding stopped, a pull request exists, or an agent reported completion.

## 2. Documentation Task Done

- Authoritative sources and owning documents were read.
- Scope, assumptions, non-goals, dependencies, security/tenant/data-integrity implications and unresolved decisions are explicit.
- Identifiers and relative links validate; duplicate sources of truth were avoided.
- Related ADR, phase, module, decision, risk and status records are reconciled.
- Regulatory claims are dated/cited or marked unverified.
- `git diff --check` and documentation validators pass, or limitations are recorded.
- Required reviewers and approvals are recorded without self-approval.

## 3. Implementation Task Done

- Task/phase authorization and exact source specification are recorded.
- Smallest coherent change is implemented without unauthorized scope.
- Data ownership, permissions, entitlements, tenant context, constraints, migration and rollback/forward-fix behavior are addressed.
- Required unit, database, service, view/API, task/integration, migration, security and regression tests execute in the required environments.
- Formatting, lint, static/type, dependency, secret and relevant container checks pass.
- Negative, cross-tenant, concurrency, idempotency, rollback and recovery cases required by the task pass.
- Documentation, runbooks, traceability and evidence are updated.
- Independent code/QA/security/domain reviews disposition findings.
- No blocking critical/high finding or hidden skip remains.

## 4. Phase Done

- Every phase AC maps to verified evidence for the approved commit/release/environment.
- Mandatory test catalogue is executed with skips/exceptions explicitly approved where eligible.
- Migration, deployment overlap, monitoring, backup/restore and reconciliation evidence exists for applicable scope.
- Open defects, risks, decisions, disabled behavior and limitations are reviewed.
- Independent reviewers reproduce sufficient evidence.
- Product Owner records phase-exit approval. Exit does not start the next phase or authorize deployment unless explicitly stated.

## 5. Non-Waivable Truthfulness

No routine exception may waive tenant isolation, authorization, entitlement, financial/posted-record integrity, duplicate external effects, secret/sensitive-data protection, destructive migration safety, audit integrity or truthful evidence reporting.
