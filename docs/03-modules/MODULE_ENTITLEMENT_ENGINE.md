# ENTITLEMENTS — Module Entitlement Engine Specification

| Property | Value |
|---|---|
| Document ID | MOD-ENTITLEMENTS-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Owning Phase | P02 |
| Django App | `subscriptions` |
| Domain Owner | Entitlement Policy within Subscription Management |
| Commercial Module | No |
| Tenant-Owned Data | Mixed policy and tenant-derived state |

## 1. Purpose and Sources

Provide one deterministic, server-side answer to whether a tenant is commercially entitled to a module or capability at a specified time and operation class. This specification implements `SUB-003`, complements [Subscription Management](SUBSCRIPTION_MANAGEMENT.md), and is governed by [Entitlement Engine Architecture](../01-architecture/ENTITLEMENT_ENGINE.md), [Module Dependencies](../01-architecture/MODULE_DEPENDENCIES.md), ADR-004, ADR-005, ADR-006, ADR-009, ADR-010, ADR-015, and ADR-018.

## 2. Scope and Boundaries

Included: dependency closure, subscription/lifecycle/effective-date evaluation, structured reasons, activation/deactivation consequences, overrides, degraded-access policy, cache safety, background-task policy, reconciliation, and enforcement adapters.

Excluded: authentication, user roles, object authorization, payment-provider truth, business-module logic, feature flags as commercial authority, and direct deletion or mutation of protected business data.

## 3. Actors and Authorization

Normal callers do not “manage” entitlements; they request a decision under trusted tenant context. Subscription services create authoritative changes. Platform override administrators need separate privileged permission, reason, scope, approval, and expiry. Auditors and support have read-only or purpose-bound access.

## 4. Decision Contract

The evaluator accepts trusted tenant ID, stable module/capability code, operation class, evaluation time, and optional authoritative context. It returns a structured result containing:

- allowed/denied;
- stable reason code safe for the caller;
- evaluated tenant, module/capability, operation, and time;
- subscription, policy, dependency, entitlement, and override versions used;
- freshness/source metadata and correlation ID;
- remediation hint appropriate to the caller without leaking internal or other-tenant data.

Absence, ambiguity, unknown codes, invalid policy, missing tenant context, failed dependency, expired override, or unsafe stale data denies access. Exceptions must be explicit policy results, never catch-all bypasses.

## 5. Evaluation Order and Invariants

1. Validate trusted tenant and normalized code.
2. Load platform module lifecycle/release policy.
3. Validate tenant/account operational state.
4. Load effective subscription and entitlement snapshot.
5. Resolve hard, conditional, and approved alternative dependencies.
6. Apply effective date, suspension/expiry/degraded-access, operation-class, and override policy.
7. Return a structured result; caller separately enforces user/object permission.

`Access = Tenant operational AND User authorized AND Module commercially available as applicable AND Subscription permits operation AND Entitlement effective AND Dependencies satisfied`.

Payment-success callbacks, client assertions, installed Django apps, UI visibility, feature flags, and cached grants are not authoritative entitlement.

## 6. Entitlement States and Operations

Conceptual states include `PENDING`, `ACTIVE`, `GRACE` (only if approved), `SUSPENDED`, `EXPIRED`, `REVOKED`, and `ERROR/INCONSISTENT`. Operation classes include normal read, new business operation, integrity-preserving completion/correction, export, subscription remediation, and privileged support. Each business module must declare its degraded-access matrix; absent policy denies new business operations.

## 7. Business Rules

| ID | Requirement | Verification |
|---|---|---|
| ENT-001 | One central evaluator governs protected module/capability access | Architecture/enforcement scan |
| ENT-002 | Entitlement and authorization are independently required | Permission matrix |
| ENT-003 | Evaluation is deterministic for the same authoritative snapshot and time | Unit/property tests |
| ENT-004 | Dependency closure is complete, acyclic, versioned, and no silent paid dependency is granted | Graph/change tests |
| ENT-005 | Unknown, absent, invalid, inconsistent, or stale-sensitive conditions deny | Negative tests |
| ENT-006 | Lifecycle and degraded access are operation-specific and effective-dated | Decision-table tests |
| ENT-007 | Overrides are scoped, authorized, time-bound, reasoned, and audited | Security tests |
| ENT-008 | Cache failure, collision, or delayed invalidation cannot grant sensitive access | Cache tests |
| ENT-009 | Tasks reload durable operation/current policy according to the approved execution rule | Task tests |
| ENT-010 | Reconciliation detects divergence among subscription, billing policy input, entitlement, cache, and provisioning | Reconciliation tests |
| ENT-011 | Disablement never deletes business data | Integration tests |
| ENT-012 | Decisions and denials expose no cross-tenant or sensitive policy data | Security tests |

## 8. Enforcement Points

Enforce in Django views and HTMX endpoints, DRF permission/service layers, application services, Celery tasks, reports, exports, file downloads, webhooks/integrations, and Django admin. UI hiding is usability only. Services remain the authoritative enforcement boundary; adapters must not reproduce policy logic.

## 9. Cache and Concurrency

Caching is optional. The authoritative record remains PostgreSQL. Keys include tenant, module/capability, operation class where relevant, policy/configuration version, entitlement generation, and other required scope. Grants use bounded TTL and reliable invalidation; sensitive writes revalidate authoritative state under the freshness policy. Outage or deserialization failure never defaults to allow.

Subscription/override changes serialize or use version preconditions, increment the entitlement generation, record audit/outbox intent atomically, and invalidate affected entries. Concurrent fill cannot republish an older generation over a newer denial.

