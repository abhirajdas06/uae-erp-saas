# Data Protection, Privacy and Records Retention

| Property | Value |
|---|---|
| Document ID | QUAL-PRIV-001 |
| Status | PROPOSED FRAMEWORK — LEGAL REVIEW AND RETENTION PERIOD CONFIRMATION REQUIRED |
| Owner | Product Owner / Privacy reviewer |
| Governing decisions | ADR-018, ADR-019, ADR-004, ADR-017 |
| Related documents | `SECURITY_REQUIREMENTS.md`, `THREAT_MODEL.md`, `../01-architecture/DATA_MIGRATION_AND_IMPORT.md`, `../06-deployment/BACKUP_AND_RECOVERY.md`, `../00-product/UAE_REGULATORY_SOURCE_REGISTER.md` |

## 1. Purpose and Boundary

`../00-product/MASTER_PRODUCT_SPECIFICATION.md` section 12.5 requires applicable personal-data obligations to be identified, and section 17 requires the data lifecycle, retention obligations, deletion eligibility, legal holds and restoration to be defined. `SECURITY_REQUIREMENTS.md` SEC-009 and SEC-017 require data classification, minimization and secure disposal. No document owns the resulting privacy and retention framework. This document owns it.

This document owns the data classification scheme, the personal-data inventory contract, the processing-role model, data-subject-request handling, the retention class framework, deletion and disposal behavior, legal hold, residency constraints and the related tests. It does not own security controls, which remain with `SECURITY_REQUIREMENTS.md`; backup mechanics, which remain with `../06-deployment/BACKUP_AND_RECOVERY.md`; or audit-trail design, which remains with ADR-018 and `../03-modules/AUDIT_FOUNDATION.md`.

### 1.1 Regulatory verification status

This document asserts no legal conclusion and records no regulatory fact as verified.

| Item | Status |
|---|---|
| UAE Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data is the principal federal personal-data instrument | `VERIFIED_PRIMARY` — read on the official UAE legislation portal on 29 October 2026 and recorded as `UAE-PDP-001` in `../00-product/UAE_REGULATORY_SOURCE_REGISTER.md` section 6. Issued 20 September 2021, Official Gazette No. 712 supplement, effective 2 January 2022, state shown as Active. Data subject rights are Articles 13 to 19, breach reporting Article 9, the impact assessment Article 21, cross-border transfer Articles 22 and 23. The portal states the Arabic text prevails |
| Status and content of the PDPL Executive Regulations | `UNRESOLVED` — recorded as `UAE-PDP-004`. Article 28 of the Decree-Law requires the Council of Ministers to issue them within six months of promulgation, and Article 29 starts the controller and processor regularisation period of up to six months from the date they are issued. No Executive Regulation was listed among the related legislation on the official portal page for the Decree-Law when read on 29 October 2026, and secondary sources contradicted one another. Absence from that page is not proof of non-issuance. The named legal reviewer must establish the status before any applicability, rights-scope or timeline statement is relied upon, and no deadline may be asserted or implied meanwhile |
| Statutory retention periods for tax, accounting, VAT and real-estate records | `VERIFIED_PRIMARY` for the instrument wording, `SPECIALIST_REQUIRED` for applicability. On 29 October 2026 the official FTA-hosted texts were read at article level and recorded as `UAE-RET-001`–`UAE-RET-005` in `../00-product/UAE_REGULATORY_SOURCE_REGISTER.md` section 5: seven years following the Tax Period for corporate tax under Article 56 of Federal Decree-Law No. 47 of 2022; five years under Article 3(1) of Cabinet Decision No. 74 of 2023 with a different start point for non-taxable persons; seven years for real estate under that same Article 3(1); fifteen years for real-estate records under the VAT Executive Regulation; and four further years, or until a dispute is settled, on dispute, ongoing audit or notified audit. The FTA labels its English texts unofficial translations, so the Arabic is authoritative. What remains for `DEC-PRIV-005` is the applicability mapping per ERP record category, not the existence of the periods |
| Capital-asset retention claim | `CORRECTED` — the widely repeated ten-year capital-asset figure is the Capital Asset Scheme monitoring and adjustment period in the VAT Executive Regulation, not a retention period. Recorded as `UAE-RET-005`. It must not be configured as a retention period |
| Employment, payroll and wage-protection record obligations | `REQUIRES_VERIFICATION` via `../00-product/UAE_EMPLOYMENT_PAYROLL_WPS_SOURCE_REGISTER.md` |
| Free-zone data-protection regimes (for example financial free-zone frameworks) applying to a tenant or to hosting | `REQUIRES_VERIFICATION` under `DEC-PRIV-003` |
| Data residency obligation for UAE business records | `UNRESOLVED` — must be validated rather than assumed, per `MASTER_PRODUCT_SPECIFICATION.md` section 12.5 |

