# P10 — Requirements, Controls, Tests and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P10-TRACE-001 |
| Status | READY FOR REVIEW |
| Test status | All tests `NOT_RUN` until implementation evidence exists |

## 1. Traceability

| Criteria | Sources | Controls | Tests | Evidence |
|---|---|---|---|---|
| P10-AC-001–006 | REP-001–003; ADR-013/018/019 | Versioned catalogue/semantics; source reconciliation; bounded execution; private exports | P10-TST-001–070 | P10-EV-001–006 |
| P10-AC-007–011 | INT-001/002; ADR-009/010/012/017/020 | Registry/secrets refs; durable operations; callback auth; retry/reconcile; domain boundary | P10-TST-071–125 | P10-EV-007–010 |
| P10-AC-012–013 | ADR-004–008/014/018–020 | Permissions/entitlements/RLS; redaction/audit; safe surfaces | P10-TST-126–150 | P10-EV-011 |
| P10-AC-014–017 | NFR-004–011; ADR-015/016 | Migration/restore; capacity/operations; independent/human gates | P10-TST-151–175 | P10-EV-012–014 |

## 2. Test Catalogue

| IDs | Scenarios | Expected result |
|---|---|---|
| P10-TST-001–015 | Catalogue/owner/version; source unavailable; metric definition; parameter schema; date/as-of/timezone; currency/rounding; null/late/uncertain; changed master; current vs historical; unsupported KPI; audit | Exact approved reproducible semantics |
| P10-TST-016–035 | Tenant/role/object/field/entitlement filters; direct URL/API/task/admin; cross-tenant joins; aggregate inference; saved filters; scheduled run; cache key/invalidation; support purpose; sensitive HR/payroll/bank; guessed UUID; RLS | No inference or cross-scope data |
| P10-TST-036–050 | Accounting/source reconciliation; opening/movement/closing; report/snapshot repeat; stale source; correction/backdate; definition upgrade; multi-currency; totals/drilldown; dashboard refresh; provenance; discrepancy workflow | Named source totals and visible variance |
| P10-TST-051–070 | Row/time/memory/concurrency quotas; cancellation; async/retry/idempotency; queue fairness; pagination; export CSV/PDF policy; formula injection; private artifact; hash/expiry; delivery reauthorization; bulk export; accessibility/locale/RTL; load | Safe bounded reporting and export |
| P10-TST-071–085 | Registry definition; tenant config; environment separation; unsupported capability; enable/disable; credential reference; secret read/rotate/revoke; permission; provider/legal/version evidence; contract drift; audit | Exact approved connection with no secret exposure |
| P10-TST-086–105 | Durable operation; outbox commit/publish; duplicate delivery; stable/changed idempotency; timeout before/after send; uncertain outcome; transient/permanent/rate limit; bounded jitter retry; circuit/degradation; scheduler singleton; dead letter; replay approval; domain rejection; reconciliation | No lost or duplicate business effect |
| P10-TST-106–125 | Webhook signature/certificate/token; body integrity; timestamp/replay; oversize/schema; unknown connection; tenant spoof; duplicate/reordered callback; inbox crash/recovery; native evidence; status mapping; log redaction; provider health; callback outage; contract tests; emergency disable | Authenticated replay-safe evidence and trusted routing |
| P10-TST-126–140 | Cross-tenant registry/operation/inbox/outbox/health/cache/file/report; role/action matrix; entitlement; support access; logs/errors/metrics/traces; payload/secret redaction; audit correlation; retention/hold/disposal | Least privilege and minimized evidence |
| P10-TST-141–150 | UI/API decimals/timestamps/errors; accessibility; pagination/filter abuse; CSV/HTML injection; safe diagnostics; claims wording; health semantics; notification safety; documentation/OpenAPI/schema compatibility | Safe accurate interfaces/contracts |
| P10-TST-151–162 | Clean/upgrade/backfill; definition/contract coexistence; restricted role/RLS; rollback boundary; restore catalogue/snapshots/artifacts; registry/operations; inbox/outbox; domain links; secrets references; audit; reconciliation | History and operational state recoverable |
| P10-TST-163–170 | Report/integration load; queue/DB capacity; provider degradation; monitoring/alerts; report/export/webhook/credential incidents; restore drill; full CI/security/exception scans | Operable within approved targets |
| P10-TST-171–175 | Domain/Finance review; Security/Privacy/Integration review; Database/Operations review; independent reproduction/critical findings; Product Owner exit/activation separation | Named reviews and bounded decisions |

## 3. Evidence Index and Exceptions

P10-EV-001 catalogue/semantics; P10-EV-002 report authorization; P10-EV-003 source reconciliation; P10-EV-004 resource/performance; P10-EV-005 export/files; P10-EV-006 report surfaces; P10-EV-007 registry/secrets; P10-EV-008 operation/outbox/retry; P10-EV-009 webhook/inbox; P10-EV-010 provider/domain reconciliation; P10-EV-011 isolation/security/audit; P10-EV-012 migration/recovery; P10-EV-013 capacity/operations/full gates; P10-EV-014 independent review and approvals. All are `PLANNED`.

No exception may waive tenant isolation, source reconciliation for financial reports, export authorization, secret protection, callback authentication, duplicate-effect prevention, uncertain-outcome reconciliation, domain ownership, audit or restore evidence.
