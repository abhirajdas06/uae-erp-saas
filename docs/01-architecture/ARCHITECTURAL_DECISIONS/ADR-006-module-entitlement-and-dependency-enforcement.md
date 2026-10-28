# ADR-006: Module Entitlement and Dependency Enforcement

| Field | Details |
|---|---|
| ADR ID | ADR-006 |
| Title | Module Entitlement and Dependency Enforcement |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / Product Owner |
| Reviewers | Product, Architecture, Security, Commercial, Finance, Development |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-001, ADR-003, ADR-004, ADR-005, ADR-010, ADR-018 |
| Related Requirements | PRD-001–PRD-003, SUB-001–SUB-005, BILL-001–BILL-004, IAM-003–IAM-004, NFR-001, NFR-005, NFR-007 |
| Related Documents | `MODULE_CATALOGUE.md`, `COMMERCIAL_MODEL.md`, `MODULE_DEPENDENCIES.md`, `ENTITLEMENT_ENGINE.md`, `AUTHENTICATION_AND_PERMISSIONS.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

Customers may subscribe to selected ERP modules. Effective access depends on more than whether code is installed: the product module must be released, the tenant's subscription and module selection must be valid, required dependencies must be satisfied, temporary restrictions or overrides may apply, and the user must still have permission for the requested operation.

If each view, API, task, or business app implements these rules independently, behavior will drift and customers may gain unauthorized access or lose appropriate access to historical records. Commercial changes must also avoid deleting business data or confusing SaaS subscription billing with ERP customer invoicing.

## 2. Decision Drivers

- Central and consistent server-side entitlement decisions.
- Configurable commercial modules, dependencies, plans, and effective dates.
- Independence between tenant entitlement and user authorization.
- Safe activation, suspension, expiry, downgrade, and reactivation.
- Preservation of customer business data when access changes.
- Auditable and idempotent subscription changes.
- Fail-safe cache and background-task behavior.
- No hardcoded commercial rules scattered across modules.

## 3. Options Considered

### Option A: Central entitlement and dependency service in `subscriptions`

Maintain authoritative commercial state and expose one evaluation contract used by all transports and domains.

**Advantages:** consistent decisions, auditable changes, configurable rules, testable dependency graph, and controlled caching.

**Disadvantages:** critical shared service requiring strong availability and careful API design.

### Option B: Per-module entitlement checks

**Advantages:** local implementation autonomy.

**Disadvantages:** duplicated logic, inconsistent expiry and dependency behavior, and weak auditability.

### Option C: Feature flags as entitlements

**Advantages:** common tooling and rapid toggles.

**Disadvantages:** feature flags do not represent contractual subscription state, price history, dependencies, or customer data-access obligations.

### Option D: UI navigation as access control

**Advantages:** minimal backend work.

**Disadvantages:** trivially bypassed through direct URLs, APIs, tasks, and integrations.

## 4. Decision

Implement a centralized entitlement and module-dependency capability owned by `subscriptions`. Every protected module operation must obtain an effective entitlement decision through the approved server-side contract and then independently evaluate user authorization and business rules.

The module catalogue, commercial availability, subscription selection, dependency policy, and effective entitlement are distinct concepts with explicit state and effective dates.

### 4.1 Authoritative concepts

| Concept | Responsibility |
|---|---|
| Module definition | Stable code, name, category, lifecycle, and capability metadata |
| Module dependency | Required or conditional relationships and enforcement policy |
| Subscription | Tenant's commercial agreement state and effective period |
| Subscription module | Tenant's selected module and commercial terms |
| Effective entitlement | Derived or materialized result permitting a tenant capability for a bounded period |
| User authorization | Actor permission and scope under ADR-005; not owned by the entitlement engine |
| SaaS billing | Charges and payments in `billing`; does not grant access by itself |

### 4.2 Evaluation contract

The central evaluator accepts trusted inputs such as:

- Tenant identifier.
- Stable module or capability code.
- Evaluation time.
- Requested operation class where access policy distinguishes new writes from historical reads.
- Optional authoritative context required by a documented policy.

It returns a structured result containing:

- Allowed or denied.
- Stable reason code.
- Evaluated module and capability.
- Subscription and policy version references.
- Effective and expiry times where applicable.
- Missing dependencies or blocking states.
- Cacheability and revalidation guidance.

A denial must not be converted into access by the caller. User-facing messages may translate reason codes without exposing sensitive commercial or platform information.

### 4.3 Evaluation order

The evaluator must consider, as applicable:

1. Module exists and is not retired for the requested use.
2. Module is implemented and released for the applicable channel.
3. Tenant is eligible for commercial use.
4. Subscription is active for the evaluation time or an approved grace policy applies.
5. Module selection is effective.
6. Required dependencies are effective.
7. No authorized suspension or restriction blocks the capability.
8. Any override is valid, bounded, and auditable.

Authorization under ADR-005 and object/business validation occur separately, even when a facade composes the checks for callers.

### 4.4 Dependency policy

Dependencies use stable module codes and explicit types:

- Hard dependency: required for activation and continued operation.
- Conditional dependency: required only for a documented capability or configuration.
- Optional integration: enhances behavior but is not required for the parent module.
- Platform prerequisite: bundled technical capability, not separately purchasable.

The dependency graph must be acyclic. Changes must be effective-dated or versioned and evaluated for impact on existing subscriptions before activation.

The system must not silently add a paid dependency, remove access, or change a customer's charges merely because a dependency definition changed.

### 4.5 State changes

Subscription activation, module addition, removal, suspension, expiry, cancellation, and reactivation must use controlled application services with:

- Valid state transitions.
- Current pricing and contract references.
- Dependency validation.
- Transactional persistence.
- Idempotency for repeated requests.
- Concurrency protection.
- Audit events.
- Durable follow-up operations where asynchronous work is required.

Billing success alone must not directly mutate entitlement through an unreviewed callback. Provider events update durable billing operations, which invoke the approved subscription workflow after authenticity and state validation.

### 4.6 Deactivation and historical data

Disabling a module or ending a subscription changes permitted operations; it does not transfer ownership or delete customer business data.

Each module specification must define its approved degraded-access policy, including whether authorized users may:

- View historical records.
- Export data.
- Complete or cancel in-flight operations.
- Correct legally or financially required records.
- Access records only through an administrator or support process.

New business transactions must be denied when the entitlement does not permit them. Retention and legal obligations override automatic deletion.

### 4.7 Overrides

Administrative overrides are exceptional. They require a dedicated permission, reason, start and end time, approved scope, audit event, and review. Permanent untracked override booleans are prohibited.

### 4.8 Caching

Entitlement caches are performance aids, not the authoritative record. Keys must include tenant, module/capability, relevant policy version, and other required scope.

Changes must invalidate or supersede cache entries. Sensitive writes and state transitions should revalidate authoritative state when stale access could cause material harm. Cache failure must not default to granting access.

### 4.9 Background tasks

Tasks must not rely only on an entitlement result captured when they were queued. They must load the durable operation and apply the module's approved execution policy. Some legally required or integrity-preserving follow-up tasks may need to finish after commercial access ends; that exception must be explicit and auditable.

## 5. Rationale

A single evaluator prevents commercial rules from diverging across transports and modules. Separating entitlement from authorization preserves least privilege: a tenant may purchase a module while a particular user remains unauthorized. Versioned dependency rules prevent catalogue changes from silently rewriting existing commercial agreements.

## 6. Consequences

### Positive consequences

- Uniform server-side module access.
- Configurable plans and dependencies.
- Auditable commercial changes.
- Safer retries, caches, and background work.
- Preservation of historical customer data.

### Negative consequences and trade-offs

- The subscriptions domain becomes a critical dependency.
- Policy versioning and invalidation add complexity.
- Every business module must define degraded-access behavior.
- Commercial changes require impact analysis and migration planning.

### Risks and mitigations

- **Stale cache grants access:** short bounded caches, invalidation, and authoritative checks for sensitive writes.
- **Dependency cycles:** graph validation in configuration and CI.
- **Billing-entitlement race:** durable state transitions and reconciliation.
- **Over-entitlement through overrides:** time-bound, scoped, audited approval.
- **Historical data lockout:** module-specific degraded-access policy and export requirements.

## 7. Security and Tenant-Isolation Implications

- Entitlement queries and caches must be tenant-scoped.
- Client-submitted module codes are requests, not proof of access.
- Platform operators require separate authorization for commercial overrides.
- Entitlement reason details must not expose other tenants or internal plan data.
- Tenant isolation under ADR-004 applies even when entitlement is valid.

## 8. Data Integrity and Migration

- Stable module codes must not be reused.
- Subscription and entitlement changes require effective dates and history.
- Unique constraints must prevent duplicate active selections and conflicting effective records.
- Policy migrations must identify affected subscriptions and provide preview, approval, execution, and reconciliation stages.
- No migration may delete tenant business records because a module becomes unavailable.

## 9. Operational Impact

Operations must monitor evaluation failures, invalid dependency graphs, stale caches, inconsistent billing and entitlement state, failed activation jobs, unusual overrides, and subscriptions stuck in transitions. Reconciliation jobs require bounded scope and audited recovery actions.

## 10. Implementation Requirements

1. Implement the authoritative module registry and dependency graph in `subscriptions` or approved configuration owned by that domain.
2. Publish a stable entitlement-evaluation interface.
3. Keep authorization and entitlement APIs separate but composable.
4. Implement transactional and idempotent subscription-change services.
5. Define cache keys, invalidation, and fail-safe behavior.
6. Require each module to define activation and degraded-access policies.
7. Add dependency-cycle and unsupported-combination validation.
8. Reconcile entitlement state with billing and operation records.
9. Audit all material entitlement changes and overrides.

## 11. Validation and Acceptance Criteria

- [ ] Every protected module path uses the central evaluator.
- [ ] Direct URLs, APIs, tasks, reports, and exports cannot bypass entitlement.
- [ ] Valid entitlement does not bypass user authorization.
- [ ] Invalid and cyclic dependency configurations are rejected.
- [ ] Concurrent and repeated subscription changes do not create conflicting state.
- [ ] Cache failure or staleness does not grant unauthorized sensitive access.
- [ ] Suspension, expiry, cancellation, and reactivation follow documented policies.
- [ ] Module removal does not delete business records.
- [ ] Existing subscriptions are not silently charged for new dependencies.
- [ ] Overrides are scoped, time-bound, authorized, and audited.
- [ ] Reconciliation detects billing-entitlement inconsistencies.

## 12. Alternatives Rejected

- Per-module entitlement logic is rejected because it creates inconsistent commercial enforcement.
- Feature flags are rejected as the authoritative subscription record.
- UI-only restrictions are rejected as insecure.
- Payment-provider status is rejected as direct entitlement authority.
- Automatic deletion on module disablement is rejected.

## 13. References

- `docs/00-product/MODULE_CATALOGUE.md`
- `docs/00-product/COMMERCIAL_MODEL.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/01-architecture/MODULE_DEPENDENCIES.md`
- `docs/01-architecture/ENTITLEMENT_ENGINE.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Central entitlement and dependency evaluation owned by `subscriptions`, independent from authorization and SaaS billing.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; pricing, grace periods, dependency transitions, and commercial policy remain Product decisions.

This accepted decision governs the P02 entitlement boundary. P02 implementation remains unauthorized and commercial policy is still unresolved.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial module entitlement and dependency decision accepted after standards review. |
