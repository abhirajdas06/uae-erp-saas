# P04 — UAE E-Invoicing Phase Specification

| Property | Value |
|---|---|
| Document ID | P04-SPEC-001 |
| Status | READY FOR REVIEW |
| Phase | P04 |
| Regulatory cut-off | 29 October 2026 |
| Implementation authorization | NOT GRANTED |

## 1. Objective and Authority

Deliver a secure, tenant-safe and provider-bounded UAE e-invoicing capability for explicitly approved document types and applicability segments. This phase implements `EIN-001`–`EIN-005`, `INT-001`–`INT-002`, and applicable security/reliability requirements under ADR-004, ADR-010, ADR-012, ADR-013, ADR-017–020; [REG-SRC-001](../../00-product/UAE_REGULATORY_SOURCE_REGISTER.md); [ARCH-PINT-AE-002](../../01-architecture/PINT_AE_V1_0_4_IMPLEMENTATION_PROFILE.md); [ARCH-PINT-AE-MAP-001](../../01-architecture/PINT_AE_V1_0_4_SEMANTIC_UBL_MAPPING_REGISTER.md); and [ARCH-EINV-CONTRACT-001](../../01-architecture/UAE_EINVOICING_PROVIDER_CONTRACT.md). The `2025-Q2` profile is historical evidence only.

The phase does not certify compliance. Legislation, customer applicability, provider accreditation/contract, schemas and production behavior require current evidence and qualified review.

## 2. Entry Gates

- P03 immutable invoice/credit-note snapshot, numbering and correction contracts are approved and implemented for the supported scope.
- P01 tenant/IAM/audit and P02 entitlement contracts are verified.
- Applicable regulatory source artefacts are retrieved, versioned and reviewed; unresolved flows are disabled.
- Product Owner approves bounded P04 scope (`APPR-P04-001`).
- Provider-dependent coding waits for provider approval (`APPR-P04-002`); provider-neutral interfaces/tests may proceed separately.

## 3. Included Scope

- Effective-dated applicability and document-eligibility rules.
- Canonical immutable e-invoice/e-credit-note preparation and preflight validation.
- Version-pinned semantic-term mapping, UBL serialization, code lists, shared PINT and AE-specific Schematron validation for each approved PINT AE transaction profile.
- UAE TDD and Message Level Status evidence under the selected ASP contract; the ERP does not impersonate the ASP or FTA.
- Approved ASP onboarding and versioned adapter.
- Durable submission/attempt/idempotency workflow and transactional outbox.
- Provider-native evidence plus controlled internal statuses.
- Authenticated, replay-safe callbacks and polling/reconciliation.
- Rejection/correction linkage without rewriting issued source records.
- Secure credentials, environments, payload/evidence retention and access.
- Operator UI, exception queues, reporting, monitoring and runbooks.
- Sandbox/conformance, isolation, security, recovery and regulatory-readiness evidence.

## 4. Excluded Scope

- Choosing a provider in this document; direct-government API assumptions; B2C, Self-Billing or other excluded/unapproved transaction categories unless separately approved.
- A general UAE e-way-bill workflow. No authoritative requirement was identified at the evidence cut-off; airway bills, despatch/delivery references and customs/transport documents remain distinct.
- Creating or changing invoices, VAT policy or ledger entries in `e_invoicing`.
- Treating PDFs, email delivery, HTTP success, provider receipt or worker success as regulatory acceptance.
- Automatic provider switching, production submission, accreditation/compliance claims, or unsupported filing/reporting.
- Hardcoded deadlines, mandatory fields, status mappings or retention periods outside an approved ruleset.

## 5. Domain and Data Contract

`e_invoicing` owns `RegulatoryRuleSet`, `ProviderConfigurationReference`, `ElectronicDocumentSnapshot`, `SubmissionOperation`, `SubmissionAttempt`, `ProviderEvidence`, `CallbackReceipt`, `StatusMappingVersion` and `ReconciliationCase`. All tenant-owned records carry explicit tenant/legal-entity ownership and same-tenant constraints. Provider secrets remain in the approved secret store.

Every snapshot references the immutable P03 source/version/hash and records regulatory, PINT AE transaction profile/resource checksums, semantic mapping, UBL syntax, code-list, Schematron, adapter and status-mapping versions. Attempts append evidence. Ordinary workflows cannot rewrite or delete a submitted snapshot, attempt, provider reference or terminal evidence.

## 6. Core Workflows

1. **Qualify:** resolve tenant/legal entity, transaction category, effective date and approved ruleset; unsupported/ambiguous applicability fails closed.
2. **Prepare:** obtain immutable source snapshot, validate mandatory/conditional data, create canonical snapshot/hash and outbox intent atomically.
3. **Submit:** authorized task resolves provider account/environment, maps and signs/authenticates, records attempt, and applies evidence-based status.
4. **Reconcile:** timeout/crash/ambiguous response becomes uncertain; inquiry or operator workflow resolves before resubmission.
5. **Callback:** authenticate/replay-check, route through trusted provider account, deduplicate, append evidence and apply valid transition.
6. **Correct:** source domain issues approved credit/correction; a distinct linked electronic-document operation is prepared. Original history remains.

## 7. Security, Isolation and Privacy

Permission and entitlement are both required. Preparation, submission, retry, reconcile, configuration and restricted-payload access are separate permissions. Enforce trusted tenant context across services, tasks, callbacks, admin, reports, caches, files and support tools; use approved RLS defenses. Unknown objects/accounts yield non-disclosing errors.