Every verified item must be recorded in `../00-product/UAE_REGULATORY_SOURCE_REGISTER.md` with source, source date, verification date and reviewer, per `AGENTS.md` section 11. No compliance, adequacy or certification claim may be made anywhere in this repository or in commercial material on the basis of this document.

## 2. Data Classification

| Class | Definition | Examples | Baseline handling |
|---|---|---|---|
| C0 — Public | Intended for publication | Marketing content, public pricing | No restriction |
| C1 — Internal | Non-sensitive operational data | Module catalogue, configuration defaults | Access-controlled |
| C2 — Tenant business | Tenant commercial data that is not personal | Items, price lists, stock, ledgers without personal content | Tenant-scoped, authorized, audited on export |
| C3 — Personal | Data identifying a natural person | Contact names, emails, phone numbers, user accounts | Minimized, purpose-bound, access-logged, retention-classed |
| C4 — Sensitive personal or financial | Personal data whose disclosure causes material harm | Salary, bank details, identity and residency documents, medical or disciplinary records, end-of-service entitlements | Least privilege, field-level restriction, mandatory disclosure audit, encryption at rest and in transit, never in logs |
| C5 — Secret | Authentication and cryptographic material | Passwords, tokens, provider credentials, signing keys | Never retained in recoverable form where avoidable, never logged, secret-backend only |

| ID | Requirement |
|---|---|
| PRIV-001 | Every model field holding C3 or above is classified in the owning module specification before implementation |
| PRIV-002 | Classification drives access control, logging, export eligibility, retention class and test-data policy; it is not documentation-only |
| PRIV-003 | A field of unknown classification is treated as C4 until classified |
| PRIV-004 | C4 and C5 data never appears in logs, traces, metrics, error reports, notifications, fixtures or support exports beyond a redacted reference |
| PRIV-005 | Reclassification downward requires privacy-reviewer approval with a recorded rationale |

## 3. Personal Data Inventory

A personal-data inventory is maintained as a living record. Each entry requires the following contract.

| Field | Requirement |
|---|---|
| Data element | The field or field group |
| Owning module | Single owning module specification |
| Classification | C3, C4 or C5 |
| Data subject category | Tenant user, employee, customer contact, supplier contact, candidate, or other |
| Purpose | The specific business purpose it serves |
| Lawful basis | Recorded once the legal reviewer confirms the applicable basis under the verified instrument |
| Source | Tenant entry, import, provider, or system-generated |
| Recipients | Internal roles and any external provider receiving it |
| Cross-border flow | Whether processing or storage leaves the UAE, and to where |
| Retention class | A class defined in section 6 |
| Deletion mechanism | Erase, anonymize, pseudonymize or retain-under-obligation |

| ID | Requirement |
|---|---|
| PRIV-010 | A module introducing a C3 or higher element adds it to the inventory in the same task; an unlisted personal-data element is a defect |
| PRIV-011 | Data minimization is applied at design time: an element without a named purpose is not collected |
| PRIV-012 | Free-text fields that predictably attract personal or sensitive content carry guidance and are classified accordingly |
| PRIV-013 | Identity, residency and immigration document handling requires explicit privacy review before implementation |

## 4. Processing Roles

| ID | Requirement |
|---|---|
| PRIV-020 | For tenant business and employee data, the tenant is the controlling party and the platform operator acts on the tenant's behalf; this allocation requires legal confirmation under `DEC-PRIV-002` and is not asserted as settled |
| PRIV-021 | For platform account, subscription, billing and usage data, the platform operator acts in its own right |
| PRIV-022 | The separation between provider-domain and tenant-domain data required by `MASTER_PRODUCT_SPECIFICATION.md` section 6.3 is also a privacy boundary and is never blurred for convenience |
| PRIV-023 | Every external provider receiving C3 or higher data requires a recorded purpose, a data-processing arrangement and a named approver before activation |
| PRIV-024 | A sub-processor list is maintained and is available to tenants; adding one is a recorded change, not a silent configuration update |
| PRIV-025 | Tenant-facing responsibilities and platform responsibilities are documented for customers before commercial launch |

