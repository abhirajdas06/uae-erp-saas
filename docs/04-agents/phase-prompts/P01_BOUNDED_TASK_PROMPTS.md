# P01 — Bounded Task Prompt Pack

| Property | Value |
|---|---|
| Document ID | P01-PROMPTS-001 |
| Status | APPROVED PROMPT BASELINE — IMPLEMENTATION NOT AUTHORIZED |
| Governing specification | [P01-SPEC-001](../../02-phases/P01_CORE_PLATFORM/P01_PHASE_SPECIFICATION.md) |
| Verification baseline | [P01-TEN-TEST-001](../../02-phases/P01_CORE_PLATFORM/P01_TENANT_ISOLATION_TEST_MATRIX.md) |

These task bodies close the P01 prompt gap. They do not authorize implementation. Before dispatch, the orchestrator must instantiate the [implementation task template](../IMPLEMENTATION_TASK_PROMPT_TEMPLATE.md) with an approval reference, exact commit and file scope, assigned reviewers, commands, evidence paths, migration/recovery plan, and unresolved decisions. Every tenant-isolation test remains `NOT_RUN` until executed against the identified environment and database role.

## P01-T01 — Toolchain and Django Bootstrap

**Objective:** Establish only the approved Django project and locked Python/Django/test toolchain.

**Scope:** Version constraints, dependency lock, project package, minimal `core` app, pytest bootstrap and documented commands. Do not create later domain apps or speculative models.

**Acceptance/evidence:** P01-AC-001–002, 030; P01-EV-002, 009–010. Record clean install, framework system check, test discovery, dependency and license/security review.

## P01-T02 — Typed Settings and Safe Configuration

**Objective:** Define development, test and production settings that fail closed and contain no secrets.

**Scope:** Environment schema, startup validation, secure cookie/CSRF/host/proxy defaults, redaction and `.env.example`. No real credential or production endpoint.

**Acceptance/evidence:** P01-AC-003–005, 025–027; P01-EV-002, 009. Test missing/invalid production settings and inspect source, logs and artifacts for secrets.

## P01-T03 — PostgreSQL Roles and Migration Foundation

**Objective:** Establish PostgreSQL as the authoritative database with separated migration and restricted runtime roles.

**Scope:** Connection configuration, role/grant contract, migration commands, clean-install evidence and forward-fix boundary. SQLite is not acceptable isolation evidence.

**Acceptance/evidence:** P01-AC-001–004, 017, 020–023, 028; P01-EV-003–004, 007. Prove runtime role is not superuser, owner or `BYPASSRLS`.

## P01-T04 — Custom User and Authentication Foundation

**Objective:** Implement the custom user model before initial migrations and the bounded session authentication flows.

**Scope:** Identity model, login/logout, approved password change/recovery, abuse controls, session/CSRF controls and security audit events. Exclude public registration, SSO and federation.

**Acceptance/evidence:** P01-AC-006–007, 024–027; applicable IAM and P01 tenant-matrix tests; P01-EV-005, 008–009. Include enumeration, fixation, CSRF, rate-limit and safe-error tests.

## P01-T05 — Tenant, Membership and Provisioning Foundation

**Objective:** Implement tenant identity, membership and one controlled atomic provisioning operation.

**Scope:** `Tenant`, `TenantMembership`, approved lifecycle, optional minimum organization records, same-tenant constraints, idempotency and audit. No subscription or commercial trial.

**Acceptance/evidence:** P01-AC-008–010, 017–019, 024; P01-EV-003–004, 006, 008. Test rollback, duplicate/concurrent request, suspension and foreign relationships.

## P01-T06 — Trusted Tenant Context

**Objective:** Resolve and propagate trusted request/service/task/database tenant context without connection leakage.

**Scope:** Membership-authorized resolution, explicit context object, transaction-local `app.current_tenant_id`, cleanup and safe rejection. Client-supplied UUID is never authority.

