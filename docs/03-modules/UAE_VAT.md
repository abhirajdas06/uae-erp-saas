# VAT — UAE VAT Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-UAE-VAT-001 |
| Status | APPROVED SPECIFICATION — TAX POLICY APPROVAL REQUIRED |
| Owning phase / app | P05 / `vat` |
| Regulatory baseline | REG-SRC-001, cut-off 29 October 2026 |

## 1. Purpose and Boundaries

Own validated, effective-dated UAE VAT configuration, calculation policy, immutable tax snapshots, transaction classification, adjustments, reconciliation and return workpapers for explicitly approved scenarios (`VAT-001`–`VAT-003`).

Invoicing/procurement own source documents; Accounting owns ledger/tax control accounts; E-Invoicing consumes approved source tax snapshots. VAT does not issue invoices, write arbitrary ledger lines, file/pay returns automatically, perform tax registration, cover corporate tax/customs, or provide tax advice.

## 2. Actors and Permissions

Tax configuration administrator; finance/tax reviewer; calculation consumer service; adjustment approver; report/workpaper preparer/approver; auditor; purpose-bound support. Configuration, activation, adjustment, report, export and privileged access are separate. Qualified human approval is required to activate a ruleset.

## 3. Model and Historical Integrity

Conceptual records: `VATRegistrationReference`, `VATRuleSet`, `TaxCode`, `TaxTreatment`, `TaxRateComponent`, `TaxCalculationSnapshot`, `VATTransaction`, `VATAdjustment`, `VATPeriodWorkpaper`, `ReturnMappingVersion` and `VATReconciliationFinding`.

- Tenant/legal-entity/registration/jurisdiction/effective-date ownership is explicit.
- Activated rulesets are immutable/versioned; effective periods cannot ambiguously overlap for the same decision key.
- Calculation snapshots preserve inputs, normalized taxable base, treatment/code, rate components, rounding stage/mode, outputs, source version/hash and ruleset.
- Historical issued/posted results never derive from current configuration.
- Adjustments/corrections link to originals and preserve both periods/effects.

## 4. Calculation and Reporting Contract

The service receives trusted tenant/entity/registration, document/line type, parties and locations only when approved, dates, currency, quantities/prices/discounts/charges and tax facts. It returns normalized strings/decimals, treatment/reason, line/category/document results, residual allocation, rule references, warnings and stable snapshot hash.

Rules decide taxable base, inclusivity, supported treatment, evidence and rounding from an approved policy. Missing/ambiguous facts fail closed; they never default silently to a common rate. Clients cannot submit authoritative tax totals.

VAT transactions are created from immutable source snapshots and linked posting evidence. Workpapers group only by approved period/box mapping and expose source-to-tax-to-ledger reconciliation. Corrections and late adjustments follow approved period rules. Outputs are labelled workpapers, not filed returns, unless a future approved filing contract says otherwise.

## 5. Business Rules

| ID | Rule / verification |
|---|---|
| VATM-001 | Only qualified-review-approved effective rulesets can calculate enabled scenarios; policy tests |
| VATM-002 | Rules/codes/evidence/mappings are tenant/entity/registration/effective-date scoped and audited; model tests |
| VATM-003 | Decimal taxable base, inclusivity, calculation and named rounding/residual stages reproduce exactly; golden/property tests |
| VATM-004 | Missing/unsupported/ambiguous facts fail closed and remain visible; negative tests |
| VATM-005 | Issued/posting snapshot remains stable after configuration/source-master changes; historical tests |
| VATM-006 | Credits/adjustments link to original and use approved period/effect without overwriting; correction tests |
| VATM-007 | Source tax snapshots, VAT register and ledger control accounts reconcile or record explained differences; reconciliation tests |
| VATM-008 | Workpaper mappings are versioned and totals drill to authorized source evidence; report tests |
| VATM-009 | No output/UI/API claims filing/compliance beyond approved scope; content/contract tests |
| VATM-010 | Permission, entitlement, tenant isolation/RLS and sensitive export controls cover all paths; security tests |
| VATM-011 | Changes/backfills/restore preserve per-treatment/currency/period totals and policy references; migration/recovery tests |
| VATM-012 | Regulatory source age/change triggers review and safe disablement of affected unverified behavior; operational tests |

## 6. Security, UI and Operations

Tax identifiers, evidence and workpapers are sensitive business data. Redact logs, restrict exports, audit privileged reads/configuration/adjustments, and prevent cross-tenant search/report/cache/task leakage. UI shows ruleset/effective date, treatment, assumptions, calculation breakdown, source/ledger links, reconciliation status and limitations; it never hides an unresolved rule behind a default.

Monitor ruleset expiry/source change, calculation failures, unsupported scenarios, snapshot/hash mismatch, adjustment/late-entry volume, workpaper-to-ledger differences, privileged configuration and exports. Restore verifies counts and totals per entity/registration/period/treatment/currency plus source/ledger/ruleset links.

## 7. Decisions and Evidence

APPR-P05-003 must approve enabled transaction types, registrations/tax groups, treatments, evidence, rates, invoice/credit rules, calculation/rounding, adjustments, periods and workpaper mappings using current official sources. Until then, only interfaces and synthetic tests may be drafted under authorization; production tax behavior remains disabled. Use P05 prompts and P05-TRACE-001.

