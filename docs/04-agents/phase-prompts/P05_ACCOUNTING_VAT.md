# P05 — Accounting and UAE VAT Orchestration Prompt

| Property | Value |
|---|---|
| Document ID | P05-ORCH-001 |
| Status | READY FOR REVIEW; NOT IMPLEMENTATION AUTHORIZATION |

## Mission

Orchestrate only an approved P05-SPEC-001 task. Read `AGENTS.md`, ACC/VAT requirements, REG-SRC-001, ADR-011/013, accounting/VAT module specs, P05-TRACE-001, quality baselines and current decisions/risks.

## Entry Check

Record manifest ID, commit/file scope, P01–P03 contract evidence, APPR-P05 status, approved legal entity/accounting/currency/period/VAT policy versions, disabled scenarios, migrations, commands, reviewers and evidence locations. No schema/posting/tax behavior may crystallize an unresolved material policy.

## Sequence and Coordination

Execute P05-T01–T09 in order. `accounting` exclusively owns ledger writes; `vat` exclusively owns tax policy/snapshots/workpapers; sources own business documents. Coordinate shared tenant/entity, Decimal/currency, audit/outbox, reporting and migration boundaries. Require independent review and reproducible evidence, not agent assertions.

## Non-Negotiable Controls

- Balanced atomic posting; immutable posted meaning; linked reversal/adjustment only.
- Exact Decimal/currency/policy snapshots; no floats or client-authoritative totals.
- Effective-dated approved VAT rules; unsupported/ambiguous treatment fails closed.
- Tenant/entity, permission, segregation, entitlement and RLS across every path.
- No tax filing, accounting-standard or compliance claim outside approved evidence.
- Migrations/restores reconcile financial totals and links, not merely row counts.

## Exit

All P05 criteria require executed evidence and Finance, qualified UAE tax, Security, Database, Operations and independent QA disposition. Phase exit and production accounting/VAT scope are separate Product Owner decisions. Update tracking records after each task.
