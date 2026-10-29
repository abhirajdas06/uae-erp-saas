# UAE Employment, Payroll and WPS Regulatory Source Register

| Property | Value |
|---|---|
| Document ID | REG-HR-001 |
| Status | DATED RESEARCH BASELINE — SPECIALIST REVIEW REQUIRED |
| Evidence cut-off | 29 October 2026 |
| Initial candidate scope | MoHRE-regulated UAE private-sector employers only |
| Owner | Product / HR / Payroll / UAE Regulatory Research |

## 1. Purpose and Limits

This register records official sources used to draft P07. It is not employment, payroll, pension, privacy or WPS advice and does not establish product compliance. English publications marked as unofficial translations cannot replace operative Arabic text or qualified UAE legal review.

Government employment, domestic workers, DIFC/ADGM and other free-zone regimes, local pension funds, military/security employment, household employers and jurisdiction-specific rules are outside the initial candidate scope until separately researched and approved. Employer, establishment, employee category, nationality, work pattern, contract, permit, pension regime and effective date must select an approved ruleset; “UAE payroll” is not one universal configuration.

## 2. Evidence Classes

`VERIFIED_PRIMARY` means official legislation/regulator material was reviewed. `OFFICIAL_GUIDANCE` supports interpretation but cannot override legislation. `TECHNICAL_CONTRACT_REQUIRED` means an exact bank/agent/API/file contract is still needed. `SPECIALIST_REQUIRED` blocks production behavior pending qualified review. `SUPERSEDED` is historical only.

## 3. Employment Sources

