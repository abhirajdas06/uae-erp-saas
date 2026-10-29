# P02 — Subscription Engine Phase Specification

| Property | Value |
|---|---|
| Document ID | P02-SPEC-001 |
| Status | READY FOR REVIEW |
| Phase | P02-SUBSCRIPTION-ENGINE |
| Legacy alias | P2-SUBSCRIPTION-ENGINE |
| Implementation Authorization | Not granted by this document |
| Owners | Product, Architecture, Commercial Operations |
| Required predecessor | P01 approved and implemented |

## 1. Objective

Deliver the provider-neutral commercial-control foundation that defines which product modules may be sold, which modules a tenant is entitled to use, and how the platform records and reconciles SaaS subscription charges. P02 must preserve the distinction between tenant entitlement, user authorization, module release state, and payment state.

## 2. Governing Sources

- [Product Requirements](../../00-product/PRODUCT_REQUIREMENTS.md): `SUB-001`–`SUB-005`, `BILL-001`–`BILL-004`.
- [Commercial Model](../../00-product/COMMERCIAL_MODEL.md).
- [Module Catalogue](../../00-product/MODULE_CATALOGUE.md).
- [Development Roadmap](../../00-product/DEVELOPMENT_ROADMAP.md), Phase 2.
- [Module Dependencies](../../01-architecture/MODULE_DEPENDENCIES.md).
- [Entitlement Engine](../../01-architecture/ENTITLEMENT_ENGINE.md).
- [Authentication and Permissions](../../01-architecture/AUTHENTICATION_AND_PERMISSIONS.md).
- [Event and Task Processing](../../01-architecture/EVENT_AND_TASK_PROCESSING.md).
- ADR-003, ADR-004, ADR-005, ADR-006, ADR-009, ADR-010, ADR-013, ADR-014, ADR-015, ADR-017, ADR-018, ADR-020.
- [Security Requirements](../../05-quality/SECURITY_REQUIREMENTS.md) and [Testing Strategy](../../05-quality/TESTING_STRATEGY.md).
- [Subscription Management](../../03-modules/SUBSCRIPTION_MANAGEMENT.md), [Module Entitlement Engine](../../03-modules/MODULE_ENTITLEMENT_ENGINE.md), and [SaaS Subscription Billing](../../03-modules/SAAS_SUBSCRIPTION_BILLING.md).

## 3. Entry Gate

Implementation may begin only when:

1. P01 exit evidence demonstrates tenant context, authentication, authorization, audit, PostgreSQL, migration, and CI foundations.
2. A bounded P02 task is explicitly authorized.
3. The implementer records which commercial policies are approved and which remain configurable or disabled.
4. Required database roles, restricted-runtime tests, background-task infrastructure, and evidence storage are available for the task concerned.
5. No unresolved decision changes the proposed schema irreversibly.

P02 documentation may be reviewed before P01 implementation closes. This does not waive the implementation entry gate.

## 4. Bounded Scope and Non-Goals

### 4.1 Included

- Versioned module catalogue, commercial availability, lifecycle, and dependency rules.
- Tenant subscription aggregate, line selections, effective dates, lifecycle, and history.
- Transactional, idempotent upgrade, downgrade, add, remove, suspend, cancel, expire, and reactivate services, subject to approved policies.
- Deterministic, deny-by-default entitlement evaluation, dependency closure, overrides, degraded access, and tenant-safe cache policy.
- Provider-neutral SaaS billing accounts, charge calculations, billing documents, payment-operation records, credits/corrections, and reconciliation foundations.
- Durable outbox/inbox processing where loss or duplication would materially affect access or money.
- Authorized platform and tenant administration views using Django templates and HTMX; DRF only for an approved consumer.
- Audit, observability, migrations, security review, automated tests, and exit evidence.

### 4.2 Excluded

- ERP invoices issued by a tenant to its customers; those belong to P03.
- Selecting or contracting a paid payment provider.
- Real payment capture without a separately approved provider integration task and sandbox evidence.
- Inventing UAE tax, invoice-retention, or legal-document rules.
- Revenue recognition, general-ledger posting, or accounting for SaaS revenue.
- Deleting customer business data because access ends.
- Implementing later ERP modules merely to demonstrate entitlement checks.
- Production release, customer onboarding, or claims of regulatory compliance.

## 5. Domain Boundaries and Invariants

1. `subscriptions` owns module definitions, commercial dependency policy, subscriptions, selections, entitlement state/history, and subscription-change operations.
2. `billing` owns SaaS billing accounts, charges, billing documents, payment operations, credits, allocations, and reconciliation records.
3. ERP customer invoicing must use a different app, models, numbering, permissions, services, and audit vocabulary.
4. Payment state is evidence used by approved subscription policy; it is never direct authority to grant access.
5. Entitlement and user permission are independent deny-by-default decisions.
6. Client input, URLs, module codes, provider callbacks, cache contents, and task payloads are not trusted authority.
7. Effective-dated and issued records retain historical pricing, currency, policy, and calculation evidence.
8. Repeated or concurrent commands cannot create conflicting subscriptions, duplicate charges, duplicate documents, or repeated entitlements.
9. Module disablement changes permitted operations, not tenant ownership or retention of business data.

