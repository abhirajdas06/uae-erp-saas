# P02 — Requirements, Controls, Tests, and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P02-TRACE-001 |
| Status | READY FOR REVIEW |
| Governing Phase | [P02-SPEC-001](P02_PHASE_SPECIFICATION.md) |
| Test Status | All tests `NOT_RUN` until implementation evidence exists |

## 1. Status Vocabulary

- `PLANNED`: test/control defined but implementation not authorized or complete.
- `NOT_RUN`: executable test exists but has not run for the cited commit/environment.
- `PASSED`, `FAILED`, `BLOCKED`: evidence-backed execution outcomes only.
- `VERIFIED`: acceptance criterion reviewed against complete cited evidence.

## 2. Traceability Matrix

| Phase criterion | Source requirements | Primary controls | Required tests | Evidence |
|---|---|---|---|---|
| P02-AC-001 | SUB-002, roadmap 7.1–7.2 | Versioned registry; separate lifecycle/release/sale flags; authorization | P02-TST-001–004 | P02-EV-002–003 |
| P02-AC-002 | SUB-003–004 | Directed dependency graph; cycle/closure validation; preview | P02-TST-005–009 | P02-EV-003 |
| P02-AC-003 | SUB-001, SUB-004–005 | State machine; row/version lock; idempotency; history | P02-TST-010–016 | P02-EV-004 |
| P02-AC-004 | SUB-004–005 | Policy-gated transitions; disabled undecided flows | P02-TST-017–023 | P02-EV-001, 004 |
| P02-AC-005 | SUB-004–005 | No cascade to business records; degraded-access contract | P02-TST-024–026 | P02-EV-004–005 |
| P02-AC-006 | SUB-003 | Structured central decision; deny-by-default | P02-TST-027–034 | P02-EV-005 |
| P02-AC-007 | SUB-003, SEC-AUTHZ controls | Permission AND entitlement composition at every boundary | P02-TST-035–043 | P02-EV-005, 010 |
| P02-AC-008 | SUB-003 | Scoped/time-bound override, dual authorization where approved, audit | P02-TST-044–047 | P02-EV-006, 012 |
| P02-AC-009 | SUB-003 | Tenant/policy cache key; invalidation; TTL; authoritative sensitive check | P02-TST-048–054 | P02-EV-006 |
| P02-AC-010 | BILL-001 | Separate apps, models, services, permissions, numbering | P02-TST-055–058 | P02-EV-002, 007 |
| P02-AC-011 | BILL-002 | Versioned prices; Decimal; currency/rounding snapshots | P02-TST-059–066 | P02-EV-007 |
| P02-AC-012 | BILL-003 | Issue transition; immutable snapshot; linked corrections | P02-TST-067–073 | P02-EV-007 |
| P02-AC-013 | BILL-004 | Verified inbound event; inbox dedupe; explicit uncertain state | P02-TST-074–081 | P02-EV-008 |
| P02-AC-014 | BILL-004, OPS-002 | Transactional outbox; idempotent consumers; reconciliation | P02-TST-082–089 | P02-EV-009 |
| P02-AC-015 | SUB-001–005, BILL-001–004 | Trusted tenant context; same-tenant constraints; RLS defense | P02-TST-090–101 | P02-EV-010 |
| P02-AC-016 | SUB-002–005, BILL-003–004 | Audit allowlist/redaction; actor/tenant/correlation/reason | P02-TST-102–106 | P02-EV-012 |
| P02-AC-017 | NFR-005–007 | Clean/upgrade migration; restricted role; overlap contract | P02-TST-107–112 | P02-EV-011 |
| P02-AC-018 | NFR-006–007 | Metrics/alerts/runbooks/reconciliation dashboards | P02-TST-113–118 | P02-EV-013 |
| P02-AC-019 | ADR-015; quality baselines | CI gates and independent specialist reviews | P02-TST-119–121 | P02-EV-010–013 |
| P02-AC-020 | Roadmap 7.6 | Immutable evidence index; independent report; human approval | P02-TST-122 | P02-EV-014 |

## 3. Test Catalogue

### 3.1 Catalogue and dependency tests

| IDs | Scenarios | Expected result |
|---|---|---|
| P02-TST-001–004 | Stable module code; independent lifecycle/release/sale flags; unauthorized publication; effective-date overlap | Invalid configuration is rejected and audited |
| P02-TST-005–009 | Direct/indirect cycle; missing hard dependency; conditional/alternative dependency; retired module; no-silent-paid-dependency | Preview/commit returns deterministic rejection or explicit customer-approved change |

### 3.2 Subscription lifecycle tests

| IDs | Scenarios | Expected result |
|---|---|---|
| P02-TST-010–016 | Create; invalid transition; repeated key; conflicting key; optimistic/pessimistic concurrency; rollback; history | One valid aggregate result, no partial or duplicate effect |
| P02-TST-017–023 | Upgrade; downgrade; add/remove; suspend; cancel/expire; reactivate; undecided policy | Approved transition executes; undecided flow remains disabled |
| P02-TST-024–026 | Remove/expire with historical business records; export/read policy; in-flight operation | Records remain owned and retained; only approved degraded operations work |

