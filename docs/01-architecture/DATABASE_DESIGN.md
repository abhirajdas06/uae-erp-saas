# DATABASE DESIGN
## UAE ERP SaaS Platform

### Document Control

| Field | Value |
|---|---|
| Document ID | ARCH-003 |
| Version | 2.0 |
| Status | APPROVED — Technical Data Architecture Baseline; Tax and Compliance Policies Pending |
| Market | United Arab Emirates |
| Primary Database | PostgreSQL |
| Backend | Django |
| Architecture | Modular Monolith |
| Database Strategy | Shared database with tenant isolation |
| Currency Default | AED |
| Primary Localization | English and Arabic |
| Parent Document | `docs/01-architecture/SYSTEM_ARCHITECTURE.md` |
| Related Document | `docs/01-architecture/DJANGO_APP_STRUCTURE.md` |
| Related Document | `docs/01-architecture/MULTI_TENANCY.md` |
| Related Document | `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md` |
| Related Document | `docs/01-architecture/ENTITLEMENT_ENGINE.md` |
| Related Document | `docs/00-product/PRODUCT_REQUIREMENTS.md` |
| Review Owners | Architecture, Finance, UAE Tax, Security and DevOps |
| Last Regulatory Review | 27 October 2026 |

---

# 1. Purpose

This document defines the database design for a UAE-focused, multi-tenant ERP SaaS platform.

The database must support UAE businesses with configurable modules covering:

- Customer relationship management.
- Sales and quotations.
- Tax invoices and credit notes.
- UAE electronic invoicing.
- General ledger and accounting.
- Value Added Tax (VAT).
- Corporate tax data preparation.
- Procurement.
- Inventory and warehouse management.
- Human resources.
- Payroll-related records.
- Projects and expenses.
- Fixed assets.
- Banking and reconciliation.
- Reporting and analytics.
- External integrations.

The database must be designed to support applicable UAE legal, tax, accounting, privacy and electronic invoicing requirements without assuming that all businesses have identical obligations.

## 1.1 Compliance objective

The objective is to make the database **compliance-supporting and auditable by design**.

Database design alone does not establish regulatory compliance. Actual compliance depends on the implemented business rules, approved configurations, validated provider integration, operating procedures, retention controls, and the customer's legal circumstances.

The platform must not advertise that a module is compliant with a UAE government requirement until the applicable requirements have been validated and the implemented solution has passed documented acceptance testing.

## 1.2 Core requirements

The database must provide:

1. Tenant-level data isolation.
2. Accurate financial calculations.
3. Immutable or controlled histories for issued financial documents.
4. Reproducible tax calculations.
5. Configurable tax rules with effective dates.
6. Reliable electronic invoice generation and submission tracking.
7. Evidence of important business and administrative actions.
8. Retention and export capabilities for relevant business records.
9. Secure handling of personal and confidential data.
10. Arabic and English content support.
11. UAE-specific company, tax registration and address information.
12. Reliable migrations and production recovery.
13. Separation between SaaS subscription billing and customer ERP invoicing.
14. Support for future regulatory changes without unnecessary schema redesign.

---

# 2. UAE Regulatory Scope

The following regulatory areas inform the database architecture.

This section is an implementation scope, not a substitute for a legal opinion.

## 2.1 Federal Tax Authority

The system must support business records and workflows associated with the UAE Federal Tax Authority (FTA), subject to the relevant module's approved scope.

Potential areas include:

- VAT registration information.
- Tax invoices and credit notes.
- VAT transaction records.
- VAT return preparation.
- Corporate tax accounting support.
- Tax-period records.
- Supporting documents.
- E-invoicing data and submission status.
- Record export and audit evidence.

The platform must not assume that every FTA interaction is available through a public API.

Where a government portal does not provide an approved integration interface, the product should provide controlled exports, preparation workflows, or documented manual procedures rather than inventing an API.

## 2.2 UAE VAT

The VAT module must support configurable tax treatments and the information required to calculate, report, review and audit VAT.

The implementation must be validated against applicable UAE VAT legislation, executive regulations, decisions, FTA guidance and the customer's circumstances.

The system must not hardcode a single VAT rate or assume every transaction is taxable in the same way.

## 2.3 UAE Corporate Tax

The accounting and reporting architecture must preserve information needed to support corporate tax calculations and reporting.

This may include:

- Accounting profit.
- Tax-period information.
- Revenue and expense records.
- Asset and depreciation records.
- Adjustments relevant to tax computations.
- Related-party transaction information where required.
- Supporting documents.
- Tax computation versions.
- Review and approval history.

The platform must distinguish accounting figures from tax adjustments and taxable-income calculations.

A standard accounting profit-and-loss report must not be presented as a final corporate tax return without the required tax computation and validation.

## 2.4 UAE Electronic Invoicing

The e-invoicing design must support the applicable UAE electronic invoicing framework and the selected Accredited Service Provider (ASP).

The Ministry of Finance has published the UAE e-invoicing framework, official guidelines, mandatory field requirements and subsequent amendments.

The current implementation must be validated against the latest applicable official material before development is finalized.

The architecture must allow for:

- Structured electronic invoice data.
- Electronic credit notes.
- Applicable buyer and seller identifiers.
- Required transaction and tax information.
- Provider-specific validation.
- Submission and response tracking.
- Error handling and retries.
- Required electronic record storage.
- Audit and export capabilities.

A PDF invoice alone must not be treated as an electronic invoice for the UAE e-invoicing system when the applicable framework requires structured electronic data exchange.

## 2.5 Personal Data Protection

The platform must be designed to support applicable UAE personal data protection requirements, subject to the customer's legal status and any applicable exceptions or special regimes.

The system must provide appropriate controls for:

- Data access.
- Purpose limitation.
- Data minimization.
- Secure processing.
- Retention and deletion.
- Data export.
- Incident investigation.
- Access logging.
- Confidential employee information.
- Personal data held in attachments and integration payloads.

Do not assume that one universal privacy rule applies to every UAE free zone, regulated entity or government customer. Applicable laws and regimes must be identified for the intended customer segment.

## 2.6 Record Retention

The database must support configurable retention policies.

For UAE corporate tax purposes, the FTA states that records and documents should generally be retained for at least seven years following the end of the relevant tax period.

> **Source added (`ISSUE-008`, closed as a documentation defect).** The seven-year statement above originally carried no citation or verification date. On 29 October 2026 the official FTA-hosted text of Federal Decree-Law No. 47 of 2022 was read, and Article 56(1) requires a Taxable Person to maintain all records and documents for seven years following the end of the Tax Period to which they relate. The statement above is therefore correct and correctly scoped to corporate tax. It is recorded as `UAE-RET-001` in `../00-product/UAE_REGULATORY_SOURCE_REGISTER.md` section 5, together with the different periods that apply under the Tax Procedures Executive Regulation and the VAT Executive Regulation. Because several instruments can cover one record, the longest applicable obligation governs, and dispute or audit events extend it. The FTA labels its English publications unofficial translations, so the Arabic is authoritative, and applicability per record category remains specialist work under `DEC-PRIV-005`. Do not configure any period from this sentence alone; use the register and the approved policy.

Other records may have different retention requirements or longer periods under applicable law.

The platform must not automatically delete financial or tax records based on a generic account deletion policy.

Retention rules must be validated for each record category before a deletion workflow is activated.

---

# 3. Database Architecture

## 3.1 Primary technology

Use PostgreSQL as the primary relational database.

Use Django ORM for standard persistence, transactions and migrations.

PostgreSQL provides the relational integrity, transactional consistency, constraints and Row-Level Security needed by the platform.

Redis may be used for caching and task coordination. It must not be the authoritative store for financial records, tax records, subscription entitlements or audit history.

## 3.2 Multi-tenant strategy

The initial architecture uses:

- One PostgreSQL deployment per environment.
- Shared database schemas.
- Tenant-owned business records.
- Explicit tenant identifiers.
- Tenant-aware application services.
- Database constraints for critical relationships.
- PostgreSQL Row-Level Security as an additional safeguard.
- Separate application and migration database roles.

