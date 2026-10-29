# P03 — Requirements, Controls, Tests, and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P03-TRACE-001 |
| Status | READY FOR REVIEW |
| Governing Phase | [P03-SPEC-001](P03_PHASE_SPECIFICATION.md) |
| Test Status | All tests `NOT_RUN` until implementation evidence exists |

## 1. Status Vocabulary

`PLANNED` means defined but not implemented. `NOT_RUN` means executable but not executed for the cited commit/environment. `PASSED`, `FAILED`, and `BLOCKED` require recorded execution. `VERIFIED` requires evidence-backed review of an acceptance criterion.

## 2. Requirements-to-Control-to-Test Traceability

| Criteria | Source | Primary controls | Tests | Evidence |
|---|---|---|---|---|
| P03-AC-001–003 | CRM-001–003 | CRM ownership; tenant constraints; lifecycle; duplicate policy; permissions | P03-TST-001–018 | P03-EV-002–004, 009 |
| P03-AC-004–006 | SALES-001–005; SALESM-001–010 | Sales ownership; snapshots; server calculation; approval/conversion services | P03-TST-019–040 | P03-EV-002, 005 |
| P03-AC-007–008 | INV-001; ADR-013 | Validated draft; Decimal/currency/policy snapshot; server totals | P03-TST-041–053 | P03-EV-006, 013 |
| P03-AC-009–011 | INV-002; ADR-011 | Scoped sequence; transactional issue; frozen fields; DB/service protection | P03-TST-054–068 | P03-EV-006, 009, 011 |
| P03-AC-012 | INV-004 | Linked correction; remaining-credit limit; immutable original | P03-TST-069–078 | P03-EV-007, 013 |
| P03-AC-013–014 | INV-005 | Payment/receipt operation; allocation constraints; balance reconciliation | P03-TST-079–091 | P03-EV-007, 010 |
| P03-AC-015 | INV-003; ADR-019 | Snapshot render; private file; authorized download; content/retention controls | P03-TST-092–101 | P03-EV-008, 011 |
| P03-AC-016–017 | CRM/INV requirements; ADR-004–006 | Trusted context; permission AND entitlement; same-tenant FK/RLS | P03-TST-102–123 | P03-EV-009, 011 |
| P03-AC-018 | ADR-010, ADR-020 | Service boundary; outbox; versioned schemas; idempotent consumer/reconciliation | P03-TST-124–134 | P03-EV-010 |
| P03-AC-019 | ADR-018 | Audit allowlist/redaction; actor/tenant/reason/correlation | P03-TST-135–141 | P03-EV-011 |
| P03-AC-020 | NFR-005–007; ADR-014–016 | Clean/upgrade migration; overlap; backup/restore reconciliation; monitoring | P03-TST-142–152 | P03-EV-012 |
| P03-AC-021–022 | ADR-015; Roadmap 8.5 | CI gates; specialist/independent reviews; human exit | P03-TST-153–156 | P03-EV-011–014 |

## 3. Test Catalogue

### 3.1 CRM

| IDs | Scenarios | Expected result |
|---|---|---|
| P03-TST-001–008 | Customer create/update/retire; required fields; normalization; exact/fuzzy duplicate candidate; override; search | Controlled tenant-safe result; duplicate handling explicit and audited |
| P03-TST-009–012 | Contact relationship; primary contact; sensitive field permission; unrelated update | Valid same-tenant relationship and least-privilege visibility |
| P03-TST-013–018 | Lead/opportunity stage; invalid transition; assignment; inactive owner; activity; concurrent update | Approved state/owner history with no lost update |

### 3.2 Sales

| IDs | Scenarios | Expected result |
|---|---|---|
| P03-TST-019–024 | Commercial item create/retire; optional inventory mapping; stale/foreign reference; snapshot after master change; permission | Sales-owned reference works without stock mutation or historical drift |
| P03-TST-025–032 | Quotation draft; line validation; Decimal/currency; discount/rounding; revision; expiry; approval; unauthorized approval | Reproducible totals and preserved revision/approval history |
| P03-TST-033–040 | Accept/reject; stale revision; repeated acceptance; quote-to-order; manual order; invalid transition; cancellation; repeated invoice request | One authorized, idempotent, historically traceable result |

### 3.3 Invoice calculation, numbering, and issue

| IDs | Scenarios | Expected result |
|---|---|---|
| P03-TST-041–053 | Manual/source draft; customer/line/currency mismatch; zero/negative/overflow; quantity/unit price; discount; line/document rounding; tax policy absent/present; due date; client total tamper | Server rejects invalid input and reproduces authoritative totals |
| P03-TST-054–060 | Sequence scope; concurrent issue; retry; rollback after reservation; configuration change; exhausted/invalid sequence; unauthorized scope | Unique approved number with documented gap/recovery behavior |
| P03-TST-061–068 | Issue success; partial failure; issued field edit/delete through service/admin/API/import; current master change; repeated issue; cancellation; direct DB/runtime restriction | One immutable authoritative snapshot; no silent mutation |

