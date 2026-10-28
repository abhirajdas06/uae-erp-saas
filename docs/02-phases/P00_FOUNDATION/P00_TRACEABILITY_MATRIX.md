# P00 Requirements-to-Control-to-Test Traceability Matrix

| Property | Value |
|---|---|
| Document ID | P00-TRACE-001 |
| Version | 1.0 |
| Status | APPROVED VERIFICATION BASELINE |
| Date | 28 October 2026 |
| Owner | QA / Project Governance |
| Reviewers | Product, Architecture, Security, QA, DevOps |
| Parent Phase | [P00 Phase Specification](P00_PHASE_SPECIFICATION.md) |

## 1. Purpose

This matrix links P00 exit requirements and relevant product requirements to accepted ADR controls, approved security requirements, approved test requirements, verification methods, evidence, owners, and current status.

It is a planning and evidence-control document. `SATISFIED` means the documentation evidence named in the row exists and was checked at the stated level; it does not claim that future application behavior has been implemented or tested.

## 2. Status Vocabulary

| Status | Meaning |
|---|---|
| SATISFIED | Required P00 documentation evidence exists and has passed the stated review/check |
| PARTIAL | Some evidence exists, but review, approval, reconciliation, or required content remains |
| OPEN | Work has not produced reviewable evidence yet |
| BLOCKED | A named unresolved dependency prevents progress |
| DEFERRED | Explicitly postponed to a named later phase/trigger with owner and consequence |
| NOT_APPLICABLE | Reviewed and determined not applicable to P00, with rationale |

Application verification remains `NOT_RUN` until an authorized implementation task executes the named tests.

## 3. P00 Exit Traceability

