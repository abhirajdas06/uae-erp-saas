# PINT AE 1.0.4 Semantic-to-UBL Mapping Register

| Property | Value |
|---|---|
| Document ID | ARCH-PINT-AE-MAP-001 |
| Status | DETAILED DESIGN BASELINE — EXACT CARDINALITIES/CONDITIONS REQUIRE MACHINE VERIFICATION |
| Release set | PINT AE Billing 1.0.4 / PINT General 1.1.3 / PDK 1.4.4 |
| Evidence cut-off | 29 October 2026 |

## 1. Purpose and Notation

This register fixes the initial mapping surface between immutable ERP invoice facts, PINT/PINT AE semantic identifiers and UBL 2.1 syntax. It is a review aid and implementation contract, not a substitute for the exact `1.0.4` semantic model, syntax binding, code lists or Schematron.

`{Doc}` means `ubl:Invoice` for Invoice or `cn:CreditNote` for Credit Note. `{Line}` means `cac:InvoiceLine` or `cac:CreditNoteLine`; quantity and extension elements use the corresponding Invoice/Credit Note names. `@schemeID`, `@currencyID` and `@unitCode` are part of the mapping. A condition marked `profile` must be resolved from the exact published cardinality and UAE rule set, never guessed.

## 2. Control, Identity and Dates

| Semantic ID | Meaning / canonical source | UBL target | Applicability / control |
|---|---|---|---|
| IBT-024 | Specification identifier / ruleset profile | `{Doc}/cbc:CustomizationID` | Required; exact value pinned by profile |
| IBT-023 | Business process type | `{Doc}/cbc:ProfileID` | Required; `1.0.4` pattern validation applies |
| BTAE-02 | Commercial transaction type | `{Doc}/cbc:ProfileExecutionID` | UAE-specific; approved code/flags only |
| IBT-001 | Invoice or credit-note number | `{Doc}/cbc:ID` | Required; immutable issued identifier |
| BTAE-07 | Electronic document UUID | `{Doc}/cbc:UUID` | Generated once; duplicate-prevention evidence |
| IBT-002 | Issue date | `{Doc}/cbc:IssueDate` | Required; authoritative business date |
| IBT-168 | Issue time | `{Doc}/cbc:IssueTime` | Serialize timezone where required by release/ASP |
| IBT-009 | Payment due date | `ubl:Invoice/cbc:DueDate` | Invoice/profile condition; not Credit Note by renaming |
| IBT-003 | Invoice/credit-note type code | `{Doc}/cbc:InvoiceTypeCode` or `cbc:CreditNoteTypeCode` | UNTDID/profile code list; UAE conditions apply |
| IBT-022 | Invoice note | `{Doc}/cbc:Note` | Repeatable/profile; sanitize and minimize |
| IBT-007 | VAT point date | `{Doc}/cbc:TaxPointDate` | Only under approved tax policy |
| IBT-005 | Document currency | `{Doc}/cbc:DocumentCurrencyCode` | ISO 4217; one authoritative document currency |
| IBT-006 | VAT accounting currency | `{Doc}/cbc:TaxCurrencyCode` | Conditional; UAE AED/tax rules and totals reconcile |
| IBT-019 | Buyer accounting reference | `{Doc}/cbc:AccountingCost` | Optional/profile; not authorization data |
| IBT-010 | Buyer reference | `{Doc}/cbc:BuyerReference` | Conditional business reference |

## 3. References and Supporting Documents