**Acceptance/evidence:** P01-AC-011–016, 020–023; P01-EV-006–007. Execute missing/forged/stale context, nested transaction and pooled-connection reuse scenarios.

## P01-T07 — RBAC, Object Scope and Platform Separation

**Objective:** Enforce deny-by-default action, object and organizational scope while separating platform administration.

**Scope:** Roles, permissions, membership-role assignment, permission catalogue, service/view/admin enforcement and auditable privileged operations. Entitlement remains a P02 seam.

**Acceptance/evidence:** P01-AC-008–016, 024; P01-EV-005–006, 008. Include direct URL, service, admin, stale role and cross-tenant negative tests.

## P01-T08 — Tenant-Aware Constraints and RLS Pilot

**Objective:** Add database-enforced same-tenant integrity and the explicitly reviewed RLS pilot.

**Scope:** Named tables/policies, `USING`/`WITH CHECK`, composite references where required, forced policy behavior, migration/rollback plan and restricted-role tests. RLS does not replace application authorization.

**Acceptance/evidence:** P01-AC-017–023; P01-EV-003–004, 006–007. Execute direct SQL read/write/reference attacks, missing context and owner/bypass checks in PostgreSQL.

## P01-T09 — Audit and Structured Logging Foundation

**Objective:** Produce durable, append-oriented material-event evidence and safe correlated logs.

**Scope:** `AuditEvent`, approved event catalogue, actor/tenant/action/resource/outcome/correlation fields, transaction behavior, protected access and redaction. Do not invent statutory retention.

**Acceptance/evidence:** P01-AC-024–027; P01-EV-008–009. Test rollback semantics, unauthorized mutation, privileged read, correlation and prohibited-data leakage.

## P01-T10 — Health and Readiness Diagnostics

**Objective:** Expose bounded operational health/readiness without leaking tenant or configuration data.

**Scope:** Liveness/readiness contracts, dependency checks, safe status codes, timeout behavior and least disclosure.

**Acceptance/evidence:** P01-AC-005, 027–028; P01-EV-002, 010. Test dependency failure and anonymous response content.

## P01-T11 — Docker Development and Test Environment

**Objective:** Provide reproducible, non-production Docker/Compose workflows for the approved P01 stack.

**Scope:** Non-root images where applicable, pinned bases, PostgreSQL integration test service, volumes, health checks and secret-free configuration. Do not imply production topology.

**Acceptance/evidence:** P01-AC-001–004, 028; P01-EV-002, 004, 009–010. Record image digests, build/start/migrate/test commands and image/source secret inspection.

## P01-T12 — CI Gates and Full P01 Verification

**Objective:** Execute all mandatory P01 quality and tenant-isolation gates reproducibly.

**Scope:** Formatting/lint/static checks, unit/integration/PostgreSQL/RLS/security/migration suites, manifest/evidence validation and artifact integrity. Skips and failures are visible and fail according to policy.

**Acceptance/evidence:** P01-AC-001–031; all mandatory P01 tenant tests; P01-EV-002–010, 012. Evidence identifies commit, environment, commands, roles, results, artifact digests and limitations.

## P01-T13 — Runbooks, Evidence and Independent Exit Review

**Objective:** Assemble the phase evidence index and independent completion report for human decision.

**Scope:** Setup/security/database/recovery runbooks; AC-to-evidence reconciliation; finding/exception disposition; independent QA, Security, Database and Operations reviews; Product Owner exit packet.

**Acceptance/evidence:** P01-AC-029–031 and P01 exit gate; P01-EV-011–014. The implementer cannot independently approve their own work. P01 exit does not authorize P02.

## Dispatch Stop Conditions

Do not dispatch or continue a dependent task when P00 exit/P01 start authorization is missing, an accepted ADR conflicts, same-tenant integrity is unresolved, PostgreSQL restricted-role evidence cannot run, or a critical isolation/authorization/secret/migration/audit finding remains. Report the exact approval or corrective evidence required and continue only independent documentation work.
