# Proposed Configuration Baseline

| Property | Value |
|---|---|
| Document ID | PROD-CONFIG-001 |
| Status | APPROVED DOCUMENTATION BASELINE — ADVISER APPROVAL REQUIRED; NOT A PROFESSIONAL OPINION |
| Proposed by | Product Owner, 30 October 2026 |
| Adviser | **Pending appointment.** No qualified adviser has reviewed any value in this document |
| Related documents | `UAE_REGULATORY_SOURCE_REGISTER.md`, `../03-modules/UAE_VAT.md`, `../03-modules/ACCOUNTING.md`, `../03-modules/HRMS.md`, `../03-modules/PAYROLL.md`, `../03-modules/INVENTORY.md`, `../03-modules/UAE_EINVOICING.md` |

## 1. What This Document Is

This records the concrete configuration the Product Owner proposes for the seven value-dependent decisions that previously had no candidate values at all. It converts those decisions from unanswerable into reviewable.

It is **not** a professional opinion and must never be cited as one. The Product Owner's own submission states that the adviser is pending appointment and that adviser approval is required for every area below. Until a named, qualified professional records a conclusion against each area, the dependent behavior stays disabled and fails closed in its owning module specification.

No value here is verified against an authoritative source by this document. Where a value happens to coincide with something recorded in `UAE_REGULATORY_SOURCE_REGISTER.md`, that register remains the only evidence record.

## 2. Review Findings Against the Verified Register

Three items in the submission do not match, or are absent from, the dated evidence in the source register. They are recorded here rather than silently adopted.

| ID | Finding | Action required |
|---|---|---|
| CONF-REV-001 | **RESOLVED 30 October 2026.** The submission described a 4-corner model. The text of the UAE Electronic Invoicing Guidelines V2.0 was read directly and enumerates **five** corners: Corner 1 Supplier, Corner 2 Supplier ASP, Corner 3 Recipient (buyer) ASP, Corner 4 Recipient (buyer), Corner 5 Federal Tax Authority. The proposed 4-corner description is therefore incorrect, and the fifth corner is the Federal Tax Authority reporting leg | No change to the architecture, which already follows five corners. The configuration proposal is corrected to five corners. A specialist should still confirm applicability and the reporting obligations attached to Corner 5 |
| CONF-REV-002 | **RESOLVED 30 October 2026 in the submission's favour.** The citation is correct and the register was incomplete. The Guidelines V2.0 text confirms that Electronic Invoicing applies to persons in the UAE regardless of VAT registration status unless specifically excluded under Article 4 of MD No. 243 of 2025 and its amendments. The instrument is now recorded as `UAE-EINV-013` | Obtain and archive the operative text of MD No. 243 of 2025 before relying on any specific exclusion, since the exclusion list itself has not been read |
| CONF-REV-003 | **PARTIALLY RESOLVED.** Category A deadlines (ASP appointment 30 October 2026, implementation 1 January 2027) match the verified `UAE-EINV-003`. The Guidelines V2.0 confirm that the phased timeline is governed by MD No. 244 of 2025 and its amendments, but the Category B and C dates (31 March 2027, 1 July 2027, 1 October 2027) were searched for in the Guidelines on 30 October 2026 and are **not** stated there | Obtain MD No. 244 of 2025 and its amendments and verify the Category B and C dates there before relying on them for planning |

## 3. UAE VAT Configuration

Owning module: `../03-modules/UAE_VAT.md`. Decision: `DEC-TAX-001`.

| Item | Proposed value |
|---|---|
| Currency | AED |
| Standard rate | 5 percent |
| Supported treatments | Standard-rated at 5 percent; zero-rated at 0 percent; exempt, with no VAT charged and distinct from zero-rated; out of scope where legally appropriate; reverse charge including applicable imports and domestic reverse-charge transactions; designated-zone transactions configurable to the applicable treatment and transaction facts; VAT adjustments through credit notes, debit adjustments and corrections; mixed and partially taxable supplies through allocation rules |

Proposed system controls:

1. VAT treatment is selected by transaction type, not merely by customer location.
2. Zero-rated, exempt and out-of-scope remain separately distinguishable at all times.
3. VAT registration status and effective dates are recorded.
4. Historical rates and treatments are retained, consistent with the immutable-policy-version rule in `MOD-UAE-VAT-001`.
5. An unsupported or unclassified VAT transaction fails closed.

**Adviser approval required** for the tax-treatment matrix, including designated-zone, export, import, reverse-charge and exempt-supply scenarios. No rate or treatment is enabled in the product until that approval is recorded.

## 4. Financial Calculation Configuration

Owning module: `../03-modules/ACCOUNTING.md`. Decision: `DEC-FIN-001`. Governing architecture: ADR-013.