| Semantic ID/group | Meaning / canonical source | UBL target | Applicability / control |
|---|---|---|---|
| IBG-03 / IBT-025 | Preceding invoice reference | `{Doc}/cac:BillingReference/cac:InvoiceDocumentReference/cbc:ID` | Credit/correction relationship; same tenant |
| IBT-026 | Preceding invoice issue date | `.../cac:InvoiceDocumentReference/cbc:IssueDate` | Preserve original date |
| IBT-013 | Purchase order reference | `{Doc}/cac:OrderReference/cbc:ID` | Profile condition |
| IBT-014 | Sales order reference | `{Doc}/cac:OrderReference/cbc:SalesOrderID` | From immutable sales source |
| IBT-011 | Project reference | `{Doc}/cac:ProjectReference/cbc:ID` | Same-tenant project contract |
| IBT-012 | Contract reference | `{Doc}/cac:ContractDocumentReference/cbc:ID` | Approved identifier only |
| IBG-24 | Additional supporting document | `{Doc}/cac:AdditionalDocumentReference` | Private file/content controls apply |
| IBT-122 | Supporting document reference | `.../cbc:ID` | Stable evidence identifier |
| IBT-123 | Supporting document description | `.../cbc:DocumentDescription` | Sanitized; no secrets |
| IBT-124 | External document location | `.../cac:Attachment/cac:ExternalReference/cbc:URI` | Only approved secure URI contract |
| IBT-125 | Attached document | `.../cac:Attachment/cbc:EmbeddedDocumentBinaryObject` | Media/filename attributes; size/scan/authorization |
| BTAE profile terms | UAE document/transaction qualifiers | Exact `AdditionalDocumentReference` or published target | Never overload without exact `1.0.4` binding |

## 4. Seller, Buyer, Payee and Tax Representative

| Semantic ID | Meaning / canonical source | UBL target | Applicability / control |
|---|---|---|---|
| IBT-029 | Seller identifier | `{Doc}/cac:AccountingSupplierParty/cac:Party/cac:PartyIdentification/cbc:ID` | Scheme-qualified |
| IBT-034 | Seller electronic address | `.../cac:Party/cbc:EndpointID` | `@schemeID`; validated participant/address |
| IBT-027 | Seller name | `.../cac:Party/cac:PartyName/cbc:Name` | Required snapshot |
| IBT-030 | Seller legal registration ID | `.../cac:Party/cac:PartyLegalEntity/cbc:CompanyID` | `@schemeID`; issuer authority per binding |
| IBT-031 | Seller VAT identifier | `.../cac:Party/cac:PartyTaxScheme/cbc:CompanyID` | VAT scheme; applicability reviewed |
| IBT-032 | Seller tax registration identifier | Separate published `PartyTaxScheme` binding | TIN/tax identifier conditions; do not place tax-type TRN incorrectly |
| IBT-033 | Seller additional legal information | `.../cac:Party/cac:PartyLegalEntity/cbc:CompanyLegalForm` | Profile condition |
| IBT-041 | Seller contact point | `.../cac:Party/cac:Contact/cbc:Name` | Minimize personal data |
| IBT-042 | Seller contact telephone | `.../cac:Party/cac:Contact/cbc:Telephone` | Conditional/profile |
| IBT-043 | Seller contact email | `.../cac:Party/cac:Contact/cbc:ElectronicMail` | Conditional/profile |
| IBT-046 | Buyer identifier | `{Doc}/cac:AccountingCustomerParty/cac:Party/cac:PartyIdentification/cbc:ID` | Scheme-qualified; UAE TIN scheme conditions |
| IBT-049 | Buyer electronic address | `.../cac:Party/cbc:EndpointID` | `@schemeID`; predefined endpoints only in exact scenario |
| IBT-044 | Buyer name | `.../cac:Party/cac:PartyName/cbc:Name` | Required snapshot |
| IBT-047 | Buyer legal registration ID | `.../cac:Party/cac:PartyLegalEntity/cbc:CompanyID` | Conditional UAE rules; distinct from IBT-046 |
| IBT-048 | Buyer VAT identifier | `.../cac:Party/cac:PartyTaxScheme/cbc:CompanyID` | Only where applicable |
| IBT-056 | Buyer contact point | `.../cac:Party/cac:Contact/cbc:Name` | Minimize personal data |
| IBT-057 | Buyer contact telephone | `.../cac:Party/cac:Contact/cbc:Telephone` | Conditional/profile |
| IBT-058 | Buyer contact email | `.../cac:Party/cac:Contact/cbc:ElectronicMail` | Conditional/profile |
| IBT-059 | Payee name | `{Doc}/cac:PayeeParty/cac:PartyName/cbc:Name` | Only when payee differs |
| IBT-060 | Payee identifier | `{Doc}/cac:PayeeParty/cac:PartyIdentification/cbc:ID` | Scheme-qualified |
| IBT-061 | Payee legal registration ID | `{Doc}/cac:PayeeParty/cac:PartyLegalEntity/cbc:CompanyID` | Profile condition |
| IBT-062 | Seller tax representative name | `{Doc}/cac:TaxRepresentativeParty/cac:PartyName/cbc:Name` | Conditional tax policy |
| IBT-063 | Seller tax representative VAT ID | `.../cac:PartyTaxScheme/cbc:CompanyID` | VAT scheme and applicability |