| Source ID | Official source | Version/date | Class | Draft-safe facts / use | Revalidation |
|---|---|---|---|---|---|
| UAE-EMP-001 | [MoHRE Federal Decree-Law No. 33 of 2021 and amendments](https://www.mohre.gov.ae/assets/download/b3a8d3c1/Federal%20Decree-Law%20No.%2033%20of%202021%20Regarding%20the%20Regulation%20of%20Employment%20Relationship%20and%20its%20amendments.pdf.aspx) | Current MoHRE publication reviewed 2026-10-29 | `VERIFIED_PRIMARY` / `SPECIALIST_REQUIRED` | Governing source for in-scope private-sector employment concepts including contracts, work patterns, wages, deductions, working time, leave, termination and end-of-service. | Retrieve/checksum operative Arabic and current amendments before policy activation. Do not use the repealed Federal Law No. 8 of 1980. |
| UAE-EMP-002 | [Cabinet Resolution No. 1 of 2022 implementing Federal Decree-Law No. 33](https://www.mohre.gov.ae/assets/download/ff353ce9/Cabinet%20Resolution%20_Executive%20Regulations%20Decree-Law%20No.%2033.pdf.aspx) | Current MoHRE publication reviewed 2026-10-29 | `VERIFIED_PRIMARY` / `SPECIALIST_REQUIRED` | Executive-regulation baseline for classifications, work models and detailed employment controls. English copy states it is not an official translation. | Operative Arabic and later resolutions/circulars prevail. |
| UAE-EMP-003 | [UAE Government private-sector employment laws page](https://u.ae/en/information-and-services/jobs/employment-in-the-private-sector/employment-laws-and-regulations-in-the-private-sector) | Updated 2026-01-15 | `OFFICIAL_GUIDANCE` | Confirms Law 33/2021 and amendments as the private-sector baseline and identifies excluded categories. | Recheck applicability and linked legislation at every P07 ruleset approval/release. |
| UAE-EMP-004 | [UAE Government types of leave and entitlements](https://u.ae/en/information-and-services/jobs/employment-in-the-private-sector/types-of-leaves-and-entitlements-in-the-private-sector) | Reviewed 2026-10-29 | `OFFICIAL_GUIDANCE` | Authoritative discovery/guidance for private-sector leave categories. | Exact eligibility, duration, pay, accrual, evidence and interaction rules require the operative law and specialist-reviewed test cases. |
| UAE-EMP-005 | [UAE Government employment process](https://u.ae/en/information-and-services/jobs/employment-in-the-private-sector/job-offers-and-work-permits-and-contracts/expatriates-employment-in-private-sector) | Updated 2026-06-02 | `OFFICIAL_GUIDANCE` | Supports contract/offer/work-permit lifecycle analysis; government registration remains an external process. | Exact MoHRE service/API contract is not approved; ERP records cannot claim permit status without evidence. |
| UAE-EMP-006 | [MoHRE New Employers Awareness Guide](https://www.mohre.gov.ae/assets/download/c52cad71/Awareness%20Guide%20for%20New%20Employers%20Companies%20-%20EN.pdf.aspx) | 2026 publication | `OFFICIAL_GUIDANCE` | Practical guidance on employer obligations, wage payment, end-of-service and record handling. | Guidance does not replace legislation; archive version/checksum before use. |

## 4. Wage Protection System Sources

| Source ID | Official source | Version/date | Class | Draft-safe facts / use | Revalidation |
|---|---|---|---|---|---|
| UAE-WPS-001 | [MoHRE Ministerial Resolution No. 598 of 2022 concerning WPS and amendment](https://mohre.gov.ae/assets/download/d0af668c/Ministerial%20Resolution%20No.%20598%20of%202022%20Regarding%20the%20Wages%20Protection%20System%20and%20Its%20Amendment.pdf.aspx) | Current MoHRE publication reviewed 2026-10-29 | `VERIFIED_PRIMARY` / `SPECIALIST_REQUIRED` | Establishes due-date/payment and WPS compliance framework for applicable establishments, with exceptions/actions requiring exact applicability review. English copy states it is not an official translation. | Retrieve operative Arabic/current amendment chain; do not hardcode reminder/penalty timing without approved policy. |
| UAE-WPS-002 | [UAE Government payment of wages](https://u.ae/en/information-and-services/jobs/employment-in-the-private-sector/payment-of-wages) | Updated 2026-03-30 | `OFFICIAL_GUIDANCE` | Official guidance describes wage due date, WPS payment route, late-payment concept and categories shown as excluded. | Revalidate against current resolution and employer/worker facts; guidance is not a technical submission contract. |
| UAE-WPS-003 | [Central Bank UAEWPS](https://centralbank.ae/en/our-operations/payments-and-settlements/uae-wages-protection-system-uaewps) | Reviewed 2026-10-29 | `VERIFIED_PRIMARY` / `OFFICIAL_GUIDANCE` | CBUAE owns/operates UAEWPS and describes employer-to-agent flows, fund security, employee-level balances, confirmations/disbursements/refunds and regulator feeds. | Exact SIF/response/agent integration is `TECHNICAL_CONTRACT_REQUIRED`; obtain current bank/agent specifications and certification evidence. |
| UAE-WPS-004 | [CBUAE WPS rulebook section](https://rulebook.centralbank.ae/en/entiresection/3526) | Dynamic; reviewed 2026-10-29 | `VERIFIED_PRIMARY` | Confirms regulated WPS service context and Salary Information File terminology for licensed persons. | Product is an employer-side preparer, not a licensed WPS agent. Validate current agent contract and rules before export/integration. |

## 5. Pension, Social Security and Data Protection Sources

| Source ID | Official source | Version/date | Class | Draft-safe facts / use | Revalidation |
|---|---|---|---|---|---|
| UAE-PEN-001 | [GPSSA registration requirement](https://www.gpssa.gov.ae/pages/en/help/faq/registration-gpssa-mandatory) | Updated 2024-10-07; reviewed 2026-10-29 | `OFFICIAL_GUIDANCE` / `SPECIALIST_REQUIRED` | GPSSA states registration/contributions are mandatory for applicable Emirati employees in government/private sectors. | Determine applicable pension authority and law cohort per employee; do not assume GPSSA covers all UAE nationals. |
| UAE-PEN-002 | [GPSSA summary of Federal Law No. 57 of 2023](https://gpssa.gov.ae/pages/en/media-center/news/gpssa-reviews-most-prominent-features-federal-law-no-57-2023) | Reviewed 2026-10-29 | `OFFICIAL_GUIDANCE` / `SPECIALIST_REQUIRED` | Demonstrates materially different pension-law cohorts, applicability dates and contribution parameters. | Exact contribution rules require current law, authority and employee-specific cohort approval. No rate is hardcoded from this summary. |
| UAE-DATA-001 | [UAE Government data-protection laws](https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws) | Updated 2025-12-04 | `VERIFIED_PRIMARY` / `OFFICIAL_GUIDANCE` | Identifies Federal Decree-Law No. 45 of 2021 and processing/security/data-subject/cross-border governance relevant to employee data. | Determine applicability, lawful basis, notices, rights, transfers, retention and free-zone regimes with Privacy/Legal review. |

## 6. Draft-Safe Architecture Conclusions

- HRMS owns employee/employment/leave history; authentication owns login identity; Payroll owns versioned payroll inputs/results; Accounting owns postings; Banking/WPS agents own settlement evidence.
- Rules must be effective-dated by jurisdiction, employer establishment, worker category/nationality/work pattern and governing scheme.
- Finalized payroll is immutable; corrections append versioned adjustment/off-cycle/reversal records.
- A payslip, payment file, bank upload or WPS preparation status is not proof of wage settlement or regulator acceptance.
- WPS uses a provider/agent boundary with exact current SIF and response contracts, idempotency, approval, encryption, reconciliation and restricted access.
- Employee identity, contract, salary, bank, pension, leave/medical evidence and payroll data require field-level purpose/role controls, minimization, private files, audited access and category-specific retention.

## 7. Explicitly Unresolved

- Supported employer jurisdictions/categories and employee/work patterns; free-zone and government scope.
- Exact employment/leave/overtime/deduction/end-of-service rules and effective dates.
- WPS applicability/exclusions, current SIF/response contract, agent/bank, submission method and acceptance meanings.
- UAE national pension authority/law cohort, contribution bases/rates/ceilings and reporting.
- Emiratisation/Nafis, unemployment insurance, work-permit and other integrations.
- Payroll components, calendars, proration, rounding, retroactivity, corrections, final settlement and accounting mappings.
- Employee-data lawful basis, notices, access, retention, legal hold, transfer/residency and deletion handling.

These decisions block dependent production implementation, not provider-neutral documentation or interfaces.

## 8. Revalidation Record

Every regulated task/release records source IDs, retrieved artefact/checksum, operative language, effective date, applicability facts, specialist reviewer, approved ruleset/version, fixtures, disabled exclusions, change impact, rollback/disable plan and next-review trigger. Revalidate on legislation/resolution/circular change, employer/employee category change, provider/agent change, P07 exit and every production release.
