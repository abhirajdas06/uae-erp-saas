# P07 — Requirements, Controls, Tests and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P07-TRACE-001 |
| Status | READY FOR REVIEW |
| Test status | All tests `NOT_RUN` until implementation evidence exists |

## 1. Traceability

| Criteria | Sources | Controls | Tests | Evidence |
|---|---|---|---|---|
| P07-AC-001 | HR/PAY requirements; REG-HR-001 | Dated sources; applicability/ruleset approval; disabled exclusions | P07-TST-001–014 | P07-EV-001–002, 015 |
| P07-AC-002–006 | HR-001/002; ADR-018/019 | Effective employment; identity separation; field/file/privacy; leave ledger | P07-TST-015–062 | P07-EV-003–005, 011–012 |
| P07-AC-007–13 | PAY-001–003; ADR-010/011/013 | Effective payroll rules; immutable snapshots/results; maker-checker; idempotent posting | P07-TST-063–122 | P07-EV-006–009 |
| P07-AC-014–015 | REG-HR-001; INT requirements | Exact WPS/pension applicability/contracts; secure operations/reconciliation | P07-TST-123–143 | P07-EV-002, 010, 015 |
| P07-AC-016–018 | ADR-004–008/017–020 | Entitlement/field/object/RLS; privacy/audit; safe UI/API/files/exports | P07-TST-144–172 | P07-EV-011–012 |
| P07-AC-019–021 | NFR-006/007/009; ADR-015/016 | Migration/recovery reconciliation; operations; specialist/independent/human gates | P07-TST-173–196 | P07-EV-013–015 |

## 2. Test Catalogue

| IDs | Scenarios | Expected result |
|---|---|---|
| P07-TST-001–014 | Current source/checksum; amendment; employer jurisdiction/category; government/domestic/free-zone exclusion; employee nationality/work pattern; contract/permit facts; leave/payroll/WPS/pension/privacy ruleset; stale/ambiguous/missing policy; effective date; disabled scenario | Only exact approved applicable ruleset; otherwise fail closed |
| P07-TST-015–026 | Employee create/normalize/duplicate; employment create/status/effective dates; overlap; entity/department/designation; employee-user link/provision/revoke; rehire; terminate; wrong tenant; current-master change; history/audit | Tenant-safe effective history without identity conflation |
| P07-TST-027–038 | Field-level profile/compensation/bank/pension/nationality/medical access; manager/object scope; self-service; support purpose/expiry; bulk export; redaction; employee document upload/scan/checksum/version/download; retention/legal hold/disposal | Least data and private controlled evidence |
| P07-TST-039–052 | Leave type/policy/effective assignment; eligibility; accrual/proration; calendar/day; overlap; balance/negative/carryover/expiry; request/approval; stale/concurrent approval; evidence; cancel/correct; direct balance edit; payroll impact | Reproducible approved append-oriented leave result |
| P07-TST-053–062 | Employment/contract/compensation retroactivity; payroll-impact detection; inactive/terminated behavior; document expiry; self-service update approval; import preview; duplicate import; report/export; privacy request; restore leave history | Controlled workflow with no finalized-pay rewrite |
| P07-TST-063–074 | Calendar/period; rule/component/effective assignment; overlap; employee eligibility; salary/input/leave/time snapshot; currency/precision; missing/stale/duplicate input; retro input; client total tamper; snapshot hash | Complete immutable payroll input or visible rejection |
| P07-TST-075–090 | Fixed/variable earning; deduction; proration; unpaid leave; overtime disabled/enabled; gross/deduction/net; line/run rounding; negative/zero/overflow; partial period; retro disabled/enabled; multi-currency disabled; golden fixtures; property invariants; reproducibility | Exact approved Decimal calculation |
| P07-TST-091–103 | Calculate/recalculate draft; exception; maker-checker; stale approval; concurrent approval/finalize; atomic failure; repeat/idempotency; changed payload/key; final result/payslip mutation/delete via all paths; correction/off-cycle/reversal | One immutable finalized result or none; linked correction only |
| P07-TST-104–113 | Payslip snapshot/render/locale/accessibility; private file; self-service authorization; failure/retry; regeneration/version; unsafe content; expired link; current-master change; bulk generation bounds | Accurate private historical payslip, no pay effect |
| P07-TST-114–122 | Accounting request/result; component mapping; source/purpose uniqueness; duplicate/conflict; closed period; failure/retry/reorder; correction/reversal; payroll-ledger reconciliation | Versioned idempotent posting with exact reconciliation |
| P07-TST-123–136 | WPS applicability; exact SIF/agent contract; prepare/approve; private/encrypted/checksummed file; duplicate operation; changed payload; secure export/upload boundary; provider response; rejection; timeout/uncertain; correction; settlement distinction; employee/period totals; reconciliation | Exact secure WPS evidence without fabricated acceptance/settlement |
| P07-TST-137–143 | Pension authority/law cohort; applicable/inapplicable employee; contribution basis/rate/ceiling from approved version; retro change; rounding; export/filing disabled; reconciliation | Only approved cohort calculation/output |
| P07-TST-144–154 | Permission/entitlement combinations; HR/payroll config; calculate/approve/finalize; WPS prepare/approve; post; report/export; self-service; direct URL/API/task/admin; support | Least privilege/maker-checker on every path |
| P07-TST-155–164 | Cross-tenant/entity employee/employment/leave/input/run/result/payslip/WPS/file/report/cache/RLS guessed UUID | No inference, reference or effect |
| P07-TST-165–172 | Log/error/metric/trace/audit scan; sensitive export; API decimals/timestamps; CSV injection; accessibility; report semantics; pagination/bounds; claims wording | Safe accurate non-misleading surfaces/evidence |
| P07-TST-173–184 | Clean/upgrade/backfill; restricted role/RLS; precision/ruleset change; old/new overlap; rollback boundary; employee/history/leave restore; payroll totals; payslip files; posting; WPS; outbox/audit; retention metadata | History and totals preserved/reconciled |
| P07-TST-185–191 | Calculation/load; bulk payslip; locking; monitoring/alerts; payroll/WPS/privacy incident runbooks; restore drill; full CI/secret/exception scans | Operable within approved targets |
| P07-TST-192–196 | HR/Payroll/Finance review; UAE Legal/WPS/Pension/Privacy review; Security/Database/Operations review; independent reproduction/defects; Product Owner exit/production separation | Named reviews and exact bounded approval |

## 3. Evidence Index

P07-EV-001 regulatory/applicability baseline; P07-EV-002 approved HR/payroll/WPS/pension/privacy policy; P07-EV-003 employee/employment; P07-EV-004 files/privacy; P07-EV-005 leave; P07-EV-006 rules/inputs; P07-EV-007 calculation; P07-EV-008 approval/finalization/correction; P07-EV-009 payslip/accounting; P07-EV-010 WPS/pension; P07-EV-011 authorization/isolation/RLS; P07-EV-012 security/privacy/audit/surfaces; P07-EV-013 migration/recovery; P07-EV-014 performance/operations/full gates; P07-EV-015 specialist/independent completion/Product Owner decisions. All are `PLANNED`.

## 4. Exception Rules

No exception may waive sensitive-data/tenant isolation, purpose/field authorization, maker-checker, deterministic Decimal calculation, immutable finalized pay, duplicate-effect prevention, secure WPS evidence, truthful settlement/status claims, audit or migration/recovery reconciliation. Unapproved employment, leave, payroll, pension, WPS and privacy behavior remains disabled.
