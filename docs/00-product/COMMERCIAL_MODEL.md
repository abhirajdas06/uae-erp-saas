# UAE ERP SaaS — Commercial Model

| Document Attribute | Value |
|---|---|
| Document ID | CM-001 |
| Version | 1.0 |
| Status | APPROVED — Commercial Design Baseline; Pricing and Terms Pending |
| Product | UAE ERP SaaS |
| Document Type | Commercial Strategy and Subscription Requirements |
| Parent Document | `docs/00-product/MASTER_PRODUCT_SPECIFICATION.md` |
| Related Documents | `PRODUCT_REQUIREMENTS.md`, `TARGET_MARKET.md`, `MODULE_CATALOGUE.md`, `DEVELOPMENT_ROADMAP.md` |
| Primary Market | United Arab Emirates |
| Commercial Model | Modular Subscription SaaS |
| Currency | AED as the proposed default |
| Intended Audience | Product Owner, Business Analyst, Architect, Development Team, Finance and Operations |

---

# 1. Purpose

This document defines the commercial model for the UAE ERP SaaS platform.

It specifies how the platform will:

- Package and sell software modules.
- Calculate subscription prices.
- Manage monthly and annual subscriptions.
- Support module-based purchasing.
- Handle module dependencies.
- Manage trials and demonstrations.
- Process upgrades, downgrades, and cancellations.
- Record payments and subscription invoices.
- Handle failed payments and overdue accounts.
- Separate SaaS subscription billing from tenant ERP transactions.
- Integrate with external payment providers.
- Support promotions, discounts, and approved commercial adjustments.
- Maintain an auditable record of commercial activity.

This document defines the intended commercial architecture. It does not approve specific prices, payment providers, tax treatments, or contractual terms.

Those decisions must be validated and approved before commercial launch.

# 2. Commercial Objectives

The commercial model should achieve the following objectives.

## 2.1 Modular Purchasing

Customers should be able to subscribe to the ERP capabilities relevant to their businesses rather than being forced to purchase every module.

## 2.2 Expandable Subscriptions

Customers should be able to add supported modules as their business requirements evolve.

## 2.3 Predictable Recurring Revenue

The platform should support recurring subscriptions with clear billing periods, renewal dates, pricing, and payment status.

## 2.4 Configurable Pricing

Authorized administrators should be able to configure prices, billing periods, discounts, and commercial availability without modifying application source code.

## 2.5 Transparent Customer Billing

Customers should be able to understand:

- Which modules they are paying for.
- How their subscription price is calculated.
- When their next payment is due.
- Which invoices have been issued.
- Whether payments have succeeded or failed.
- What happens when they change or cancel their subscription.

## 2.6 Financial Integrity

Subscription calculations, invoice records, payment events, and entitlement changes must be traceable and protected against duplicate processing.

## 2.7 Commercial Scalability

The commercial architecture should support future pricing models without requiring a complete redesign.

Potential future models include:

- Per-module subscriptions.
- Bundled plans.
- Per-user pricing.
- Usage-based charges.
- Paid implementation services.
- Premium support.
- Additional storage or transaction allowances.

These models are not automatically included in the initial release.

# 3. Commercial Model Overview

## 3.1 Proposed Initial Model

The proposed initial model is a recurring subscription based on selected software modules.

Each tenant selects from the modules that are available for commercial sale and compatible with its subscription.

The subscription price is calculated using the approved pricing configuration.

Conceptually:

`Subscription Price = Base Charges + Selected Module Charges + Approved Add-ons - Eligible Discounts`

Taxes and other applicable charges must be calculated according to the approved commercial and tax rules.

The formula is illustrative. The actual calculation engine must be designed to support the approved pricing configuration.

## 3.2 Commercial Components

The commercial model may contain the following components:

| Component | Description | Initial Status |
|---|---|---|
| Module subscription | Recurring charge for an individual module | Proposed |
| Base subscription fee | Common recurring charge independent of selected modules | Decision required |
| Bundled package | A predefined combination of modules | Future option or decision required |
| Per-user charge | Recurring charge based on licensed users | Decision required |
| Usage-based charge | Charge based on measurable usage | Not required for initial release unless approved |
| Trial subscription | Time-limited evaluation access | Decision required |
| Implementation fee | One-time charge for setup or onboarding | Decision required |
| Data migration fee | Charge for agreed migration services | Decision required |
| Premium support | Paid support tier | Future option |
| Integration fee | Charge for specific third-party integrations | Decision required |
| Additional storage | Charge for storage beyond an included allowance | Future option |

Only approved components may be enabled for customer purchasing.

The system must not assume that every commercial component is active.

# 4. Pricing Principles

## 4.1 Pricing Must Be Configurable

Pricing must be stored in database-backed commercial configuration.

Do not hardcode module prices in:

- Django views.
- Serializers.
- Templates.
- Frontend JavaScript.
- Payment-provider callbacks.
- Subscription services.
- API endpoints.
- Background tasks.

Application code should use a centralized pricing service to calculate charges.

The service must use the applicable approved price version and billing rules.

## 4.2 Pricing Currency

AED is the proposed default currency for the initial UAE market.

The system should be designed to support additional currencies in a future release.

Each price record must explicitly identify its currency.

A subscription must not silently change currency after activation.

Changing a customer's subscription currency should require an explicitly supported commercial operation.

## 4.3 Price Precision

All monetary calculations must use decimal arithmetic.

