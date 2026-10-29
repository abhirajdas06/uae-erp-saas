# UAE Regulatory Source Register — E-Invoicing and VAT

| Property | Value |
|---|---|
| Document ID | REG-SRC-001 |
| Status | DATED RESEARCH BASELINE — SPECIALIST REVIEW REQUIRED |
| Evidence cut-off | 29 October 2026 |
| Owner | Product / UAE Regulatory Research |
| Applies to | P03–P05 and production release governance |

## 1. Purpose and Limits

This register records the authoritative sources used to draft the UAE e-invoicing and VAT specifications. It is not legal or tax advice, provider accreditation evidence, or a compliance certificate. A dated entry proves only that the cited official material was reviewed on the stated date.

Regulated behavior must use an approved, effective-dated policy derived from the operative legislation, official guidance, the tenant's facts, and qualified UAE tax/legal review. When sources conflict, later amending legislation prevails over earlier text; guidance cannot override legislation. Marketing pages, blogs, provider summaries, search snippets, and agent recollection are not authoritative.

## 2. Evidence Classifications

| Class | Meaning | Permitted use |
|---|---|---|
| `VERIFIED_PRIMARY` | Current official legislation or official regulator publication was reviewed | May inform a proposed policy, subject to applicability and specialist review |
| `OFFICIAL_GUIDANCE` | Official explanatory or technical guidance | May guide design; legislation and later amendments prevail |
| `CONTRACT_REQUIRED` | Exact behavior depends on a selected provider or service contract | Interface/test drafting only until provider evidence is approved |
| `SPECIALIST_REQUIRED` | Applicability or interpretation needs qualified UAE tax/legal/accounting review | Affected production behavior remains disabled |
| `SUPERSEDED` | Replaced or amended source | Historical traceability only; never used alone as current rule |

## 3. UAE E-Invoicing Sources

