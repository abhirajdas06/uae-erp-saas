# P05 — Requirements, Controls, Tests and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P05-TRACE-001 |
| Status | READY FOR REVIEW |
| Test status | All tests `NOT_RUN` until implementation evidence exists |

## 1. Traceability

| Criteria | Sources | Controls | Tests | Evidence |
|---|---|---|---|---|
| P05-AC-001 | PRD-DEC-005/008/010; REG-SRC-001 | Versioned finance/VAT policy; unsupported behavior disabled | P05-TST-001–010 | P05-EV-001–002, 014 |
| P05-AC-002–004 | ACC-001/002/004 | Tenant/entity keys; chart/period/journal state; approvals | P05-TST-011–035 | P05-EV-003 |
| P05-AC-005–007 | ACC-002; ADR-010/011/013 | Transactional balanced posting; immutability; reversal; idempotent source contract | P05-TST-036–068 | P05-EV-004–006 |
| P05-AC-008–009 | ACC-003/005; REP-002 | Posted-line truth; trial balance; control-account/source reconciliation | P05-TST-069–086 | P05-EV-005–006 |
| P05-AC-010–014 | VAT-001–003; REG-SRC-001 | Effective rules; Decimal calculation; snapshots; corrections; workpapers/reconciliation | P05-TST-087–126 | P05-EV-007–009, 014 |
| P05-AC-015–016 | ADR-004–006/018 | Permission/segregation/entitlement; RLS; audit/redaction/immutability | P05-TST-127–151 | P05-EV-010–011 |
| P05-AC-017–018 | NFR-009; ADR-016/019/020 | Migration/recovery reconciliations; bounded safe reports/exports | P05-TST-152–169 | P05-EV-010, 012 |
| P05-AC-019–021 | ADR-015; Roadmap 10 | Full gates; finance/tax/independent review; human exit | P05-TST-170–180 | P05-EV-013–015 |

## 2. Test Catalogue

