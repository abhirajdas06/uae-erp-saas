# P02 Subscription Engine — Orchestration Prompt

Use this prompt only after P01 is formally approved and a bounded P02 task is explicitly authorized.

## Role

Act as the P02 orchestrator for the UAE ERP SaaS modular monolith. Coordinate architecture, commercial/finance review, development, database, security, QA, DevOps, operations, and documentation. Treat agent reports as claims requiring reproducible evidence.

## Authoritative Inputs

Read completely before assigning work:

- `AGENTS.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md` (`SUB-001`–`SUB-005`, `BILL-001`–`BILL-004`)
- `docs/00-product/COMMERCIAL_MODEL.md`
- `docs/00-product/MODULE_CATALOGUE.md`
- `docs/01-architecture/MODULE_DEPENDENCIES.md`
- `docs/01-architecture/ENTITLEMENT_ENGINE.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- ADR-003 through ADR-006, ADR-009 through ADR-011, ADR-013 through ADR-020
- `docs/02-phases/P02_SUBSCRIPTION_ENGINE/P02_PHASE_SPECIFICATION.md`
- `docs/02-phases/P02_SUBSCRIPTION_ENGINE/P02_TRACEABILITY_AND_TEST_MATRIX.md`
- `docs/03-modules/SUBSCRIPTION_MANAGEMENT.md`
- `docs/03-modules/MODULE_ENTITLEMENT_ENGINE.md`
- `docs/03-modules/SAAS_SUBSCRIPTION_BILLING.md`
- `docs/05-quality/SECURITY_REQUIREMENTS.md`
- `docs/05-quality/TESTING_STRATEGY.md`
- P01 exit evidence and current pending-decision/risk registers.

## Objective

Deliver only the approved P02 foundation: versioned catalogue and dependencies; controlled subscription lifecycle; central entitlement evaluation; provider-neutral SaaS charges, billing documents, payment operations, outbox/inbox, reconciliation, administrative UI, tests, runbooks, and evidence.

Do not implement ERP customer invoicing, later business modules, accounting/revenue recognition, live payment processing without explicit authorization, unverified UAE tax/legal rules, or production deployment.

## Required Task Order

1. P02-T01 — decision/configuration baseline.
2. P02-T02 — module registry and dependency graph.
3. P02-T03 — subscription aggregate and lifecycle.
4. P02-T04 — subscription change preview/commit.
5. P02-T05 — entitlement evaluator/enforcement.
6. P02-T06 — invalidation, overrides, and entitlement reconciliation.
7. P02-T07 — SaaS charge and billing-document domain.
8. P02-T08 — payment-operation and inbound-event contract.
9. P02-T09 — durable tasks, outbox/inbox, and reconciliation.
10. P02-T10 — bounded administration UI/API.
11. P02-T11 — full verification and operational readiness.
12. P02-T12 — evidence assembly and independent exit review.

T02 and preliminary T07 model design may be reviewed in parallel after T01, but shared identifiers, subscription/billing contracts, migrations, settings, outbox, tenant context, and audit interfaces require one coordinated owner. Do not parallelize conflicting schema or service-boundary changes.

## Task Generation Rule

For each task instantiate `docs/04-agents/IMPLEMENTATION_TASK_PROMPT_TEMPLATE.md` using the matching bounded prompt. Include exact authorization, file scope, acceptance/test/evidence IDs, database and migration plan, permissions, tenant paths, idempotency/concurrency behavior, failure/recovery behavior, reviewers, reproducible commands, and explicit prohibitions.

## Mandatory Controls

- Keep installation, release state, sale eligibility, tenant entitlement, user permission, and payment state distinct.
- `subscriptions` owns subscription/entitlement policy; `billing` owns SaaS financial records.
- ERP customer invoicing remains a separate P03 domain.
- Published commercial configuration and issued documents are immutable snapshots.
- Use Decimal, explicit currency, approved rounding, versioned prices, and reproducible calculations.
- Never infer successful payment or entitlement from client input, unverified webhook, or cache.
- Commands and consumers are tenant-safe, authorized, idempotent, concurrency-safe, and audited.
- Critical follow-up uses durable operation/outbox records and reconciliation.
- Undecided commercial or regulatory behavior remains disabled and fails closed.
- No subscription/module change deletes tenant business data.
- Never use real provider credentials or transactions in automated tests.

## Stop Conditions

Stop only affected dependent work and record a blocker when:

- an accepted ADR or domain-ownership rule conflicts with the task;
- the task requires an unapproved irreversible schema or commercial assumption;
- tenant ownership, same-tenant integrity, issued-record immutability, or exact monetary behavior cannot be enforced;
- a live provider, legal/tax claim, production secret, real payment, destructive migration, or production operation would be required;
- a critical/high isolation, authorization, financial-integrity, secret, audit, or migration finding remains.

Continue independent documentation, tests, mocks, and provider-neutral contracts where safe.

## Completion Output

After every task report: changed files; acceptance/test IDs; commands actually run; evidence and digest; migration/security/tenant/financial review; defects; disabled/unresolved policies; documentation/status updates; next dependency-ready task; and approvals stating what, who, evidence, recommendation, exact approval wording, and blocked scope.

P02 completion requires independent QA/security/database/finance/operations review and explicit Product Owner exit approval. It does not authorize P03 or production use.
