# ADR-019: File and Document Storage

| Field | Details |
|---|---|
| ADR ID | ADR-019 |
| Title | File and Document Storage |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 28 October 2026 |
| Decision Owner | Architecture / Security / Operations |
| Reviewers | Product, Architecture, Security, Privacy, Compliance, Operations, Domain Owners |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-002–ADR-006, ADR-009–ADR-010, ADR-012, ADR-014–ADR-018, ADR-020 |
| Related Requirements | NFR-001–NFR-004, AUD-001, REP-003, INT-001 |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DJANGO_APP_STRUCTURE.md`, `DATABASE_DESIGN.md`, `MULTI_TENANCY.md`, `API_STANDARDS.md`, `EVENT_AND_TASK_PROCESSING.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The platform will store customer attachments, invoices and credit-note renderings, e-invoicing evidence, imports, reports, exports, identity and employment documents, payroll evidence, banking documents, and operational artifacts. These objects vary in sensitivity, lifetime, mutability, size, and legal significance.

PostgreSQL is authoritative for business state, but placing large binary content in ordinary relational tables would increase database size, backup cost, restore time, and transaction load. Keeping production files on container-local disks would make them ephemeral, difficult to share across web and worker processes, and unsafe during replacement or scaling. Public or predictable object URLs would bypass application authorization and tenant isolation.

The design therefore needs a provider-neutral storage boundary, authoritative metadata, tenant-aware authorization, safe upload processing, auditable lifecycle controls, and coordinated recovery without selecting a paid provider or asserting unverified retention obligations.

## 2. Decision Drivers

- Tenant isolation across uploads, downloads, exports, tasks, support operations, and recovery.
- Private-by-default handling of financial, employee, identity, tax, banking, and regulatory evidence.
- Durable storage independent of application containers.
- Database-backed ownership, lifecycle, audit, and integrity metadata.
- Controlled processing of untrusted content.
- Reproducible evidence and immutable versions where business records require them.
- Provider portability and explicit operational responsibility.
- Retention, legal hold, deletion, backup, restore, and reconciliation.
- Bounded cost and performance for large objects and exports.

## 3. Options Considered

### Option A: Private object storage with authoritative relational metadata

Store binary objects in an approved private object-storage service and store ownership, classification, integrity, and lifecycle metadata in PostgreSQL behind a platform storage abstraction.

**Advantages:** durable and scalable object handling, container independence, controlled access, and provider portability.

**Disadvantages:** two coordinated data stores, lifecycle reconciliation, provider cost, and more complex backup and recovery.

### Option B: Store binary objects in PostgreSQL

**Advantages:** one transactional store and simpler atomic metadata/content writes.

**Disadvantages:** database growth, heavy backups and restores, memory and connection pressure, and poor fit for large exports and documents.

### Option C: Store production files on application or shared server filesystems

**Advantages:** simple local development and familiar tooling.

**Disadvantages:** container-local storage is ephemeral; shared filesystems add infrastructure coupling, scaling, permission, and recovery risk.

### Option D: Make objects public or depend on obscure URLs

**Advantages:** simple delivery and caching.

**Disadvantages:** unacceptable authorization, revocation, enumeration, and data-exposure risk.

## 4. Decision

Use an explicit, provider-neutral file-storage abstraction. Production binary content is stored in an approved **private object-storage service**. PostgreSQL stores authoritative metadata, ownership, lifecycle state, and references. Local filesystem storage may be used only in controlled development and test environments and must not define production semantics.

Large binary content is not stored in ordinary PostgreSQL columns unless a separately reviewed requirement justifies a bounded exception.

### 4.1 Ownership and domain boundaries

Each file record has one authoritative owning domain and an explicit parent or business purpose. A shared storage component may provide upload, download, scanning, checksum, and lifecycle primitives, but it does not take ownership of invoice, employee, payroll, banking, or regulatory meaning.

Metadata includes, where applicable:

- Stable file or document-version ID following ADR-014.
- Direct `tenant_id` and `legal_entity_id` where scope requires it.
- Owning domain, parent type, and stable parent reference.
- Opaque generated storage key; original filename is display metadata only.
- Detected and declared media type, byte size, and cryptographic checksum.
- Classification, document category, retention category, and legal-hold state.
- Upload actor, creation time, source, scan state, lifecycle state, and version lineage.
- Encryption/key reference metadata where the approved storage design needs it.

Tenant and parent relationships follow ADR-014's same-tenant reference rules. A storage key, UUID, filename, path prefix, signed URL, or checksum is never an authorization mechanism.

### 4.2 Storage organization

Object keys are generated by the server, are not derived directly from untrusted filenames, and use a tenant-scoped organizational prefix such as:

```text
tenants/<tenant_uuid>/<classification-or-domain>/<opaque_object_key>
```

The prefix supports administration, reconciliation, lifecycle policy, and incident containment. Authorization remains based on trusted metadata and execution context. Bucket, account, or key separation may be strengthened for high-risk classes or contractual isolation after security and operational review.

### 4.3 Upload lifecycle

Uploads use a staged lifecycle:

