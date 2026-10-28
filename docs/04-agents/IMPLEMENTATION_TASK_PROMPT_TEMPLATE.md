# Bounded Implementation Task Prompt Template

Use this template only after the applicable phase and task are authorized.

## Task identity

- **Task ID:** `PNN-TNN`
- **Parent phase:** `PNN`
- **Module/capability:**
- **Authorization reference:**
- **Owner role:**
- **Required reviewers:**

## Objective

State one coherent implementation outcome.

## Authoritative documents

List exact repository paths. Include `AGENTS.md`, phase specification, module specification, applicable ADRs, security requirements, testing strategy, and decisions.

## Scope

### Included

- List the exact behavior and expected components.

### Excluded

- List later tasks, speculative features, production actions, paid-provider decisions, and unresolved regulatory behavior.

## Expected changes

List expected files, applications, models, services, views/APIs, templates, tasks, migrations, tests, and documentation. Treat this as a boundary, not permission for unrelated rewrites.

## Dependencies and assumptions

List prior tasks, approved decisions, environment requirements, and explicitly unverified assumptions.

## Required behavior

Use requirement and acceptance-criterion identifiers. Include validation, permissions, tenant scope, entitlements, transactions, constraints, concurrency, idempotency, audit, errors, retries, and reconciliation.

## Required tests

Include applicable:

- unit and service tests;
- PostgreSQL model/constraint/migration tests;
- permission and cross-tenant negative tests;
- view/API/HTMX tests;
- background-task and duplicate-delivery tests;
- financial calculation/rounding tests;
- external integration failure tests;
- security/static/dependency/secret checks;
- regression and end-to-end tests.

Never mark a test passed unless it was executed.

## Permissions

- **Filesystem:** Exact allowed paths.
- **Network:** None unless explicitly required.
- **Secrets:** None unless an approved test credential mechanism is named.
- **Database:** Development/test only; no destructive production actions.
- **External side effects:** Mock/sandbox only unless explicitly approved.

## Evidence

Define commands, expected results, artifact paths, commit/run identifiers, reviewer dispositions, and retention/sensitivity.

## Completion report

Report:

1. outcome and files changed;
2. tests/checks actually executed and results;
3. acceptance criteria and evidence;
4. security/tenant/data-integrity review;
5. limitations, defects, and deferred decisions;
6. documentation/status updates;
7. pending approvals, including what, who, evidence, recommendation, exact approval statement, and blocked scope.