| IDs | Scenarios | Expected result |
|---|---|---|
| P05-TST-001–010 | Missing/approved/stale policy; entity/base currency; precision/scale; rounding stage; FX disabled/enabled; chart policy; period policy; VAT source version; unsupported treatment | Only exact approved policy is active; otherwise fail closed |
| P05-TST-011–020 | Account create/type/code/hierarchy; duplicate; wrong tenant/entity; protected account change; retire unused/used; permission; audit | Valid scoped chart without historical reinterpretation |
| P05-TST-021–028 | Fiscal year/period boundaries; overlap; open/soft-close/close; closed posting; reopen; backdate; concurrent close | Controlled auditable period lifecycle |
| P05-TST-029–035 | Journal draft/lines; account/dimension/date/currency; zero/negative/overflow; stale approval; segregation | Valid approved draft only |
| P05-TST-036–048 | Balanced/unbalanced; atomic failure; exact decimals; base/transaction currency; source snapshot; policy snapshot; concurrent/repeated posting; changed key payload; DB constraint; outbox; crash; restricted runtime | One complete balanced immutable entry or none |
| P05-TST-049–059 | Posted update/delete through service/UI/API/admin/import/task/DB role; reversal amounts/date/period; duplicate/concurrent reversal; adjustment; original preservation | No silent mutation; linked controlled correction |
| P05-TST-060–068 | Invoice posting request; wrong tenant/entity; duplicate source/purpose; version/hash conflict; disabled module; contract schema; consumer retry/reorder; source cancellation/correction; reconciliation | Explicit versioned idempotent source-ledger boundary |
| P05-TST-069–078 | Ledger filters; opening/period activity/closing; trial balance; debit-credit; multi-currency display; statement mapping; drill-down; unposted exclusion; projection rebuild | Reproducible posted-line reports |
| P05-TST-079–086 | AR source/control total; payment/credit effect; AP future seam; missing/duplicate posting; currency difference; cutoff; explained exception; repair/replay | Source/control reconciliation detects every difference |
| P05-TST-087–096 | Tax registration/entity/effective rules; overlap; activation approval; code/treatment/evidence; unauthorized change; future/past rule; source age; cache version; audit | One approved applicable VAT policy |
| P05-TST-097–110 | Taxable base; exclusive/inclusive; line/category/document rounding; negative/correction; discount/charge; residual; precision boundary; client tamper; missing fact; unsupported treatment; golden examples; property invariants; reproducibility | Exact approved Decimal result or safe rejection |
| P05-TST-111–118 | Snapshot/hash; current-rule/master change; issued invoice; credit/adjustment; period allocation; duplicate event; source/ledger link; historical read | Immutable historically reproducible tax result |
| P05-TST-119–126 | VAT register; date/treatment/currency grouping; return mapping version; source-to-register; register-to-ledger; adjustment; late item; workpaper/drill-down | Reconciled workpaper with explicit limitations, not filing claim |
| P05-TST-127–138 | Missing permission/entitlement; prepare/approve/post; configure/activate; close/reopen; report/export; support; direct URL/API/HTMX/task/admin; segregation | Least privilege on every boundary |
| P05-TST-139–147 | Cross-tenant/entity account/period/journal/source/tax rule/snapshot/report/export/cache/task and guessed UUID/RLS | No cross-scope inference or effect |
| P05-TST-148–151 | Audit completeness/immutability/redaction; sensitive dimension/tax ID; privileged read/export | Durable sufficient evidence without excess data |
| P05-TST-152–162 | Clean install/upgrade/backfill; precision/ruleset change; restricted role/RLS; old/new overlap; rollback boundary; backup/restore; per-account/currency/tax totals; source/reversal links; projection rebuild; audit/outbox | Migration/recovery preserves financial truth |
| P05-TST-163–169 | Report authorization/bounds/pagination; decimal/API; CSV injection; private files; accessibility; currency/treatment labels; import drafts only | Safe, accurate, bounded surfaces |
| P05-TST-170–176 | Posting/report load; lock contention; monitoring/alerts; reconciliation runbook; restore drill; full CI; exception scan | Operable within approved targets |
| P05-TST-177–180 | Finance review; qualified UAE tax review; independent reproduction/security review; Product Owner exit/production separation | Exact scope approved; no inferred accounting/tax compliance |

## 3. Evidence Index

| Evidence | Scope | Status |
|---|---|---|
| P05-EV-001 | Approved accounting/currency/period policy | PLANNED |
| P05-EV-002 | Approved UAE VAT policy/source/version baseline | PLANNED |
| P05-EV-003 | Chart/period/journal schema and tests | PLANNED |
| P05-EV-004 | Posting/immutability/concurrency tests | PLANNED |
| P05-EV-005 | Reversal/ledger/trial-balance tests | PLANNED |
| P05-EV-006 | Source/AR/AP contract and reconciliation | PLANNED |
| P05-EV-007 | VAT configuration/ruleset tests | PLANNED |
| P05-EV-008 | VAT calculation/golden/property tests | PLANNED |
| P05-EV-009 | VAT register/workpaper/reconciliation tests | PLANNED |
| P05-EV-010 | UI/API/report/export/accessibility tests | PLANNED |
| P05-EV-011 | Authorization/isolation/RLS/security/audit review | PLANNED |
| P05-EV-012 | Migration/backup/restore evidence | PLANNED |
| P05-EV-013 | Performance/operations/full quality gates | PLANNED |
| P05-EV-014 | Finance and qualified UAE tax review | PLANNED |
| P05-EV-015 | Independent completion and Product Owner decisions | PLANNED |

## 4. Exception Rules

No exception may waive balanced atomic posting, immutable posted/tax history, tenant/legal-entity isolation, permission/entitlement, exact Decimal/currency rules, duplicate-posting protection, audit, regulatory-source validation or migration reconciliation. Unsupported tax/FX/period/filing behavior stays disabled. Other exceptions require named owner, risk, control, expiry and human approval.