Binary floating-point values must not be used for authoritative monetary calculations.

The system must define:

- Internal decimal precision.
- Currency-specific rounding rules.
- Discount calculation rules.
- Tax calculation rules.
- Invoice rounding behavior.
- Treatment of fractional allocations and prorated amounts.

Use `Decimal` and appropriately configured database decimal fields for financial amounts.

Rounding must occur at documented calculation boundaries rather than arbitrarily throughout the application.

## 4.4 Effective Dates

Prices should have effective dates or versions.

A new price should not silently modify the historical price associated with an existing subscription invoice.

The system must distinguish between:

- Current published prices.
- Future-dated prices.
- Retired prices.
- Historical prices used by existing subscriptions.

When a price changes, the system must follow an approved migration policy.

Existing subscriptions should not automatically be repriced unless the applicable commercial policy explicitly permits it and any required customer notice or consent has been handled.

## 4.5 Price Visibility

Customer-facing prices must be derived from approved commercial configuration.

Customers must not be able to modify the amount they owe by manipulating browser requests or API payloads.

The server must recalculate and validate all charges before creating a subscription, invoice, or payment request.

# 5. Module Catalogue and Commercial Availability

## 5.1 Module States

Each module must have an explicit lifecycle state.

Suggested states:

- `PLANNED`
- `IN_DEVELOPMENT`
- `INTERNAL_ONLY`
- `PILOT`
- `AVAILABLE`
- `DEPRECATED`
- `RETIRED`

The exact implementation may use Django model choices or a controlled reference table.

The commercial rules associated with these states are:

| State | Customer Purchase Allowed? |
|---|---|
| PLANNED | No |
| IN_DEVELOPMENT | No |
| INTERNAL_ONLY | No |
| PILOT | Only for explicitly authorized pilot customers |
| AVAILABLE | Yes, subject to dependencies and subscription rules |
| DEPRECATED | No new purchases unless explicitly approved |
| RETIRED | No |

A module marked `AVAILABLE` must also pass the product's release-approval process.

Changing a module's commercial status must not automatically grant entitlements to every tenant.

## 5.2 Initial Module Catalogue

The following is the proposed commercial catalogue.

Prices remain unapproved until market validation and cost analysis are completed.

| Module Code | Module | Proposed Commercial Purpose |
|---|---|---|
| CRM | Customer Relationship Management | Leads, contacts, opportunities |
| SALES | Sales Management | Quotations, sales orders, sales workflows |
| INVOICING | Customer Invoicing | Customer invoices, credit notes, payment tracking |
| ACCOUNTING | Accounting | Ledgers, journals, financial statements |
| VAT | VAT Management | Tax configuration, tax calculations, reports |
| E_INVOICING | UAE E-Invoicing Integration | Integration with an approved, validated provider |
| PROCUREMENT | Procurement | Suppliers, purchase orders, goods receipts |
| INVENTORY | Inventory Management | Products, stock movements, warehouse operations |
| HRMS | Human Resource Management | Employee records and HR workflows |
| PAYROLL | Payroll | Payroll calculations and records |
| PROJECTS | Project Management | Projects, activities, project tracking |
| EXPENSES | Expense Management | Employee and operational expenses |
| FIXED_ASSETS | Fixed Asset Management | Asset registers and depreciation |
| BANKING | Banking and Reconciliation | Bank transactions and reconciliation |
| REPORTING | Reporting and Analytics | Management reports and analytical views |
| INTEGRATIONS | Integration Hub | Supported external-system integrations |

The catalogue must be maintained in `docs/00-product/MODULE_CATALOGUE.md`.

Do not make every listed module purchasable in the first release.

## 5.3 Dependencies

Module dependencies must be configurable and validated by the server.

Potential examples include:

- VAT may depend on invoicing or accounting capabilities.
- Inventory accounting may depend on accounting.
- Payroll may depend on HRMS.
- Advanced financial reports may depend on accounting.
- E-invoicing may depend on customer invoicing and provider configuration.

These examples require confirmation before being adopted as definitive dependency rules.

When a customer selects a module, the subscription service must:

1. Confirm that the module is commercially available.
2. Confirm that the tenant is eligible to purchase it.
3. Resolve required dependencies.
4. Calculate the resulting charges.
5. Present any additional required modules and their costs.
6. Validate the customer's final selection.
7. Create or update the subscription only after the required confirmation.
8. Generate the appropriate audit events.

The system must not silently add paid modules without informing the customer and obtaining any required approval.

## 5.4 Removing a Dependent Module

If a module is required by another active module, the system must not allow the dependency to be removed while it remains necessary.

It should present the affected modules and require the customer to resolve the dependency.

Possible resolutions include:

- Remove the dependent module.
- Retain the required module.
- Choose a supported alternative configuration.

Dependency changes must not delete business data.

# 6. Subscription Architecture

## 6.1 Core Entities

The commercial domain should distinguish the following entities.

### ProductModule

Represents a software module that may be available for purchase.

Suggested fields:

- `code`
- `name`
- `description`
- `lifecycle_status`
- `commercially_available`
- `sort_order`
- `created_at`
- `updated_at`

### PricePlan

Represents a configurable commercial package or pricing definition.

It may be used for a base subscription, a bundle, or another approved pricing arrangement.

Suggested fields:

- `code`
- `name`
- `description`
- `currency`
- `billing_interval`
- `status`
- `effective_from`
- `effective_until`
- `created_at`
- `updated_at`