1. Authorize the action and establish tenant, legal-entity, parent, and entitlement context.
2. Enforce declared size and permitted-type limits before accepting content where possible.
3. Write to a private staging or quarantine location using a generated object key.
4. Calculate integrity metadata and inspect actual content; do not trust extension, filename, or client MIME type.
5. Perform malware or security scanning according to the approved risk policy.
6. Promote to an available state only after mandatory checks succeed.
7. Record audit evidence for sensitive or material uploads.

Rejected, incomplete, infected, abandoned, or orphaned uploads are inaccessible to ordinary users and removed through bounded, auditable cleanup. Direct-to-object-storage uploads, if used, require short-lived, narrowly scoped upload authorization and server-side completion validation before metadata becomes available.

### 4.4 Download and rendering

Every protected download validates identity, active tenant, file metadata ownership, parent ownership, permissions, legal-entity or branch scope, entitlement where applicable, lifecycle state, and any sensitivity-specific control.

The application may stream content or issue a short-lived, object-specific signed URL after authorization. Signed URLs must have bounded expiry and method/scope; they are not persisted as permanent business references. Sensitive downloads and exports are audited where policy requires.

Untrusted content is served with safe `Content-Type` and `Content-Disposition` behavior, content-sniffing protections, and an isolated delivery origin or equivalent controls where active content could affect the application session. Uploaded files are never executed by application processes.

### 4.5 Immutability, versions, and generated documents

Evidence-bearing issued documents, accepted provider artifacts, posted financial attachments, and other protected records are not overwritten in place. Corrections create a new document version or a linked replacement while retaining required history. Ordinary collaborative attachments may be replaced only under an explicitly defined domain policy.

For generated documents, the owning domain specifies whether the authoritative artifact is:

- A stored immutable rendering.
- A reproducible rendering from an immutable business snapshot and template/rule version.
- Both, when evidentiary or operational requirements justify it.

The system must not silently regenerate historical evidence from changed templates or mutable business data and present it as the original.

### 4.6 Exports and temporary artifacts

Exports are high-risk data operations. Data retrieval is tenant-scoped at query time, access is permission-controlled, large jobs follow ADR-009, and completion notifications or downstream delivery follow ADR-010 where reliability matters.

Generated exports are private, inherit tenant and sensitivity classification, have explicit expiry, and are deleted by a monitored cleanup process. Export metadata records requestor, filters or safe criteria, generation status, object reference, expiry, and audit correlation without unnecessarily duplicating exported sensitive values.

### 4.7 Encryption and credentials

Use TLS for transport and approved provider-side encryption at rest. Storage credentials follow ADR-017: no secrets in source, images, URLs, ordinary configuration tables, or logs; use scoped runtime identities and least privilege. Customer-managed keys or application-level envelope encryption require a separate need, key-management design, recovery procedure, and performance review.

### 4.8 Retention, legal hold, and deletion

Retention is category-specific and derives from validated legal, regulatory, contractual, business, and security requirements. Subscription expiry or module disablement does not by itself delete customer business documents.

Deletion is an authorized lifecycle operation that considers parent-state rules, immutable evidence, legal hold, backup retention, provider versioning, and tenant offboarding. Metadata and object deletion use a recoverable or tombstoned workflow where required; failures remain visible and retryable. Exact retention periods are not established by this ADR.

### 4.9 Backup, restore, and reconciliation

Database metadata and object content require coordinated protection. The production design must define:

- Object versioning or equivalent recovery behavior where justified.
- Backup scope, encryption, retention, access, and restore testing.
- Recovery ordering and consistency checks between metadata and objects.
- Handling of missing objects, orphaned objects, partial uploads, and failed deletions.
- Tenant-level export or recovery procedures without uncontrolled cross-tenant exposure.
- RPO/RTO expectations approved under the operational decision process.

A scheduled reconciliation process compares authorized metadata with storage inventory using bounded scopes. It must not expose filenames, keys, or contents across tenants.

### 4.10 Provider selection

The storage adapter must support the required private-object operations without leaking provider-specific SDK objects into domain services. Provider, region, residency, durability class, lifecycle configuration, malware-scanning service, content-delivery topology, and cost controls remain deployment decisions subject to security, legal, privacy, and operational review.

## 5. Rationale

Private object storage separates large durable content from transactional relational state while PostgreSQL preserves trustworthy ownership and lifecycle controls. Provider-neutral application contracts reduce lock-in without pretending all providers are operationally identical. Staged uploads, immutable evidence versions, short-lived delivery, and reconciliation address the principal security and recoverability risks.

## 6. Consequences

### Positive consequences

- Files survive container replacement and worker/web scaling.
- Tenant ownership and access are explicit and testable.
- Sensitive content is private by default.
- Large objects do not dominate relational backups and transactions.
- Evidence versions and generated artifacts have controlled semantics.
- Storage providers can change behind a bounded adapter.

### Negative consequences and trade-offs

- Database and object-store state can diverge and require reconciliation.
- Upload scanning, temporary storage, and cleanup add asynchronous workflows.
- Provider selection, residency, backup, and egress cost remain operational work.
- Fine-grained retention and legal hold increase lifecycle complexity.
- Signed-URL delivery requires careful expiry and incident revocation design.

