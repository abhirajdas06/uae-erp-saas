# Test Data, Fixtures and Demonstration Datasets

| Property | Value |
|---|---|
| Document ID | QUAL-TESTDATA-001 |
| Status | PROPOSED STANDARD — DEMONSTRATION DATASET APPROVAL REQUIRED |
| Owner | QA / Test Engineer |
| Governing decisions | ADR-015, ADR-004, ADR-018 |
| Related documents | `TESTING_STRATEGY.md`, `DATA_PROTECTION_AND_RETENTION.md`, `SECURITY_REQUIREMENTS.md`, `../01-architecture/DATA_MIGRATION_AND_IMPORT.md` |

## 1. Purpose and Boundary

`TESTING_STRATEGY.md` requires extensive automated testing and `SECURITY_REQUIREMENTS.md` SEC-009 prohibits copying sensitive data into test fixtures, but no document defines how test data is constructed, where it lives, how tenant-isolation tests obtain multiple tenants, or how a demonstration dataset is produced. Without this, test suites tend to accumulate ad hoc fixtures that silently weaken isolation and financial-integrity testing. This document owns that definition.

This document owns fixture construction rules, the mandatory multi-tenant baseline, financial and regulated-data rules, the demonstration and sales dataset, performance datasets, prohibited practices and the related verification. It does not own test levels or coverage targets, which remain with `TESTING_STRATEGY.md`, nor retention and classification policy, which remains with `DATA_PROTECTION_AND_RETENTION.md`.

## 2. Absolute Prohibitions

| ID | Prohibition |
|---|---|
| TD-001 | Production tenant data is never copied into a development, test, continuous-integration, demonstration or training environment, in whole or in part |
| TD-002 | Real personal data of any identifiable person is never used as test data, including the data of staff, founders, friends or the development team |
| TD-003 | Real bank account numbers, IBANs, card data, identity-document numbers, residency-permit numbers or tax registration numbers of real entities are never used |
| TD-004 | Real credentials, provider API keys, tokens or signing material are never committed as fixtures, including expired or sandbox-labelled values that have not been verified as disposable test credentials |
| TD-005 | A production database dump is never restored into a lower environment, even temporarily and even when access-restricted |
| TD-006 | Anonymization of a production extract is not an approved route to test data; synthetic generation is the required approach |
| TD-007 | Test fixtures never disable tenant scoping, authorization, entitlement or validation to simplify setup |

An exception to `TD-001` to `TD-006` is not available through developer convenience, urgency or a support investigation. A support investigation uses the purpose-bound, audited access path in `DATA_PROTECTION_AND_RETENTION.md` PRIV-065.

## 3. Synthetic Data Principles

| ID | Requirement |
|---|---|
| TD-010 | All test data is synthetic and deterministically generated from recorded seeds so a failure is reproducible |
| TD-011 | Generated values are obviously fictional on inspection: reserved example domains, clearly invented entity names, and documented placeholder identifier formats |
| TD-012 | Generated identifiers that resemble regulated identifiers, such as tax registration numbers or IBANs, use documented invalid or reserved patterns that cannot match a real registration, while still exercising format validation |
| TD-013 | Arabic-script, mixed-direction, long-string, diacritic and special-character values are included in the standard generator set so localization defects surface early |
| TD-014 | Monetary generators produce boundary values: zero, smallest unit, rounding-sensitive thirds, large magnitudes, negative values where permitted, and multi-currency combinations |
| TD-015 | Date generators produce period boundaries, fiscal-year boundaries, closed periods, leap days, and time-zone-sensitive business dates |
| TD-016 | A fixture declares its intent; a fixture that silently encodes an assumption about business rules is a defect |
| TD-017 | Fixtures are constructed through application services or documented factories, not by direct database insertion, so they remain valid as rules evolve |

## 4. Mandatory Multi-Tenant Baseline

Tenant isolation is the platform's foundational requirement, so the test baseline makes cross-tenant defects detectable by default.

| ID | Requirement |
|---|---|
| TD-020 | The shared test baseline always contains at least two fully populated tenants with overlapping business data, plus a third minimally configured tenant |
| TD-021 | Overlapping data is deliberate: the tenants share customer names, item codes, document numbers, email addresses and amounts, so a missing tenant filter produces a visible wrong result rather than an empty one |
| TD-022 | Each baseline tenant has a distinct entitlement profile: one broadly entitled, one narrowly entitled, and one with an expired or suspended subscription |
| TD-023 | Each baseline tenant has users at several authority levels, including a tenant administrator, a limited operator, an approver, a read-only auditor and a deactivated user |
| TD-024 | A platform-administration identity exists separately and is never a member of a tenant |
| TD-025 | A test asserting an authorized positive outcome must also assert the corresponding cross-tenant negative outcome where the data is tenant-owned |
| TD-026 | No fixture, factory default or helper permits a record to be created without a tenant where the model is tenant-owned |

## 5. Financial and Regulated Fixtures

| ID | Requirement |
|---|---|
| TD-030 | A financial fixture set includes a complete, balanced chart of accounts and a balanced opening position; an unbalanced financial baseline is a defect |
| TD-031 | Posted, draft, cancelled and reversed states are all represented so immutability rules under ADR-011 are exercised |
| TD-032 | Open and closed periods are both represented so period-close enforcement is exercised |
| TD-033 | VAT fixtures cover each tax treatment the owning module declares, including zero-rated, exempt, out-of-scope and reverse-charge cases, without asserting a tax position not confirmed by the owning specification |
| TD-034 | E-invoicing fixtures use clearly synthetic payloads and never transmit to a real provider endpoint; provider interaction is stubbed by default |
| TD-035 | Payroll fixtures exercise salary structures, pro-rata periods, end-of-service scenarios and wage-protection file generation using synthetic employees only |
| TD-036 | Banking fixtures use documented invalid IBAN patterns and never reference a real financial institution account |
| TD-037 | A regulated-output fixture, such as a tax return figure or a wage-protection file, is a format and arithmetic test; it is never evidence of regulatory conformance |

