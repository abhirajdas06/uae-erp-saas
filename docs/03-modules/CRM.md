# CRM — Customer Relationship Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-CRM-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Owning Phase | P03 |
| Django App | `crm` |
| Domain Owner | Customer Relationship Management |
| Commercial Module | Yes |
| Tenant-Owned Data | Yes |

## 1. Purpose and Sources

Own tenant customer/account, contact, lead, opportunity, pipeline, activity, and relationship history needed by revenue workflows. This module implements `CRM-001`–`CRM-003` under the [P03 phase specification](../02-phases/P03_CRM_SALES_INVOICING/P03_PHASE_SPECIFICATION.md), Module Catalogue CRM boundary, ADR-003 through ADR-006, ADR-014, ADR-015, and ADR-018 through ADR-020.

## 2. Scope

### 2.1 Included

- Customer/business account and individual-customer records according to approved party policy.
- Contacts and validated relationships to accounts.
- Leads, opportunities, pipelines/stages, ownership/assignment, activities, notes, tasks, and source tracking.
- Duplicate-candidate detection/review, search/filtering, import/export, audit, and downstream reference contract.

### 2.2 Excluded

- Quotations/orders (`sales`), invoices/payments (`invoicing`), supplier master, marketing automation, communications delivery platform, accounting, and universal master-data management.
- Automated merging, deletion, enrichment, consent claims, or identity resolution without approved policy.

## 3. Actors and Authorization

| Actor | Typical permissions |
|---|---|
| CRM user | View/create/update records in assigned organizational/object scope |
| Sales representative | Manage own/assigned leads, opportunities, contacts, and activities |
| Sales manager | Assign, approve merge/closure where configured, and report within scope |
| Data steward | Review duplicates, merge/retire under controlled policy, manage reference data |
| Tenant administrator | Configure tenant-approved stages/sources/fields, not platform security controls |
| Support/auditor | Purpose-bound privileged read or audit review; no implicit mutation |

Every operation requires CRM entitlement and user/object permission. Assignment does not transfer tenant ownership. Sensitive contact fields and exports may need narrower permissions.

## 4. Domain Ownership

| Record/capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Customer/account | `crm` | Direct tenant | Customer service |
| Contact and account-contact relationship | `crm` | Direct/inherited tenant | Contact service |
| Lead/opportunity | `crm` | Direct tenant | Workflow service |
| Pipeline/stage/source configuration | `crm` | Tenant configuration | Configuration publication service |
| Activity/note/task | `crm` | Parent plus direct tenant | Activity service |
| Customer snapshot in sales/invoice | Owning downstream document | Tenant inherited from document | Created only by downstream service |

Sales and Invoicing reference stable CRM IDs and snapshot required facts. They must not maintain competing customer-master rows.

## 5. Data Model Requirements

Conceptual entities: `CustomerAccount`, `Contact`, `AccountContact`, `Lead`, `Opportunity`, `Pipeline`, `PipelineStage`, `CRMActivity`, `CRMTask`, `LeadSource`, `DuplicateCandidate`, and `MergeOperation`.

- UUID public IDs and explicit tenant IDs on tenant-owned aggregate/search tables.
- Same-tenant constraints across accounts, contacts, leads, opportunities, stages, activities, assignments, and users where enforceable.
- Names, identifiers, email/phone, addresses, tax/registration references, language, status, source, owner, timestamps, and custom data are typed/normalized and minimized.
- Search indexes are tenant-leading; sensitive identifiers are not exposed through global search.
- Tenant-scoped uniqueness only where business policy proves uniqueness; names alone are not unique.
- Retire/archive rather than hard-delete when downstream financial/history references exist.
- Notes and custom fields follow size, content, classification, and allowlist rules; no unrestricted executable markup.

## 6. Workflows and States

### 6.1 Customer/contact lifecycle

`ACTIVE`, `INACTIVE`, `BLOCKED` (business-use restriction, not security identity), `MERGED`, and `ARCHIVED` as approved. Create/update normalizes values, evaluates duplicate candidates, validates relationships, writes audit evidence, and preserves downstream references. Merge is a privileged, previewable, idempotent operation that redirects permitted future references while preserving source identity/history.

### 6.2 Lead/opportunity lifecycle

Tenant-configured stages map to stable semantic categories such as open, won, lost, and closed. Transitions validate current version, required fields, owner, reason, probability/value policy, and permissions. Closing/winning never creates an order/invoice directly; it may emit a durable fact consumed by Sales through an approved command.

### 6.3 Activities and assignment

Activities record type, occurred/due time, actor/owner, parent, safe summary, status, and outcome. Assignment changes are authorized and audited. Tasks/reminders are idempotent and tenant-safe; notification delivery is a separate capability.