Secrets, tokens, certificates, full payloads, tax identifiers, addresses and invoice contents are prohibited in ordinary logs. Store only necessary payload/evidence, encrypted and access-controlled according to the approved retention policy. Test data is synthetic.

## 8. Reliability, Migration and Operations

Stable idempotency plus uniqueness and locking prevent duplicate operations. Retry classification is adapter-versioned; uncertain outcomes never use blind retry. Migrations preserve historical schema/adapter/status meaning and are tested clean-install, upgrade, rollback boundary and old/new overlap. Restore verification reconciles source hashes, snapshots, operations, attempts, references, statuses, callbacks, outbox and audit.

Monitor validation/rejection rate, latency, uncertain cases, backlog/age, callback failures/replay, duplicate conflicts, provider health/rate limit, credential/certificate expiry, schema deprecation and source-register review date.

## 9. Acceptance Criteria

| ID | Criterion |
|---|---|
| P04-AC-001 | Current authoritative sources, applicability, ruleset versions and review evidence are recorded |
| P04-AC-002 | Selected provider accreditation, contract, capability and environment are approved before dependent activation |
| P04-AC-003 | Only eligible immutable invoice/credit snapshots can be prepared |
| P04-AC-004 | Every supported transaction has complete reviewed mandatory/conditional semantic-to-UBL mapping and totals, and passes the pinned structural, shared PINT, AE-specific, code-list and provider-preflight layers |
| P04-AC-005 | Source and provider processing remain separate; provider processing cannot mutate issued financial meaning |
| P04-AC-006 | Submission is durable, idempotent, tenant/legal-entity scoped and linked to one source version |
| P04-AC-007 | Timeout/crash/ambiguous outcomes reconcile safely before retry |
| P04-AC-008 | Native and internal statuses/evidence remain distinct, versioned and historically readable |
| P04-AC-009 | Callbacks authenticate, resist replay, deduplicate/reorder safely and cannot forge tenant context |
| P04-AC-010 | Rejections and corrections are investigable, auditable and linked without overwriting history |
| P04-AC-011 | Permission, entitlement, isolation, RLS and support-access tests cover every boundary |
| P04-AC-012 | Credentials/payloads are protected; logs, exports and evidence obey minimization/retention controls |
| P04-AC-013 | UI/queues/reports clearly distinguish prepared, transmitted, acknowledged, accepted-if-evidenced, rejected and uncertain |
| P04-AC-014 | Migration, backup/restore, schema change, provider outage and cutover procedures are proven |
| P04-AC-015 | Contract/sandbox/conformance, failure-injection and reconciliation suites pass for the exact approved versions |
| P04-AC-016 | No product text or evidence overstates regulatory acceptance or compliance |
| P04-AC-017 | Qualified UAE tax/legal, Security, Finance, Operations and independent QA reviews are dispositioned |
| P04-AC-018 | Product Owner approves P04 exit and separately approves any production activation |

## 10. Task Order and Evidence

| Task | Scope | Primary evidence |
|---|---|---|
| P04-T01 | Regulatory applicability/ruleset baseline | P04-EV-001 |
| P04-T02 | Canonical snapshot and validation | P04-EV-002 |
| P04-T03 | Provider due diligence, selection and onboarding contract | P04-EV-003 |
| P04-T04 | Adapter and contract tests | P04-EV-004 |
| P04-T05 | Durable submission/outbox/idempotency | P04-EV-005 |
| P04-T06 | Status, callback and reconciliation | P04-EV-006 |
| P04-T07 | Rejection, credit/correction and operator workflows | P04-EV-007 |
| P04-T08 | Secrets, payload, UI/report and operations controls | P04-EV-008–010 |
| P04-T09 | Migration/recovery/full verification | P04-EV-011–013 |
| P04-T10 | Independent review and exit decision | P04-EV-014 |

## 11. Exit Gate

All P04-AC-001–018 must be `VERIFIED`; no critical/high isolation, authorization, secret, payload, duplicate-submission, financial-integrity, callback or migration finding remains; exact source/provider/schema/status versions and disabled limitations are recorded; and specialist plus Product Owner approvals are explicit. Exit does not itself authorize production traffic or a compliance claim.

## 12. Pending Approvals

| ID | Decision / approver | Review and recommendation | Recording method | Blocks |
|---|---|---|---|---|
| APPR-P04-001 | Bounded P04 scope — Product Owner | Review this spec/matrix; approve provider-neutral scope with unresolved regulated flows disabled | “I approve P04-SPEC-001 as the bounded P04 implementation scope, subject to its named gates.” | P04 implementation |
| APPR-P04-002 | ASP and contract — Product, Security, Legal, Finance, Operations | Review current MoF listing, contract/capabilities, privacy/security, SLA/exit; choose only after evidence | Approved provider-selection record naming legal entity, services, versions, limitations and date | Provider-dependent code/activation |
| APPR-P04-003 | Applicability/rules/schema/status/retention — qualified UAE reviewer + Product | Approve effective-dated ruleset and disabled exclusions; do not generalize beyond evidence | Signed/versioned P04 policy record referencing REG-SRC IDs and artefact checksums | Schema migration, submission activation |
| APPR-P04-004 | Exit/production — Product Owner after independent reviewers | Approve exit and production activation separately with tenant/document/environment limits and rollback | Explicit P04 exit statement plus separate production-activation record | Phase exit / production |
