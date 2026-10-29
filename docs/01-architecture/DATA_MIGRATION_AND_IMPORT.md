# Tenant Data Migration, Import and Export

| Property | Value |
|---|---|
| Document ID | ARCH-MIGRATION-001 |
| Status | PROPOSED SPECIFICATION — OPENING BALANCE POLICY AND FORMAT APPROVAL REQUIRED |
| Owner | Product Architect / Finance domain owner |
| Governing decisions | ADR-011, ADR-013, ADR-004, ADR-019 |
| Related documents | `DATABASE_DESIGN.md`, `DOCUMENT_NUMBERING_AND_SEQUENCES.md`, `../03-modules/ACCOUNTING.md`, `../05-quality/DATA_PROTECTION_AND_RETENTION.md` |

## 1. Purpose and Boundary

`../00-product/MASTER_PRODUCT_SPECIFICATION.md` section 17 requires the data lifecycle to address tenant onboarding, import and migration, customer data export and restoration, but no document owns how a new tenant brings existing master data and opening balances into the platform without compromising financial integrity. A commercial ERP cannot onboard a real business without this capability. This document owns that definition.

This document owns the import and migration framework: supported data domains, file and record contracts, validation stages, staging and commit semantics, opening-balance treatment, idempotency and rollback, tenant data export, and the related tests. It does not own database schema migrations, which remain with `DATABASE_DESIGN.md` and the migration-safety rules in `AGENTS.md` section 13; report-oriented export, which remains with `../03-modules/REPORTING.md`; or retention and deletion policy, which remains with `../05-quality/DATA_PROTECTION_AND_RETENTION.md`.

Import is a privileged, authorized, auditable business operation. It is never a bypass of validation, authorization, tenant isolation, entitlement or financial-integrity rules.

## 2. Framework Principles

| ID | Requirement |
|---|---|
| MIG-001 | Every import executes through the same application services and validation as interactive data entry; direct database insertion into business tables is prohibited |
| MIG-002 | Import is tenant-scoped; a file is bound to exactly one target tenant resolved server-side, never from a value inside the file |
| MIG-003 | Import requires an explicit permission distinct from ordinary create permission, and a financial import additionally requires maker-checker approval |
| MIG-004 | Import respects module entitlement: data for an unsubscribed module is rejected, not staged for later activation |
| MIG-005 | An import job is a first-class record with an identifier, actor, tenant, domain, file reference, checksum, stage outcomes, counts and terminal state |
| MIG-006 | Import never creates or modifies a posted financial record outside the approved opening-balance and correction paths defined in ADR-011 |
| MIG-007 | Every imported record is marked with its originating import job for traceability, reconciliation and support investigation |

## 3. Supported Domains and Sequence

Domains are imported in dependency order. A domain cannot be imported before its prerequisites are present and validated.

| Order | Domain | Prerequisites |
|---|---|---|
| 1 | Chart of accounts, tax codes, currencies, fiscal calendar | Tenant provisioned, accounting module entitled |
| 2 | Customers, suppliers, contacts, addresses, tax registration details | Master configuration |
| 3 | Items, services, units of measure, price lists, warehouses | Master configuration |
| 4 | Employees, organizational structure, salary structure components | HR module entitled |
| 5 | Projects, cost centres, asset register | Owning modules entitled |
| 6 | Opening balances: trial balance, accounts receivable and payable ageing, inventory quantities and valuation, fixed-asset cost and accumulated depreciation, loan and lease balances | All of the above, plus an approved cut-over date |
| 7 | Historical open transactions required for operational continuity | Opening balances committed and reconciled |
| 8 | Historical closed transactions, where in scope | Explicit approval; never required for go-live |

| ID | Requirement |
|---|---|
| MIG-010 | Each domain declares its required and optional fields, data types, precision, validation rules, uniqueness keys and reference resolution strategy in the owning module specification |
| MIG-011 | Reference resolution matches on an explicit business key; silent fuzzy matching or creation of a missing referenced master record is prohibited |
| MIG-012 | A domain with an unapproved contract cannot be imported, even manually |

## 4. File and Record Contracts

