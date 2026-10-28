# P02 — Bounded Task Prompt Pack

| Property | Value |
|---|---|
| Document ID | P02-PROMPTS-001 |
| Status | READY FOR REVIEW |
| Use with | `IMPLEMENTATION_TASK_PROMPT_TEMPLATE.md` and `P02_SUBSCRIPTION_ENGINE.md` |

These are task bodies, not implementation authorization. The orchestrator must add the authorization reference, exact repository scope, current commit, commands, reviewers, evidence locations, and unresolved decisions before dispatch.

## P02-T01 — Decision and Configuration Baseline

**Objective:** Produce the machine-readable/controlled baseline of approved, unresolved, and disabled commercial policies without implementing business features.

**Scope:** Reconcile `CM-DEC-*`, `PRD-DEC-001/002/014`, module codes, lifecycle states, billing intervals, currencies, pricing/tax/rounding sources, trial/grace/dunning/refund/cancellation policy, and provider status. Define immutable identifiers and configuration publication workflow.

**Acceptance/evidence:** P02-AC-001, 004, 011; P02-EV-001. Verify every unresolved behavior is explicitly disabled or represented as pending. No price, tax, provider, deadline, or legal rule may be invented.

## P02-T02 — Module Registry and Dependency Graph

**Objective:** Implement versioned module definitions, lifecycle/commercial release states, policy versions, and dependency validation.

**Scope:** Models, constraints, publication service, effective dates, directed graph validation, preview, permissions, audit, migrations, and tests. Do not implement subscriptions or business modules.

**Acceptance/evidence:** P02-AC-001–002, 015–017; P02-TST-001–009, 090–106, 107–112 as applicable; P02-EV-002–003, 010–012. Reject cycles, missing dependencies, overlaps, retired/unreleased sale, unauthorized publication, and silent paid dependency.

## P02-T03 — Subscription Aggregate and Lifecycle

**Objective:** Implement the tenant subscription aggregate, selections, history, and policy-gated lifecycle.

**Scope:** Tenant-aware models, same-tenant constraints, states/transitions, versioning/locking, idempotency records, effective dates, audit, migrations, and tests. Undecided transitions remain disabled.

**Acceptance/evidence:** P02-AC-003–005, 015–017; P02-TST-010–026, 090–112; P02-EV-002, 004, 010–012. No billing implementation, entitlement bypass, or business-data deletion.

## P02-T04 — Subscription Change Preview and Commit

**Objective:** Implement one transactional service for upgrade, downgrade, add, remove, suspend, cancel, expire, and reactivate commands allowed by policy.

**Scope:** Deterministic preview, dependency/price reference resolution, confirmation token/version precondition, idempotent commit, outbox intent, failure/rollback, provisioning operation, reconciliation hooks, and tests.

**Acceptance/evidence:** P02-AC-002–005, 014, 016; P02-TST-005–026, 082–089, 102–106; P02-EV-003–004, 009, 012. Preview must expose consequences; commit must reject stale preview/configuration.

## P02-T05 — Central Entitlement Evaluator and Enforcement

**Objective:** Implement a deterministic structured entitlement decision and adapters for every in-scope boundary.

**Scope:** Evaluator, reason codes, operation classes, dependency resolution, lifecycle/effective-date policy, service/view/API/task/report/file/admin enforcement, and tests. User/object authorization stays independent.

**Acceptance/evidence:** P02-AC-006–007, 015; P02-TST-027–043, 090–101; P02-EV-005, 010. Unknown/missing/invalid context denies; no UI-only or feature-flag enforcement.

## P02-T06 — Entitlement Invalidation, Overrides, and Reconciliation

**Objective:** Make entitlement changes safe under cache, concurrency, override, and partial-failure conditions.

**Scope:** Generation/version invalidation, optional cache only if justified, authoritative sensitive recheck, time-bound override, recompute operation, reconciliation, metrics/runbooks, and tests.

**Acceptance/evidence:** P02-AC-008–009, 014, 016, 018; P02-TST-044–054, 082–089, 102–106, 113–118; P02-EV-006, 009, 012–013. Prefer no cache until measured need; cache outage never grants.

## P02-T07 — SaaS Charge and Billing-Document Domain

**Objective:** Implement provider-neutral SaaS charge calculation and immutable billing documents, wholly separate from P03 invoicing.

**Scope:** Billing account, charge snapshot, document/line, sequence, issue, correction/credit foundations, allocations/balance, Decimal/currency/rounding, permissions, audit, migrations, and tests. Only approved pricing/tax rules may run.

**Acceptance/evidence:** P02-AC-010–012, 015–017; P02-TST-055–073, 090–112; P02-EV-002, 007, 010–012. No ledger/revenue recognition, ERP invoice models, live payment, or invented UAE rule.

## P02-T08 — Payment Operation and Inbound Event Contract

**Objective:** Implement provider-neutral payment operations and secure, idempotent inbound-event handling with mocks/sandbox contracts.

**Scope:** Adapter protocol, internal state machine, idempotency, minimal inbox/quarantine, authenticity interface, timeout/uncertainty, versioned schemas, reconciliation hooks, and tests. Provider-specific adapter requires separate approval.

**Acceptance/evidence:** P02-AC-013, 015–016; P02-TST-074–081, 090–106; P02-EV-008, 010, 012. No real credentials/transactions; uncertain never means success.

## P02-T09 — Durable Processing and Reconciliation

**Objective:** Close dual-write and recovery gaps for subscription, entitlement, billing, and provider follow-up.

**Scope:** ADR-010 outbox/inbox integration, claims/leases, bounded retry, idempotent consumers, schema versions, replay authorization, reconciliation services, observability, and runbooks.

**Acceptance/evidence:** P02-AC-014, 016, 018; P02-TST-082–089, 102–106, 113–118; P02-EV-009, 012–013. Broker is not authority; duplicate and crash points cause no duplicate business effect.

## P02-T10 — Administration UI and Approved APIs

**Objective:** Deliver accessible server-rendered workflows for catalogue, subscriptions, entitlements, billing, and reconciliation.

**Scope:** Django/HTMX views, forms, safe error/remediation messages, pagination/filtering, confirmation, downloads, permissions, CSRF, audit, and view tests. DRF only for an approved consumer.

**Acceptance/evidence:** P02-AC-006–016; applicable P02-TST-027–106; P02-EV-005–010, 012. Direct URL/HTMX/API paths repeat server-side authorization and tenant checks.

## P02-T11 — Full Verification and Operational Readiness

**Objective:** Execute the complete P02 matrix and close review findings.

**Scope:** Unit/database/service/view/task/migration/security/performance suites; restricted-role and RLS evidence; clean/upgrade deployment; backup/restore reconciliation; runbooks; security, finance, database, and operations review.

**Acceptance/evidence:** P02-AC-001–019; P02-TST-001–121; P02-EV-001–013. Do not convert `NOT_RUN` to passed without command, commit, environment, artifact, and result evidence.

## P02-T12 — Exit Evidence and Independent Review

**Objective:** Assemble an immutable evidence index and independent completion report for human decision.

**Scope:** Map every acceptance criterion to evidence; verify artifacts/digests; disposition defects, exceptions, risks, disabled policies, and pending approvals; obtain independent QA/security/database/finance/operations reviews; prepare Product Owner decision.

**Acceptance/evidence:** P02-AC-020; P02-TST-122; P02-EV-014. The reviewer must not approve their own work. Product Owner approval is a separate human gate and does not authorize P03 unless explicitly stated.