| P00 criterion | Source requirement | Accepted architecture controls | Security controls | Test/verification controls | Required P00 evidence | Owner | Current status |
|---|---|---|---|---|---|---|---|
| P00-AC-001 | Roadmap §5.3; PRD-003, PRD-004 | ADR-001, ADR-003 | SEC-001 | TST-001 | Reviewed product scope/non-goals and status-language audit | Product | SATISFIED |
| P00-AC-002 | Roadmap §5.3; PRD-003, PRD-004 | ADR-015 | SEC-001 | TST-001 | Identifier uniqueness check and requirements review | QA / Documentation | SATISFIED |
| P00-AC-003 | PRD-001, PRD-002 | ADR-001, ADR-003, ADR-006 | SEC-005 | TST-001, TST-006 | Module catalogue and ownership/dependency review | Product / Architecture | SATISFIED |
| P00-AC-004 | PRD-001 | ADR-001, ADR-003 | SEC-001 | TST-001 | Dependency graph review and circular-dependency check design | Architecture | SATISFIED |
| P00-AC-005 | TEN-001, TEN-002, TEN-003; IAM-001, IAM-002, IAM-003, IAM-004, IAM-005; SUB-003 | ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-014 | SEC-002, SEC-003, SEC-004, SEC-005 | TST-003, TST-004, TST-005, TST-006 | Accepted ADRs plus reconciled membership/RLS-key documents | Architecture / Security | SATISFIED |
| P00-AC-006 | BILL-001; NFR-006, NFR-007 | ADR-011, ADR-013 | SEC-014 | TST-010 | Financial-principles review and explicit DEC-FIN-001 deferral | Finance / Architecture | SATISFIED |
| P00-AC-007 | INT-001, INT-002; AUD-001; OPS-001, OPS-002; DEP-001, DEP-002 | ADR-009, ADR-010, ADR-012, ADR-016, ADR-017, ADR-018, ADR-019, ADR-020 | SEC-007, SEC-008, SEC-011, SEC-012, SEC-013, SEC-015, SEC-016, SEC-017 | TST-008, TST-009, TST-011, TST-012, TST-013, TST-014, TST-015, TST-018 | Cross-ADR review and standards approval record | Architecture / Security / DevOps | SATISFIED |
| P00-AC-008 | Roadmap §5.3; NFR-001, NFR-002, NFR-003, NFR-008 | ADR-015, ADR-017, ADR-018 | SEC-001 through SEC-018 | TST-001 through TST-018 | Approved quality documents with reviewer/date records | Security / QA | SATISFIED |
| P00-AC-009 | PRD-003, PRD-004; TST-001 | ADR-015 | SEC-001 | TST-001 | This matrix plus validation report | QA / Governance | SATISFIED |
| P00-AC-010 | Roadmap §5.3 | All applicable ADRs | SEC-001, SEC-018 | TST-001 | Decision/risk register review with owners and required-by gates | Product / Governance | SATISFIED |
| P00-AC-011 | NFR-008 | ADR-001, ADR-003, ADR-015 | SEC-001, SEC-015 | TST-001, TST-016 | `AGENTS.md`, repository structure, link/identifier checks | Architecture / QA | SATISFIED |
| P00-AC-012 | PRD-003, PRD-004 | ADR-015 | SEC-001, SEC-015 | TST-001, TST-016 | Manifest schema/specification and validation evidence | Governance / DevOps | SATISFIED |
| P00-AC-013 | NFR-002, NFR-008; DEP-003 | ADR-015, ADR-016, ADR-017 | SEC-011, SEC-015, SEC-016 | CI/release gates; TST-015, TST-016 | Initial CI run or explicit approved P00 exception | QA / DevOps | SATISFIED |
| P00-AC-014 | PRD-003; TEN-001, TEN-002, TEN-003; IAM-001, IAM-002, IAM-003, IAM-004, IAM-005 | ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-014, ADR-015 | SEC-001, SEC-002, SEC-003, SEC-004, SEC-005 | TST-001, TST-003, TST-004, TST-005, TST-006 | Bounded P01 specification and task/evidence map | Product / Architecture / Security / QA | SATISFIED |
| P00-AC-015 | TEN-002, TEN-003; IAM-003, IAM-004, IAM-005; NFR-006, NFR-009 | ADR-002, ADR-003, ADR-004, ADR-005, ADR-011, ADR-014, ADR-017 | SEC-002, SEC-003, SEC-004, SEC-005, SEC-011, SEC-014 | TST-003, TST-004, TST-005, TST-006, TST-010, TST-014, TST-015, TST-016 | Critical finding/decision review showing no P01 blocker | Security / Architecture | PARTIAL |
| P00-AC-016 | PRD-004 | ADR-015, ADR-018 | SEC-001, SEC-012 | TST-001; evidence format | Complete P00 evidence index and independent review | QA / Governance | PARTIAL |
| P00-AC-017 | PRD-003; DEP-003; Roadmap §5.4 | ADR-015, ADR-016 | SEC-001, SEC-016 | Production/phase gate rules | Explicit P00 exit approval and separate P01 authorization | Product Owner | PARTIAL |

## 4. Product Requirement Control Matrix

This section covers product requirements that establish foundation controls or later release gates. Later-phase requirements are included to verify architectural coverage; they are not P00 implementation commitments.