## 10. Tenant Isolation, Security, Audit, and Privacy

All tenant-derived reads use trusted context, same-tenant constraints, and approved RLS. Batch tasks isolate failures and context per tenant. Reason details are audience-filtered. Material grant/revoke, override, policy error, reconciliation repair, and privileged decision inspection are audited with actor/service, tenant, correlation, before/after state, reason, and source versions—never secrets or unnecessary billing payloads.

## 11. Integrations, Events, and Operations

Entitlement recomputation is driven by committed subscription/policy/lifecycle facts through durable outbox intent where loss matters. Consumers are idempotent and validate aggregate version. Monitoring covers deny/error rate, invalid graph, stale generation, invalidation failure, override use, recompute age, and reconciliation mismatch. Recovery uses bounded replay/recompute, not direct grant edits.

## 12. UI and API

Tenant users receive safe denial and remediation messages. Authorized platform screens expose policy/decision diagnostics and override review with tenant boundaries and redaction. Any external decision API is versioned under ADR-020, rate-limited, does not reveal internal configuration, and cannot accept a caller-asserted tenant as authority.

## 13. Acceptance, Tests, and Evidence

Acceptance criteria are `ENT-001`–`ENT-012` plus P02-AC-002, 006–009, 014–016, and 018. Required tests are P02-TST-005–009, 027–054, 082–106, and 113–118. Evidence: P02-EV-003, 005, 006, 009, 010, 012, and 013 in the [P02 matrix](../02-phases/P02_SUBSCRIPTION_ENGINE/P02_TRACEABILITY_AND_TEST_MATRIX.md).

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| ENT-DEC-001 | Per-state operation matrix | Product/Security/module owners | Activating each commercial module | Deny new operations by default; explicitly permit remediation/integrity operations |
| ENT-DEC-002 | Cache TTL/freshness budgets | Architecture/Security/SRE | Enabling cache | Start uncached; enable only with measured need and invalidation evidence |
| ENT-DEC-012 | Override approval model | Product/Security | Overrides | Time-bound least privilege; independent approval for material grants |

## 15. Implementation Prompt

Use [P02 orchestration](../04-agents/phase-prompts/P02_SUBSCRIPTION_ENGINE.md) and P02-T05/T06 in [P02 bounded tasks](../04-agents/phase-prompts/P02_BOUNDED_TASK_PROMPTS.md).

## 16. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved.

| Gate | Disposition for `entitlements` |
|---|---|
| RDY-001 attributes | The decision contract in section 4 and the entitlement states in section 6 define the owned structures. Effective-entitlement records carry tenant, module code, source subscription reference, effective from and to dates, dependency closure result, decision version and evaluation timestamp, with dependency definitions pinned to `../01-architecture/MODULE_DEPENDENCIES.md` |
| RDY-002 states | Owned by section 6, covering the entitlement lifecycle and the operations that change it; evaluation order and invariants are fixed by section 5 |
| RDY-003 testable rules | Satisfied by the business rules in section 7 with the enforcement points in section 8 |
| RDY-004 permissions | `entitlements.view_effective_entitlement`, `entitlements.view_module_catalogue`, `entitlements.evaluate_entitlement` as an internal service capability, `entitlements.manage_module_definition` and `entitlements.manage_dependency` as platform-only capabilities. A tenant user never holds authority to change an entitlement; that authority belongs to the provider domain through `subscriptions` |
| RDY-005 interface surfaces | Module availability indicators, the unentitled-module affordance decided by `DEC-UI-004`, and the upgrade path surface, mapped to `../01-architecture/UI_DESIGN_SYSTEM.md` `UIX-012`. Hiding a module is a usability measure and never an authorization boundary |
| RDY-006 reports and imports | Contributes to `RPT-803` module adoption and usage, a provider-domain report. Import is not applicable; entitlement state derives from subscriptions and is never imported directly |
| RDY-007 document numbering | Not applicable. No document type is allocated |
| RDY-008 notifications | Registered in `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md`: module entitled, module entitlement expiring, module entitlement lost, and dependency conflict detected. These are subscription-and-billing category, mandatory and never opt-out per `NTF-011`, because losing a module changes what a tenant can lawfully do in the product |
| RDY-009 classification and retention | Entitlement state is `C2` and contains no personal data. Retention follows `RET-14` for provider-domain subscription records and `RET-09` for entitlement change audit, under `../05-quality/DATA_PROTECTION_AND_RETENTION.md` |
| RDY-010 threats | `THR-022` direct manipulation of entitlement state to obtain unpaid modules, `THR-021` self-granting authority, `THR-012` cache key omitting tenant or entitlement scope, `THR-011` missing filter in an entitlement-aware query, `ABU-08` using an unsubscribed module through a direct endpoint or fragment |
| RDY-011 decision dependencies | The decisions in section 14 remain open. `DEC-COM-001` governs commercial policy and `DEC-UI-004` the unentitled presentation; absent approval the engine denies rather than defaults to granting |
| RDY-012 regulatory assertions | None |

## 17. Migration, Compatibility and Recovery

Entitlement evaluation is on the authorization path for every protected surface, so a change to the decision contract, the evaluation order or the cache key composition is a platform-wide breaking change requiring an ADR under ADR-006. Adding a module definition is additive; removing one requires a deprecation that preserves historical entitlement records, because they explain why past actions were permitted.

A cache or dependency-definition change must invalidate every derived decision, and a stale grant is a security defect rather than a performance artefact. Restore verification confirms module definitions, dependency closure results, effective entitlement per tenant against the authoritative subscription state, that no cached decision survives the restore unvalidated, and audit continuity for entitlement changes.