### ModulePrice

Represents the price of a module for a particular currency, billing interval, and effective period.

Suggested fields:

- `module`
- `currency`
- `billing_interval`
- `amount`
- `effective_from`
- `effective_until`
- `status`

The design must prevent ambiguous overlapping active prices for the same pricing key and effective date.

### Subscription

Represents a tenant's commercial relationship with the SaaS platform.

Suggested fields:

- `tenant`
- `status`
- `currency`
- `billing_interval`
- `started_at`
- `current_period_start`
- `current_period_end`
- `trial_start`
- `trial_end`
- `next_billing_at`
- `cancel_at_period_end`
- `cancelled_at`
- `created_at`
- `updated_at`

The final schema must support the approved trial and billing lifecycle.

### SubscriptionItem

Represents an individual module or commercial item attached to a subscription.

Suggested fields:

- `subscription`
- `module`
- `price_reference`
- `quantity`, if applicable
- `unit_price_snapshot`
- `billing_interval`
- `effective_from`
- `effective_until`
- `status`

The item must retain the pricing information needed to reconstruct historical charges.

### SubscriptionInvoice

Represents an invoice issued by the SaaS provider to the tenant for platform subscription charges.

Suggested fields:

- `tenant`
- `subscription`
- `invoice_number`
- `currency`
- `subtotal`
- `discount_total`
- `tax_total`
- `total`
- `amount_paid`
- `amount_due`
- `status`
- `issued_at`
- `due_at`
- `period_start`
- `period_end`

The exact tax and legal invoice fields must be confirmed for the SaaS provider's own circumstances.

### PaymentTransaction

Represents an attempted or completed payment associated with an invoice or another approved commercial transaction.

Suggested fields:

- `tenant`
- `invoice`
- `provider`
- `provider_reference`
- `idempotency_key`
- `amount`
- `currency`
- `status`
- `initiated_at`
- `completed_at`
- `failure_code`
- `failure_reason`

Sensitive payment credentials must not be stored in this model.

### SubscriptionEvent

Records important subscription lifecycle events.

Suggested event types include:

- Subscription created.
- Trial started.
- Trial ended.
- Module added.
- Module removed.
- Subscription upgraded.
- Subscription downgraded.
- Renewal initiated.
- Payment succeeded.
- Payment failed.
- Subscription suspended.
- Cancellation requested.
- Subscription cancelled.
- Subscription reactivated.

Events must be traceable and protected from unauthorized modification.

The final entity design belongs in the architecture and database documentation.

# 7. Subscription Lifecycle

## 7.1 Proposed Statuses

The subscription model should support the following conceptual states:

| Status | Meaning |
|---|---|
| DRAFT | Subscription configuration has not been confirmed |
| PENDING | Subscription is awaiting an action, such as payment or approval |
| TRIALING | Tenant is using an approved time-limited trial |
| ACTIVE | Subscription is active and satisfies the applicable commercial rules |
| PAST_DUE | A payment or billing obligation is overdue |
| SUSPENDED | Access has been restricted under the approved policy |
| CANCELLATION_SCHEDULED | Cancellation is scheduled for a future effective date |
| CANCELLED | Subscription has been cancelled |
| EXPIRED | Subscription or trial has ended without an active continuation |

The implementation may distinguish subscription status from payment status and tenant status.

These are separate concepts and must not be represented by a single overloaded field.

## 7.2 Subscription Creation

The proposed subscription creation flow is:

1. Customer creates or selects a tenant.
2. Customer selects an available plan or module combination.
3. Server validates commercial availability and dependencies.
4. Server calculates the subscription price.
5. Customer reviews the selected modules and charges.
6. Customer accepts the applicable commercial terms.
7. The system creates a pending subscription or an approved trial.
8. If payment is required, the system initiates the provider's checkout flow.
9. The provider reports the payment result.
10. The system validates the provider event.
11. The subscription becomes active when the required activation conditions are satisfied.
12. The entitlement engine grants the corresponding module access.
13. The system records the lifecycle events.

A browser redirect to a payment-success page must not, by itself, be treated as proof that payment succeeded.

## 7.3 Subscription Activation

The system must explicitly define activation rules for:

- Paid subscriptions.
- Free trials.
- Approved complimentary subscriptions.
- Offline or manually reconciled payments, if supported.
- Pilot subscriptions.

Activation must follow verified commercial state and must be auditable.

## 7.4 Subscription Renewal

At renewal time, the system must:

1. Determine the applicable billing period.
2. Identify the subscription items that are billable.
3. Resolve the applicable price policy.
4. Calculate the invoice.
5. Apply eligible discounts.
6. Calculate applicable taxes.
7. Create the subscription invoice.
8. Attempt payment through the configured payment workflow, if applicable.
9. Record the result.
10. Update the next billing date when the renewal is successfully processed according to policy.
11. Update subscription and entitlement states where necessary.
12. Send appropriate customer notifications.

Renewal processing must be safe to retry without generating duplicate invoices or charging the customer twice.

## 7.5 Trial Expiration

If trials are enabled, the system must support a defined expiration policy.

Possible policies include:

- Restrict module access at trial expiry.
- Allow a configurable grace period.
- Retain read-only access for a limited period.
- Require payment to continue using paid modules.

The policy must be explicitly approved.

Trial expiration must not delete customer business data.

# 8. Billing Intervals

## 8.1 Supported Intervals

The proposed initial billing intervals are:

- Monthly.
- Annual.

Quarterly billing and other intervals may be introduced later if commercially justified.

The system must represent billing intervals explicitly rather than relying on arbitrary numbers of days.

For example, a monthly subscription should follow calendar-month billing rules, including the defined behavior for start dates near the end of a month.

## 8.2 Annual Billing

Annual billing may offer a discounted effective monthly rate.

However, the discount must be explicitly configured and approved.

The platform must distinguish between:

- Monthly recurring price.
- Annual recurring price.
- Effective monthly equivalent.
- Annual discount.
- Applicable tax.
- Any one-time fees.

The system must not infer an annual price by simply multiplying a monthly price by twelve unless that is the approved pricing rule.

## 8.3 Billing Dates and Time Zones

Billing events must use consistent, documented date and time rules.

Store timestamps using timezone-aware values.

The system must define how tenant-local dates relate to UTC timestamps for:

- Renewal dates.
- Trial expiry.
- Invoice issue and due dates.
- Payment retries.
- Scheduled cancellations.
- Notifications.

Do not rely on the web server's local time zone.

# 9. Upgrades, Downgrades, and Module Changes

## 9.1 Adding a Module

When a customer adds a module:

1. Validate commercial availability.
2. Validate dependencies.
3. Calculate the additional charges.
4. Determine the effective date.
5. Present the price and billing implications.
6. Obtain required confirmation.
7. Update the subscription.
8. Update entitlements when the approved activation condition is satisfied.
9. Record the change.
10. Notify the customer.

The effective date and payment requirement must follow the approved commercial policy.

## 9.2 Removing a Module

When a customer removes a module:

1. Identify dependencies.
2. Identify the effective date.
3. Calculate any applicable credit or adjustment.
4. Explain the impact on access.
5. Obtain required confirmation.
6. Update the subscription schedule.
7. Apply entitlement changes at the correct time.
8. Preserve the tenant's existing business data.
9. Record the change.
10. Notify the customer.

Module removal must not automatically delete module data.

## 9.3 Proration

Proration is a decision requiring explicit approval.

If enabled, the system must define:

- Whether module additions are prorated.
- Whether module removals are prorated.
- Whether credits are issued or carried forward.
- The calculation basis.
- The rounding method.
- The treatment of taxes.
- Whether adjustments are immediate or deferred.

Proration rules must be implemented in a centralized billing service and tested at period boundaries.

Do not invent a proration policy in individual views or payment callbacks.

## 9.4 Downgrade Restrictions

A downgrade must not silently invalidate business operations or delete records.

If removing a module would leave the tenant with data or workflows that are no longer supported, the system must:

- Identify the impact.
- Explain any limitations.
- Preserve the underlying records.
- Apply the approved access policy.
- Prevent unsupported financial or operational state changes.

Data retention and export policies must be documented separately.

# 10. Cancellation and Reactivation

## 10.1 Cancellation Options

The commercial model should support cancellation according to the approved contract.

Possible options include:

- Immediate cancellation.
- Cancellation at the end of the current paid period.

The initial release should implement only the approved option or options.

## 10.2 Cancellation Processing

The cancellation workflow must:

1. Authenticate the requesting user.
2. Verify authorization.
3. Display the cancellation effective date.
4. Explain the impact on paid modules.
5. Obtain confirmation.
6. Record the request.
7. Update the subscription schedule.
8. Notify the customer.
9. Apply entitlement changes at the appropriate effective time.
10. Preserve customer data according to the retention policy.

## 10.3 Reactivation

If reactivation is supported, the system must validate:

- Whether the previous subscription remains eligible for reactivation.
- Whether the original pricing is still valid.
- Whether a new price applies.
- Whether payment is required.
- Whether module availability has changed.
- Whether the tenant has outstanding invoices.
- Whether historical data remains accessible.

Reactivation must not bypass payment or authorization rules.

# 11. Failed Payments and Overdue Accounts

## 11.1 Payment Failure Handling

A payment failure must not automatically delete or corrupt the subscription.

The system must record:

- Payment attempt.
- Provider response.
- Failure code, where available.
- Timestamp.
- Invoice association.
- Retry eligibility.
- Next action.
- Customer notification status.

Do not store sensitive authentication data or full payment-card details.

## 11.2 Retry Policy

The retry schedule is a commercial decision.

If automated retries are enabled, the system should support configurable:

- Retry intervals.
- Maximum attempts.
- Grace period.
- Customer notifications.
- Final failure action.

Avoid embedding a fixed retry schedule in code.

## 11.3 Grace Period

A grace period may allow temporary continued access after a payment becomes overdue.

If enabled, it must define:

- Duration.
- Eligible subscription states.
- Whether all modules remain available.
- Whether new module purchases are permitted.
- When restricted access begins.
- How successful payment restores access.

The grace period must not permit unpaid subscriptions to remain indefinitely active.

## 11.4 Suspension

Suspension must be enforced by the server-side entitlement layer.

The policy may distinguish between:

- Full application access.
- Read-only access.
- Access to billing and subscription management.
- Access to data export.
- Access to selected paid modules.

The approved policy must prioritize reasonable customer data access and avoid destructive actions.

Suspension must not delete customer records, accounting entries, invoices, or audit logs.

## 11.5 Outstanding Balances

The platform must track unpaid invoices independently from subscription status.

The system must not mark an invoice as paid solely because:

- A checkout session was created.
- A payment page was opened.
- A customer returned to a success URL.
- A client-side request claimed success.

Payment status must be based on verified provider information or an authorized, auditable manual reconciliation process.

# 12. Discounts, Promotions, and Credits

## 12.1 Discount Support

The commercial architecture may support:

- Percentage discounts.
- Fixed-value discounts.
- Annual billing discounts.
- Promotional codes.
- Approved customer-specific discounts.
- Time-limited introductory offers.

Only explicitly approved discount types should be implemented in the initial release.

## 12.2 Discount Configuration

A discount definition may contain:

- Unique code.
- Name.
- Discount type.
- Discount value.
- Eligible modules or plans.
- Currency, where applicable.
- Start and expiry dates.
- Maximum redemptions.
- Per-customer redemption limit.
- Minimum purchase amount.
- Eligibility rules.
- Combinability rules.
- Status.

The server must validate all eligibility conditions.

## 12.3 Discount Controls

The system must prevent:

- Reusing expired promotions.
- Exceeding redemption limits.
- Applying discounts to ineligible modules.
- Combining incompatible discounts.
- Manipulating the discount amount through a client request.
- Applying an unauthorized discount to an existing invoice.

Discounts must be traceable to their source and authorizing policy.

## 12.4 Credits and Refunds

Credits and refunds must be separate, explicitly controlled commercial operations.

The system should distinguish between:

- Invoice credit.
- Customer account credit.
- Payment refund.
- Provider-initiated reversal.
- Manual adjustment.

Each operation must retain its amount, currency, reason, authorization, related transaction, and status.

Refunding a payment must not automatically delete the original invoice or payment history.

The accounting treatment and customer-facing documents must follow the approved financial policy.

# 13. SaaS Subscription Invoicing

## 13.1 Separate Billing Domain

The SaaS provider's subscription invoices must be separate from invoices generated by tenant businesses.

For example:

- A tenant paying the platform subscription receives a SaaS subscription invoice.
- That tenant's customer receives an invoice generated by the tenant's ERP.

These invoices serve different commercial relationships and must not share transaction ownership or numbering logic.

## 13.2 Subscription Invoice Requirements

The subscription billing system should support:

- Unique invoice numbers.
- Tenant or customer identification.
- Subscription identification.
- Invoice issue date.
- Billing period.
- Line-item descriptions.
- Module or service references.
- Quantity, where applicable.
- Unit price.
- Discounts.
- Applicable tax.
- Subtotal.
- Total.
- Amount paid.
- Outstanding balance.
- Currency.
- Due date, where applicable.
- Payment status.
- Credit-note or adjustment references, where applicable.

The applicable legal invoice requirements must be confirmed before launch.

## 13.3 Invoice Numbering

Invoice numbering rules must be configurable and must satisfy applicable legal requirements.

The system must prevent duplicate invoice numbers within the required numbering scope.

Invoice numbers must not be generated using unsafe patterns such as an unprotected count of existing rows.

Use database-backed sequences, transactional allocation, or another concurrency-safe strategy.

## 13.4 Invoice Immutability

Once an invoice is issued, the system must preserve its historical financial content.

Corrections must use the approved credit-note, cancellation, or adjustment process.

The application must not silently overwrite an issued invoice's amounts, line items, tax calculations, or identity.

## 13.5 Subscription Provider Tax Treatment

The SaaS provider's own tax obligations must be evaluated separately from the tax treatment of transactions processed by tenant businesses.

The product owner must confirm the applicable invoicing and tax requirements for the SaaS provider before enabling production billing.

# 14. Payment Provider Integration

## 14.1 Provider Selection

The payment provider must be selected after evaluating the SaaS provider's business requirements.

Selection criteria should include:

- UAE business onboarding eligibility.
- Supported currencies.
- Recurring payment support.
- Tokenized payment methods.
- Webhook support.
- Refund support.
- Payment status APIs.
- Checkout experience.
- Security requirements.
- Settlement and reconciliation capabilities.
- Transaction fees.
- Chargeback handling.
- Sandbox availability.
- Documentation quality.
- Operational reliability.
- Commercial contract terms.

No specific payment provider is approved by this document.

## 14.2 Integration Boundary

Payment-provider logic must be isolated behind a defined integration interface.

The subscription domain must not depend directly on provider-specific response formats throughout the codebase.

A provider adapter should translate provider-specific events into the platform's internal payment states.

The design should allow a future provider to be introduced without rewriting subscription lifecycle logic.

## 14.3 Payment Workflow

A typical payment flow is:

1. The subscription service creates an invoice or a pending commercial transaction.
2. The server calculates and stores the amount.
3. The server creates a payment request with the provider.
4. The customer completes the provider-hosted or otherwise approved checkout flow.
5. The provider sends a webhook or another verified payment notification.
6. The system authenticates and validates the notification.
7. The system retrieves authoritative payment status where necessary.
8. The system processes the event idempotently.
9. The payment transaction is updated.
10. The invoice balance is recalculated.
11. Subscription and entitlement states are updated according to policy.
12. An audit event is recorded.
13. The customer receives an appropriate notification.

## 14.4 Webhook Security

Payment webhooks must:

- Validate provider signatures using the provider's documented method.
- Reject invalid or unverifiable requests.
- Validate event identifiers.
- Prevent duplicate processing.
- Handle out-of-order events.
- Avoid trusting client-supplied payment amounts.
- Record relevant event metadata.
- Avoid logging secrets or sensitive payment credentials.
- Support safe retries.
- Provide operational visibility for failed processing.

