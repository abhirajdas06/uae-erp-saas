# Localization, Bilingual Interface and Formatting Standards

| Property | Value |
|---|---|
| Document ID | ARCH-L10N-001 |
| Status | APPROVED DOCUMENTATION BASELINE — LANGUAGE SCOPE AND DOCUMENT LANGUAGE APPROVAL REQUIRED |
| Owner | Product Architect / UX Lead |
| Governing decisions | ADR-007, ADR-013, ADR-012 |
| Related documents | `UI_DESIGN_SYSTEM.md`, `API_STANDARDS.md`, `PINT_AE_V1_0_4_IMPLEMENTATION_PROFILE.md`, `../05-quality/ACCESSIBILITY_AND_BROWSER_SUPPORT.md` |

## 1. Purpose and Boundary

`../00-product/MASTER_PRODUCT_SPECIFICATION.md` section 16.9 requires time zones, date and number formatting, currency formatting, Arabic and English interface requirements, right-to-left layout, multilingual business documents, character encoding and locale-aware search to receive explicit design decisions and acceptance criteria rather than being assumed complete. ADR-007 section 4.6 requires text to be localizable and prohibits claiming completed localization without validation. This document owns those definitions.

This document owns the language and locale model, translation workflow, directionality rules, formatting rules for dates, numbers and currency, bilingual business-document behavior, and the related acceptance criteria. It does not own statutory invoice content, which remains with `../03-modules/UAE_EINVOICING.md`, `../03-modules/UAE_VAT.md` and the PINT AE profile documents; nor monetary precision, which remains with ADR-013.

No claim of completed Arabic localization or right-to-left readiness may be made in any document, status record or release note until the acceptance criteria in section 10 have been executed and evidenced.

## 2. Language and Locale Model

| ID | Requirement |
|---|---|
| L10N-001 | English is the baseline development and source-string language; every user-facing string is externalized for translation from first implementation |
| L10N-002 | Arabic is a first-class planned interface language whose delivery scope, phase and acceptance criteria are set by `DEC-L10N-001`; it is never assumed delivered |
| L10N-003 | Interface language is resolved per user, with a tenant default and a platform default fallback; the resolved language is explicit in every rendered response |
| L10N-004 | Interface language, business-document language and tenant data language are independent concerns and are never conflated |
| L10N-005 | A tenant may store Arabic and English values for designated bilingual business fields; storage of a second language is additive and never overwrites the first |
| L10N-006 | Locale data uses recognized identifiers (`en`, `ar`, `en-AE`, `ar-AE`); custom locale codes are prohibited |
| L10N-007 | Adding a language beyond English and Arabic requires an approved decision and a translation-coverage gate; a partially translated language is not enabled for tenants |

## 3. Translation Workflow

| ID | Requirement |
|---|---|
| L10N-010 | Source strings use Django translation utilities; string concatenation to build sentences is prohibited |
| L10N-011 | Strings carry translator context for ambiguous terms, and plural forms use plural-aware calls rather than conditional English grammar |
| L10N-012 | Variable interpolation uses named placeholders so translators may reorder them |
| L10N-013 | Business, financial, tax and legal terminology is translated from the approved bilingual glossary in `../00-product/GLOSSARY.md`; ad hoc translation of regulated terms is prohibited |
| L10N-014 | Translation catalogues are version-controlled; a missing translation falls back to the baseline language visibly in non-production and safely in production |
| L10N-015 | Machine translation may seed a catalogue but may not be the final source for financial, tax, payroll, legal, contractual or security-notice strings without named human review |
| L10N-016 | A documentation or interface string asserting a regulatory position is translated only after the owning specialist approves both language versions |

## 4. Directionality

| ID | Requirement |
|---|---|
| L10N-020 | The document element declares `lang` and `dir` from the resolved language on every response, including fragment responses that replace a directional region |
| L10N-021 | Layout, spacing, alignment and iconography use logical direction tokens; physical left/right values are prohibited where a logical equivalent exists |
| L10N-022 | Directional icons such as navigation chevrons, progress arrows and indentation mirror in right-to-left mode; brand marks, media and logos do not mirror |
| L10N-023 | Mixed-direction content (an Arabic narrative containing a Latin reference, or an Arabic interface showing a Latin tax registration number) renders with correct isolation and never visually reorders an identifier |
| L10N-024 | Monetary amounts, account numbers, tax registration numbers, invoice numbers, IBANs and quantities remain unambiguous and non-reordered in both directions |
| L10N-025 | Right-to-left behavior is validated for the shell, every catalogue component, printable documents and every data table before an Arabic interface release |

## 5. Dates, Times and Calendars

| ID | Requirement |
|---|---|
| L10N-030 | Timestamps are stored in UTC and rendered in the tenant time zone; the platform default business time zone is `Asia/Dubai` |
| L10N-031 | A business date such as an invoice date, tax point, posting date or payroll period is a calendar date and is never shifted by time-zone conversion |
| L10N-032 | Interchange and API representations use ISO 8601 as required by `API_STANDARDS.md` section 12; display formatting is locale-derived and never parsed back as input |
| L10N-033 | The Gregorian calendar is authoritative for all financial, tax, payroll and statutory records |
| L10N-034 | Hijri date display, where offered, is presentation-only, labelled as such, and never used as the authoritative value of a financial or statutory record; its scope is set by `DEC-L10N-003` |
| L10N-035 | Arabic-language interfaces display Western Arabic numerals in financial figures unless `DEC-L10N-002` approves Eastern Arabic numeral presentation with a defined export behavior |
| L10N-036 | Week start, weekend definition and working days are tenant-configurable; the UAE default weekend is Saturday and Sunday and is confirmed per tenant rather than assumed |

