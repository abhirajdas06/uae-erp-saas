# P09 — Banking and Advanced Finance Phase Specification

| Property | Value |
|---|---|
| Document ID | P09-SPEC-001 |
| Status | READY FOR REVIEW — BANKING MODE AND FINANCE POLICY APPROVAL REQUIRED |
| Regulatory evidence cut-off | 29 October 2026 |
| Implementation authorization | NOT GRANTED |

## 1. Objective and Authority

Deliver provider-neutral bank-account records, statement ingestion, matching and reconciliation while keeping Accounting authoritative and regulated connectivity separately gated. Implements `BANK-001`–`BANK-003`, ADR-009–015, ADR-017–020, [REG-BANK-001](../../00-product/UAE_BANKING_PAYMENT_INTEGRATION_SOURCE_REGISTER.md) and [ARCH-BANK-CONTRACT-001](../../01-architecture/BANKING_PROVIDER_CONTRACT.md).

The recommended initial increment is manual bank-statement import and reconciliation. It does not make the platform a bank, payment provider, Open Finance provider or settlement system and does not establish regulatory compliance.

## 2. Entry Gates

- P01 tenancy/IAM/audit, P02 entitlement, P05 Accounting and ADR file/secret/event controls are verified for enabled scope.
- Connectivity mode, regulatory role, account ownership/consent, statement formats, matching, reconciliation and posting policies are approved.
- Every direct provider/data/payment capability has current licensing/provider evidence, exact contract, sandbox/conformance and security review.
- Product Owner approves bounded P09 scope (`APPR-P09-001`).

## 3. Capability Modes

| Mode | Capability | Initial state |
|---|---|---|
| A | User-authorized upload of bank-issued statement file and reconciliation | Recommended initial scope |
| B | Consent-driven bank/account data retrieval through an approved Open Finance/provider contract | Disabled pending APPR-P09-002/003 |
| C | Payment file/instruction preparation for authorized export, without claiming bank submission or settlement | Disabled pending policy/provider approval |
| D | Direct payment initiation/service initiation and callbacks | Disabled pending licensing/legal/provider/security approval |

Modes are independently enabled, entitled, permissioned, monitored and reversible. Enabling one never implies another.

## 4. Included Scope

- Tenant/legal-entity bank-account references, masked display, currency, status and approved ledger mapping.
- Private statement upload, parser/version selection, preview, validation, immutable statement/line evidence and duplicate/overlap detection.
- Deterministic normalized transaction facts without destroying provider-native values.
- Rule-based candidate matching, authorized confirm/unmatch/reassign, exception queues and period/account reconciliation.
- Versioned Accounting/source contracts, cash-position reporting from explicitly labelled evidence and audit.
- Optional Modes B–D only after their exact gates; migrations, recovery, monitoring and incident handling.

## 5. Excluded Scope

- Deposit taking, fund custody, lending, FX dealing, remittance, card acquiring/issuing, cash pooling, hedging, treasury trading or any claim of bank/payment-provider status.
- Automated direct payment initiation or account-data access without approved legal/licensing, consent and provider contracts.
- Treating IBAN format validation as proof of account existence, ownership or authority.
- Treating local preparation, upload, transport success or provider receipt as acceptance, execution or settlement.
- Ledger mutation outside approved Accounting services.

## 6. Ownership and Data Boundaries

`banking` owns bank-account references, statement/import records, provider-native evidence, normalized lines, match candidates/decisions and reconciliation records. Accounting owns chart/ledger entries, periods and balances. Source modules own invoices, payments, expenses and payroll obligations. Banks/providers own account facts, provider statuses and settlement evidence.

Raw files, account identifiers, transaction narratives, consent artifacts and provider payloads are sensitive. Store the minimum necessary, encrypt/private-store as approved, mask display, restrict exports/support and exclude secrets/full payloads from logs.

## 7. Import, Matching and Reconciliation Controls