### 3.4 Corrections, payments, and balances

| IDs | Scenarios | Expected result |
|---|---|---|
| P03-TST-069–078 | Full/partial credit; over-credit; cross-currency; wrong invoice/tenant; repeated credit; concurrent credits; credit document issue; cancellation/replacement; downstream event | Linked correction once; original preserved; balance accurate |
| P03-TST-079–091 | Payment record; partial/full; over-allocation; multi-invoice allocation; currency mismatch; duplicate reference/key; concurrent allocation; unallocate/reverse; cross-tenant; uncertain evidence; statement; reconciliation mismatch | Allocation constrained, reversible by policy, and reconcilable; no bank-truth claim |

### 3.5 Documents, security, isolation, and reliability

| IDs | Scenarios | Expected result |
|---|---|---|
| P03-TST-092–101 | Invoice/credit render; snapshot accuracy; locale/layout; visual golden; render failure/retry; private storage; authorization at download; expired link; unsafe content; regeneration | Accurate private artifact; no duplicate financial effect or data leak |
| P03-TST-102–111 | Missing entitlement; missing permission; role/object scope; direct URL; HTMX; API; service; task; report/export; admin | Every boundary independently enforces entitlement and authorization |
| P03-TST-112–123 | Cross-tenant list/detail/search/reference/conversion/issue/credit/payment/allocation/file/report/cache/task; guessed UUID/forged tenant | No disclosure, reference, or side effect across tenants |
| P03-TST-124–134 | Transaction rollback; crash before/after publish; duplicate/reordered consumer; stale lease; schema version overlap; poison event; replay; source/invoice reconciliation; invoice/accounting seam; invoice/e-invoice seam; restore replay | Durable, versioned, idempotent, observable recovery |
| P03-TST-135–141 | Lifecycle audit; issue/credit/payment audit; privileged read; assignment/approval; redaction; audit immutability; correlation | Sufficient durable evidence without prohibited data |
| P03-TST-142–152 | Clean install; upgrade; backfill; restricted role/RLS; rollback boundary; old/new code; queued schema; backup/restore; sequence reconciliation; file restore; monitoring alert | Supported deployment/recovery succeeds or fails safely |
| P03-TST-153–156 | Full CI; security/privacy review; finance/regulatory-readiness review; independent evidence reproduction | Gates pass and findings/limitations are dispositioned |

## 4. Required Test Levels

- Unit/property: normalization, duplicate rules, state machines, calculations, allocation, reason codes.
- Model/database: tenant keys, same-tenant references, uniqueness, sequence/locking, immutable snapshots, precision/range, RLS.
- Service: permissions, entitlements, approvals, idempotency, concurrency, rollback, correction, audit.
- View/API: forms, direct URL, HTMX, malformed input, pagination/filter scope, safe errors.
- Task/integration: document rendering, files, outbox, duplicate/reordered work, retries, reconciliation, future-domain seams.
- Migration/recovery: clean install, upgrade/backfill, old/new overlap, backup/restore and totals/balances/sequence reconciliation.
- Security/accessibility/performance: IDOR, mass assignment, XSS/CSV injection, private files, keyboard/labels/errors, search/list/issue concurrency and report bounds.

## 5. Evidence Index

| Evidence | Scope | Status |
|---|---|---|
| P03-EV-001 | Entry gate and policy snapshot | PLANNED |
| P03-EV-002 | Ownership/schema/migration design | PLANNED |
| P03-EV-003 | Customer/contact tests | PLANNED |
| P03-EV-004 | Lead/opportunity/activity tests | PLANNED |
| P03-EV-005 | Quotation/order tests | PLANNED |
| P03-EV-006 | Invoice calculation/numbering/issue tests | PLANNED |
| P03-EV-007 | Correction/payment/allocation tests | PLANNED |
| P03-EV-008 | Document/file/visual/accessibility tests | PLANNED |
| P03-EV-009 | Entitlement/authorization/isolation review | PLANNED |
| P03-EV-010 | Events/tasks/reconciliation resilience | PLANNED |
| P03-EV-011 | Security/privacy/audit review | PLANNED |
| P03-EV-012 | Migration/deployment/recovery/operations | PLANNED |
| P03-EV-013 | Finance/regulatory-readiness limitations | PLANNED |
| P03-EV-014 | Independent completion and Product Owner decision | PLANNED |

## 6. Exception Rules

No exception may waive tenant isolation, authorization, entitlement, issued-document integrity, exact money/currency rules, duplicate-financial-effect prevention, secret/sensitive-data protection, audit integrity, or required migration safety. Other exceptions require owner, scope, rationale, compensating control, linked risk, expiry, and human approval. Unresolved tax, legal, e-invoicing, accounting, or payment-provider functionality remains disabled.
