# Repository-Wide Development Instructions

## 1. Purpose

This repository contains the specifications, source code, tests, documentation, deployment configuration, and development workflows for a modular, multi-tenant ERP SaaS platform targeting businesses in the United Arab Emirates (UAE).

The system is being developed incrementally with OpenAI Codex and supporting development agents.

These instructions establish the repository-wide rules that all AI coding agents and human contributors must follow.

The objective is to build a secure, maintainable, commercially viable, production-ready ERP SaaS platform through controlled implementation phases.

## 2. Product Principles

All work must follow these principles:

1. Build a modular ERP platform with subscription-based module access.
2. Treat tenant isolation, authorization, financial integrity, auditability, and security as foundational requirements.
3. Prefer a modular monolith over premature microservices.
4. Define clear responsibilities and interfaces between modules.
5. Enforce permissions and subscription entitlements on the server side.
6. Make commercial plans, module availability, dependencies, and prices configurable wherever appropriate.
7. Avoid unnecessary complexity and speculative functionality.
8. Implement functionality incrementally against approved requirements.
9. Maintain automated tests and verifiable acceptance criteria.
10. Design for reliable deployment, backup, recovery, monitoring, and ongoing maintenance.
11. Verify UAE regulatory requirements against authoritative sources before implementing or claiming compliance.
12. Keep implementation documentation synchronized with the actual codebase.

## 3. Technology Direction

The intended technology direction is:

- Backend: Python and Django.
- API: Django REST Framework where API functionality is required.
- Database: PostgreSQL.
- Frontend: Django templates, HTMX, and Tailwind CSS, unless an approved architecture decision changes this.
- Background processing: Celery and Redis where asynchronous processing is needed.
- Web serving: Gunicorn behind Nginx in applicable production deployments.
- Containerization: Docker and Docker Compose for suitable development and deployment workflows.
- Testing: pytest and pytest-django, supplemented by other appropriate automated checks.
- Version control: Git and GitHub.
- CI/CD: GitHub Actions or an explicitly approved alternative.

These are architectural defaults, not permission to introduce every component immediately.

Before implementing a technology-dependent feature, inspect the approved architecture documents and the existing repository.

Do not replace an approved technology or introduce a major dependency without documenting the reason and obtaining approval when required.

## 4. Documentation Is the Source of Requirements

Before starting any non-trivial task, inspect:

1. This `AGENTS.md` file.
2. The root `README.md`, if present.
3. Relevant documents under `docs/00-product/`.
4. Relevant documents under `docs/01-architecture/`.
5. The specification for the active implementation phase under `docs/02-phases/`.
6. Relevant module specifications under `docs/03-modules/`.
7. Applicable quality, security, testing, and deployment requirements.
8. Existing code, tests, migrations, and configuration affected by the task.

Use the following authority order when interpreting requirements:

1. Explicit, current human-approved decisions.
2. Approved architecture decisions and approved product specifications.
3. Approved phase and module specifications.
4. Approved task specifications and acceptance criteria.
5. Existing implementation and tests, where consistent with approved requirements.
6. Unapproved proposals, inferred requirements, and agent suggestions.

Existing code is not automatically correct simply because it exists.

If documents conflict, stop the affected work, identify the conflicting statements, and request a decision or follow an explicitly documented conflict-resolution procedure.

Do not silently resolve material product, security, financial, architectural, or regulatory conflicts.

## 5. Documentation-First Development

The repository must be developed in controlled stages.

During the initial documentation stage:

- Create and validate foundational product documents.
- Define the architecture and major system boundaries.
- Define agent responsibilities and handoff rules.
- Establish reusable documentation templates.
- Define phase dependencies and acceptance criteria.
- Establish quality, testing, security, and deployment standards.
- Record unresolved questions and assumptions.
- Validate consistency across documents.

Do not implement the complete ERP merely because its directory structure or roadmap has been documented.

Application implementation must follow an explicitly authorized phase and bounded task scope.

Do not create empty application files, placeholder models, speculative migrations, or non-functional components solely to make the repository appear complete.

## 6. Phase and Task Authorization

Every implementation task must identify:

- Task ID.
- Parent phase.
- Objective.
- Relevant specifications.
- Scope.
- Files or components expected to change, when known.
- Dependencies.
- Acceptance criteria.
- Required tests.
- Security and data-integrity considerations.
- Documentation updates required.
- Required reviewer or approver.

Agents may execute tasks that fall within an explicitly approved phase and its authorized scope.

Do not start a new phase simply because the previous phase appears finished.

A phase may proceed only after its required acceptance criteria, verification evidence, and approval gates have been satisfied.

