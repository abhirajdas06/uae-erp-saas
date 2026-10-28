# BILLING — SaaS Subscription Billing Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-BILLING-001 |
| Status | READY FOR REVIEW |
| Owning Phase | P02 |
| Django App | `billing` |
| Domain Owner | SaaS Subscription Billing |
| Commercial Module | No; platform provider capability |
| Tenant-Owned Data | Tenant/customer-account billing records plus controlled platform configuration |

## 1. Purpose and Sources

Own charges made by the SaaS operator for use of the ERP platform. Implement `BILL-001`–`BILL-004` while remaining strictly separate from ERP customer invoicing in P03. Governing sources are the [P02 phase specification](../02-phases/P02_SUBSCRIPTION_ENGINE/P02_PHASE_SPECIFICATION.md), [Commercial Model](../00-product/COMMERCIAL_MODEL.md), ADR-010, ADR-011, ADR-013, ADR-014, ADR-015, ADR-017, ADR-018, ADR-019, and ADR-020.

## 2. Scope

Included: billing account, charge calculation snapshot, SaaS billing document, line, credit/correction, payment operation/attempt, allocation, inbound provider event, reconciliation, provider-neutral adapter, audit, and authorized customer/platform views.

Excluded: tenant-issued ERP invoices, accounting ledger/revenue recognition, provider selection/contracting, storing card credentials, unsupported taxes, and real charging before explicit provider authorization.

## 3. Actors and Authorization

- Tenant billing administrator: own account/documents, approved checkout/remediation actions.
- Platform billing operator: controlled issue, correction, reconciliation, and support actions.
- Finance/commercial approver: publish approved billing policies and review corrections/refunds.
- Provider service principal: authenticated narrow webhook/return contract; no general tenant access.
- Auditor/support: scoped read or purpose-limited action under privileged policy.

No actor may edit issued documents or mark a payment successful without authoritative evidence and service validation.

## 4. Domain Ownership

| Record/capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Billing account | `billing` | Direct tenant/customer account | Billing account service |
| Charge/calculation snapshot | `billing` | Billing account/subscription reference | Charge service |
| SaaS billing document/line | `billing` | Billing account | Document issue/correction service |
| Payment operation/attempt | `billing` | Billing account/document | Payment service/adapter |
| Provider event/inbox | `billing` | Resolved tenant or quarantined | Verified inbound-event service |
| Credit/allocation/reconciliation | `billing` | Billing account | Controlled finance service |

`billing` references subscription snapshots; it does not mutate subscription or entitlement tables directly.

## 5. Data and Monetary Requirements

- UUID identifiers, trusted tenant/account ownership, same-tenant references, explicit currency, decimal amounts, and ADR-013 rounding policy.
- Charge snapshots preserve plan/price/policy version, quantity, period, tax decision source, discount/proration components, rounding, and calculation version.
- Billing documents have a domain-specific sequence/identifier, lifecycle, issue timestamp, immutable customer/line/totals snapshot, balance, and correction links.
- Payment operations preserve provider-neutral state, idempotency key, provider reference (non-secret), amount/currency, attempts, timestamps, and safe error/reconciliation status.
- Constraints enforce nonnegative/allowed signed amounts, currency agreement, unique event/provider/idempotency identifiers within scope, balanced totals, and valid state transitions.
- Secrets, PAN/card credentials, CVV, tokens not intended for storage, and full unnecessary payloads are prohibited.

## 6. Workflows and States

### 6.1 Charge and issue

Resolve approved effective subscription/price snapshot, calculate deterministically, validate currency/rounding/tax policy, persist draft, authorize issue, assign number, freeze snapshot, record audit and required outbox intent in one transaction. Repeated scheduling/issue commands cannot duplicate documents.

### 6.2 Correction

Drafts may be edited under authorization. Issued documents are not overwritten. Corrections use linked credit, cancellation, or replacement records under an approved policy, preserve reason/actor/history, and reconcile balance.

### 6.3 Payment operation

Conceptual states: `CREATED`, `ACTION_REQUIRED`, `PENDING`, `SUCCEEDED`, `FAILED`, `CANCELLED`, `UNCERTAIN`, `REFUND_PENDING`, `REFUNDED`, and `RECONCILIATION_REQUIRED` as applicable. Transitions require authoritative adapter evidence. Timeout/ambiguous response becomes uncertain and is reconciled before another potentially duplicative charge.

### 6.4 Inbound event

Retain minimal raw evidence safely, verify source/authenticity and freshness, deduplicate using provider/event identity, resolve operation/account without trusting payload tenant fields, apply a valid transition transactionally, emit durable follow-up, acknowledge according to contract, and quarantine unknown/invalid/conflicting events.

## 7. Business Rules