| Item | Proposed value |
|---|---|
| Calculation precision | 8 decimal places |
| Stored monetary precision | Minimum 4 decimal places internally, with higher precision retained where calculations require it |
| AED presentation precision | 2 decimal places, fils |
| VAT calculation | Calculated on unrounded taxable amounts at the applicable rate, with the legally required rounding applied at the prescribed calculation level |
| Rounding method | Decimal half-up, proposed as default, subject to confirmation against applicable UAE VAT requirements and the accounting policy |
| Functional currency | AED, unless an entity's approved accounting policy specifies otherwise |
| VAT foreign-currency conversion | Applicable UAE Central Bank exchange rate in accordance with the VAT legislation |
| Accounting FX conversion | The approved accounting-policy exchange-rate source |

Proposed controls: record exchange-rate source, currency pair, effective date and rate used; never silently substitute a missing rate; separate calculation precision from display precision; preserve the original transaction currency and amount; store the converted AED value with its rate evidence; keep rounding adjustments traceable; prohibit binary floating-point arithmetic in financial calculations, which is already required by ADR-013 and `MIG-022`.

**Adviser and financial controller approval required** for the rounding methodology, the VAT rounding level, the accounting FX source and the functional currency.

## 5. Employer Jurisdiction and Worker Categories

Owning module: `../03-modules/HRMS.md`. Decision: `DEC-HR-001`.

| Item | Proposed value |
|---|---|
| Country | United Arab Emirates |
| Default employment framework | UAE Federal Decree-Law No. 33 of 2021 and applicable implementing regulations, where applicable |
| Employer establishment | To be confirmed |
| Emirate | To be confirmed |
| Mainland or free-zone status | To be confirmed |
| Applicable employment authority | To be confirmed: MOHRE or the relevant free-zone authority |

Proposed worker categories: full-time, part-time, temporary, flexible-working, remote-working, and other legally recognised employment arrangements where applicable. Worker records must distinguish employees from contractors, consultants, agency workers and other non-employee relationships.

**Adviser approval required** for jurisdiction, governing framework, worker categories, applicable authorities and any sector-specific requirements.

**Production restriction.** Payroll and statutory employment calculations remain disabled until the employer jurisdiction and worker classification are approved. Free-zone status is unresolved, which also leaves `DEC-PRIV-003` open.

## 6. Payroll Component Catalogue

Owning module: `../03-modules/PAYROLL.md`. Decision: `DEC-PAY-001`.

| Group | Proposed components |
|---|---|
| Earnings | Basic salary; housing allowance; transport allowance; other fixed allowances; variable allowances; overtime; commission; incentives and bonuses; other contractual earnings |
| Deductions | Employee-authorised deductions; lawfully permitted absence deductions; loans and salary advances where legally permitted; other legally permitted deductions |
| Employer contributions and costs | Employer pension or social-security contributions where applicable; applicable employer statutory contributions; employer-paid benefits |
| Leave and termination | Paid annual leave; sick leave; other statutory or contractual leave; leave encashment; end-of-service benefits or an applicable alternative savings scheme; final settlement adjustments |
| Outputs | Gross earnings; total deductions; net salary payable; employer contributions; wage-protection reported salary; statutory and contractual liabilities |

Every component carries a component identifier, an earning, deduction or employer-cost classification, its tax and statutory treatment, its wage-protection reporting mapping, an effective date, a calculation method, and approval and audit history. This matches the effective-dated, versioned component model already specified in `MOD-PAYROLL-001`.

**Adviser approval required** for component eligibility, statutory treatment, wage-protection mapping, overtime rules, leave treatment, deductions and end-of-service calculations.

## 7. Wage Protection Configuration

Owning module: `../03-modules/PAYROLL.md`. Decision: `DEC-PAY-002`.

| Item | Proposed value |
|---|---|
| Framework | UAE Wages Protection System, where applicable to the employer |
| File format | MOHRE-approved Salary Information File, using the current specification supported by the selected bank or authorised exchange-house agent |
| Format version | **Pending** confirmation from the selected bank or agent and applicable MOHRE requirements |
| Bank or agent | **Not selected** |

Proposed configuration fields: employer establishment identifier; MOHRE establishment number where applicable; employer bank or agent identifier; employee labour card or applicable identification reference; employee bank account or salary payment identifier; salary period; salary payment date; fixed salary; variable salary; net salary payable; applicable days and leave information; wage-protection transaction and reconciliation references.

Proposed controls: validate file structure before submission; validate employee and employer identifiers; reconcile payroll totals against the generated file; retain submission acknowledgements and rejection responses; prevent duplicate salary submissions; record payment confirmation separately from file generation. These align with `PAYM-006`, `PAYM-008` and the uncertainty rules already specified.

**Production restriction.** No wage-protection file may be generated or submitted until the bank or agent and the format specification are confirmed and tested. This remains the position in `MOD-PAYROLL-001`.

## 8. E-Invoicing Applicability

Owning module: `../03-modules/UAE_EINVOICING.md`. Decisions: `DEC-REG-001`, `DEC-REG-002`, `DEC-INT-002`.

