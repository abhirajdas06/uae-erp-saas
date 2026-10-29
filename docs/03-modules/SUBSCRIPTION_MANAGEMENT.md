# SUBSCRIPTIONS — Subscription Management Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-SUBSCRIPTIONS-001 |
| Status | APPROVED SPECIFICATION — IMPLEMENTATION NOT AUTHORIZED |
| Owning Phase | P02 |
| Django App | `subscriptions` |
| Domain Owner | Subscription Management |
| Commercial Module | No; platform commercial-control capability |
| Tenant-Owned Data | Mixed: global catalogue/policy and tenant subscriptions |

## 1. Purpose and Sources

Own the authoritative module catalogue, subscription aggregate, tenant module selections, lifecycle, effective-dated commercial configuration references, and controlled subscription changes. It implements `SUB-001`, `SUB-002`, `SUB-004`, and `SUB-005` under the [P02 phase specification](../02-phases/P02_SUBSCRIPTION_ENGINE/P02_PHASE_SPECIFICATION.md), [Commercial Model](../00-product/COMMERCIAL_MODEL.md), [Module Dependencies](../01-architecture/MODULE_DEPENDENCIES.md), ADR-003, ADR-004, ADR-005, ADR-006, ADR-010, ADR-014, ADR-015, and ADR-018.

## 2. Scope

### 2.1 Included

- Stable module definitions, lifecycle and commercial release state.
- Versioned plan, offer, price-reference, and dependency policy publication.
- Tenant subscription, selections, scheduled changes, lifecycle, history, previews, and reconciliation.
- Approved platform overrides and provisioning-operation tracking.
- Service contracts consumed by entitlement and billing.

### 2.2 Excluded

- SaaS charges, invoices, payment attempts, and credits (`billing`).
- User roles and object permissions (`users`/`tenants`).
- Feature implementation inside commercial ERP modules.
- Provider-specific payment logic and invented commercial policy.

## 3. Actors and Authorization

| Actor | Permitted scope |
|---|---|
| Platform catalogue administrator | Draft configuration; cannot publish without publication permission and required review |
| Platform commercial approver | Publish approved effective-dated configuration and lifecycle policy |
| Tenant subscription administrator | View own subscription, preview and request permitted changes |
| Billing service principal | Read referenced subscription facts; submit verified billing outcome through a controlled service |
| Support operator | Time-bounded, purpose-limited access under privileged-access policy |
| Auditor | Read authorized history and evidence; no mutation |

All mutations require trusted tenant/platform context, explicit permission, and a service-layer command. Entitlement never grants these permissions.

## 4. Domain Ownership

| Record/capability | Owner | Tenant path | Mutation interface |
|---|---|---|---|
| Module definition/lifecycle | `subscriptions` | Platform-global | Catalogue publication service |
| Dependency/policy version | `subscriptions` | Platform-global | Policy publication service |
| Plan/offer configuration | `subscriptions` | Platform-global | Commercial configuration service |
| Subscription | `subscriptions` | Direct tenant/account | Subscription lifecycle service |
| Subscription selection | `subscriptions` | Inherited from subscription | Subscription-change service |
| Change preview/request/operation | `subscriptions` | Inherited from subscription | Preview/commit service |
| Entitlement history/override | `subscriptions` | Direct/inherited tenant | Entitlement services only |

Other apps may reference stable identifiers and call services; they must not mutate these tables.

## 5. Data Model Requirements

Conceptual entities include `ModuleDefinition`, `ModulePolicyVersion`, `ModuleDependency`, `PlanVersion`, `PlanModule`, `PriceReference`, `Subscription`, `SubscriptionSelection`, `SubscriptionChange`, `SubscriptionOperation`, `EntitlementRecord`, and `EntitlementOverride`.

- Public and aggregate IDs are UUIDs; stable module codes are immutable, unique, case-normalized, and never reused.
- Tenant-owned tables carry or inherit an authoritative tenant key with enforceable same-tenant references.
- Published configuration is versioned and immutable; corrections create a new version.
- Effective ranges must be valid and non-overlapping where exclusivity is required.
- One current subscription per approved account/scope is enforced according to the commercial model.
- Status, version, effective period, source configuration, actor, correlation, and idempotency evidence are explicit.
- Deletion is restricted; referenced or historical records are retired, ended, or superseded.

This is a conceptual contract, not authorization to create migrations.

## 6. Workflows and States

### 6.1 Configuration publication

`DRAFT → REVIEWED → PUBLISHED → SUPERSEDED/RETIRED`. Publication validates codes, effective dates, prices, dependency closure, lifecycle eligibility, approvals, and impact. Published records are immutable.

### 6.2 Subscription lifecycle

Minimum conceptual states are `DRAFT`, `PENDING_ACTIVATION`, `ACTIVE`, `PAST_DUE` (only if policy approved), `SUSPENDED`, `CANCELLATION_SCHEDULED`, `CANCELLED`, and `EXPIRED`. Exact transitions and access consequences are policy data, not scattered `if` statements.

### 6.3 Change workflow

1. Load aggregate under trusted tenant context and lock/version precondition.
2. Authorize actor and validate idempotency key.
3. Resolve effective configuration and dependency closure.
4. Produce a deterministic preview: selections, dates, charge instructions, data-access impact, and warnings.
5. Obtain required customer/platform confirmation.
6. Commit subscription state, history, audit, and outbox intent atomically.
7. Execute provisioning/billing follow-up idempotently and reconcile final state.

