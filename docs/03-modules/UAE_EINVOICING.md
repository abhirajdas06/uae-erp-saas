# E_INVOICING — UAE E-Invoicing Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-EINVOICING-001 |
| Status | APPROVED SPECIFICATION — PROVIDER/SPECIALIST GATES REMAIN |
| Owning phase / app | P04 / `e_invoicing` |
| Commercial module | Yes; entitlement plus permission required |

## 1. Purpose and Scope

Own provider-bound preparation, validation, submission, evidence, status, callback and reconciliation for approved UAE electronic invoices and electronic credit notes. Implements `EIN-001`–`EIN-005` under P04-SPEC-001, ADR-012, REG-SRC-001, ARCH-PINT-AE-002, ARCH-PINT-AE-MAP-001 and ARCH-EINV-CONTRACT-001.

Included: effective-dated applicability; provider configurations by tenant/legal entity/environment; canonical snapshots; approved PINT AE transaction-profile mapping/UBL serialization/shared-and-AE Schematron/code-list validation; operations/attempts; adapters; callbacks; exception queues; reconciliation; audit, reports and runbooks. Excluded: invoice authorship, VAT policy, ledger posting, provider selection by code, direct-government assumptions, PDF/email as eInvoice, Self-Billing or other unapproved document types, and compliance claims.

## 2. Actors and Permissions

| Actor | Scope |
|---|---|
| Configuration administrator | Reference approved provider account/environment and non-secret configuration |
| Submission operator | View eligible prepared records and submit within assigned entity |
| Exception/reconciliation operator | Investigate rejected/uncertain operations and execute approved actions |
| Finance/tax reviewer | Review source/rule/status evidence and corrections |
| Auditor/support | Read-only or purpose-bound privileged access; restricted payload access separately granted |

Prepare, submit, retry, reconcile, configure, export, view restricted payload and activate production are distinct permissions.

## 3. Authoritative Records and Invariants

Conceptual records: `RegulatoryRuleSet`, `ApplicabilityDecision`, `ProviderAccountReference`, `CanonicalDocumentSnapshot`, `SubmissionOperation`, `SubmissionAttempt`, `ProviderEvidence`, `CallbackReceipt`, `StatusMapping`, `ReconciliationCase` and `ProviderHealthObservation`.

- UUID public IDs and explicit tenant/legal-entity ownership; all source/provider/callback relationships are same-tenant/account valid.
- One source document version/hash and submission purpose maps to at most one active authoritative operation under the approved retry/correction model.
- Snapshot, ruleset, transaction profile, semantic mapping, UBL syntax, code-list/resource checksums, Schematron, adapter and status-map versions are immutable after preparation/submission.
- Attempts/evidence append; native status is never overwritten by a normalized label.
- Secrets are references to the approved secret store, never model fields or exported configuration.
- Ordinary deletion of submitted evidence is prohibited; retention disposal is policy-controlled and audited.

## 4. Workflows

**Applicability/preflight:** resolve effective policy from trusted tenant/legal-entity/transaction facts. Missing, expired, ambiguous or unsupported policy blocks preparation with a safe reason.

**Preparation:** fetch the immutable invoicing snapshot, validate content and correction links, build canonical form, map reviewed `IBT`/`IBG`/`BTAE` terms, serialize the exact UBL transaction profile, run structural/shared-PINT/AE-specific/code-list/provider-preflight layers, calculate hashes, and persist versioned findings plus outbox intent atomically. Current CRM/config changes cannot change it.

**Submission:** worker resolves approved adapter/environment/secret, maps and validates again, sends with stable idempotency controls, and records sanitized request evidence and response. Network work occurs after commit.

**Status/callback:** authenticate callback, enforce replay/deduplication, route via trusted provider account, record native evidence, apply allowed versioned transition, and quarantine unknown/conflicting events. Polling follows the same evidence service.

