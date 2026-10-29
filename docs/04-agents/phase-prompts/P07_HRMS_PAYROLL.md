# P07 — HRMS and Payroll Orchestration Prompt

| Property | Value |
|---|---|
| Document ID | P07-ORCH-001 |
| Status | APPROVED PROMPT BASELINE — IMPLEMENTATION NOT AUTHORIZED |

## Mission

Orchestrate only an authorized P07-SPEC-001 task. Read `AGENTS.md`, HR/PAY requirements, REG-HR-001, module specs, P07-TRACE-001, accepted ADRs, security/testing requirements and current decisions/risks.

## Entry Check

Record task/commit/files, dependency evidence, APPR-P07 status, approved employer/employee jurisdiction, employment/leave/payroll/pension/WPS/privacy ruleset and artefact checksums, disabled scenarios, migrations, commands, reviewers and evidence paths. No legal/payroll rule may be inferred from common practice.

## Delivery Rules

Execute P07-T01–T10 in order. HRMS owns employee/employment/leave; Payroll owns immutable calculation/results; Users owns login; Accounting owns postings; bank/WPS agent owns settlement. Enforce field/purpose/object access, maker-checker, Decimal determinism, effective versions, private files, idempotency, reconciliation and recovery.

Use synthetic data. Never log salary/bank/identity/medical/secret payloads, claim compliance, or map local export/upload to WPS settlement. Qualified UAE Legal/Payroll/WPS/Pension/Privacy and independent reviews precede Product Owner exit. Exit and production activation are separate decisions.
