# UAE ERP SaaS — Target Market Definition

| Document Attribute | Value |
|---|---|
| Document ID | TM-001 |
| Version | 1.0 |
| Status | Initial Draft — Pending Approval |
| Product | UAE ERP SaaS |
| Document Type | Product Strategy and Target Market Definition |
| Parent Document | `docs/00-product/MASTER_PRODUCT_SPECIFICATION.md` |
| Related Documents | `PRODUCT_REQUIREMENTS.md`, `COMMERCIAL_MODEL.md`, `MODULE_CATALOGUE.md`, `DEVELOPMENT_ROADMAP.md` |
| Primary Market | United Arab Emirates |
| Intended Audience | Product Owner, Business Analyst, Architect, Development Team, Marketing and Sales Teams |

---

# 1. Purpose

This document defines the initial target market and commercial positioning for a modular, multi-tenant Enterprise Resource Planning (ERP) SaaS platform intended for businesses operating in the United Arab Emirates (UAE).

It establishes:

- The geographical market and initial customer segments.
- The proposed ideal customer profiles.
- The business problems the product intends to solve.
- The initial product positioning.
- The commercial model and customer purchasing assumptions.
- The UAE-specific business requirements that influence product design.
- The initial go-to-market strategy.
- The market validation activities required before making significant commercial or technical commitments.
- The criteria for determining the first commercially viable release.

This document provides product direction. It does not replace legal, tax, accounting, payroll, security, or regulatory requirements.

All assumptions must be validated before being treated as confirmed product requirements.

# 2. Market Definition

## 2.1 Geographic Scope

The initial target market is the United Arab Emirates.

The platform should be designed to support businesses operating in the UAE, including businesses based in:

- Dubai
- Abu Dhabi
- Sharjah
- Ajman
- Ras Al Khaimah
- Fujairah
- Umm Al Quwain

The initial commercial focus should be determined by customer discovery, the availability of implementation and support resources, the competitive landscape, and the requirements of the selected customer segments.

The product should not assume that every emirate, industry, or customer segment must be targeted at launch.

## 2.2 Initial Market Strategy

The initial strategy is to develop a configurable ERP platform for small and medium-sized businesses that need integrated business management capabilities without purchasing an unnecessarily large ERP implementation.

The product should offer a modular subscription model in which customers can select the modules relevant to their operations.

Potential modules include:

- CRM
- Sales
- Invoicing
- Accounting
- VAT management
- UAE e-invoicing integration
- Procurement
- Inventory
- HRMS
- Payroll
- Project management
- Expense management
- Fixed asset management
- Banking and financial reconciliation
- Reporting and integrations

The presence of a module in the product roadmap does not mean it is available for commercial sale. Only implemented, tested, supported, and explicitly approved modules may be presented as purchasable products.

## 2.3 Market Positioning Hypothesis

**Proposed positioning:**

A modular ERP platform for UAE businesses that want to manage their core business operations through one configurable system, with the ability to start with the capabilities they need and expand as their requirements grow.

This positioning must be validated through customer interviews and competitor research.

The platform should avoid positioning itself as the cheapest ERP in the market unless competitive research and cost analysis substantiate that claim.

# 3. Target Customer Segments

## 3.1 Primary Segment: Small and Medium-Sized Businesses

### Profile

Businesses that need to coordinate several operational functions but may not require a highly customized enterprise ERP implementation.

Potential characteristics include:

- A growing number of customers and suppliers.
- Multiple employees responsible for sales, operations, finance, or administration.
- Reliance on spreadsheets or disconnected applications.
- A need for consistent invoicing and financial records.
- Increasing requirements for inventory or procurement control.
- A preference for predictable recurring software costs.
- A need to introduce additional capabilities as the business grows.

These characteristics are hypotheses to validate, not mandatory customer eligibility rules.

### Problems to Solve

- Duplicate data entry across applications.
- Inconsistent customer and supplier records.
- Limited visibility into receivables and payables.
- Manual sales and purchase workflows.
- Poor coordination between inventory and sales.
- Delayed or inconsistent management reports.
- Difficulty controlling access to financial and operational information.
- High cost or complexity associated with adopting a comprehensive ERP system.

### Relevant Product Capabilities

Depending on the validated segment, the initial package may include:

- CRM
- Sales and invoicing
- Accounting and VAT
- Procurement and inventory
- Basic reporting
- User and role management

The exact module combination must be selected using market validation rather than assumed in advance.

## 3.2 Secondary Segment: Trading and Distribution Businesses

### Profile

Businesses that buy, store, distribute, and sell physical products.

Potential examples include wholesalers, importers, distributors, and general trading businesses.

### Problems to Solve