If the scope changes materially, document the change and obtain the required approval before proceeding.

## 7. Agent Responsibilities

### Orchestrator

The orchestrator coordinates the workflow.

It must:

- Read the authoritative specifications.
- Identify dependencies and missing requirements.
- Break approved work into bounded tasks.
- Assign tasks to suitable agents.
- Track task status and verification evidence.
- Coordinate testing and reviews.
- Prevent unauthorized phase transitions.
- Maintain project status and decision records.
- Produce factual completion reports.
- Request human decisions when required.

The orchestrator must not treat an agent's completion message as sufficient proof of correctness.

### Architect Agent

The architect defines and reviews system boundaries, data models, interfaces, dependencies, and architectural decisions.

It must identify cross-module impacts before major shared-interface changes.

Material architectural changes require approval according to the project's decision policy.

### Developer Agent

The developer implements authorized tasks against approved specifications.

It must:

- Inspect relevant existing code before editing.
- Make the smallest coherent set of changes that satisfies the task.
- Follow established coding standards.
- Add or update tests.
- Preserve existing functionality unless a change is explicitly authorized.
- Update relevant documentation.
- Report files changed, checks executed, and outstanding issues.

The developer must not claim that unexecuted tests passed.

### Test Engineer Agent

The test engineer independently evaluates the implementation against acceptance criteria.

It should test relevant:

- Normal workflows.
- Validation failures.
- Authorization failures.
- Tenant-isolation boundaries.
- Duplicate and repeated requests.
- Transaction and rollback behavior.
- Concurrent operations where applicable.
- External integration failures.
- Financial rounding and calculation rules.
- Regression scenarios.

It must report reproducible evidence and distinguish automated results from manual review.

### Security Review Agent

The security reviewer examines applicable authentication, authorization, tenant isolation, secrets management, input handling, file handling, dependency risks, logging, and data exposure.

Financial and personal data require particular care.

Security findings must be classified by severity and tracked until resolved or explicitly accepted by an authorized human.

### Code Review Agent

The code reviewer checks correctness, maintainability, readability, scope compliance, test coverage, regression risks, and consistency with approved architecture.

It must not approve a change solely because the developer's tests pass.

### DevOps Agent

The DevOps agent manages authorized infrastructure, CI/CD, deployment configuration, monitoring, backup, recovery, and release workflows.

It must not perform production deployment, destructive infrastructure operations, credential rotation, or irreversible database operations without the required explicit authorization.

### Documentation Agent

The documentation agent maintains accurate specifications, technical documentation, deployment instructions, decision records, and release notes.

It must not document proposed or planned functionality as implemented functionality.

## 8. Multi-Agent Coordination

Agents must not make conflicting changes to shared files or shared interfaces without coordination.

For parallel work:

1. Assign each task a unique identifier.
2. Define task ownership and expected outputs.
3. Identify shared files and dependencies.
4. Prefer independent workstreams.
5. Use separate branches or worktrees when appropriate.
6. Integrate changes through review and automated checks.
7. Resolve conflicting changes before acceptance.

Database models, migrations, settings, tenancy middleware, authentication, shared services, and module interfaces are high-coordination areas.

Do not allow multiple agents to independently redesign these components.

## 9. Security and Tenant Isolation

Tenant isolation is a core product requirement.

All tenant-owned data access must follow the approved tenancy architecture.

Agents must not assume that hiding a user-interface element provides authorization.

Required safeguards include, as applicable:

- Server-side permission checks.
- Server-side subscription entitlement checks.
- Tenant-scoped queries and object access.
- Validation of tenant ownership at trust boundaries.
- Secure background task execution.
- Tenant-aware exports and reports.
- Tenant-safe caching and file storage.
- Appropriate audit logging.
- Protection against insecure direct object references.
- Automated tests for cross-tenant access.

Any task that could weaken tenant isolation requires additional review.

Do not introduce cross-tenant access paths without an explicitly approved business requirement and documented authorization model.

## 10. Financial Integrity

Financial functionality must preserve the integrity and traceability of business records.

As applicable:

- Use appropriate decimal representations for monetary values.
- Define currency precision and rounding rules explicitly.
- Use database transactions for related financial operations.
- Enforce appropriate database constraints.
- Make repeated requests safe where duplicate processing is possible.
- Preserve audit history for material financial changes.
- Define correction, reversal, and cancellation behavior.
- Avoid silent modification or deletion of posted financial records.
- Test calculations, edge cases, concurrency, and rollback behavior.
- Separate SaaS subscription billing from ERP customer invoicing.