| Requirement IDs | P00 applicability | ADR controls | Security controls | Test controls | Evidence / future verification | P00 status |
|---|---|---|---|---|---|---|
| PRD-001 | Foundation design | ADR-001, ADR-003, ADR-006 | SEC-001, SEC-005 | TST-001, TST-002, architecture dependency checks | Module catalogue, ownership map, dependency review | PARTIAL |
| PRD-002 | Foundation design; P02 implementation | ADR-006, ADR-007, ADR-008 | SEC-005 | TST-006, TST-007, TST-008 | Entitlement contract and future server/UI denial tests | PARTIAL |
| PRD-003 | P00 gate | ADR-015 | SEC-001 | TST-001 | Phase specs, status register, manifest/approval evidence | PARTIAL |
| PRD-004 | P00 gate and every release | ADR-015, ADR-018 | SEC-001, SEC-012 | TST-001 | Evidence-based status and release records | PARTIAL |
| TEN-001 | P01 design | ADR-002, ADR-014 | SEC-002 | TST-003, TST-004 | P01 model/constraint specification; future tests | PARTIAL |
| TEN-002 | Critical P01 design | ADR-002, ADR-004, ADR-014 | SEC-002, SEC-005, SEC-008 | TST-004, TST-006, TST-012 | Tenant-isolation matrix; future negative tests | PARTIAL |
| TEN-003 | Critical P01 design | ADR-004, ADR-005, ADR-009 | SEC-002–SEC-004, SEC-013 | TST-004, TST-005, TST-009 | Request/task/RLS context design and future tests | PARTIAL |
| IAM-001 | P01 design | ADR-005, ADR-007, ADR-008, ADR-017 | SEC-003, SEC-004, SEC-011 | TST-005, TST-015, TST-016 | Auth/session specification and future abuse tests | PARTIAL |
| IAM-002 | P01 design | ADR-003–ADR-005, ADR-014 | SEC-002, SEC-005 | TST-003, TST-004, TST-006 | Accepted ownership; P01 membership model/tests | PARTIAL |
| IAM-003, IAM-004 | Critical P01 design | ADR-005, ADR-008 | SEC-005, SEC-006, SEC-007 | TST-006, TST-008 | Permission/object matrix and negative tests | PARTIAL |
| IAM-005 | Critical P01 design | ADR-005, ADR-018 | SEC-003, SEC-005, SEC-012 | TST-005, TST-006, TST-013 | Platform/support access and audit specification | PARTIAL |
| SUB-001, SUB-003 | P02 design dependency | ADR-006, ADR-010, ADR-014 | SEC-005, SEC-013 | TST-006, TST-009 | Entitlement contract; future state/cache/duplicate tests | PARTIAL |
| BILL-001 | Architecture boundary | ADR-003, ADR-006, ADR-011 | SEC-005, SEC-014 | TST-006, TST-010 | Ownership map and later integration tests | SATISFIED |
| EIN-001, EIN-002, EIN-003, EIN-004, EIN-005 | Future P04 release gate | ADR-009, ADR-010, ADR-011, ADR-012, ADR-020 | SEC-007, SEC-013, SEC-014 | TST-008, TST-009, TST-011 | Provider/regulatory decisions and controlled integration evidence | DEFERRED |
| REP-001, REP-002, REP-003 | Cross-phase design | ADR-002, ADR-004, ADR-009, ADR-014, ADR-019 | SEC-002, SEC-005, SEC-008, SEC-009 | TST-004, TST-006, TST-012, TST-017 | Tenant-scoped query/export specification and later tests | PARTIAL |
| INT-001, INT-002 | Integration baseline | ADR-009, ADR-010, ADR-012, ADR-017, ADR-020 | SEC-007, SEC-011, SEC-013 | TST-008, TST-009, TST-011 | Interface catalogue/contracts and future provider evidence | PARTIAL |
| AUD-001 | P01 design and all phases | ADR-010, ADR-018 | SEC-012 | TST-013 | Audit taxonomy/coverage matrix and future transactional tests | PARTIAL |
| OPS-001 | P01 design and operations | ADR-017, ADR-018 | SEC-011, SEC-012 | TST-013, TST-015, TST-016 | Logging/redaction standard and future tests | PARTIAL |
| OPS-002 | When background work begins | ADR-009, ADR-010 | SEC-013 | TST-009 | Task/outbox contracts and reliability tests | DEFERRED |
| OPS-003 | Production release gate | ADR-002, ADR-016, ADR-019 | SEC-017 | TST-018 | Approved RPO/RTO, backup design, restore evidence | DEFERRED |
| OPS-004 | Production release gate | ADR-009, ADR-010, ADR-016, ADR-018 | SEC-012, SEC-013, SEC-016 | TST-009, TST-013, TST-015, TST-018 | Monitoring/alert catalogue and exercises | DEFERRED |
| NFR-001 | P00/P01 design | ADR-005, ADR-016, ADR-017 | SEC-003, SEC-004, SEC-010, SEC-011, SEC-016 | TST-005, TST-015, TST-016 | Security, cryptography, and configuration baseline tests | PARTIAL |
| NFR-002 | P00 gate and every release | ADR-015, ADR-016, ADR-017 | SEC-015, SEC-016 | TST-015, TST-016 | Dependency/CI policy and future scan evidence | PARTIAL |
| NFR-003 | Cross-phase design | ADR-007, ADR-008, ADR-019, ADR-020 | SEC-006, SEC-007, SEC-008 | TST-007, TST-008, TST-012, TST-016 | Input/output/file standards and future negative tests | PARTIAL |
| NFR-004, NFR-005 | Future performance gate | ADR-002, ADR-009, ADR-014, ADR-015, ADR-016 | SEC-016 | TST-003, TST-017 | Approved workloads/targets and performance evidence | DEFERRED |
| NFR-006, NFR-007 | Architecture baseline | ADR-009, ADR-010, ADR-011, ADR-012, ADR-013, ADR-020 | SEC-007, SEC-013, SEC-014 | TST-008, TST-009, TST-010, TST-011 | Failure/idempotency contracts and future simulations | PARTIAL |
| NFR-008 | P00 gate | ADR-001, ADR-003, ADR-015 | SEC-001, SEC-015 | TST-001, CI gates | Approved quality standards and CI evidence | PARTIAL |
| NFR-009 | P01 and every schema phase | ADR-002, ADR-014, ADR-015, ADR-016 | SEC-016, SEC-017 | TST-003, TST-014, TST-015 | Migration policy and future clean/upgrade tests | PARTIAL |
| NFR-010, NFR-011 | Production planning | ADR-016, ADR-019 | SEC-016, SEC-017 | TST-017, TST-018 | Approved objectives, capacity, restore evidence | DEFERRED |
| NFR-012, NFR-013 | UI/document phases | ADR-007, ADR-013, ADR-019 | SEC-006, SEC-008 | TST-007, TST-010, TST-012 | Locale/language/RTL decisions and future tests | DEFERRED |
| DEP-001 | P00 design; production gate | ADR-015–ADR-017 | SEC-011, SEC-015, SEC-016 | TST-014–TST-016 | Deployment specification and future exercise | PARTIAL |
| DEP-002 | P00/P01 design | ADR-016, ADR-017 | SEC-011, SEC-016 | TST-015, TST-016 | Configuration catalogue and future startup/secret checks | PARTIAL |
| DEP-003 | P00 governance; production gate | ADR-015, ADR-016 | SEC-001, SEC-015, SEC-016, SEC-017, SEC-018 | CI/release/production gates; TST-015, TST-016, TST-018 | Approval and release evidence package | PARTIAL |