- Inaccurate stock availability.
- Inconsistent purchase and sales records.
- Difficulty tracking supplier and customer transactions.
- Limited control over stock movements between locations.
- Inadequate visibility into inventory costs and margins.
- Manual purchase-order and goods-receipt processes.
- Difficulty reconciling inventory movements with financial records.

### Relevant Product Capabilities

- Customer and supplier management.
- Sales orders and invoices.
- Purchase orders.
- Goods receipt and supplier bills.
- Inventory movements.
- Multiple warehouse or store locations.
- Stock adjustments and stock counts.
- Inventory valuation.
- Receivables and payables.
- Financial reporting.

### Validation Requirement

Inventory valuation, landed costs, multiple units of measure, lot or serial tracking, and multi-warehouse workflows can significantly increase implementation complexity.

These features must be prioritized based on the needs of the first target customers.

Do not advertise support for a complex inventory workflow until its behavior and accounting implications have been implemented and tested.

## 3.3 Secondary Segment: Professional and Business Services

### Profile

Service-oriented businesses that manage customer relationships, proposals, projects, expenses, and invoices.

Potential examples include:

- IT and software service providers.
- Marketing agencies.
- Business consultancies.
- Technical service companies.
- Professional service providers.

### Problems to Solve

- Poor visibility into sales opportunities.
- Inconsistent quotation and invoice preparation.
- Difficulty tracking project costs.
- Manual expense reporting.
- Limited visibility into outstanding customer payments.
- Disconnected CRM, project, and accounting information.

### Relevant Product Capabilities

- CRM.
- Quotations and sales orders.
- Customer invoicing.
- Expense management.
- Project tracking.
- Time or activity tracking, if validated.
- Receivables management.
- Accounting and VAT.
- Management reports.

This segment may be suitable for an early release if customer discovery confirms that its essential workflows can be delivered without the complexity of advanced inventory or payroll.

## 3.4 Secondary Segment: Small Businesses with HR and Payroll Needs

### Profile

Businesses seeking a central system for employee information, attendance-related records, leave management, and payroll administration.

### Problems to Solve

- Employee records spread across spreadsheets.
- Manual leave and attendance administration.
- Repeated payroll calculations.
- Inconsistent employee-document management.
- Difficulty maintaining payroll records.
- Limited access controls for confidential employee data.

### Relevant Product Capabilities

- Employee records.
- Departments and designations.
- Leave management.
- Attendance integration or attendance management.
- Payroll calculations.
- Payroll records and reports.
- Employee document management.
- Role-based access control.

### Regulatory Caution

UAE payroll requirements may depend on the employer's jurisdiction, employee category, applicable labour rules, and other circumstances.

Requirements involving the Wage Protection System (WPS), end-of-service benefits, employment rules, and free-zone arrangements must be researched and validated before implementation.

Do not represent the HRMS or payroll modules as legally compliant until the applicable requirements have been confirmed and the implementation independently tested.

## 3.5 Enterprise Customers

Large enterprises may require advanced functionality such as:

- Complex approval hierarchies.
- Intercompany accounting.
- Consolidated reporting.
- Extensive audit trails.
- Advanced segregation of duties.
- Custom integrations.
- High availability and disaster recovery.
- Dedicated infrastructure.
- Formal security reviews.
- Service-level agreements.
- Complex data migration.
- Specialized compliance requirements.

Enterprise customers should not be the default target for the first release unless discovery identifies a commercially attractive opportunity that the product can support responsibly.

Enterprise readiness should be evaluated separately from basic SaaS functionality.

# 4. Ideal Customer Profiles

The following profiles are starting hypotheses for customer interviews.

They must not be treated as verified market segments or as statistically representative of the UAE business population.

## ICP-01: Growing Trading Company

| Attribute | Initial Hypothesis |
|---|---|
| Business Type | Trading, wholesale, distribution |
| Company Size | Small or medium-sized |
| Primary Need | Integrated sales, purchasing, inventory, and finance |
| Likely Buyer | Owner, General Manager, Finance Manager, Operations Manager |
| Current Alternative | Spreadsheets, accounting software, disconnected applications, or an existing ERP |
| Initial Module Interest | Sales, invoicing, procurement, inventory, accounting |
| Purchase Motivation | Better stock visibility, reduced manual work, improved financial control |
| Main Objection | Migration effort, feature completeness, cost, staff adoption |
| Validation Priority | High |

### Discovery Questions

1. How are purchases, sales, and inventory currently recorded?
2. How many storage locations are managed?
3. How are stock adjustments and physical stock counts handled?
4. How is inventory valuation calculated?
5. Which accounting system is currently used?
6. Which operational tasks require repeated manual data entry?
7. What would justify changing the current system?
8. Which integrations are essential?
9. What is the current annual software and support expenditure?
10. Who approves the purchase of a new ERP system?