The platform should not begin with a separate database for every tenant unless an approved business or regulatory requirement justifies it.

The architecture must not assume that every UAE customer requires the same hosting location or data residency arrangement.

## 3.3 Data residency

Data residency requirements must be assessed before selecting production infrastructure.

The deployment design must document:

- Primary database location.
- Backup storage location.
- Disaster recovery location.
- Object storage location.
- Log and monitoring storage location.
- External processor locations.
- Cross-border data transfer paths.
- Provider subprocessors where applicable.

A UAE-focused product does not automatically become compliant with every data localization requirement by hosting its primary database in the UAE.

Customer contracts, applicable laws, sector-specific rules and provider terms must inform the final decision.

## 3.4 Architecture principles

| Principle | Requirement |
|---|---|
| Tenant isolation | Tenant-owned records must be isolated at application and database layers. |
| Financial integrity | Use decimal arithmetic and controlled posting operations. |
| Tax reproducibility | Preserve tax treatment, calculation inputs and relevant rule versions. |
| Auditability | Record important state changes and user actions. |
| Historical integrity | Preserve issued and posted financial records. |
| Regulatory adaptability | Store configurable rules and effective dates. |
| Data minimization | Store only necessary information. |
| Privacy | Restrict access to personal and confidential information. |
| Localization | Support Arabic, English, UAE dates and currencies. |
| Security | Apply least privilege and protect secrets. |
| Migration safety | Version-control and test all schema changes. |
| Operational recovery | Maintain tested backups and restoration procedures. |

---

# 4. Database Naming and Types

## 4.1 Naming conventions

Use lowercase `snake_case` for database columns.

Examples:

```text
tenant_id
legal_name
trade_name
tax_registration_number
invoice_number
issue_date
tax_point_date
tax_amount
currency_code
created_at
updated_at
```

Use Django's standard table naming conventions unless an approved reason requires an explicit database table name.

## 4.2 Primary keys

Use UUID primary keys for tenants and major business entities unless a documented exception is approved.

UUIDs reduce exposure of sequential identifiers and support safe identifier generation.

They do not provide authorization or tenant isolation by themselves.

## 4.3 Timestamps

Use timezone-aware timestamps.

Recommended field types include:

- `DateField` for business dates.
- `DateTimeField` for event timestamps.
- PostgreSQL `TIMESTAMPTZ` for timezone-aware timestamps.

Store timestamps consistently and render them according to the tenant's configured timezone.

Do not use a timestamp as a substitute for a legally meaningful invoice date or tax point date.

## 4.4 Monetary values

Use Django `DecimalField` and PostgreSQL `NUMERIC` for financial values.

Never use binary floating-point fields for monetary amounts.

The exact precision and rounding rules must be defined for each financial domain and validated against the applicable business and tax requirements.

## 4.5 Country and currency codes

Use standardized country and currency codes.

The tenant's default currency should ordinarily be AED for the UAE-focused default configuration, but the database must support other currencies where permitted.

Store the currency code on historical financial documents. Do not derive the currency of an old invoice from the tenant's current default currency.

---

# 5. Core Platform Data Model

## 5.1 Tenant

App: `tenants`

The tenant represents a customer organization using the SaaS platform.

A tenant is not automatically equivalent to a UAE legal entity, VAT registration, branch or tax group.

A single tenant may need to manage multiple legal entities, registrations or branches, depending on the approved product scope.

Recommended fields:

| Field | Purpose |
|---|---|
| id | UUID primary key |
| name | Display name |
| slug | Platform identifier |
| status | Tenant lifecycle status |
| default_currency_code | Default transaction currency |
| default_country_code | Default country |
| timezone | IANA timezone |
| default_locale | Default interface locale |
| created_at | Creation timestamp |
| updated_at | Last update timestamp |
| suspended_at | Optional suspension timestamp |
| closed_at | Optional closure timestamp |

Recommended statuses:

```text
PENDING
ACTIVE
SUSPENDED
CLOSED
```

Tenant closure must not automatically delete historical business records.

## 5.2 Legal Entity

App: `tenants` or an approved organization domain app.

A legal entity represents the business or legal person whose records are maintained by the ERP.

Recommended fields:

```text
id
tenant_id
legal_name
trade_name
legal_form
country_of_incorporation
commercial_registration_number
trade_licence_number
licence_issuing_authority
registered_address_id
functional_currency_code
financial_year_start
financial_year_end_policy
status
created_at
updated_at
```

The precise fields must be finalized for the intended UAE mainland, free zone and other customer types.

Do not assume that every legal entity has the same licence structure or registration identifiers.

## 5.3 Branch and Establishment

A branch may represent a business location or establishment belonging to a legal entity.

Recommended fields:

```text
id
tenant_id
legal_entity_id
branch_code
branch_name
address_id
status
created_at
updated_at
```

Do not treat branches as separate legal entities unless the customer's legal structure requires that distinction.

## 5.4 Legal Entity Relationships

The data model must be capable of representing:

- One tenant with one legal entity.
- One tenant with multiple legal entities.
- Multiple branches belonging to a legal entity.
- Tax registrations associated with the appropriate legal entity.
- Separate accounting books where required.
- Group-level reporting where authorized.

Whether multi-entity accounting is included in the first commercial release remains a product decision.

## 5.5 User and Tenant Membership

Apps: `users`, `tenants`

A user represents an authenticated platform identity.

A tenant membership represents a user's relationship with a particular tenant.

Recommended membership fields:

```text
id
tenant_id
user_id
status
joined_at
created_at
updated_at
```

Recommended constraint:

```text
UNIQUE (tenant_id, user_id)
```

A user may belong to more than one tenant.

Tenant membership, business roles and permissions must be checked before granting access to tenant data.

---

# 6. UAE Organization and Tax Registration Model

The organization model must separate company identity from tax registration.

Do not place all tax-related fields directly on the tenant record.

## 6.1 Tax Registration

App: `vat` or an approved shared tax domain app.

A legal entity may have one or more tax registrations over time or for different tax purposes, subject to the applicable legal structure.

Recommended conceptual fields:

```text
id
tenant_id
legal_entity_id
tax_type
registration_number
registration_status
effective_from
effective_until
registered_name_snapshot
registered_address_snapshot
created_at
updated_at
```

Possible tax types include:

```text
VAT
CORPORATE_TAX
OTHER_APPROVED_TAX_TYPE
```

These values are illustrative. The actual implementation must define valid types and the appropriate identifiers.

Do not assume that a VAT registration number and a corporate tax registration identifier are interchangeable.

## 6.2 Tax Registration History

A change to a registration number, status or effective date must preserve the history needed to explain which registration applied to a transaction at a particular time.

Avoid overwriting a historical registration snapshot referenced by an issued invoice.

## 6.3 VAT Group Support

The database should be capable of representing a VAT group if the commercial scope requires it.

Potential entities:

```text
TaxGroup
TaxGroupMember
TaxGroupRegistration
TaxGroupMembershipHistory
```

The final structure must distinguish:

- A legal entity.
- A VAT group.
- A member of a VAT group.
- The relevant tax registration.
- The effective dates of membership.
- The role of the representative member, where applicable.

A tax group must not be modeled merely as a label shared by several companies.

Changes to tax group membership must be historically traceable.

## 6.4 UAE Corporate Tax Group Support

If corporate tax group support is included, model it separately from VAT group membership.

Do not assume the membership criteria, legal effects or effective dates are identical.

Potential entities:

```text
CorporateTaxGroup
CorporateTaxGroupMember
CorporateTaxGroupHistory
```

The implementation must be validated against applicable UAE corporate tax requirements.

---

# 7. UAE Address and Localization Data

## 7.1 Address model

Use a reusable address model when appropriate.

Potential fields:

```text
id
tenant_id, nullable for approved global references
country_code
emirate
city
district
street
building_name
building_number
unit_number
po_box
postal_code
address_line_1
address_line_2
created_at
updated_at
```

Not every address field is mandatory for every address type.