Webhook processing must be transactionally safe and must not grant entitlements based solely on an unverified notification.

## 14.5 Idempotency

Payment and billing operations must be safe to retry.

Examples include:

- Creating a renewal invoice.
- Initiating a payment.
- Processing a payment-success event.
- Processing a refund event.
- Updating subscription status.
- Granting module entitlements.

Use database constraints, unique event identifiers, idempotency keys, and transactional state transitions as appropriate.

The same verified event must not cause duplicate invoices, duplicate payments, or repeated entitlement grants.

# 15. Entitlements and Module Access

## 15.1 Commercial Entitlements

The subscription system determines which commercial entitlements a tenant is eligible to receive.

The entitlement engine determines whether a user may access a particular module or operation.

These are related but distinct responsibilities.

## 15.2 Entitlement Inputs

Entitlement decisions may depend on:

- Tenant status.
- Subscription status.
- Subscription item status.
- Module availability.
- Module dependencies.
- Trial state.
- Payment state.
- Effective dates.
- Approved administrative overrides.
- User permissions.

The exact entitlement rules must be documented in `docs/01-architecture/ENTITLEMENT_ENGINE.md`.

## 15.3 Server-Side Enforcement

Module access must be enforced in the backend.

Hiding navigation links is not sufficient.

The system must validate entitlements in:

- Django views.
- DRF API endpoints.
- Service-layer operations.
- Background tasks where tenant and subscription state are relevant.
- File downloads and exports.
- Other access paths that expose protected module functionality.

A user must not gain access by calling an endpoint directly.

## 15.4 Administrative Overrides

Any manual commercial override must require explicit authorization.

An override must record:

- Tenant.
- Affected module or entitlement.
- Previous state.
- New state.
- Reason.
- Authorized actor.
- Effective date.
- Expiry date, if applicable.
- Timestamp.

Overrides must not silently change the underlying subscription invoice or payment history.

# 16. Commercial Administration

Authorized platform administrators need controlled interfaces to manage commercial configuration.

## 16.1 Administrative Capabilities

Subject to role permissions, the administration area may support:

- Module availability.
- Price configuration.
- Price publication and retirement.
- Billing intervals.
- Plan configuration.
- Module dependencies.
- Trial policies.
- Promotion management.
- Subscription inspection.
- Invoice inspection.
- Payment reconciliation.
- Refund processing.
- Approved manual adjustments.
- Subscription suspension and reactivation.
- Commercial audit history.

## 16.2 Price Change Workflow

A price change should follow this workflow:

1. Authorized administrator creates a proposed price.
2. The system validates the pricing configuration.
3. The administrator reviews the effective date and scope.
4. The price is approved and published.
5. New purchases use the applicable published price.
6. Existing subscriptions follow the approved repricing policy.
7. The system records the change.
8. The new configuration becomes visible to authorized staff.

Where required, price changes for existing customers must include customer communication and any necessary consent before taking effect.

## 16.3 Separation of Duties

Sensitive commercial operations should use role-based permissions.

For example, the permission to publish a price should not automatically grant permission to issue refunds or alter payment records.

The final permission matrix belongs in the authentication and authorization documentation.

# 17. Notifications

The commercial system should support configurable notifications for relevant subscription events.

Potential notifications include:

- Trial started.
- Trial approaching expiry.
- Trial expired.
- Subscription activated.
- Module added.
- Module scheduled for removal.
- Renewal approaching.
- Invoice issued.
- Payment succeeded.
- Payment failed.
- Invoice overdue.
- Grace period approaching expiry.
- Subscription suspended.
- Cancellation scheduled.
- Subscription cancelled.
- Subscription reactivated.

Notification channels may include email and in-app notifications.

SMS or messaging integrations should be added only if approved.

Notifications must not expose sensitive financial information to unauthorized recipients.

The system should track delivery attempts and support retrying transient failures without duplicating the underlying commercial operation.

# 18. Commercial Reporting

The platform should provide authorized administrators with commercial reporting.

Potential reports include:

- Active subscriptions.
- Subscriptions by status.
- Recurring subscription revenue.
- Revenue by module.
- Revenue by billing interval.
- New subscriptions.
- Renewals.
- Cancellations.
- Failed payments.
- Outstanding subscription invoices.
- Refunds and credits.
- Trial-to-paid conversion.
- Module adoption.
- Subscription expansion and contraction.

## 18.1 Metric Definitions

Revenue metrics must have documented definitions.

For example, Monthly Recurring Revenue (MRR) should be calculated from eligible recurring subscription commitments using a consistent policy.

The calculation must specify how it treats:

- Annual subscriptions.
- Discounts.
- Paused or suspended subscriptions.
- Trials.
- Non-recurring implementation fees.
- Refunds and credits.
- Currency conversion.
- Failed or overdue payments.

MRR is not automatically equal to cash received during a calendar month.

Recognized accounting revenue, invoiced revenue, booked recurring revenue, and collected cash are different measures.

The reporting system must label these metrics accurately and avoid presenting one as another.

# 19. Data Integrity and Auditability

Commercial data affects revenue, customer access, and financial records. It must receive stronger controls than ordinary configuration data.

The system must ensure that:

