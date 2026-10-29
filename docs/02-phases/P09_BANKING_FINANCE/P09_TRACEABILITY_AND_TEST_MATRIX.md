# P09 — Requirements, Controls, Tests and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P09-TRACE-001 |
| Status | APPROVED VERIFICATION BASELINE — APPLICATION TESTS NOT RUN |
| Regulatory evidence cut-off | 29 October 2026 |
| Test status | All tests `NOT_RUN` until implementation evidence exists |

## 1. Traceability

| Criteria | Sources | Controls | Tests | Evidence |
|---|---|---|---|---|
| P09-AC-001 | BANK-001–003; REG-BANK-001 | Explicit modes/role/provider scope; fail-closed capability flags | P09-TST-001–010 | P09-EV-001–002, 015 |
| P09-AC-002–005 | ADR-014/019; ARCH-BANK-CONTRACT-001 | Account scoping/masking; safe versioned imports; native provenance; dedup/overlap | P09-TST-011–055 | P09-EV-003–005 |
| P09-AC-006–009 | BANK-001–003; ADR-010/011/013 | Explainable match; append history; deterministic reconciliation; idempotent reports/posting | P09-TST-056–105 | P09-EV-006–009 |
| P09-AC-010–012 | REG-BANK-001; ADR-009/010/017/020 | Exact provider/consent/security; durable operations; maker-checker; native statuses | P09-TST-106–137 | P09-EV-010–011 |
| P09-AC-013–015 | ADR-004–006/018/019 | Permission/entitlement/RLS; sensitive-data/file/log controls | P09-TST-138–157 | P09-EV-012 |
| P09-AC-016–019 | NFR-006/007/009; ADR-015/016 | Migration/restore; operations; specialist/independent/human gates | P09-TST-158–180 | P09-EV-013–015 |

## 2. Test Catalogue

| IDs | Scenarios | Expected result |
|---|---|---|
| P09-TST-001–010 | Mode A/B/C/D configuration; missing/stale legal/provider approval; unsupported bank/account/customer; provider license snapshot; capability/entitlement disabled; claims wording; emergency disable; audit | Only exact approved capability can operate |
| P09-TST-011–024 | Bank-account create/update/deactivate; entity/currency/ledger mapping; masked display; IBAN format/check digit; ownership not inferred; duplicate account; wrong tenant; role/object access; historical mapping; audit | Tenant-safe minimal account reference |
| P09-TST-025–040 | File extension/MIME/signature/size; malware; encoding/delimiter/date/decimal; parser/schema version; header/account/currency; opening/closing; preview/cancel/commit; malformed/partial; unsafe filename/CSV; private download; checksum | Valid private immutable statement or no commit |
| P09-TST-041–055 | Same file; renamed file; native line ID; content fingerprint; overlapping period; repeated balance line; provider correction; duplicate within file; ambiguous collision; concurrent imports; rollback; normalization provenance; native text/time/amount preservation; parser upgrade | No duplicate effect or lost native evidence; ambiguity reviewed |
| P09-TST-056–072 | Match by reference/amount/date; many-to-one/one-to-many policy; tolerance; currency; split/fee disabled; ordered rules/version; confidence/explanation; candidate only; stale candidate; manual confirm; maker-checker; wrong tenant/source; concurrent confirm; unmatch/reassign; audit | Explainable authorized append-oriented decision |
| P09-TST-073–090 | Opening + movement = closing; debit/credit signs; matched/unmatched/difference; locked period; close/reopen/correct; concurrent close; source missing/changed; ledger missing/duplicate; posting request/idempotency/failure/retry/reversal; multi-currency semantics; rounding; account/period totals | Exact exception-visible reconciliation |
| P09-TST-091–105 | Cash/bank report as-of/source/currency; unmatched/uncertain disclosures; current vs historical mapping; export/API pagination; duplicate report job; task/cache isolation; Accounting/source/provider totals; performance bounds; accessibility | Accurate bounded non-misleading reports |
| P09-TST-106–120 | Provider onboarding/version; consent grant/scope/purpose/account/duration; auth; expired/revoked consent; incremental cursor; pagination; rate limit; timeout/retry; duplicate/reordered data; credential/certificate rotation; authenticated callback; provider drift; emergency disable | Secure authorized data sync with native evidence |
| P09-TST-121–137 | Payment capability disabled; immutable instruction; beneficiary/amount/currency/purpose; maker-checker/limits/signatory; idempotency same/conflict; export vs submit; timeout/unknown; unsafe retry; rejection; callback replay/reorder/signature; provider accepted vs executed vs settled; cancellation; reconciliation; duplicate-payment invariant | At most one intended effect and truthful outcome |
| P09-TST-138–149 | Account/import/match/reconcile/provider/payment role combinations; entitlement; direct URL/API/admin/task; support purpose/expiry; sensitive fields; bulk export; provider operator separation; cross-entity access; RLS restricted/bypass role | Least privilege and no cross-tenant effect |
| P09-TST-150–157 | Cross-tenant file/cache/report/callback; logs/errors/metrics/traces; account/narrative/consent/payload/secret redaction; audit completeness; retention/legal hold/disposal; PDPL request workflow; incident evidence | Minimized protected data and useful audit |
| P09-TST-158–169 | Clean/upgrade/backfill; restricted role; old/new parser/rule/provider overlap; rollback; restore files/hashes/statements/lines; matches/reconciliations; ledger/source/provider; consent/operations; outbox/audit; reconciliation totals | Preserved provenance and exact restore evidence |
| P09-TST-170–175 | Large-file/match/report load; locking; monitoring/alerts; provider outage/credential/consent/uncertain-payment incidents; restore drill; full CI/security/exception scans | Operable within approved targets |
| P09-TST-176–180 | Finance/Accounting review; UAE Legal/Compliance/provider review; Security/Privacy/Database/Operations review; independent reproduction/critical findings; Product Owner exit and per-mode activation | Named reviews and exact bounded decisions |

## 3. Evidence Index

P09-EV-001 dated regulatory/mode baseline; P09-EV-002 approved role/provider/capability record; P09-EV-003 account/security; P09-EV-004 import/parser/file; P09-EV-005 native/dedup/normalization; P09-EV-006 matching; P09-EV-007 reconciliation; P09-EV-008 Accounting/source contract; P09-EV-009 reports; P09-EV-010 provider data/consent; P09-EV-011 payment operation when enabled; P09-EV-012 authorization/isolation/privacy/audit; P09-EV-013 migration/recovery; P09-EV-014 performance/operations/full gates; P09-EV-015 legal/provider/finance/security/independent completion and Product Owner decisions. All are `PLANNED`.

## 4. Exception Rules

No exception may waive licensing/role validation for a regulated mode, consent and credential security, tenant isolation, native evidence/provenance, duplicate-effect prevention, maker-checker for payments, uncertainty reconciliation, truthful provider/settlement state, audit or restore reconciliation. Unapproved Modes B–D remain disabled.
