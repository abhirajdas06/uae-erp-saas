# P04 — Bounded Task Prompt Pack

| Property | Value |
|---|---|
| Document ID | P04-PROMPTS-001 |
| Status | APPROVED PROMPT BASELINE — IMPLEMENTATION NOT AUTHORIZED |

These bodies require an authorized task manifest with commit/file scope, approved decisions/versions, commands, reviewers and evidence paths.

## P04-T01 — Regulatory Applicability and Ruleset Baseline

Version official artefacts/checksums, amendments, applicability decision inputs, effective dates, exclusions and disabled scenarios. Obtain qualified review; update REG-SRC/decisions/risks. Evidence P04-EV-001/013; tests 001–006, 139. No regulated code from unapproved interpretation.

## P04-T02 — Canonical Snapshot and Preflight

Implement provider-neutral ownership, immutable source/version/hash snapshot, rule/schema references, deterministic validation/hash, same-tenant/entity constraints, migrations and synthetic golden tests. Evidence P04-EV-002; tests 013–032. No provider call.

## P04-T03 — Provider Due Diligence and Onboarding

Capture current accreditation, contracted legal entity/services, security/privacy/data/exit/SLA, exact technical artefacts and sandbox evidence; present choice for human approval. Evidence P04-EV-003. No selection by agent and no credential in repository.

## P04-T04 — Versioned Provider Adapter

After APPR-P04-002/003, implement declared capabilities, preflight/map/submit/query/callback verification/status normalization, secret references and contract tests for exact approved versions. Evidence P04-EV-004; tests 007–012, 023–032, 125–138.

## P04-T05 — Durable Submission Workflow

Implement operation/attempt/outbox, stable idempotency, locking, bounded retry, crash recovery and safe evidence. Network after commit. Evidence P04-EV-005; tests 033–052.

## P04-T06 — Callback, Status and Reconciliation

Implement authenticated replay-safe callbacks, polling/inquiry, native/internal versioned transitions, uncertain queue and reconciliation. Evidence P04-EV-006; tests 043–070. Never map transport success to unsupported acceptance.

## P04-T07 — Rejection and Correction Workflow

Implement rejection investigation and linked credit/correction operations without source/history mutation; audit manual action. Evidence P04-EV-007; tests 071–076.

## P04-T08 — Secure Operator Surfaces and Operations

Deliver accessible status/exception UI, bounded API/reports, permission/entitlement/RLS, secret/payload/log controls, monitoring and runbooks. Evidence P04-EV-008–011; tests 077–114, 125–134.

## P04-T09 — Migration, Recovery and Full Verification

Prove clean/upgrade/overlap, historical schema/adapter/status reads, backup/restore/outbox replay, provider cutover boundary, full test matrix and defect closure. Evidence P04-EV-012–013; tests 115–143.

## P04-T10 — Independent Review and Exit

Independently reproduce evidence and disposition exceptions/limitations. Prepare separate Product Owner decisions for phase exit and production activation. Evidence P04-EV-014; test 144. Reviewer cannot approve own work.