The system must distinguish registered addresses, billing addresses, shipping addresses and other address purposes where needed.

Do not assume that every UAE address has a conventional postal code.

## 7.2 Arabic and English

The application must support Unicode and Arabic text.

The schema should support Arabic and English company names, addresses and descriptions where needed.

Possible approaches include:

- Separate Arabic and English columns for stable, commonly used fields.
- A translation model for larger multilingual structures.
- JSONB only for limited, versioned translation metadata where justified.

Do not put core business fields exclusively into JSONB merely to support multilingual content.

## 7.3 RTL support

Right-to-left display is principally an application presentation requirement, but the database must preserve Arabic text without destructive normalization.

Testing must cover:

- Arabic company names.
- Arabic addresses.
- Mixed Arabic and English text.
- Arabic and Latin numerals.
- Invoice descriptions.
- Search and sorting behavior.
- Exported documents.

## 7.4 Date handling

Store business dates in date fields where appropriate.

Store event timestamps using timezone-aware timestamps.

The system must distinguish between:

- Invoice issue date.
- Supply or tax point date, where applicable.
- Accounting posting date.
- Payment date.
- E-invoicing submission timestamp.
- Provider response timestamp.
- Database creation timestamp.

These dates serve different purposes and must not be collapsed into one generic field.

---

# 8. Module Catalogue and Subscription Data

Apps: `subscriptions`, `billing`

The SaaS subscription system must remain separate from ERP financial records.

## 8.1 Module Catalogue

The module catalogue defines the modules available on the platform.

Recommended fields:

```text
id
code
name
description
lifecycle_status
is_commercial
is_sellable
version
created_at
updated_at
```

Example module codes:

```text
CRM
SALES
INVOICING
E_INVOICING
ACCOUNTING
VAT
CORPORATE_TAX
PROCUREMENT
INVENTORY
HRMS
PAYROLL
PROJECTS
EXPENSES
FIXED_ASSETS
BANKING
REPORTING
INTEGRATIONS
```

A module must not be marked sellable merely because a database model exists.

A module may be sold only when its required functionality, security, testing, documentation and acceptance criteria are satisfied.

## 8.2 Subscription

Recommended fields:

```text
id
tenant_id
status
billing_cycle
currency_code
starts_at
current_period_start
current_period_end
cancel_at_period_end
cancelled_at
created_at
updated_at
```

## 8.3 Subscription Module

Recommended fields:

```text
id
tenant_id
subscription_id
module_id
status
price_snapshot
currency_code
effective_from
effective_until
created_at
updated_at
```

Module prices and dependency rules must be configurable data, not hardcoded in application logic.

## 8.4 SaaS Billing

SaaS billing records represent amounts charged by the platform to its customers.

They are not the same as ERP invoices issued by a tenant to its own customers.

Use separate domain entities for:

- SaaS invoices.
- SaaS invoice lines.
- SaaS payments.
- SaaS refunds.
- ERP invoices.
- ERP credit notes.
- ERP customer payments.

This separation is required for clear financial ownership and reporting.

---

# 9. UAE VAT Data Model

App: `vat`

The VAT module must support configurable tax treatments and historical reproducibility.

It must not assume that a single fixed tax rate is sufficient for every transaction.

## 9.1 Tax Code

Potential fields:

```text
id
tenant_id, nullable for approved global templates
code
name
description
tax_type
treatment_category
rate
effective_from
effective_until
is_active
rule_version
created_at
updated_at
```

The final structure must support the required UAE VAT treatments.

Do not hardcode tax rates into invoice calculation functions.

Where shared default tax codes are provided, distinguish platform templates from tenant-specific configurations.

## 9.2 Tax Treatment

A tax treatment must represent the classification and calculation rules used for a transaction.

Potential fields:

```text
id
tenant_id
code
name
jurisdiction
effective_from
effective_until
rule_version
configuration
created_at
updated_at
```

The configuration must be validated and versioned.

A tax treatment should not be editable in a way that silently changes the interpretation of a previously posted invoice.

## 9.3 Transaction Tax Detail

Invoice and credit note lines must preserve the tax treatment applied when the document was issued.

Potential fields:

```text
id
tenant_id
document_type
document_id
document_line_id
tax_code_id
tax_treatment_code_snapshot
tax_rate_snapshot
taxable_amount
tax_amount
currency_code
rule_version
created_at
```

The actual schema should use direct foreign keys to the relevant invoice or credit note entities rather than relying solely on polymorphic identifiers wherever practical.

The table above illustrates the required information and does not prescribe a single physical schema.

## 9.4 VAT Calculation Requirements

The calculation service must define:

- Taxable amount.
- Applicable tax code.
- Tax treatment.
- Tax rate.
- Tax amount.
- Discount treatment.
- Rounding policy.
- Currency.
- Tax point date where applicable.
- Exemption or exception reason where required.
- Related document references.

The calculation must use decimal arithmetic and validated configuration.

## 9.5 VAT Return Data

Potential entities:

```text
VATReturn
VATReturnLine
VATReturnAdjustment
VATReturnReview
VATReturnSubmissionRecord
VATReturnEvidence
```

The exact return structure must be validated against the applicable FTA reporting requirements.

A prepared return must retain:

- The reporting period.
- The underlying transaction scope.
- The calculation version.
- Adjustments.
- Review and approval history.
- Submission status, if submission is integrated.
- Any relevant external reference.

Do not represent a draft or internally prepared VAT return as submitted to the FTA unless submission has been confirmed through an authorized process.

## 9.6 Tax Calculation Versioning

Each tax calculation must be reproducible from the recorded transaction values and the rule version applied.

Changing a tax code must not retroactively rewrite issued documents.

Where rules change, use effective dates and versioned configurations.

---

# 10. UAE Corporate Tax Data Model

App: `corporate_tax`, or another explicitly approved app.

The corporate tax module should be developed after the core accounting model and applicable UAE requirements are validated.

## 10.1 Corporate Tax Profile

Potential fields:

```text
id
tenant_id
legal_entity_id
tax_registration_id
tax_period_start
tax_period_end
taxpayer_category
status
created_at
updated_at
```

Use the actual registration relationship and approved tax-period model.

Do not duplicate tax registration information without a clear historical or domain-specific reason.

## 10.2 Corporate Tax Period

Potential fields:

```text
id
tenant_id
legal_entity_id
period_start
period_end
status
accounting_period_reference
created_at
updated_at
```

The schema must support the relevant tax period and its relationship to the legal entity's accounting period.

Do not assume that every company has a calendar-year financial year.

## 10.3 Tax Adjustments

Potential fields:

```text
id
tenant_id
legal_entity_id
tax_period_id
adjustment_code
description
amount
currency_code
source_reference
supporting_document_id
status
prepared_by_id
reviewed_by_id
created_at
updated_at
```

The exact adjustment categories must be validated against applicable law and approved tax computation requirements.

Tax adjustments must remain distinct from ordinary accounting journal entries unless an approved accounting treatment requires a corresponding journal.

## 10.4 Corporate Tax Computation

Potential entities:

```text
CorporateTaxComputation
CorporateTaxComputationLine
CorporateTaxAdjustment
CorporateTaxReview
CorporateTaxSubmissionRecord
```

A computation should retain:

- Accounting result used as the starting point.
- Applicable tax period.
- Adjustment values.
- Relevant rule version.
- Computation timestamp.
- Prepared-by and reviewed-by information.
- Supporting references.
- Approval status.
- Finalized calculation snapshot.

Do not treat the computation as a filed tax return unless a verified filing process confirms that state.

## 10.5 Record Retention

Corporate tax records and supporting documentation must be retained according to the applicable legal requirements.

The FTA states that corporate tax records and documents should generally be retained for at least seven years following the end of the relevant tax period.

Implement retention policies by record category and legal basis rather than using one arbitrary retention period for all data.

---

# 11. UAE Electronic Invoicing Data Model

App: `e_invoicing`

This is a critical module for the UAE market.

The database must support the applicable UAE e-invoicing framework and the selected Accredited Service Provider.

