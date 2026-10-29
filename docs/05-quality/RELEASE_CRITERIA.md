# Release Criteria

| Property | Value |
|---|---|
| Document ID | QUAL-REL-001 |
| Status | READY FOR REVIEW |
| Owner | Product / Release / QA / Security / Operations |

## 1. Release Levels

| Level | Meaning | Authority |
|---|---|---|
| Development baseline | Reproducible local/CI build for authorized task | Engineering + QA |
| Phase candidate | All phase AC/evidence assembled for independent review | Phase reviewers |
| Deployment candidate | Immutable release passed staging/rehearsal and operational gates | Release Owner |
| Production deployed | Technical deployment completed and verified | Authorized change/deployment approver |
| Business launched | Approved users/tenants may use named capabilities | Product Owner |

These states are distinct. Deployment is not business launch or regulatory compliance.

## 2. Mandatory Candidate Gates

- Exact source commit, dependency locks, image/artifact digests, SBOM/provenance and configuration schema.
- Required CI/tests, migration rehearsal, tenant/security/financial reconciliation and no hidden skips.
- Threat, privacy, dependency/secret, file, provider and domain reviews applicable to scope.
- Backup/restore, monitoring/alerts, capacity, incident, support and rollback/containment evidence.
- Regulated/provider capabilities use current sources, accredited/authorized provider evidence, conformance tests and qualified approval.
- Open findings/exceptions/risks have permitted severity, owner, compensating control and expiry.
- Release notes name enabled/disabled capabilities, migrations, compatibility, known limitations and rollback/forward-recovery plan.

## 3. Blocking Findings

Unresolved critical or unapproved high findings affecting tenant isolation, authorization, secrets, sensitive data, financial integrity, duplicate external effects, destructive migration/recovery, audit evidence or regulatory misrepresentation block release. A deadline is not an exception.

## 4. Approval Record

Record release ID/version, scope, environments/tenants, evidence index/digests, reviewers, findings/exceptions, deployment window, rollback/containment authority and separate Product Owner launch decision. P12 owns the final operational evidence and approval gates.
