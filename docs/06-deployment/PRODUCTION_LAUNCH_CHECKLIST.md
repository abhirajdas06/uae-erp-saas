# Production Launch Checklist

| Property | Value |
|---|---|
| Document ID | DEP-LAUNCH-001 |
| Status | TEMPLATE — NOT APPROVED FOR ANY RELEASE |

Use this checklist with P12-TRACE-001 and DEP-EVID-001. Every checked item links to a verified evidence ID/artifact/digest; narrative assertion is insufficient.

## Scope and Authority
- [ ] Exact release, tenants, modules, providers, region, window and exclusions recorded.
- [ ] P00–P11 applicable exits/evidence verified.
- [ ] APPR-P12-002 provisioning/spend and APPR-P12-003 deployment authority recorded.
- [ ] Product Owner launch approver and rollback/incident authority available.

## Artifact, Configuration and Infrastructure
- [ ] Commit/image digest/provenance/SBOM/scans verified.
- [ ] Production configuration/secrets/roles/network/DNS/TLS/database/Redis/object storage validated.
- [ ] Capacity/headroom, quotas, costs and provider limits reviewed.
- [ ] Clean deployment/migration/rollback-forward recovery rehearsed.

## Safety and Recovery
- [ ] Release-candidate isolation, permission, entitlement, file/audit and domain-integrity tests pass.
- [ ] Backups are current/protected/alerted and independent restore/PITR/object recovery meets approved target.
- [ ] Monitoring, alerts, on-call, incident/escalation and runbooks are exercised.
- [ ] Enabled integrations have exact conformance, credentials, uncertainty/reconciliation and disable evidence.

## Users and Operations
- [ ] UAT/onboarding/support/training/locale/accessibility scope approved.
- [ ] Status/customer/provider communications and escalation are ready.
- [ ] Critical findings resolved and permitted residual risks approved with expiry.
- [ ] Stabilization duration, abort thresholds and reconciliation owners are named.

## Final Decisions
- [ ] Independent release review signs the evidence manifest.
- [ ] APPR-P12-004 exact Product Owner launch statement recorded.
- [ ] Deployment/smoke/reconciliation passes for the exact production release.
- [ ] Stabilization and post-launch review record incidents, capacity, reconciliations and follow-up.
