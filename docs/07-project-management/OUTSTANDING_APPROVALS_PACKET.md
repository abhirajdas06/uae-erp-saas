# Outstanding Approvals Action Packet

| Property | Value |
|---|---|
| Document ID | GOV-APPROVAL-002 |
| Date | 29 October 2026 |
| Status | ACTION REQUIRED BY NAMED HUMANS — NO APPROVAL IS RECORDED HERE |
| Purpose | Make every remaining blocker actionable in one pass, with the exact statement that records each decision |
| Full register | `DECISIONS_PENDING.md` remains canonical; this packet orders and operationalizes it |

## 1. Why This Packet Exists

`AGENTS.md` requires that whenever an approval is pending, the record states the approval identifier, the exact decision required, the authorized approver, the evidence to review, the recommended option, and an explicit example statement that records approval. It also forbids reporting only that "approval is pending".

Every documentation gap found by `GOV-GAP-001` is closed and every module satisfies the `RDY-001`–`RDY-012` gate per `GOV-READINESS-001`. What remains is not writing. It is a set of human decisions and specialist verifications that no agent may record. This packet exists so that set can be cleared efficiently rather than read as a vague blocker.

An agent must never record any approval below, must never mark an ADR `ACCEPTED`, and must never infer an approval from silence or from a related approval.

## 2. Critical Path — Four Decisions Unblock The Most

Approving these four, in this order, moves the project from specification to implementation.

| Order | ID | Exact decision required | Approver | Recommended option | Example statement that records it |
|---|---|---|---|---|---|
| 1 | `APPR-P01-001` | Authorize the first bounded P01 implementation task, naming the task ID, manifest version, file scope, reviewers and evidence requirements | Product Owner | Authorize `P01-T01` only, against the approved P01 baseline, with later tasks remaining unauthorized | "I authorize P01-T01 only, against the approved P01 baseline and manifest version `<version>`, with reviewers `<names>` and the evidence requirements in `P01-TRACE-001`. Later P01 tasks remain unauthorized." |
| 2 | `DEC-GOV-007` | Adopt the `RDY-001`–`RDY-012` phase-entry specification gate as a precondition for authorizing any phase | Product Owner / Architecture | Adopt it. All 24 module specifications already satisfy it, so adoption costs nothing now and prevents regression later | "I approve the `RDY-001`–`RDY-012` phase-entry gate in `GOV-READINESS-001` section 7 as a mandatory precondition for phase implementation authorization." |
| 3 | `DEC-DWF-003` | Approve the local service stack composition and pinned versions for development | DevOps / Architecture | PostgreSQL and Redis in containers at the intended production major versions, Docker Compose per ADR-016 | "I approve the local development stack in `QUAL-DEVWF-001` section 5 with PostgreSQL `<major>` and Redis `<major>` pinned to the intended production majors." |
| 4 | `DEC-TD-002` | Approve the placeholder identifier formats for tax registration numbers, IBANs and identity documents used in fixtures | Tax specialist / Finance | Use documented reserved or structurally invalid patterns that cannot collide with a real registration | "I approve the placeholder identifier formats in `QUAL-TESTDATA-001` section 3 for use in all non-production fixtures." |

`DEC-UI-002` design tokens is required before interface scaffolding specifically, so it joins this list the moment a P01 task touches a screen.

## 3. Product Owner Decisions

| ID | Exact decision | Recommended option | Blocks |
|---|---|---|---|
| `DEC-UI-002` | Design token values, typography pairing and brand palette | Approve a bounded token set; provisional neutral palette for scaffolding only | Any interface work |
| `DEC-UI-003` | Primary navigation grouping and module-to-group mapping | Group by business domain | Shell and navigation |
| `DEC-UI-004` | Presentation of an unentitled module | Non-actionable upgrade affordance, enforcement staying server-side | Navigation and entitlement surfacing |
| `DEC-UI-005` | Printable document layout family and bilingual document header | One layout family for tax invoice, credit note and statement | Document rendering |
| `DEC-L10N-001` | Arabic interface delivery scope, owning phase and release gate | Externalize all strings from the first task; schedule Arabic explicitly | Any Arabic claim |
| `DEC-L10N-003` | Whether Hijri display is offered and where | Presentation-only if at all; Gregorian stays authoritative | Date presentation scope |
| `DEC-A11Y-001` | Accessibility conformance target and surfaces in scope | WCAG 2.2 Level AA | Conformance claims |
| `DEC-A11Y-003` | Browser, platform and minimum-width support matrix | Approve the proposed three-tier matrix | Support claims and test scope |
| `DEC-A11Y-005` | Device classes per data-entry-intensive workflow | State the intended class per workflow | Responsive acceptance |
| `DEC-NTF-001` | Launch channel set | In-application and transactional email only | Notification work |
| `DEC-NTF-003` | Launch notification catalogue and mandatory categories | Approve the catalogue; security, billing and regulatory stay non-optional | Notification work |
| `DEC-NTF-005` | Whether outbound document delivery to customers and suppliers is in scope | Treat as authorized outbound disclosure | Customer-facing delivery |
| `DEC-REP-001` | Launch report catalogue and semantics | Approve `PROD-REPORTS-001` as the catalogue | All reporting work |
| `DEC-REP-004` | Default role-to-report visibility matrix | Restrict payroll and banking reports by default | Report authorization |
| `DEC-MIG-001` | Supported import formats and published templates per domain | Publish a versioned template per domain | Tenant onboarding |
| `DEC-MIG-003` | Whether historical closed transactions are in migration scope | Exclude from go-live | Migration effort |
| `DEC-MIG-006` | Whether an assisted migration service is offered | Defer until self-service is proven | Commercial packaging |
| `DEC-TD-001` | Demonstration dataset scope and reset cadence | Fully synthetic UAE business profile | Demonstrations |
| `DEC-TD-003` | Performance dataset volumes and tenant skew | One large tenant among many small | Performance evidence |
| `DEC-GLOS-001` | Arabic terminology reviewer and bilingual term list | Name the reviewer before Arabic release | Arabic release |
| `DEC-COM-001` | Pricing, trials, grace periods and subscription-change policy | Existing open decision; P02 specifications fail closed meanwhile | P02 acceptance |
| `DEC-PROD-001` | Commercial pilot planning | Existing open decision | Pilot |

