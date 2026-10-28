# ADR-007: Server-Rendered UI with HTMX and Tailwind CSS

| Field | Details |
|---|---|
| ADR ID | ADR-007 |
| Title | Server-Rendered UI with HTMX and Tailwind CSS |
| Status | ACCEPTED |
| Version | 1.0 |
| Date | 27 October 2026 |
| Decision Owner | Product Architect / UX Lead |
| Reviewers | Product, Architecture, Security, Accessibility, Development |
| Affected Phases | P00–P12 |
| Related ADRs | ADR-001, ADR-003, ADR-005, ADR-006, ADR-008, ADR-019 |
| Related Requirements | PRD-001–PRD-003, IAM-003–IAM-004, NFR-001, NFR-004–NFR-005, NFR-012–NFR-013 |
| Related Documents | `SYSTEM_ARCHITECTURE.md`, `DJANGO_APP_STRUCTURE.md`, `AUTHENTICATION_AND_PERMISSIONS.md`, `API_STANDARDS.md` |
| Supersedes | None |
| Superseded By | None |

## 1. Context

The ERP requires a broad authenticated business interface containing data-entry forms, tables, approval workflows, financial documents, dashboards, and administrative screens. The initial team must deliver these capabilities without maintaining an unnecessary second client application and duplicate validation or authorization logic.

The intended stack already identifies Django Templates, HTMX, and Tailwind CSS. This ADR determines whether that stack is the primary application interface and defines the boundary for client-side behavior.

## 2. Decision Drivers

- Fast delivery of secure business workflows.
- Reuse of Django forms, sessions, CSRF protection, localization, and validation.
- Minimal duplication between browser and server business rules.
- Accessibility, keyboard use, responsive layout, and progressive enhancement.
- Maintainable component conventions across many modules.
- Selective interactivity without adopting a full single-page application by default.
- Clear boundary with external APIs under ADR-008.

## 3. Options Considered

### Option A: Django Templates with HTMX and Tailwind CSS

**Advantages:** one primary application stack, direct Django integration, reduced client state, progressive enhancement, and simpler security and deployment.

**Disadvantages:** complex offline or highly interactive experiences may need targeted JavaScript; template discipline is required.

### Option B: Separate JavaScript single-page application

**Advantages:** rich client state and independent frontend deployment.

**Disadvantages:** duplicated contracts, validation and authorization risks, larger toolchain, more API surface, and greater initial complexity.

### Option C: Django Templates without HTMX

**Advantages:** simplest behavior and strong progressive enhancement.

**Disadvantages:** more full-page reloads and reduced usability for filters, inline workflows, and modal interactions.

### Option D: Multiple frontend frameworks by module

**Advantages:** local flexibility.

**Disadvantages:** inconsistent user experience, duplicated dependencies, fragmented security patterns, and high maintenance cost.

## 4. Decision

Use Django Templates as the primary server-rendered UI, HTMX for bounded server-driven interactions, and Tailwind CSS for the shared design system. Add small, framework-light JavaScript only when browser-local behavior cannot be expressed cleanly through HTML and HTMX.

A full SPA framework is not part of the initial architecture. Introducing one for a material product surface requires a new ADR with measured requirements.

### 4.1 Server authority

The server owns authentication, authorization, entitlement, validation, calculations, state transitions, and persisted business state. Client behavior may improve usability but must not become the only enforcement layer.

### 4.2 Template ownership

- Global layouts, navigation, error pages, and reusable primitives belong in shared template locations.
- Domain templates belong to the owning Django app.
- Shared components require documented inputs and safe escaping behavior.
- Templates must not perform business calculations or unrestricted database access.

### 4.3 HTMX interaction contract

HTMX endpoints are ordinary protected server endpoints. They must enforce the same tenant, permission, entitlement, CSRF, validation, transaction, and audit rules as full-page requests.

Endpoints should distinguish full-page and fragment responses deliberately. Out-of-band swaps, triggers, and redirects must use documented conventions. A user opening an HTMX endpoint directly must not bypass security or corrupt state.

### 4.4 Forms and validation

Django forms or equivalent server-side schemas remain authoritative. Validation errors must be returned accessibly and preserve safe user input. Financial totals and protected ownership fields must be calculated or loaded server-side.

Unsafe methods require CSRF protection and use POST or another explicitly approved method. State changes through GET are prohibited.

### 4.5 Tailwind and design system

Tailwind CSS supports a project-owned set of design tokens and reusable components. Do not scatter one-off class combinations when a stable component exists. Production builds must generate bounded assets and must not depend on a public CDN.

### 4.6 Accessibility and localization

The primary interface must support semantic HTML, keyboard navigation, focus management, labels, error associations, adequate contrast, and screen-reader announcements for dynamic updates.

Text must be localizable. Layouts and components must not assume English-only width or left-to-right behavior. Arabic and RTL readiness require validation before the relevant release; documentation does not claim completed localization.

