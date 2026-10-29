# BANKING — Banking and Reconciliation Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-BANKING-001 |
| Status | APPROVED CONTRACT BASELINE; EXPANDED IMPLEMENTATION DETAIL PROPOSED — CONNECTIVITY/RECONCILIATION POLICY REQUIRED |
| Owning phase / app | P09 / `banking` |
| Domain owner | Treasury and Banking |
| Commercial module | Yes |
| Tenant-owned data | Yes |
| Readiness | Expanded under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`; sections 3–14 are PROPOSED and unapproved |

## 1. Purpose and Boundary

Own provider-neutral bank-account references, statement and provider evidence, normalized lines, candidate matches, match decisions and reconciliations under `BANK-001`–`BANK-003` and [P09-SPEC-001](../02-phases/P09_BANKING_FINANCE/P09_PHASE_SPECIFICATION.md). Accounting owns ledger truth; source modules own obligations and receipts; banks and providers own external account and settlement truth.

Governing sources: `BANK-001`–`BANK-003`, P09-SPEC-001, [ARCH-BANK-CONTRACT-001](../01-architecture/BANKING_PROVIDER_CONTRACT.md), [UAE banking source register](../00-product/UAE_BANKING_PAYMENT_INTEGRATION_SOURCE_REGISTER.md), ADR-003–ADR-006, ADR-010, ADR-011, ADR-013–ADR-015, ADR-017–ADR-020, `ARCH-SEQ-001`, `ARCH-NOTIFY-001`, `ARCH-MIGRATION-001`, `QUAL-PRIV-001`, `QUAL-THREAT-001`, `PROD-REPORTS-001`.

Default scope is manual import and reconciliation. Direct account-data access, payment preparation and payment initiation are independent gated modes under `ARCH-BANK-CONTRACT-001`.

## 2. Actors and Authorization

| Actor | Permitted scope |
|---|---|
| Bank-account administrator | Maintain account references and ledger mapping |
| Import preparer | Upload and commit statement evidence |
| Matcher | Review candidates and confirm or unmatch |
| Reconciliation reviewer / approver | Approve a reconciliation and authorize reopen |
| Payment preparer | Prepare an instruction where a payment mode is enabled |
| Payment approver | Authorize release of a prepared instruction |
| Finance auditor | Read-only evidence review |
| Integration operator | Operate connections, consents and replay within bounds |
| Purpose-bound support | Time-bounded, audited privileged access under ADR-018 |

Concrete permission codenames, satisfying `RDY-004`:

`banking.view_bank_account`, `banking.add_bank_account`, `banking.change_bank_account`, `banking.view_account_identifier_full`, `banking.import_statement`, `banking.commit_statement`, `banking.view_statement_line`, `banking.configure_match_rule`, `banking.confirm_match`, `banking.unmatch`, `banking.reconcile`, `banking.approve_reconciliation`, `banking.reopen_reconciliation`, `banking.prepare_posting`, `banking.configure_provider_connection`, `banking.manage_consent`, `banking.prepare_payment`, `banking.approve_payment`, `banking.replay_operation`, `banking.export_banking_data`, `banking.view_all_bank_data`.

Account and credential setup, import, match, reconcile, reopen, post, payment preparation and approval, export and support access are separate, with maker-checker wherever a financial or external effect occurs. A payment preparer can never approve the same instruction.

## 3. Domain Ownership

| Record / capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Bank account reference and ledger mapping | `banking` | Direct tenant and legal entity | Account service |
| Statement import, statement, line, native evidence | `banking` | Account tenant | Import service, immutable after commit |
| Normalization, match rule, candidate, decision | `banking` | Account tenant | Matching services |
| Reconciliation and finding | `banking` | Account tenant | Reconciliation service |
| Provider connection, consent, operation, evidence | `banking` | Direct tenant | Integration services behind `MOD-INTEGRATIONS-001` |
| Journal entry, ledger balance, period | `accounting` | Same-tenant reference | Accounting contract |
| Customer payment evidence | `invoicing` | Same-tenant reference | Invoicing contract |
| Supplier payment obligation | `procurement` | Same-tenant reference | Procurement contract |
| Payroll payment artifact | `payroll` | Same-tenant reference | Payroll contract |
| Provider credential material | Secrets backend | Reference only | ADR-017 secret references |

## 4. Data Model Requirements

Conceptual entities: `BankAccount`, `BankStatementImport`, `BankStatement`, `BankStatementLine`, `BankNormalization`, `BankMatchRule`, `BankMatchCandidate`, `BankMatchDecision`, `BankReconciliation`, `BankProviderConnection`, `BankConsent`, `BankOperation`, `BankOperationEvidence`, `BankReconciliationFinding`.

Field-level requirements satisfying `RDY-001`:

| Entity | Required attributes |
|---|---|
| `BankAccount` | UUID id; tenant FK; legal-entity FK; account name; masked display identifier; full identifier stored with restricted read; IBAN where applicable with syntactic validation only; currency; ledger account mapping; `status`; created and updated timestamps and actors |
| `BankStatementImport` | Account FK; uploaded file reference; SHA-256 checksum; parser and schema version; `status`; uploaded-by; committed-by; quarantine and validation results |
| `BankStatement` | Import FK; account FK; statement period start and end; `NUMERIC` opening and closing balance; native currency; provider reference; immutable after commit |
| `BankStatementLine` | Statement FK; line sequence; value and booking dates; `NUMERIC` amount with sign convention; native narrative and identifiers preserved verbatim; native payload reference; immutable after commit |
| `BankNormalization` | Line FK; parser and rule version; normalized counterparty, reference and category; confidence; provenance; regenerable without altering native data |
| `BankMatchRule` | Tenant FK; version; effective dates; criteria; confidence weighting; active flag |
| `BankMatchCandidate` | Line FK; target reference and type; rule version; confidence; explanation; non-authoritative |
| `BankMatchDecision` | Line FK; target reference; decision; actor; decided-at; reason; append-only; supersession reference on unmatch |
| `BankReconciliation` | Account FK; period; `status`; `NUMERIC` statement closing balance, ledger balance, matched, unmatched and difference; approver; approved-at |
| `BankProviderConnection` | Tenant FK; provider; contract version; environment; credential reference; `status`; health |
| `BankConsent` | Connection FK; scope; granted-at; expires-at; evidence reference; `status` |
| `BankOperation` | Tenant FK; operation type; immutable payload hash; idempotency key; `status` including an explicit uncertain state; attempt history; approver references |
| `BankOperationEvidence` | Operation FK; native request and response reference; received-at; checksum; provider status verbatim |
| `BankReconciliationFinding` | Tenant FK; scope; detected-at; finding type; amounts; resolution state |

Constraints: UUID primary keys; mandatory tenant and legal-entity ownership; `NUMERIC`/`Decimal` for every monetary value per ADR-013; immutability enforcement on committed statements, lines and native evidence; unique import checksum per account and unique native line key to prevent duplicate effects while leaving overlap reviewable; unique idempotency key per operation; same-tenant foreign keys throughout; append-only decision, evidence and audit history; no hard deletion of committed evidence, decisions, reconciliations or operations through any ordinary path.

Native values and identifiers remain immutable. Normalized facts, parser and rule version, provenance and confidence are stored separately from native data. Credentials are references to an approved secrets backend and never ordinary model fields.

## 5. Workflows and States

| Record | States |
|---|---|
| `BankStatementImport` | `UPLOADED`, `QUARANTINED`, `VALIDATED`, `PARSED`, `PREVIEWED`, `COMMITTED`, `REJECTED` |
| `BankReconciliation` | `OPEN`, `IN_PROGRESS`, `BALANCED`, `APPROVED`, `REOPENED`, `EXCEPTION` |
| `BankOperation` | `DRAFT`, `PENDING_APPROVAL`, `APPROVED`, `SENT`, `ACKNOWLEDGED`, `EXECUTED`, `REJECTED`, `UNCERTAIN`, `SETTLED`, `FAILED` |
| `BankConsent` | `REQUESTED`, `ACTIVE`, `EXPIRING`, `EXPIRED`, `REVOKED` |

Mode A, the default: upload, quarantine and validate and parse, preview, commit immutable evidence, generate candidates, confirm or unmatch, reconcile, raise an approved Accounting request where applicable, then close or record an exception.

Mode B: establish an exact connection and consent, sync incrementally, record native evidence, normalize and deduplicate, reconcile. Modes C and D: prepare an immutable instruction, obtain maker-checker approval, export or initiate exactly once, record native responses and callbacks, then reconcile an uncertain or final outcome.

Modes B, C and D remain disabled until `DEC-BANK-001`–`DEC-BANK-003` and the applicable `APPR-P09` approvals are recorded; the module fails closed rather than degrading to an unapproved mode. An `UNCERTAIN` operation is never reported as executed or settled, and is resolved only by provider evidence or an authorized reconciliation decision.

## 6. Business Rules

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
| BANKM-014 | An unapproved connectivity or payment mode is unreachable rather than partially enabled; negative tests |
| BANKM-015 | A change to a stored account identifier requires maker-checker and is audited before any payment use; change-control tests |
| BANKM-016 | A closed accounting period rejects a new reconciliation posting; period tests |

## 7. Tenant Isolation, Security and Sensitive Data

Every request, service, task, report, export, cache, file, callback and administrative path derives trusted tenant context and validates same-tenant relationships, with row-level security as defence in depth. Inbound provider callbacks authenticate, verify signatures, enforce replay protection and route to the correct tenant fail-closed, per `ARCH-API-001` section 19.4.

Applicable threats from `QUAL-THREAT-001`, satisfying `RDY-010`: `THR-010`, `THR-011`, `THR-014`, `THR-035`, `THR-040` forged provider webhook, `THR-041` replayed callback duplicating a financial effect, `THR-042` compromised provider credential, `THR-043` server-side request forgery through a provider URL, `THR-044` malicious uploaded statement file, `THR-046` provider outage cascading, `THR-047` loss of provider acknowledgement evidence, `ABU-03` payment diversion, `ABU-05` self-approval, `ABU-09` duplicate payment through retry.

Data classification and retention, satisfying `RDY-009`: reconciliation summaries are `C2`; counterparty narratives may contain `C3`; full account identifiers, IBANs, payment instructions and provider payloads are `C4`. Retention classes are `RET-01` for records forming part of the accounting record, `RET-07` for bank details and payment instructions, and `RET-12` for artifacts, under `QUAL-PRIV-001`. Periods remain unresolved pending `DEC-PRIV-005`; none is asserted here.

Logs, metrics, traces, notifications and support exports exclude full identifiers, transaction narratives beyond operational need, consent material and all secrets. Account identifiers are masked by default and unmasked only for `banking.view_account_identifier_full` with audit. IBAN validation is syntactic only and never proves account ownership or authority.

## 8. Entitlements and Degraded Access

`BANKING` entitlement and the relevant user permission are both required on every path. Suspension or expiry denies import, matching, reconciliation approval, posting and any payment preparation by default; approved read and export for remediation may be explicitly allowed and audited. Deactivation never deletes committed evidence, decisions or operation history, and never prevents required retention or recovery.

## 9. Integrations and Events

- Accounting: publish versioned, balanced reconciliation facts; Accounting owns journal entries and periods, and the control reconciliation behind `RPT-701`.
- Invoicing: match statement lines to customer payment evidence through the explicit contract.
- Procurement: match outgoing lines to supplier obligations.
- Payroll: reconcile the approved payment or wage-protection artifact to statement evidence.
- Provider: exchange only through the versioned contract behind `MOD-INTEGRATIONS-001`; provider-native evidence is retained separately from internal status.
- Reporting: expose banking facts for `RPT-701`–`RPT-704`.

Durable intent and the transactional outbox per ADR-010 protect commits, postings and payment operations. Every outbound operation carries an immutable payload hash and a stable idempotency key. Reconciliation detects import-to-statement, line-to-match, match-to-source, reconciliation-to-ledger and operation-to-evidence mismatches.

## 10. UI, API, Reports, Imports and Exports

Django and HTMX surfaces cover account configuration with masked identifiers, statement upload with preview and validation findings, line browsing with native and normalized views, candidate review with confidence and explanation, match confirmation, reconciliation workspace with difference analysis, approval and reopen confirmation, provider connection and consent status where enabled, payment preparation and approval where enabled, operation status including uncertainty, and reconciliation findings. Surfaces use the data table, monetary cell, file upload, form error summary, destructive confirmation dialog, asynchronous operation status and bulk action bar components in `ARCH-UI-001`. Payment release and reconciliation reopen require explicit confirmation naming the record and effect per `UIX-036`.

Reports registered in `PROD-REPORTS-001`: `RPT-701` bank reconciliation statement, `RPT-702` cash and bank position, `RPT-703` payment run and instruction status, `RPT-704` unreconciled and ageing exceptions. Reports state account, currency, source, as-of timestamp, opening and closing basis, matched, unmatched and difference amounts, and any provider uncertainty.

Imports follow `ARCH-MIGRATION-001`: statement import is the module's primary ingest path and uses the same staged validation, quarantine, preview and idempotent commit discipline. Opening bank balances enter through domain 6 as reconciled opening balances. Exports are private, authorized, formula-safe, checksummed and audited as a disclosure.

Document types registered in `ARCH-SEQ-001`, satisfying `RDY-007`: bank transaction batch reference, payment instruction number, payment file reference and reconciliation statement reference, each allocated at its approved point and scoped to tenant, entity and account. Gapless requirements follow `DEC-SEQ-002`, with conservative defaults until confirmed.

Notifications registered in `ARCH-NOTIFY-001`, satisfying `RDY-008`: statement import completed or rejected, reconciliation difference detected, reconciliation awaiting approval, payment awaiting approval, payment rejected or uncertain, consent expiring and expired, connection unhealthy, and account identifier changed. Financial and security categories are mandatory and never digested.

## 11. Regulatory and Financial Readiness

This module establishes no banking, payment-services, open-banking, anti-money-laundering or licensing position, and asserts no provider availability, pricing, accreditation or capability. Connectivity and payment modes are regulated activities whose applicability is unresolved and governed by `DEC-BANK-001`–`DEC-BANK-003` and `APPR-P09-001`–`APPR-P09-006`, with dated sources in the banking source register.

A successful API call or file acceptance is never evidence of regulatory compliance or of settlement. No regulatory fact or retention period is asserted here, per `RDY-012`.

## 12. Operations, Migration and Recovery

Monitor parser and provider drift, duplicate and overlapping imports, match anomalies, stale reconciliations, consent and credential expiry, callback failures, uncertain operations, sensitive access and export volume. Runbooks cover a rejected or malformed statement file, a duplicate import, an erroneous confirmed match requiring authorized unmatch, a stale reconciliation, an expired consent, a failed callback, an uncertain payment requiring provider confirmation, a suspected payment diversion, and restore reconciliation.

Migration preserves native evidence, checksums, decisions, reconciliations and operation history. Restore verifies import checksums, statement and line counts, opening and closing balances per account and currency, match decision chains, reconciliation differences against the ledger, operation idempotency keys, outbox age and audit completeness.

## 13. Acceptance Criteria, Tests and Evidence

Acceptance criteria are `BANKM-001`–`BANKM-016` and the applicable criteria in `P09-AC-001`–`P09-AC-019`. Required tests are the banking scenarios within `P09-TST-001`–`P09-TST-176`, including `P09-TST-001`–`P09-TST-010` for mode and policy readiness. Evidence records are `P09-EV-001`–`P09-EV-015` in the [P09 matrix](../02-phases/P09_BANKING_FINANCE/P09_TRACEABILITY_AND_TEST_MATRIX.md).

All scenarios are `NOT_RUN`. Tests use synthetic statements and the documented invalid IBAN patterns in `QUAL-TESTDATA-001`; no test contacts a real bank or provider endpoint, and no test initiates a real payment.

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| DEC-BANK-001 | Which connectivity and payment modes are in scope, and in what order | Product / Finance / Legal | Any connectivity or payment implementation | Deliver Mode A manual import and reconciliation only; keep B, C and D disabled |
| DEC-BANK-002 | Provider selection, contract version, consent model and environment | Product / DevOps / Legal | Mode B, C or D activation | Do not select a provider before the regulated scope is confirmed |
| DEC-BANK-003 | Reconciliation policy, matching confidence thresholds, difference tolerance and reopen authority | Finance domain owner | Reconciliation implementation | Require authorized confirmation for every match; set tolerance to zero by default |
| DEC-SEQ-002 | Statutory expectations for payment and reconciliation references | Tax specialist | Numbering implementation | Default to gapless and conservative until confirmed |
| DEC-PRIV-005 | Retention periods for bank details, instructions and provider payloads | Tax and finance specialists | Automated disposal | Confirm with dated sources; retain under obligation until then |
| DEC-GOV-007 | Phase-entry specification gate covering this expansion | Product Owner / Architecture | P09 implementation authorization | Approve the gate and this expanded specification together |

## 15. Implementation Prompt

Use the [P09 orchestration prompt](../04-agents/phase-prompts/P09_BANKING_FINANCE.md) and the banking tasks in the [P09 bounded task prompts](../04-agents/phase-prompts/P09_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest; no implementation is authorized by this document.