The module must be implemented against the latest official technical and legal requirements, not against assumptions based on generic electronic invoicing systems.

## 11.1 Architectural requirements

The database must support:

- Structured electronic invoice data.
- Electronic credit note data.
- Required invoice and transaction fields.
- Applicable buyer and seller identifiers.
- Tax information.
- Provider routing and identifiers.
- Validation results.
- Submission attempts.
- Provider responses.
- Status history.
- Required electronic data retention.
- Reconciliation and audit exports.

The integration architecture must be capable of supporting the applicable UAE framework, including the relevant Peppol-based exchange and reporting model.

The precise schema, mandatory fields and payload format must be taken from the current official specifications and the selected provider's validated implementation.

## 11.2 Legal and technical versions

Maintain a controlled registry of applicable technical and rule versions.

Potential entities:

```text
RegulatoryRuleSet
RegulatoryRuleVersion
EInvoiceSchemaVersion
EInvoiceValidationRule
EInvoiceProviderCapability
```

Potential fields:

```text
id
code
version
effective_from
effective_until
source_reference
status
approved_at
approved_by_id
created_at
updated_at
```

Do not silently replace an old validation rule with a new rule when the old rule remains relevant to historical records.

## 11.3 E-Invoice Submission

Potential fields:

```text
id
tenant_id
legal_entity_id
invoice_id
provider_id
external_submission_id
idempotency_key
submission_status
schema_version
rule_version
payload_hash
submitted_at
accepted_at
rejected_at
last_error_code
last_error_summary
created_at
updated_at
```

The final schema must reflect the selected provider and the actual regulatory process.

Do not assume every provider returns the same statuses or identifiers.

## 11.4 Submission Status

The internal status model must distinguish the following concepts:

- Prepared.
- Validated internally.
- Queued.
- Submitted.
- Acknowledged.
- Accepted.
- Rejected.
- Retryable failure.
- Permanent failure.
- Cancelled, where legally and technically permitted.

The final status mapping must be based on the selected provider's response model.

A network timeout must not automatically be interpreted as a failed submission. The provider may have received and processed the request.

The system must reconcile uncertain outcomes before resubmitting.

## 11.5 Submission Attempts

Use a separate submission-attempt record if the provider workflow requires multiple attempts.

Potential fields:

```text
id
tenant_id
submission_id
attempt_number
request_timestamp
response_timestamp
provider_request_id
request_payload_hash
response_payload_hash
http_status
provider_status_code
error_classification
retryable
created_at
```

Avoid storing unnecessary copies of sensitive payloads in every attempt.

Where payload storage is required, apply encryption, access restrictions and retention rules.

## 11.6 Payload Snapshots

The system must retain the information needed to reproduce or inspect the electronic invoice data that was submitted.

The snapshot should capture the relevant values at submission time rather than regenerating a historical payload from mutable records.

Potential information includes:

- Invoice identity.
- Supplier and buyer details.
- Relevant tax registration data.
- Invoice line values.
- Tax classification.
- Totals.
- Document references.
- Applicable schema version.
- Applicable rule version.
- Payload hash.
- Submission metadata.

The final field list must be validated against the official specification.

## 11.7 Electronic Credit Notes

Electronic credit notes must have their own controlled lifecycle and required references.

Where a credit note relates to a previous invoice, the relationship must be explicit.

The system must not silently overwrite an issued invoice to represent a correction.

## 11.8 Accredited Service Provider

Store the selected provider as a controlled integration configuration.

Potential fields:

```text
id
tenant_id
provider_code
provider_name
accreditation_status_snapshot
external_account_reference
environment
connection_status
credential_reference
effective_from
effective_until
created_at
updated_at
```

Do not treat a provider as accredited merely because it is listed in a hardcoded application configuration.

Provider status and eligibility must be verified against the applicable official source before onboarding and reviewed periodically.

Sensitive credentials must be held in a secret manager or stored using an approved encryption strategy.

## 11.9 Regulatory deadlines and applicability

The database and business logic must support configurable implementation dates and applicability rules.

Do not hardcode a single universal UAE e-invoicing date into invoice creation logic.

Potential applicability fields include:

```text
effective_from
effective_until
annual_revenue_threshold
taxpayer_category
transaction_scope
exclusion_code
legal_reference
rule_version
```

These fields are illustrative. The actual applicability engine must follow the current legal framework.

As of the document review date, the Ministry of Finance has published updates to the e-invoicing framework and its implementation rules during 2026. The applicable dates and thresholds must be revalidated against the current official decisions before production release.

## 11.10 Government reporting boundary

Do not assume that every e-invoice must be submitted through a direct ERP-to-FTA API.

Implement the actual required exchange and reporting workflow through the selected ASP and the applicable national framework.

The platform must not claim that a document has been reported to or accepted by a government system unless the integration has evidence of the relevant outcome.

---

# 12. Invoice and Credit Note Model

App: `invoicing`

## 12.1 Invoice

The invoice must preserve the data required to reproduce the issued document.

Potential fields:

```text
id
tenant_id
legal_entity_id
branch_id
customer_id
invoice_number
document_type
issue_date
supply_date
tax_point_date
currency_code
exchange_rate
payment_terms
subtotal
discount_amount
taxable_amount
tax_amount
total_amount
amount_paid
amount_outstanding
document_status
accounting_status
payment_status
created_at
updated_at
```

Not every field is required for every document type. Final fields must follow the approved invoice lifecycle and applicable UAE requirements.

Do not collapse document, accounting, payment and e-invoicing status into one field.

## 12.2 Invoice Snapshot

An issued invoice must retain the relevant buyer and seller details that applied when the document was issued.

Potential snapshot fields include:

- Legal name.
- Trade name, where relevant.
- Registered address.
- Tax registration information.
- Buyer identity and address.
- Invoice currency.
- Payment terms.
- Relevant tax details.
- Document references.

The snapshot must not depend exclusively on mutable customer or legal-entity records.

## 12.3 Invoice Line

Potential fields:

```text
id
tenant_id
invoice_id
line_number
description
product_id
quantity
unit_of_measure
unit_price
discount_amount
taxable_amount
tax_code_snapshot
tax_rate_snapshot
tax_amount
line_total
created_at
updated_at
```

The actual fields must support the applicable invoice and e-invoice requirements.

## 12.4 Credit Note

A credit note must preserve its relationship to the relevant original invoice where required.

Potential fields:

```text
id
tenant_id
legal_entity_id
original_invoice_id
credit_note_number
issue_date
currency_code
reason_code
reason_description
subtotal
tax_amount
total_amount
document_status
created_at
updated_at
```

Use the appropriate document and correction process for the applicable transaction.

Do not use a generic negative invoice as a substitute for a properly modeled credit note where the legal or operational requirements call for a credit note.

## 12.5 Invoice Numbering

Invoice numbering must be concurrency-safe and scoped according to the approved legal and business rules.

Never generate invoice numbers using a count of existing invoices or an unprotected `MAX(invoice_number) + 1` query.

Potential entity:

```text
InvoiceNumberSequence
    id
    tenant_id
    legal_entity_id
    document_type
    financial_year, nullable
    prefix
    next_number
    created_at
    updated_at
```

The final sequence scope must be validated.

Issued document numbers must not be silently reused following deletion or cancellation.

---

# 13. Accounting Data Model

App: `accounting`

The accounting module must preserve a complete, traceable financial ledger.

## 13.1 Core entities

```text
ChartOfAccounts
Account
AccountingPeriod
FiscalYear
Journal
JournalEntry
JournalEntryLine
JournalEntryReversal
AccountingDimension
PeriodCloseRecord
```

## 13.2 Journal entry

A journal entry should contain:

```text
id
tenant_id
legal_entity_id
journal_id
entry_number
posting_date
document_date
currency_code
description
status
source_module
source_document_reference
posted_at
posted_by_id
created_at
updated_at
```

## 13.3 Journal entry line

Potential fields:

```text
id
tenant_id
journal_entry_id
account_id
debit_amount
credit_amount
transaction_currency_code
transaction_currency_amount
exchange_rate
description
created_at
updated_at
```