- Issued subscription invoices retain their historical contents.
- Payment records are traceable.
- Refunds reference the appropriate payment or invoice.
- Price changes preserve historical pricing.
- Subscription changes retain effective dates.
- Duplicate provider events are handled safely.
- Manual adjustments are authorized and auditable.
- Commercial events are associated with the correct tenant.
- Tenant users cannot access another tenant's commercial records.
- Platform administrators are subject to explicit permissions.
- Financial calculations use deterministic decimal arithmetic.
- Background jobs are safe to retry.

Database constraints should enforce critical invariants wherever possible.

Application-level validation alone is insufficient for invariants that can be protected through appropriate database constraints.

# 20. Security and Privacy

The commercial domain may contain customer identity, billing history, payment references, and business contact information.

The implementation must:

- Enforce tenant isolation.
- Apply role-based access control.
- Protect payment-provider credentials.
- Use secure secret management.
- Avoid storing prohibited payment-card data.
- Redact sensitive values from logs.
- Validate webhook authenticity.
- Record sensitive administrative operations.
- Limit access to billing information.
- Protect exported invoices and reports.
- Follow the approved retention and deletion policy.

The platform must use the payment provider's recommended secure payment collection flow.

The application must not store full payment-card numbers or card verification codes unless a formally approved, compliant architecture explicitly permits a specific form of handling. The default design should avoid collecting or storing such data.

# 21. Operational Requirements

The commercial system must support:

- Reliable scheduled billing jobs.
- Safe retries.
- Failed-job visibility.
- Payment-provider outage handling.
- Reconciliation of uncertain payment states.
- Monitoring of renewal failures.
- Monitoring of webhook failures.
- Recovery after interrupted background processing.
- Backup and restoration of subscription records.
- Controlled replay of eligible events.
- Documented manual reconciliation procedures.

A payment-provider outage must not cause subscription invoices or payment history to be lost.

When a payment outcome is uncertain, the system should reconcile against authoritative provider information before initiating another charge.

# 22. Initial Release Scope

The following table defines a proposed minimum commercial implementation.

| Capability | Initial Priority | Notes |
|---|---|---|
| Configurable module catalogue | Required | Must support commercial availability states |
| Configurable module prices | Required | Must support historical prices |
| Subscription creation | Required | Must validate module dependencies |
| Subscription status management | Required | Statuses must be explicit |
| Monthly billing | Proposed | Confirm before implementation |
| Annual billing | Proposed | Confirm before implementation |
| Subscription invoices | Required | Subject to approved legal and tax requirements |
| Payment-provider integration | Required for automated paid checkout | Provider selection remains open |
| Payment webhook handling | Required when provider webhooks are used | Must be authenticated and idempotent |
| Manual payment reconciliation | Required if manual payments are accepted | Must be authorized and auditable |
| Module entitlements | Required | Server-side enforcement |
| Upgrade workflow | Required | Exact proration policy remains open |
| Downgrade workflow | Required | Must preserve customer data |
| Cancellation | Required | Effective-date policy remains open |
| Trial support | Optional | Implement only if approved |
| Promotions | Optional | Implement only if approved |
| Usage-based billing | Not required initially | Reassess after demand validation |
| Per-user billing | Not required initially | Reassess after demand validation |
| Automated refunds | Optional | Requires approved provider and financial rules |
| Premium support tiers | Not required initially | Reassess after commercial validation |
| Advanced revenue analytics | Later phase | Basic operational reports may be required earlier |

The product owner must approve the actual initial scope before development begins.

# 23. Acceptance Criteria

The commercial model implementation is acceptable only when the following criteria are satisfied.

## 23.1 Pricing

- Prices are configurable through authorized administrative functionality.
- The system uses the correct price for the applicable effective date.
- Historical invoices preserve their original pricing.
- Price changes do not silently rewrite active subscriptions.
- Monetary calculations use decimal arithmetic.
- Currency and rounding rules are documented and tested.

## 23.2 Subscription Lifecycle

- Subscription transitions follow documented rules.
- Unauthorized users cannot create or modify subscriptions.
- Module dependencies are validated server-side.
- Subscription upgrades and downgrades preserve historical records.
- Cancellation follows the approved effective-date policy.
- Trial behavior follows the approved trial policy, if enabled.
- Subscription state changes are auditable.

## 23.3 Billing

- Renewal processing creates the correct invoice.
- Duplicate job execution does not create duplicate invoices.
- Failed payment attempts are recorded.
- Invoice balances reflect verified payment transactions.
- Payment failures do not delete subscription records.
- Subscription invoices are distinct from tenant-generated customer invoices.
- Issued invoices cannot be silently overwritten.

## 23.4 Payment Integration

- Payment requests use server-calculated amounts.
- Provider events are authenticated.
- Duplicate webhooks do not duplicate financial effects.
- Invalid provider events are rejected or safely quarantined.
- Out-of-order events are handled according to documented state-transition rules.
- Uncertain payment states can be reconciled.
- Secrets and sensitive payment data are not exposed in logs.

## 23.5 Entitlements

- Only entitled tenants can access paid module functionality.
- Backend endpoints enforce module access.
- Subscription suspension applies the approved access policy.
- Module removal does not delete business data.
- Administrative overrides require authorization and an audit trail.

## 23.6 Commercial Administration

- Unauthorized users cannot publish prices or issue refunds.
- Price changes retain effective dates and historical records.
- Commercial adjustments record their reason and authorizing actor.
- Customer-facing prices match the server's approved pricing configuration.

# 24. Testing Requirements

The implementation must include automated tests for at least the following scenarios.