## 6. Fixture Organization and Lifecycle

| ID | Requirement |
|---|---|
| TD-040 | Shared factories live in a common test support location; domain-specific factories live with their owning app |
| TD-041 | A test creates the minimum data it needs through factories; large shared fixture files that many tests depend on implicitly are prohibited |
| TD-042 | Tests are isolated and order-independent: no test depends on data created by another, per `../01-architecture/API_STANDARDS.md` section 23.7 |
| TD-043 | Database state is rolled back or recreated between tests; a test that leaves residue is a defect |
| TD-044 | External providers are stubbed at the adapter boundary with recorded contract fixtures; no test performs a live external call by default |
| TD-045 | A contract fixture captured from a provider sandbox records capture date, endpoint, contract version and redaction applied, and contains no credential |
| TD-046 | Time is injected rather than read ambiently so date-sensitive behavior is deterministic |
| TD-047 | Factories and fixtures are reviewed when a business rule changes; a stale fixture that masks a rule change is a defect |

## 7. Demonstration and Training Dataset

| ID | Requirement |
|---|---|
| TD-050 | A demonstration dataset is a deliberate, approved product artifact, generated by a documented, repeatable seeding command |
| TD-051 | It represents a plausible UAE business with a realistic volume of master data, trading history, bilingual content and multi-module activity, while remaining entirely synthetic |
| TD-052 | It never contains a real customer, prospect, employee, supplier or bank account |
| TD-053 | Demonstration tenants are visibly marked as demonstration data in the interface and are excluded from production reporting, billing and regulatory submission |
| TD-054 | A demonstration environment is reset on a schedule and is never used to hold real customer data entered during a trial without an explicit migration to a real tenant |
| TD-055 | Any figure used in sales or marketing material drawn from the demonstration dataset is labelled as illustrative |

## 8. Performance and Volume Datasets

| ID | Requirement |
|---|---|
| TD-060 | Performance datasets are generated to declared volumes per entity, with the generator and parameters recorded so a run is reproducible |
| TD-061 | Volume targets derive from `PERFORMANCE_REQUIREMENTS.md` and `../06-deployment/CAPACITY_AND_PERFORMANCE.md`; an unstated volume assumption invalidates the result |
| TD-062 | Performance datasets include realistic tenant multiplicity and skew, including one large tenant among many small ones |
| TD-063 | A performance result records dataset identity, size, environment and configuration; a result without them is not comparable evidence |
| TD-064 | Performance datasets are disposed of after use per their retention class |

## 9. Secrets in Test Configuration

| ID | Requirement |
|---|---|
| TD-070 | Test configuration uses clearly fictional placeholder values that cannot authenticate anywhere |
| TD-071 | Placeholder secrets are structurally distinguishable from real ones and are allowlisted explicitly in the secret scanner baseline with a recorded reason |
| TD-072 | The secret scanner runs over fixtures and test configuration, not only over application code |
| TD-073 | A disposable sandbox credential, where one is genuinely required, is supplied by environment variable at run time and never committed |
| TD-074 | A test that cannot run without a real credential is marked and excluded from the default suite, with its manual execution requirements recorded |

## 10. Verification

| ID | Verification |
|---|---|
| TD-TST-001 | The shared baseline provides the required multi-tenant, multi-entitlement, multi-authority fixture set |
| TD-TST-002 | Overlapping cross-tenant data exists so a missing tenant filter yields a wrong result rather than an empty one |
| TD-TST-003 | No tenant-owned fixture can be created without a tenant |
| TD-TST-004 | The financial baseline balances, and posted, cancelled, reversed, open-period and closed-period states are present |
| TD-TST-005 | Arabic, mixed-direction and boundary string values are present in the standard generator set |
| TD-TST-006 | Monetary and date boundary generators produce the declared cases |
| TD-TST-007 | Tests pass in randomized order with no inter-test data dependency |
| TD-TST-008 | No test performs a live external provider call in the default suite |
| TD-TST-009 | The secret scanner finds no unexplained credential-like value in fixtures or test configuration |
| TD-TST-010 | The demonstration dataset seeds reproducibly and is marked as demonstration data |
| TD-TST-011 | No identifier in the fixture set matches a real registration or account format that could belong to a live entity |
| TD-TST-012 | Non-production environments contain no production data, verified as part of `DATA_PROTECTION_AND_RETENTION.md` PRIV-TST-012 |

All scenarios are `NOT_RUN` until the owning phase implements the test suite.

## 11. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-TD-001 | Approve the demonstration dataset scope, business profile and reset cadence | Product Owner |
| DEC-TD-002 | Approve the placeholder identifier formats for tax registration numbers, IBANs and identity documents, confirming they cannot collide with real registrations | Tax specialist / Finance |
| DEC-TD-003 | Approve the performance dataset volumes and tenant skew profile | Product Owner / DevOps |
| DEC-TD-004 | Approve whether any provider sandbox is used in automated testing, and the credential-handling model if so | Product Owner / DevOps |

These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`.