The final design must define how base currency, transaction currency, exchange rates, and rounding are represented.

## 13.4 Double-entry integrity

A posted journal entry must satisfy:

```text
SUM(debit_amount) = SUM(credit_amount)
```

The equality must be evaluated under the approved currency and rounding rules.

A normal row-level check constraint cannot validate a sum across all journal lines.

Use a transactional posting service with appropriate locking and database safeguards.

A journal entry must not be posted unless it is balanced.

## 13.5 Posted entries

Posted journal entries must not be silently edited or deleted.

Corrections must use approved reversal or adjustment entries.

Preserve:

- Original entry.
- Reversal reference.
- Correction reason.
- Actor.
- Timestamp.
- Approval evidence where required.

## 13.6 Accounting periods

Accounting periods must have explicit opening, closing and reopening rules.

A period close must not be represented only by a user interface flag.

The posting service must enforce the period state during financial posting.

Any exceptional reopening must be authorized and audited.

## 13.7 Financial reports

Financial reports must distinguish:

- Draft entries.
- Posted entries.
- Reversed entries.
- Current-period entries.
- Prior-period adjustments.
- Closed periods.

A report must document which records it includes.

---

# 14. Procurement and Inventory

Apps: `procurement`, `inventory`

## 14.1 Procurement entities

Potential entities:

```text
Supplier
PurchaseRequest
PurchaseRequestLine
PurchaseOrder
PurchaseOrderLine
GoodsReceipt
GoodsReceiptLine
SupplierInvoiceReference
```

Supplier records must be tenant-owned unless a specific shared catalogue feature is approved.

Supplier invoice data must preserve the information needed for accounting and tax review.

## 14.2 Inventory entities

Potential entities:

```text
Product
ProductCategory
Warehouse
WarehouseLocation
StockMovement
StockReservation
StockAdjustment
StockTransfer
StockTransferLine
InventoryBalance
InventoryValuationLayer
```

## 14.3 Stock movement integrity

Stock movements must be the authoritative history of inventory changes.

Inventory balance tables may be maintained for performance but must be reconcilable to the underlying movement records.

Stock operations must be transactional.

Prevent:

- Cross-tenant warehouse references.
- Invalid product references.
- Duplicate processing of external stock events.
- Unapproved negative stock.
- Untraceable manual adjustments.

Whether negative stock is allowed must be an explicit product and accounting policy.

## 14.4 Inventory valuation

Inventory valuation policy must be selected and documented before implementing accounting valuation.

Potential methods include FIFO and weighted average, subject to the applicable accounting policy.

The system must preserve enough historical data to reproduce valuation results.

Do not assume that one valuation method applies to every tenant or item category without an approved product policy.

---

# 15. HRMS and Payroll

Apps: `hrms`, `payroll`

## 15.1 Employee records

Potential entities:

```text
Employee
EmploymentContract
Department
Designation
AttendanceRecord
LeaveRequest
EmployeeDocument
PayrollComponent
PayrollRun
PayrollLine
Payslip
PayrollAdjustment
```

## 15.2 Sensitive information

Employee, salary, identity, bank and payroll data must have stricter access controls than ordinary CRM data.

Do not expose payroll data through generic tenant-wide list endpoints.

Sensitive documents should be stored in controlled object storage with metadata and access checks.

## 15.3 Payroll snapshots

A payroll run must preserve the employee, compensation, component and calculation inputs used for that run.

Subsequent changes to the employee's current salary or employment status must not silently rewrite historical payroll calculations.

## 15.4 UAE-specific validation

Payroll requirements must be validated against the applicable UAE labour and employment framework, including any requirements relevant to the customer's jurisdiction and employment category.

Do not claim that a generic payroll module satisfies every UAE labour, wage protection, end-of-service or pension obligation.

Those rules require explicit requirements, validated calculations and acceptance tests.

---

# 16. Fixed Assets, Expenses and Projects

Apps: `fixed_assets`, `expenses`, `projects`

## 16.1 Fixed assets

Potential entities:

```text
FixedAsset
AssetCategory
AssetAcquisition
AssetDepreciationRun
AssetDepreciationLine
AssetDisposal
AssetAdjustment
```

The data model must support historical acquisition cost, depreciation, disposals and relevant accounting references.

Depreciation rules must be configurable according to the approved accounting policy.

Tax depreciation and accounting depreciation must not automatically be treated as identical.

## 16.2 Expenses

Potential entities:

```text
ExpenseClaim
ExpenseClaimLine
ExpenseApproval
ExpenseReimbursement
ExpenseAttachment
```

Expense records must preserve approval history, relevant receipts, tax information and accounting references.

## 16.3 Projects

Potential entities:

```text
Project
ProjectTask
ProjectMember
ProjectCost
ProjectBillingReference
```

Project cost reporting must distinguish operational estimates from posted financial amounts.

---

# 17. Banking and Payment Data

App: `banking`

Potential entities:

```text
BankAccount
BankStatement
BankStatementLine
BankReconciliation
BankReconciliationMatch
Payment
PaymentAllocation
Refund
```

## 17.1 Security

Do not store raw payment card data.

Do not store bank passwords or provider credentials as unprotected plaintext.

Use an approved secret-management or encryption strategy for external credentials.

## 17.2 Payment processing

Payment processing must support idempotency.

Store external provider references and the minimum information needed for reconciliation.

A repeated callback must not create duplicate payments or allocations.

## 17.3 Reconciliation

Bank statement lines and ERP payments must be matched through explicit reconciliation records.

Do not delete reconciliation history when a match is changed.

Changes must preserve the original and revised state as required by the audit policy.

---

# 18. Audit and Compliance Evidence

App: `audit`

## 18.1 Audit event

Potential fields:

```text
id
tenant_id, nullable for platform events
legal_entity_id, nullable
actor_user_id, nullable for system actions
actor_type
action
resource_type
resource_id
occurred_at
request_id
correlation_id
source
metadata
```

The final design must distinguish tenant-level business events from platform-level administrative events.

## 18.2 Events requiring audit

Record relevant events, including:

- Login and security events.
- User membership and permission changes.
- Legal entity and tax registration changes.
- Invoice issuance.
- Credit note issuance.
- Accounting posting and reversal.
- VAT calculation changes.
- Tax return preparation and approval.
- Corporate tax computation changes.
- E-invoicing submissions and responses.
- Provider configuration changes.
- Payroll approval and posting.
- Inventory adjustments.
- Bank reconciliation changes.
- Data export.
- Retention or deletion operations.
- Administrative access to tenant data.
- Tenant suspension or closure.

## 18.3 Audit integrity

Audit events must be append-only from the ordinary application's perspective.

Ordinary application users must not be able to rewrite or delete audit history.

If a stronger tamper-evident or externally archived audit mechanism is required, it must be designed explicitly.

Do not store passwords, access tokens, bank credentials or unnecessary personal information in audit metadata.

## 18.4 Evidence packages

Where required, the system should be able to produce a controlled export of relevant evidence.

An evidence package may include:

- Original business document.
- Relevant document snapshot.
- Related accounting entries.
- Tax calculation details.
- Applicable rule version.
- E-invoicing submission history.
- Provider responses.
- Audit events.
- Supporting attachments.

The export must be tenant-authorized, logged and reproducible.

---

# 19. Retention, Deletion and Legal Holds

## 19.1 Retention policy

Retention must be configurable by record category and legal basis.

Potential categories:

```text
ACCOUNTING_RECORD
CORPORATE_TAX_RECORD
VAT_RECORD
TAX_INVOICE
EINVOICE_DATA
PAYROLL_RECORD
EMPLOYEE_PERSONAL_DATA
AUDIT_EVENT
INTEGRATION_LOG
TEMPORARY_FILE
```

These are internal classifications, not statements that every category has the same statutory retention period.

## 19.2 Retention policy model

Potential entity:

```text
RetentionPolicy
    id
    record_category
    legal_basis
    minimum_retention_period
    retention_period_unit
    retention_trigger
    effective_from
    effective_until
    approval_status
```

