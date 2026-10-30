# UI Design System and Interaction Standards

| Property | Value |
|---|---|
| Document ID | ARCH-UI-001 |
| Status | APPROVED DOCUMENTATION BASELINE — IMPLEMENTATION EVIDENCE REQUIRED |
| Owner | Product Architect / UX Lead |
| Governing decisions | ADR-007, ADR-006, ADR-005 |
| Related documents | `ARCHITECTURAL_DECISIONS/ADR-007-server-rendered-ui-with-htmx-and-tailwind.md`, `API_STANDARDS.md`, `LOCALIZATION_AND_BILINGUAL_UI.md`, `../05-quality/ACCESSIBILITY_AND_BROWSER_SUPPORT.md` |

## 1. Purpose and Boundary

`../00-product/MASTER_PRODUCT_SPECIFICATION.md` section 13 requires the detailed design system and interaction patterns to be established separately, and ADR-007 section 10 requires base layouts, component conventions and template ownership to be defined before frontend scaffolding. This document owns that definition.

This document owns shared layout structure, navigation information architecture, design tokens, the reusable component catalogue, form and table conventions, state behavior and HTMX fragment conventions. It does not own business workflows, screen-by-screen functional requirements, authorization rules or accessibility conformance targets; those remain with the module specifications, `AUTHENTICATION_AND_PERMISSIONS.md` and `../05-quality/ACCESSIBILITY_AND_BROWSER_SUPPORT.md`.

Hiding or omitting a user-interface element is never an authorization control. Every fragment, action and navigation target is independently authorized on the server under ADR-005 and ADR-006.

## 2. Application Shell and Layout

| ID | Requirement |
|---|---|
| UIX-001 | One authenticated application shell provides the skip link, global header, tenant context indicator, primary navigation, content region, notification region and footer in a single base template |
| UIX-002 | Layout variants are limited to the authenticated shell, the unauthenticated identity shell, the platform-administration shell, the print/document layout and the error layout |
| UIX-003 | The content region declares one page header contract: title, optional context subtitle, record status, primary action, secondary actions and breadcrumb trail |
| UIX-004 | The shell renders the active tenant and active user identity on every authenticated page so that tenant confusion is visible to the operator |
| UIX-005 | Page width, spacing scale, breakpoint behavior and content density derive from tokens, not per-template values |
| UIX-006 | A single ARIA live region per page owns asynchronous status announcements; components do not create ad hoc live regions |

## 3. Navigation Information Architecture

| ID | Requirement |
|---|---|
| UIX-010 | Primary navigation is grouped by business domain, not by Django app name, and each group maps to one or more entitled modules |
| UIX-011 | Navigation is generated from a server-side registry recording label key, URL name, required permission, required module entitlement and ordering |
| UIX-012 | A module the tenant has not subscribed to is either hidden or rendered as an explicit non-actionable upgrade affordance according to `../03-modules/MODULE_ENTITLEMENT_ENGINE.md`; it is never rendered as an available action |
| UIX-013 | A permission the user lacks removes the navigation entry and the corresponding in-page action; the server still authorizes the target |
| UIX-014 | Breadcrumbs reflect record ownership hierarchy, not browser history |
| UIX-015 | Deep links to a record remain stable and tenant-scoped; navigation never encodes a client-supplied tenant identifier |

## 4. Design Tokens

Tokens are defined once in the Tailwind configuration and consumed by name. Literal colors, spacing values, font sizes, shadows and radii are prohibited in templates.

| Token group | Contents | Rule |
|---|---|---|
| Color — neutral | Surface, raised surface, border, muted text, body text, heading text | Must meet the contrast requirement in `../05-quality/ACCESSIBILITY_AND_BROWSER_SUPPORT.md` |
| Color — brand | Primary, primary hover, primary contrast text | Not used to convey state meaning |
| Color — status | Info, success, warning, danger, each with surface, border, text and icon variants | Status is never communicated by color alone |
| Color — financial | Debit, credit, negative amount, reconciled, unreconciled | Negative monetary values carry a sign or parenthesis, not only a color |
| Typography | Font family for Latin and Arabic, size scale, line height, weight, tabular-numeral face | Monetary and quantity columns use the tabular-numeral face |
| Spacing | A single base scale | No arbitrary one-off values |
| Radius, border, elevation | Bounded named steps | No per-component exceptions |
| Motion | Duration and easing steps | Honors `prefers-reduced-motion` |
| Logical direction | Inline-start and inline-end spacing and alignment tokens | Physical left/right utilities are prohibited where a logical token exists |