| ID | Requirement |
|---|---|
| MIG-020 | Supported file formats are declared explicitly with their encoding, delimiter, decimal convention, date convention, header requirement and maximum size |
| MIG-021 | Files are UTF-8 and must round-trip Arabic text without loss, per `LOCALIZATION_AND_BILINGUAL_UI.md` L10N-050 |
| MIG-022 | Monetary and quantity values are parsed as exact decimals under ADR-013; floating-point parsing of monetary values is prohibited |
| MIG-023 | A localized display string is never accepted as a numeric value; ambiguous numeric input is rejected rather than inferred |
| MIG-024 | Dates are parsed from a declared unambiguous format; a two-digit year or an ambiguous day-month order is rejected |
| MIG-025 | Uploaded files are validated for type, size and content safety under `../05-quality/SECURITY_REQUIREMENTS.md` SEC-008, stored privately under ADR-019, and are never executed or interpreted |
| MIG-026 | A formula, macro or active content in a spreadsheet input is neutralized or rejected; cell values are read as data only |
| MIG-027 | Each uploaded file is checksummed, and the checksum is recorded on the import job |
| MIG-028 | A versioned template is published for every supported domain so a tenant can prepare a conforming file |

## 5. Validation Stages

An import passes through ordered stages. A later stage never runs on input that failed an earlier one.

| Stage | Purpose | Failure behavior |
|---|---|---|
| 1 — Intake | Format, encoding, size, checksum, template version, declared domain | Reject the file; no staging |
| 2 — Structural | Required columns, data types, precision, allowed characters | Reject with per-row, per-field findings |
| 3 — Referential | Resolution of accounts, parties, items, employees, currencies, tax codes | Reject unresolved rows with the unresolved key named |
| 4 — Business rule | Domain validation identical to interactive entry, including entitlement and period rules | Reject with the same error semantics as interactive entry |
| 5 — Integrity | Cross-row and whole-file consistency, including balance, ageing and valuation reconciliation | Reject the entire file where the domain requires whole-file consistency |
| 6 — Preview | Authorized reviewer sees counts, totals, reconciliation result and findings before commit | No business effect until approval |
| 7 — Commit | Transactional application of the approved staged set | Atomic per the domain commit unit |

| ID | Requirement |
|---|---|
| MIG-030 | Validation findings identify row, field, submitted value and reason, and exclude sensitive values from logs |
| MIG-031 | A finding report is downloadable by the authorized importer and retained with the import job |
| MIG-032 | Partial-success behavior is declared per domain: all-or-nothing, or row-level with an explicit rejected-row report; a financial opening-balance import is always all-or-nothing |
| MIG-033 | A whole-file integrity failure in an opening-balance import blocks commit; forcing an unbalanced import is prohibited |

## 6. Staging and Commit Semantics

| ID | Requirement |
|---|---|
| MIG-040 | Staged data is held in dedicated staging structures, is tenant-scoped, is never visible as live business data, and is excluded from reports, ledgers and exports |
| MIG-041 | Commit occurs within database transactions sized to the declared commit unit, so a failed commit leaves no partially applied business state |
| MIG-042 | A large import is chunked with per-chunk atomicity and a resumable, idempotent job record; a resumed job never reapplies a committed chunk |
| MIG-043 | Document numbers allocated during import use the standard allocation service under `DOCUMENT_NUMBERING_AND_SEQUENCES.md` SEQ-015 |
| MIG-044 | Commit emits the same domain events and audit entries as interactive creation, with the import job as the recorded cause |
| MIG-045 | Re-uploading an identical file is detected by checksum and business key and does not duplicate records |
| MIG-046 | Staged data has a bounded lifetime and is purged on a declared schedule after terminal job state |
| MIG-047 | Concurrent imports affecting the same domain and tenant are serialized or rejected; interleaved commits to one domain are prohibited |

## 7. Opening Balances and Cut-Over

| ID | Requirement |
|---|---|
| MIG-050 | An opening balance is recorded through an explicit, identifiable opening-balance mechanism, dated at the approved cut-over date, and is never disguised as ordinary trading activity |
| MIG-051 | The cut-over date, prior-system reference and responsible approver are recorded before any opening-balance commit |
| MIG-052 | A trial-balance import must balance exactly in the tenant base currency before commit |
| MIG-053 | Subsidiary ledger imports must reconcile to their control account: receivables and payables ageing to their control totals, inventory quantity and valuation to the inventory control account, and fixed-asset cost and accumulated depreciation to their control accounts |
| MIG-054 | A reconciliation difference is reported with its amount and composition and blocks commit; it is never written to a suspense account automatically |
| MIG-055 | Opening tax balances and any prior-period VAT position are imported only with tax-specialist approval and never generate a filing obligation claim |
| MIG-056 | Imported historical documents are flagged as migrated and are excluded from statutory e-invoicing submission unless an approved decision and a verified regulatory basis require otherwise |
| MIG-057 | Foreign-currency opening balances record their original currency, rate basis and base-currency equivalent under ADR-013 |
| MIG-058 | Post-cut-over correction of an opening balance follows the correction and reversal rules in ADR-011, not re-import over existing data |

