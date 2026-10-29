# Operational Evidence Specification

| Property | Value |
|---|---|
| Document ID | DEP-EVID-001 |
| Status | READY FOR REVIEW |

## 1. Evidence Principles

Evidence must be reproducible, attributable, immutable or integrity-protected, scoped to the exact release/environment and safe to retain. A document describing a control is not executed evidence. Screenshots alone are insufficient when machine-verifiable output exists.

## 2. Evidence Manifest

Every item records evidence ID, criterion/control/test, status (`PLANNED`, `PARTIAL`, `VERIFIED`, `FAILED`, `WAIVED` where permitted), environment, source commit/image/config/migration versions, command/tool version, start/end/timezone, actor/reviewer, exit/result, artifact URI, SHA-256 or equivalent digest, redaction/classification/retention, dependencies, findings/exceptions and approval.

`VERIFIED` requires successful result, complete identity, accessible artifact, integrity check and authorized independent review where mandated. `PARTIAL` states exactly what is missing. Evidence expiry/revalidation trigger is explicit.

## 3. Required P12 Evidence Classes

- Release manifest, build provenance/SBOM/scans and protected approval.
- Infrastructure/configuration/secret/network/TLS/access validation.
- Clean deployment, migration rehearsal, smoke and rollback/forward-recovery exercise.
- Tenant-isolation, authorization, entitlement and critical financial/domain reconciliation.
- Monitoring signal/alert and operator runbook exercises.
- Backup inventory, restore/PITR/object recovery and measured RPO/RTO.
- Incident tabletop/technical exercises and escalation roster review.
- Representative performance/capacity/soak/failure results.
- UAT, tenant onboarding, support/training and provider conformance for enabled scope.
- Security/privacy/accessibility/readiness findings and residual-risk decisions.
- Launch decision and post-launch review.

## 4. Permissions and Handling

Evidence writers cannot overwrite verified artifacts; corrections create a new version. Reviewers are independent where required. Secrets, production payloads and unnecessary personal/financial data are prohibited; sensitive evidence uses restricted storage, access audit, expiry/retention and secure disposal. Public/customer-facing evidence is separately approved.

## 5. Exceptions

Waivers cannot replace production-launch authorization or waive tenant isolation, financial integrity, usable backup/restore, critical secret/security remediation, release identity, audit or incident ownership. A permitted waiver has owner, rationale, compensating control, affected scope, approver, expiry and re-test date.