| Item | Proposed value |
|---|---|
| Default scope | The Guidelines V2.0 state that Electronic Invoicing applies to persons in the UAE regardless of VAT registration status, unless specifically excluded under Article 4 of MD No. 243 of 2025 and its amendments. This is broader than the business-to-business and business-to-government framing in the submission, so applicability must be determined per entity against the exclusions and never inferred from VAT registration |
| Model | Peppol-based accredited-service-provider model, **five corners**, verified from the Guidelines V2.0 text on 30 October 2026: Supplier, Supplier ASP, Recipient ASP, Recipient, Federal Tax Authority. The submission's 4-corner description was incorrect and is superseded, per `CONF-REV-001` |
| Applicability determination | Per legal entity, using entity and establishment identity, government or non-government classification, annual revenue and reporting period, applicable transaction types, statutory exclusions, and any voluntary or pilot arrangement |

Proposed categories: A, revenue at or above AED 50 million; B, revenue below AED 50 million; C, government entity within the framework; D, specifically excluded person or transaction where legally established; E, voluntary participant where applicable.

| Category | Proposed ASP appointment | Proposed implementation | Verification state |
|---|---|---|---|
| A | 30 October 2026 | 1 January 2027 | Matches verified `UAE-EINV-003` |
| B | 31 March 2027 | 1 July 2027 | **Unverified**, per `CONF-REV-003` |
| C | 31 March 2027 | 1 October 2027 | **Unverified**, per `CONF-REV-003` |

Proposed controls: establish applicability per legal entity; never infer applicability from VAT registration alone; distinguish structured electronic invoices from PDFs and ordinary email attachments; preserve the invoice and credit-note data required for reporting; maintain ASP accreditation and integration status; support statutory exclusions; retain submission, rejection and acceptance evidence.

**Adviser approval required** for the entity category, revenue calculation, transaction scope, exclusions and applicable deadlines. The selected provider must be checked against the current Ministry of Finance accredited-provider list recorded as `UAE-EINV-006`.

## 9. Inventory Valuation

Owning module: `../03-modules/INVENTORY.md`. Decision: `DEC-INV-002`.

| Item | Proposed value |
|---|---|
| Default method | Weighted average cost |
| Alternative supported | First-in, first-out |
| Specific identification | Supported for items not ordinarily interchangeable, or where individual identification is appropriate |
| Valuation basis | Lower of cost and net realisable value, subject to the applicable accounting framework |
| Prohibited | Last-in, first-out |

Proposed cost components: purchase price; import duties and non-recoverable taxes; freight and transport; handling costs; direct conversion costs where applicable; other costs necessary to bring inventory to its present location and condition.

Proposed method-selection rules: weighted average as default for interchangeable goods; first-in, first-out where older stock is consumed or sold first, including expiry-sensitive stock; specific identification for unique, high-value or individually identifiable inventory.

Proposed controls: one approved cost formula per inventory class of similar nature and use; effective-date tracking; historical valuation reproducibility; stock adjustment audit trails; write-downs and reversals; no retrospective method change without authorised accounting approval. The prohibition on retrospective change matches the path-dependence rule already stated in `MOD-INVENTORY-001`.

**Financial controller or qualified accountant approval required** for the accounting framework, stock characteristics, valuation policy and opening inventory treatment.

## 10. Status of Each Area

| Decision | Status after this document | What closes it |
|---|---|---|
| `DEC-TAX-001` | `RECOMMENDED` | Named tax adviser approves the treatment matrix |
| `DEC-FIN-001` | `RECOMMENDED` | Tax adviser and financial controller approve rounding, VAT rounding level, FX source and functional currency |
| `DEC-HR-001` | `RECOMMENDED` | Employment adviser confirms jurisdiction, establishment, emirate, mainland or free-zone status, authority and categories |
| `DEC-PAY-001` | `RECOMMENDED` | Payroll adviser approves components and statutory treatment |
| `DEC-PAY-002` | `RECOMMENDED` | Bank or agent selected, and the format specification confirmed and tested |
| `DEC-REG-001`, `DEC-REG-002` | `RECOMMENDED` | Tax adviser confirms category and scope; `CONF-REV-001` to `CONF-REV-003` resolved |
| `DEC-INV-002` | `RECOMMENDED` | Financial controller or accountant approves the valuation policy |

`RECOMMENDED` means a proposed option is documented and awaits review, per the status vocabulary in `../07-project-management/DECISIONS_PENDING.md` section 2. It does not mean approved, and no dependent behavior is enabled by it.

## 11. Next Action

Appoint the advisers. Each area above is now a review task with its values written down, not an open question. `APPROVAL_RECORD_FORM.md` section 4 holds the blocks for recording each conclusion, and `CONF-REV-001` to `CONF-REV-003` should be put to the e-invoicing specialist first, because the corner-model question affects P04 architecture rather than configuration.