## ICP-02: Professional Services Company

| Attribute | Initial Hypothesis |
|---|---|
| Business Type | IT services, consulting, marketing, technical services |
| Company Size | Small or medium-sized |
| Primary Need | CRM, project visibility, invoicing, expense management |
| Likely Buyer | Owner, Managing Director, Finance Manager |
| Current Alternative | Spreadsheets, accounting software, CRM tools, project applications |
| Initial Module Interest | CRM, sales, invoicing, accounting, projects, expenses |
| Purchase Motivation | Centralized customer and financial information |
| Main Objection | Existing tools may already be sufficient |
| Validation Priority | High |

### Discovery Questions

1. How are leads, opportunities, quotations, and customer records managed?
2. How are project budgets and expenses tracked?
3. How are customer invoices generated and followed up?
4. Which financial reports are needed every month?
5. Which applications currently hold customer and financial data?
6. What information must be shared between sales, delivery, and finance?
7. Which workflows consume the most administrative time?
8. What would make an integrated system more valuable than the current applications?

## ICP-03: Small Business with Finance and HR Requirements

| Attribute | Initial Hypothesis |
|---|---|
| Business Type | General small business |
| Primary Need | Finance, invoicing, employee administration |
| Likely Buyer | Owner, Finance Manager, HR Manager |
| Current Alternative | Spreadsheets, accounting software, manual payroll processes |
| Initial Module Interest | Invoicing, accounting, VAT, HRMS, payroll |
| Purchase Motivation | Reduced administrative overhead and better control |
| Main Objection | Trust, data migration, regulatory coverage, implementation effort |
| Validation Priority | Medium to High |

### Discovery Questions

1. Which accounting and payroll applications are currently used?
2. Who calculates and approves payroll?
3. Which employee records require restricted access?
4. Which tax, payroll, and employment reports are needed?
5. Are any payroll or attendance systems already integrated?
6. What is the cost of the current process?
7. Which compliance requirements are mandatory before adopting a new system?

# 5. Customer Personas and Buying Roles

The product and marketing strategy should consider the different people involved in selecting and using an ERP.

## 5.1 Business Owner or Managing Director

**Primary concerns:**

- Business visibility.
- Cost predictability.
- Ease of use.
- Return on investment.
- Operational control.
- Ability to add functionality as the business grows.

**Product implications:**

- Clear dashboards.
- Understandable pricing.
- Simple onboarding.
- Consolidated reports.
- Low-friction module activation.

## 5.2 Finance Manager or Accountant

**Primary concerns:**

- Accounting accuracy.
- Invoice integrity.
- VAT treatment.
- Receivables and payables.
- Bank reconciliation.
- Audit trails.
- Financial reporting.

**Product implications:**

- Consistent financial records.
- Traceable transactions.
- Configurable accounting controls.
- Period locking.
- Reconciliation tools.
- Permission-controlled financial operations.

Finance-related workflows require strong correctness guarantees. A visually complete interface is not sufficient evidence of financial correctness.

## 5.3 Operations or Inventory Manager

**Primary concerns:**

- Stock availability.
- Purchase planning.
- Supplier performance.
- Warehouse operations.
- Stock adjustments.
- Order fulfillment.

**Product implications:**

- Fast inventory search.
- Clear stock movement history.
- Controlled stock adjustments.
- Reliable reservation and availability calculations.
- Traceable goods receipts and deliveries.

## 5.4 HR or Payroll Administrator

**Primary concerns:**

- Employee information.
- Payroll accuracy.
- Confidentiality.
- Leave and attendance records.
- Employment-related reporting.

**Product implications:**

- Restricted access to employee data.
- Payroll calculation validation.
- Approval workflows.
- Traceable changes.
- Secure employee document handling.

## 5.5 External Accountant or Implementation Partner

An external accountant, consultant, or implementation partner may influence purchasing decisions.

Potential requirements include:

- Secure delegated access.
- Read-only financial access.
- Exportable accounting records.
- Controlled access to multiple client organizations.
- Clear audit logs.
- Supportable configuration workflows.

These capabilities should be prioritized only after their demand and security implications are validated.

# 6. Customer Problems and Value Proposition

## 6.1 Core Value Proposition

The platform should aim to provide:

1. **Modular adoption:** Customers can subscribe to the modules they need.
2. **Integrated information:** Authorized modules can use consistent customer, supplier, product, and financial records.
3. **Operational visibility:** Users can access timely information relevant to their roles.
4. **Controlled access:** Permissions determine which users can view and perform specific operations.
5. **Scalable functionality:** Customers can add supported modules as their needs evolve.
6. **UAE-oriented workflows:** Localization and integrations are prioritized for the confirmed needs of UAE businesses.
7. **Predictable commercial terms:** Customers can understand the cost of their selected modules and associated services.

