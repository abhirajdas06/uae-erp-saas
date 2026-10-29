# P09 — Banking and Advanced Finance Orchestration Prompt

| Property | Value |
|---|---|
| Document ID | P09-ORCH-001 |
| Status | APPROVED PROMPT BASELINE — IMPLEMENTATION NOT AUTHORIZED |

## Mission

Orchestrate only an authorized P09-SPEC-001 task. Read `AGENTS.md`, BANK requirements, REG-BANK-001, ARCH-BANK-CONTRACT-001, BANKING, P09-TRACE-001, accepted ADRs, security/testing requirements and current decisions/risks.

## Entry Check

Record task/commit/files, APPR-P09 status, exact capability mode, regulatory/legal role evidence, bank/provider/license snapshot, consent/security/schema/status contract versions and checksums, disabled modes, statement/matching/reconciliation policies, migrations, commands, reviewers and evidence paths.

## Delivery Rules

Execute P09-T01–T10 in order. Default to Mode A manual import/reconciliation. Modes B–D require exact prior approval. Preserve provider-native evidence and Accounting authority; normalization/matching is non-authoritative until confirmed. Enforce private files, tenant/object access, maker-checker, idempotent durable operations, authenticated callbacks, uncertain-outcome reconciliation and truthful status semantics.

Use synthetic data and provider sandboxes. Never log full account/transaction/consent/credential payloads, infer licensing, claim bank access, or map local preparation/provider receipt to settlement. Qualified Finance, UAE Legal/Compliance, provider, Security, Database, Operations and independent reviews precede exit; each production mode is separately activated.
