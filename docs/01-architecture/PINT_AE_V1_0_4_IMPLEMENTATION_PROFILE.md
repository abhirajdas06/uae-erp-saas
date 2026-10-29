# PINT AE 1.0.4 Current Implementation Candidate

| Property | Value |
|---|---|
| Document ID | ARCH-PINT-AE-002 |
| Status | CURRENT TECHNICAL CANDIDATE — PRODUCTION APPROVAL REQUIRED |
| Evidence cut-off | 29 October 2026 |
| Billing / Self-Billing / TDD | `1.0.4` / `1.0.4` / `1.0.4` |
| PINT General / PDK | `1.1.3` / `1.4.4` |

## 1. Decision Boundary

P04 must target the exact UAE PINT AE release contracted with a current UAE Accredited Service Provider. OpenPeppol currently publishes final PINT AE Billing `1.0.4`, Self-Billing `1.0.4`, and UAE TDD `1.0.4`; this set supersedes `2025-Q2`/`1.0.0` as the implementation candidate. The historical profile remains preserved for change analysis.

This is a technical baseline, not a claim of legal compliance, ASP accreditation or production authorization.

## 2. Supported Initial Profiles

| Profile | Default state | Activation gate |
|---|---|---|
| Billing Invoice | Candidate enabled scope | Mapping coverage, ruleset, provider sandbox/conformance, UAE reviewer and Product Owner approval |
| Billing Credit Note | Candidate enabled scope | Original/correction relationship, financial/VAT review, provider conformance and approval |
| Self-Billing Invoice/Credit Note | Disabled | Separate contractual, actor-authority, tax, provider and Product Owner approval |
| Tax Data Document | Provider-bound reporting profile | Exact ASP/FTA responsibility, status and evidence contract approval |

## 3. UAE Exchange and Reporting Boundary

The current MoF model is a five-corner DCTCE flow: supplier, supplier ASP, buyer ASP, buyer and FTA. Supplier data is sent as PINT AE or an ASP-agreed input; ASPs validate/convert to UAE XML, exchange the invoice, report TDD, and return Message Level Status evidence. Transport acceptance, recipient delivery, provider validation and FTA reporting are distinct states. No timeout, HTTP success or locally valid XML is regulatory acceptance.

## 4. Release-Set Contract

An approved ruleset pins semantic model and UBL binding; code lists; shared and AE-aligned Schematron/XSLT; profile versions; ERP mapping version; provider API/status contract; MoF mandatory-field/guidance versions; and positive/negative fixtures. Resource digests are in [REG-EV-EINV-20261029-001](../00-product/regulatory-evidence/PINT_AE_RESOURCE_ARCHIVE_MANIFEST_2026-10-29.md). Any component change invalidates compatibility evidence until the full set is rerun.

## 5. Validation Pipeline

Validation order is: internal invoice/VAT invariants; semantic cardinality/conditions; exact UBL serialization; XML/schema safety; code lists; shared PINT Schematron; AE-specific Schematron; provider preflight; financial reconciliation; provider sandbox/conformance. Findings retain profile, release, layer, rule ID, severity and safe message.

The `1.0.4` regression suite must cover its published corrections: reverse-charge allowance VAT rate, standard-rated 5% consistency, multiple VAT-category subtotals, permitted categories for out-of-scope document types, ProfileID pattern and malformed numeric safeguards. These validator rules do not become universal accounting policy without applicability review.

## 6. Data and Evidence

- Preserve immutable internal invoice/credit snapshots and exact mapping/ruleset/provider versions.
- Store operation, idempotency key, payload hash, safe request/response evidence, native and normalized statuses, MLS/TDD references and reconciliation state.
- Never log full payloads, secrets or unnecessary personal/tax data.
- Reprocessing historical documents uses their historical release unless a reviewed resubmission rule says otherwise.
- Generated XML is private evidence under ADR-019, not a public attachment.

## 7. Current UAE Guidance Controls

MoF V2.0 guidance identifies structured XML exchange, PINT AE, participant/TIN rules, accredited ASP responsibilities, phased dates, retention expectations and no QR code/barcode in the electronic invoice. These are effective-dated policy inputs, not hardcoded universal assumptions. The mandatory-field publication and legislation/amendments require qualified review before activation.

No authoritative general UAE e-way-bill regime was identified. P04 must not add one. Transport, customs, delivery and airway-bill data remain separate bounded integrations or optional PINT fields where verified.

## 8. Exit Evidence

P04 release evidence requires 100% supported mandatory/conditional mapping coverage; current resource digests; validator execution; golden/negative fixtures; provider sandbox/conformance; MLS/TDD reconciliation; retry/duplicate/uncertain-outcome tests; security/tenant/file tests; current ASP accreditation evidence; qualified UAE review; and Product Owner activation approval.