### 3.3 Entitlement and authorization tests

| IDs | Scenarios | Expected result |
|---|---|---|
| P02-TST-027–034 | Active; pending; suspended; expired; missing/unknown module; invalid graph; future entitlement; absent tenant context | Structured deterministic decision; deny unless explicitly allowed |
| P02-TST-035–043 | UI; direct URL; HTMX; API; service; task; report/export; file; Django admin | Both tenant entitlement and user permission enforced |
| P02-TST-044–047 | Unauthorized override; valid override; expiry; scope escape | Denied or tightly scoped, time-bound, and audited |
| P02-TST-048–054 | Cross-tenant cache key; invalidation; missed invalidation; outage; stale sensitive write; version change; concurrent fill | No cross-tenant or stale-sensitive grant |

### 3.4 SaaS billing tests

| IDs | Scenarios | Expected result |
|---|---|---|
| P02-TST-055–058 | SaaS vs ERP invoice creation/read/mutation/numbering | Domains cannot modify or number each other's records |
| P02-TST-059–066 | Monthly/annual; effective price; currency mismatch; rounding edge; discount; proration disabled/enabled; repeated calculation | Reproducible amount from approved snapshot; unsupported rules reject |
| P02-TST-067–073 | Draft edit; issue; issued edit; credit; cancellation/replacement; duplicate issuance; authorization | Issued record immutable; corrections linked and balanced |
| P02-TST-074–081 | Valid event; bad authenticity; duplicate; reordered; unknown; failed; uncertain/timeout; later reconciliation | No false success or duplicate monetary/access effect |

### 3.5 Reliability, isolation, audit, and operations

| IDs | Scenarios | Expected result |
|---|---|---|
| P02-TST-082–089 | Rollback; crash before/after publish; duplicate consumer; stale lease; poison item; replay; provider uncertainty; reconciliation mismatch | Durable, observable, idempotent recovery |
| P02-TST-090–101 | Cross-tenant list/detail/change/charge/document/export/task/cache/admin; UUID guessing; forged tenant ID; same-tenant FK | Every cross-tenant attempt denied or indistinguishable; no side effect |
| P02-TST-102–106 | Material transition audit; privileged read; secret/payload redaction; audit immutability; correlation | Durable sufficient evidence without prohibited data |
| P02-TST-107–112 | Clean install; upgrade; rollback boundary; old/new code overlap; queued schema versions; restricted runtime role | Supported deployment path succeeds or fails safely |
| P02-TST-113–118 | Stuck transition; invalid graph; stale cache; outbox age; payment uncertainty; reconciliation failure | Actionable signal and runbook without sensitive leakage |
| P02-TST-119–121 | Full CI; security review; finance/commercial and operations review | Required gates pass and findings are dispositioned |
| P02-TST-122 | Evidence index/reproduction review | Independent reviewer can reproduce and verify P02 evidence |

## 4. Minimum Test Levels

- Unit: graph evaluation, state transitions, money/currency/rounding, structured entitlement reasons.
- Model/database: constraints, effective-date overlap, same-tenant references, immutable state, RLS/restricted role.
- Service: authorization, entitlement, idempotency, concurrency, rollback, audit.
- View/API: normal, direct URL, HTMX, malformed input, permission and tenant denial.
- Task/integration: outbox/inbox, duplicate/reordered events, retry, timeout, replay, reconciliation.
- Migration: clean install, supported upgrade, data backfill, deployment overlap.
- Security: cross-tenant matrix, IDOR, cache isolation, secret/redaction, webhook authenticity.
- Performance: entitlement decision budget, large plan/dependency graph, billing batch, reconciliation bounds.

## 5. Evidence Index

| Evidence | Required contents | Status |
|---|---|---|
| P02-EV-001 | Entry gate and approved/disabled commercial policies | PLANNED |
| P02-EV-002 | Domain/schema/migration review | PLANNED |
| P02-EV-003 | Catalogue/dependency tests | PLANNED |
| P02-EV-004 | Subscription lifecycle/concurrency tests | PLANNED |
| P02-EV-005 | Entitlement/enforcement tests | PLANNED |
| P02-EV-006 | Cache/override/reconciliation tests | PLANNED |
| P02-EV-007 | Billing calculation/document tests | PLANNED |
| P02-EV-008 | Provider-contract/inbound-event simulation | PLANNED |
| P02-EV-009 | Outbox/task resilience tests | PLANNED |
| P02-EV-010 | Tenant-isolation/authorization review | PLANNED |
| P02-EV-011 | Migration/deployment evidence | PLANNED |
| P02-EV-012 | Security/audit/sensitive-data review | PLANNED |
| P02-EV-013 | Operations/recovery review | PLANNED |
| P02-EV-014 | Independent completion and Product Owner decision | PLANNED |

## 6. Exception Rules

No exception may waive tenant isolation, least privilege, entitlement enforcement, financial integrity, issued-record immutability, secret protection, audit integrity, or required migration safety. Any other exception must identify owner, scope, rationale, compensating control, expiry, linked risk, and approval. A disabled undecided feature is not an exception; it is the required safe state.
