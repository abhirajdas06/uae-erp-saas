# P01 Core Platform and Multi-Tenancy — Orchestration Prompt

Use this prompt only after P00 is formally closed and a bounded P01 task is explicitly authorized.

## Role

Act as the P01 orchestrator for the UAE ERP SaaS modular monolith. Coordinate architecture, development, testing, security, database, DevOps, and documentation work. Do not treat a coding-agent completion message as evidence.

## Authoritative inputs

Read completely before assigning work:

- `AGENTS.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/00-product/MODULE_CATALOGUE.md`
- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- `docs/01-architecture/DJANGO_APP_STRUCTURE.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- ADR-001 through ADR-006 and ADR-014 through ADR-018
- `docs/02-phases/P01_CORE_PLATFORM/P01_PHASE_SPECIFICATION.md`
- `docs/02-phases/P01_CORE_PLATFORM/P01_TENANT_ISOLATION_TEST_MATRIX.md`
- `docs/03-modules/CORE_PLATFORM.md`
- `docs/03-modules/TENANT_MANAGEMENT.md`
- `docs/03-modules/USERS_ACCESS_CONTROL.md`
- `docs/03-modules/AUDIT_FOUNDATION.md`
- `docs/05-quality/SECURITY_REQUIREMENTS.md`
- `docs/05-quality/TESTING_STRATEGY.md`

## Objective

Deliver only the approved P01 foundation: reproducible Django/PostgreSQL bootstrap; `core`, `tenants`, `users`, and `audit`; trusted tenant context; deny-by-default authorization; tenant-aware constraints; reviewed RLS pilot; secure sessions; audit/logging foundation; health/readiness; migrations; tests; CI evidence; and runbooks.

Do not implement subscriptions, billing, entitlements, CRM, finance, HRMS, payroll, e-invoicing, production deployment, or speculative application skeletons.

## Required task order

1. P01-T01 — toolchain and Django bootstrap.
2. P01-T02 — typed settings and safe configuration.
3. P01-T03 — PostgreSQL roles and migration foundation.
4. P01-T04 — custom user and authentication.
5. P01-T05 — tenant/membership models and provisioning.
6. P01-T06 — request/service/task/database tenant context.
7. P01-T07 — RBAC, scope, and platform separation.
8. P01-T08 — same-tenant constraints and RLS pilot.
9. P01-T09 — audit and structured logging.
10. P01-T10 — health/readiness diagnostics.
11. P01-T11 — Docker development/test environment.
12. P01-T12 — complete P01 verification and CI.
13. P01-T13 — runbooks, evidence, and completion review.

Do not start a dependent task until its predecessor evidence passes. High-coordination models, migrations, settings, middleware, authentication, tenant context, and RLS changes must not be redesigned in parallel.

## Task-generation rule

For each task, instantiate `docs/04-agents/IMPLEMENTATION_TASK_PROMPT_TEMPLATE.md` and include:

- exact task ID and authorization reference;
- exact file/directory scope;
- source requirement and acceptance IDs;
- models/services/interfaces permitted;
- migration and rollback/forward-fix plan;
- tenant-isolation and permission tests;
- PostgreSQL/RLS/restricted-role tests where applicable;
- security reviewer and code reviewer;
- reproducible commands and evidence locations;
- explicit prohibitions and unresolved decisions.

## Mandatory controls

- Use the custom user model from the first migration.
- `tenants` owns `TenantMembership`.
- Use `app.current_tenant_id` transaction-locally for approved RLS work.
- Runtime roles are not superuser, table owner, or `BYPASSRLS`.
- UUID possession never grants access.
- Permission and entitlement remain separate; P02 entitlement is not faked.
- Required audit evidence is durable and redacted.
- No customer/business data is deleted through tenant lifecycle changes.
- All P01 isolation scenarios remain `NOT_RUN` until actually executed.

## Verification and stop conditions

Stop dependent work and record a blocker when:

- an accepted ADR conflicts with the proposed model or migration;
- same-tenant integrity cannot be enforced as specified;
- a task requires an unresolved Product/Security decision;
- PostgreSQL/RLS tests cannot run in the approved environment;
- a critical cross-tenant, authorization, secret, migration, or audit finding remains;
- scope expands into P02 or later modules.

## Completion output

After each task report:

- files changed;
- acceptance criteria;
- commands/tests actually executed;
- evidence artifacts;
- tenant/security/data-integrity review;
- defects and limitations;
- documentation/status updates;
- next dependency-ready P01 task;
- pending approvals with what, who, evidence, recommendation, exact approval statement, and blocked scope.

P01 phase completion requires independent QA/security review and Product Owner exit approval. It does not authorize P02.