## 5. Postal Addresses

| Terms | Meaning | UBL target from relevant Party/Delivery | Control |
|---|---|---|---|
| IBT-035 / 050 / 064 | Address line 1 | `cac:PostalAddress/cbc:StreetName` | Seller / buyer / tax representative |
| IBT-036 / 051 / 065 | Address line 2 | `cac:PostalAddress/cbc:AdditionalStreetName` | Profile condition |
| IBT-162 / 163 / 164 | Address line 3 | `cac:PostalAddress/cac:AddressLine/cbc:Line` | Exact party context |
| IBT-037 / 052 / 066 | City | `cac:PostalAddress/cbc:CityName` | UAE completeness rules apply |
| IBT-038 / 053 / 067 | Postal code | `cac:PostalAddress/cbc:PostalZone` | Profile condition |
| IBT-039 / 054 / 068 | Country subdivision | `cac:PostalAddress/cbc:CountrySubentity` | UAE emirate code rules where applicable |
| IBT-040 / 055 / 069 | Country code | `cac:PostalAddress/cac:Country/cbc:IdentificationCode` | ISO 3166-1 |

## 6. Delivery, Period and Payment

| Semantic ID | Meaning / canonical source | UBL target | Applicability / control |
|---|---|---|---|
| IBT-072 | Actual delivery date | `{Doc}/cac:Delivery/cbc:ActualDeliveryDate` | Business evidence, not e-way bill |
| IBT-073 / 074 | Invoicing period start/end | `{Doc}/cac:InvoicePeriod/cbc:StartDate` / `cbc:EndDate` | Valid ordered interval |
| IBT-075 / 076 | Line period start/end | `{Line}/cac:InvoicePeriod/...` | Line-specific applicability |
| IBT-070 | Deliver-to location ID | `{Doc}/cac:Delivery/cac:DeliveryLocation/cbc:ID` | Scheme-qualified where supplied |
| IBT-071 | Deliver-to address | `{Doc}/cac:Delivery/cac:DeliveryLocation/cac:Address` | Address subterms/code lists |
| IBT-081 | Payment means code | `{Doc}/cac:PaymentMeans/cbc:PaymentMeansCode` | Approved code list |
| IBT-082 | Payment means text | `.../cbc:PaymentMeansCode` content/attribute per binding | Do not invent unsupported value |
| IBT-083 | Payment reference | `.../cbc:PaymentID` | Reconciliation reference |
| IBT-084 | Payment account ID | `.../cac:PayeeFinancialAccount/cbc:ID` | Sensitive; approved format |
| IBT-085 | Payment account name | `.../cac:PayeeFinancialAccount/cbc:Name` | Conditional |
| IBT-086 | Payment service provider ID | `.../cac:FinancialInstitutionBranch/cbc:ID` | Scheme/format validation |
| IBT-087 / 088 | Card account / holder hint | `.../cac:CardAccount` | Never store full prohibited card data |
| IBT-089 | Mandate reference | `.../cac:PaymentMandate/cbc:ID` | Conditional direct-debit contract |
| IBT-020 | Payment terms | `{Doc}/cac:PaymentTerms/cbc:Note` | Approved terms snapshot |