These are product objectives, not claims that the platform already delivers them.

## 6.2 Measurable Value Hypotheses

The product team should test whether customers value improvements such as:

- Less duplicate data entry.
- Faster invoice preparation.
- Improved visibility into outstanding receivables.
- Reduced time required to prepare management reports.
- More accurate stock information.
- Easier retrieval of transaction history.
- Fewer errors caused by disconnected systems.

Baseline measurements should be collected from pilot customers wherever practical.

Do not publish quantified savings, productivity improvements, or return-on-investment claims without evidence.

# 7. Commercial Model and Customer Expectations

The commercial model is modular subscription SaaS.

Customers select available modules and pay according to the approved pricing model.

## 7.1 Subscription Principles

The commercial architecture must support:

- Configurable module pricing.
- Monthly and annual billing options, if approved.
- Module dependencies.
- Module availability by subscription plan.
- Trial or demonstration access, if approved.
- Subscription upgrades and downgrades.
- Renewal and cancellation workflows.
- Payment status tracking.
- Grace periods and suspension policies.
- Invoice generation for the SaaS subscription itself.
- Subscription history and auditability.

Commercial rules must be stored as configurable data rather than embedded throughout application code.

## 7.2 Separate SaaS Billing from ERP Invoicing

Two distinct billing domains must be maintained.

### Platform Subscription Billing

This concerns what the SaaS provider charges its customers for:

- Module subscriptions.
- Subscription plans.
- Recurring charges.
- Approved add-ons.
- Discounts and promotions.
- Subscription renewals.
- Subscription-related taxes.

### Customer ERP Invoicing

This concerns the transactions that a tenant records between its own business and its customers.

Examples include:

- Sales invoices.
- Credit notes.
- Customer payments.
- Receivables.
- VAT calculations.
- E-invoicing provider submissions.

The two domains must not share transaction logic merely because both generate invoices.

They require separate business rules, permissions, numbering policies, accounting treatment, and reporting.

## 7.3 Pricing Validation

No final price should be assumed until the following are researched:

- Competitor pricing and packaging.
- Customer willingness to pay.
- Implementation and onboarding costs.
- Hosting and support costs.
- Third-party provider fees.
- E-invoicing integration charges.
- Payment processing charges.
- Expected support workload.
- Gross margin targets.
- Applicable taxes on SaaS subscriptions.

Pricing decisions belong in `COMMERCIAL_MODEL.md`.

# 8. UAE-Specific Product Considerations

UAE-specific requirements are a key potential differentiator, but they must be implemented from verified requirements rather than assumptions.

## 8.1 Currency and Financial Precision

The initial market design should support AED as the default tenant currency.

The architecture should allow additional currencies where needed.

Requirements to validate include:

- Currency precision and rounding.
- Exchange-rate source and update frequency.
- Transaction currency versus base currency.
- Realized and unrealized foreign exchange differences.
- Foreign-currency customer and supplier balances.
- Currency-specific reports.
- Historical exchange-rate retention.

Money values must use appropriate decimal arithmetic. Binary floating-point arithmetic must not be used for authoritative financial calculations.

Currency and rounding behavior must be specified and tested.

## 8.2 VAT

The product must support a configurable tax model suitable for validated UAE VAT workflows.

Requirements to validate include:

- Tax registration information.
- Tax codes and rates.
- Tax-inclusive and tax-exclusive pricing.
- Tax treatment of line items.
- Input and output VAT.
- Credit notes.
- Tax adjustments.
- VAT reporting periods.
- Tax reports and supporting transaction details.
- Treatment of exempt, zero-rated, and out-of-scope transactions where applicable.
- Data exports required for accounting and tax review.

The system must not assume that all transactions use a single tax rate or that every business has the same VAT obligations.

The implementation must be reviewed against applicable official requirements and qualified tax advice.

## 8.3 UAE E-Invoicing

The platform roadmap includes integration with an appropriate UAE e-invoicing service provider.

The selected provider and applicable technical requirements must be confirmed before implementation commitments are finalized.

Validation must cover:

- Applicable regulatory scope and effective dates.
- Whether the customer falls within the relevant requirements.
- Provider accreditation or authorization status, where applicable.
- Required invoice data and formats.
- Submission and response workflows.
- Validation failures and retry handling.
- Credit notes and correction workflows.
- Unique identifiers and references.
- Audit and retention requirements.
- API authentication and credentials.
- Provider charges and support arrangements.
- Sandbox and production access.
- Responsibility boundaries between the ERP provider and the e-invoicing provider.

The system should isolate provider-specific behavior behind an integration boundary so that provider changes do not require rewriting the invoicing domain.