Do not invent accounting policies, tax treatments, payroll rules, or statutory requirements.

Record unresolved financial rules for review.

## 11. UAE Regulatory and Provider Requirements

The product is intended for businesses operating in the UAE.

For regulatory, tax, payroll, privacy, data-residency, and e-invoicing requirements:

- Consult authoritative and current sources.
- Record the source and date of verification.
- Distinguish confirmed requirements from interpretations and assumptions.
- Document applicability conditions and effective dates where relevant.
- Obtain specialist review when the consequences justify it.
- Do not claim regulatory approval, provider accreditation, or compliance without evidence.
- Do not treat a successful API integration as proof of regulatory compliance.

E-invoicing functionality must use an appropriately validated provider and a documented integration contract.

If provider selection or regulatory requirements remain unresolved, record the dependency instead of inventing an implementation.

## 12. Testing and Verification

Follow the approved testing strategy and definition of done.

Tests should be added at the appropriate levels, including:

- Unit tests.
- Model and database tests.
- Service-layer tests.
- API and view tests.
- Permission tests.
- Tenant-isolation tests.
- Integration tests.
- Regression tests.
- Relevant end-to-end tests.

For every task:

1. Run the relevant tests when the environment permits.
2. Run required formatting, linting, type checks, or static analysis.
3. Inspect the final diff.
4. Record failures and environmental limitations.
5. Never report an unexecuted check as passed.

If a required check cannot be executed, state why and identify the remaining verification required.

## 13. Database and Migration Safety

Before modifying database models or migrations:

- Inspect the existing models and migration history.
- Identify affected modules and dependencies.
- Consider existing tenant data and backward compatibility.
- Define safe migration and rollback expectations.
- Test the migration where the environment permits.
- Document operational risks.

Never delete, reset, or irreversibly modify a database to make a task pass without explicit authorization.

Do not run destructive commands against production without specific, explicit approval.

Do not rewrite shared migration history without an approved plan.

## 14. Secrets and Environment Configuration

- Never commit credentials, API keys, private keys, tokens, or production secrets.
- Use environment variables or an approved secrets-management system.
- Keep example configuration free of real credentials.
- Document required variables and safe defaults.
- Validate required settings at startup where appropriate.
- Do not expose secrets in logs, error messages, test artifacts, or documentation.
- Do not copy production secrets into development environments.

Use `.env.example` or an equivalent safe template when environment variables are required.

## 15. External Integrations

External integrations must have clearly defined boundaries.

For each significant integration, document:

- Provider and purpose.
- Configuration requirements.
- Authentication mechanism.
- Request and response expectations.
- Timeout and retry behavior.
- Idempotency requirements.
- Error handling.
- Rate limits where known.
- Logging and data-retention considerations.
- Testing strategy.
- Provider-specific assumptions.

Do not hardcode provider-specific behavior throughout unrelated business modules.

Use adapters or clearly defined integration services where appropriate.

Do not assume a provider's availability, pricing, approval status, or capabilities without verification.

## 16. Deployment and Operations

Production readiness includes more than successful application startup.

Deployment documentation must address, as applicable:

- Supported operating environment.
- Infrastructure requirements.
- Domain, DNS, and TLS.
- Application and database configuration.
- Database migrations.
- Static and uploaded files.
- Background workers and scheduling.
- Secrets management.
- Monitoring and alerting.
- Backup and restoration.
- Recovery objectives.
- Rollback procedures.
- Security updates.
- Incident response.
- Capacity and scaling.
- Operational costs and assumptions.

Keep deployment documentation synchronized with the actual implementation.

Distinguish required infrastructure from optional enhancements and estimates from verified quotations.

## 17. Project Status and Reporting

Project status must be evidence-based.

Task and phase reports should identify:

- Status.
- Completed scope.
- Files or components changed.
- Tests and checks executed.
- Results and relevant evidence.
- Review outcomes.
- Outstanding defects.
- Known limitations.
- Deferred requirements.
- Decisions required.
- Dependencies and blockers.
- Recommended next action.

Use the project's approved status vocabulary.

Do not mark a phase completed merely because coding has stopped or a pull request has been opened.

## 18. Failure Handling

When an agent encounters a blocker:

1. Stop work that depends on the unresolved issue.
2. Record the blocker and its impact.
3. Identify relevant documents, code, or test evidence.
4. Propose a resolution where possible.
5. Request a human decision if the issue exceeds the agent's authority.
6. Resume only when the required dependency or decision is resolved.

Do not conceal failing tests, security findings, conflicting specifications, or incomplete requirements.

## 19. Initial Documentation-Only Mode

