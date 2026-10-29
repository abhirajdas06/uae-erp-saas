# Documentation Inventory and Disposition

| Property | Value |
|---|---|
| Document ID | GOV-INVENTORY-001 |
| Status | COMPLETE INVENTORY — APPROVED DOCUMENTATION BASELINE |
| Inventory date | 29 October 2026 |
| Owner | Documentation / Orchestrator |

## 1. Status Vocabulary

`COMPLETE` means substantive and validation-ready, not necessarily human-approved or implemented. `READY_FOR_REVIEW` requires human/domain review. `BLOCKED_EXTERNAL` is complete as a specification but needs a named external decision/fact/evidence. `NOT_APPLICABLE_DUPLICATE` means another named canonical artifact owns the content. `IMPLEMENTATION_DERIVED` means exact values/commands/evidence cannot truthfully exist before implementation.

## 2. Inventory Summary

| Area | Actual inventory | Disposition |
|---|---:|---|
| Product/regulatory Markdown | 10 | COMPLETE / specialist gates identified |
| Architecture/ADR Markdown | 36 | COMPLETE; 20 numbered ADR files plus template/register |
| Phase Markdown | 30 | COMPLETE: 13 phase specs, 13 phase trace/matrix records plus P00/P01 supporting records |
| Module Markdown | 25 | COMPLETE: 24 substantive module/capability specs plus template |
| Agent/prompt Markdown | 34 | COMPLETE: eight role charters, task template, README and 24 phase prompt files |
| Quality Markdown | 7 | COMPLETE / newly added standards ready for review |
| Deployment/operations Markdown | 17 | COMPLETE as provider-neutral specifications/templates |
| Project-management Markdown | 14 | COMPLETE / completion audit present; current approvals tracked separately |
| Repository traceability Markdown | 2 | COMPLETE / implementation evidence remains planned |

Counts describe the working tree at inventory time and must be regenerated after material additions/removals.

## 3. Required Artifact Disposition

| Requested artifact class | Canonical path/disposition |
|---|---|
| Repository instructions | `AGENTS.md` — COMPLETE |
| Repository goal record | `GOALS.md` — COMPLETE; active Codex Goal remains separate |
| Overall/phase status | `PROJECT_STATUS.md`, `PHASE_STATUS.md` — COMPLETE |
| ADR register/template/001–020 | Architecture decisions directory — COMPLETE; preserve recorded approval provenance |
| Pending decisions / risks / changelog | `DECISIONS_PENDING.md`, `RISKS_AND_ISSUES.md`, `CHANGELOG.md` — COMPLETE |
| Requirements traceability / ID convention | `docs/08-requirements-traceability/` — COMPLETE |
| Eight agent role charters | `docs/04-agents/` — COMPLETE |
| Security/testing/CI | Existing quality baselines — COMPLETE |
| DoD/coding/performance/release | `docs/05-quality/` — COMPLETE, READY_FOR_REVIEW |
| Deployment architecture/infrastructure/env/guide | `docs/06-deployment/` — COMPLETE specifications |
| Backup/monitoring/incident/release/capacity/runbooks | `docs/06-deployment/` — COMPLETE specifications/templates |
| Exact topology/provider/contacts/commands/thresholds/RPO/RTO | IMPLEMENTATION_DERIVED / BLOCKED_EXTERNAL by DEC-OPS-001–005; omission is intentional, not hidden |
| P00–P12 phase specifications | 13 owning phase specs — COMPLETE |
| Phase task breakdowns | Phase spec task sections + bounded prompt packs — NOT_APPLICABLE_DUPLICATE for separate `TASKS.md` |
| Phase acceptance criteria | Phase spec AC sections — NOT_APPLICABLE_DUPLICATE for separate `ACCEPTANCE_CRITERIA.md` |
| Phase test plans | Phase traceability/test matrices — NOT_APPLICABLE_DUPLICATE for separate `TEST_PLAN.md` |
| Phase deployment requirements | Phase operational/deployment sections + canonical deployment docs — NOT_APPLICABLE_DUPLICATE for separate files |
| Phase MVP files | Bounded scope/non-goals in each phase spec — NOT_APPLICABLE_DUPLICATE |
| Planned modules | 24 module specs cover all named domains, with clearer filenames for Core/Tenants/Users/Billing/Invoicing — COMPLETE |
| Module prompt directory | Module documents contain implementation prompts/boundaries — separate directory NOT_APPLICABLE_DUPLICATE |

## 4. Approval and External-Evidence Disposition

- P00–P12 specification baselines, matrices, modules and prompts are approved through Packet A and Packets B–G; the approval record does not authorize implementation.
- P00 formal exit is approved. P01 implementation authorization remains a separate gate.
- Finance, VAT, employment/payroll/WPS, e-invoicing, banking, privacy/retention and operations values remain with named specialist/human decisions.
- PINT AE `1.0.4` is the current technical candidate; selected ASP support, applicability, conformance and production activation are `BLOCKED_EXTERNAL`.
- Application, database, security, provider, performance, recovery and operational evidence is `NOT_RUN` until authorized implementation/rehearsal.
- Production provider/spend/provisioning/deployment and business launch remain explicitly unauthorized.

## 5. Completion Evidence Required

Repository validators, internal-link/ID/ADR/phase checks and `git diff --check` passed on 29 October 2026; independent audit findings were integrated and `GOV-COMPLETE-001` records the results. A best-effort probe assessed 112 unique external URLs: 90 were reachable and 22 remained automation-unresolved because of anti-bot responses, timeouts or access controls. Unresolved URLs are not represented as verified or broken; all external sources still require dated revalidation at the owning phase/release. Packet A–G approval is recorded; implementation-derived and specialist evidence remains separately gated.