**Marketing restriction:** Do not advertise the platform as UAE e-invoicing compliant until the applicable requirements, selected provider, integration behavior, and necessary validation have been confirmed.

## 8.4 Payroll and Employment Requirements

Before marketing payroll functionality, validate the applicable requirements for each supported employer and employee category.

Areas for investigation include:

- Salary components and deductions.
- Payroll periods and approval workflows.
- Leave and attendance inputs.
- End-of-service benefit calculations.
- WPS-related file generation or integration, where applicable.
- Employment-related reports.
- Payroll data retention.
- Confidential employee information.
- Differences that may apply to free-zone employers or other categories.

The product must not assume one payroll configuration is legally suitable for every UAE employer.

## 8.5 Arabic and English Localization

The product should be designed so that localization can be introduced without restructuring its core data model.

Requirements to consider include:

- English interface.
- Arabic interface.
- Right-to-left layout support.
- Unicode-safe text handling.
- Localized dates and number formatting.
- Configurable invoice language.
- Arabic and English customer and supplier information where needed.
- PDF generation that supports Arabic shaping and right-to-left text.
- Search and sorting behavior for Arabic text.
- Consistent localization of validation messages and reports.

The initial release language must be selected after market validation.

Arabic support must be tested throughout the interface and document-generation pipeline. Translating menu labels alone is not sufficient.

## 8.6 UAE Business Configuration

The tenant configuration should be capable of storing relevant business details, including:

- Legal business name.
- Trade or registration information, where required.
- Registered address.
- Contact information.
- Tax registration details, where applicable.
- Default currency.
- Time zone.
- Fiscal-year settings.
- Invoice numbering configuration.
- Logo and document branding.
- Enabled modules.
- Accounting and tax configuration.

Sensitive information must be protected through appropriate access controls and secure storage.

## 8.7 Data Hosting and Privacy

Hosting location, cross-border data transfer, data protection, retention, and deletion requirements must be reviewed against the applicable legal framework and customer contracts.

Do not assume that all UAE businesses are subject to identical hosting or data-residency obligations.

The infrastructure design should support a documented hosting decision and allow the deployment architecture to evolve if validated requirements demand it.

# 9. Competitive Landscape and Alternatives

The product competes not only with other ERP systems but also with combinations of existing tools.

The research process must examine at least the following categories.

## 9.1 Established ERP Platforms

Investigate the suitability, pricing, implementation effort, localization, and support model of established ERP products.

Research candidates may include:

- Odoo.
- Microsoft Dynamics 365 Business Central.
- SAP Business One.
- Oracle NetSuite.

These are research candidates, not a final competitor ranking or a claim that all are direct competitors for every target segment.

Official product information, local implementation partners, and customer interviews should be used to establish the actual competitive position.

## 9.2 Accounting and Invoicing Applications

Investigate accounting-focused tools used by UAE businesses, including their invoicing, VAT, banking, reporting, and integration capabilities.

The key question is whether customers need a broader ERP platform or whether their current accounting software already meets their requirements.

## 9.3 Spreadsheets and Disconnected Applications

Spreadsheets and disconnected applications are important alternatives because they may have:

- Low direct software costs.
- Familiar user interfaces.
- Flexible workflows.
- Minimal implementation requirements.

The product must demonstrate sufficient value to justify migration, training, subscription fees, and process changes.

## 9.4 Competitor Research Matrix

Maintain a research matrix with the following fields:

| Field | Purpose |
|---|---|
| Vendor | Identify the provider |
| Product | Identify the specific product or edition |
| Target segment | Understand intended customers |
| Core modules | Compare functional coverage |
| UAE localization | Verify available localization |
| VAT capabilities | Validate relevant tax workflows |
| E-invoicing support | Record verified capabilities and provider relationships |
| Arabic support | Confirm interface and document capabilities |
| Payroll support | Record supported scenarios and limitations |
| Pricing | Record verified pricing and billing basis |
| Implementation fees | Capture setup and migration costs |
| Hosting options | Identify relevant deployment choices |
| Integration ecosystem | Understand supported integrations |
| Support model | Compare availability and service arrangements |
| Limitations | Document credible gaps relevant to target customers |
| Source and date | Preserve evidence and freshness |

Do not publish unsupported competitor comparisons or claim that the proposed product is superior without evidence.

# 10. Market Validation Plan

The target market must be validated before the product roadmap is treated as commercially final.

## 10.1 Customer Interviews

Conduct an initial discovery program with a proposed target of 15–25 businesses.

This is a research target, not a statistically representative sample.

Include a mix of:

- Trading and distribution companies.
- Professional services companies.
- Small businesses with finance and HR needs.
- Accountants or implementation partners who influence purchasing decisions.

Interview participants should be selected based on actual purchasing authority, operational involvement, and relevance to the proposed segments.

## 10.2 Interview Topics