## 5. Data Subject Requests

The rights the platform must be technically capable of serving are now identified: Articles 13 to 19 of `UAE-PDP-001` cover the right to receive information, the right to request transfer of personal data, correction and erasure, restriction of processing, objection to processing, and rights concerning automated processing. Their exact scope, exemptions and response timelines still depend on the Executive Regulations and specialist review under `DEC-PRIV-002`, and Article 29 means no regularisation deadline may be asserted. The workflow below is therefore the operational capability the platform provides, built to serve those articles without configuring a timeline.

| ID | Requirement |
|---|---|
| PRIV-030 | A request is received, identity-verified, logged, assigned an owner, tracked to a terminal outcome and evidenced |
| PRIV-031 | A request concerning tenant-held data is routed to the tenant as the controlling party; the platform provides the technical means and does not unilaterally alter tenant business records |
| PRIV-032 | Access and portability are served by the tenant data export capability in `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` section 9 |
| PRIV-033 | Correction is served through ordinary authorized maintenance with audit history, never by silent overwrite of a financial record |
| PRIV-034 | Erasure is evaluated against retention obligation, legal hold and financial-integrity constraints; a posted financial record is never deleted to satisfy a request, and the conflict is recorded and escalated |
| PRIV-035 | Where erasure is not permitted, anonymization or pseudonymization of non-statutory elements is the fallback, with the retained statutory elements named |
| PRIV-036 | Objection, restriction and consent-withdrawal handling is implemented once the applicable rights are confirmed; the capability is designed to accept them |
| PRIV-037 | Request handling spans primary data, backups, exports, report artifacts, notification evidence, audit trail and provider copies; a request closed without considering each is incomplete |
| PRIV-038 | Backups are not selectively edited; erasure applied to live data is accompanied by a documented backup-expiry path and a prohibition on restoring erased data without re-application |
| PRIV-039 | Response timelines are configurable and set from the verified instrument; no timeline is asserted here |

## 6. Retention Class Framework

Retention periods are configuration, not code, and every period requires a named specialist confirmation with a dated authoritative source. No period is asserted by this document.

| Class | Scope | Period source | Disposal action |
|---|---|---|---|
| RET-01 | Accounting and ledger records | `DEC-PRIV-005`, tax and accounting specialist | Retain, then review; financial records are never silently deleted |
| RET-02 | Tax and VAT records and filings | `DEC-PRIV-005`, tax specialist | Retain under obligation |
| RET-03 | Tax invoices, credit notes and e-invoicing submission evidence | `DEC-PRIV-005`, tax and e-invoicing specialists | Retain under obligation with submission evidence |
| RET-04 | Real-estate and capital-asset records, where a longer period applies | `DEC-PRIV-005`, tax specialist | Retain under obligation |
| RET-05 | Employment, payroll and wage-protection records | `DEC-PRIV-006`, employment specialist | Retain under obligation |
| RET-06 | Employee identity and residency documents | `DEC-PRIV-006`, employment and privacy reviewers | Minimum necessary retention, then erase |
| RET-07 | Banking details and payment instructions | `DEC-PRIV-005`, finance and privacy reviewers | Retain per obligation, then erase |
| RET-08 | Customer and supplier contact data | `DEC-PRIV-007`, privacy reviewer | Erase or anonymize when the relationship and obligations end |
| RET-09 | Audit trail records | `DEC-PRIV-008`, security and privacy reviewers | Append-only retention; disposal requires approval |
| RET-10 | Security, access and application logs | `DEC-PRIV-008`, security reviewer | Time-bounded retention, then automatic disposal |
| RET-11 | Notification records and delivery evidence | `DEC-NTF-004` | Time-bounded disposal |
| RET-12 | Report artifacts, exports and generated documents | `DEC-PRIV-009` | Short expiry with checksum record |
| RET-13 | Backups and recovery artifacts | `DEC-OPS-003` and `../06-deployment/BACKUP_AND_RECOVERY.md` | Expiry by schedule with verified destruction |
| RET-14 | Platform subscription, invoicing and payment records | `DEC-PRIV-010` | Retain per provider obligation |
| RET-15 | Terminated-tenant data | `DEC-PRIV-011` | Defined grace period, export window, then approved disposal |
| RET-16 | Support and diagnostic data | `DEC-PRIV-009` | Minimal retention, purpose-bound |

