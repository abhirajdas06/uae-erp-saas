# Banking Provider and Payment Integration Contract Boundary

| Property | Value |
|---|---|
| Document ID | ARCH-BANK-CONTRACT-001 |
| Status | READY FOR REVIEW — PROVIDER NEUTRAL |
| Regulatory baseline | REG-BANK-001, cut-off 29 October 2026 |

## 1. Boundary and Modes

`banking` owns bank-account references, imported statement snapshots/transactions, matching and reconciliation. `accounting` owns ledger entries; source domains own invoices/payments/expenses/payroll; external banks/providers own account truth, payment execution and settlement evidence.

Supported modes are separately approved: (A) manual statement file import, recommended initial mode; (B) provider data feed/Open Finance data sharing; (C) payment-file preparation for authorized upload; (D) direct payment initiation. Approval of one mode does not authorize another.

## 2. Provider Adapter Manifest

Each adapter declares provider legal entity/license evidence, mode/capabilities, banks/accounts/customer types, environment, contract/API/file/webhook versions, auth/certificates, consent model, rate/cutoff/limits, idempotency, statuses, retention/location, support/SLA and limitations. Unsupported capability fails closed.

## 3. Versioned Contracts

| Contract | Semantics |
|---|---|
| `ImportBankStatement.v1` | Tenant/entity/account, format/version, file hash, statement identity/period/opening/closing currency balances, immutable lines and import idempotency |
| `BankDataSync.v1` | Approved consent/account/provider, cursor/window, operation identity and safe incremental/replay semantics |
| `PreparePaymentInstruction.v1` | Approved source/payee/account/currency/amount/value date/purpose, beneficiary evidence, signatory policy and stable idempotency; creates no settlement |
| `BankOperationEvidence.v1` | Provider-native reference/status/time/evidence, controlled internal state, mapping version and reconciliation need |
| `ReconciliationChanged.v1` | Statement line, ERP source/ledger references, allocation, reason, actor/version and controlled reversal history |

Decimals are strings; identifiers opaque; timestamps include timezone; schemas follow ADR-020.

## 4. File/Data Import

Files are private, quarantined/type-size checked, parser/version selected explicitly, hashed and retained/disposed by policy. Parser validates account/currency/period/balances/lines and never trusts tenant/account/status from the file. Duplicate file and overlapping/repeated transaction detection uses provider IDs where reliable plus documented composite/fingerprint and human review. Imported lines are immutable external evidence; normalization is separately versioned.

## 5. Data Sharing, Consent and Security

Direct data access is enabled only after legal/licensing/provider approval. Store consent/authorization reference, purpose, accounts/scopes, grant/expiry/revocation and provider evidence without exposing tokens. Use secure standards, least-privilege scopes, mTLS/certificates/keys as contracted, rotation and separate environments. Revocation stops new access; historical authorized evidence follows approved retention.

## 6. Payment Operations

Payment preparation and initiation are distinct. Maker-checker/signatory/limit/beneficiary controls are revalidated immediately before external action. A durable operation/outbox records intent; network action occurs after commit. Stable idempotency is used where supported. Timeout after possible send is `UNCERTAIN`; query/reconcile before retry. States such as prepared, submitted, accepted, processing, rejected, cancelled, returned and settled are enabled only when exact provider evidence defines them. Local success never fabricates settlement.

## 7. Callbacks, Reconciliation and Errors

Callbacks verify provider identity, body integrity, replay/time controls and trusted provider-account routing. Duplicate/reordered evidence produces no duplicate financial effect. Errors normalize validation, authorization/consent, authentication, rate/cutoff, insufficient/beneficiary, transient, permanent, conflict and uncertain while preserving safe native evidence.

Reconciliation compares immutable statement/provider evidence with ERP payment/source and Accounting ledger records. Suggestions are non-authoritative; confirm/unmatch/reassign/correct operations preserve history, reason and approval. Reconciliation never silently creates ledger entries unless an explicitly approved posting service is invoked idempotently.

## 8. Acceptance and Onboarding Evidence

Required evidence: legal/licensing classification; current CBUAE/provider evidence; contract and data-processing terms; bank coverage; exact schemas/statuses; security/consent/certificate review; sandbox/conformance; idempotency/uncertainty/callback tests; retention/residency/exit; support/SLA/runbooks; production activation/rollback.

Contract tests cover valid/invalid/duplicate/overlap files, incremental sync/replay, consent expiry/revocation, credential rotation, payment success/rejection/timeout/crash/duplicate, callback authentication/reorder and restore/cutover. Production capability remains disabled until its exact mode is approved.
