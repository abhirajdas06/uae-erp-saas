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

## 10. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved. `core` is a domain-neutral infrastructure application, so several gate items are legitimately not applicable; each is stated rather than left blank.

| Gate | Disposition for `core` |
|---|---|
| RDY-001 attributes | Not applicable. `core` owns no business entity and must not define a universal base model carrying tenant or business fields, per section 3. Value-object and primitive interfaces are code contracts, specified by CORE-006 and CORE-007 |
| RDY-002 states | Not applicable. No stateful business record is owned. Health and readiness results are computed, not persisted states |
| RDY-003 testable rules | Satisfied by CORE-001–CORE-008, each with a named verification method |
| RDY-004 permissions | `core.view_health_detail` is the only codename; liveness and readiness endpoints are unauthenticated only where explicitly approved under CORE-004, and detailed diagnostics always require the permission |
| RDY-005 interface surfaces | Error pages, the unavailable result and the maintenance surface map to the error layout in `../01-architecture/UI_DESIGN_SYSTEM.md` `UIX-002`; `core` owns no business screen |
| RDY-006 reports and imports | Not applicable. No report, import or export is owned. `core` contributes liveness and readiness signals to `RPT-804` |
| RDY-007 document numbering | Not applicable. No document type is allocated. `core` may host the shared allocation primitive only if `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md` places it here, and the sequence records remain owned by their domains |
| RDY-008 notifications | Not applicable as a catalogue owner. Readiness and health alerting is operational monitoring under `DEP-OBS-001`, not a user notification |
| RDY-009 classification and retention | `core` stores no personal data. Correlation identifiers are `C1`. Structured logs follow `RET-10` in `../05-quality/DATA_PROTECTION_AND_RETENTION.md`; CORE-008 prohibits secrets and unnecessary personal data in them |
| RDY-010 threats | `THR-004` verbose error or debug disclosure, `THR-006` misconfigured unauthenticated endpoint, `THR-035` sensitive data in logs, and `THR-013` correlation propagation into background tasks without tenant context |
| RDY-011 decision dependencies | `CORE-DEC-001` and `CORE-DEC-002` remain open; the readiness dependency set and timeout budget fail closed until `CORE-DEC-002` is approved |
| RDY-012 regulatory assertions | None. `core` asserts no regulatory fact |

## 11. Migration, Compatibility and Recovery

`core` primitives are consumed across the monolith, so a change to an exception type, correlation contract, clock interface or health contract is a breaking change for every dependent application. Such a change requires the API change classification in `../01-architecture/API_STANDARDS.md` section 30.1 and must preserve existing behavior for at least one release unless an approved exception is recorded.

`core` owns no migration of business data. Any schema it introduces, such as an idempotency or operation primitive placed here by an approved decision, is additive and backward compatible. Restore verification for `core` is limited to confirming that health and readiness report correctly against restored dependencies and that correlation continuity is preserved in logs and audit records.

## 12. Evidence and Definition of Done

Acceptance criteria are `CORE-001`–`CORE-008` plus the applicable criteria in `P01-AC-001`–`P01-AC-030`. Evidence records are the `P01-EV` entries named for toolchain, settings and health work in the [P01 traceability matrix](../02-phases/P01_CORE_PLATFORM/P01_TRACEABILITY_AND_TEST_MATRIX.md), principally `P01-EV-002` and `P01-EV-009`–`P01-EV-010`. All evidence is `NOT_RUN` until executed under an authorized P01 task. The definition of done in `../05-quality/DEFINITION_OF_DONE.md` applies in full.
