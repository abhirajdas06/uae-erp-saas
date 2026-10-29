# P04 — Requirements, Controls, Tests and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P04-TRACE-001 |
| Status | READY FOR REVIEW |
| Test status | All tests `NOT_RUN` until implementation evidence exists |

`PLANNED` defines a future test; it is not a pass. `VERIFIED` requires reproducible evidence for the exact commit, environment, ruleset, adapter and provider contract.

## 1. Traceability

| Criteria | Sources | Controls | Tests | Evidence |
|---|---|---|---|---|
| P04-AC-001–002 | EIN-001; REG-SRC-001; ADR-012 | Dated source/applicability register; provider due diligence; version pinning | P04-TST-001–012 | P04-EV-001, 003, 013 |
| P04-AC-003–005 | EIN-001–002; INV-001/004 | Immutable source/hash; canonical snapshot; preflight; domain boundary | P04-TST-013–032 | P04-EV-002, 004 |
| P04-AC-006–007 | EIN-002/004; ADR-010 | Operation/outbox; idempotency; attempts; uncertainty/reconciliation | P04-TST-033–052 | P04-EV-005–006 |
| P04-AC-008–010 | EIN-003–004; INT-002 | Native/internal status mapping; authenticated callbacks; correction links | P04-TST-053–076 | P04-EV-006–007 |
| P04-AC-011–012 | ADR-004/005/006/017–019 | Permission AND entitlement; RLS; secret/payload minimization; audit | P04-TST-077–104 | P04-EV-008–009, 011 |
| P04-AC-013 | ADR-007/008/020 | Explicit UX/status semantics; safe/bounded API/report/export | P04-TST-105–114 | P04-EV-008 |
| P04-AC-014–015 | NFR-006/007/009; OPS-002/003 | Version compatibility; recovery; monitoring; contract/failure tests | P04-TST-115–138 | P04-EV-004–006, 010, 012 |
| P04-AC-016–018 | PRD-004; Roadmap 9 | Claims review; specialist/independent review; human exit/activation | P04-TST-139–144 | P04-EV-013–014 |

## 2. Test Catalogue

| IDs | Scenarios | Expected result |
|---|---|---|
| P04-TST-001–006 | Source/version retrieval; amendment/supersession; stale source; applicability category/effective date; ambiguous facts; disabled exclusion | Only approved current ruleset qualifies; ambiguity/staleness fails closed |
| P04-TST-007–012 | Provider accreditation snapshot; contract capability/version/environment; unsupported type; expired credential/cert; sandbox/prod separation; provider portability gap | Exact approved provider contract or safe rejection |
| P04-TST-013–022 | Invoice/credit source/version/hash; party/line/tax/currency/totals; conditional/missing fields; correction link; current-master change; foreign tenant/source | Exact immutable canonical snapshot or validation finding |
| P04-TST-023–032 | PINT/provider mapping golden cases; decimal strings; code lists; serialization/hash; schema mismatch; adapter capability; payload minimization; provider-specific leakage; historical version read | Deterministic versioned mapping with no fabricated value |
| P04-TST-033–042 | Atomic prepare/outbox; send success/rejection; duplicate command; changed payload/key; concurrent submit; crash before/after send; worker replay; transient retry; permanent error | One durable operation; no duplicate external/business effect |
| P04-TST-043–052 | Timeout; connection loss; missing response; inquiry success/not found/ambiguous; bounded backoff; retry exhaustion; manual reconcile; repeat action; provider outage | Uncertain outcome reconciled before any resubmission |
| P04-TST-053–062 | Native/internal mapping; unsupported status; valid/invalid/regressive transition; duplicate/reordered evidence; terminal conflict; sent vs acknowledged vs accepted; mapping upgrade; historical display | Evidence-based, non-regressing, versioned status |
| P04-TST-063–070 | Valid signature/mTLS contract; invalid/missing auth; replay; wrong account/tenant; duplicate/reordered callback; unknown reference; body tamper | Reject/quarantine safely; no disclosure or side effect |
| P04-TST-071–076 | Provider rejection; operator resolution; credit/correction; original preservation; repeated correction operation; status/source reconciliation | Linked traceable remediation without history rewrite |
| P04-TST-077–088 | Permission/entitlement combinations; direct URL/API/HTMX/task/admin/report/export; configuration vs payload access; support purpose/expiry; production activation | Least privilege independently enforced |
| P04-TST-089–100 | Cross-tenant list/detail/source/account/operation/callback/file/cache/task/report; guessed UUID/forged tenant/RLS role | No cross-tenant inference, reference or effect |
| P04-TST-101–104 | Log/error/metric/trace/export/audit secret and payload scanning; encrypted evidence; retention/disposal | No prohibited disclosure; policy-controlled evidence |
| P04-TST-105–114 | Status labels/actions; uncertainty/rejection UX; accessibility; pagination/filter; decimal/timestamp API; report semantics; CSV injection; payload download; audit timeline; claims text | Accurate, accessible, bounded and non-misleading surfaces |
| P04-TST-115–124 | Clean/upgrade/backfill; restricted role/RLS; old/new adapter/schema/status map; rollback boundary; backup/restore; outbox replay; provider cutover; evidence export | Historical meaning and reconciliation preserved |
| P04-TST-125–138 | Rate limit/load; latency/backlog; poison message; circuit/outage; callback burst; monitoring/alerts; runbooks; credential rotation; schema deprecation; sandbox contract; end-to-end; recovery drill; full CI | Bounded resilient operation with actionable evidence |
| P04-TST-139–144 | Regulatory source review; provider/legal/security/privacy review; claims review; independent reproduction; defect/exception disposition; exit/activation separation | Named reviewers approve exact scope; no inferred compliance |

## 3. Evidence Index

| Evidence | Scope | Status |
|---|---|---|
| P04-EV-001 | Regulatory sources, applicability and approved/disabled ruleset | PLANNED |
| P04-EV-002 | Canonical snapshot/data/validation design | PLANNED |
| P04-EV-003 | Provider due diligence, accreditation and contract approval | PLANNED |
| P04-EV-004 | Adapter/schema/status contract suite | PLANNED |
| P04-EV-005 | Durable operation/idempotency/failure suite | PLANNED |
| P04-EV-006 | Callback/status/reconciliation suite | PLANNED |
| P04-EV-007 | Rejection/correction/operator workflow suite | PLANNED |
| P04-EV-008 | UI/API/report/accessibility review | PLANNED |
| P04-EV-009 | Tenant isolation/authorization/entitlement/RLS review | PLANNED |
| P04-EV-010 | Operations/monitoring/runbook evidence | PLANNED |
| P04-EV-011 | Security/privacy/secrets/payload/audit review | PLANNED |
| P04-EV-012 | Migration/backup/restore/cutover evidence | PLANNED |
| P04-EV-013 | Qualified UAE regulatory and claims review | PLANNED |
| P04-EV-014 | Independent completion and Product Owner decisions | PLANNED |

## 4. Exception Rules

No exception may waive tenant isolation, callback authenticity, authorization/entitlement, secret protection, immutable source/snapshot evidence, idempotency/uncertainty controls, truthful statuses/claims, or migration/recovery safety. Other exceptions require owner, risk, compensating control, expiry and approval. Unverified/provider-dependent behavior remains disabled.
