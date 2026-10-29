# P08 — Projects, Expenses and Fixed Assets Orchestration Prompt

| Property | Value |
|---|---|
| Document ID | P08-ORCH-001 |
| Status | APPROVED PROMPT BASELINE — IMPLEMENTATION NOT AUTHORIZED |

## Mission

Orchestrate only an authorized P08-SPEC-001 task. Read `AGENTS.md`, PROJ/EXP/FA requirements, PROJECTS/EXPENSES/FIXED_ASSETS, P08-TRACE-001, accepted ADRs, security/testing requirements and current decisions/risks.

## Entry Check

Record task/commit/files, dependency evidence, APPR-P08 status, approved project/expense/asset policy versions, disabled behaviors, cross-module contract versions, migrations, commands, reviewers and evidence paths. Do not infer accounting, VAT, reimbursement, depreciation or settlement policy.

## Delivery Rules

Execute P08-T01–T10 in order. Preserve domain ownership: Projects is operational; Expenses owns claims; Fixed Assets owns register/schedules; Accounting owns ledger; Payroll/Banking owns settlement; ADR-019 governs files. Enforce tenant/object/field access, maker-checker, Decimal determinism, effective snapshots, immutable finalized evidence, idempotency and reconciliation.

Use synthetic data. Never log receipt content, bank data, salary or secrets; never claim an approved claim is paid without exact evidence. Finance/Security/Database/Operations and independent reviews precede Product Owner exit; exit and production activation are separate decisions.
