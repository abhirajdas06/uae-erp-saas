# Backup and Recovery Specification

| Property | Value |
|---|---|
| Document ID | DEP-BCR-001 |
| Status | READY FOR REVIEW — RPO/RTO AND TOPOLOGY OPEN |
| Related decision | DEC-OPS-002 |

## 1. Objectives and Scope

Protect and recover PostgreSQL, object/file storage, required configuration metadata, secrets-system recovery material, integration/event evidence and deployment identity. Redis is recovered according to its approved non-authoritative/durable-task semantics; it is never assumed to be the sole business record.

RPO and RTO are explicit per service/data class and scenario. No target is promised until measured restore evidence demonstrates it or an authorized gap is recorded.

## 2. Backup Contract

| Asset | Required controls |
|---|---|
| PostgreSQL | Scheduled full/base plus WAL/PITR where target requires; consistent encryption; version/extension/config inventory; integrity and restore tests |
| Object storage | Version/inventory and backup/replication appropriate to threat; metadata/content/checksum linkage; deletion/retention protection |
| Configuration | Non-secret schema/version and infrastructure/release definitions; secret references only |
| Secret recovery | Provider-approved protected recovery/escrow process; no plaintext secret in ordinary backup evidence |
| Audit/integration evidence | Retention-consistent protection and reconciliation with database/files |

Backups use least-privilege identities separate from runtime where practical, encrypted transport/storage, isolated account/credentials, immutability/deletion protection, monitored schedules and tested retention/expiry. A backup job’s success is not proof of recoverability.

## 3. Recovery Scenarios

- Accidental row/data corruption with known point.
- Failed migration or release corruption.
- Database/service/host/zone loss.
- Object deletion or metadata/content divergence.
- Credential compromise or ransomware/destructive administrator.
- Full environment loss and region/provider contingency if required.
- Tenant-specific logical recovery request within shared-schema constraints.

Tenant-level recovery must not overwrite other tenants. Preferred methods restore to an isolated environment, identify authoritative tenant-scoped records/files/events, validate dependencies, then execute a reviewed logical repair/import. Limitations are explicit.

## 4. Restore Procedure and Evidence

Authorize incident/recovery owner; select verified recovery point; create isolated target; validate versions/keys/config; restore database and files; apply WAL/version recovery; reconcile counts/totals/hashes/tenant ownership/outbox/audit; run application/security/business smoke tests; decide cutover or abandon; protect failed/original evidence; document actual RPO/RTO.

Evidence includes backup IDs/times/ranges/checksums, encryption/key access result, restored versions, commands/exit codes, start/end duration, point/data loss, database/file reconciliation, critical domain totals, tenant isolation, application tests, defects, approver and secure destruction of test copies.

## 5. Required Drills

At approved frequency: representative PostgreSQL restore, object/file recovery, point-in-time recovery, credential/key recovery, release-corruption recovery and tenant logical-recovery exercise. Failures create tracked findings; critical recovery gaps block launch or require explicit authorized scope reduction.