### Pricing Tests

- Valid module price calculation.
- Missing price configuration.
- Retired module.
- Future-dated price.
- Price change during an active subscription.
- Monthly and annual pricing.
- Discount eligibility.
- Tax calculation and rounding.
- Currency mismatch.
- Dependency pricing.
- Concurrent subscription changes.

### Subscription Tests

- Subscription creation.
- Activation after verified payment.
- Trial activation and expiry, if enabled.
- Module addition.
- Module removal.
- Dependency violation.
- Upgrade and downgrade.
- Cancellation scheduling.
- Reactivation.
- Suspension and restoration.
- Unauthorized state changes.

### Billing Tests

- Initial invoice creation.
- Renewal invoice creation.
- Duplicate renewal execution.
- Failed payment.
- Successful payment.
- Partial payment, if supported.
- Refund and credit handling, if supported.
- Invoice immutability.
- Concurrent invoice numbering.
- Recovery after interrupted billing jobs.

### Payment Integration Tests

- Valid webhook.
- Invalid signature.
- Duplicate webhook.
- Unknown provider event.
- Out-of-order events.
- Timeout while checking payment status.
- Provider outage.
- Retry after transient failure.
- Payment marked successful by provider after an initial timeout.
- Reconciliation of uncertain payments.

### Tenant Isolation Tests

- Customer cannot view another tenant's subscription.
- Customer cannot access another tenant's invoice.
- Customer cannot change another tenant's subscription.
- Tenant administrator cannot change platform-wide pricing.
- A user cannot grant paid entitlements through a direct API request.

Tests must use a provider sandbox or mocked provider interface. Automated tests must not trigger real financial transactions.

# 25. Decisions Pending

The following decisions require explicit approval.

| Decision ID | Decision | Required Input |
|---|---|---|
| CM-DEC-001 | Whether to charge a base subscription fee | Customer research and pricing strategy |
| CM-DEC-002 | Initial module prices | Competitor research, costs, willingness to pay |
| CM-DEC-003 | Monthly billing availability | Commercial approval |
| CM-DEC-004 | Annual billing and discount policy | Commercial approval |
| CM-DEC-005 | Trial availability and duration | Acquisition strategy |
| CM-DEC-006 | Initial payment provider | Provider assessment and onboarding eligibility |
| CM-DEC-007 | Supported payment methods | Provider capabilities and customer demand |
| CM-DEC-008 | Proration policy | Billing and accounting requirements |
| CM-DEC-009 | Downgrade effective-date policy | Commercial approval |
| CM-DEC-010 | Cancellation policy | Contractual and commercial requirements |
| CM-DEC-011 | Failed-payment retry schedule | Provider capabilities and risk policy |
| CM-DEC-012 | Grace period and suspension policy | Customer experience and risk policy |
| CM-DEC-013 | Discount and promotion support | Commercial approval |
| CM-DEC-014 | Manual payment support | Operational requirements |
| CM-DEC-015 | Refund and credit policy | Commercial and accounting review |
| CM-DEC-016 | SaaS subscription tax treatment | Qualified tax review |
| CM-DEC-017 | Customer invoice numbering requirements | Applicable legal requirements |
| CM-DEC-018 | Customer notification channels | Operational requirements |
| CM-DEC-019 | Per-user pricing | Customer research |
| CM-DEC-020 | Usage-based pricing | Customer research and metering cost |
| CM-DEC-021 | Payment retry and recovery procedures | Operational and technical assessment |
| CM-DEC-022 | Data access after cancellation | Retention policy and contractual requirements |

Each decision must be recorded in `docs/07-project-management/DECISIONS_PENDING.md` until resolved.

# 26. Related Documentation

This document must remain consistent with:

- `docs/00-product/MASTER_PRODUCT_SPECIFICATION.md`
- `docs/00-product/PRODUCT_REQUIREMENTS.md`
- `docs/00-product/TARGET_MARKET.md`
- `docs/00-product/MODULE_CATALOGUE.md`
- `docs/00-product/DEVELOPMENT_ROADMAP.md`
- `docs/01-architecture/DATABASE_DESIGN.md`
- `docs/01-architecture/MULTI_TENANCY.md`
- `docs/01-architecture/AUTHENTICATION_AND_PERMISSIONS.md`
- `docs/01-architecture/MODULE_DEPENDENCIES.md`
- `docs/01-architecture/ENTITLEMENT_ENGINE.md`
- `docs/01-architecture/EVENT_AND_TASK_PROCESSING.md`
- `docs/06-deployment/ENVIRONMENT_VARIABLES.md`
- `docs/06-deployment/OPERATIONS_RUNBOOK.md`

When commercial behavior changes, the product requirements, architecture, test plan, and implementation must be updated together.

# 27. Definition of Completion

This document is ready for implementation planning when:

- The proposed commercial model has been reviewed.
- Initial pricing and packaging decisions have owners.
- The initial billing intervals have been selected.
- The payment-provider selection process has been defined.
- Trial, cancellation, and failed-payment policies have been decided.
- Module dependency and entitlement responsibilities are documented.
- Subscription invoicing requirements have been reviewed.
- Tax-related decisions have been assigned for qualified review.
- Initial release scope has been approved.
- Acceptance criteria and testing requirements have been accepted.

Completion of this document does not mean that the commercial model is ready for production. Production billing must also pass implementation, integration, financial-integrity, security, operational, and release validation.

---

**End of Document**
