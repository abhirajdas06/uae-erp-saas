# Repository Requirements Traceability Matrix

| Property | Value |
|---|---|
| Document ID | GOV-TRACE-001 |
| Status | DOCUMENTATION COVERAGE VERIFIED — IMPLEMENTATION TESTS NOT RUN |
| Baseline date | 29 October 2026 |
| Canonical requirements | [PRODUCT_REQUIREMENTS.md](../00-product/PRODUCT_REQUIREMENTS.md) |

## 1. Reading the Matrix

This matrix proves planned documentation coverage, not implemented behavior. `PLANNED` means the requirement has an owning phase, controls, acceptance and planned verification. `NOT_RUN` means no application test result is claimed. Phase matrices are authoritative for individual scenario ranges and evidence content.

| Requirements | Primary ADR/control | Module owner | Phase/task family | Acceptance / planned test | Evidence | State |
|---|---|---|---|---|---|---|
| PRD-001–004 | ADR-001, ADR-003, module catalogue | Platform/Product | P00; P02-T01/T02 | P00-AC-001–017; P02-AC-001–002 | P00-EV-001–015; P02-EV-001–003 | PLANNED |
| TEN-001–005 | ADR-002, ADR-004, ADR-014 | Tenants/Core | P01-T05/T06/T08 | P01-AC-008–023; P01 tenant matrix | P01-EV-003–007 | NOT_RUN |
| IAM-001–005 | ADR-005, ADR-017/018 | Users/Access | P01-T04/T07/T09; P11 privileged access | P01-AC-006–016/024–027; P11 matrix | P01-EV-005/008/009; P11 evidence | NOT_RUN |
| SUB-001–005 | ADR-006, ADR-010 | Subscription Management | P02-T03/T04 | P02-AC-003–005/014–017; P02-TST-010–026/082–112 | P02-EV-002/004/009–012 | NOT_RUN |
| BILL-001–004 | ADR-011/013/020 | SaaS Billing | P02-T07/T08/T09 | P02-AC-010–014; P02-TST-055–089 | P02-EV-007–009/012 | NOT_RUN |
| CRM-001–003 | ADR-003–006 | CRM | P03-T02/T03 | P03-AC-001–003; P03-TST-001–018 | P03-EV-002–004/009 | NOT_RUN |
| SALES-001–005 | ADR-003/006/010/013/018–020 | Sales | P03-T04/T05 | P03-AC-004–006/016–020; P03-TST-019–040/102–152 | P03-EV-002/005/009–012 | NOT_RUN |
| INV-001–005 | ADR-011/013/019 | ERP Invoicing | P03-T06–T10 | P03-AC-007–015; P03-TST-041–101 | P03-EV-006–008/013 | NOT_RUN |
| EIN-001–005 | ADR-012/020; ARCH-PINT-AE-002/MAP-001 | UAE E-Invoicing | P04 task pack | P04-AC-001–018; P04-TST-001–139 | P04-EV-001–014 | NOT_RUN |
| ACC-001–005 | ADR-011/013 | Accounting | P05 accounting tasks | P05 accounting/posting/period AC; matrix tests | P05 accounting/ledger evidence | NOT_RUN |
| VAT-001–003 | REG-SRC-001; ADR-011/013 | UAE VAT | P05 VAT tasks | P05 tax/rules/report AC; matrix tests | P05 tax/specialist evidence | NOT_RUN |
| INVN-001–002 | ADR-003/010/011 | Procurement | P06 procurement tasks | P06 procurement/supplier AC; matrix tests | P06 procurement evidence | NOT_RUN |
| INVN-003–005 | ADR-011/013/014 | Inventory | P06 inventory tasks | P06 movement/count/valuation AC; matrix tests | P06 inventory/reconciliation evidence | NOT_RUN |
| HR-001–002 | ADR-005/018/019 | HRMS | P07 HR tasks | P07 HR/privacy AC; matrix tests | P07 HR/security evidence | NOT_RUN |
| PAY-001–003 | ADR-011/013/018 | Payroll | P07 payroll/WPS tasks | P07 payroll/posting/WPS AC; matrix tests | P07 payroll/specialist evidence | NOT_RUN |
| PROJ-001 | ADR-003/014 | Projects | P08 project tasks | P08 project AC; matrix tests | P08 project evidence | NOT_RUN |
| EXP-001 | ADR-011/018/019 | Expenses | P08 expense tasks | P08 expense/approval/payment AC; matrix tests | P08 expense evidence | NOT_RUN |
| FA-001–002 | ADR-011/013 | Fixed Assets | P08 asset tasks | P08 asset/depreciation/disposal AC; matrix tests | P08 asset/finance evidence | NOT_RUN |
| BANK-001–003 | ADR-010/017–020; banking contract | Banking | P09 import/reconciliation tasks | P09 bank/reconciliation AC; matrix tests | P09 banking/security evidence | NOT_RUN |
| REP-001–003 | ADR-004–006/015/019 | Reporting | P10 reporting tasks | P10 report/export/reconciliation AC; matrix tests | P10 report/isolation evidence | NOT_RUN |
| INT-001–002 | ADR-010/017/020 | Integrations + domain adapters | P04/P09/P10 integration tasks | Respective callback/contract AC and tests | Respective provider/security evidence | NOT_RUN |
| AUD-001 | ADR-018 | Audit Foundation | P01-T09; P11 hardening | P01-AC-024–027; P11 audit tests | P01-EV-008; P11 review | NOT_RUN |
| OPS-001 | ADR-017/018 | Core/Operations | P01-T09/T10; P12 | Logging/diagnostic/operations AC | P01-EV-008/010; P12 evidence | NOT_RUN |
| OPS-002 | ADR-009/010 | Shared async/domain owner | P02+ durable-task tasks | Phase resilience/idempotency AC/tests | Phase task/outbox/reconciliation evidence | NOT_RUN |
| OPS-003–004 | ADR-015–017/019 | Operations | P11/P12 recovery/monitoring | P11/P12 recovery/alert AC/tests | P11/P12 operational evidence | NOT_RUN |
| NFR-001–003 | ADR-004/005/015/017–019 | All | P01 foundation; every phase security gate | SEC controls and phase negative tests | Security review per phase | NOT_RUN |
| NFR-004–005 | DEP-CAP-001; ADR-015 | All/Operations | P10/P11/P12 performance tasks | Defined workload/SLO/query AC | Capacity/performance evidence | NOT_RUN |
| NFR-006–007 | ADR-009/010/020 | All service owners | P02+ failure/retry tasks | Failure/idempotency/concurrency tests | Phase resilience evidence | NOT_RUN |
| NFR-008–009 | ADR-014–016 | Engineering/Database | Every implementation/CI/migration task | CI, migration and compatibility gates | Phase CI/migration evidence | NOT_RUN |
| NFR-010–011 | Deployment/backup specifications | Operations | P11/P12 | SLO/RPO/RTO and restore AC/tests | Measured operations/recovery evidence | NOT_RUN |
| NFR-012–013 | UI/localization controls | Product/UI | P03+, P11 | Locale/RTL/accessibility scenarios | UX/accessibility evidence | NOT_RUN |
| DEP-001–002 | ADR-016/017 | DevOps | P00/P01 bootstrap; P12 | Reproducible deploy/config AC | CI/build/config evidence | PARTIAL: documentation/initial CI only |
| DEP-003 | ADR-015–017; release criteria | Release/Operations | P12 | P12 release/deploy/launch gates | P12 signed evidence | NOT_RUN |

