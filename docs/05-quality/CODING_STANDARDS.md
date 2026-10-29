# Coding Standards

| Property | Value |
|---|---|
| Document ID | QUAL-CODE-001 |
| Status | READY FOR REVIEW — TOOL VERSIONS SELECTED IN AUTHORIZED P01 TASK |
| Applies to | Python, Django, templates/HTMX, JavaScript where necessary, SQL/migrations, tests and configuration |

## 1. General

- Prefer clear domain language, small explicit services and the simplest design satisfying approved requirements.
- Preserve Django app ownership and avoid circular dependencies, hidden signals and cross-domain model mutation.
- Public/service contracts are typed or schema-defined and versioned when externally consumed.
- Comments explain constraints or rationale, not obvious syntax. Dead/speculative code is prohibited.
- Dependency additions require need, maintenance/security/license review and lockfile update.

## 2. Python and Django

- Follow supported Python/Django conventions and one automated formatter/linter selected and pinned in P01.
- Use explicit imports and type annotations at service/contracts boundaries.
- Validate input at trust boundaries; server state, permission, entitlement and tenant ownership remain authoritative.
- Put material workflows in application services with explicit transactions; views/forms/serializers remain adapters.
- Avoid business logic in templates, model `save()`, global middleware side effects or ungoverned Django signals.
- Use timezone-aware datetimes, `Decimal` for money and approved currency/rounding policies.
- Querysets, managers, caches, files, tasks and admin paths are tenant-safe by construction and tested negatively.

## 3. Database and Migrations

- PostgreSQL is authoritative. Constraints enforce critical uniqueness, referential, tenant and financial invariants.
- UUID possession is never authorization. Same-tenant critical references use approved database enforcement.
- Migrations are reviewed, deterministic, data-safe, compatible with deployment strategy and tested on clean/upgrade paths.
- Do not rewrite shared migration history or use automatic destructive rollback.
- Indexes require query/constraint rationale; raw SQL requires parameterization, ownership and PostgreSQL tests.

## 4. UI, API and Files

- Server-rendered Django/HTMX is default; DRF/API exists only for an approved consumer.
- Accessible semantic HTML, keyboard behavior, CSRF protection, safe escaping and localized formatting are mandatory.
- API/errors expose stable safe codes, not secrets, stack traces or cross-tenant existence.
- Uploaded/generated files are private, validated, scanned/quarantined as required and downloaded only after fresh authorization.

## 5. Tests and Review

- Tests are deterministic, isolated, readable and assert externally meaningful behavior and invariants.
- No hidden skip, network/time dependency or shared mutable fixture without explicit control.
- Security and financial regressions receive permanent tests.
- Review checks architecture, correctness, scope, tests, migrations, operations, privacy and evidence—not style alone.

Exact formatter/linter/type-checker versions and thresholds are implementation decisions recorded with P01 evidence; this document does not invent them.
