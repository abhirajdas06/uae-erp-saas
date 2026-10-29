# P12 — Bounded Task Prompt Pack

| Property | Value |
|---|---|
| Document ID | P12-PROMPTS-001 |
| Status | READY FOR REVIEW |

Every task requires explicit authorization appropriate to rehearsal, infrastructure spend/provisioning, production deployment or launch. Never infer broader authority.

## P12-T01 — Launch Scope, Targets and Inventory
Approve exact release/modules/providers/tenants, topology/region, RPO/RTO/availability, ownership, budget and evidence dependencies. EV-001–002; tests 001–012.

## P12-T02 — Build, Supply Chain and Promotion
Produce reproducible non-root immutable image with digest, provenance/SBOM/scans and protected registry promotion. EV-003; tests 013–027.

## P12-T03 — Production Configuration and Infrastructure
Validate typed config, secrets, role/network/TLS/DNS/storage/observability with no development defaults. EV-002/004; tests 028–042. Provision only under APPR-P12-002.

## P12-T04 — Deployment, Migration and Recovery Rehearsal
Execute clean deploy, compatibility/lock/backfill analysis, migration failure and rollback/forward-fix exercises. EV-005–006/016; tests 043–055.

## P12-T05 — Release Security and Domain Verification
Run isolation, authorization, entitlement, files/audit and critical financial/domain/provider candidate tests. EV-007/014; tests 056–075/137–148.

## P12-T06 — Monitoring, Backup and Restore
Inject signals/alerts; validate protected backups; independently restore/PITR/files and reconcile actual RPO/RTO. EV-008–011; tests 076–120.

## P12-T07 — Capacity, Resilience and Operations Exercises
Run representative load/soak/failure and incident/runbook exercises; verify integrity, headroom, escalation and findings. EV-012–013; tests 121–136/161–170.

## P12-T08 — UAT, Onboarding and Support Readiness
Execute bounded user journeys, onboarding, locale/accessibility, support/training and defect disposition. EV-015; tests 149–160.

## P12-T09 — Independent Release Review
Complete Security/Privacy/Database/Finance/Domain/Operations reviews, residual-risk decisions and evidence-manifest verification. EV-017; tests 171–175.

## P12-T10 — Production Deployment, Launch and Stabilization
Only after APPR-P12-003/004, deploy exact release, run smoke/isolation/reconciliation, observe abort thresholds, record launch and post-launch review. EV-018; tests 176–180. Production launch authority is never delegated to an agent.
