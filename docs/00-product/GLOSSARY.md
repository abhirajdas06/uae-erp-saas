# Glossary and Domain Dictionary

| Property | Value |
|---|---|
| Document ID | PROD-GLOSSARY-001 |
| Status | PROPOSED BASELINE — REGULATORY AND ARABIC TERMINOLOGY REVIEW REQUIRED |
| Owner | Documentation / Product |
| Related documents | `MASTER_PRODUCT_SPECIFICATION.md`, `PRODUCT_REQUIREMENTS.md`, `UAE_REGULATORY_SOURCE_REGISTER.md`, `../08-requirements-traceability/REQUIREMENT_ID_CONVENTIONS.md` |

## 1. Purpose and Boundary

The specifications use platform, commercial, accounting, tax and payroll vocabulary across more than one hundred and seventy documents, and several terms carry different meanings in the provider domain and the customer domain. A single controlled vocabulary prevents a model, interface label, translation or regulated document from being built on an ambiguous reading.

This document owns the canonical meaning of each term as used in this repository, and the Arabic terminology column used for interface and document translation under `../01-architecture/LOCALIZATION_AND_BILINGUAL_UI.md` L10N-013.

This document is a vocabulary record. It is not a legal definition, an accounting standard, a tax ruling or a compliance statement. Where a term has a statutory meaning, the authoritative definition belongs to the instrument recorded in `UAE_REGULATORY_SOURCE_REGISTER.md`, and the entry here is a working description pending the verification noted in section 6.

## 2. Platform and Tenancy Terms

| Term | Canonical meaning in this repository |
|---|---|
| Platform | The multi-tenant SaaS system as a whole, operated by the provider |
| Provider domain | The provider's own business: tenants, subscriptions, SaaS billing, platform administration. Strictly separated from customer business data per `MASTER_PRODUCT_SPECIFICATION.md` section 6.3 |
| Customer domain | A customer's own ERP data and business processes |
| Tenant | One isolated customer organization and the boundary that owns its data. The foundational isolation unit |
| Tenant isolation | The guarantee that no tenant can read, infer or affect another tenant's data through any path, including cache, file, task, report, sequence and export |
| Tenant context | The server-resolved identity of the acting tenant for a request or task. Never accepted from client input |
| Platform administrator | A provider-side operator acting in the provider domain. Never a member of a tenant |
| Tenant administrator | The highest authority within one tenant, with no authority over the platform or another tenant |
| Module | A bounded ERP capability that can be subscribed to, with an owning specification and a defined interface |
| Module entitlement | A tenant's server-enforced right to use a module, derived from its subscription |
| Module dependency | A module that must be entitled for another module to function |
| Subscription | The commercial agreement governing a tenant's entitlements, lifecycle state and billing |
| SaaS subscription invoice | An invoice the provider issues to a tenant for platform use. Distinct from an ERP customer invoice |
| ERP customer invoice | An invoice a tenant issues to its own customer. Distinct from a SaaS subscription invoice |
| Phase | An authorized increment of work, `P00` to `P12`, with its own specification and exit gate |
| Bounded task | The smallest authorized unit of implementation work, identified as `Pnn-Tnn` |
| Evidence | A recorded artifact supporting a claim, with a declared state such as `NOT_RUN` or `VERIFIED` |
| Entitlement bypass | Any path reaching module functionality without a server-side entitlement check. Always a defect |

## 3. Security and Data Terms

| Term | Canonical meaning in this repository |
|---|---|
| Authentication | Establishing who the actor is |
| Authorization | Establishing what the authenticated actor may do to a specific object |
| Permission | A named authority assignable to a role |
| Role | A named collection of permissions within a tenant |
| Separation of duties | A control requiring distinct actors for conflicting steps of one process |
| Maker-checker | A control requiring a second authorized actor to approve an action before it takes effect |
| Object-level authorization | Authorizing the specific record, not only the endpoint or action type |
| Insecure direct object reference | Reaching a record by identifier without an authorization check. Always a defect |
| Audit trail | The append-only record of who did what, when, to which record, and with what before and after values |
| Data classification | The `C0` to `C5` scheme in `../05-quality/DATA_PROTECTION_AND_RETENTION.md` driving handling, logging, export and retention |
| Personal data | Data identifying a natural person, classified `C3` or above |
| Retention class | The `RET-nn` class determining how long a record is kept and how it is disposed of |
| Legal hold | An authorized suspension of disposal for a named scope |
| Idempotency | The property that a repeated request produces no additional effect |
| Trust boundary | A point where data or control crosses between parties of differing trust, enumerated in `../05-quality/THREAT_MODEL.md` |