Token values require UX approval under `DEC-UI-002`. Until approved, a provisional neutral palette may be used for scaffolding and must not be presented as the approved brand system.

## 5. Component Catalogue

Each component requires a documented contract: name, purpose, template path, inputs, required permission or entitlement context, accessible name source, keyboard behavior, direction behavior and states.

| Group | Components |
|---|---|
| Structure | Shell, page header, section card, tabs, accordion, toolbar, sidebar filter panel, empty state, skeleton loader |
| Data display | Data table, sortable column header, pagination control, definition list, key-value summary, status badge, audit trail list, attachment list, monetary cell, quantity cell, date cell |
| Input | Text, textarea, number, monetary, quantity, percentage, select, searchable select, multi-select, date, date range, checkbox, radio group, switch, file upload, hidden token, line-item editor |
| Feedback | Inline field error, form error summary, toast, banner, confirmation dialog, destructive confirmation dialog, progress indicator, asynchronous operation status panel |
| Action | Primary button, secondary button, tertiary link action, destructive action, icon button with accessible label, action menu, bulk action bar |
| Document | Printable document header, totals block, VAT summary block, bilingual document header, signature and stamp block |

| ID | Requirement |
|---|---|
| UIX-020 | A one-off markup block is not introduced where a catalogue component exists; extension is by documented variant |
| UIX-021 | Every interactive component is reachable and operable by keyboard with a visible focus indicator |
| UIX-022 | Every icon-only control carries a translated accessible name |
| UIX-023 | Components escape untrusted output by default; rich text requires reviewed sanitization under `../05-quality/SECURITY_REQUIREMENTS.md` SEC-006 |
| UIX-024 | No component embeds authoritative permissions, entitlements, secrets or server-calculated financial values in client-readable attributes beyond what the view requires |

## 6. Form and Validation Conventions

| ID | Requirement |
|---|---|
| UIX-030 | Server-side Django forms or equivalent schemas remain authoritative; client validation is an optional convenience |
| UIX-031 | Every field has a programmatically associated label, and every error is associated with its field |
| UIX-032 | A failed submission re-renders with safe user input preserved, a form-level error summary that receives focus, and per-field messages |
| UIX-033 | Monetary and quantity inputs apply the precision and rounding rules in ADR-013; the client never computes an authoritative total |
| UIX-034 | Server-controlled and protected ownership fields are never rendered as editable inputs |
| UIX-035 | Unsafe operations use POST or another approved method with CSRF protection; state change through GET is prohibited |
| UIX-036 | Destructive, posting, approval and irreversible financial actions require explicit confirmation naming the record and the effect |
| UIX-037 | Multi-line document editors preserve unsaved line state across validation failures and declare their concurrency behavior |
| UIX-038 | Repeated submission of a financial or externally visible action is protected by the idempotency rules in `API_STANDARDS.md` section 14 |

## 7. Data Table Conventions

| ID | Requirement |
|---|---|
| UIX-040 | Tables are paginated by default with server-side filtering and sorting; unbounded result rendering is prohibited |
| UIX-041 | Filter state is expressed in the URL so a filtered view is shareable and reproducible within the tenant |
| UIX-042 | Column definitions declare label key, alignment, data type, sensitivity and whether the column is exportable |
| UIX-043 | Monetary and numeric columns are end-aligned with tabular numerals and a declared currency presentation |
| UIX-044 | Row-level actions reflect the user permissions for that object; the server re-authorizes the action target |
| UIX-045 | Bulk actions declare maximum selection size, authorization scope, partial-failure reporting and audit behavior |
| UIX-046 | Tables declare loading, empty, filtered-empty, error and truncated-result states |
| UIX-047 | Export from a table honors export permission, sensitive-column policy and the audit requirements in `../03-modules/REPORTING.md` |

