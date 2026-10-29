# Risks and Issues Register — UAE ERP SaaS

| Property | Value |
|---|---|
| Document ID | PM-RISK-001 |
| Version | 1.0 |
| Status | Active |
| Last Updated | 29 October 2026 |

## 1. Purpose

This register tracks material technical, security, product, commercial, regulatory, and operational uncertainty. Detailed controls remain in their owning specifications and ADRs.

Severity values are `CRITICAL`, `HIGH`, `MEDIUM`, and `LOW`. Status values are `OPEN`, `MITIGATING`, `ACCEPTED`, `RESOLVED`, and `CLOSED`.

## 2. Active Risks

| ID | Risk | Severity | Status | Owner | Current mitigation / next evidence |
|---|---|---|---|---|---|
| RISK-001 | Tenant data can be exposed through inconsistent request, service, task, report, cache, file, or database scoping | CRITICAL | MITIGATING | Architecture / Security | Accepted ADR-002/004/014 and approved SEC-002/TST-004 define controls; implementation evidence remains required |
| RISK-002 | Draft architecture language may be treated as approved implementation direction | HIGH | MITIGATING | Architecture / Governance | ADR register separates record state from decision status; approval remains explicit |
| RISK-003 | Conflicting ownership of tenant membership may create competing models, migrations, or authorization paths | HIGH | RESOLVED | Architecture / Security | ADR-003 accepted and `DJANGO_APP_STRUCTURE.md` reconciled to `tenants.TenantMembership` on 28 October 2026 |
| RISK-004 | Inconsistent RLS context keys may produce denied operations, untested policies, or false isolation confidence | CRITICAL | RESOLVED | Security / Database | ADR-004 accepted and `MULTI_TENANCY.md` reconciled to `app.current_tenant_id` on 28 October 2026 |
| RISK-005 | Duplicated registries and scattered pending decisions may drift | HIGH | MITIGATING | Documentation / Governance | Canonical ADR, decision, risk, project, and phase registers established |
| RISK-006 | Reused or unmapped requirement and test identifiers may break traceability and acceptance reporting | HIGH | MITIGATING | QA / Documentation | P00 traceability baseline created; validate remaining namespaces, completeness, and executed evidence as phases progress |
| RISK-007 | Approved security/testing/CI standards may not be enforced consistently in implementation | HIGH | MITIGATING | Security / QA / DevOps | Initial validators/workflow pass locally and in hosted run 40647091699; protected-branch enforcement and later application gates remain required |
| RISK-008 | Unverified UAE regulatory assumptions may produce incorrect product behavior or compliance claims | HIGH | MITIGATING | Product / Compliance | REG-SRC-001 now supplies a 29 October 2026 official-source/supersession baseline; applicability, exact artefacts, interpretations, provider and specialist approval remain open and require revalidation |
| RISK-009 | Shared-database restore may have a multi-tenant blast radius and no validated tenant-level recovery path | CRITICAL | OPEN | DevOps / Database | Define RPO/RTO, backup architecture, restore tests, and tenant recovery procedure |
| RISK-010 | Financial rules may be implemented before precision, rounding, posting, reversal, and valuation policies are approved | CRITICAL | MITIGATING | Finance / Architecture | P05 specs fail closed pending DEC-FIN-001/005 and DEC-TAX-001; concrete finance/tax policy and specialist evidence remain mandatory before migrations/calculation |
| RISK-011 | External retries may duplicate payments, e-invoices, or business effects | CRITICAL | MITIGATING | Architecture / Integration | Accepted ADR-009/010/012 require operation records, idempotency, outbox, and reconciliation; implementation tests remain required |
| RISK-012 | Missing Git metadata prevents reliable history, diff review, and change attribution | MEDIUM | RESOLVED | Repository Maintainer | Git repository root and working-tree visibility verified at `D:/Project/uae-erp-saas` on 28 October 2026 |
| RISK-013 | Scope expansion across the full ERP catalogue may bypass phase gates | HIGH | MITIGATING | Product / Orchestrator | Keep documentation-only mode; authorize bounded phases and tasks only |
| RISK-014 | Sensitive payroll, banking, tax, and employee data may receive insufficient access controls | CRITICAL | OPEN | Security / Domain Owners | Define data classification, least privilege, audit, export, retention, and security tests |
| RISK-015 | UUIDs may be mistaken for authorization or cross-tenant references may rely only on application validation | CRITICAL | MITIGATING | Architecture / Database / Security | ADR-014 requires tenant-scoped lookup, direct ownership, and composite constraints for critical relationships |
| RISK-016 | Provider integration may misrepresent timeout, transport success, or provider receipt as regulatory acceptance | CRITICAL | MITIGATING | Integration / Compliance | P04 contract/matrix require separate native/internal statuses, authenticated evidence and uncertain-outcome reconciliation; provider-specific execution evidence remains required |
| RISK-017 | Containerization may be mistaken for production availability, backup, or recovery readiness | HIGH | MITIGATING | DevOps / Architecture | ADR-016 separates image/runtime design from topology, persistent data, RPO/RTO, and production approval |
| RISK-018 | Secrets may leak through source, images, CI, logs, task payloads, or shared credentials | CRITICAL | MITIGATING | Security / DevOps | ADR-017 requires runtime secret injection, scoped identities, redaction, scanning, rotation, and compromise response |
| RISK-019 | Audit records or logs may omit critical evidence or become an uncontrolled sensitive-data repository | CRITICAL | MITIGATING | Security / Compliance / Audit Owner | ADR-018 separates audit/log/telemetry purposes and requires minimization, append controls, access, and category retention |
| RISK-020 | CI may report false confidence through SQLite-only tests, skipped failures, unsafe secrets, or weak release gates | HIGH | MITIGATING | QA / DevOps / Security | Initial P00 gates fail closed, use no secrets, and have hosted evidence; later PostgreSQL/application gates remain required |
| RISK-021 | File metadata and object content may diverge, expose another tenant, preserve malicious content, or lose regulated evidence | CRITICAL | MITIGATING | Architecture / Security / Privacy / Operations | ADR-019 requires private storage, trusted metadata authorization, quarantine/scanning, checksums, immutable versions, reconciliation, and recovery tests |
| RISK-022 | External API, webhook, event, or provider contracts may drift silently and create incompatible or duplicate business effects | HIGH | MITIGATING | Architecture / Integration / QA / Product | ADR-020 requires explicit versions, machine-readable contracts, compatibility gates, idempotency, consumer inventory, and governed deprecation |
| RISK-023 | Documentation traceability may be mistaken for implemented or executed control evidence | HIGH | MITIGATING | QA / Governance | P00 matrix distinguishes documentation status from `NOT_RUN` application verification and requires evidence-linked status changes |
| RISK-024 | An approved P01 specification or test matrix may be mistaken for authorization or proof that tenant isolation is implemented | CRITICAL | MITIGATING | Product / Governance / Security | Approval is explicitly specification-only, all 53 tests are `NOT_RUN`, and entry requires P00 exit plus separate P01 authorization |
| RISK-025 | The dependency-free P00 secret scanner may miss novel, encoded, high-entropy, or history-only credentials | HIGH | MITIGATING | Security / DevOps | Initial patterns fail closed on recognized credentials; retain Git hygiene, review findings, and select a specialist history-aware scanner before application secrets or deployment workflows are introduced |
| RISK-026 | Missing dedicated `SALES-*` product requirements may allow Sales scope and acceptance behavior to drift | HIGH | MITIGATING | Product / Sales / Documentation | `SALESM-*` and P03 criteria provide a bounded draft baseline; reconcile stable product requirement IDs before P03 implementation approval |
| RISK-027 | Customer, sellable-item, and downstream snapshot ownership may be duplicated across CRM, Sales, Inventory, and Invoicing | HIGH | MITIGATING | Architecture / Domain Owners | P03 specs recommend CRM customer ownership and a minimal Sales item with explicit snapshots/mapping; DEC-P03-001 must be approved before schema work |
| RISK-028 | Invoice issuance may embed unverified numbering, tax, currency, rounding, correction, retention, or legal-document rules | CRITICAL | MITIGATING | Product / Finance / UAE Tax and Legal | P03/P04/P05 specifications and REG-SRC-001 require versioned authoritative-source/specialist approval and fail closed; concrete policies remain open |
| RISK-029 | Rapid 2026 e-invoicing/VAT amendments or dynamic technical artefacts may make an approved ruleset stale | CRITICAL | MITIGATING | Product / Compliance / Integration / Tax | REG-SRC-001 records supersession and revalidation triggers; implementation must pin checksummed artefacts, monitor change, and disable affected unverified behavior |
| RISK-030 | Accounting, VAT and source subledgers may diverge through duplicate/missing postings or mutable historical policy | CRITICAL | MITIGATING | Finance / Accounting / VAT / QA | P05 requires unique versioned source-purpose posting, immutable snapshots and source-to-tax-to-ledger reconciliation; implementation/recovery evidence remains required |
| RISK-031 | Direct or concurrent stock changes may corrupt quantities, availability or valuation | CRITICAL | MITIGATING | Inventory / Database / QA | P06 requires movement-only atomic operations, idempotency/locking, approved negative/reservation policy and movement-balance-value reconciliation; implementation evidence remains required |
| RISK-032 | Unapproved item/UOM/valuation choices may make P03/P06/P05 records incompatible or financially incorrect | CRITICAL | MITIGATING | Product / Architecture / Finance / Operations | APPR-P06-002–004 gate schema and valuation; advanced behavior stays disabled and versioned mappings/contracts are required |
| RISK-033 | One generic “UAE payroll” ruleset may be applied to the wrong employer, jurisdiction, worker or pension cohort | CRITICAL | MITIGATING | Product / HR / Payroll / UAE Legal | REG-HR-001 defines a MoHRE-private-sector candidate scope and exclusions; P07 requires effective applicability and specialist-approved rulesets |
| RISK-034 | Employee identity, salary, bank, pension, medical/leave or payroll data may be exposed through broad roles, exports, files, logs or support access | CRITICAL | MITIGATING | Security / Privacy / HR / Payroll | P07 requires purpose/field/object access, private files, redaction, audited privileged access and APPR-P07-005 before production data |
| RISK-035 | Payroll/WPS processing may duplicate pay/posting or misrepresent prepared/uploaded data as accepted, disbursed or settled wages | CRITICAL | MITIGATING | Payroll / Finance / Integration / Compliance | P07 requires immutable runs, maker-checker, idempotent posting/WPS operations, exact agent contracts and evidence-based reconciliation/statuses |
| RISK-036 | Retroactive HR/leave/payroll rule changes may silently rewrite finalized results or produce unreconciled adjustments | HIGH | MITIGATING | HR / Payroll / Finance | P07 requires effective-dated snapshots, stale-approval detection and linked adjustment/off-cycle/reversal workflows with reconciliation |
| RISK-037 | Project operational records may be treated as financial/project-accounting truth or duplicated across CRM, HRMS and Accounting | HIGH | MITIGATING | Product / Architecture / Project Operations / Finance | P08 keeps Projects operational, requires explicit cross-domain references/snapshots and gates time/costing/project-accounting scope through DEC-PROJ-001 |
| RISK-038 | Expense claims may duplicate reimbursement/posting or expose receipts, bank details and personal data | CRITICAL | MITIGATING | Finance / Security / Privacy / HR | P08 requires private files, maker-checker, duplicate detection, immutable approvals, idempotent external effects and evidence-based settlement |
| RISK-039 | Unapproved or retroactively changed asset policy may produce irreproducible depreciation, disposal or ledger values | CRITICAL | MITIGATING | Finance / Tax / Architecture | P08 requires effective versioned policy/snapshots, Decimal fixtures, immutable runs, linked corrections and asset-ledger reconciliation; DEC-FA-001 remains open |
| RISK-040 | Statement parser drift, duplicate/overlapping imports or opaque matching may corrupt bank reconciliation | CRITICAL | MITIGATING | Finance / Banking / QA / Architecture | P09 preserves native evidence, pins parser/rule versions, detects duplicate/overlap and requires explainable human-confirmed matches and reconciliation |
| RISK-041 | Direct bank data or payment functionality may be enabled without correct CBUAE licensing, consent or provider authority | CRITICAL | MITIGATING | Product / UAE Legal and Compliance / Security / Finance | REG-BANK-001 and P09 separate Modes A–D; Modes B–D fail closed pending APPR-P09-002/003/005 and exact current evidence |
| RISK-042 | Bank account, transaction narrative, consent, credentials or provider payloads may leak through files, logs, exports or support access | CRITICAL | MITIGATING | Security / Privacy / Banking / Operations | P09 applies private storage, masking, minimization, secrets references, purpose-bound access, redaction, audit and isolation tests |
| RISK-043 | Provider receipt, timeout or local preparation may be misrepresented as executed or settled payment, causing duplicate payment attempts | CRITICAL | MITIGATING | Finance / Integration / Operations | Provider contract requires native/internal status separation, stable idempotency, authenticated callbacks, uncertain-outcome reconciliation and no blind retry |
| RISK-044 | Reporting may leak cross-tenant/sensitive data through joins, aggregation, cache, schedules or exports, or publish metrics that diverge from source domains | CRITICAL | MITIGATING | Reporting / Security / Domain Owners / Finance | P10 requires pre-aggregation authorization, scoped cache/artifacts, explicit semantics and Accounting/source reconciliation with 175 planned tests |
| RISK-045 | A generic integration hub may bypass domain controls, leak credentials/payloads or duplicate external business effects | CRITICAL | MITIGATING | Integration / Security / Architecture / Domain Owners | P10 preserves domain ownership and requires secrets references, durable operations, authenticated inbox/outbox, uncertainty and reconciliation |
| RISK-046 | Platform support or impersonation may create invisible cross-tenant privileged access | CRITICAL | MITIGATING | Security / Privacy / Support / Product | P11 defaults impersonation off and requires purpose-bound expiring grants, real-actor audit, step-up, revocation, alert and independent review |
| RISK-047 | Retention, deletion or tenant offboarding may erase financial/audit evidence or leave inaccessible copies and credentials | CRITICAL | MITIGATING | Privacy / Legal / Finance / Security / Domain Owners | P11 requires inventory, hold precedence, dependency-aware preview/resume/reconciliation and explicit policy approval |
| RISK-048 | Performance or enterprise-readiness claims may rely on non-representative tests and hide noisy-tenant, peak, batch or dependency failures | HIGH | MITIGATING | Performance / Operations / Architecture / QA | P11 and DEP-CAP-001 require reproducible representative load, failure, headroom and integrity/isolation evidence |
| RISK-049 | Production deployment may be mistaken as safe because containers start or CI passes despite unsafe configuration, migrations, secrets or access | CRITICAL | MITIGATING | DevOps / Security / Database / Release Owner | P12 requires exact release identity, protected configuration, migration rehearsal, release review and separate deployment/launch approvals |
| RISK-050 | Backups may be missing, corrupt, incomplete or unusable within required objectives, especially across database and files | CRITICAL | MITIGATING | DevOps / Database / Operations / File Owner | DEP-BCR-001 and P12 require protected inventory plus independent DB/PITR/object restore, reconciliation and measured RPO/RTO |
| RISK-051 | Monitoring or incident procedures may miss tenant exposure, financial corruption, provider uncertainty or recovery failure | CRITICAL | MITIGATING | Operations / Security / Domain Owners | DEP-OBS/RUN/INC and P12 require business/security/recovery signals, actionable alerts, on-call ownership and exercised scenarios |
| RISK-052 | Rollback may worsen data integrity because code, schema, tasks, providers and files are not backward compatible | CRITICAL | MITIGATING | Release / Database / Integration / Domain Owners | DEP-REL/GUIDE require compatibility analysis, single migrations, containment, forward recovery and reconciled verification; no automatic schema rollback |
| RISK-053 | A PINT AE web page, semantic model, code list, Schematron or provider mapping may be used from a different or stale release, or Self-Billing may be enabled because its data model resembles Billing | CRITICAL | MITIGATING | E-Invoicing / Tax / Integration / QA | UAE-EINV-010 and ARCH-PINT-AE-001 require an archived checksummed release set, separate transaction profiles, complete term-to-UBL mapping, layered validation, historical coexistence and explicit current-version/Self-Billing approval |