## 4. Specialist Verifications

These require a qualified professional, not a product decision. Each has evidence prepared.

| ID | Specialist | Exact question | Evidence prepared |
|---|---|---|---|
| `DEC-PRIV-002` | Legal | Confirm the applicable personal-data instruments, the current status of the PDPL Executive Regulations, the processing-role allocation and the lawful bases | `UAE-PDP-001`–`UAE-PDP-004` in the source register record the law, its Article 28 issuance requirement, the Article 29 regularisation trigger, and that no Executive Regulation was listed on the official portal page on 29 October 2026 |
| `DEC-PRIV-005` | Tax and finance | Map each verified retention period to each ERP record category | `UAE-RET-001`–`UAE-RET-005` record the article-level periods: seven years for corporate tax, five years and seven years under the Tax Procedures Executive Regulation, fifteen years for real estate under the VAT Executive Regulation, and four-year extensions on dispute or audit |
| `DEC-PRIV-006` | Employment | Confirm retention for employment, payroll, wage-protection and identity documents | `REG-HR-001` and the employment source register |
| `DEC-SEQ-002` | Tax | Confirm which document types carry a statutory sequential or gapless numbering expectation | `UAE-NUM-001`–`UAE-NUM-003` record the article-level particulars read on 29 October 2026: tax invoices require a sequential number or a unique number enabling identification and order; no numbering particular appeared in the simplified invoice or credit note lists read, with an extraction caveat. `ARCH-SEQ-001` applies conservative gapless defaults meanwhile |
| `DEC-TAX-001` | Tax | Approve supported VAT treatments, rates, thresholds and return-line composition | `MOD-UAE-VAT-001` fails closed without it |
| `DEC-REP-002` | Tax | Confirm VAT preparation report line composition and whether any return box reference may be used | `PROD-REPORTS-001` forbids box references until then |
| `DEC-MIG-004` | Tax and e-invoicing | Confirm treatment of migrated historical invoices for e-invoicing obligations | `MIG-056` excludes them by default |
| `DEC-A11Y-002` | Legal | Determine whether any UAE or contractual accessibility obligation applies | `QUAL-A11Y-001` asserts none |
| `DEC-PRIV-003` | Legal | Determine whether any free-zone data-protection regime applies | Open |
| `DEC-FIN-001`–`DEC-FIN-005` | Finance | Precision, rounding, posting, reversal and valuation policy | `MOD-ACCOUNTING-001` fails closed without them |
| `DEC-HR-001`, `DEC-PAY-001`, `DEC-PAY-002` | Employment and payroll | Employment and leave scope, payroll component model and wage-protection format and agent | `MOD-HRMS-001` and `MOD-PAYROLL-001` fail closed |
| `DEC-BANK-001`–`DEC-BANK-003` | Finance and legal | Connectivity and payment modes, provider, reconciliation policy | Modes B, C and D are unreachable meanwhile |
| `DEC-PROJ-001`, `DEC-EXP-001`, `DEC-FA-001`, `DEC-P06-001` | Finance and operations | Domain policy for projects, expenses, assets, procurement and inventory | Each owning specification fails closed |
| `DEC-SEC-006` | Product Owner | Scope, timing and provider of independent security testing | `QUAL-THREAT-001` states no assurance exists |

## 5. Infrastructure and Launch Authority

| ID | Decision | Approver |
|---|---|---|
| `DEC-OPS-001`–`DEC-OPS-005` | Provider, topology, SLO, RPO and RTO, capacity and alert thresholds | Product Owner / DevOps |
| `DEC-PRIV-004` | Hosting region, data-at-rest location and residency position | Product Owner / Legal |
| `DEC-NTF-002` | Transactional email provider, sending domain and data-processing terms | Product Owner / DevOps |
| `DEC-INT-001`–`DEC-INT-003` | Integration scope, credential handling and shared transport behavior | Product Owner / DevOps / Architecture |
| `DEC-DWF-002` | Branch protection, required reviewers and merge strategy | Product Owner / DevOps |
| `DEC-DWF-004` | Formatter, linter and type-checker toolchain | Architecture / QA |
| ASP selection and PINT AE activation | E-invoicing provider and profile activation | Product Owner / E-invoicing specialist |
| Production provider, spend, provisioning, deployment and launch | Explicitly unapproved | Product Owner |

## 6. Recording Requirements

For each decision the record must state the identifier, the selected option and its scope, the approver and date, the reviewed evidence version, the documents requiring reconciliation, the implementation and test implications, and any deferred follow-up. `DECISIONS_PENDING.md` section 12 holds the full requirement and section 13 holds the decision log.

A decision recorded without its scope is treated as unapproved, because an unbounded approval cannot be verified later.

## 7. What Cannot Be Delegated To An Agent

1. Recording any approval or marking any ADR `ACCEPTED`.
2. Confirming a regulatory fact as a professional opinion. Agents may locate and date official text, as done for `UAE-RET-001`–`UAE-RET-005` and `UAE-PDP-001`–`UAE-PDP-003`, but applicability and interpretation are specialist work.
3. Selecting a provider, authorizing spend, provisioning infrastructure, deploying to production or launching commercially.
4. Accepting a residual security risk.

This packet records no approval and authorizes no implementation.
