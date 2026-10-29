# UAE Banking and Payment Integration Source Register

| Property | Value |
|---|---|
| Document ID | REG-BANK-001 |
| Status | DATED RESEARCH BASELINE — LEGAL/PROVIDER REVIEW REQUIRED |
| Evidence cut-off | 29 October 2026 |
| Initial product posture | Employer/business ERP with manual statement import; not a bank or payment provider |

## 1. Purpose and Limits

This register records official sources used to bound P09 bank-data and payment-integration architecture. It does not determine that the ERP is licensed, exempt, accredited, connected to any bank, or permitted to provide an Open Finance or payment service. Exact activity, legal entity, customer type, data flow, provider role, consent and contractual route require qualified UAE regulatory/legal review.

Internal bank-account records, customer-supplied statement files and ledger reconciliation are distinct from regulated data sharing, account-information services, payment initiation, fund transfer, merchant acquiring and settlement. The product must not hold customer funds or represent itself as a financial institution under this baseline.

## 2. Source Register

| Source ID | Official source | Version/date | Class | Draft-safe use | Revalidation |
|---|---|---|---|---|---|
| UAE-BANK-001 | [CBUAE Open Finance Regulation](https://rulebook.centralbank.ae/en/rulebook/open-finance-regulation) | In force/phased framework; reviewed 2026-10-29 | `VERIFIED_PRIMARY` / `SPECIALIST_REQUIRED` | Establishes licensed/deemed-licensed roles for Data Sharing and Service Initiation, secure communication, consent, authentication, trust/API infrastructure and conformance. | Legal review must classify every proposed direct-data/payment activity. Pin operative regulation, phase notice, standard and participant requirements. |
| UAE-BANK-002 | [CBUAE Open Finance overview](https://centralbank.ae/en/our-operations/fintech-digital-transformation/open-finance/) | Reviewed 2026-10-29 | `OFFICIAL_GUIDANCE` | Official programme context: consent-driven access by accredited providers and staged roadmap. | Overview is not an API contract or authorization. Obtain Trust Framework/API Hub standards and certification evidence. |
| UAE-BANK-003 | [Retail Payment Services and Card Schemes Regulation](https://rulebook.centralbank.ae/en/rulebook/312-retail-payment-services-and-card-schemes-regulation) | Effective 2022-08-01; in force at cut-off | `VERIFIED_PRIMARY` / `SPECIALIST_REQUIRED` | Shows that payment initiation, payment-account information, fund transfer and other retail payment activities are regulated/licensed categories. | Determine whether proposed activity is provided by the ERP, bank or licensed provider; later law/regulation prevails. |
| UAE-BANK-004 | [CBUAE licensing register](https://centralbank.ae/en/licensing) | Dynamic; reviewed 2026-10-29 | `VERIFIED_PRIMARY` | Dated due-diligence source for a bank/payment-provider candidate and license category. | Capture a dated listing and verify exact legal entity/category at selection and release. Listing does not prove contracted capability. |
| UAE-BANK-005 | [CBUAE UAEFTS](https://centralbank.ae/en/our-operations/payments-and-settlements/uae-fund-transfer-system-uaefts/) | Reviewed 2026-10-29 | `VERIFIED_PRIMARY` / `OFFICIAL_GUIDANCE` | UAEFTS is the CBUAE-owned RTGS used by participating institutions with prescribed messages and confirmations. | ERP must not assume participant/direct access. Bank/provider contract defines customer-channel submission and evidence. |
| UAE-BANK-006 | [CBUAE IBAN](https://centralbank.ae/en/our-operations/payments-and-settlements/regulations-and-standards/iban/) | Dynamic; reviewed 2026-10-29 | `VERIFIED_PRIMARY` / `OFFICIAL_GUIDANCE` | Supports format/check-digit validation and distinguishes bank-issued IBAN from ERP account identity. | Validation is not proof of account ownership, existence or beneficiary authorization. Recheck current standard. |
| UAE-BANK-007 | [CBUAE Payments and Settlements regulations and standards](https://centralbank.ae/en/our-operations/payments-and-settlements/regulations-and-standards/) | Reviewed 2026-10-29 | `VERIFIED_PRIMARY` | Official discovery point for payment-system and provider regulation. | Recheck before selecting any payment/data connectivity route. |
| UAE-BANK-008 | [CBUAE Consumer Protection Standards](https://rulebook.centralbank.ae/en/rulebook/consumer-protection-standards) | N 1158/2021, in force | `VERIFIED_PRIMARY` / `SPECIALIST_REQUIRED` | Relevant evidence for licensed-financial-institution/provider obligations including disclosure, consent, data protection and authorized agents. | Applicability to ERP/provider/customer arrangement requires legal review; do not import provider obligations selectively as a compliance claim. |
| UAE-BANK-009 | [UAE Personal Data Protection overview](https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws) | Updated 2025-12-04; reviewed 2026-10-29 | `VERIFIED_PRIMARY` / `OFFICIAL_GUIDANCE` | Baseline for personal-data processing, confidentiality, rights and cross-border governance where bank data includes personal information. | Privacy/Legal must approve lawful basis, controller/processor roles, retention, residency/transfers and incident handling. |

## 3. Evidence Classes and Safe Conclusions

`VERIFIED_PRIMARY` is an official regulatory source; `OFFICIAL_GUIDANCE` explains but does not override law; `PROVIDER_CONTRACT_REQUIRED` means exact API/file/webhook/security/status behavior is not known; `SPECIALIST_REQUIRED` blocks activation.

- Manual files may be specified using an approved format contract without implying direct bank connectivity.
- Direct account-data access and payment initiation require a separate activity/licensing analysis and an approved bank or licensed-provider route.
- Provider listing, API success, upload, “processed” or local matching is not proof of final settlement.
- IBAN validation only verifies format/check digits; beneficiary ownership requires an approved verification method.
- Bank credentials/tokens/keys belong in the secrets system; statements and bank data are highly sensitive and private.
- The ERP must maintain provider-native evidence, consent/authorization where applicable, idempotent operations, uncertain outcomes and reconciliation.

## 4. Explicitly Unresolved

- Initial connectivity mode: manual file only, bank-hosted channel, licensed aggregator/Open Finance provider or other approved route.
- Legal/licensing role of the platform and contracted parties for data sharing or initiation.
- Supported banks/accounts/customer types, file/API/webhook schemas, authentication, consent, certificate and conformance requirements.
- Payment initiation scope, approvers/signatories, sanctions/fraud controls, limits, callbacks, cutoffs, fees, FX and settlement evidence.
- Data residency/transfer, retention, revocation/termination, portability, incident and provider-exit obligations.

## 5. Revalidation Record

Every integration task/release records source IDs, retrieved versions/checksums, legal activity classification, provider legal entity/license/category, exact contract/environment, supported institutions/accounts, consent/authentication/security, data fields/retention/location, status meanings, test/conformance evidence, reviewer, limitations, rollback/disable plan and review trigger. Revalidate on regulation/standard/provider/license/contract change, P09 exit and production release.