## 6. Task Packages and Dependencies

| Task | Objective | Depends on | Primary evidence |
|---|---|---|---|
| P02-T01 | Reconcile approved commercial policies and immutable configuration identifiers | Entry gate | Decision/configuration review |
| P02-T02 | Implement versioned module registry and dependency graph validation | T01 | Model, migration, graph tests |
| P02-T03 | Implement subscription aggregate and lifecycle invariants | T01–T02 | State, constraint, concurrency tests |
| P02-T04 | Implement subscription-change preview/commit services | T03 | Idempotency, rollback, audit tests |
| P02-T05 | Implement central entitlement evaluator and enforcement adapters | T02–T04 | Decision-table and boundary tests |
| P02-T06 | Implement entitlement invalidation, overrides, reconciliation, and optional cache | T05 | Freshness, failure, override tests |
| P02-T07 | Implement provider-neutral SaaS charge and billing-document domain | T01, T03 | Calculation, immutability, separation tests |
| P02-T08 | Implement payment-operation contract and verified inbound-event handling | T07 | Contract, signature fixture, deduplication tests |
| P02-T09 | Implement durable tasks, outbox/inbox, retries, and reconciliation | T04, T06–T08 | Crash/retry/replay tests |
| P02-T10 | Implement bounded subscription, catalogue, entitlement, and billing administration UI | T04–T09 | View, permission, accessibility tests |
| P02-T11 | Complete security, migration, performance, and operational verification | T02–T10 | Review reports and CI artifacts |
| P02-T12 | Assemble exit evidence and independent review | T11 | P02 evidence index and approvals |

Each task must instantiate the implementation task template and specify files, permissions, acceptance IDs, test IDs, migration/forward-fix behavior, reviewers, evidence, and prohibited scope.

## 7. Deliverables

- `subscriptions` and `billing` Django apps only when their tasks are authorized.
- Explicit service contracts and no cross-domain model mutation.
- Tenant-aware database constraints and indexes.
- Versioned configuration and effective-date history.
- Provider-neutral integration interface and safe test adapter; no live credentials.
- Outbox/inbox and durable operation records for material workflows.
- Server-rendered administration workflows and selective APIs where justified.
- Automated test suite mapped by [P02 Traceability and Test Matrix](P02_TRACEABILITY_AND_TEST_MATRIX.md).
- Operational runbooks for reconciliation, retries, policy publication, billing uncertainty, and entitlement incidents.
- Updated architecture, module, status, risk, and decision documentation.

## 8. Phase Acceptance Criteria

| ID | Criterion |
|---|---|
| P02-AC-001 | Module code, lifecycle, commercial availability, dependency policy, and release state are separately represented and versioned. |
| P02-AC-002 | Invalid, cyclic, unavailable, or silently chargeable dependency combinations are rejected before commit. |
| P02-AC-003 | Subscription records use controlled state transitions, effective dates, history, idempotency, and concurrency control. |
| P02-AC-004 | Upgrade, downgrade, addition, removal, suspension, cancellation, expiry, and reactivation obey an approved or explicitly disabled policy. |
| P02-AC-005 | Subscription changes preserve historical configuration and never delete unrelated tenant business data. |
| P02-AC-006 | The central evaluator produces deterministic structured decisions and denies missing, invalid, stale-sensitive, or cross-tenant requests. |
| P02-AC-007 | Entitlement is enforced independently of user permission at views, services, APIs, tasks, reports, exports, files, and admin paths in scope. |
| P02-AC-008 | Overrides are exceptional, authorized, scoped, time-bound, reasoned, reviewed, and audited. |
| P02-AC-009 | Cache use is optional, tenant/policy scoped, invalidated reliably, bounded by freshness policy, and fail-closed for grants. |
| P02-AC-010 | SaaS billing and ERP customer invoicing have distinct ownership, records, numbering, permissions, and services. |
| P02-AC-011 | Charges use approved versioned prices, decimal arithmetic, explicit currency, rounding, billing periods, and reproducible calculation evidence. |
| P02-AC-012 | Issued SaaS billing documents are immutable; corrections use linked credit, cancellation, or replacement workflows. |
| P02-AC-013 | Payment events are authenticated where applicable, idempotent, explicitly stateful, and cannot turn uncertain or failed outcomes into success. |
| P02-AC-014 | Outbox/inbox processing survives rollback, retries, duplicate delivery, task restart, and reconciliation without duplicate business effects. |
| P02-AC-015 | Tenant A cannot view, change, bill, export, or use Tenant B's subscription or entitlement data through any tested boundary. |
| P02-AC-016 | Material changes and privileged reads create durable, redacted, tenant-attributed audit evidence. |
| P02-AC-017 | Clean-install and upgrade migrations pass with restricted roles, supported deployment overlap, and documented forward-fix/rollback boundaries. |
| P02-AC-018 | Observability detects stuck operations, inconsistent subscription/billing/entitlement states, invalid policies, and reconciliation failures without leaking sensitive data. |
| P02-AC-019 | All required tests, security review, finance/commercial review, and operational review meet approved severity thresholds. |
| P02-AC-020 | Exit evidence is complete, reproducible, linked to the commit, independently reviewed, and approved by the Product Owner. |

