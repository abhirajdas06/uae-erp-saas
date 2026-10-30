# Accessibility, Browser Support and Device Compatibility

| Property | Value |
|---|---|
| Document ID | QUAL-A11Y-001 |
| Status | APPROVED DOCUMENTATION BASELINE — CONFORMANCE CLAIMS REQUIRE EXECUTED EVIDENCE |
| Owner | QA / UX Lead |
| Governing decisions | ADR-007 |
| Related documents | `../01-architecture/UI_DESIGN_SYSTEM.md`, `../01-architecture/LOCALIZATION_AND_BILINGUAL_UI.md`, `TESTING_STRATEGY.md`, `DEFINITION_OF_DONE.md` |

## 1. Purpose and Boundary

`../00-product/MASTER_PRODUCT_SPECIFICATION.md` section 16.8 requires the project to define supported browsers, responsive behavior, accessibility expectations and device constraints. ADR-007 section 10 requires an accessibility review checklist and names accessibility regression as a tracked risk. This document owns those definitions.

This document owns the accessibility conformance target, the per-pattern accessibility requirements, the supported browser and device matrix, responsive behavior expectations, the verification method and the evidence required at a release gate. It does not own visual tokens or component structure, which remain with `../01-architecture/UI_DESIGN_SYSTEM.md`, nor language and directionality, which remain with `../01-architecture/LOCALIZATION_AND_BILINGUAL_UI.md`.

No document, status record, release note or commercial material may claim accessibility conformance before the evidence in section 8 exists. An automated check alone is never sufficient evidence of conformance.

## 2. Conformance Target

| ID | Requirement |
|---|---|
| A11Y-001 | The proposed conformance target is WCAG 2.2 Level AA for the authenticated business interface, the identity and sign-in surfaces, and generated business documents in their on-screen presentation |
| A11Y-002 | The target requires approval under `DEC-A11Y-001`; until approved it is the working engineering standard and not a conformance claim |
| A11Y-003 | Whether any UAE statutory or public-sector accessibility obligation applies to this product is an open question recorded as `DEC-A11Y-002`; no such obligation is asserted or denied by this document |
| A11Y-004 | A deliberate, time-bounded exception requires a recorded rationale, the affected success criteria, an accessible alternative path and a named approver |
| A11Y-005 | Third-party or embedded components must meet the same target; an inaccessible dependency is a selection defect, not an accepted limitation |

## 3. Core Requirements by Pattern

| ID | Requirement |
|---|---|
| A11Y-010 | Semantic HTML carries structure: one page heading, a correct heading hierarchy, landmark regions, lists for list content and tables for tabular data only |
| A11Y-011 | All functionality is operable by keyboard alone, in a logical order, with no keyboard trap and with a visible, sufficiently contrasting focus indicator |
| A11Y-012 | A skip link reaches the main content region, and the shell exposes navigation, main and complementary landmarks |
| A11Y-013 | Every form control has a programmatically associated, visible label; placeholder text is never the only label |
| A11Y-014 | Required fields, input format expectations and constraints are communicated in text, not by color or symbol alone |
| A11Y-015 | Validation errors are announced, associated with their field, and summarized in a focusable summary that preserves submitted input |
| A11Y-016 | Text and interactive elements meet the contrast requirement of the approved target; status is never conveyed by color alone |
| A11Y-017 | Data tables use header cells with correct scope and an accessible caption or accessible name |
| A11Y-018 | Dialogs trap focus while open, are dismissible by keyboard, restore focus on close and carry an accessible name |
| A11Y-019 | Dynamic updates, including HTMX swaps, announce their outcome through the single page live region and manage focus deliberately per `../01-architecture/UI_DESIGN_SYSTEM.md` UIX-056 |
| A11Y-020 | Icon-only controls, charts and meaningful images carry text alternatives; decorative images are hidden from assistive technology |
| A11Y-021 | Content remains usable at 200 percent text zoom and at 400 percent zoom with reflow and without loss of function |
| A11Y-022 | Motion respects `prefers-reduced-motion`, and no content flashes in a manner that risks a seizure |
| A11Y-023 | Session timeout warns the user, allows extension and does not discard entered data without warning |
| A11Y-024 | Accessible names, error text and announcements are translated and correct in every released interface language and in both text directions |
| A11Y-025 | Target size, drag alternatives, consistent help placement and redundant-entry avoidance follow the approved target version |

## 4. Browser Support Matrix

The proposed matrix requires approval under `DEC-A11Y-003`. Versions are expressed as policy rather than fixed numbers so the matrix does not silently expire.

| Tier | Scope | Support commitment |
|---|---|---|
| Tier 1 — fully supported | Current and immediately previous stable major versions of Chrome, Edge, Firefox and Safari on desktop; current Chrome on Android and current Safari on iOS | Full functionality, visual fidelity and accessibility; defects are release-blocking per severity |
| Tier 2 — functional | Older versions within a declared support window, and additional Chromium-based browsers | Core business functionality and data integrity; minor visual deviation accepted |
| Tier 3 — unsupported | Browsers outside the window, browsers without current security updates, and legacy engines | Not tested; the application may present a clear unsupported-browser notice and must not corrupt data |