Each interview should investigate:

1. Business model and operating structure.
2. Current software and manual processes.
3. The most expensive or disruptive operational problems.
4. Current accounting and invoicing workflows.
5. Inventory and procurement requirements, where relevant.
6. HR and payroll requirements, where relevant.
7. Existing integrations and migration constraints.
8. Regulatory and reporting requirements.
9. Current software expenditure.
10. Decision-making authority and purchasing process.
11. Required implementation and support.
12. Willingness to pay for a modular solution.
13. Reasons for rejecting a new ERP.
14. Requirements that would prevent adoption.

Avoid relying solely on questions such as "Would you use this product?"

Seek evidence of actual problems, current spending, purchasing behavior, and willingness to participate in a pilot or pay for a solution.

## 10.3 Validation Evidence

Record the following for each interview:

- Interview date.
- Business segment.
- Participant role.
- Existing systems.
- Main operational problems.
- Frequency and impact of each problem.
- Current workaround.
- Estimated cost or time impact, if available.
- Required functionality.
- Essential integrations.
- Buying authority.
- Budget information, where voluntarily disclosed.
- Pilot interest.
- Evidence supporting or contradicting the product hypothesis.
- Follow-up action.

Avoid collecting personal or confidential business information that is not needed for research.

## 10.4 Market Validation Exit Criteria

The discovery phase should not conclude merely because the planned number of interviews has been completed.

Before finalizing the first release, the product owner should have:

- Identified a clearly defined initial customer segment.
- Documented recurring problems across multiple independent businesses.
- Established which problems customers are willing to pay to solve.
- Identified the minimum viable module combination.
- Identified mandatory localization and regulatory requirements.
- Estimated implementation and support effort.
- Obtained evidence of willingness to pilot or purchase.
- Compared the proposed offer with credible alternatives.
- Recorded unresolved risks and assumptions.

The product owner must document the findings and approve the initial segment and release scope.

# 11. First Commercially Viable Release

## 11.1 Release Strategy

The first commercial release should solve a coherent business problem for a defined customer segment.

It should not attempt to deliver every module in the roadmap simultaneously.

The preferred initial scope must be selected after customer discovery.

Two potential release hypotheses are provided below.

### Option A: Finance-Led Release

Potential capabilities:

- Tenant and user management.
- Role-based access control.
- Customer and supplier records.
- Sales quotations and invoices.
- Credit notes.
- Receivables tracking.
- Basic accounting.
- VAT configuration and reporting.
- Essential financial reports.
- Supported SaaS subscription billing.
- Backups, monitoring, audit logs, and operational controls.

**Potential target:** Service businesses or other companies whose main requirement is integrated invoicing and financial visibility.

This option depends on the accounting and tax scope being sufficiently bounded and validated.

### Option B: Trading-Led Release

Potential capabilities:

- Tenant and user management.
- Customer and supplier records.
- Products and services.
- Sales orders and invoices.
- Purchase orders.
- Goods receipts.
- Inventory movements.
- Basic warehouse support.
- Receivables and payables.
- Basic accounting and VAT, as required by the validated scope.
- Operational and financial reports.

**Potential target:** Trading and distribution businesses that need integrated sales, procurement, stock, and finance.

This option may require additional design and testing for stock valuation, inventory accounting, and multi-location operations.

## 11.2 Selection Criteria

Evaluate both options against:

- Evidence of customer demand.
- Willingness to pay.
- Competitive differentiation.
- Development effort.
- Accounting and regulatory complexity.
- Third-party integration dependencies.
- Data migration difficulty.
- Customer onboarding effort.
- Support requirements.
- Time to first paying customer.
- Ongoing maintenance cost.

The product owner must select and document one initial scope or explicitly approve a justified alternative.

Do not implement both complete product paths by default.

## 11.3 General Minimum Release Requirements

Regardless of the selected commercial segment, a production-capable SaaS release must include:

- Secure authentication.
- Tenant isolation.
- Server-side authorization.
- Module entitlement enforcement.
- Auditable critical actions.
- Reliable data validation.
- Database migration management.
- Automated tests.
- Backup and recovery procedures.
- Error monitoring.
- Operational logging.
- Documented deployment procedures.
- Security review.
- Customer onboarding and support procedures.
- Clear limitations and release documentation.

A feature-complete demonstration is not equivalent to a production-ready commercial release.

# 12. Customer Acquisition and Go-to-Market

## 12.1 Initial Acquisition Hypotheses

Potential acquisition channels include:

- Direct outreach to UAE businesses.
- Partnerships with accountants and bookkeeping firms.
- Partnerships with ERP implementation consultants.
- Partnerships with business setup and advisory firms.
- Search-engine marketing.
- Educational content about business operations and accounting workflows.
- Product demonstrations.
- Referral programs.
- Industry-specific outreach.