## 8. Readiness Gate Compliance

Added under `GOV-READINESS-001` gate `RDY-001`–`RDY-012`. This section is PROPOSED and unapproved. Nothing in this section asserts a UAE tax position; every rate, treatment, threshold, period and filing obligation remains owned by the dated sources in the [UAE regulatory source register](../00-product/UAE_REGULATORY_SOURCE_REGISTER.md) and gated by `DEC-TAX-001`.

| Gate | Disposition for `vat` |
|---|---|
| RDY-001 attributes | Section 3 names the owned records and historical-integrity invariants. Tax treatment records carry tenant, effective dates, treatment code, applicability conditions and approval provenance; computed tax results carry `NUMERIC` amounts with the precision, scale and rounding stages approved under ADR-013, the policy version applied, and an immutable link to the source document. No rate value is embedded in code or schema defaults |
| RDY-002 states | A tax determination is draft while its source document is draft, becomes fixed when the source document is issued or posted, and is corrected only through a linked recalculation tied to an authorized correction of the source document. A reporting period has states of open, prepared, under review, finalized and superseded; a finalized period is immutable per ADR-011 |
| RDY-003 testable rules | Satisfied by the business rules in section 5, each with a named verification method |
| RDY-004 permissions | `vat.view_tax_configuration`, `vat.configure_tax_treatment`, `vat.view_determination`, `vat.recalculate_determination`, `vat.view_return_preparation`, `vat.prepare_return_figures`, `vat.review_return_figures`, `vat.finalize_return_figures`, `vat.view_exception`, `vat.export_vat_data`, `vat.view_all_vat`. Preparing, reviewing and finalizing return figures are separate, with maker-checker, because a figure leaving the platform may be relied upon for a filing |
| RDY-005 interface surfaces | Tax treatment configuration, per-document determination detail with its applied policy version, return preparation workspace with per-line drill-down, exception review for documents failing validation, and reconciliation against the ledger, mapped to the data table, monetary cell, definition list and confirmation dialog components in `../01-architecture/UI_DESIGN_SYSTEM.md`. Every surface presenting return figures carries the non-filing disclosure required by `REPM-011` |
| RDY-006 reports and imports | Owns `RPT-301` VAT summary by tax treatment, `RPT-302` VAT transaction detail, `RPT-303` VAT return preparation view, `RPT-304` tax reconciliation and `RPT-305` non-compliant document exception report in `../00-product/REPORT_CATALOGUE.md`. These are preparation aids and never filings; their line composition and any return box reference require `DEC-REP-002` with a dated source. Tax code import follows `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` domain 1, and opening tax balances enter through domain 6 only with tax-specialist approval per `MIG-055`, and never generate a filing obligation claim |
| RDY-007 document numbering | No document type is owned here; tax invoice, credit note and debit note numbering is owned by `ERP_CUSTOMER_INVOICING.md` and registered in `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md`. Whether those series carry a statutory sequential expectation is exactly the open question in `DEC-SEQ-002`, and this module asserts no answer |
| RDY-008 notifications | Registered in `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md`: return figures prepared, return figures awaiting review, return figures finalized, tax reconciliation variance detected, and document failing tax validation. All are regulatory-status category, mandatory and never digested. No notification states or implies that a filing has been made |
| RDY-009 classification and retention | Tax determinations and return figures are `C2`; counterparty tax registration identifiers are `C3`. Retention classes are `RET-02` for tax records and filings and `RET-03` for tax invoices and submission evidence, with `RET-04` where a longer real-estate or capital-asset period applies, under `../05-quality/DATA_PROTECTION_AND_RETENTION.md`. These are precisely the periods that secondary sources contradicted; none is asserted, and `DEC-PRIV-005` with `ISSUE-008` governs |
| RDY-010 threats | `THR-010`, `THR-011`, `THR-034` race producing duplicate determinations, `THR-021` self-approval of return figures, `ABU-01` altering a posted record, `ABU-02` altering a submitted tax invoice, `ABU-06` back-dating into a filed period, `ABU-07` bulk extraction of tax data |
| RDY-011 decision dependencies | `DEC-TAX-001` and `DEC-FIN-001`–`DEC-FIN-005` remain open. Every unapproved treatment, rate, threshold and period rule leaves the dependent behavior disabled and visibly unavailable; the module never defaults to a rate or treatment |
| RDY-012 regulatory assertions | None. No rate, treatment, threshold, tax point, place-of-supply rule, designated-zone rule, filing frequency, deadline or retention period is asserted. A successful calculation is never evidence of compliance |

## 9. Migration, Compatibility and Recovery

A tax policy version is immutable once a determination references it, because recomputing a historical determination under a later policy would falsify a prepared or filed position. A policy correction therefore creates a new version and, where a source document must change, an authorized correction of that document under ADR-011.

Restore verification confirms determination counts and totals by treatment and period, that each finalized period's figures are reproducible from retained snapshots, that tax control accounts reconcile to the computed position, and that audit continuity and policy-version linkage are unbroken.
