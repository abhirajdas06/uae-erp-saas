# P06 — Requirements, Controls, Tests and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P06-TRACE-001 |
| Status | READY FOR REVIEW |
| Test status | All tests `NOT_RUN` until implementation evidence exists |

## 1. Traceability

| Criteria | Sources | Controls | Tests | Evidence |
|---|---|---|---|---|
| P06-AC-001–004 | INVN-001/002; ADR-003/011/013 | Approved ownership/policies; supplier/PO revisions; concept separation | P06-TST-001–035 | P06-EV-001–004 |
| P06-AC-005–011 | INVN-002–004 | Idempotent receipt; movement-only stock; UOM/transfer/concurrency/policy; reconciliation | P06-TST-036–088 | P06-EV-005–007 |
| P06-AC-012–013 | INVN-005; ACC/VAT contracts | Versioned valuation; immutable layers; accounting/VAT requests/reconciliation | P06-TST-089–112 | P06-EV-008–009 |
| P06-AC-014–016 | ADR-004–008/018–020 | Permission AND entitlement; RLS; sensitive data; bounded surfaces | P06-TST-113–143 | P06-EV-010–011 |
| P06-AC-017–020 | NFR-006/007/009; ADR-015/016 | Migration/recovery totals; performance/operations; independent/human gates | P06-TST-144–170 | P06-EV-012–014 |

## 2. Test Catalogue

| IDs | Scenarios | Expected result |
|---|---|---|
| P06-TST-001–010 | Approved/missing item owner; sales mapping; supplier owner; requisition/service/stock scope; UOM policy; negative stock; reservation; valuation; accounting/VAT policy | Exact enabled scope or fail closed |
| P06-TST-011–020 | Supplier create/update/deactivate; required/normalized fields; duplicate candidate/override/merge; contact; sensitive bank/tax; search; wrong tenant; audit | Controlled tenant-safe supplier history |
| P06-TST-021–035 | Requisition/PO draft; line/item/service/UOM/currency; server totals; revision; stale approval; thresholds/segregation; issue; cancel/close; unauthorized transition; repeated conversion; supplier change; snapshot; concurrency | Valid immutable approved PO revision and history |
| P06-TST-036–048 | Full/partial/over/under receipt; tolerance; wrong PO/revision/line/item/UOM/location; duplicate/retry/concurrent receipt; service receipt; return; over-return; rejected inventory call | One bounded traceable receipt/return effect |
| P06-TST-049–060 | Bill reference/match; PO-receipt-bill distinction; duplicate bill; quantity/price/tax/currency variance; payment separation; source/accounting seam; reconciliation; reordered event; correction; close with exception; report | Explicit matching/evidence, no invented liability/payment |
| P06-TST-061–070 | Item/mapping/category; UOM/conversion direction/effective date/precision; warehouse/location uniqueness/hierarchy/inactive; cross-tenant/entity; historical master change | Valid scoped historically stable master data |
| P06-TST-071–080 | Receipt/issue/transfer; atomic source/destination; duplicate/concurrent issue; availability; negative policy; backdate; reversal; direct balance edit; failure rollback | One authorized append-oriented movement, consistent balance |
| P06-TST-081–088 | Reservation/create/release/expiry/overcommit; stock count cutoff/freeze; variance approval; adjustment reason; concurrent count/movement; balance rebuild; cutoff report | Approved availability/count adjustment with reconciliation |
| P06-TST-089–100 | Cost source; method golden cases; layer consumption; partial/return/adjustment; precision/rounding; negative-stock valuation; current-cost change; backdate/cutoff; multicurrency disabled/enabled; quantity-value reconciliation; overflow; revaluation disabled | Reproducible approved historical valuation |
| P06-TST-101–112 | Posting request/result; unique source/purpose; duplicate/conflict; tax snapshot; inventory/control account; failed/retry/reordered posting; correction/reversal; period closed; source-ledger reconciliation; unsupported integration; outbox | Versioned idempotent downstream effects or visible exception |
| P06-TST-113–123 | Permission/entitlement combinations; PO approval; receipt; adjustment; count; valuation; warehouse scope; direct URL/API/task/admin; support; export | Least privilege at every boundary |
| P06-TST-124–133 | Cross-tenant/entity supplier/item/PO/location/movement/reservation/count/valuation/file/report/cache/RLS guessed UUID | No inference, reference or effect |
| P06-TST-134–143 | Supplier/cost sensitive field; log/audit redaction; file download; report semantics; API decimals; import preview/draft only; CSV injection; accessibility; pagination/bounds; audit timeline | Safe accurate bounded surfaces |
| P06-TST-144–155 | Clean install/upgrade/backfill; restricted role/RLS; UOM/precision change; old/new schema; rollback boundary; backup/restore; movement/balance rebuild; reservation; valuation; document/source links; outbox/audit replay | Quantity/value/history preserved and reconciled |
| P06-TST-156–166 | Load/locking; concurrent hot item; report bounds; backlog; monitoring/alerts; negative/duplicate/mismatch runbooks; count/restore drill; full CI; secret scan; exception scan | Operable with actionable evidence |
| P06-TST-167–170 | Operations/Finance/Security review; independent reproduction; defect/exception disposition; Product Owner exit/production separation | Exact approved scope and evidence |

## 3. Evidence Index

P06-EV-001 policy/ownership; P06-EV-002 schema/contracts; P06-EV-003 supplier tests; P06-EV-004 purchase tests; P06-EV-005 item/UOM/location; P06-EV-006 movement/receipt/transfer; P06-EV-007 reservation/count/adjustment; P06-EV-008 valuation; P06-EV-009 accounting/VAT reconciliation; P06-EV-010 surfaces/accessibility; P06-EV-011 authorization/isolation/security/audit; P06-EV-012 migration/recovery; P06-EV-013 performance/operations/full gates; P06-EV-014 independent completion/Product Owner decisions. All are `PLANNED`.

## 4. Exception Rules

No exception may waive movement-only stock integrity, tenant/entity/warehouse isolation, authorization/entitlement, exact UOM/Decimal rules, duplicate-effect prevention, immutable movement/valuation history, financial reconciliation or migration/recovery safety. Unapproved negative stock, valuation, advanced tracking and integrations remain disabled.