## 5. ADR-to-Control-to-Test Matrix

| ADR | Accepted control outcome | Security requirements | Test requirements | Required P00 evidence | Status |
|---|---|---|---|---|---|
| ADR-001 | Modular monolith with explicit boundaries | SEC-001 | TST-001, TST-002 | Architecture/module boundary review | PARTIAL |
| ADR-002 | Shared PostgreSQL/schema with explicit ownership | SEC-002, SEC-017 | TST-003, TST-004, TST-018 | Tenancy/database design review | PARTIAL |
| ADR-003 | One owner per model/write operation | SEC-001, SEC-005 | TST-001, TST-002 | Ownership map reconciled | PARTIAL |
| ADR-004 | Application isolation plus phased RLS | SEC-002 | TST-003, TST-004 | Canonical key reconciled; RLS verification plan | PARTIAL |
| ADR-005 | Identity, membership, scoped authorization | SEC-003, SEC-004, SEC-005 | TST-005, TST-006 | IAM design/test matrix | OPEN |
| ADR-006 | Entitlement independent from authorization | SEC-005 | TST-006 | Entitlement contract review | PARTIAL |
| ADR-007 | Server-rendered UI/HTMX/Tailwind | SEC-004–SEC-006 | TST-007 | UI/accessibility/security conventions | OPEN |
| ADR-008 | Selective DRF for approved consumers | SEC-005–SEC-007 | TST-008 | API exposure criteria | PARTIAL |
| ADR-009 | Celery/Redis execution; PostgreSQL authority | SEC-013 | TST-009 | Task contract/reliability specification | PARTIAL |
| ADR-010 | Transactional outbox and idempotent consumers | SEC-012, SEC-013 | TST-009, TST-013 | Outbox/event contract specification | PARTIAL |
| ADR-011 | Protected posted entries and linked correction | SEC-014 | TST-010 | Financial integrity principles plus open-policy record | PARTIAL |
| ADR-012 | Provider-neutral e-invoicing boundary | SEC-007, SEC-013, SEC-014 | TST-008, TST-009, TST-011 | Boundary approved; regulatory/provider decisions deferred | SATISFIED |
| ADR-013 | Decimal, currency, versioned rounding | SEC-014 | TST-010 | Principles approved; concrete matrix deferred | PARTIAL |
| ADR-014 | UUIDs and database-enforced tenant references | SEC-002 | TST-003, TST-004 | Identifier/constraint design for P01 | OPEN |
| ADR-015 | Risk-based CI gates and evidence | SEC-001, SEC-015 | TST-001–TST-018 | Approved testing strategy and CI evidence | OPEN |
| ADR-016 | Immutable Docker image and explicit roles | SEC-016, SEC-017 | TST-014, TST-015, TST-018 | Deployment design; provider/topology deferred | PARTIAL |
| ADR-017 | Typed config and runtime secret injection | SEC-011, SEC-015, SEC-016 | TST-015, TST-016 | Configuration/secrets standard | PARTIAL |
| ADR-018 | Separate audit/log/telemetry with minimization | SEC-009, SEC-012 | TST-013 | Audit/log taxonomy and retention decision route | OPEN |
| ADR-019 | Private object storage and governed files | SEC-008, SEC-009, SEC-017 | TST-012, TST-018 | File classification/lifecycle design; provider deferred | PARTIAL |
| ADR-020 | Versioned APIs and external contracts | SEC-007 | TST-008, TST-011 | Interface catalogue template and deprecation decision route | OPEN |

