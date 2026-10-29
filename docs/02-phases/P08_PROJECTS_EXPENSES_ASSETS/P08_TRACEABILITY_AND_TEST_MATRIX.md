# P08 — Requirements, Controls, Tests and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P08-TRACE-001 |
| Status | APPROVED VERIFICATION BASELINE — APPLICATION TESTS NOT RUN |
| Test status | All tests `NOT_RUN` until implementation evidence exists |

## 1. Traceability

| Criteria | Sources | Controls | Tests | Evidence |
|---|---|---|---|---|
| P08-AC-001–003 | PROJ-001; ADR-003/005/006 | Approved scope; tenant-safe hierarchy/workflow; operational/financial boundary | P08-TST-001–035 | P08-EV-001–003 |
| P08-AC-004–008 | EXP-001; ADR-010/011/013/019 | Snapshots/Decimal; maker-checker; private files; idempotent posting/reimbursement | P08-TST-036–080 | P08-EV-004–007 |
| P08-AC-009–012 | FA-001/002; ADR-011/013 | Effective asset policy; deterministic immutable depreciation; linked disposal | P08-TST-081–120 | P08-EV-008–010 |
| P08-AC-013–014 | ADR-004–006/014/018–020 | Permission/entitlement/RLS; private files; redaction; safe surfaces | P08-TST-121–151 | P08-EV-011 |
| P08-AC-015–018 | NFR-006/007/009; ADR-015/016 | Migration/restore reconciliation; operations; independent and human gates | P08-TST-152–175 | P08-EV-012–014 |

## 2. Test Catalogue

| IDs | Scenarios | Expected result |
|---|---|---|
| P08-TST-001–010 | Approved/disabled scope; project code uniqueness; create/status; customer/member reference; wrong tenant; inactive customer; date/timezone; duplicate/concurrency; audit | One valid tenant-safe project or visible rejection |
| P08-TST-011–025 | Task/milestone create; parent/depth/cycle; dependency; assignment; project membership vs CRM/HR access; status/progress; stale/concurrent transition; close with open work; reopen/cancel; history | Bounded acyclic authorized lifecycle |
| P08-TST-026–035 | Project list/detail/report/export/API; object permission; entitlement; task/cache/report scoping; operational semantics; migration/restore hierarchy | Accurate non-financial project evidence |
| P08-TST-036–050 | Claimant user/employee/delegate; category/policy/effective dates; line/date/currency/Decimal/tax snapshot; project/customer reference; receipt upload/scan/checksum/version/access; missing/stale policy; client total tamper | Complete reproducible private draft or rejection |
| P08-TST-051–064 | Submit/return/reject/approve; maker-checker; self-approval; stale/concurrent approval; override/reason; approved mutation/delete; correction/cancel; duplicate receipt/merchant/date/amount; duplicate false positive; audit | One immutable approved version with linked correction |
| P08-TST-065–080 | Accounting/VAT map; posting request/duplicate/conflict/failure/retry/reorder/reversal; reimbursement prepare/approve; payroll/bank route; timeout/uncertain/reject/settle evidence; duplicate effect; reconciliation; report/export | Exact idempotent effects and evidence-based status |
| P08-TST-081–094 | Asset/category/policy create; source/acquisition/currency/cost/residual/in-service; duplicate; custodian/location; transfer/effective history; missing/overlap/stale policy; unauthorized change; asset evidence file | Complete stable asset and policy snapshot |
| P08-TST-095–108 | Straight-line approved method; period/day convention; useful life; residual boundary; rounding; partial period; leap/date edge; suspension disabled/enabled; deterministic rerun; batch/individual equality; stale/concurrent finalization; atomic failure | Exact reproducible depreciation or no commit |
| P08-TST-109–120 | Posted schedule mutation/delete; repeat run; accounting duplicate/conflict/retry; transfer; correction; disposal/proceeds; reversal; cost/depreciation/NBV equation; source-ledger reconciliation; period close | Immutable linked lifecycle and balanced reconciliation |
| P08-TST-121–136 | Role/action combinations across modules; object/field/sensitive amount/receipt access; entitlement disabled/expired; direct URL/API/admin/task; support purpose/expiry; bulk export; maker-checker | Least privilege and fail-closed enforcement |
| P08-TST-137–151 | Cross-tenant project/task/claim/receipt/asset/run/posting guessed UUID; RLS restricted/bypass role; cache/file/export/report leak; CSV injection; unsafe filenames/content; log/error/metric/trace redaction; audit completeness; accessibility | No cross-tenant/sensitive leakage; safe surface |
| P08-TST-152–163 | Clean/upgrade/backfill; old/new overlap; financial dry-run; rollback boundary; restore projects/claims/assets/files; claim/reimbursement totals; asset cost/depreciation/NBV; postings/outbox/audit | Preserved history and exact recovery reconciliation |
| P08-TST-164–170 | Load/batch depreciation/report; lock contention; monitoring/alerts; duplicate/reimbursement/depreciation/file incidents; backup restore drill; full CI/secret/exception scans | Operable within approved targets |
| P08-TST-171–175 | Project/Finance review; Security/Privacy/File review; Database/Operations review; independent reproduction/critical findings; Product Owner exit/production separation | Named reviews and bounded approval |

## 3. Evidence Index

P08-EV-001 approved scope/policies; P08-EV-002 project lifecycle/hierarchy; P08-EV-003 project permissions/reports; P08-EV-004 expense calculation/files; P08-EV-005 approval/immutability; P08-EV-006 posting/VAT; P08-EV-007 reimbursement/reconciliation; P08-EV-008 asset register/policy; P08-EV-009 depreciation; P08-EV-010 disposal/accounting; P08-EV-011 authorization/isolation/security/audit/surfaces; P08-EV-012 migration/recovery; P08-EV-013 performance/operations/full gates; P08-EV-014 domain/finance/security/independent completion and Product Owner decisions. All are `PLANNED`.

## 4. Exception Rules

No exception may waive tenant isolation, private receipt/evidence access, exact Decimal calculations, maker-checker for material financial effects, immutable approved/finalized history, duplicate-effect prevention, truthful settlement, audit or restore reconciliation. Unapproved project accounting, tax, reimbursement and asset policy remains disabled.