| ID | Requirement |
|---|---|
| A11Y-030 | The matrix is reviewed at each release gate and updated with a dated record; an unreviewed matrix is treated as stale |
| A11Y-031 | JavaScript is required for the authenticated interface; this constraint is documented for customers rather than silently assumed |
| A11Y-032 | Core business workflows degrade safely without unnecessary client dependency and never leave a financial operation in an indeterminate state on a client failure |
| A11Y-033 | Cookies and session storage requirements are declared, and the application behaves predictably when they are blocked |
| A11Y-034 | A browser without current security support is not accommodated by weakening a security control |

## 5. Responsive and Device Behavior

| ID | Requirement |
|---|---|
| A11Y-040 | A single responsive implementation serves all screen sizes; a separate mobile codebase is out of scope under ADR-007 |
| A11Y-041 | Breakpoints derive from design tokens, and layouts are verified at small, medium, large and extra-large widths in both text directions |
| A11Y-042 | No horizontal scrolling is required for primary content at the declared minimum supported width |
| A11Y-043 | Dense data tables declare their small-screen strategy: priority columns, stacked presentation or an explicit horizontal-scroll region with an accessible affordance |
| A11Y-044 | Pointer and touch targets meet the minimum size and spacing of the approved target; hover-only interaction is prohibited for essential function |
| A11Y-045 | Data-entry-intensive workflows declare the device classes they are designed for; a workflow unsuitable for a small screen states that rather than degrading silently |
| A11Y-046 | Printed and PDF business documents have a defined page size, margin, direction and font-coverage behavior for both scripts |
| A11Y-047 | Native mobile applications and offline operation are out of initial scope and are not implied by responsive support |

## 6. Verification Method

| Layer | Method | Scope |
|---|---|---|
| Automated | Accessibility rule engine integrated into the test suite and CI per `CI_QUALITY_GATES.md` | Every shared component and every representative page and fragment |
| Static | Template and markup review against this standard during code review | Each changed template |
| Keyboard | Manual keyboard-only traversal | Every workflow changed in the task, and the full shell at a release gate |
| Screen reader | Manual testing with at least one screen reader per supported platform family | Representative workflows per release gate, and any changed dynamic pattern |
| Zoom and reflow | Manual verification at 200 and 400 percent | Representative workflows per release gate |
| Direction | Manual verification in right-to-left mode | Required before any Arabic interface release, per `../01-architecture/LOCALIZATION_AND_BILINGUAL_UI.md` L10N-TST-003 |

| ID | Requirement |
|---|---|
| A11Y-050 | Automated results are reported with the rule set and version; a rule set change is recorded because it changes result comparability |
| A11Y-051 | An automated pass is necessary but never sufficient; manual keyboard and screen-reader evidence is required for a conformance statement |
| A11Y-052 | A finding is classified by severity and tracked in `../07-project-management/RISKS_AND_ISSUES.md` until resolved or formally accepted by a named approver |
| A11Y-053 | Fixtures covering accessibility behavior are regression tests; a resolved finding gains a test that prevents recurrence |

## 7. Definition-of-Done Additions

A task that changes the interface is not done until all of the following hold, in addition to `DEFINITION_OF_DONE.md`.

1. Automated accessibility checks pass for the changed surfaces with results recorded.
2. Keyboard-only operation of the changed workflow is verified.
3. Labels, error associations and accessible names exist and are translatable.
4. Dynamic updates announce outcomes and manage focus.
5. Contrast and non-color status conveyance hold for changed components.
6. The changed surface renders correctly at the declared breakpoints and in both text directions.
7. New or changed components have a documented accessibility contract in the component catalogue.
8. Any exception is recorded with rationale, alternative path and approver.

## 8. Release Gate Evidence

| Evidence | Required content | State |
|---|---|---|
| Automated conformance report | Tool, rule set, version, scope, findings, severity | `NOT_RUN` |
| Keyboard traversal record | Workflows covered, outcome, defects raised | `NOT_RUN` |
| Screen-reader record | Screen reader and platform, workflows, outcome | `NOT_RUN` |
| Zoom and reflow record | Levels tested, workflows, outcome | `NOT_RUN` |
| Direction record | Right-to-left verification of shell, components, tables and documents | `NOT_RUN` |
| Browser matrix verification | Tier 1 coverage result and dated matrix review | `NOT_RUN` |
| Exception register | Open exceptions with approver and alternative path | `NOT_RUN` |

Evidence identifiers are allocated by the owning phase under `../08-requirements-traceability/REQUIREMENT_ID_CONVENTIONS.md`. All evidence is `NOT_RUN` until the interface exists and the checks are executed. A conformance statement issued without this evidence is a reporting defect under `AGENTS.md` section 12.

## 9. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-A11Y-001 | Approve the conformance target and version, and the surfaces in scope | Product Owner |
| DEC-A11Y-002 | Determine, against authoritative sources with a recorded verification date, whether any UAE accessibility obligation applies to a private-sector SaaS product, and whether any target customer imposes one contractually | Product Owner / Legal reviewer |
| DEC-A11Y-003 | Approve the browser, platform and minimum-width support matrix and its review cadence | Product Owner |
| DEC-A11Y-004 | Approve the screen readers and assistive technologies in the tested set | QA / UX Lead |
| DEC-A11Y-005 | Approve the device classes each data-entry-intensive workflow must support | Product Owner |

These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`. No conformance claim is made by this document.