## 8. Rollback and Recovery

| ID | Requirement |
|---|---|
| MIG-060 | Every import declares its reversal path before execution; an import without a defined reversal path is not authorized |
| MIG-061 | Reversal of a non-financial master import deactivates rather than hard-deletes where a reference exists |
| MIG-062 | Reversal of a posted financial import uses authorized reversal entries, never deletion of posted records |
| MIG-063 | A reversal is itself an authorized, audited operation with a recorded reason and approver |
| MIG-064 | A reversal that would leave dependent data orphaned is blocked with the dependency named |
| MIG-065 | Database-level restore to undo an import requires the authorization in `../06-deployment/BACKUP_AND_RECOVERY.md` and is never performed by an agent or developer on tenant data without it |

## 9. Tenant Data Export

| ID | Requirement |
|---|---|
| MIG-070 | A tenant can obtain a complete, machine-readable export of its own business data, satisfying the customer data export requirement in `../00-product/MASTER_PRODUCT_SPECIFICATION.md` section 17 |
| MIG-071 | Export is tenant-scoped and authorized; it never includes another tenant's data, platform secrets or internal operational metadata |
| MIG-072 | Export declares its schema, version, encoding, completeness scope and generation timestamp |
| MIG-073 | Export of personal, payroll or financial data requires export permission and is audited as a sensitive disclosure |
| MIG-074 | Export artifacts are private, checksummed, expiring and delivered over an authenticated channel |
| MIG-075 | Export availability during and after subscription suspension or cancellation follows the retention rules in `../05-quality/DATA_PROTECTION_AND_RETENTION.md`; cancellation never triggers immediate irreversible deletion |
| MIG-076 | Large exports run as background operations with an authorization-revalidated delivery step |

## 10. Acceptance and Tests

| ID | Verification |
|---|---|
| MIG-TST-001 | Import of data for a tenant other than the resolved target is impossible, including when the file names another tenant |
| MIG-TST-002 | Import without the dedicated import permission, or a financial import without approval, is rejected |
| MIG-TST-003 | Import for an unentitled module is rejected |
| MIG-TST-004 | Malformed, oversized, wrong-encoding and active-content files are rejected safely at intake |
| MIG-TST-005 | Arabic text round-trips through import and export without loss |
| MIG-TST-006 | Exact decimal parsing is preserved for monetary and quantity values; ambiguous numeric and date input is rejected |
| MIG-TST-007 | Unresolved references are reported with the named key and never auto-created |
| MIG-TST-008 | An unbalanced trial balance and an unreconciled subsidiary ledger both block commit |
| MIG-TST-009 | A failed commit leaves no partially applied business state |
| MIG-TST-010 | A resumed chunked job reapplies no committed chunk |
| MIG-TST-011 | Re-uploading an identical file creates no duplicate records |
| MIG-TST-012 | Staged data is invisible to reports, ledgers, exports and other users, and is purged on schedule |
| MIG-TST-013 | Imported records carry their import job reference and produce audit entries equivalent to interactive creation |
| MIG-TST-014 | Concurrent imports to one domain and tenant are serialized or rejected |
| MIG-TST-015 | Reversal of master and financial imports behaves as specified and never deletes a posted record |
| MIG-TST-016 | Migrated historical documents are excluded from statutory submission by default |
| MIG-TST-017 | Tenant export is complete, schema-declared, tenant-isolated, audited and checksummed |
| MIG-TST-018 | Export remains available through suspension and cancellation per the retention policy |

All scenarios are `NOT_RUN` until the owning phase implements the capability.

## 11. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-MIG-001 | Approve the supported import file formats and published template versions per domain | Product Owner |
| DEC-MIG-002 | Approve the opening-balance mechanism, cut-over approval authority and reconciliation tolerance, which this document sets to zero by default | Finance domain owner |
| DEC-MIG-003 | Approve whether historical closed transactions are in migration scope, and for which document families | Product Owner |
| DEC-MIG-004 | Confirm, with a dated authoritative source, the treatment of migrated historical invoices with respect to UAE e-invoicing obligations | Tax specialist / e-invoicing specialist |
| DEC-MIG-005 | Approve the tenant export schema, completeness scope and post-cancellation availability window | Product Owner / Privacy reviewer |
| DEC-MIG-006 | Approve whether an assisted or provider-led migration service is offered commercially, and its authorization model | Product Owner |

`DEC-MIG-004` is a regulatory dependency. This document asserts no statutory position on migrated documents and records none as verified. These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`.