## 2. Phase Document Coverage

### 2.1 Explicit requirement coverage anchors

The following individual IDs are deliberately enumerated so automated reference checks can distinguish explicit coverage from a prose range:

- P00/product: PRD-001, PRD-002, PRD-003, PRD-004.
- P01/core: TEN-001, TEN-002, TEN-003, TEN-004, TEN-005; IAM-001, IAM-002, IAM-003, IAM-004, IAM-005; AUD-001; OPS-001.
- P02/commercial: SUB-001, SUB-002, SUB-003, SUB-004, SUB-005; BILL-001, BILL-002, BILL-003, BILL-004.
- P03/customer: CRM-001, CRM-002, CRM-003; SALES-001, SALES-002, SALES-003, SALES-004, SALES-005; INV-001, INV-002, INV-003, INV-004, INV-005.
- P04/e-invoicing: EIN-001, EIN-002, EIN-003, EIN-004, EIN-005.
- P05/finance: ACC-001, ACC-002, ACC-003, ACC-004, ACC-005; VAT-001, VAT-002, VAT-003.
- P06/supply: INVN-001, INVN-002, INVN-003, INVN-004, INVN-005.
- P07/people: HR-001, HR-002; PAY-001, PAY-002, PAY-003.
- P08/operations: PROJ-001; EXP-001; FA-001, FA-002.
- P09/banking: BANK-001, BANK-002, BANK-003.
- P10/reporting/integration: REP-001, REP-002, REP-003; INT-001, INT-002.
- Cross-phase operations: OPS-002, OPS-003, OPS-004; NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-006, NFR-007, NFR-008, NFR-009, NFR-010, NFR-011, NFR-012, NFR-013; DEP-001, DEP-002, DEP-003.

### 2.2 Integrated phase artifact disposition

| Phase | Specification | Trace/test plan | Task prompts | Deployment/operations coverage | Disposition |
|---|---|---|---|---|---|
| P00 | `P00_PHASE_SPECIFICATION.md` | `P00_TRACEABILITY_MATRIX.md` | Manifest/task schema | Integrated P00 CI/evidence | Present |
| P01 | `P01_PHASE_SPECIFICATION.md` | Tenant-isolation matrix | Orchestration + `P01_BOUNDED_TASK_PROMPTS.md` | Integrated AC/evidence | Present |
| P02–P12 | One phase specification per phase | One traceability/test matrix per phase | Orchestration + bounded prompts | Phase sections plus canonical deployment docs | Present |

Separate `MVP.md`, `TASKS.md`, `ACCEPTANCE_CRITERIA.md`, `TEST_PLAN.md` and `DEPLOYMENT_REQUIREMENTS.md` files are `NOT_APPLICABLE_DUPLICATE`: their required content is integrated into the phase specification, phase matrix and prompt pack. This disposition avoids competing sources of truth.

## 3. Known Gaps and Gates

- Implementation, security, migration, provider and operational tests are not run unless cited by a concrete evidence file.
- Regulated and specialist-dependent behavior remains gated in `DECISIONS_PENDING.md`.
- Numeric performance, availability, RPO/RTO and retention values require Product/Operations/Legal approval and measured evidence.
- PINT AE `1.0.4` is a current technical candidate, not production approval or compliance certification.
- This matrix must be updated when a requirement, phase AC/test range, task or evidence status changes.