## 7. Allowances, Charges, Tax and Totals

| Semantic ID/group | Meaning / canonical source | UBL target | Control |
|---|---|---|---|
| IBG-20 / IBT-092 | Document allowance amount | `{Doc}/cac:AllowanceCharge[cbc:ChargeIndicator='false']/cbc:Amount` | `@currencyID`; exact rounding |
| IBT-093 / 094 | Allowance base / percentage | Same group `cbc:BaseAmount` / `cbc:MultiplierFactorNumeric` | Arithmetic reconciliation |
| IBT-095 / 096 | Allowance VAT category / rate | `cac:TaxCategory/cbc:ID` / `cbc:Percent` | UAE category/rate rules |
| IBT-097 / 098 | Allowance reason / code | `cbc:AllowanceChargeReason` / `cbc:AllowanceChargeReasonCode` | Approved code/text |
| IBG-21 / IBT-099 | Document charge amount | `{Doc}/cac:AllowanceCharge[cbc:ChargeIndicator='true']/cbc:Amount` | `@currencyID`; exact rounding |
| IBT-100 / 101 | Charge base / percentage | Same group `cbc:BaseAmount` / `cbc:MultiplierFactorNumeric` | Arithmetic reconciliation |
| IBT-102 / 103 | Charge VAT category / rate | `cac:TaxCategory/cbc:ID` / `cbc:Percent` | UAE rules |
| IBT-104 / 105 | Charge reason / code | `cbc:AllowanceChargeReason` / `cbc:AllowanceChargeReasonCode` | Approved value |
| IBG-23 / IBT-116 | Paid amount | `{Doc}/cac:LegalMonetaryTotal/cbc:PrepaidAmount` | Evidence-backed; not bank settlement inference |
| IBT-113 | Line net total | `{Doc}/cac:LegalMonetaryTotal/cbc:LineExtensionAmount` | Sum/reconcile lines |
| IBT-107 | Allowance total | `.../cbc:AllowanceTotalAmount` | Sum document allowances |
| IBT-108 | Charge total | `.../cbc:ChargeTotalAmount` | Sum document charges |
| IBT-109 | Tax-exclusive amount | `.../cbc:TaxExclusiveAmount` | Reconciled Decimal snapshot |
| IBT-110 | Tax total in document currency | `{Doc}/cac:TaxTotal/cbc:TaxAmount` | `@currencyID`; breakdown reconciliation |
| IBT-111 | Tax total in tax currency | Additional `cac:TaxTotal/cbc:TaxAmount` | Conditional; approved exchange rate |
| IBT-112 | Tax-inclusive amount | `{Doc}/cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount` | Reconcile tax exclusive + tax |
| IBT-114 | Rounding amount | `.../cbc:PayableRoundingAmount` | Approved rounding stage/mode |
| IBT-115 | Amount due | `.../cbc:PayableAmount` | Reconcile totals/prepaid/rounding |
| IBG-23 tax breakdown | Category taxable/tax amounts | `{Doc}/cac:TaxTotal/cac:TaxSubtotal` | One/more breakdowns per exact rules |
| IBT-118 / 119 | VAT category / rate | `.../cac:TaxCategory/cbc:ID` / `cbc:Percent` | Code list and `1.0.4` UAE validation |
| IBT-120 / 121 | Exemption reason text/code | `.../cac:TaxCategory/cbc:TaxExemptionReason` / `cbc:TaxExemptionReasonCode` | Only eligible categories |
| BTAE-04 | Tax currency exchange rate | `{Doc}/cac:TaxExchangeRate/cbc:CalculationRate` plus source/target currency elements | Versioned rate source and precision |

## 8. Lines, Items and Prices