## 4. Financial and Accounting Terms

| Term | Canonical meaning in this repository |
|---|---|
| Posted | A financial record committed to the ledger. Immutable under ADR-011; corrected only by reversal or an approved correction path |
| Draft | A record not yet committed to the ledger, editable within its validation rules |
| Reversal | A new posted entry that negates an earlier one, preserving both |
| Cancellation | Marking a document void while retaining it and its number |
| Journal entry | A balanced set of debit and credit lines posted to the ledger |
| Chart of accounts | The tenant's structured set of ledger accounts |
| Control account | A ledger account whose balance must reconcile to a subsidiary ledger total |
| Subsidiary ledger | A detailed ledger, such as receivables or payables, reconciling to its control account |
| Trial balance | The list of account balances that must sum to zero in the base currency |
| Opening balance | The position carried into the platform at the approved cut-over date, recorded through the explicit mechanism in `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` section 7 |
| Cut-over date | The approved date separating prior-system history from platform-recorded activity |
| Period close | The authorized closing of an accounting period, after which new postings are prevented |
| Base currency | The tenant's accounting currency, in which the trial balance must balance |
| Presentation currency | A currency used for display or reporting without changing stored values |
| Monetary precision | The exact decimal representation and rounding rules in ADR-013 |
| Ageing | The breakdown of outstanding receivable or payable balances by time band |
| Reconciliation | Verifying that two independently maintained records agree, and recording any difference |
| Gapless numbering | A document series with no missing value within its scope, per `../01-architecture/DOCUMENT_NUMBERING_AND_SEQUENCES.md` |
| Suspense account | An account holding an unresolved amount. Never populated automatically to force a reconciliation |

## 5. UAE Regulatory and Business Terms

Each entry below is a working description for development purposes. None is a verified statutory definition. Applicability, thresholds, effective dates and exact wording must be taken from the dated sources in `UAE_REGULATORY_SOURCE_REGISTER.md`, `UAE_EMPLOYMENT_PAYROLL_WPS_SOURCE_REGISTER.md` and `UAE_BANKING_PAYMENT_INTEGRATION_SOURCE_REGISTER.md`.

| Term | Working description | Verification status |
|---|---|---|
| FTA | The UAE Federal Tax Authority, the federal tax administration body | `REQUIRES_VERIFICATION` |
| MoF | The UAE Ministry of Finance | `REQUIRES_VERIFICATION` |
| TRN | Tax Registration Number, the identifier issued to a registered taxable person | `REQUIRES_VERIFICATION` |
| VAT | Value Added Tax as applied in the UAE | `REQUIRES_VERIFICATION` |
| Taxable person | A person registered or required to register for VAT | `REQUIRES_VERIFICATION` |
| Tax invoice | The document a taxable person issues for a taxable supply, with mandatory content set by the governing instrument | `REQUIRES_VERIFICATION` |
| Simplified tax invoice | A reduced-content invoice permitted in defined circumstances | `REQUIRES_VERIFICATION` |
| Tax credit note | The document correcting a previously issued tax invoice | `REQUIRES_VERIFICATION` |
| Standard-rated supply | A supply subject to the standard VAT rate | `REQUIRES_VERIFICATION` |
| Zero-rated supply | A taxable supply at a zero rate, retaining input-recovery treatment | `REQUIRES_VERIFICATION` |
| Exempt supply | A supply outside the charge with restricted input recovery | `REQUIRES_VERIFICATION` |
| Out of scope | A transaction outside the VAT charge | `REQUIRES_VERIFICATION` |
| Reverse charge | A mechanism placing the accounting obligation on the recipient | `REQUIRES_VERIFICATION` |
| Tax point | The date determining the tax period in which a supply is accounted for | `REQUIRES_VERIFICATION` |
| Tax period | The period covered by a VAT return | `REQUIRES_VERIFICATION` |
| Designated zone | A defined area with special VAT treatment | `REQUIRES_VERIFICATION` |
| Corporate tax | The UAE federal corporate tax regime | `REQUIRES_VERIFICATION` |
| E-invoicing | The structured electronic invoicing regime and its exchange model | `REQUIRES_VERIFICATION` |
| ASP | Accredited Service Provider, an entity authorized to transmit structured invoices on a taxpayer's behalf | `REQUIRES_VERIFICATION`; selection remains `BLOCKED_EXTERNAL` |
| PINT AE | The UAE implementation profile of the Peppol international invoice specification, versioned per `../01-architecture/PINT_AE_V1_0_4_IMPLEMENTATION_PROFILE.md` | Technical candidate; activation `BLOCKED_EXTERNAL` |
| UBL | Universal Business Language, the XML syntax underlying the structured invoice | Technical reference |
| Clearance and reporting | The submission model by which a structured invoice reaches the authority | `REQUIRES_VERIFICATION` |
| WPS | Wage Protection System, the mechanism for salary payment through approved channels | `REQUIRES_VERIFICATION` |
| SIF | Salary Information File, the structured payroll submission file format | `REQUIRES_VERIFICATION` |
| MOHRE | The UAE Ministry of Human Resources and Emiratisation | `REQUIRES_VERIFICATION` |
| End of service benefit | The terminal entitlement payable to an employee on separation | `REQUIRES_VERIFICATION` |
| Gratuity | A commonly used name for the end of service benefit | `REQUIRES_VERIFICATION` |
| Emiratisation | Policy requirements concerning the employment of UAE nationals | `REQUIRES_VERIFICATION` |
| GPSSA | The federal pensions and social security authority for eligible nationals | `REQUIRES_VERIFICATION` |
| Emirates ID | The national identity document | `REQUIRES_VERIFICATION` |
| Trade licence | The authorization under which an entity conducts business | `REQUIRES_VERIFICATION` |
| Free zone | A jurisdiction with its own licensing and sometimes its own regulatory framework | `REQUIRES_VERIFICATION` |
| PDPL | Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data | `REQUIRES_VERIFICATION`; Executive Regulations status `UNRESOLVED` per `../05-quality/DATA_PROTECTION_AND_RETENTION.md` section 1.1 |
| IBAN | The international bank account number format used for UAE payments | `REQUIRES_VERIFICATION` |
| AED | The UAE dirham, the platform default presentation currency | Settled |

