# ADR-013: Monetary Precision, Currency, and Rounding

| Field | Details |
|---|---|
| ADR ID | ADR-013 |
| Title | Monetary Precision, Currency, and Rounding |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / Finance Domain Owner |
| Reviewers | Finance, Accounting, UAE Tax, Architecture, Database, Product |
| Affected Phases | P02–P12 |
| Related ADRs | ADR-002, ADR-003, ADR-011, ADR-012, ADR-014, ADR-020 |
| Related Requirements | BILL-002–BILL-004, INV-001–INV-005, ACC-002–ACC-005, VAT-001–VAT-003, PAY-001–PAY-003, FA-002, REP-002, API-008 |
| Related Documents | `MASTER_PRODUCT_SPECIFICATION.md`, `PRODUCT_REQUIREMENTS.md`, `DATABASE_DESIGN.md`, `API_STANDARDS.md`, `COMMERCIAL_MODEL.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The platform will calculate prices, discounts, VAT, invoice totals, journal entries, payroll, depreciation, inventory valuation, payments, foreign-currency amounts, and SaaS subscription charges. Binary floating point, premature rounding, missing currency identity, or inconsistent line-versus-document rounding can produce irreconcilable totals.

Different numeric concepts need different precision: settlement amounts, unit prices, quantities, percentages, tax rates, and exchange rates are not interchangeable. Applicable tax, accounting, payroll, provider, and currency rules can also differ and change over time.

## 2. Decision Drivers

- Exact decimal arithmetic and reproducible calculations.
- Explicit currency and historically stable document values.
- One approved rounding policy per calculation context.
- Reconciliation between UI, API, documents, ledger, reports, and providers.
- Support for AED defaults and approved additional currencies.
- Versioned tax, exchange-rate, and calculation rules.
- Database constraints and tests appropriate to each numeric class.

## 3. Options Considered

### Option A: Decimal arithmetic with typed numeric policies

Use Python `Decimal`, PostgreSQL `NUMERIC`, explicit currency codes, named rounding stages, and effective-dated calculation policies.

**Advantages:** exact, testable, reproducible, and adaptable to domain rules.

**Disadvantages:** requires careful schema design, context control, and comprehensive fixtures.

### Option B: Binary floating point with display rounding

**Advantages:** common in general computation.

**Disadvantages:** representation error and non-reproducible financial equality make it unsuitable.

### Option C: Store all monetary values as integer minor units

**Advantages:** exact for simple settlement amounts.

**Disadvantages:** insufficient alone for unit prices, exchange rates, percentages, intermediate tax calculations, and currencies or policies with different scales.

### Option D: One universal decimal precision and rounding rule

**Advantages:** simple conventions.

**Disadvantages:** conflates distinct measurements and may violate accounting, tax, provider, or currency requirements.

## 4. Decision

Use decimal arithmetic throughout financial workflows. Django `DecimalField`, Python `Decimal`, and PostgreSQL `NUMERIC(precision, scale)` are required for monetary and precision-sensitive values. Binary floating-point types are prohibited for authoritative financial calculation and persistence.

Every authoritative monetary amount must carry or inherit an unambiguous currency from the immutable document or transaction context. Rounding must occur only at named stages defined by an approved, versioned calculation policy.

### 4.1 Numeric classes

Each field must be classified and assigned explicit precision and scale before migration:

| Class | Examples | Policy |
|---|---|---|
| Settled/document money | Invoice total, payment, posted debit/credit | Stored decimal plus currency; final scale follows approved currency/domain rule |
| Unit price and unit cost | Sales price, purchase price, inventory cost | Higher scale than final money where required; rounded only at defined calculation stage |
| Quantity | Units, weight, time | Domain/UOM-specific scale; not treated as currency |
| Percentage/rate | Discount, tax, depreciation rate | Explicit decimal fraction or percentage convention; never ambiguous |
| Exchange rate | Transaction-to-base conversion | Higher explicit scale, direction, source, timestamp/date, and version |
| Derived/report amount | Aggregations, balances | Calculated from authoritative stored values under the documented reporting rule |

A universal database shape for every class is not approved. Module specifications must choose concrete precision and scale within the platform limits before migrations are created.

### 4.2 Currency representation

Use stable standardized currency codes and validate them against an approved currency registry. Store the transaction/document currency on authoritative historical records. Do not derive an old document's currency from the tenant's current default.

AED is the proposed default for UAE tenant configuration, not a universal hardcoded currency. Currency configuration must not change the meaning of existing records.

### 4.3 Calculation context

Financial calculation services must use an explicit decimal context with sufficient working precision. Do not construct `Decimal` from a binary float. Inputs from JSON and forms must be parsed from validated strings or decimal-safe representations.

Database and application precision must agree; silent database rounding or truncation is prohibited.

### 4.4 Rounding policy

Every financial workflow must identify:

- Values rounded.
- Stage of rounding: input normalization, line, tax component, document, posting, settlement, or reporting.
- Scale or quantum.
- Rounding mode.
- Treatment of negative values.
- Aggregation order.
- Residual allocation rule.
- Governing policy or regulatory version.

The recommended technical default where no external or domain rule applies is decimal round-half-up, but it is not approved as a universal UAE tax or accounting rule. VAT, payroll, provider, currency, and contractual rules require explicit validation.

### 4.5 Line and document totals

The product must choose and document whether applicable tax and discount calculations round per line, per tax category, or at document total. Do not calculate one way in the UI and another way in the ledger or provider payload.

Where the sum of rounded components differs from a rounded aggregate, apply a deterministic residual-allocation rule and retain evidence of the adjustment. Never hide a discrepancy through an untraceable “rounding fix.”

### 4.6 Multi-currency

For foreign-currency transactions retain, as applicable:

- Transaction currency and amounts.
- Functional/base currency and amounts.
- Exchange-rate value and direction.
- Rate source, type, and applicable date/time.
- Rate version or external reference.
- Realized and unrealized difference records under approved accounting policy.

Do not recompute historical posted base amounts from a current exchange rate.

### 4.7 Tax and regulated calculations

Tax rules, thresholds, inclusivity, exemptions, apportionment, and rounding are effective-dated domain policies. Store enough snapshots and policy references to reproduce historical results. No value in this ADR establishes a UAE tax rate or filing rule.

### 4.8 API and documents

JSON APIs represent decimal values as strings under `API_STANDARDS.md`; clients must not be required to parse authoritative money from binary JSON numbers. Generated documents and exports must render the stored currency and approved display scale without changing authoritative values.

### 4.9 Equality and reconciliation

Compare quantized amounts under the applicable policy, not approximate floating-point tolerances. Journal balance, payment allocation, document totals, and reconciliation differences must use explicit zero and tolerance rules. Any non-zero tolerated residual must be posted or recorded through an approved account or adjustment policy.

## 5. Rationale

Typed decimal policies preserve precision where necessary while avoiding the false simplicity of one scale for every measurement. Explicit rounding stages make invoice, tax, ledger, API, and provider results reproducible. Currency and exchange-rate snapshots prevent configuration changes from rewriting history.

## 6. Consequences

### Positive consequences

- Reproducible calculations and reports.
- Consistent results across transports and documents.
- Support for unit prices, rates, quantities, and multiple currencies.
- Traceable regulatory and policy changes.

### Negative consequences and trade-offs

- More schema and policy decisions per domain.
- Decimal calculations and residual handling need extensive tests.
- Third-party APIs using floating numbers require careful parsing and validation.
- Higher numeric precision increases storage and index width modestly.

### Risks and mitigations

- **Premature rounding:** central calculation services and named stages.
- **Scale overflow:** field-range tests and explicit database limits.
- **UI/backend mismatch:** shared server calculations and golden fixtures.
- **Historical drift:** snapshot currency, rates, inputs, outputs, and policy versions.
- **Provider mismatch:** adapter-specific contract tests and reconciliation.

## 7. Security and Tenant-Isolation Implications

- Pricing, exchange rates, payroll amounts, and financial policies are tenant/legal-entity scoped where applicable.
- Clients cannot submit authoritative totals or protected exchange-rate results without server verification.
- Sensitive payroll, cost, margin, and banking values require authorization and safe exports.
- Cache keys for calculation policies must include tenant, version, currency, and effective date as applicable.

## 8. Data Integrity and Migration

- Every numeric migration documents precision, scale, range, rounding, and backfill behavior.
- Reducing precision or scale is destructive unless a reviewed conversion and reconciliation plan proves otherwise.
- Constraints validate valid ranges and currency relationships where appropriate.
- Posted historical values must not be bulk-recalculated under new policies.
- Backfills require before/after totals, exceptions, and rollback evidence.

## 9. Operational Impact

Monitor calculation exceptions, overflow, residual adjustments, provider mismatches, exchange-rate gaps, and reconciliation differences. Configuration changes need effective dates, approval, preview of impacted open documents, and rollback procedures.

## 10. Implementation Requirements

1. Create shared decimal parsing and policy primitives without centralizing domain business rules.
2. Define numeric classes, precision, scale, range, and rounding for every financial model before migration.
3. Store currency and rate evidence on authoritative historical records.
4. Define line, tax, document, posting, and settlement rounding per module.
5. Use decimal strings in APIs and exact values in imports/exports.
6. Add golden, boundary, negative, multi-currency, and residual-allocation tests.
7. Version tax and regulated calculation policies.
8. Reconcile generated documents, provider payloads, and ledger postings to stored values.

## 11. Validation and Acceptance Criteria

- [ ] No authoritative monetary calculation uses binary floating point.
- [ ] Every precision-sensitive field has documented precision, scale, and range.
- [ ] Currency is explicit on historical documents and postings.
- [ ] Rounding mode and stage are documented for each workflow.
- [ ] UI, API, document, provider payload, and ledger totals reconcile.
- [ ] Repeated calculation with the same inputs and policy version produces the same result.
- [ ] Exchange-rate direction and historical source are unambiguous.
- [ ] Boundary and overflow inputs fail safely.
- [ ] Negative values and reversals follow symmetrical documented rules.
- [ ] Precision-changing migrations include reconciliation evidence.

## 12. Alternatives Rejected

- Binary floating point is rejected.
- Implicit currency from current tenant settings is rejected for historical records.
- One universal precision and scale is rejected.
- Silent residual write-off is rejected.
- Recalculating posted history under current rules is rejected.

## 13. References

- `docs/00-product/MASTER_PRODUCT_SPECIFICATION.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/API_STANDARDS.md`
- Python decimal arithmetic: https://docs.python.org/3/library/decimal.html
- PostgreSQL numeric types: https://www.postgresql.org/docs/current/datatype-numeric.html
- ISO 4217 currency information must be obtained from the approved maintained source selected during implementation.

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Decimal arithmetic with typed numeric classes, explicit currencies, and versioned rounding policies.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** The monetary representation principles are accepted following `ADR_STANDARDS_REVIEW.md`. Concrete precision, VAT rounding, currency, exchange-rate, and residual policies still require finance/tax approval.

Concrete database precision/scale matrices, VAT rounding, currency support, exchange-rate sources, and domain residual rules remain pending finance and tax review. They block affected model migrations and financial implementation.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial monetary precision, currency, and rounding decision accepted after standards review. |
