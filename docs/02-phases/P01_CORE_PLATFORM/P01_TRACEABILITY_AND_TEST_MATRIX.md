# P01 Requirements, Controls, Tests and Evidence Matrix

| Property | Value |
|---|---|
| Document ID | P01-TRACE-001 |
| Status | APPROVED-SPECIFICATION COMPANION — ALL APPLICATION TESTS NOT RUN |
| Governing phase | [P01-SPEC-001](P01_PHASE_SPECIFICATION.md) |
| Detailed isolation scenarios | [P01-TEN-TEST-001](P01_TENANT_ISOLATION_TEST_MATRIX.md) |

## 1. Traceability

| Acceptance criteria | Source requirements / ADRs | Task/control | Planned verification | Evidence |
|---|---|---|---|---|
| P01-AC-001–005 | DEP-001/002; NFR-001/002/008; ADR-015–017 | P01-T01/T02/T10/T11 | Bootstrap, lock, production fail-closed, secret scan, safe health tests | P01-EV-002/009–011 |
| P01-AC-006–007 | IAM-001; ADR-005/017/018 | P01-T04 | Custom-user migration, session, CSRF, recovery, abuse/enumeration tests | P01-EV-004/005/008/009 |
| P01-AC-008–010 | TEN-001/005; IAM-002; ADR-004/005/014 | P01-T05 | Membership/lifecycle/provisioning transaction, concurrency, idempotency and audit tests | P01-EV-003–006/008 |
| P01-AC-011–016 | TEN-002/003/004; IAM-003–005; ADR-004/005 | P01-T06/T07 | Trusted-context, RBAC/object/org/platform separation and every-boundary negative tests | P01-EV-005/006/013 |
| P01-AC-017–023 | TEN-002; ADR-002/004/014 | P01-T03/T08 | PostgreSQL same-tenant constraints, RLS USING/WITH CHECK, runtime role, pooling/context cleanup | P01-EV-003/004/006/007 |
| P01-AC-024–027 | AUD-001; OPS-001; ADR-018 | P01-T09 | Audit durability/access/immutability, structured logging, redaction/correlation tests | P01-EV-008/009/013 |
| P01-AC-028 | DEP-001/002; OPS-003/004 | P01-T03/T10/T11 | Clean/upgrade migration, health, container and bounded recovery checks | P01-EV-002/004/010/011 |
| P01-AC-029–031 | NFR-008/009; ADR-015 | P01-T12/T13 | Complete CI, documentation/evidence validation, independent QA/Security/DB/DevOps review | P01-EV-010–014 |

## 2. Test Suites

| Suite ID | Scope | Mandatory evidence state |
|---|---|---|
| P01-SUITE-BOOT | Dependency lock, settings, startup, health, containers | NOT_RUN |
| P01-SUITE-IAM | User/authentication/session/CSRF/abuse/RBAC/object scope | NOT_RUN |
| P01-SUITE-TEN | All 53 scenarios in P01-TEN-TEST-001 | NOT_RUN |
| P01-SUITE-DB | PostgreSQL migrations, roles, constraints, RLS and pooled connections | NOT_RUN |
| P01-SUITE-AUDIT | Audit durability/permissions/redaction/correlation | NOT_RUN |
| P01-SUITE-SEC | Secret/dependency/static/configuration and manual threat review | NOT_RUN |
| P01-SUITE-OPS | Diagnostics, backup/recovery assumptions and runbooks | NOT_RUN |
| P01-SUITE-CI | Reproducible complete gate and artifact integrity | NOT_RUN |

The detailed tenant matrix owns its scenario IDs. Concrete non-tenant executable test IDs must be allocated in the authorized P01 task manifest before implementation; suite labels do not pretend that unimplemented tests exist.

## 3. Evidence Status

| Evidence | Purpose | State |
|---|---|---|
| P01-EV-001 | Phase/task authorizations | PLANNED |
| P01-EV-002 | Locks/configuration/build metadata | PLANNED |
| P01-EV-003 | Architecture/model/ownership/threat reviews | PLANNED |
| P01-EV-004 | Migration plans and PostgreSQL results | NOT_RUN |
| P01-EV-005 | Authentication/permission test reports | NOT_RUN |
| P01-EV-006 | Executed tenant-isolation matrix | NOT_RUN |
| P01-EV-007 | Restricted-role/RLS/pooling evidence | NOT_RUN |
| P01-EV-008 | Audit/logging/redaction evidence | NOT_RUN |
| P01-EV-009 | Secret/dependency/container/static scans | NOT_RUN |
| P01-EV-010 | CI run and exception report | NOT_RUN |
| P01-EV-011 | Setup/migration/security documentation | PLANNED |
| P01-EV-012 | Open defect/risk/decision review | PLANNED |
| P01-EV-013 | Independent QA/Security review | PLANNED |
| P01-EV-014 | Completion report and Product Owner exit | PLANNED |

## 4. Exit Rule

P01 cannot exit until all 31 acceptance criteria and mandatory detailed isolation scenarios have evidence, required independent reviewers have dispositioned findings, no prohibited blocker remains, and the Product Owner records P01 exit. Specification approval and P00 evidence do not satisfy this gate.