Until the foundational specifications and development workflow are approved, the repository is in documentation-only mode.

During this period, agents may:

- Inspect the repository.
- Create and edit Markdown documentation.
- Create documentation templates.
- Propose architecture decisions.
- Record unresolved questions.
- Create or validate documentation manifests and schemas when explicitly in scope.
- Check documentation consistency.

They must not:

- Implement ERP business features.
- Generate speculative database models or migrations.
- Build all Django applications pre-emptively.
- Claim the platform is production-ready.
- Start subsequent implementation phases without authorization.

If the repository already contains application code, inspect it and preserve it. Do not delete or replace existing work to conform to a proposed directory structure.

## 20. Completion Requirements

A task is complete only when its defined acceptance criteria have been addressed and its required evidence has been recorded.

Before reporting completion:

1. Check the task scope.
2. Review the changed files.
3. Validate relevant references and links.
4. Run required checks where possible.
5. Update related documentation and status records.
6. Record unresolved issues and assumptions.
7. Identify any required human approval.
8. Provide a concise, factual completion report.

A phase is complete only when all mandatory phase-level requirements, verification steps, and approval gates have been satisfied.

## 21. Final Operating Rule

When uncertain, prefer a small, reversible, well-documented change over a broad, speculative change.

Read first. Verify requirements. Work within the authorized scope. Test. Review. Document evidence. Escalate unresolved decisions.

Never trade security, tenant isolation, financial integrity, or truthful reporting for speed.

## Persistent Project Workflow

The project owner has authorized routine documentation maintenance and the drafting of proposed architecture decisions without requiring a new instruction after every completed documentation task.

This standing authorization does not permit an agent to:

- Mark an ADR `ACCEPTED` without explicit human approval.
- Approve a phase or release on behalf of the product owner.
- Implement application features before the applicable phase is authorized.
- Perform destructive data or infrastructure operations.
- Deploy to production, incur costs, select a paid provider, or make legal or regulatory commitments.

After every meaningful documentation task, the responsible agent must:

1. Validate changed documents, identifiers, and internal references.
2. Check related product, architecture, ADR, and tracking documents for conflicts.
3. Update the appropriate project tracking records.
4. Record unresolved decisions in `docs/07-project-management/DECISIONS_PENDING.md`.
5. Record material risks in `docs/07-project-management/RISKS_AND_ISSUES.md`.
6. Update `docs/07-project-management/PROJECT_STATUS.md` and, when applicable, `PHASE_STATUS.md`.
7. Identify and proceed with the next dependency-ready documentation task when it is within standing authorization and does not depend on unresolved human approval.

Whenever an approval remains pending, the completion report and applicable tracking record must state:

1. The approval identifier and exact decision required.
2. The authorized approver or reviewer role.
3. The evidence and alternatives to review.
4. The recommended option and practical consequences.
5. An explicit example statement or repository action that records approval.
6. Whether the approval blocks the current phase, the next phase, or only a later release gate.

Do not report only that “approval is pending.” Make the required decision and recording method actionable without implying approval.

The tracking documents have distinct responsibilities:

- `PROJECT_STATUS.md` records current overall progress, blockers, and the next recommended action.
- `PHASE_STATUS.md` records phase lifecycle status and exit-gate evidence.
- `DECISIONS_PENDING.md` is the canonical register for unresolved decisions and approval requests.
- `RISKS_AND_ISSUES.md` is the canonical register for material risks and active issues.
- The ADR register records ADR identifiers, record state, decision status, and file location.

Detailed requirements remain in their owning specifications. Tracking documents must link to those sources rather than duplicating them.

## Architectural Decision Governance

Before making a change that materially affects architecture, database design, tenant isolation, security, module entitlements, financial integrity, integrations, or deployment:

1. Read the relevant documents under `docs/01-architecture/`.
2. Read the relevant ADRs under `docs/01-architecture/ARCHITECTURAL_DECISIONS/`.
3. Identify conflicts between the proposed implementation and existing ACCEPTED ADRs.
4. Do not silently change an accepted decision.
5. If a material architectural change is required, prepare a proposed ADR describing the context, alternatives, recommendation, consequences, risks, and tests.
6. Do not mark an ADR ACCEPTED without explicit human approval.
7. After approval, update the affected architecture documents, implementation tasks, tests, and ADR register.
8. Preserve superseded ADRs and record their replacements.
9. If the decision is unresolved, stop the affected architectural work and report the specific decision required.
10. Do not create an ADR for every routine implementation detail; use ADRs for decisions with material architectural, security, data-integrity, operational, or long-term maintenance consequences.