| ID | Requirement |
|---|---|
| GLOS-001 | A term marked `REQUIRES_VERIFICATION` must not be used in code, interface text, a regulated document or a customer-facing statement in a way that asserts a statutory position before its source is verified and dated |
| GLOS-002 | A verified term is recorded in the owning source register with source, source date, verification date and reviewer, and this glossary is updated to point at it |
| GLOS-003 | A regulated term is never redefined locally in a module specification; the module references this glossary and the owning register |

## 6. Arabic Terminology

| ID | Requirement |
|---|---|
| GLOS-010 | An approved Arabic term is recorded here for every term appearing in the interface or in a business document before Arabic release, per `../01-architecture/LOCALIZATION_AND_BILINGUAL_UI.md` L10N-013 |
| GLOS-011 | The Arabic terminology column is populated by a qualified reviewer under `DEC-GLOS-001`; it is intentionally empty rather than machine-translated |
| GLOS-012 | Financial, tax, payroll and legal terms require the named specialist review in `DEC-L10N-005` before use in either language |
| GLOS-013 | Once approved, an Arabic term is used consistently; ad hoc variation in templates or translation catalogues is a defect |

The Arabic terminology table is created when `DEC-GLOS-001` names the reviewer. Populating it with unreviewed translations is prohibited, because an incorrect Arabic rendering of a tax or payroll term on a statutory document carries regulatory consequence.

## 7. Prohibited Ambiguities

| Ambiguity | Required discipline |
|---|---|
| "Invoice" without qualification | Always state SaaS subscription invoice or ERP customer invoice |
| "Customer" without qualification | Always state platform customer, meaning a tenant, or tenant customer, meaning the tenant's own customer |
| "Admin" without qualification | Always state platform administrator or tenant administrator |
| "User" meaning a person or a record | State user account where the record is meant |
| "Delete" for a financial record | State cancel, reverse, deactivate or dispose of, per the applicable rule |
| "Compliant" or "certified" | Never used for this product; state the verified requirement and its evidence instead |
| "Complete" without a subject | State complete as a documentation baseline, as an implementation, or as an approved gate |
| "Supported" for a language or browser | State the verified support level and its evidence |

## 8. Maintenance

| ID | Requirement |
|---|---|
| GLOS-020 | A task introducing a new domain, regulatory or commercial term adds it here in the same task |
| GLOS-021 | A term's meaning is changed only by an approved change, because a semantic change may invalidate a model, a label, a translation or a requirement reference |
| GLOS-022 | A deprecated term is retained with its replacement named, per `../08-requirements-traceability/REQUIREMENT_ID_CONVENTIONS.md` section 1 |

## 9. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-GLOS-001 | Name the qualified Arabic terminology reviewer and approve the bilingual term list before Arabic release | Product Owner |
| DEC-GLOS-002 | Confirm the working descriptions in section 5 against dated authoritative sources and record each verification | Tax, employment and legal reviewers |

These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`. No regulatory definition is asserted as verified by this document.