## 6. Quality Baseline Traceability

| Quality baseline | P00 use | Approval/evidence required | Current status |
|---|---|---|---|
| SEC-001–SEC-018 | Defines secure design, implementation, release, and operational controls | Security review, applicability decisions, approval record | APPROVED BASELINE |
| TST-001–TST-018 | Defines verification layers, negative tests, CI/release gates, and evidence | QA/Security/DevOps review and approval record | APPROVED BASELINE |
| ADR-015 acceptance criteria | Defines non-bypassable risk-based gates | Testing strategy plus initial CI evidence/approved exception | SATISFIED |
| P00 evidence rules | Prevents unsupported phase-status claims | Independent documentation and approval review | APPROVED BASELINE |

## 7. Exit Evidence Index

| Evidence ID | Evidence | Owner | State | Exit blocker |
|---|---|---|---|---|
| P00-EV-001 | Reviewed product baseline and scope/non-goals | Product | VERIFIED | Yes |
| P00-EV-002 | Requirement identifier and verification audit | QA / Documentation | VERIFIED | Yes |
| P00-EV-003 | Module ownership/dependency review | Architecture / Product | VERIFIED | Yes |
| P00-EV-004 | Accepted ADR register and approval record | Architecture | VERIFIED | Yes |
| P00-EV-005 | Architecture source reconciliation report | Architecture | VERIFIED | Yes |
| P00-EV-006 | Approved security requirements | Security | VERIFIED | Yes |
| P00-EV-007 | Approved testing strategy | QA / Security / DevOps | VERIFIED | Yes |
| P00-EV-008 | Validated P00 traceability matrix | QA / Governance | APPROVED | Yes |
| P00-EV-009 | Decision/risk/issue review | Product / Governance | VERIFIED | Yes |
| P00-EV-010 | Manifest schema and validation evidence | Governance / DevOps | VERIFIED | Yes |
| P00-EV-011 | Initial CI execution or approved exception | QA / DevOps | VERIFIED | Yes |
| P00-EV-012 | Bounded P01 specification | Product / Architecture / Security / QA | VERIFIED | Yes |
| P00-EV-013 | P00 completion and independent review report | Governance / Reviewers | READY_FOR_REVIEW | Yes |
| P00-EV-014 | Product Owner P00 exit approval | Product Owner | APPROVED | Yes |
| P00-EV-015 | Separate P01 implementation authorization | Product Owner | NOT_STARTED | Yes |

