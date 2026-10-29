# BANKING — Banking and Reconciliation Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-BANKING-001 |
| Status | READY FOR REVIEW — CONNECTIVITY/RECONCILIATION POLICY REQUIRED |
| Owning phase / app | P09 / `banking` |

## 1. Purpose and Boundary

Own provider-neutral bank-account references, statement/provider evidence, normalized lines, candidate matches, match decisions and reconciliations under `BANK-001`–`BANK-003` and P09-SPEC-001. Accounting owns ledger truth; source modules own obligations/receipts; banks/providers own external account and settlement truth.

Default scope is manual import/reconciliation. Direct account-data access, payment preparation and payment initiation are independent gated modes under ARCH-BANK-CONTRACT-001.

## 2. Actors and Permissions

Bank-account administrator, import preparer, matcher, reconciliation reviewer/approver, payment preparer/approver when enabled, finance auditor, integration operator and purpose-bound support. Account/credential setup, import, match, reconcile, reopen, post, payment prepare/approve, export and support are separate with maker-checker where financial or external effects occur.

## 3. Conceptual Model

`BankAccount`, `BankStatementImport`, `BankStatement`, `BankStatementLine`, `BankNormalization`, `BankMatchRule`, `BankMatchCandidate`, `BankMatchDecision`, `BankReconciliation`, `BankProviderConnection`, `BankConsent`, `BankOperation`, `BankOperationEvidence` and `BankReconciliationFinding`.

Native values and identifiers remain immutable. Normalized facts, parser/rule version, provenance and confidence are separate. Secrets are references to an approved secrets backend, never ordinary model fields.

## 4. Workflows

Mode A: upload → quarantine/validate/parse → preview → commit immutable evidence → generate candidates → confirm/unmatch → reconcile → approved Accounting request where applicable → close/exception.

Mode B: establish exact connection/consent → incremental sync → record native evidence → normalize/deduplicate → reconcile. Modes C/D: prepare immutable instruction → maker/checker approval → export/initiate once → record native responses/callbacks → reconcile uncertain/final outcome.

## 5. Rules and Verification

| ID | Rule / verification |
|---|---|
| BANKM-001 | Account/entity/currency/ledger mapping and identifiers are tenant-safe, masked and authorized |
| BANKM-002 | File/API evidence uses exact parser/schema/provider version, provenance and immutable native data |
| BANKM-003 | Checksum/native/content keys prevent exact duplicate effects while overlap remains reviewable |
| BANKM-004 | Matching is explainable, confidence-labelled and non-authoritative until authorized confirmation |
| BANKM-005 | Match/unmatch/reassign/reconcile/reopen is append-oriented, concurrent-safe and audited |
| BANKM-006 | Statement totals, matched/unmatched/difference and source-ledger reconciliation are deterministic |
| BANKM-007 | Accounting requests are versioned/idempotent; Banking never writes ledger lines directly |
| BANKM-008 | Consent/credential/certificate/callback controls meet exact approved provider contract |
| BANKM-009 | Payment operations use immutable payload hash, maker-checker, stable idempotency and uncertainty reconciliation |
| BANKM-010 | Local/provider statuses cannot overstate acceptance, execution or settlement |
| BANKM-011 | Permissions, entitlement, tenant isolation, RLS, tasks, caches, files/reports/exports protect every path |
| BANKM-012 | Logs/audit/evidence minimize and redact account, transaction, consent and secret data |
| BANKM-013 | Migration/restore reconciles files, lines, matches, providers, ledger/source, events and audit |

## 6. Reports and Operations

Reports state account, currency, source, as-of timestamp, opening/closing basis, matched/unmatched/difference and provider uncertainty. Monitor parser/provider drift, duplicate/overlap, match anomalies, stale reconciliations, consent/credential expiry, callback failures, uncertain operations and sensitive access.

`DEC-BANK-001`–`003` and `APPR-P09-001`–`006` gate mode, provider, reconciliation and payment behavior. IBAN format validation is syntactic only and never proves account ownership or authority.
