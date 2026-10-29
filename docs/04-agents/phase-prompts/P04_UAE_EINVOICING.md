# P04 — UAE E-Invoicing Orchestration Prompt

| Property | Value |
|---|---|
| Document ID | P04-ORCH-001 |
| Status | APPROVED PROMPT BASELINE — IMPLEMENTATION NOT AUTHORIZED |

## Mission

Orchestrate only the approved subset of P04-SPEC-001. Read `AGENTS.md`, product requirements, REG-SRC-001, ADR-012, ARCH-EINV-CONTRACT-001, MOD-EINVOICING-001, P04-TRACE-001, security/testing requirements and current decisions/risks before dispatch.

## Mandatory Entry Check

Record the authorized task ID/commit/scope, P03 source contract evidence, APPR-P04 status, approved regulatory/provider/schema/status-map versions, disabled flows, exact files, reviewers, commands and evidence locations. If provider/ruleset approval is absent, restrict work to provider-neutral contracts, models and synthetic tests; do not create a real adapter or regulated field mapping.

## Delivery Sequence

Execute P04-T01–T10 in dependency order. Coordinate changes to invoice contracts, tenancy/IAM, outbox, secrets, settings and shared schemas. Each task must produce code/tests/migrations/docs only within its explicit authorization, run applicable gates, inspect the diff and record reproducible evidence. Completion messages are not proof.

## Non-Negotiable Controls

- Never infer compliance, acceptance or applicability.
- Never select a provider or embed credentials without approved records.
- Never let provider code mutate issued invoice/VAT/accounting truth.
- Fail closed on missing rules/fields/capabilities; timeout is uncertain, not failure-to-receive.
- Enforce tenant/entity, permission and entitlement across request/service/task/callback/report/admin/file paths.
- Preserve native evidence, version mappings and immutable snapshots; no blind retry.
- Use synthetic data and sandbox only until separate production activation.

## Verification and Exit

Map each task to P04 tests/evidence. Independent QA/Security/Privacy/Finance/Operations and qualified UAE review must reproduce the applicable evidence. P04 exit, provider activation and production traffic are separate Product Owner decisions. Update phase/project/decision/risk records after meaningful work.
