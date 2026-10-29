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
