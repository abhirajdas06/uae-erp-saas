# P05 — Bounded Task Prompt Pack

| Property | Value |
|---|---|
| Document ID | P05-PROMPTS-001 |
| Status | READY FOR REVIEW |

Each prompt requires an authorized manifest with exact policy versions, commit/file scope, migrations, tests, reviewers and evidence paths.

## P05-T01 — Policy and Contract Baseline

Resolve or disable legal entity, chart/dimensions, base/multi-currency, precision/rounding, posting/reversal, periods/opening balances and supported VAT rules/workpapers. Define versioned source/VAT/accounting contracts. Evidence P05-EV-001–002/014; tests 001–010. No dependent schema until approval.

## P05-T02 — Chart, Fiscal Period and Journal Foundation

Implement tenant/entity-scoped accounts, fiscal years/periods, journals/drafts/lines, validation, permissions/audit, constraints, migrations and tests. Evidence P05-EV-003; tests 011–035, applicable isolation/migration cases. No direct posting bypass.

## P05-T03 — Transactional Posting and Immutable Ledger

Implement approval/post service, balance/currency/source/idempotency/locking, posted snapshots, outbox, protected mutation, failure rollback and tests. Evidence P05-EV-004; tests 036–048, 127–162 as applicable.

## P05-T04 — Reversal, Period Close and Ledger Reports

Implement linked reversal/adjustment, close/reopen/backdate policy, ledger, trial balance, statement mappings and reconciliation. Evidence P05-EV-005; tests 021–028, 049–078.

## P05-T05 — Source Posting and AR/AP Controls

Implement versioned P03 posting requests/results, source uniqueness, control-account balances and reconciliation; preserve source-domain ownership and P06 future seam. Evidence P05-EV-006; tests 060–086.

## P05-T06 — VAT Configuration and Calculation

After APPR-P05-003, implement effective-dated registration/rules/codes/treatments and deterministic Decimal calculation/snapshots for enabled scenarios only. Evidence P05-EV-007–008; tests 087–118. Missing/ambiguous rules fail closed.

## P05-T07 — VAT Register, Adjustments and Workpapers

Implement immutable VAT transactions, corrections/adjustments, versioned workpaper mappings, source-to-tax-to-ledger reconciliation and explicit limitations. Evidence P05-EV-009; tests 111–126. No filing/payment API.

## P05-T08 — Surfaces, Security, Migration and Operations

Deliver accessible UI/API/reports/exports/import-draft boundary, permissions/segregation/entitlements/RLS, audit/redaction, migrations, backup/restore, monitoring/runbooks and performance evidence. Evidence P05-EV-010–013; tests 127–176.

## P05-T09 — Specialist/Independent Review and Exit

Reproduce all evidence; obtain Finance and qualified UAE tax review; disposition security/database/operations findings, exceptions and disabled limitations; prepare separate phase-exit and production-scope decisions. Evidence P05-EV-014–015; tests 177–180. Reviewer cannot approve own work.