**Failure/reconciliation:** validation and permanent errors do not retry automatically. Bounded transient errors may retry. Timeout/crash after possible send is uncertain; provider inquiry/reconciliation precedes any resubmission. Manual actions require reason and audit.

**Correction:** source domain issues an approved credit/correction. The module prepares a new linked operation; it never edits the original invoice or prior submission evidence.

## 5. Rules and Acceptance Criteria

| ID | Rule / verification |
|---|---|
| EINM-001 | Only an approved effective ruleset can qualify a document; negative/applicability tests |
| EINM-002 | Canonical snapshot matches immutable source version/hash and approved totals; golden/contract tests |
| EINM-003 | Provider adapter is versioned and provider-specific behavior does not leak into invoicing; architecture tests |
| EINM-004 | One durable idempotent operation/attempt history exists per approved business key; concurrency/retry tests |
| EINM-005 | Timeout and crash cannot cause blind duplicate submission; failure-injection/reconciliation tests |
| EINM-006 | Native/internal statuses and acceptance meanings are distinct and historical; transition tests |
| EINM-007 | Callback authenticity, replay, order, account and tenant routing are enforced; security tests |
| EINM-008 | Rejection/correction/operator action preserves source and full traceability; workflow tests |
| EINM-009 | Secrets/full payloads are absent from logs/errors/ordinary exports; scanning/redaction tests |
| EINM-010 | Every UI/API/task/admin/report/file boundary enforces entitlement, permission and isolation; IDOR/RLS tests |
| EINM-011 | Schema/provider/status changes and restore preserve historical readability/reconciliation; migration/recovery tests |
| EINM-012 | Labels, reports and product claims never imply unsupported compliance/acceptance; content/review tests |

## 6. Interfaces, UI and Operations

Consumes `PrepareElectronicDocument.v1`; emits controlled status/reconciliation facts defined by ARCH-EINV-CONTRACT-001. APIs follow ADR-020; decimals are strings and provider payloads are not general API responses. UI shows eligibility, validation, source version, internal/native status, attempt timeline, safe evidence, correction links and allowed next action. Reports define date/status/provider/entity semantics and mask sensitive data.

Monitor validation/rejection/uncertain/backlog/latency/callback/rate-limit/authentication/schema/credential signals. Runbooks cover rejection, outage, uncertainty, callback attack, schema cutover, credential rotation and provider transition. Backup/restore reconciles hashes, operations, references, states, outbox and audit.

## 7. Decisions and Implementation Prompt

Dependent approvals are APPR-P04-001–004. Provider-neutral model/interface work can proceed only under an authorized P04 task; provider mapping/submission cannot proceed without provider and ruleset approval. Use P04 orchestration and P04-T01–T10; evidence/test identifiers are in P04-TRACE-001.

## 8. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved. Nothing here asserts applicability, accreditation, a deadline or compliance; the technical candidate, its version and its evidence remain governed by `ARCH-PINT-AE-002`, `ARCH-PINT-AE-MAP-001` and the [e-invoicing provider contract](../01-architecture/UAE_EINVOICING_PROVIDER_CONTRACT.md), and activation is `BLOCKED_EXTERNAL`.

