# Documentation Inventory and Disposition

| Property | Value |
|---|---|
| Document ID | GOV-INVENTORY-001 |
| Status | COMPLETE INVENTORY — APPROVED BASELINE PLUS TWELVE PROPOSED DEVELOPMENT-READINESS ADDITIONS |
| Inventory date | 29 October 2026 |
| Owner | Documentation / Orchestrator |

## 1. Status Vocabulary

`COMPLETE` means substantive and validation-ready, not necessarily human-approved or implemented. `READY_FOR_REVIEW` requires human/domain review. `BLOCKED_EXTERNAL` is complete as a specification but needs a named external decision/fact/evidence. `NOT_APPLICABLE_DUPLICATE` means another named canonical artifact owns the content. `IMPLEMENTATION_DERIVED` means exact values/commands/evidence cannot truthfully exist before implementation.

## 2. Inventory Summary

| Area | Actual inventory | Disposition |
|---|---:|---|
| Product/regulatory Markdown | 12 | COMPLETE; glossary and launch report catalogue added by `GOV-GAP-001` and PROPOSED |
| Architecture/ADR Markdown | 41 | COMPLETE; 20 numbered ADR files plus template/register, and five PROPOSED development-readiness specifications |
| Phase Markdown | 30 | COMPLETE: 13 phase specs, 13 phase trace/matrix records plus P00/P01 supporting records |
| Module Markdown | 25 | COMPLETE: 24 substantive module/capability specs plus template |
| Agent/prompt Markdown | 34 | COMPLETE: eight role charters, task template, README and 24 phase prompt files |
| Quality Markdown | 12 | COMPLETE; five PROPOSED standards added by `GOV-GAP-001` cover accessibility, threat model, privacy/retention, test data and developer workflow |
| Deployment/operations Markdown | 18 | COMPLETE as provider-neutral specifications/templates; `EXTERNAL_API_AND_ACCESS_REQUIREMENTS.md` adds the external access and acquisition register |
| Project-management Markdown | 17 | COMPLETE; `DOCUMENTATION_GAP_AUDIT.md`, `DEVELOPMENT_READINESS_CHECKLIST.md` and `OUTSTANDING_APPROVALS_PACKET.md` record the audit, the tested readiness criterion and the actionable approval set |
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
| UI design system and interaction patterns | `../01-architecture/UI_DESIGN_SYSTEM.md` — PROPOSED; previously deferred by `MASTER_PRODUCT_SPECIFICATION.md` section 13 and required by ADR-007 section 10 |
| Localization, Arabic and right-to-left behavior | `../01-architecture/LOCALIZATION_AND_BILINGUAL_UI.md` — PROPOSED; previously deferred by section 16.9 |
| Document numbering and sequence allocation | `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md` — PROPOSED; previously unowned |
| Notifications and outbound communications | `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md` — PROPOSED; previously unowned |
| Tenant data migration, import and export | `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` — PROPOSED; previously deferred by section 17 |
| Accessibility, browser and device support | `../05-quality/ACCESSIBILITY_AND_BROWSER_SUPPORT.md` — PROPOSED; previously deferred by section 16.8 |
| Threat model | `../05-quality/THREAT_MODEL.md` — PROPOSED; required by SEC-001 and previously unowned |
| Data protection, privacy and retention | `../05-quality/DATA_PROTECTION_AND_RETENTION.md` — PROPOSED; previously deferred by sections 12.5 and 17; periods remain BLOCKED_EXTERNAL |
| Test data, fixtures and demonstration datasets | `../05-quality/TEST_DATA_AND_FIXTURES.md` — PROPOSED; previously unowned |
| Developer onboarding, local environment and contribution workflow | `../05-quality/DEVELOPER_ONBOARDING_AND_WORKFLOW.md` and root `CONTRIBUTING.md` — PROPOSED; previously unowned |
| Glossary and controlled vocabulary | `../00-product/GLOSSARY.md` — PROPOSED; Arabic terminology intentionally unpopulated pending `DEC-GLOS-001` |
| Launch report catalogue | `../00-product/REPORT_CATALOGUE.md` — PROPOSED; previously deferred by section 14 and gated by `DEC-REP-001` |

## 4. Approval and External-Evidence Disposition

- P00–P12 specification baselines, matrices, modules and prompts are approved through Packet A and Packets B–G; the approval record does not authorize implementation.
- P00 formal exit is approved. P01 implementation authorization remains a separate gate.
- Finance, VAT, employment/payroll/WPS, e-invoicing, banking, privacy/retention and operations values remain with named specialist/human decisions.
- PINT AE `1.0.4` is the current technical candidate; selected ASP support, applicability, conformance and production activation are `BLOCKED_EXTERNAL`.
- Application, database, security, provider, performance, recovery and operational evidence is `NOT_RUN` until authorized implementation/rehearsal.
- Production provider/spend/provisioning/deployment and business launch remain explicitly unauthorized.

## 5. Development-Readiness Additions

`GOV-GAP-001` tested sufficiency for implementation rather than inventory completeness and found twelve topics that no document owned and that section 3 had not dispositioned. Those twelve are now listed above and are `PROPOSED`, not approved. The earlier completion records remain accurate for the inventory they describe; this section widens that inventory rather than contradicting them. Counts in section 2 were regenerated after the additions, as that section requires.

## 6. Completion Evidence Required

Repository validators, internal-link/ID/ADR/phase checks and `git diff --check` passed on 29 October 2026; independent audit findings were integrated and `GOV-COMPLETE-001` records the results. A best-effort probe assessed 112 unique external URLs: 90 were reachable and 22 remained automation-unresolved because of anti-bot responses, timeouts or access controls. Unresolved URLs are not represented as verified or broken; all external sources still require dated revalidation at the owning phase/release. Packet A–G approval is recorded; implementation-derived and specialist evidence remains separately gated.