## 3. Active Issues

| ID | Issue | Severity | Status | Required resolution |
|---|---|---|---|---|
| ISSUE-001 | `SYSTEM_ARCHITECTURE.md` used a conflicting ADR-004–ADR-010 sequence | HIGH | RESOLVED | Canonical ADR sequence restored on 27 October 2026 |
| ISSUE-002 | Project status, phase status, decision, and risk registers were absent | HIGH | RESOLVED | Registers established on 27 October 2026 |
| ISSUE-003 | Some intended phase, module, agent, quality, and deployment directories/documents remain absent | MEDIUM | OPEN | `docs/02-phases/P00_FOUNDATION/` and `docs/05-quality/` now exist; create other units only when authorized and required |
| ISSUE-004 | Product and non-ADR architecture narratives required scoped approval/reconciliation | HIGH | RESOLVED | Repository-wide baseline review completed on 28 October 2026; open specialist decisions remain in the canonical register |
| ISSUE-005 | Authentication test IDs collided with product requirement IDs | HIGH | RESOLVED | Test scenarios renamed to IAM-TST-001 through IAM-TST-044 on 27 October 2026 |
| ISSUE-006 | Initial ADR roadmap was incomplete and lacked a set-level consistency/approval review | HIGH | RESOLVED | ADR-001 through ADR-020 are accepted; `ADR_INITIAL_SET_REVIEW.md` and `ADR_STANDARDS_REVIEW.md` preserve review and approval evidence |