The implementation must distinguish the legally required minimum from a customer-configured retention period.

## 19.3 Legal hold

Where appropriate, support a legal hold that prevents automatic deletion of records subject to an investigation, dispute, audit or other approved hold.

Potential entities:

```text
LegalHold
LegalHoldRecord
```

A legal hold must have:

- A documented reason.
- An authorized owner.
- An effective date.
- A defined scope.
- A review process.
- A release process.
- An audit trail.

## 19.4 Deletion

Tenant closure or subscription cancellation must not immediately delete financial and tax records.

Deletion must consider:

- Applicable retention obligations.
- Active legal holds.
- Accounting dependencies.
- External provider records.
- Backup lifecycle.
- Personal data minimization.
- Contractual commitments.

A deletion request must be evaluated against the applicable legal and retention policy.

---

# 20. PostgreSQL Row-Level Security

## 20.1 Required isolation model

Tenant isolation must be enforced through multiple layers:

```text
User Authentication
        |
        v
Tenant Membership Validation
        |
        v
Authorization and Entitlements
        |
        v
Tenant-Aware Service Layer
        |
        v
Tenant-Aware Database Relationships
        |
        v
PostgreSQL Row-Level Security
```

## 20.2 Tenant-owned tables

Every tenant-owned business table must have a documented ownership strategy.

Prefer an explicit `tenant_id` foreign key.

Avoid relying only on a relationship chain through another table.

## 20.3 Tenant context

A possible PostgreSQL setting is:

```sql
SELECT set_config(
    'app.current_tenant_id',
    '<validated-tenant-uuid>',
    true
);
```

Set tenant context within the transaction that accesses protected data.

Never trust a tenant ID supplied directly by the client without validating the user's membership and authorization.

## 20.4 RLS policy

Illustrative policy:

```sql
ALTER TABLE crm_customer ENABLE ROW LEVEL SECURITY;

ALTER TABLE crm_customer FORCE ROW LEVEL SECURITY;

CREATE POLICY crm_customer_tenant_policy
ON crm_customer
USING (
    tenant_id =
    NULLIF(
        current_setting('app.current_tenant_id', true),
        ''
    )::uuid
)
WITH CHECK (
    tenant_id =
    NULLIF(
        current_setting('app.current_tenant_id', true),
        ''
    )::uuid
);
```

This is illustrative SQL. The actual migration must be tested against the implemented schema and transaction management.

## 20.5 Database roles

- Do not run the application using a PostgreSQL superuser.
- Do not grant `BYPASSRLS` to the normal application role.
- Restrict schema ownership and privileged operations.
- Use a separate migration role where appropriate.
- Test RLS with the same privileges used by the production application.
- Ensure that background tasks establish tenant context correctly.

RLS is a defense-in-depth control and does not eliminate the need to prevent SQL injection or unauthorized SQL execution.

---

# 21. Cross-Tenant Referential Integrity

Every tenant-owned relationship must preserve tenant consistency.

Required invariant:

```text
child.tenant_id == parent.tenant_id
```

For critical relationships, use database-level composite foreign keys where appropriate.

Example:

```sql
ALTER TABLE crm_customer
ADD CONSTRAINT crm_customer_tenant_id_uniq
UNIQUE (tenant_id, id);
```

Then:

```sql
ALTER TABLE invoicing_invoice
ADD CONSTRAINT invoicing_invoice_customer_tenant_fk
FOREIGN KEY (tenant_id, customer_id)
REFERENCES crm_customer (tenant_id, id);
```

The actual implementation must account for Django-generated foreign keys and ensure that database constraints and migration state remain consistent.

Test that the database rejects cross-tenant relationships.

---

# 22. Financial Integrity and Transaction Processing

## 22.1 Transaction boundaries

Use Django transactions for multi-record business operations.

Examples:

- Creating an invoice and its lines.
- Posting a journal entry.
- Reserving inventory.
- Issuing an invoice number.
- Processing a payment callback.
- Finalizing a payroll run.
- Completing a bank reconciliation.

## 22.2 Concurrency

Use appropriate locking and database constraints to prevent race conditions.

Do not use unprotected count-based or maximum-value-based numbering.

## 22.3 External operations

Do not hold long-running database transactions open while waiting for external providers unless an approved design requires it.

For important external operations:

1. Validate the business record.
2. Persist the required internal state.
3. Create a durable job or outbox event.
4. Commit the transaction.
5. Submit the external request.
6. Persist the response.
7. Record the resulting state transition.

## 22.4 Transactional outbox

Potential entity:

```text
OutboxEvent
    id
    tenant_id
    event_type
    aggregate_type
    aggregate_id
    payload
    status
    occurred_at
    published_at
    attempt_count
    last_error
```

Use an outbox where losing an event between database commit and message publication would violate business requirements.

Consumers must be idempotent.

---

# 23. Regulatory Configuration and Change Management

The platform must not treat legal rules as permanent application constants.

## 23.1 Configuration registry

Potential entities:

```text
RegulatoryRuleSet
RegulatoryRuleVersion
RegulatoryRuleParameter
RegulatoryRuleApproval
RegulatoryRuleChangeLog
```

These records may represent validated tax, invoice, retention or reporting rules.

## 23.2 Rule versioning

Every rule that materially affects financial or regulatory calculations must have a version or another reliable historical identification mechanism.

Potential fields:

```text
id
rule_code
version
jurisdiction
effective_from
effective_until
source_reference
approval_status
approved_by_id
approved_at
created_at
updated_at
```

The exact schema must be designed around the rule engine that is actually implemented.

## 23.3 Change process

A regulatory change must follow this process:

1. Identify the official legislative or technical source.
2. Confirm the effective date and applicable customer scope.
3. Obtain review from the designated tax or compliance owner.
4. Document the expected database and business-rule changes.
5. Implement the new rule without silently rewriting historical records.
6. Add tests for the old and new rules.
7. Validate the change in staging.
8. Deploy according to the approved release plan.
9. Record the implementation version and approval evidence.

## 23.4 No unsupported compliance claims

Do not infer compliance merely because a field or table exists.

For example:

- Storing a tax registration number does not prove tax compliance.
- Creating a VAT report does not prove that it matches the applicable FTA return.
- Storing an XML or JSON payload does not prove e-invoicing compliance.
- Recording a provider response does not prove that all required government reporting steps have completed.
- Supporting payroll fields does not prove compliance with every employment obligation.

---

# 24. Indexing and Performance

Indexes must support tenant-scoped queries and actual access patterns.

Potential indexes include:

| Table | Candidate index |
|---|---|
| TenantMembership | `(tenant_id, user_id)` unique |
| LegalEntity | `(tenant_id, status)` |
| TaxRegistration | `(tenant_id, legal_entity_id, tax_type)` |
| Customer | `(tenant_id, created_at)` |
| Invoice | `(tenant_id, issue_date)` |
| Invoice | `(tenant_id, document_status, issue_date)` |
| Invoice | `(tenant_id, invoice_number)` unique where appropriate |
| JournalEntry | `(tenant_id, posting_date)` |
| StockMovement | `(tenant_id, product_id, occurred_at)` |
| VATReturn | `(tenant_id, legal_entity_id, period_start, period_end)` |
| EInvoiceSubmission | `(tenant_id, submission_status, created_at)` |
| AuditEvent | `(tenant_id, occurred_at)` |
| RetentionPolicy | `(record_category, effective_from)` |

These are candidate indexes. The final indexes must be based on the actual schema and measured query patterns.

Avoid redundant indexes and unnecessary indexing of every field.

Use pagination and query optimization for large datasets.

Partitioning and read replicas should be introduced only when justified by measured performance, retention requirements and operational needs.

---

# 25. Data Protection and Security

## 25.1 Least privilege

Use separate database roles where appropriate:

- Application runtime.
- Migration.
- Backup.
- Monitoring.
- Restricted operational access.

The normal application role must not have unnecessary administrative privileges.

## 25.2 Sensitive data

Potentially sensitive data includes:

