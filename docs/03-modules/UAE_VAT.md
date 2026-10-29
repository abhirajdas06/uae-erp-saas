# VAT — UAE VAT Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-UAE-VAT-001 |
| Status | READY FOR REVIEW — TAX POLICY APPROVAL REQUIRED |
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