| Source ID | Authority / source | Version or date | Class | Verified facts and implementation use | Supersession / revalidation |
|---|---|---|---|---|---|
| UAE-EINV-001 | [Ministry of Finance E-Invoicing portal](https://mof.gov.ae/en/about-us/initiatives/einvoicing/) | Reviewed 2026-10-29 | `VERIFIED_PRIMARY` / `OFFICIAL_GUIDANCE` | Official programme entry point; describes structured eInvoices, the five-corner model, PINT AE, ASP participation, tax data reporting and message statuses. PDF/image/email alone is not treated as the structured eInvoice. | Recheck at every P04 task, provider selection, phase exit and release. Portal states it is the official programme source. |
| UAE-EINV-002 | [Ministerial Decision No. 244 of 2025](https://mof.gov.ae/wp-content/uploads/2025/09/Ministerial-Decision-No.-244-of-2025-on-the-Implementation-of-the-Electronic-Invoicing-System.pdf) | 2025 | `VERIFIED_PRIMARY` | Establishes implementation categories and original dates, including pilot/voluntary commencement and phased obligations. B2C is excluded until a further decision. | Use only with UAE-EINV-003 and later amendments. Applicability requires specialist review. |
| UAE-EINV-003 | [Ministerial Resolution No. 66 of 2026](https://mof.gov.ae/wp-content/uploads/2026/05/Ministerial-Resolution-No.-66-of-2026-Amending-Certain-Provisions-of-Ministerial-Resolution-No.-244-of-2025-Regarding-the-Implementation-of-the-Electronic-Invoicing-System-En-20260514.pdf) | 2026 | `VERIFIED_PRIMARY` | Amends Decision 244; for businesses at or above AED 50 million revenue, the ASP appointment deadline is 30 October 2026 while implementation remains 1 January 2027. | Operative amendment as of evidence cut-off; recheck for later decisions. Do not infer a tenant's category from incomplete data. |
| UAE-EINV-004 | [MoF announcement of Ministerial Decision No. 197 of 2026](https://mof.gov.ae/en/news/ministry-of-finance-amends-electronic-invoicing-regulations-to-ease-the-burden-on-businesses/) | Effective 2026-10-01 | `VERIFIED_PRIMARY` | Announces amendments including temporary exclusion for transactions within the same Tax Group for 24 months from 1 January 2027; retention aligned to the Tax Procedures Law with production to FTA on request; removal of prior UAE-location storage wording; repeal of the former system-failure notification article. | Obtain and archive the operative decision text before implementing these rules. Do not retain superseded notification/location behavior as current. |
| UAE-EINV-005 | [MoF accreditation framework announcement — Ministerial Decision No. 168 of 2026](https://mof.gov.ae/en/news/ministry-of-finance-issues-decision-on-accreditation-of-einvoicing-service-providers-under-updated-regulatory-framework/) | Effective 2026-10-01 | `VERIFIED_PRIMARY` | Replaces the earlier accreditation framework, removes the pre-approval stage, and provides transition treatment for earlier preliminary approvals. | Decisions 64/2025 and 56/2026 are not a current provider-selection baseline. Verify the operative text and list at selection. |
| UAE-EINV-006 | [Official accredited ASP list](https://mof.gov.ae/en/about-us/initiatives/einvoicing/einvoicing-accredited-service-providers-asps/) | Dynamic; reviewed 2026-10-29 | `VERIFIED_PRIMARY` | Authoritative current-list check for provider due diligence. | Dynamic evidence: capture dated page/export and current accreditation at onboarding and release. Listing does not prove contractual capability or product compliance. |
| UAE-EINV-007 | [MoF ASP accreditation service](https://mof.gov.ae/en/services/accreditation-of-einvoicing-service-providers/) | Reviewed 2026-10-29 | `OFFICIAL_GUIDANCE` | Official process and conditions for ASP accreditation. | Provider selection remains a Product/Security/Legal/Commercial decision. |
| UAE-EINV-008 | [UAE Electronic Invoicing Guidelines v1.1](https://mof.gov.ae/wp-content/uploads/2026/06/UAE-Electronic-Invoicing-Guidelines_V-1.1-01June2026.pdf) | 2026-06-01 | `OFFICIAL_GUIDANCE` | Technical and programme guidance supporting vocabulary, actors and workflow analysis. | Later decisions and portal publications prevail. Archive checksum/version before implementation. |
| UAE-EINV-009 | Mandatory field requirements and current PINT AE technical artefacts linked from UAE-EINV-001 | Dynamic | `CONTRACT_REQUIRED` / `SPECIALIST_REQUIRED` | Exact supported documents, fields, validations, code lists, XML and status semantics must be versioned into the P04 ruleset and adapter contract. | Not approved by this register; download, checksum, map and review before P04 schema/code. |

### 3.1 Draft-safe conclusions

- Use a dedicated provider-neutral domain boundary, but do not claim providers are interchangeable.
- Preserve immutable canonical invoice/credit snapshots and the exact regulatory/provider schema version used.
- Model the five-corner workflow and its acknowledgements/statuses without equating transport success to tax-authority acceptance.
- Provider selection, tenant applicability, mandatory-field mapping, status semantics, retention interpretation and production compliance remain approval gates.

## 4. UAE VAT and Accounting-Record Sources

| Source ID | Authority / source | Version or date | Class | Verified facts and implementation use | Revalidation |
|---|---|---|---|---|---|
| UAE-VAT-001 | [Federal Tax Authority VAT legislation index](https://tax.gov.ae/en/legislation/vat.aspx) | Page updated 2026-09-28; reviewed 2026-10-29 | `VERIFIED_PRIMARY` | Canonical discovery page for the VAT Decree-Law, Executive Regulation, amendments and current FTA decisions. Its 2026 index includes the September 2026 Executive Regulation and current FTA decisions. | Recheck before every P05 policy approval, phase exit and release. |
| UAE-VAT-002 | [VAT Federal Decree-Law legislation page](https://tax.gov.ae/en/legislation/vat/vat-decree-law.aspx) | Dynamic; reviewed 2026-10-29 | `VERIFIED_PRIMARY` | Official access point for the VAT law and amendments. | Archive the operative consolidated text and amendment chain for the implementation policy version. |
| UAE-VAT-003 | [VAT Executive Regulation and amendments](https://tax.gov.ae//Datafolder/Files/Legislation/2026/Law-No-8-of-2017-and-its-amendments--09-2026.pdf) | Issued 2026-09-01; published 2026-09-10 | `VERIFIED_PRIMARY` | Current official Executive Regulation listed by the FTA at the cut-off. It is the starting source for tax invoices/credit notes, calculation, evidence and procedural rules. | Exact interpretations, supported treatments, rounding and fields require qualified review; later amendments prevail. |
| UAE-VAT-004 | [FTA amendments index](https://tax.gov.ae/en/content/amendments.to.the.vat.federal.decreelaw.no.8.of.2017.aspx) | Dynamic; reviewed 2026-10-29 | `VERIFIED_PRIMARY` | Official amendment discovery and change-control input. | Policy activation must confirm no later amendment. |
| UAE-VAT-005 | [FTA VAT return filing and payments](https://tax.gov.ae/en/content/filing.vat.returns.and.making.payments.aspx) | Reviewed 2026-10-29 | `OFFICIAL_GUIDANCE` | Official operational guidance states returns and payments are due within 28 days after the end of the tax period. | Tenant tax periods, exceptions and filing responsibility require review; P05 initially produces workpapers, not automatic filing. |
| UAE-VAT-006 | [FTA VAT Returns User Guide](https://tax.gov.ae/-/media/Files/EN/PDF/Guides/VAT-Returns-User-Guide.pdf) | Dynamic guide | `OFFICIAL_GUIDANCE` | Supports proposed return-workpaper mapping and reconciliation design. | Check guide revision, form version and legislation at implementation/release. |
| UAE-VAT-007 | [FTA Decision No. 4 of 2026 on accounting records and commercial books](https://tax.gov.ae//Datafolder/Files/Legislation/2026/FTA%20Decision%20No.%204%20of%202026%20on%20the%20Rules%20and%20Requirements%20-%2018%2008%202026.pdf) | 2026 | `VERIFIED_PRIMARY` | Official input to accounting-record form, accessibility and electronic-record governance. | Qualified review must determine applicability and retention obligations for each record class. |
| UAE-VAT-008 | FTA decisions and clarifications listed on UAE-VAT-001, including 2026 decisions affecting evidence and input-tax treatment | Dynamic | `SPECIALIST_REQUIRED` | Signals that treatments and evidence can change and cannot be represented by one hardcoded rate. | Tax specialist selects applicable decisions per supported scenario. |

### 4.1 Draft-safe conclusions

- Tax codes, treatments, evidence requirements and reporting mappings must be effective-dated and versioned.
- P05 must reproduce calculations and reports from immutable source/tax snapshots using decimal arithmetic.
- No VAT rate, registration threshold, place-of-supply rule, recovery rule, invoice field, retention period or filing representation becomes enabled merely because it appears in guidance.
- Initial P05 scope is calculation, reconciliation and return workpapers for explicitly approved treatments; government filing/API submission is excluded until separately specified and approved.

## 5. Required Revalidation Record

Every regulated task/release records: source IDs and retrieved versions; retrieval date and checksum for downloaded artefacts; effective date; applicability assumptions; differences from the prior policy; qualified reviewer; approved policy version; test fixtures; affected tenants/document types; rollback/disable plan; and next-review trigger.

Revalidate on any official amendment, portal/schema/provider notice, tenant applicability change, provider onboarding/change, failed conformance test, P04/P05 exit, and production release. Regulatory drift opens an issue and disables only the affected unverified behavior where safe.

## 6. Explicitly Unresolved

- Tenant/legal-entity applicability and phased e-invoicing dates.
- Selected ASP, commercial contract, environments, credentials, SLAs and exact API/status contract.
- Current PINT AE, mandatory-field, code-list and validation artefact versions.
- Tax invoice/credit-note fields, VAT treatments, calculation/rounding, evidence, adjustments and return-box mappings for the supported market scope.
- Accounting policy, chart design, functional/multi-currency policy, period close/reopen, opening balances, retention and filing responsibility.

These items are tracked in `DECISIONS_PENDING.md`; none blocks documentation drafting, but each blocks its dependent implementation or production activation.