- Employee information.
- Payroll records.
- Identity documents.
- Bank details.
- Integration credentials.
- Tax documents.
- Confidential customer data.
- Personal contact information.

Use access controls, encryption and retention rules appropriate to each data category.

## 25.3 Secrets

Do not store raw provider secrets in ordinary configuration tables.

Use a secret manager or an approved encryption design with documented key management and rotation.

Do not log credentials or tokens.

## 25.4 Attachments

Store document files in controlled object storage where appropriate.

Database metadata should include:

```text
id
tenant_id
document_category
storage_key
original_filename
content_type
file_size
checksum
uploaded_by_id
uploaded_at
retention_category
```

Do not expose internal storage paths or permanent public URLs for confidential documents.

Access must be authorized at download time.

## 25.5 Data exports

Exports must be tenant-scoped, permission-controlled and audited.

Sensitive exports should have controlled access and expiry where appropriate.

A tenant must not be able to request a report or export that returns another tenant's data.

---

# 26. Government and External Integrations

The integration layer must distinguish between internal ERP identifiers and external identifiers.

Potential entities:

```text
IntegrationProvider
IntegrationConnection
ExternalEntityMapping
IntegrationJob
IntegrationEvent
IntegrationError
```

## 26.1 Provider mapping

A mapping may include:

```text
id
tenant_id
integration_connection_id
entity_type
internal_entity_id
external_entity_id
external_status
last_synced_at
created_at
updated_at
```

External identifier uniqueness must be scoped according to the provider's documented behavior.

## 26.2 Government portal integrations

Do not assume that a government portal exposes a supported public API for every workflow.

For each proposed government integration, document:

- Official system.
- Approved integration channel.
- Authentication method.
- Supported operations.
- Required identifiers.
- Data format.
- Error behavior.
- Rate limits, if applicable.
- Data retention obligations.
- Legal and contractual restrictions.
- Evidence of successful submission or response.

If direct integration is unavailable or not authorized, provide a controlled manual workflow or validated export.

## 26.3 Integration status

Do not represent a record as officially submitted or accepted unless the integration has evidence supporting that status.

Store provider references, timestamps and relevant responses.

---

# 27. Database Migration Strategy

All schema changes must be version-controlled and represented through Django migrations or an approved database-specific migration process.

## 27.1 Migration requirements

Every migration must be:

- Reviewed.
- Tested.
- Reproducible.
- Compatible with the intended deployment sequence.
- Safe for existing data.
- Documented where operationally significant.

Do not manually alter production schema without reconciling the migration history.

## 27.2 Expand-and-contract

For changes that overlap with running application versions:

1. Add the new schema element.
2. Deploy compatible application code.
3. Backfill existing data.
4. Validate consistency.
5. Switch reads and writes.
6. Remove the old schema in a later release.

## 27.3 Data migrations

Data migrations must handle malformed or missing values and must not load entire large tables into memory unnecessarily.

Use historical model definitions through Django migration APIs.

Document recovery procedures for high-risk data migrations.

## 27.4 Production migration checks

Before production deployment:

- Test the migration in staging.
- Review SQL and locking behavior.
- Confirm backup availability.
- Estimate migration duration.
- Check table sizes and index behavior.
- Verify post-migration constraints.
- Verify RLS policies.
- Confirm application health after migration.

---

# 28. Backup and Recovery

Production backup and recovery requirements must be defined in:

`docs/06-deployment/BACKUP_AND_RECOVERY.md`

The plan must specify:

- Backup frequency.
- Point-in-time recovery capability.
- Backup retention.
- Encryption.
- Backup storage location.
- RPO.
- RTO.
- Restore testing frequency.
- Recovery access controls.
- Post-restoration integrity checks.

RPO and RTO must be approved based on the product's business requirements.

Restoration tests must verify:

- Financial data consistency.
- Tenant isolation.
- RLS policies.
- Database roles.
- Migrations.
- Background task safety.
- Integration behavior.
- Historical document accessibility.

A backup is not considered verified until restoration has been tested.

---

# 29. Required Test Coverage

## 29.1 Tenant isolation

Test that:

- Tenant A cannot retrieve Tenant B's invoices.
- Tenant A cannot access Tenant B's customers.
- Tenant A cannot create cross-tenant invoice relationships.
- Tenant A cannot access another tenant's payroll records.
- Tenant A cannot retrieve another tenant's tax records.
- Tenant A cannot access another tenant's attachments.
- Tenant A cannot retrieve another tenant's e-invoicing payloads.
- Tenant A cannot access another tenant's exports.
- Missing tenant context fails closed under RLS.
- Background tasks cannot access records outside their validated tenant context.

## 29.2 Financial integrity

Test that:

- Monetary calculations use decimal arithmetic.
- Invoice totals match the defined calculation rules.
- Historical tax calculations remain reproducible.
- Invoice numbers remain unique under concurrency.
- Posted journal entries balance.
- Posted entries cannot be silently modified.
- Reversals preserve the original entry.
- Inventory operations remain consistent under concurrency.
- Payment callbacks are idempotent.

## 29.3 UAE tax and e-invoicing

Test that:

- Tax codes respect effective dates.
- Historical invoices retain their original tax snapshots.
- Tax calculations use the correct configured rule version.
- Required invoice fields are validated.
- Invalid electronic invoice payloads are rejected before submission.
- Submission retries are idempotent.
- Uncertain provider outcomes are reconciled before resubmission.
- Provider responses are preserved appropriately.
- E-invoicing status is not falsely marked as accepted.
- Regulatory rule changes do not silently rewrite historical documents.

## 29.4 Retention and privacy

Test that:

- Financial records are not deleted by generic account closure.
- Legal holds prevent prohibited deletion.
- Retention policies are applied to the correct categories.
- Sensitive exports are permission-controlled and audited.
- Confidential attachments are not publicly accessible.
- Personal data is not unnecessarily copied into logs or audit metadata.

## 29.5 PostgreSQL integration tests

Use PostgreSQL for tests involving:

- RLS.
- Row locking.
- Composite foreign keys.
- PostgreSQL-specific constraints.
- Production-relevant migrations.
- Concurrent posting and numbering.

SQLite tests alone are insufficient for validating these PostgreSQL-specific controls.

---

# 30. Implementation Roadmap

Implement database features incrementally.

## P0 — Foundation

Implement:

- PostgreSQL configuration.
- Environment separation.
- Database role strategy.
- UUID convention.
- Timestamp convention.
- Initial migration workflow.
- Test database configuration.
- Backup design.
- CI migration checks.

## P1 — Core Platform

Implement:

- Tenant.
- User integration.
- Tenant membership.
- Legal entity foundation.
- Tenant-scoped services.
- Tenant-aware constraints.
- Initial RLS controls.
- Tenant isolation tests.
- Audit foundation.

## P2 — Subscription and Billing

Implement:

- Module catalogue.
- Subscription.
- Subscription module selection.
- Module dependency configuration.
- Pricing snapshots.
- SaaS invoices and payments.
- Subscription history.
- Entitlement checks.

## P3 — CRM, Sales and Invoicing

Implement:

- Customer and supplier foundations.
- Sales orders.
- ERP invoices.
- Invoice lines.
- Credit notes.
- Numbering.
- Tax snapshots.
- Document lifecycle.
- Audit history.

## P4 — UAE E-Invoicing

Before implementation, validate:

- Current official UAE requirements.
- Current technical specifications.
- Mandatory data fields.
- Applicable scope and exclusions.
- Implementation timelines.
- Provider selection and accreditation status.
- Payload and validation requirements.
- Submission and response workflow.
- Data retention obligations.

Then implement the provider integration, submission records, attempts, snapshots, error handling and acceptance tests.

## P5 — Accounting and VAT

Implement:

- Chart of accounts.
- Journal entries and lines.
- Posting and reversal.
- Accounting periods.
- Tax codes and treatments.
- VAT reporting data.
- Tax calculation versioning.
- Financial integrity tests.

## P6 — Procurement and Inventory

Implement:

- Suppliers.
- Purchase orders.
- Goods receipts.
- Products.
- Warehouses.
- Stock movements.
- Inventory valuation.
- Inventory-to-accounting integration.

## P7 — HRMS and Payroll

Implement employee and payroll models only after the applicable requirements and calculation rules have been validated.

## P8 — Projects, Expenses and Fixed Assets

Implement project costs, expenses, asset records, depreciation and related accounting integration.

## P9 — Banking and Advanced Finance

Implement bank statements, reconciliation, payments and related financial controls.

## P10 — Reporting and Integrations

Implement tenant-safe reporting, external mappings, integration event history and relevant evidence exports.

## P11 — Enterprise Readiness

Review multi-entity support, advanced permissions, retention, data residency, audit requirements and scaling.

## P12 — Production Launch

Complete:

- Security review.
- Regulatory validation.
- Migration review.
- Backup restoration testing.
- Performance testing.
- Operational monitoring.
- Incident procedures.
- Production acceptance.

---

# 31. Compliance Acceptance Checklist

The following checklist must be completed before declaring the relevant module ready for commercial release.

## Organization and Tenant Data

- [ ] Legal entity and tenant are modeled separately.
- [ ] Tax registrations are represented independently of general company details.
- [ ] Branch and legal entity relationships are defined.
- [ ] Cross-tenant access tests pass.
- [ ] Required tenant relationship constraints exist.

## VAT

- [ ] Applicable UAE VAT requirements have been reviewed.
- [ ] Tax codes and treatments are configurable.
- [ ] Tax rule effective dates are supported.
- [ ] Historical tax snapshots are preserved.
- [ ] Calculation and rounding rules are documented.
- [ ] VAT reporting outputs have been validated.
- [ ] Supporting evidence and retention rules are documented.

## Corporate Tax

- [ ] Accounting records can be traced to the relevant tax period.
- [ ] Tax adjustments are separately represented.
- [ ] Corporate tax computation versions are retained.
- [ ] Supporting documentation can be retrieved.
- [ ] Applicable record retention is configured.
- [ ] Corporate tax outputs have been validated by a qualified reviewer.

## Electronic Invoicing

- [ ] Current official UAE requirements have been reviewed.
- [ ] Applicable scope and exclusions are configurable.
- [ ] Current implementation deadlines have been verified.
- [ ] Required data fields are validated.
- [ ] Provider accreditation and suitability have been checked.
- [ ] Payload format has passed provider and applicable technical validation.
- [ ] Submission attempts and responses are traceable.
- [ ] Idempotency and retry behavior have been tested.
- [ ] Required electronic data retention is implemented.
- [ ] The platform does not falsely claim official submission or acceptance.

## Privacy and Security

- [ ] Sensitive data categories are identified.
- [ ] Access restrictions are implemented.
- [ ] Retention and deletion rules are documented.
- [ ] Data export is permission-controlled.
- [ ] Database and attachment access are tenant-safe.
- [ ] Provider secrets are protected.
- [ ] Backup locations and data residency have been reviewed.
- [ ] Applicable privacy obligations have been assessed.

## Financial Integrity

- [ ] Financial amounts use decimal types.
- [ ] Invoice numbering is concurrency-safe.
- [ ] Posted entries cannot be silently altered.
- [ ] Corrections preserve audit history.
- [ ] Accounting periods are enforced.
- [ ] Inventory and payment operations are idempotent where required.

---

# 32. Decisions Requiring Approval

Record unresolved decisions in:

`docs/07-project-management/DECISIONS_PENDING.md`

| ID | Decision | Owner |
|---|---|---|
| DB-UAE-001 | Final legal entity and multi-entity accounting scope | Product / Architect |
| DB-UAE-002 | UAE hosting and data residency requirements | Product / Legal / DevOps |
| DB-UAE-003 | Applicable privacy regimes by customer segment | Legal / Security |
| DB-UAE-004 | VAT group data model and supported workflows | Tax / Product |
| DB-UAE-005 | Corporate tax group scope | Tax / Product |
| DB-UAE-006 | VAT calculation and rounding policy | Tax / Finance |
| DB-UAE-007 | Corporate tax computation scope | Tax / Finance |
| DB-UAE-008 | Invoice numbering and correction policy | Tax / Finance |
| DB-UAE-009 | UAE e-invoicing provider selection | Product / Architecture |
| DB-UAE-010 | E-invoicing payload and schema version strategy | Architect / Integration |
| DB-UAE-011 | Applicable electronic record retention policy | Legal / Compliance |
| DB-UAE-012 | Payroll and labour-law scope | HR / Legal / Product |
| DB-UAE-013 | Accounting and inventory valuation policies | Finance |
| DB-UAE-014 | Backup RPO and RTO | Product / DevOps |
| DB-UAE-015 | Regulatory rule approval process | Product / Tax / Compliance |

No agent may silently resolve a legal, tax, accounting or regulatory decision by inventing a value or assuming a universal rule.

---

# 33. Instructions for Codex Agents

## Architect Agent

- Validate this document against the system architecture.
- Review the tenant and legal entity model.
- Review tax registration and group relationships.
- Review RLS and cross-tenant constraints.
- Identify missing relationships and data integrity rules.
- Keep regulatory rules configurable and versioned.
- Do not introduce unsupported government API assumptions.

## Developer Agent

- Implement only the approved phase.
- Keep domain ownership within the correct Django app.
- Use migrations for all schema changes.
- Use decimal arithmetic for financial amounts.
- Preserve historical financial and tax snapshots.
- Do not hardcode legal or tax rules without approved requirements.
- Do not mark a government submission as successful without evidence.
- Implement tenant-safe service methods and database access.

## Test Engineer Agent

- Test tenant isolation at API, service and database levels.
- Test tax rule effective dates.
- Test historical calculation reproducibility.
- Test concurrent invoice numbering.
- Test financial posting invariants.
- Test e-invoicing retries and uncertain outcomes.
- Test retention and legal hold behavior.
- Use PostgreSQL for PostgreSQL-specific tests.

## Security Review Agent

- Review tenant isolation.
- Review RLS and database roles.
- Review employee and payroll data access.
- Review attachment access.
- Review exports and background jobs.
- Review secrets management.
- Review audit integrity and retention behavior.

## Compliance Review Owner

- Validate the current official legal and technical requirements.
- Approve the relevant tax and regulatory rule versions.
- Confirm implementation scope and effective dates.
- Review tax calculations and reports.
- Review electronic invoice data and submission behavior.
- Record approval evidence before commercial release.

## DevOps Agent

- Implement secure database connectivity.
- Restrict database network access.
- Configure backups and restoration.
- Verify production migration safety.
- Review data residency and external processor locations.
- Monitor database health and capacity.

---

# 34. Definition of Done

A database feature is complete only when:

1. Data ownership is documented.
2. Tenant isolation is implemented and tested.
3. Database constraints protect critical relationships.
4. Financial values use appropriate decimal types.
5. Required migrations are committed and tested.
6. Historical financial and tax records remain reproducible.
7. Important state transitions are controlled and auditable.
8. Sensitive data is protected.
9. Background tasks preserve tenant isolation.
10. PostgreSQL-specific tests pass.
11. Retention implications are understood.
12. Regulatory requirements have been validated where applicable.
13. Operational recovery implications are documented.
14. The relevant phase acceptance criteria are satisfied.

---

# 35. Official Regulatory Sources for Review

Before implementing or releasing a UAE tax or e-invoicing feature, the responsible owner must review the current official sources, including:

- UAE Ministry of Finance — Electronic Invoicing System, official guidelines, legislation, mandatory field requirements and provider accreditation information.
- UAE Federal Tax Authority — VAT legislation, guides, tax invoice requirements and corporate tax recordkeeping guidance.
- UAE Government portal — applicable personal data protection legislation.
- Applicable UAE legislation, ministerial decisions, executive regulations and sector-specific requirements.

The official sources must be checked again when the relevant phase begins and before production release because rules, technical specifications, deadlines and provider accreditation status may change.

---

**End of Document**