### Risks and mitigations

- **Cross-tenant file exposure:** trusted metadata authorization, direct tenant ownership, same-tenant constraints, and negative tests.
- **Malicious content:** quarantine, type detection, scanning, isolated delivery, and no execution.
- **Lost or orphaned objects:** durable operation states, checksums, reconciliation, retry, and recovery tests.
- **Permanent leaked access:** private buckets, short-lived scoped URLs, credential rotation, and access logging.
- **Evidence overwritten or regenerated incorrectly:** immutable object versions, document lineage, and snapshot/template versioning.
- **Unbounded storage cost:** size quotas, lifecycle policies, monitored retention, and tenant-aware usage reporting.

## 7. Security and Tenant-Isolation Implications

- Object storage is a tenant-data system even when paths are operational rather than authoritative.
- Runtime identities receive only the bucket, prefix, and operation rights required by their role.
- Download authorization occurs before every stream or signed-URL issuance.
- Sensitive classifications can require step-up authorization, audit, watermarking, or restricted support access.
- Storage events, scan systems, CDNs, backups, and support tools are part of the data-flow and vendor/security review.
- Tests must cover guessed IDs, altered parent references, cross-tenant tasks, expired links, disabled memberships, and malicious filenames/content.

## 8. Data Integrity and Migration

- File metadata changes and object operations use explicit states rather than pretending cross-system atomicity.
- The database record is authoritative for availability and ownership; object presence alone does not make a file valid.
- Checksums detect corruption and support reconciliation but do not replace authenticity controls.
- Storage migrations preserve IDs, ownership, checksums, classifications, retention, version history, and audit evidence.
- Provider migration uses copy, verification, controlled cutover, rollback, and post-cutover reconciliation.
- Protected parent deletion cannot silently orphan or erase required evidence.

## 9. Operational Impact

Operations must manage storage capacity, credentials, encryption, lifecycle policies, malware scanning, reconciliation, backups, restores, region/residency, alerts, and incident response. Monitoring covers failed upload promotion, unavailable objects, scan backlog, expired-export cleanup, abnormal download volume, orphan growth, integrity mismatch, and provider errors.

## 10. Implementation Requirements

1. Define a provider-neutral storage interface and domain-owned file metadata model.
2. Define document classifications, allowed types/sizes, scan policy, and download controls.
3. Implement staged upload states, checksums, promotion, rejection, and orphan cleanup.
4. Implement authorization-checked streaming or signed-URL issuance.
5. Define immutable evidence and document-version rules per domain.
6. Implement export expiry and lifecycle cleanup with audit and failure visibility.
7. Define backup, restore, reconciliation, provider migration, and incident runbooks.
8. Select production provider, region, identity, encryption, lifecycle, and scanning configuration through deployment review.
9. Add tenant-isolation, active-content, malware, expiry, reconciliation, recovery, and lifecycle tests under ADR-015.

## 11. Validation and Acceptance Criteria

- [ ] Production objects are private and independent of application-container filesystems.
- [ ] File metadata has authoritative tenant, owner, classification, checksum, state, and lifecycle fields.
- [ ] Cross-tenant and unauthorized downloads fail even with a valid object key or signed URL request path.
- [ ] Uploads cannot become available before required validation and scanning complete.
- [ ] Filenames, MIME declarations, and tenant-supplied paths are not trusted.
- [ ] Evidence-bearing files cannot be overwritten without versioned domain behavior.
- [ ] Exports are tenant-scoped, audited where required, expire, and are cleaned up.
- [ ] Missing, orphaned, corrupt, and partially deleted objects are detected and recoverable or escalated.
- [ ] Backup and restore tests cover metadata/object consistency and approved tenant recovery scenarios.
- [ ] Storage credentials, logs, and URLs do not disclose reusable secrets or permanent private access.

## 12. Alternatives Rejected

- Container-local or server-local filesystems for production durable content are rejected.
- Public buckets and security through unpredictable object names are rejected.
- Large binary content in ordinary PostgreSQL tables by default is rejected.
- Client-supplied filenames, MIME types, or paths as trusted security input are rejected.
- In-place overwrite of protected evidence is rejected.
- One arbitrary retention period for all documents is rejected.

## 13. References

- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- `docs/01-architecture/DJANGO_APP_STRUCTURE.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- `docs/01-architecture/API_STANDARDS.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Private production object storage behind a provider-neutral abstraction, with authoritative PostgreSQL metadata, staged safe uploads, authorization-checked delivery, versioned evidence, and governed lifecycle/recovery.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; provider, region/residency, retention, scanning, quotas, encryption keys, RPO/RTO, and tenant recovery remain unresolved.

Production provider, region, residency, exact retention periods, malware-scanning implementation, storage quotas, encryption-key model, backup RPO/RTO, and tenant-recovery procedure remain unresolved. They block production storage configuration, not further documentation or provider-neutral interface design.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial file and document storage decision accepted after standards review. |
