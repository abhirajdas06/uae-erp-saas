# Environment and Secret Configuration Specification

| Property | Value |
|---|---|
| Document ID | DEP-CONFIG-001 |
| Status | READY FOR REVIEW — IMPLEMENTATION INVENTORY TO BE GENERATED |
| Authority | ADR-017 |

## 1. Configuration Contract

Every setting has a stable name, owner, type, required environments, safe default or no default, sensitivity class, validation rule, reload/restart behavior and documentation. Startup validates the complete typed configuration and fails closed on missing, malformed, placeholder or incompatible production values.

## 2. Configuration Groups

| Group | Examples of required contract, not literal values |
|---|---|
| Django runtime | environment, debug=false, secret-key reference, allowed hosts, CSRF origins, timezone/locale, secure cookies/proxy settings |
| Database | DSN/host/name, role identity/credential reference, TLS mode/CA, pool/timeout/connection limits, tenant context requirements |
| Redis/Celery | broker/backend endpoints, TLS/auth reference, queues, concurrency, visibility/time limits, scheduler identity |
| Files | private storage endpoint/region/container, credential reference, encryption, signed URL expiry, upload limits/scanner/quarantine |
| Email/provider APIs | endpoint/environment, credential reference, timeout, rate/retry, sender/callback identifiers; disabled unless approved |
| Observability | log level/format, service/release/environment, metric/trace endpoints and credential references, sampling/redaction |
| Security | HTTPS/header settings, key/certificate references, rate/request limits, support/break-glass switches |
| Release | source revision, image digest, configuration version, migration/release identity, enabled modules/contracts |

## 3. Secret Rules

Secrets are never committed, printed, placed in images, ordinary database tables, client code, crash reports or evidence artifacts. Production uses an approved secrets backend or protected runtime injection; environment variables may carry injected values only where the threat model approves it. Prefer short-lived workload identity and separate credentials per role/environment.

Rotation supports overlap where required, verification and revocation. Compromise handling identifies affected versions/workloads/data, rotates, revokes, audits access and validates recovery. Example configuration uses unmistakable non-secret placeholders.

## 4. Change and Evidence

Configuration changes are reviewed, versioned, diffable without secret values, validated in staging and linked to a release or emergency change. Evidence records schema/version, validation result, secret references/versions—not values—approver, rollout and rollback/forward-fix.

## 5. Acceptance Tests

Missing/placeholder/malformed values; debug/test defaults in production; unsafe host/origin/proxy/TLS; database/Redis/storage TLS and least privilege; role credential separation; secret log/error/task/artifact scan; rotation/revoke; environment cross-use; configuration compatibility; startup/health behavior and recovery after secret-backend degradation.