## 8. Open Traceability Gaps

| Gap ID | Gap | Owner | Blocks | Required resolution |
|---|---|---|---|---|
| P00-GAP-001 | Security requirements baseline | Security / Product | Resolved | Approved on 28 October 2026; implementation evidence remains phase-specific |
| P00-GAP-002 | Testing strategy baseline | QA / Security / DevOps / Product | Resolved | Approved on 28 October 2026; execution evidence remains phase-specific |
| P00-GAP-003 | Product baseline and scope/non-goals | Product | Resolved for planning baseline | Launch segment and release scope remain separate decisions |
| P00-GAP-004 | Phase identifier convention | Governance / Product | Resolved | Canonical `P00`–`P12`; legacy aliases are non-primary identifiers |
| P00-GAP-005 | Hosted CI execution evidence | Governance / QA / DevOps | Resolved | GitHub Actions run 40647091699 passed for commit 74267c5a2a2f495d8cf5b5e0b8efaec987c45301; artifact 12798425785 and its SHA-256 digest are recorded in P00-EV-011 |
| P00-GAP-006 | Bounded P01 specification and tenant-isolation matrix | Product / Architecture / Security / QA / Database / DevOps | Resolved for specification | Approved on 28 October 2026; all tests remain `NOT_RUN` and implementation is not authorized |
| P00-GAP-007 | Requirement-to-test evidence is design-level because application implementation has not started | QA | P01 and later exits | Populate executed evidence only through authorized tasks |
| P00-GAP-008 | Operational objectives, retention, providers, finance policies, and regulatory details remain open | Named decision owners | Later phase/production gates | Resolve by required-by phase; do not invent values |
| P00-GAP-009 | Independent P00 completion and P00-AC-015 review | Architecture / Security / QA / DevOps | P00 exit | Approve or reject P00-EV-013 using APPR-P00-001 |
| P00-GAP-010 | Initial implementation increment prerequisite is not explicitly reconciled with open DEC-PROD-001 | Product Owner | P00 exit | Approve bounded P01 as the initial implementation increment while retaining commercial launch scope for later, or amend the prerequisite explicitly |

## 9. Validation Rules

The matrix is valid only if:

1. P00, product, ADR, SEC, and TST identifiers resolve to an owning document.
2. Every P00 acceptance criterion appears exactly once in Section 3.
3. Every ADR-001 through ADR-020 appears exactly once in Section 5.
4. Every mandatory exit evidence item has an owner, state, and blocker designation.
5. `SATISFIED` rows link to actual documentation evidence.
6. Application tests are not marked passed before execution.
7. Deferred items name a later trigger and do not silently disappear.
8. Status changes are reviewed with the affected source documents and registers.

## 10. Approval

**Current Status:** APPROVED VERIFICATION BASELINE

- **Recommended disposition:** Use this approved verification baseline to close the remaining P00 implementation/evidence gaps without treating document approval as phase exit.
- **Approved By:** Product Owner — explicit market-standard review instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Matrix approval confirms traceability design, not application behavior or regulatory compliance.

## 11. Change Log

| Version | Date | Status | Description |
|---|---|---|---|
| 1.0 | 28 October 2026 | APPROVED VERIFICATION BASELINE | P00 traceability design approved; execution and exit evidence remain open. |
