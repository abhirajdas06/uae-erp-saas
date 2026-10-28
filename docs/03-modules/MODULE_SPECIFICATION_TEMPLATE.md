# MODULE_CODE — Module Specification Template

| Property | Value |
|---|---|
| Document ID | MOD-MODULE_CODE-001 |
| Status | TEMPLATE |
| Owning Phase | PNN |
| Django App | `app_name` |
| Domain Owner | Named application/domain |
| Commercial Module | Yes / No |
| Tenant-Owned Data | Yes / No / Mixed |

## 1. Purpose

Define the business capability and why it belongs in the product.

## 2. Governing sources

Link product requirements, phase specification, architecture documents, ADRs, security/testing standards, and authoritative regulatory sources.

## 3. Scope

### 3.1 Included

List bounded capabilities.

### 3.2 Excluded

List explicit non-goals and later-phase work.

## 4. Actors and authorization

Define actors, tenant membership requirements, permissions, organizational/object scope, separation of duties, support/platform access, and entitlement checks.

## 5. Domain ownership

| Record/capability | Authoritative owner | Tenant ownership path | Mutation interface |
|---|---|---|---|
| Example | `app` | Direct / inherited / global | Application service |

## 6. Data model requirements

Define conceptual entities, identifiers, tenant keys, uniqueness, same-tenant references, protected fields, indexes, retention, and deletion rules. Do not treat this section as a migration.

## 7. Workflows and states

For every material workflow define:

- states and allowed transitions;
- initiating actor and permission;
- validation and invariants;
- transaction boundary;
- idempotency/concurrency behavior;
- audit events;
- correction/cancellation behavior;
- failure and retry behavior.

## 8. Business rules

Use stable requirement identifiers and testable statements.

| ID | Requirement | Verification |
|---|---|---|
| MODULE-001 | Testable rule | Named test/review |

## 9. Tenant isolation and security

Define request, service, task, API, report, export, cache, file, and administrative isolation requirements. Include sensitive-data classification and prohibited logging.

## 10. Entitlements

Define commercial availability, hard/optional/conditional dependencies, enforcement points, behavior after suspension/expiry, and preservation of existing data.

## 11. Integrations and events

Define synchronous service contracts, events/outbox messages, background tasks, external adapters, API/webhook contracts, timeouts, retries, idempotency, reconciliation, and versioning.

## 12. UI and API

Define primary Django/HTMX workflows, accessibility and validation behavior, selective DRF consumers, error semantics, pagination, filtering, and permission enforcement.

## 13. Reports, imports, and exports

Define authorized scope, filters, totals, file formats, asynchronous thresholds, retention, audit, and spreadsheet/formula-injection protections.

## 14. Financial and regulatory considerations

Separate:

- verified authoritative requirements with source/date;
- approved product/accounting policy;
- technical recommendation;
- unresolved specialist decision.

Do not claim compliance.

## 15. Operations and recovery

Define observability, metrics, health dependencies, data-volume assumptions, archival, backup/restore dependencies, reconciliation, support procedures, and failure modes.

## 16. Migration and compatibility

Define clean-install, upgrade, rollback/forward-fix, data migration, existing-tenant, dependency-policy, and contract-compatibility expectations.

## 17. Acceptance criteria

Use stable IDs covering normal, negative, tenant-isolation, authorization, entitlement, transaction, concurrency, idempotency, failure, audit, reporting, and recovery behavior.

## 18. Required tests

Map acceptance criteria to unit, model/database, service, view/API, permission, tenant-isolation, integration, task, migration, security, performance, and end-to-end tests.

## 19. Evidence and definition of done

List required CI artifacts, test reports, migration evidence, review dispositions, documentation, unresolved decisions, and approval records.

## 20. Pending decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|

## 21. Implementation prompt

Link the reusable module prompt and state that every coding task must be further bounded by a task manifest.