| ID | Requirement | Verification |
|---|---|---|
| BILLM-001 | SaaS and ERP customer invoicing share no authoritative models, numbering, mutation services, or permissions | Boundary tests |
| BILLM-002 | Charges derive only from approved effective versioned configuration | Calculation tests |
| BILLM-003 | Decimal, currency, precision, tax-source, and rounding evidence are explicit | Financial tests |
| BILLM-004 | Unsupported proration, discount, tax, refund, or interval policy rejects rather than guesses | Negative tests |
| BILLM-005 | Repeated/concurrent processing cannot duplicate charge, document, payment, credit, or allocation | Idempotency/concurrency tests |
| BILLM-006 | Issued documents are immutable and corrections are linked | Database/service tests |
| BILLM-007 | Unverified, failed, or uncertain provider evidence cannot become successful payment or entitlement | Integration tests |
| BILLM-008 | Payment and balance changes reconcile to source operations and documents | Reconciliation tests |
| BILLM-009 | All financial and privileged operations are authorized, tenant-safe, and audited | Security tests |
| BILLM-010 | Provider outage/retry/replay cannot lose history or create duplicate external effect | Resilience tests |

## 8. Tenant Isolation, Security, and Sensitive Data

Every list/detail/document/download/task/reconciliation lookup is tenant/account scoped from trusted context. Provider callbacks use an integration identity and resolve internal ownership after validation. Runtime logs and audit exclude secrets, payment credentials, full payloads, and unnecessary personal data. Files follow ADR-019 with private storage, authorized download, malware/content controls where applicable, and bounded retention.

## 9. Entitlement and Subscription Interaction

Billing never calls an entitlement-table mutation. Verified billing outcomes are submitted to an approved subscription policy service using a durable operation. That service decides lifecycle and entitlement consequences. A billing success alone does not grant access; a billing failure does not delete the subscription or business data. Remediation access is defined by subscription policy and still requires permission.

## 10. Provider Contract, Events, and Tasks

The adapter exposes create/inspect/cancel/refund capabilities only as approved, maps provider states into internal states, defines timeout/retry/idempotency/authentication/version behavior, and provides sandbox/mocked contract tests. No provider is selected by this specification.

Material local changes and follow-up use ADR-010. Consumers handle duplicates/reordering; reconciliation compares internal operation, provider state, document balance, and subscription consequence. Retry is bounded with jitter and terminal/operator states.

## 11. UI, API, Reports, and Exports

Server-rendered screens cover own billing overview, documents, safe payment/remediation initiation, platform reconciliation, correction approval, and operation history. APIs/webhooks follow ADR-020, strict schemas, request size/rate limits, safe errors, and no internal model leakage. Billing reports define currency and metric semantics; cross-currency totals are prohibited without an approved conversion policy.

## 12. Regulatory and Financial Classification

This specification is a technical baseline, not tax/legal advice. SaaS tax treatment, invoice fields/numbering/retention, refund policy, and provider obligations require current authoritative UAE and specialist review before activation. Technical design keeps such rules versioned and traceable rather than hardcoded.

## 13. Operations, Recovery, and Migration

Monitor duplicate conflicts, issue failures, uncertain payments, webhook verification failures, inbox/outbox backlog, balance mismatch, reconciliation age, and correction/refund exceptions. Runbooks cover provider outage, secret rotation, replay, quarantine, manual reconciliation with dual control, and recovery after restore. Migrations preserve issued snapshots and support old/new payload versions during controlled overlap.

## 14. Acceptance Criteria, Tests, and Evidence

Acceptance criteria are `BILLM-001`–`BILLM-010` plus P02-AC-010–018. Required tests are P02-TST-055–118 in the [P02 matrix](../02-phases/P02_SUBSCRIPTION_ENGINE/P02_TRACEABILITY_AND_TEST_MATRIX.md). Evidence includes P02-EV-002, 007–013. Automated tests use mocks or an approved sandbox and must never perform real financial transactions.

## 15. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| PRD-DEC-002 | Payment provider | Product/Security/Finance | Live integration | Remain provider-neutral; perform due diligence and sandbox proof |
| CM-DEC-003–016 | Intervals, discounts, trial, grace, dunning, manual payment, refunds, tax | Product/Commercial/Finance/specialist | Affected flow | Version approved choices; disable unsupported flows |
| BILLM-DEC-001 | SaaS billing document legal classification/fields/retention | Qualified UAE tax/legal reviewer | Issuing customer documents | Validate current authoritative requirements; do not claim compliance |
| BILLM-DEC-002 | Numbering scope and gap policy | Finance/Operations | Document issue | Separate sequence from ERP customer invoices; document concurrency/recovery |

## 16. Implementation Prompt

Use [P02 orchestration](../04-agents/phase-prompts/P02_SUBSCRIPTION_ENGINE.md) and P02-T07–T09 in [P02 bounded tasks](../04-agents/phase-prompts/P02_BOUNDED_TASK_PROMPTS.md).
