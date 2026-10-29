# P12 — Production Launch and Operations Orchestration Prompt

| Property | Value |
|---|---|
| Document ID | P12-ORCH-001 |
| Status | APPROVED PROMPT BASELINE — NO PRODUCTION AUTHORIZATION |

Orchestrate only an explicitly authorized P12 rehearsal, provisioning, deployment or launch task. Read `AGENTS.md`, P12-SPEC/TRACE, all `docs/06-deployment/` specifications, release scope, phase evidence, accepted ADRs and decisions/risks.

Before action, record exact authorization ID, environment/provider/account/region, release commit/digest/config/migrations, scope, cost/destructive effects, RPO/RTO, commands, identities, window, abort/rollback authority, monitoring and evidence paths. Absence of any required authority blocks that action but not safe documentation/rehearsal work.

Execute P12-T01–T10 in order. Use immutable artifacts, protected environments, typed configuration, least privilege, single migrations, preflight/backup confidence, smoke/isolation/reconciliation, stabilization and integrity-protected evidence. Never expose secrets, improvise destructive recovery, deploy excluded scope, incur costs or claim compliance/readiness from startup alone. Independent reviews and exact Product Owner launch statement are mandatory.