| Gate | Disposition for `e_invoicing` |
|---|---|
| RDY-001 attributes | Section 3 names the authoritative records and invariants. A submission record carries tenant, source document reference, profile and version identifier, generated payload reference with checksum, immutable payload hash, idempotency key, provider reference, status, attempt history and provider-native evidence reference. Mapped field cardinalities and conditions are owned by `ARCH-PINT-AE-MAP-001`, which still requires machine reconciliation to the approved version before implementation |
| RDY-002 states | Section 4 owns the workflows. Submission states are explicitly evidence-driven, including an uncertain state, and local state never advances to accepted, cleared or reported without provider or authority evidence. A submitted payload is immutable; a correction is a new document and a new submission, never a rewrite |
| RDY-003 testable rules | Satisfied by the rules and acceptance criteria in section 5, each with a named verification method |
| RDY-004 permissions | `e_invoicing.view_submission`, `e_invoicing.generate_payload`, `e_invoicing.validate_payload`, `e_invoicing.submit_document`, `e_invoicing.resubmit_document`, `e_invoicing.view_payload_evidence`, `e_invoicing.configure_profile`, `e_invoicing.configure_provider`, `e_invoicing.reconcile_submission`, `e_invoicing.export_submission_evidence`, `e_invoicing.view_all_submissions`. Generating, submitting and resubmitting are separate, and provider configuration is separate from all of them |
| RDY-005 interface surfaces | Submission status list with exception filters, per-document submission detail with validation findings and provider-native status, payload evidence inspection under purpose capture, resubmission confirmation, profile and provider configuration, and reconciliation review, mapped to the data table, status badge, asynchronous operation status and confirmation dialog components in `../01-architecture/UI_DESIGN_SYSTEM.md`. No surface presents a provider acknowledgement as regulatory compliance |
| RDY-006 reports and imports | Owns `RPT-209` e-invoicing submission status and contributes exception rows to `RPT-305` in `../00-product/REPORT_CATALOGUE.md`. Import of historical invoices is owned by `../01-architecture/DATA_MIGRATION_AND_IMPORT.md`, whose `MIG-056` excludes migrated historical documents from statutory submission by default; whether any must be submitted is the open question `DEC-MIG-004` |
| RDY-007 document numbering | No document type is owned here. The invoice, credit note and debit note numbers carried in a payload are allocated by `ERP_CUSTOMER_INVOICING.md` and registered in `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md`; `SEQ-035` requires the number in a structured payload to match the stored authoritative value exactly |
| RDY-008 notifications | Registered in `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md`: payload validation failed, submission accepted, submission rejected, submission uncertain past its window, provider credential expiring, profile version deprecated, and reconciliation variance detected. All are regulatory-status category, mandatory and never digested. `NTF-065` prohibits presenting delivery evidence as proof of regulatory submission |
| RDY-009 classification and retention | Submission metadata is `C2`; generated payloads and provider evidence contain full invoice and counterparty detail and are `C4` in effect; provider credentials are `C5` and exist only as secret-backend references per ADR-017. Retention class is `RET-03` for tax invoices and submission evidence, under `../05-quality/DATA_PROTECTION_AND_RETENTION.md`; the period is unresolved pending `DEC-PRIV-005` and is not asserted |
| RDY-010 threats | `THR-040` forged provider webhook creating a false regulatory state, `THR-041` replayed callback duplicating a submission, `THR-042` compromised credential used to submit under the tenant identity, `THR-043` server-side request forgery, `THR-046` provider outage cascading, `THR-047` loss of acknowledgement evidence, `ABU-02` issuing then silently altering a submitted invoice, `ABU-09` duplicate submission through retry |
| RDY-011 decision dependencies | Provider and service-provider selection, applicability, profile version activation and the conformance gate all remain `BLOCKED_EXTERNAL`. Generation and submission stay disabled and visibly unavailable until the owning approvals are recorded; the module never submits under an unapproved profile or provider |
| RDY-012 regulatory assertions | None. No applicability, threshold, deadline, accreditation or compliance status is asserted, and a successful API exchange is never treated as proof of compliance, per `AGENTS.md` section 11 |

## 9. Migration, Compatibility and Recovery

A profile version is pinned per submission, and a historical submission is always interpreted under the version it used, because reinterpreting it under a later profile would misrepresent what was transmitted. A profile upgrade is additive: a new version is configured, newly generated payloads use it, and prior submissions and their evidence remain unchanged.

Restore verification confirms submission counts by status and period, payload and evidence checksums, idempotency keys, that no submission advanced status during restore without evidence, that provider-native evidence is retained separately from internal status per `INTM-007`, and that no credential material was captured in a backup artifact.