Repeated identical commands return the original outcome. Reuse with a different payload conflicts. Invalid or partially failed changes leave no contradictory active selection.

### 6.4 Suspension, cancellation, and reactivation

Access behavior, grace, billing, export, read-only mode, and effective date must come from an approved policy. When undecided, the transition is disabled. No lifecycle transition deletes tenant business records.

## 7. Business Rules

| ID | Requirement | Verification |
|---|---|---|
| SUBM-001 | Code installation, module lifecycle, commercial availability, tenant entitlement, and user permission remain distinct | Model/service review |
| SUBM-002 | Only published effective configuration may create a commercial commitment | State/permission tests |
| SUBM-003 | Dependency graphs are acyclic and all required closure is explicit before commit | Graph tests |
| SUBM-004 | No new paid dependency is added silently to an existing agreement | Change-preview tests |
| SUBM-005 | Every change preserves source policy/price versions and history | History tests |
| SUBM-006 | Commands are authorized, tenant-scoped, idempotent, concurrency-safe, and audited | Security/concurrency tests |
| SUBM-007 | Unsupported or undecided commercial behavior fails closed | Negative tests |
| SUBM-008 | Module removal or subscription end never deletes business data | Lifecycle/integration tests |
| SUBM-009 | Business apps cannot grant, revoke, or modify subscription selections directly | Boundary tests |
| SUBM-010 | Billing outcome affects lifecycle only through an approved subscription service | Integration tests |

## 8. Tenant Isolation, Security, and Entitlements

Catalogue data is platform-global but publication is privileged. Tenant subscriptions, changes, entitlements, overrides, exports, tasks, caches, and audit queries are tenant-scoped. RLS is defense-in-depth where approved. UUID possession and a valid entitlement are not authorization.

Subscription management is a platform foundation capability, not a purchasable module. Tenant self-service remains permission-controlled even during degraded commercial access when the approved policy permits billing/remediation access.

## 9. Integrations and Events

Synchronous contracts: get effective subscription snapshot; preview/commit change; submit verified billing disposition; evaluate configuration impact. Durable events/commands include `subscription.changed.v1`, `subscription.lifecycle_changed.v1`, `entitlement_recompute_requested.v1`, and provisioning/billing instructions. Names are illustrative until the event catalogue is approved.

All material follow-up uses ADR-010 where loss matters. Payloads contain identifiers and minimal versioned facts, not secrets or full sensitive records. Consumers validate tenant and current operation state.

## 10. UI, API, Reports, and Exports

Django/HTMX screens cover authorized catalogue publication, tenant subscription summary, change preview/confirmation, history, override review, and reconciliation. DRF requires an approved consumer and ADR-020 contract. Lists are scoped and paginated; validation is repeated server-side.

Exports are asynchronous above an approved threshold, tenant-scoped, audited, formula-injection safe, access-controlled at download, and retained for a bounded period.

## 11. Financial and Regulatory Considerations

Subscription configuration references prices but does not own issued billing records. Currency, precision, and rounding follow ADR-013. Pricing, proration, tax, trial, grace, dunning, refund, and cancellation choices remain commercial/finance decisions. No document or state implies UAE tax or legal compliance without authoritative validation.

## 12. Operations, Migration, and Recovery

Monitor invalid graphs, publication failures, conflicting transitions, stuck operations, override usage, reconciliation mismatch, and entitlement recompute backlog. Provide bounded dry-run/replay and repair services; prohibit ad hoc row edits. Migrations preserve stable codes and published versions and support controlled old/new deployment overlap.

## 13. Acceptance Criteria and Tests

Acceptance criteria are `SUBM-001`–`SUBM-010` plus P02-AC-001–009, 014–018. Required tests are P02-TST-001–054 and 082–118, including unit, database, service, permission, tenant-isolation, task, migration, performance, and recovery tests in the [P02 matrix](../02-phases/P02_SUBSCRIPTION_ENGINE/P02_TRACEABILITY_AND_TEST_MATRIX.md).

## 14. Evidence and Definition of Done

Required: reviewed schema/ownership, migration evidence, dependency and state-machine reports, authorization/isolation matrix, concurrency/idempotency results, outbox/reconciliation evidence, audit/redaction review, operations runbook, CI artifacts, unresolved-decision disposition, independent review, and phase evidence links. Planned behavior must not be documented as implemented.

## 15. Pending Decisions

| ID | Decision | Owner | Required before | Recommendation |
|---|---|---|---|---|
| CM-DEC-001–019 | Pricing, intervals, trials, grace, dunning, discounts, refunds, tax, retention, cancellation | Product/Commercial/Finance/specialist | Affected flow activation | Version decisions; leave undecided flows disabled |
| ENT-DEC-012 | Override approvers and process | Product/Security | Override implementation | Least privilege, expiry, reason, independent review for material grants |
| SUBM-DEC-001 | Account-to-subscription cardinality | Product/Architecture | Schema implementation | One active commercial subscription per tenant initially unless approved use case requires more |

## 16. Implementation Prompt

Use [P02 orchestration](../04-agents/phase-prompts/P02_SUBSCRIPTION_ENGINE.md) and the applicable prompt in [P02 bounded tasks](../04-agents/phase-prompts/P02_BOUNDED_TASK_PROMPTS.md). Every coding task requires an authorized manifest.