| ID | Requirement |
|---|---|
| PRIV-040 | Every data element carries exactly one retention class; an unclassed element is not eligible for automated disposal |
| PRIV-041 | Where two classes conflict, the longer statutory obligation governs the shared record and the conflict is recorded |
| PRIV-042 | Automated disposal runs as an authorized, logged, reversible-until-committed operation with a dry-run mode and a disposal report |
| PRIV-043 | Disposal of a financial, tax or audit record requires explicit human authorization; automation never disposes of RET-01 to RET-05 or RET-09 unattended |
| PRIV-044 | Disposal is evidenced: what was disposed of, under which class, by whose authority, when, and with what verification |
| PRIV-045 | A retention period change is a recorded, approved change and is never applied retroactively to already-disposed data |

## 6.1 Record Form and Accessibility Requirements

Derived from `UAE-VAT-007`, FTA Decision No. 4 of 2026, read on 29 October 2026. These are form and accessibility obligations rather than periods, and they constrain how this platform stores, exports and protects retained records. Applicability per tenant remains specialist work under `DEC-PRIV-005`.

| ID | Requirement |
|---|---|
| PRIV-046 | A retained record or its electronic copy is complete and identical to the original document, and remains clear and easily legible for the whole retention period |
| PRIV-047 | An electronic copy or photocopy of a document includes every page in the same order as the original; partial capture of a document is not an acceptable retained record |
| PRIV-048 | The platform can produce retained records to an authorized authority on request, including providing access to the system in which the records are held, within the tenant's own authorization and audit controls |
| PRIV-049 | Where retained records or the systems holding them are protected by encryption or passwords, an approved process exists for the tenant to supply the keys or credentials needed to enable authorized authority access. Encryption is therefore never a reason the tenant cannot meet a production request, and this requirement never authorizes the platform operator to disclose tenant data on its own initiative |
| PRIV-050 | Where the platform acts as the third party maintaining a tenant's records, the documentation and customer terms state plainly that the tenant remains legally responsible for maintaining those records and ensuring their safety, and the platform's obligations are contractual |
| PRIV-051 | Retention, export and disposal behavior preserves legibility, completeness and page order, so a disposal or format migration can never silently degrade a retained record into a non-conforming one |

## 7. Legal Hold

| ID | Requirement |
|---|---|
| PRIV-050 | A legal hold suspends disposal for named scope: a tenant, a data domain, a period or specific records |
| PRIV-051 | A hold is placed and released only by named authority, with reason, scope, start and expected review date recorded |
| PRIV-052 | A hold overrides automated disposal and erasure in every path, including backups and provider copies, and is verified to do so |
| PRIV-053 | A data subject request intersecting a hold is recorded as restricted with the reason, not silently refused |
| PRIV-054 | Active holds are reviewed on a defined cadence; an indefinite unreviewed hold is an issue |

## 8. Residency, Transfer and Environment Flow

| ID | Requirement |
|---|---|
| PRIV-060 | Hosting region, data-at-rest location, backup location and every provider processing location are recorded per environment; residency is validated rather than assumed |
| PRIV-061 | A cross-border flow is documented with its destination, purpose, safeguard and approver before activation |
| PRIV-062 | A provider whose processing location is unknown is not activated for C3 or higher data |
| PRIV-063 | Production personal data is never copied into development, test, demonstration or training environments; `TEST_DATA_AND_FIXTURES.md` governs the permitted alternatives |
| PRIV-064 | Data flow between environments is one-directional from lower to higher trust for code and configuration only; any exception requires approval and a sanitization record |
| PRIV-065 | A support or diagnostic extract containing C3 or higher data is purpose-bound, time-bounded, audited and disposed of on a recorded schedule |

## 9. Breach and Incident Interaction