## 7. Business Rules

| ID | Requirement | Verification |
|---|---|---|
| CRMM-001 | Every CRM record and relationship has one validated tenant | Database/isolation tests |
| CRMM-002 | Customer/account is the authoritative P03 party reference; downstream documents use IDs plus snapshots | Boundary tests |
| CRMM-003 | Required, normalized, and size-constrained fields are validated server-side | Model/form/API tests |
| CRMM-004 | Duplicate rules produce candidates and controlled review; they do not silently merge | Duplicate tests |
| CRMM-005 | Search, counts, suggestions, and exports never cross tenant or permission scope | Security tests |
| CRMM-006 | Pipeline configuration and transitions are versioned, valid, and auditable | Workflow tests |
| CRMM-007 | Assignment/ownership cannot grant access beyond role/object scope | Permission tests |
| CRMM-008 | Current customer changes do not rewrite sales/invoice snapshots | Integration tests |
| CRMM-009 | Referenced records are retired/merged through controlled workflows, not casually deleted | Retention tests |
| CRMM-010 | Notes, imports, and exports are sanitized and data-minimized | Security tests |

## 8. Tenant Isolation, Security, and Privacy

Use trusted tenant context in requests, services, tasks, reports, search, autocomplete, imports, exports, cache, and admin. Validate tenant ownership before revealing object existence. RLS is defense-in-depth where approved. Prevent IDOR, mass assignment, stored XSS, formula injection, unauthorized field selection, unbounded queries, and inference through duplicate/search results.

Classify contact details and relationship notes as customer business data; collect only necessary data and restrict bulk export. Do not log full notes, identifiers, addresses, email bodies, or imported rows. Retention/anonymization requires a record-category policy that preserves financial references and audit evidence.

## 9. Entitlements and Degraded Access

`CRM` entitlement is required for normal CRM operations. Authorization remains separately required. On suspension/expiry, new/updated CRM operations deny by default; approved read/export or integrity-preserving access may remain available according to P02 policy. Deactivation never deletes records or invalidates downstream historical references.

## 10. Integrations and Events

Expose read-only customer/contact snapshot services and stable events such as customer changed/merged and opportunity won only after contract approval. Payloads carry minimal IDs/versioned facts. Downstream domains must tolerate customer retirement/merge and preserve their snapshots. Reliable follow-up uses ADR-010; tasks reload tenant and current operation state.

No CRM workflow creates accounting entries, invoice rows, or stock movements.

## 11. UI, API, Reports, Imports, and Exports

Django/HTMX workflows cover list/search, detail, create/update, duplicate review, assignment, pipeline board/list, activities, and history. Accessible forms provide explicit validation and conflict messages. DRF is used only for an approved client under ADR-020.

Imports require template/version, mapping preview, validation report, duplicate strategy, bounded batch, row-level outcomes, idempotency, and rollback/compensation policy. Exports are permission/tenant scoped, audited, formula-injection safe, private, and asynchronously generated above an approved threshold. CRM reports define population, dates, stage semantics, and access scope.

## 12. Operations, Migration, and Recovery

Monitor duplicate backlog, import failures, invalid transitions, stale assignments/tasks, search latency, export volume, cross-tenant denials, and event backlog. Migration/backfill preserves tenant ownership, stable IDs, merge redirects, and history. Backup/restore tests verify relationships, counts, search indexes, merge mappings, and downstream reference reconciliation.

## 13. Acceptance Criteria, Tests, and Evidence

Acceptance criteria are `CRMM-001`–`CRMM-010` and P03-AC-001–003, 016–020. Required tests are P03-TST-001–018, 102–152 as applicable. Evidence is P03-EV-002–004 and P03-EV-009–012 in the [P03 matrix](../02-phases/P03_CRM_SALES_INVOICING/P03_TRACEABILITY_AND_TEST_MATRIX.md).

## 14. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| P03-DEC-001 | Customer/party master model and individual vs organization support | Product/Architecture/Privacy | CRM schema | CRM owns one customer-account abstraction with typed party details; avoid a premature universal party model |
| CRM-DEC-001 | Duplicate matching and merge approval | Product/Data Steward/Security | Merge activation | Start with deterministic candidates and human-reviewed merge; no automatic destructive merge |
| CRM-DEC-002 | Custom fields and sensitive-field policy | Product/Security/Privacy | Custom-field implementation | Use typed allowlisted fields with classification, limits, and export rules |

## 15. Implementation Prompt

Use [P03 orchestration](../04-agents/phase-prompts/P03_CRM_SALES_INVOICING.md) and P03-T02/T03 in [P03 bounded tasks](../04-agents/phase-prompts/P03_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest.