## 4. Review Rules

- Review this register after every material ADR, phase transition, security finding, provider decision, or regulatory verification.
- A risk may be marked `ACCEPTED` only by an authorized human with rationale and review date.
- A risk is not `RESOLVED` merely because documentation describes a control; implementation and verification evidence are required where applicable.
- Critical and high risks must appear in phase exit reviews when they affect the phase scope.

## 5. Change Log

| Date | Change |
|---|---|
| 27 October 2026 | Established the canonical risk and issue register from the repository audit. |
| 28 October 2026 | Added file-storage and external-contract risks after ADR-019/020 and closed the initial ADR-set review issue. |
| 28 October 2026 | Recorded ADR acceptance, reconciled membership ownership and RLS context-key conflicts, and updated quality-governance risk status. |
| 28 October 2026 | Added P00 traceability-status risk and updated phase/documentation issues after creating the P00 specification and matrix. |
| 28 October 2026 | Added the P01 authorization/evidence risk after drafting the bounded P01 specification and tenant-isolation matrix. |
| 28 October 2026 | Updated quality, tenant-isolation, and document-state risks after scoped repository approval and the manifest/CI specifications. |
| 28 October 2026 | Recorded local completion evidence and remaining hosted-enforcement limitations for P00-T-001. |
| 28 October 2026 | Recorded successful hosted P00 run 40647091699; retained later application-gate and specialist-scanner limitations. |
| 29 October 2026 | Added P04/P05 regulatory-drift and source-tax-ledger reconciliation risks; linked existing controls to the dated regulatory register and new phase specifications. |
| 29 October 2026 | Added P06 stock/master/valuation and P07 applicability/privacy/payroll/WPS/retroactivity risks with explicit approval and evidence gates. |
| 29 October 2026 | Added P08 project/expense/asset and P09 import/licensing/sensitive-data/payment risks with provider-neutral, fail-closed and reconciliation controls. |
| 29 October 2026 | Added P10 reporting/integration, P11 privileged/data-lifecycle/readiness and P12 deployment/recovery/incident/release risks with explicit evidence and approval gates. |
| 29 October 2026 | Added the pinned PINT AE 2025-Q2 structure/mapping/validation strategy and stale/mixed-profile risk after reviewing the OpenPeppol publication. |