## 6. Numbers, Currency and Quantities

| ID | Requirement |
|---|---|
| L10N-040 | Monetary precision, rounding and currency behavior follow ADR-013; localization governs presentation only and never alters a stored or computed value |
| L10N-041 | The currency symbol or code, its position, the decimal separator, the group separator and the negative-value presentation are locale-derived and consistent across interface, export and printed document |
| L10N-042 | `AED` is the platform default presentation currency; a tenant base currency and any foreign-currency presentation are explicit configuration, never inferred |
| L10N-043 | Number input accepts locale-plausible entry, normalizes to a canonical decimal before validation, and rejects ambiguous input rather than guessing a separator convention |
| L10N-044 | Exported numeric data is machine-parseable with a declared decimal convention and encoding; a localized display string is never written into a numeric export column |
| L10N-045 | Quantities, unit codes and unit-of-measure names are translated for display while the stored unit code remains canonical |

## 7. Encoding, Search and Sorting

| ID | Requirement |
|---|---|
| L10N-050 | UTF-8 is used end to end across database, application, templates, API, files and email; database collation supports Arabic text without data loss |
| L10N-051 | File exports declare encoding explicitly, and a format consumed by external spreadsheet tools includes the agreed byte-order-mark behavior recorded in its format contract |
| L10N-052 | Filenames, attachments and generated documents support Arabic characters safely in storage, headers and downloads |
| L10N-053 | Search normalizes Arabic diacritics, hamza and alef variants, and `taa marbuta` so equivalent spellings match; normalization is documented and tested |
| L10N-054 | Sorting is locale-aware, and a mixed Arabic and Latin list has a deterministic, documented order |
| L10N-055 | Identifier, code and reference fields are validated against an explicit allowed character set rather than accepting arbitrary multilingual input |

## 8. Bilingual Business Documents

| ID | Requirement |
|---|---|
| L10N-060 | A business document template declares its language behavior: baseline-language only, tenant-language only, or bilingual side-by-side presentation |
| L10N-061 | Statutory and mandatory document content required by UAE tax or e-invoicing rules is governed by `../03-modules/UAE_VAT.md`, `../03-modules/UAE_EINVOICING.md` and the PINT AE profile documents; localization never adds, removes or reinterprets a mandatory field |
| L10N-062 | A tax invoice issued in Arabic, English or both renders identical authoritative amounts, tax treatment, identifiers and totals in every language version |
| L10N-063 | Legal entity name, trade licence name, address and tax registration identifiers are rendered from stored tenant data in the language in which they were recorded and are never machine-translated |
| L10N-064 | Document numbering is language-independent and governed by `DOCUMENT_NUMBERING_AND_SEQUENCES.md` |
| L10N-065 | A bilingual document declares font coverage for both scripts and remains legible and non-overlapping when rendered to PDF or print |
| L10N-066 | Structured e-invoicing payloads carry the language-tagged content the approved profile requires and are never populated from a display-formatted string |

## 9. Notifications and Outbound Communication

| ID | Requirement |
|---|---|
| L10N-070 | Outbound notification language resolves from the recipient preference, then the tenant default, then the platform default, as specified in `NOTIFICATIONS_AND_COMMUNICATIONS.md` |
| L10N-071 | Notification subject, body, attachment name and embedded business values are consistently localized within one message; mixed-language assembly of one sentence is prohibited |
| L10N-072 | Security, authentication, billing and regulatory notices require reviewed translations before release in a given language |

## 10. Acceptance and Tests

| ID | Verification |
|---|---|
| L10N-TST-001 | No user-facing string is hardcoded outside the translation mechanism in reviewed scope |
| L10N-TST-002 | Language resolution across user, tenant and platform default produces the correct `lang` and `dir` on full pages and fragments |
| L10N-TST-003 | Right-to-left rendering is correct for the shell, every catalogue component, data tables and printable documents |
| L10N-TST-004 | Mixed-direction identifiers, amounts, IBANs and tax registration numbers are not visually reordered |
| L10N-TST-005 | Business dates do not shift across time zones; timestamps render correctly in the tenant time zone |
| L10N-TST-006 | Locale-plausible numeric input normalizes correctly and ambiguous input is rejected |
| L10N-TST-007 | Monetary presentation differs by locale while stored and computed values remain identical |
| L10N-TST-008 | Arabic text round-trips without loss through database, API, export, filename, email and generated document |
| L10N-TST-009 | Arabic search normalization and locale-aware sorting behave as documented |
| L10N-TST-010 | A bilingual tax invoice presents identical authoritative amounts, identifiers and tax treatment in both languages |
| L10N-TST-011 | Missing translations fall back safely without leaking a translation key to an end user in production |
| L10N-TST-012 | Numeric exports remain machine-parseable with the declared encoding and decimal convention |

All scenarios are `NOT_RUN` until the owning phase implements the capability. Passing `L10N-TST-003`, `L10N-TST-004`, `L10N-TST-008` and `L10N-TST-010` is a precondition for any statement that Arabic or right-to-left support is delivered.

## 11. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-L10N-001 | Approve the Arabic interface delivery scope, owning phase and release gate | Product Owner |
| DEC-L10N-002 | Approve numeral presentation in Arabic interfaces and the corresponding export behavior | Product Owner / Finance |
| DEC-L10N-003 | Approve whether Hijri date display is offered and where it may appear | Product Owner |
| DEC-L10N-004 | Approve the bilingual presentation rule for each statutory document family | Product Owner / Tax specialist |
| DEC-L10N-005 | Approve the translation review authority for financial, tax, payroll, legal and security strings | Product Owner |

These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`. No approval is recorded by this document.