The effectiveness of each channel must be tested before allocating a significant recurring budget.

## 12.2 Initial Sales Process

The proposed sales process is:

1. Identify a qualified prospect.
2. Understand its business model and operational problems.
3. Confirm the required workflows.
4. Demonstrate only relevant, implemented capabilities.
5. Identify missing features and integration requirements.
6. Provide a documented scope and commercial proposal.
7. Confirm onboarding and migration requirements.
8. Obtain the customer's approval.
9. Configure the tenant and activate eligible modules.
10. Migrate and validate approved data.
11. Train users where required.
12. Monitor adoption and resolve onboarding issues.
13. Collect feedback and assess expansion opportunities.

Do not promise a delivery date for unsupported functionality without an approved scope and delivery commitment.

## 12.3 Pilot Customer Strategy

A pilot program should validate both product functionality and commercial assumptions.

Potential pilot conditions include:

- Clearly documented scope.
- Defined customer responsibilities.
- Agreed data-migration process.
- Named decision-maker.
- Defined success criteria.
- Documented limitations.
- Support expectations.
- Agreed commercial terms.
- Permission to use feedback in product development.

Customer information must not be used in marketing materials without appropriate authorization.

## 12.4 Early Commercial Metrics

Track a focused set of metrics:

| Metric | Purpose |
|---|---|
| Qualified leads | Measure relevant demand |
| Demonstration-to-pilot conversion | Assess product relevance |
| Pilot-to-paid conversion | Test willingness to pay |
| Time to onboarding | Measure implementation effort |
| Time to first business transaction | Measure activation |
| Active tenants | Track adoption |
| Active users per tenant | Understand usage |
| Module attachment rate | Measure module demand |
| Subscription expansion | Measure customer growth |
| Subscription churn | Assess retention |
| Support requests per tenant | Estimate service burden |
| Gross margin | Evaluate commercial sustainability |
| Customer acquisition cost | Assess acquisition efficiency |
| Customer lifetime value | Evaluate long-term economics when sufficient data exists |

Do not set arbitrary performance targets without a documented business rationale and a defined measurement period.

# 13. Product Packaging Principles

## 13.1 Modular Availability

Customers should be able to select modules that are commercially available and compatible with their subscription.

The platform must distinguish between:

- Planned modules.
- Modules in development.
- Internal-only modules.
- Modules available for pilot use.
- Modules approved for commercial sale.
- Deprecated modules.

Only approved commercial modules should appear as purchasable options.

## 13.2 Dependencies

Some modules may depend on other capabilities.

Examples:

- Payroll may depend on HRMS and validated employee data.
- Inventory accounting may depend on accounting.
- VAT reporting may depend on correctly classified financial transactions.
- Advanced financial reporting may depend on accounting data.
- E-invoicing integration may depend on invoicing and the required provider configuration.

These are examples, not final dependency declarations.

The definitive dependency graph belongs in `docs/01-architecture/MODULE_DEPENDENCIES.md` and `docs/00-product/MODULE_CATALOGUE.md`.

The subscription engine must enforce dependencies on the server side.

A customer must not be able to bypass module requirements by manipulating the browser, API request, or client-side interface.

## 13.3 Pricing and Packaging Transparency

The commercial interface should clearly explain:

- What each module does.
- Which modules are required dependencies.
- The subscription price and billing period.
- Whether onboarding or implementation fees apply.
- Which integrations incur separate charges.
- Any applicable usage limits.
- How upgrades and downgrades work.
- What happens when a subscription expires or is cancelled.
- How customer data can be exported.

The final commercial terms must be approved before publication.

# 14. Non-Goals for the Initial Market Entry

Unless market research demonstrates a compelling need, the initial release should not attempt to provide:

- A complete replacement for every enterprise ERP.
- Extensive industry-specific customization for numerous sectors.
- A large marketplace of third-party extensions.
- Multiple independent accounting engines.
- Unvalidated regulatory claims.
- Every possible payroll configuration.
- Complex consolidation across numerous legal entities.
- A fully bespoke implementation for each customer.
- An unlimited number of integrations.
- Guaranteed compatibility with every UAE free zone or regulatory scenario.

These are scope-control principles, not permanent prohibitions.

A future release may address any of these areas through a documented product decision.

# 15. Risks and Mitigation

