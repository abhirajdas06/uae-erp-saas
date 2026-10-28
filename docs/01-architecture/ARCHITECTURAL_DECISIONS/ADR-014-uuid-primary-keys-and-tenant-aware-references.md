# ADR-014: UUID Primary Keys and Tenant-Aware References

| Field | Details |
|---|---|
| ADR ID | ADR-014 |
| Title | UUID Primary Keys and Tenant-Aware References |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / Database Lead |
| Reviewers | Architecture, Database, Security, Development, DevOps |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-002, ADR-003, ADR-004, ADR-011, ADR-013, ADR-018, ADR-020 |
| Related Requirements | TEN-001–TEN-003, IAM-004, NFR-001, NFR-005, NFR-009, API-006 |
| Related Documents | `DATABASE_DESIGN.md`, `MULTI_TENANCY.md`, `DJANGO_APP_STRUCTURE.md`, `API_STANDARDS.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The shared-schema platform needs stable identifiers for tenants, users, subscriptions, invoices, journal entries, employees, operations, and other business records. Identifiers appear in URLs, APIs, task messages, audit events, integration records, imports, and cross-domain references.

Sequential identifiers are simple and compact but can expose volume and are awkward to generate independently. UUIDs provide globally unique, application-generated identifiers, but random UUID indexing, careless public exposure, or reliance on obscurity can create performance and security problems.

Tenant isolation also requires more than globally unique IDs. A Tenant A invoice must not reference a Tenant B customer even when both IDs are valid.

## 2. Decision Drivers

- Stable identifiers across modules, tasks, imports, and external operations.
- Safe application-side generation before persistence.
- Prevention of cross-tenant relationships.
- Clear distinction between internal identity, public reference, and business numbering.
- Predictable migration and indexing behavior.
- Compatibility with Django and PostgreSQL.
- No reliance on unguessable identifiers for authorization.

## 3. Options Considered

### Option A: UUID primary keys for tenants and major entities with tenant-aware constraints

Use native PostgreSQL UUID/Django UUID fields and explicit tenant-aware relationships.

**Advantages:** globally unique identifiers, safe pre-generation, integration-friendly references, and no centralized sequence dependency.

**Disadvantages:** larger indexes than bigint and random UUID locality concerns.

### Option B: Bigint primary keys everywhere

**Advantages:** compact, fast indexes, and familiar database behavior.

**Disadvantages:** sequential public exposure, coordination for distributed imports, and less portable references.

### Option C: Composite `(tenant_id, local_id)` primary keys

**Advantages:** tenant ownership is inherent in identity.

**Disadvantages:** broad Django complexity, cumbersome foreign keys and URLs, and difficult integration contracts.

### Option D: UUID primary keys without tenant-aware relationships

**Advantages:** simple schema.

**Disadvantages:** global uniqueness does not prevent cross-tenant foreign keys or authorization errors.

## 4. Decision

Use native UUID primary keys for tenants, users, memberships, major business aggregates, externally addressable records, durable operations, audit correlations, and records that cross module or asynchronous boundaries.

The initial implementation should use application-generated UUID version 4 through Django's supported `UUIDField(default=uuid.uuid4, editable=False)` unless a separately reviewed, dependency-supported ordered UUID strategy is adopted before initial migrations.

High-volume internal child, history, or join tables may use bigint keys when a documented database review shows no need for global/public identity and preserves all tenant-aware constraints. Exceptions must be recorded in the model specification before migration.

### 4.1 Identifier categories

Keep these concepts separate:

- Primary key: internal stable row identity.
- Tenant identifier: ownership boundary.
- Public identifier: identifier safe to expose under authorization; it may equal the UUID primary key when approved.
- Business number: human-facing invoice, journal, employee, or document number with domain rules.
- External identifier: provider or customer-system reference, scoped to provider/account/tenant.
- Idempotency key: identifies a retry-safe business request, not necessarily a resource.

Do not use a UUID as an invoice number, accounting sequence, or proof of permission.

### 4.2 UUID storage and validation

Use PostgreSQL's native `uuid` type rather than text. Validate syntax at the transport boundary, but return authorization-safe results after tenant-scoped lookup.

Do not accept a client-supplied UUID for server-owned identity unless the contract explicitly permits client-generated IDs and applies collision, ownership, replay, and authorization controls.

### 4.3 Tenant ownership

Every tenant-owned table must have an authoritative ownership path. Prefer a direct, non-null, immutable `tenant_id` foreign key on major tenant-owned tables, even when ownership could be derived through another relationship.

An indirect path requires explicit justification, database and service enforcement, query-performance analysis, and equivalent security tests.

### 4.4 Tenant-aware references

For relationships between tenant-owned records, ensure child and parent belong to the same tenant. The preferred database pattern for critical relationships is:

1. Parent has a unique constraint on `(tenant_id, id)`.
2. Child stores `tenant_id` and the parent ID.
3. A composite foreign key references `(tenant_id, id)`.

This supplements the ordinary primary key and RLS. Where Django does not express the required composite foreign key directly, use reviewed migrations or another enforceable database mechanism and keep migration state aligned.

Application validation alone is insufficient for high-integrity financial, tenant, user-membership, document, and ownership relationships when a practical database constraint exists.

### 4.5 Ownership immutability

Tenant ownership must not change through ordinary model updates, serializers, forms, bulk operations, or admin editing. A supported transfer between tenants requires a dedicated, authorized, audited migration workflow that validates the entire relationship graph and legal implications. If no approved transfer exists, reject the operation.

### 4.6 Platform-global records

Global records may omit `tenant_id` only when their ownership classification is documented. Nullable `tenant_id` must not be used casually to mix global and tenant rows because it complicates uniqueness, RLS, and authorization.

Tenant-specific overrides of global configuration should normally use a separate tenant-owned record linked to the global definition.

### 4.7 External identifiers

Store provider identifiers separately and scope uniqueness to the relevant tenant, provider, account, environment, and object type. Never assume an external identifier is globally unique or safe to expose.

Preserve provider and environment context during provider migration or test-to-production transitions.

### 4.8 Business numbering

Human-facing numbers follow domain-specific, concurrency-safe sequences and legal/business rules. They may be unique per tenant, legal entity, document type, period, or another approved scope.

Do not generate them from row counts, maximum existing values without locking, UUID formatting, or database primary-key order.

### 4.9 Indexing and performance

UUID primary keys require normal primary-key indexes. Tenant access patterns additionally require indexes beginning with `tenant_id` and relevant filter/order columns. Composite foreign keys require supporting indexes selected from actual query patterns.

Measure write amplification, index size, page locality, and query plans before changing UUID strategy. Do not adopt an ordered UUID library solely on theoretical performance.

### 4.10 APIs, tasks, and logs

Pass stable UUIDs and explicit tenant/operation identifiers in task and API contracts. Consumers reload and validate ownership; message possession is not authorization.

Logs may include identifiers needed for correlation under the data-classification policy, but must avoid exposing sensitive business numbers or external references unnecessarily.

## 5. Rationale

UUIDs suit a modular system with asynchronous work and external contracts because IDs can be generated before persistence and remain stable across boundaries. Direct tenant ownership and composite references address the security property UUIDs cannot provide. Allowing reviewed bigint exceptions prevents UUID policy from imposing needless cost on internal high-volume tables.

## 6. Consequences

### Positive consequences

- Stable identifiers across processes and integrations.
- Reduced accidental exposure of sequential volume.
- Strong database enforcement of cross-tenant relationships.
- Clear separation from business numbering and provider references.

### Negative consequences and trade-offs

- Larger keys and indexes than bigint.
- UUIDv4 insert locality may reduce index efficiency at scale.
- Composite constraints can require custom migrations and careful Django state management.
- Direct `tenant_id` duplicates derivable ownership for some child records.

### Risks and mitigations

- **UUID treated as authorization:** tenant-scoped lookup and negative access tests.
- **Cross-tenant foreign key:** composite constraints and service validation.
- **Index growth:** targeted indexes, monitoring, and evidence-based exceptions.
- **External collision or reuse:** scoped uniqueness including provider/environment.
- **Ownership mutation:** frozen fields, service restrictions, and database enforcement.

## 7. Security and Tenant-Isolation Implications

- Guess resistance is not an access control.
- All identifier resolution is tenant- and permission-scoped.
- Error responses must not reveal cross-tenant existence unnecessarily.
- Composite references and RLS provide independent protection.
- Bulk imports and support tools must validate every tenant-aware relationship.

## 8. Data Integrity and Migration

- Primary-key strategy must be settled before initial migrations for foundational models.
- Changing deployed primary-key type is a material migration requiring a separate plan.
- Add and validate tenant-aware constraints before relying on them for security.
- Backfills must derive tenant ownership unambiguously and quarantine conflicts.
- Migration and runtime roles must preserve ADR-004 protections.

## 9. Operational Impact

Operations must monitor index growth, constraint violations, failed ownership backfills, external-ID collisions, and sequence contention. Backup, restore, import, and tenant-recovery tooling must preserve UUIDs and tenant-aware relationships.

## 10. Implementation Requirements

1. Define an approved base UUID model convention.
2. Document identifier category and tenant ownership for every model.
3. Use native PostgreSQL UUID types.
4. Add direct immutable `tenant_id` to major tenant-owned records.
5. Add composite constraints for critical same-tenant references.
6. Scope external-ID uniqueness by provider/account/environment.
7. Implement concurrency-safe business numbering separately.
8. Add architecture and migration checks for missing ownership and unsafe references.

## 11. Validation and Acceptance Criteria

- [ ] Foundation and major business entities use the approved UUID convention.
- [ ] Every tenant-owned model has a documented ownership path.
- [ ] Tenant A records cannot reference Tenant B parents.
- [ ] Tenant ownership cannot change through ordinary APIs, forms, admin, or bulk updates.
- [ ] UUID possession does not bypass authorization.
- [ ] Business numbers and external IDs are separate from primary keys.
- [ ] External uniqueness includes the required provider and environment scope.
- [ ] Composite constraints and indexes are migration-tested on PostgreSQL.
- [ ] Backfills detect and report ambiguous or cross-tenant data.
- [ ] Query plans and index sizes are reviewed for high-volume tables.

## 12. Alternatives Rejected

- Bigint for every major/public entity is rejected as the default.
- Composite primary keys for all tenant tables are rejected due to Django complexity.
- UUIDs without tenant-aware constraints are rejected as insufficient isolation.
- UUID-derived business document numbers are rejected.
- Ordered UUID dependencies are deferred until measured need and compatibility justify them.

## 13. References

- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- `docs/01-architecture/API_STANDARDS.md`
- Django UUIDField: https://docs.djangoproject.com/en/stable/ref/models/fields/#uuidfield
- PostgreSQL UUID type: https://www.postgresql.org/docs/current/datatype-uuid.html
- PostgreSQL constraints: https://www.postgresql.org/docs/current/ddl-constraints.html

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** UUIDv4 primary keys for foundational and major entities, with documented bigint exceptions and database-enforced tenant-aware references.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; an ordered UUID strategy may be proposed before initial migrations only through a supported, evidence-based review.

This accepted decision governs foundational model identifiers and tenant-aware references. Initial migrations still require an authorized P01 task and reviewed constraint design.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial UUID and tenant-aware reference decision accepted after standards review. |