| ID | Requirement |
|---|---|
| PRIV-070 | A suspected personal-data breach follows `../06-deployment/INCIDENT_RESPONSE.md` with privacy-specific assessment of categories, volume, subjects and harm |
| PRIV-071 | Notification obligations, recipients and timelines are set from the verified instrument and the tenant arrangement; none is asserted here |
| PRIV-072 | Tenants are informed of a breach affecting their data under the documented customer commitment |
| PRIV-073 | Breach assessment evidence is retained under RET-09 |

## 10. Acceptance and Tests

| ID | Verification |
|---|---|
| PRIV-TST-001 | Every C3 or higher field in reviewed scope appears in the personal-data inventory with a complete contract |
| PRIV-TST-002 | C4 and C5 data is absent from logs, traces, metrics, error reports, notifications and fixtures |
| PRIV-TST-003 | Field-level restriction prevents unauthorized roles from reading C4 data through interface, API, report and export paths |
| PRIV-TST-004 | Access to and export of C4 data is audited as a disclosure |
| PRIV-TST-005 | Tenant export is complete, tenant-isolated and excludes other tenants and platform internals |
| PRIV-TST-006 | Erasure removes or anonymizes eligible data across primary data, artifacts, notification evidence and provider copies while preserving statutorily retained records |
| PRIV-TST-007 | Erasure never deletes a posted financial record, and the conflict is recorded and escalated |
| PRIV-TST-008 | Automated disposal honors retention class, dry-run, authorization and evidence requirements |
| PRIV-TST-009 | Automated disposal cannot dispose of RET-01 to RET-05 or RET-09 without human authorization |
| PRIV-TST-010 | A legal hold suspends disposal and erasure in every path, including restore |
| PRIV-TST-011 | Restoring a backup does not reintroduce erased or disposed data without re-application of the disposal |
| PRIV-TST-012 | Non-production environments contain no production personal data |
| PRIV-TST-013 | Residency and provider processing locations match the recorded configuration for each environment |
| PRIV-TST-014 | A data subject request workflow reaches a terminal state with retained evidence |

All scenarios are `NOT_RUN` until the owning phase implements the capability.

## 11. Pending Decisions

Two decisions in this area already exist in the register and are not restated here: `DEC-PRIV-001` owns employee and payroll data classification, lawful basis, notices, access, retention, transfer and deletion policy, and `DEC-DATA-002` owns the overall retention, deletion, legal-hold and tenant-level recovery policy. The entries below are additional decisions this framework requires; `DEC-PRIV-006` refines `DEC-PRIV-001` for the specific periods, and the retention classes in section 6 implement `DEC-DATA-002` rather than replacing it.

| ID | Decision required | Owner |
|---|---|---|
| DEC-PRIV-002 | Confirm the applicable personal-data instruments, the status of the PDPL Executive Regulations, the processing-role allocation and the lawful bases, with dated primary sources | Legal reviewer |
| DEC-PRIV-003 | Determine whether any free-zone data-protection regime applies to the platform or to target tenants | Legal reviewer |
| DEC-PRIV-004 | Approve the hosting region, data-at-rest location and residency position, and validate it against any applicable obligation | Product Owner / Legal reviewer |
| DEC-PRIV-005 | Confirm, with dated authoritative sources, retention periods for accounting, tax, VAT, invoicing, real-estate, capital-asset and banking records | Tax and finance specialists |
| DEC-PRIV-006 | Confirm retention periods for employment, payroll, wage-protection and identity-document records | Employment specialist |
| DEC-PRIV-007 | Approve retention and anonymization policy for customer and supplier contact data | Product Owner / Privacy reviewer |
| DEC-PRIV-008 | Approve audit-trail and security-log retention periods and disposal authority | Security and privacy reviewers |
| DEC-PRIV-009 | Approve retention for report artifacts, exports and support extracts | Product Owner |
| DEC-PRIV-010 | Approve platform subscription and billing record retention | Product Owner |
| DEC-PRIV-011 | Approve the terminated-tenant grace period, export window and disposal authority | Product Owner |
| DEC-PRIV-012 | Approve the data-subject-request timelines and the customer-facing privacy commitment | Product Owner / Legal reviewer |

Until `DEC-PRIV-002` to `DEC-PRIV-012` are recorded, dependent implementation of automated disposal, erasure and residency enforcement is blocked. These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`.
