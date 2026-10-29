# P06 — Procurement and Inventory Orchestration Prompt

| Property | Value |
|---|---|
| Document ID | P06-ORCH-001 |
| Status | READY FOR REVIEW; NOT IMPLEMENTATION AUTHORIZATION |

## Mission

Orchestrate only an authorized P06-SPEC-001 task. Read `AGENTS.md`, INVN requirements, domain/module/quality specifications, accepted ADRs, P03 item/Sales contracts, P05 Accounting/VAT contracts, P06-TRACE-001 and current decisions/risks.

## Entry Check

Record manifest, commit/file scope, dependency evidence, APPR-P06 status, approved supplier/item/UOM/purchasing/movement/negative/reservation/count/valuation policies, disabled features, migrations, commands, reviewers and evidence paths. Do not crystallize unresolved master ownership or valuation in schema.

## Delivery Rules

Execute P06-T01–T09 in order. Procurement owns purchasing intent; Inventory exclusively owns stock movement; Accounting/VAT own financial/tax consequences. Require immutable revisions/movements, exact Decimal/UOM, idempotency/concurrency, tenant/entity/warehouse isolation, private sensitive data, reconciliation and recovery. No direct balance or ledger write.

Each task runs mapped tests and records reproducible evidence. Independent QA/Security/Finance/Operations/Database review precedes Product Owner exit. Phase exit and production inventory activation are separate decisions; update tracking records after meaningful work.