- Import uses an allowlisted exact parser/schema version, size/type/content checks, quarantine/scan, checksum and preview before commit.
- Statement/account/date/opening/closing facts and native line identifiers are retained. Normalization is additive and versioned.
- File checksum plus account/period/native identifiers and content fingerprints detect exact duplicates and overlaps; ambiguity requires review.
- Matching rules are ordered/versioned and generate explainable candidates with confidence, never silent authoritative matches.
- Confirm/unmatch/reassign is authorized, concurrent-safe and append-oriented. A locked/closed reconciliation is corrected by linked adjustment/reopen policy.
- Reconciliation proves statement opening + movements = closing where supplied, matches line totals, explains unmatched/differences and reconciles Accounting without duplicate postings.

## 8. Direct Connectivity and Payment Controls

Modes B–D implement ARCH-BANK-CONTRACT-001. Consent scope, purpose, account, duration, revocation and provider authorization are explicit. Credentials/certificates use ADR-017. Operations use stable idempotency keys, authenticated callbacks, timeout/unknown states, retries and active reconciliation. Provider-native evidence is retained separately from normalized internal state.

Payment preparation/initiation requires maker-checker, beneficiary verification policy, limits, approval/signatory evidence, payload hash and immutable instruction version. An uncertain outcome is never blindly retried. Only exact bank/provider evidence may establish execution or settlement.

## 9. Migration, Recovery and Operations

Migrations preserve account/statement/provider identity, native evidence, parser/rule versions, match history, consent, operation keys, posting references and audit. Restore reconciles file hashes, statements/lines, matches, unmatched/differences, provider operations, source records, ledger evidence, outbox and audit.

Monitor duplicate/overlap imports, parser drift, abnormal unmatched rates, stale reconciliation, consent expiry/revocation, credential/certificate expiry, callback failure/replay, uncertain operations, duplicate-payment attempts, provider degradation and sensitive-data access.

## 10. Acceptance Criteria

| ID | Criterion |
|---|---|
| P09-AC-001 | Approved mode, regulatory role, provider/account scope and disabled capabilities are explicit and current |
| P09-AC-002 | Bank-account records are tenant/entity/currency scoped, masked and separately authorized |
| P09-AC-003 | Statement files are private, validated, scanned, checksummed, parser-versioned and previewed |
| P09-AC-004 | Native statement/line evidence is immutable and normalization preserves provenance |
| P09-AC-005 | Exact duplicates, overlapping statements and duplicate lines are safely detected and reviewable |
| P09-AC-006 | Matching candidates are explainable; confirmation/unmatch/reassign is authorized and historically preserved |
| P09-AC-007 | Reconciliation is deterministic, concurrent-safe, exception-visible and source/ledger reconciled |
| P09-AC-008 | Repeated imports, matches, posting requests and provider callbacks cannot duplicate effects |
| P09-AC-009 | Cash/bank reports distinguish source, as-of time, currency, unmatched and uncertainty semantics |
| P09-AC-010 | Direct data access uses exact provider contract, valid consent, secure credentials and authenticated evidence |
| P09-AC-011 | Payment preparation/initiation uses maker-checker, limits, immutable versions and stable idempotency |
| P09-AC-012 | Provider/internal statuses distinguish preparation, receipt, acceptance, execution, rejection, uncertainty and settlement |
| P09-AC-013 | Timeouts, callback replay/reorder, provider outage and uncertain outcomes reconcile without unsafe retry |
| P09-AC-014 | Permissions, entitlement, tenant isolation, RLS, tasks, caches, reports and support fail closed |
| P09-AC-015 | Sensitive bank/transaction/consent/credential data is minimized, private, redacted and audited |
| P09-AC-016 | Migration and restore reconcile accounts, files, lines, matches, ledger/source/provider/event/audit evidence |
| P09-AC-017 | Performance, monitoring, incident/credential/provider runbooks and accessibility meet approved targets |
| P09-AC-018 | Finance, Legal/Compliance, Security, Database, Operations and independent findings are dispositioned |
| P09-AC-019 | Product Owner records bounded exit and each production provider/mode activation separately |

## 11. Evidence and Approval Gates

Planned evidence `P09-EV-001`–`P09-EV-015` is defined by P09-TRACE-001. Required approvals are `APPR-P09-001` scope, `APPR-P09-002` mode/regulatory role, `APPR-P09-003` provider/consent contract, `APPR-P09-004` reconciliation/posting policy, `APPR-P09-005` payment initiation and `APPR-P09-006` exit/activation. See `DECISIONS_PENDING.md` for actionable recording instructions.