## 8. State Behavior

Every interactive workflow declares all of the following, as required by ADR-007 section 4.8.

| State | Required behavior |
|---|---|
| Loading | Non-blocking indicator; disable the submitting control to prevent duplicate submission |
| Empty | Explain the cause and offer the permitted next action |
| Validation failure | Field-level and summary messaging; focus moves to the summary |
| Authorization failure | Neutral message that does not disclose the existence of an out-of-scope record |
| Entitlement failure | Explicit module-availability message distinguishable from an authorization failure |
| Conflict | Stale-edit detection with a reconciliation path, never silent overwrite |
| Timeout or transient failure | Safe retry guidance that does not duplicate a financial effect |
| Server error | Correlation identifier presented for support without sensitive detail |
| Asynchronous accepted | Operation status surface with terminal outcome and audit linkage |

## 9. HTMX Fragment Conventions

| ID | Requirement |
|---|---|
| UIX-050 | A fragment endpoint is an ordinary protected endpoint enforcing identical tenant, permission, entitlement, CSRF, validation, transaction and audit rules as a full-page request |
| UIX-051 | A fragment response returns a bounded, self-contained template partial with a documented target and swap strategy |
| UIX-052 | Direct browser navigation to a fragment endpoint returns a safe response and never bypasses security or corrupts state |
| UIX-053 | Out-of-band swaps, triggers, redirects and history behavior use documented project conventions rather than per-template invention |
| UIX-054 | A fragment that changes authoritative state returns the authoritative server-rendered result, not a client-assumed outcome |
| UIX-055 | Fragment responses set cache headers that preserve tenant and authorization boundaries |
| UIX-056 | Dynamic insertions manage focus and announce status through the page live region |

## 10. Asset Pipeline

| ID | Requirement |
|---|---|
| UIX-060 | Tailwind and all frontend dependencies are pinned and built through the approved pipeline; production must not depend on a public CDN |
| UIX-061 | Static assets build reproducibly, are versioned or fingerprinted, and are served with appropriate cache headers |
| UIX-062 | Client JavaScript is small, framework-light and contains no authoritative business, authorization or entitlement logic |
| UIX-063 | Adopting a material client-state framework requires a new ADR with measured requirements |
| UIX-064 | Fonts, icons and media are self-hosted unless an approved decision records an external source |

## 11. Acceptance and Tests

| ID | Verification |
|---|---|
| UIX-TST-001 | Shell, navigation registry, permission filtering and entitlement filtering render correctly for entitled, unentitled and unauthorized contexts |
| UIX-TST-002 | Full-page and fragment routes for representative workflows enforce identical security outcomes |
| UIX-TST-003 | Direct access to fragment endpoints is safe and non-corrupting |
| UIX-TST-004 | Validation failure preserves input, associates errors and focuses the summary |
| UIX-TST-005 | Destructive and posting actions require confirmation and are audited |
| UIX-TST-006 | Table pagination, filter-state round-trip, sorting and bulk-action authorization behave as specified |
| UIX-TST-007 | Keyboard operability and focus management hold after dynamic updates |
| UIX-TST-008 | Templates contain no literal color, spacing or physical-direction values where a token exists |
| UIX-TST-009 | Static assets build reproducibly with no production CDN dependency |
| UIX-TST-010 | No authoritative permission, entitlement, secret or server-calculated total is exposed in client-readable attributes |

All scenarios are `NOT_RUN` until the owning phase implements the interface.

## 12. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-UI-002 | Approve design token values, typography pairing and brand palette | Product Owner / UX Lead |
| DEC-UI-003 | Approve primary navigation grouping and module-to-group mapping | Product Owner |
| DEC-UI-004 | Approve the unentitled-module presentation: hidden or non-actionable upgrade affordance | Product Owner / Commercial |
| DEC-UI-005 | Approve the printable document layout family and bilingual document header | Product Owner / Finance |

These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`. No approval is recorded by this document.
