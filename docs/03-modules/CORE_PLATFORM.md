# CORE — Platform Core Specification

| Property | Value |
|---|---|
| Document ID | MOD-CORE-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Owning Phase | P01 |
| Django App | `core` |
| Commercial Module | No |
| Tenant-Owned Data | Primarily no; tenant context values are handled but not owned |

## 1. Purpose

`core` owns technical primitives required across the modular monolith without becoming a dumping ground for domain behavior. It provides safe exceptions, request/correlation foundations, health/readiness checks, common value-object interfaces, and narrowly approved infrastructure seams.

## 2. Governing sources

- `docs/02-phases/P01_CORE_PLATFORM/P01_PHASE_SPECIFICATION.md`
- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- ADR-001, ADR-003, ADR-007, ADR-015, ADR-017, and ADR-018
- `docs/05-quality/SECURITY_REQUIREMENTS.md`
- `docs/05-quality/TESTING_STRATEGY.md`

## 3. Scope and non-goals

Included:

- correlation/request identifiers;
- safe shared exception types and error presentation;
- health, liveness, and readiness checks;
- clock and identifier interfaces where deterministic testing requires them;
- shared pagination/validation primitives only when domain-neutral;
- future entitlement and event interfaces without fake implementations.

Excluded:

- customer, supplier, product, financial, subscription, or employee records;
- generic “service” classes that own another module's rules;
- a universal base model containing tenant or business fields;
- production monitoring-provider selection;
- commercial module activation.

## 4. Ownership rules

Domain applications may depend on stable `core` primitives. `core` must not import business applications or mutate their models. A primitive used by only one domain belongs in that domain until reuse is demonstrated.

## 5. Requirements

| ID | Requirement | Verification |
|---|---|---|
| CORE-001 | Every inbound request receives or validates a bounded correlation ID; unsafe values are replaced | Request tests |
| CORE-002 | Error responses and pages disclose no secrets, stack traces, tenant data, or internal identifiers beyond approved references | Negative/security tests |
| CORE-003 | Liveness checks only process health; readiness checks verify approved dependencies with strict timeouts | Health tests |
| CORE-004 | Health endpoints are unauthenticated only where explicitly approved and never enumerate tenants/configuration | Security review |
| CORE-005 | Shared exceptions map consistently to HTTP/UI behavior without hiding authorization failures | View/service tests |
| CORE-006 | Time-dependent logic accepts an injectable clock at important business boundaries | Unit tests |
| CORE-007 | Core utilities remain domain-neutral and do not import business apps | Dependency check |
| CORE-008 | Structured logs include correlation metadata but exclude secrets and unnecessary personal data | Log-capture tests |

## 6. Security and tenant isolation

`core` may carry trusted tenant context but never decides tenant membership itself. Client-provided tenant identifiers remain untrusted until validated by `tenants`. Cache keys, diagnostics, errors, and logs must not create cross-tenant disclosure.

## 7. Operational behavior

Readiness failure returns a stable unavailable result, not dependency credentials or raw exceptions. Checks require timeouts and must not perform destructive writes. Expensive downstream/provider checks belong in operational monitoring, not every health request.

## 8. Acceptance and tests

CORE is ready for P01 exit when:

- CORE-001 through CORE-008 pass;
- forbidden cross-app imports are absent;
- correlation survives request, task-dispatch metadata, audit, and logs;
- health endpoints pass normal, dependency-failure, timeout, and disclosure tests;
- setup and troubleshooting documentation identifies every readiness dependency.

Required tests: unit, request/view, security-disclosure, structured-log, dependency-boundary, and health failure tests.

## 9. Pending decisions

| ID | Decision | Owner | Required before |
|---|---|---|---|
| CORE-DEC-001 | Exact lint/type/static toolchain and versions | QA / Architecture | P01 task authorization |
| CORE-DEC-002 | Production health dependency set and timeout budget | DevOps | Production topology approval |