### 4.7 Client-side JavaScript

Small JavaScript modules may support widgets, focus management, charts, local formatting, or browser APIs. They must not store authoritative permissions, entitlements, financial values, or secret material.

Large client-state libraries, duplicated domain models, and framework-specific business workflows require explicit architectural review.

### 4.8 Error and loading states

Every interactive workflow must define loading, empty, validation, authorization, conflict, timeout, and server-error behavior. Optimistic updates are permitted only when rollback and authoritative reconciliation are clear.

## 5. Rationale

Most ERP workflows are server-authoritative forms, tables, searches, approvals, and documents. Server rendering with bounded HTMX interactions provides useful responsiveness without forcing every capability through a public-style REST API or duplicating business rules in a client application.

## 6. Consequences

### Positive consequences

- Smaller initial toolchain and deployment surface.
- Consistent reuse of Django security and validation.
- Faster delivery of accessible business workflows.
- Reduced client/server contract duplication.

### Negative consequences and trade-offs

- Some highly interactive experiences may require custom JavaScript.
- Fragment contracts require conventions and tests.
- Template and component reuse needs active governance.
- Offline-first behavior is not a default capability.

### Risks and mitigations

- **Inconsistent fragments:** shared response and component conventions.
- **Authorization assumed from hidden UI:** enforce every server endpoint independently.
- **Accessibility regressions:** automated checks plus keyboard and screen-reader review.
- **CSS sprawl:** design tokens and reusable components.
- **Excessive client logic:** architecture review thresholds.

## 7. Security and Tenant-Isolation Implications

- All full and partial requests use server-side authorization and tenant scoping.
- CSRF protections apply to HTMX requests.
- Templates escape untrusted output by default; reviewed sanitization is required for approved rich text.
- Sensitive data must not be embedded in DOM attributes or client logs unnecessarily.
- Cache headers and fragment caches must preserve tenant and authorization boundaries.

## 8. Data Integrity and Migration

UI changes do not alter authoritative business state outside reviewed application services. Forms must handle concurrency and stale edits for applicable records. Database migrations remain owned by the affected domain, not the presentation layer.

## 9. Operational Impact

The deployment pipeline must build and version static assets, collect them reproducibly, apply appropriate cache headers, and monitor frontend errors and failed HTMX requests without recording sensitive content.

## 10. Implementation Requirements

1. Define base layouts, component conventions, and template ownership.
2. Establish HTMX full-page/fragment response conventions.
3. Establish CSRF, error, redirect, and history behavior.
4. Create accessibility and localization review checklists.
5. Pin and build Tailwind through the approved asset pipeline.
6. Add representative tests for full and fragment requests.
7. Document the threshold requiring review of a larger JavaScript framework.

## 11. Validation and Acceptance Criteria

- [ ] Protected full and fragment routes enforce identical security rules.
- [ ] Unsafe requests are CSRF-protected and do not use GET.
- [ ] Server-side validation remains authoritative.
- [ ] Keyboard navigation and focus behavior work after dynamic updates.
- [ ] Dynamic errors and status changes are accessible.
- [ ] Templates support localization and do not hardcode tenant-sensitive values.
- [ ] Static assets build reproducibly without production CDN dependency.
- [ ] Client scripts contain no authoritative business or authorization rules.
- [ ] Representative workflows work with full-page fallback where required.

## 12. Alternatives Rejected

- A separate SPA is rejected as the default because current requirements do not justify its duplicate application surface.
- Per-module frontend frameworks are rejected because they fragment security and usability.
- HTMX-only enforcement is rejected; the server remains authoritative.
- CDN-only production assets are rejected due to availability, integrity, and change-control concerns.

## 13. References

- `docs/01-architecture/SYSTEM_ARCHITECTURE.md`
- `docs/01-architecture/DJANGO_APP_STRUCTURE.md`
- `docs/01-architecture/API_STANDARDS.md`
- Django templates: https://docs.djangoproject.com/en/stable/topics/templates/
- Django CSRF: https://docs.djangoproject.com/en/stable/howto/csrf/
- HTMX documentation: https://htmx.org/docs/
- Tailwind CSS documentation: https://tailwindcss.com/docs
- WCAG overview: https://www.w3.org/WAI/standards-guidelines/wcag/

## 14. Approval

**Current Status:** ACCEPTED

- **Recommended option:** Django Templates, HTMX, and Tailwind CSS as the primary interface.
- **Approved By:** Product Owner — explicit project instruction
- **Approval Date:** 28 October 2026
- **Approval Notes:** Accepted following `ADR_STANDARDS_REVIEW.md`; a material SPA surface requires a new evidence-based ADR.

This accepted decision governs future frontend scaffolding; implementation remains phase-authorized work.

## 15. Supersession History

| Version | Status | Description |
|---|---|---|
| 1.0 | ACCEPTED | Initial server-rendered UI decision accepted after standards review. |