| Risk ID | Risk | Potential Impact | Mitigation |
|---|---|---|---|
| TM-R01 | Target segment is too broad | Weak positioning and excessive scope | Select an initial segment using discovery evidence |
| TM-R02 | Customers will not pay for modular ERP | Weak commercial viability | Test willingness to pay before finalizing packaging |
| TM-R03 | Existing alternatives are sufficient | Low conversion | Identify measurable gaps in current workflows |
| TM-R04 | UAE tax requirements are misunderstood | Incorrect tax calculations or reports | Obtain qualified review and validate against applicable requirements |
| TM-R05 | E-invoicing requirements or provider selection change | Integration rework and delayed launch | Validate provider and applicable rules; isolate integration logic |
| TM-R06 | Payroll scope is underestimated | Regulatory and financial risk | Restrict initial scope and obtain specialist validation |
| TM-R07 | Arabic support is added too late | Expensive localization rework | Establish localization architecture early |
| TM-R08 | Data migration is more complex than expected | Delayed onboarding and data errors | Test migration with representative customer datasets |
| TM-R09 | Support costs exceed revenue | Poor unit economics | Measure onboarding and support effort during pilots |
| TM-R10 | Too many modules are launched together | Delayed release and unstable software | Release modules incrementally behind approval gates |
| TM-R11 | Third-party services create hidden costs | Reduced margins | Track provider fees, API limits, and support dependencies |
| TM-R12 | Customers expect unsupported capabilities | Trust and retention problems | Publish clear module availability and limitations |

# 16. Decisions Required

The following decisions must be recorded in the product decision log before the relevant scope is finalized.

| Decision ID | Decision | Required Evidence |
|---|---|---|
| TM-DEC-001 | Select the first target customer segment | Customer discovery and competitive research |
| TM-DEC-002 | Select the first commercially viable module combination | Validated workflows and implementation estimate |
| TM-DEC-003 | Define the initial customer size range | Interview findings and support capacity |
| TM-DEC-004 | Determine initial interface languages | Customer demand and localization cost |
| TM-DEC-005 | Determine initial accounting and VAT scope | Qualified tax/accounting review |
| TM-DEC-006 | Select the UAE e-invoicing integration approach | Applicable requirements, provider validation, technical assessment |
| TM-DEC-007 | Determine payroll scope | Employer requirements and specialist review |
| TM-DEC-008 | Determine initial hosting approach | Cost, privacy, security, and customer requirements |
| TM-DEC-009 | Define subscription packaging and pricing | Competitor research and willingness-to-pay evidence |
| TM-DEC-010 | Determine onboarding and data-migration services | Pilot requirements and implementation cost |
| TM-DEC-011 | Define initial support arrangements | Expected customer count and operational capacity |
| TM-DEC-012 | Define initial acquisition channels | Early marketing and sales experiments |

Each decision must have an owner, status, decision date, supporting evidence, and rationale.

# 17. Governance and Change Control

The target market may evolve as the product receives feedback from customers and implementation partners.

Changes must be documented rather than applied informally.

A material change to the target market must trigger a review of:

- `MASTER_PRODUCT_SPECIFICATION.md`
- `PRODUCT_REQUIREMENTS.md`
- `COMMERCIAL_MODEL.md`
- `MODULE_CATALOGUE.md`
- `DEVELOPMENT_ROADMAP.md`
- Relevant architecture documents.
- Relevant phase specifications and acceptance criteria.
- Pricing, deployment, and support assumptions.

The product owner must approve material changes to the target segment or initial release scope.

Development agents must not independently redefine the target market or make unsupported commercial commitments.

# 18. Instructions for AI Development Agents

AI agents working on this repository must follow these rules:

1. Treat this document as a market-strategy input, not proof of validated demand.
2. Distinguish confirmed product requirements from commercial hypotheses.
3. Do not invent customer interviews, competitor research, market statistics, or customer commitments.
4. Do not invent certifications, partnerships, regulatory approvals, or provider accreditation.
5. Do not claim UAE tax, payroll, or e-invoicing compliance without approved evidence.
6. Do not hardcode subscription pricing or module dependencies.
7. Do not make unapproved modules commercially available.
8. Do not expand the initial release scope without documented approval.
9. Preserve tenant isolation, financial integrity, and server-side authorization.
10. Record unresolved questions in `docs/07-project-management/DECISIONS_PENDING.md`.
11. Update the requirements traceability matrix when market findings change requirements.
12. Include tests and documented evidence when implementing requirements derived from this document.

When market validation produces new evidence, agents may prepare proposed revisions but must not treat those revisions as approved until the product owner authorizes them.

# 19. Definition of Completion

This document is considered ready for implementation planning when:

- The product owner has reviewed the proposed customer segments.
- The market-validation plan has been approved.
- The first customer discovery activities have been assigned.
- The initial release options have been evaluated.
- The open decisions have owners.
- The risks have been reviewed.
- The commercial and regulatory assumptions are clearly marked.
- The document has been linked to the master specification and roadmap.

Completion of this document does not mean that the target market has been validated.

The market-validation process must produce separate findings and an explicit product-owner decision.

---

**End of Document**