## 9. Security, Tenant Isolation, and Data Integrity

- Derive tenant context from the trusted P01 mechanism; never from an unvalidated request or task argument.
- Enforce direct or inherited tenant ownership and same-tenant composite references for all tenant-owned records.
- Platform catalogue/pricing administration and tenant subscription self-service require different permissions and scopes.
- Support access and overrides require explicit privileged-access controls; Django admin is not a bypass.
- Never log payment credentials, secrets, full provider payloads, sensitive billing details, or authorization tokens.
- Verify inbound provider authenticity before material state changes; retain only minimum necessary payload evidence.
- Use transactions and constraints for local invariants; use outbox/operation records for required post-commit work.
- Treat critical cross-tenant access, unauthorized entitlement, duplicate monetary effect, secret exposure, or mutable issued documents as no-waiver exit blockers.

## 10. Migration and Operational Requirements

- Provide clean-install and upgrade evidence from the supported predecessor.
- Stable public identifiers use UUIDs; module codes and published configuration identifiers are never reused.
- Published policy changes require preview, impact analysis, authorization, effective date, publication, and reconciliation.
- Deployments must tolerate supported old/new code and queued-message overlap or define a controlled maintenance boundary.
- Backups must include authoritative subscription, billing, operation, outbox/inbox, and audit records; restore drills must verify reconciliation, not only row presence.
- Alerts cover invalid dependency graphs, entitlement failures, cache invalidation failures, duplicate/conflicting transitions, payment uncertainty, outbox age, terminal retries, and reconciliation mismatches.

## 11. Test and Evidence Plan

The [P02 Traceability and Test Matrix](P02_TRACEABILITY_AND_TEST_MATRIX.md) is authoritative for mappings. Required evidence includes:

- P02-EV-001: approved entry-gate and decision snapshot.
- P02-EV-002: schema, ownership, and migration review.
- P02-EV-003: catalogue/dependency test report.
- P02-EV-004: subscription lifecycle/concurrency test report.
- P02-EV-005: entitlement decision and enforcement report.
- P02-EV-006: cache/override/reconciliation report.
- P02-EV-007: charge and billing-document calculation report.
- P02-EV-008: provider-contract/inbound-event simulation report.
- P02-EV-009: outbox/task resilience report.
- P02-EV-010: tenant-isolation and authorization report.
- P02-EV-011: migration and deployment-overlap report.
- P02-EV-012: security and sensitive-data review.
- P02-EV-013: operations/recovery review.
- P02-EV-014: independent completion report and Product Owner decision.

Evidence must include commit SHA, commands, environment, result, artifact reference/digest where applicable, reviewer, limitations, and retention location.

## 12. Exit Gate

P02 may be marked `APPROVED` only when:

1. P02-AC-001 through P02-AC-020 are verified or an explicitly waivable non-security exception is approved and time-bounded.
2. No open critical/high tenant-isolation, authorization, financial-integrity, secret, audit, or migration finding remains.
3. Commercial policy used by implemented flows is approved; undecided flows remain disabled and tested as disabled.
4. Architecture, Security, QA, Database, Finance/Commercial, and Operations reviewers record dispositions.
5. The Product Owner explicitly approves P02 exit.

P02 exit does not authorize P03, production use, provider contracting, or customer charging.

## 13. Pending Approvals

| ID | Decision/approval | Owner | Required before | Recommendation | Exact approval form |
|---|---|---|---|---|---|
| APPR-P02-001 | P02 bounded implementation scope | Product Owner | P02-T01 implementation | Approve this phase specification and task sequence | “I approve P02-SPEC-001 as the bounded P02 implementation scope.” |
| APPR-P02-002 | Initial commercial policy set | Product Owner / Commercial / Finance | Affected lifecycle and billing tasks | Approve only researched prices, intervals, proration, trial, grace, dunning, refund, tax, and cancellation rules; disable the rest | Reference approved `CM-DEC-*` decisions and effective date |
| APPR-P02-003 | Payment provider and integration mode | Product Owner / Security / Finance | Live provider task | Keep provider-neutral contracts and mocks until due diligence is complete | Approve provider, mode, jurisdictions, data handling, and evidence |
| APPR-P02-004 | P02 exit | Product Owner | Phase transition | Approve only after P02-EV-014 independent review | “I approve the P02 exit evidence and authorize the stated next phase separately.” |