| Semantic ID | Meaning / canonical source | UBL target | Control |
|---|---|---|---|
| IBT-126 | Line identifier | `{Line}/cbc:ID` | Stable within document |
| IBT-129 | Invoiced/credited quantity | `{Line}/cbc:InvoicedQuantity` or `cbc:CreditedQuantity` | `@unitCode`; positive/negative policy |
| IBT-131 | Line net amount | `{Line}/cbc:LineExtensionAmount` | `@currencyID`; server-calculated |
| IBT-132 | Referenced purchase-order line | `{Line}/cac:OrderLineReference/cbc:LineID` | Optional/profile |
| IBT-133 | Line buyer accounting reference | `{Line}/cbc:AccountingCost` | Optional/profile |
| IBT-127 | Line note | `{Line}/cbc:Note` | Sanitized/minimized |
| IBT-153 | Item name | `{Line}/cac:Item/cbc:Name` | Required item snapshot |
| IBT-154 | Item description | `{Line}/cac:Item/cbc:Description` | Sanitized item snapshot |
| IBT-155 | Seller item ID | `{Line}/cac:Item/cac:SellersItemIdentification/cbc:ID` | Optional/profile |
| IBT-156 | Buyer item ID | `{Line}/cac:Item/cac:BuyersItemIdentification/cbc:ID` | Optional/profile |
| IBT-157 | Standard item ID | `{Line}/cac:Item/cac:StandardItemIdentification/cbc:ID` | `@schemeID` |
| IBT-158 | Item classification | `{Line}/cac:Item/cac:CommodityClassification/cbc:ItemClassificationCode` | `@listID` and version where bound |
| IBT-159 | Country of origin | `{Line}/cac:Item/cac:OriginCountry/cbc:IdentificationCode` | ISO 3166-1 |
| IBT-160 / 161 | Item attribute name/value | `{Line}/cac:Item/cac:AdditionalItemProperty/cbc:Name` / `cbc:Value` | Approved attribute; no unsupported extension |
| IBT-151 | Line VAT category | `{Line}/cac:Item/cac:ClassifiedTaxCategory/cbc:ID` | UAE category rules |
| IBT-152 | Line VAT rate | `.../cac:ClassifiedTaxCategory/cbc:Percent` | Exact policy/category condition |
| IBT-146 | Item net price | `{Line}/cac:Price/cbc:PriceAmount` | `@currencyID`; server-calculated |
| IBT-149 | Price base quantity | `{Line}/cac:Price/cbc:BaseQuantity` | `@unitCode`; ratio validation |
| IBT-147 / 148 | Item price discount / gross price | `{Line}/cac:Price/cac:AllowanceCharge` amount/base binding | Reconcile net price; exact binding |
| IBG-27 / 28 | Line allowance / charge | `{Line}/cac:AllowanceCharge` | ChargeIndicator, amount, reason; line reconciliation |

## 9. UAE-Specific and Profile-Controlled Terms

Every `BTAE-*` term not listed above must be added from the exact `1.0.4` semantic/syntax tables before its scenario is supported. This includes transaction flags and scenario-specific principal, tax, establishment, free-zone, margin, export, e-commerce, continuous-supply, deemed-supply, summary-invoice and disclosed-agent information. A generic `extra_fields` object is prohibited.

For each added term record: exact ID/name/definition; section and cardinality; Billing/Credit/Self-Billing/TDD applicability; UBL XPath and attributes; code-list release; source owner; transformation; privacy class; rule IDs; positive/negative fixture; UAE reviewer; and activation decision.

## 10. Coverage and Verification Gate

Before implementing a document profile, generate a machine-readable mapping from this register and the exact `1.0.4` publication. Coverage must show:

- 100% of mandatory terms mapped exactly once;
- every conditional term mapped or explicitly unsupported with its triggering scenario disabled;
- no syntax target populated from an invented fact;
- no unsupported extension or optional field added outside the published/provider contract;
- Invoice and Credit Note mappings tested separately;
- Self-Billing disabled until separately approved;
- all amounts, categories, currencies, identifiers and totals reconciled;
- shared PINT, AE-specific, code-list and provider findings retained separately;
- payload and ruleset digests linked to P04 evidence.

Any unmapped mandatory/triggered conditional term, ambiguous UBL path, mixed release, validator disagreement or provider transformation that changes a business fact blocks submission.
