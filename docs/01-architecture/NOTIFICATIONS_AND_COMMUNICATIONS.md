# Notifications and Outbound Communications

| Property | Value |
|---|---|
| Document ID | ARCH-NOTIFY-001 |
| Status | APPROVED DOCUMENTATION BASELINE — CHANNEL SCOPE AND PROVIDER SELECTION REQUIRED |
| Owner | Product Architect / Platform domain owner |
| Governing decisions | ADR-009, ADR-010, ADR-018, ADR-019 |
| Related documents | `EVENT_AND_TASK_PROCESSING.md`, `../03-modules/INTEGRATIONS.md`, `LOCALIZATION_AND_BILINGUAL_UI.md`, `../05-quality/DATA_PROTECTION_AND_RETENTION.md` |

## 1. Purpose and Boundary

Notification behavior is referenced across the module specifications but no document owns the channel model, template governance, recipient resolution, suppression rules, delivery evidence or privacy constraints for outbound communication. This document owns that definition.

This document owns the notification catalogue contract, channel model, recipient resolution, template and localization governance, delivery semantics, suppression and rate control, delivery evidence and the related tests. It does not own transport infrastructure or provider credentials, which remain with `../03-modules/INTEGRATIONS.md`; event emission and task execution, which remain with ADR-009, ADR-010 and `EVENT_AND_TASK_PROCESSING.md`; or statutory e-invoice transmission, which remains with `../03-modules/UAE_EINVOICING.md` and the provider contract.

A notification is an advisory copy of an event. It is never the authoritative record of a business fact, never the mechanism of a state transition, and never a substitute for the audit trail.

## 2. Channel Model

| ID | Requirement |
|---|---|
| NTF-001 | Supported channels are declared explicitly; the initial set is in-application notification and transactional email, with SMS and webhook subscription gated by `DEC-NTF-001` |
| NTF-002 | Each channel declares its delivery guarantee, latency expectation, failure semantics, retry behavior, size limits and sensitivity ceiling |
| NTF-003 | No channel is assumed available; a channel without an approved provider and configuration is inactive and its notifications are suppressed with a recorded reason |
| NTF-004 | Provider-specific behavior is confined to an adapter behind the integration boundary; business modules emit notification intents, never provider payloads |
| NTF-005 | Marketing, promotional and bulk commercial messaging is out of scope for this specification and requires separate consent, suppression and regulatory review |

## 3. Notification Catalogue

Every notification requires a registered definition before implementation. A notification sent from code without a catalogue entry is a defect.

| Field | Requirement |
|---|---|
| Notification ID | Stable identifier in the owning module namespace |
| Trigger | The named domain event or schedule that produces it |
| Category | Security, authentication, financial, approval workflow, operational, subscription and billing, or regulatory submission status |
| Audience | Tenant user role, tenant contact, external business party, or platform operator |
| Channels | Permitted channels and the fallback order |
| Sensitivity | Data classification of the content, per `../05-quality/DATA_PROTECTION_AND_RETENTION.md` |
| Opt-out | Whether the recipient may disable it; security, billing and regulatory notices are not opt-out |
| Rate policy | Batching, digest eligibility and per-recipient ceiling |
| Retention | Retention class for the notification record and its delivery evidence |

| ID | Requirement |
|---|---|
| NTF-010 | Categories are mutually exclusive; a notification carrying both financial and security meaning is split or classified at the higher sensitivity |
| NTF-011 | Security, authentication, subscription-billing and regulatory-status notifications are mandatory and cannot be suppressed by recipient preference |
| NTF-012 | Each catalogue entry names the permission or entitlement context that makes a recipient eligible |

## 4. Recipient Resolution

| ID | Requirement |
|---|---|
| NTF-020 | Recipients are resolved server-side at send time from tenant-scoped data; a client-supplied recipient address is never trusted for a tenant notification |
| NTF-021 | Eligibility requires the recipient to hold the permission and module entitlement needed to see the referenced record at send time; entitlement loss suppresses the notification |
| NTF-022 | A recipient is resolved exactly once per notification; duplicate resolution through overlapping roles is collapsed |
| NTF-023 | Notification to an external business party such as a customer or supplier uses the contact record on the tenant document and is authorized as an outbound disclosure, not as internal messaging |
| NTF-024 | Deactivated users, unverified addresses, failed-address records and recipients outside the tenant are excluded with a recorded reason |
| NTF-025 | Platform-operator notifications never include tenant business content beyond what the operational purpose requires, per ADR-018 |
| NTF-026 | A notification never discloses the existence of a record the recipient is not authorized to see, including through its subject line or preview text |

## 5. Content and Localization

| ID | Requirement |
|---|---|
| NTF-030 | Content is rendered from a versioned template; string assembly in business logic is prohibited |
| NTF-031 | Template language resolves from recipient preference, then tenant default, then platform default, per `LOCALIZATION_AND_BILINGUAL_UI.md` L10N-070 |
| NTF-032 | A single message is internally consistent in one language, including subject, body, attachment name and embedded values |
| NTF-033 | Templates escape all interpolated values; untrusted tenant content is never rendered as executable or active content |
| NTF-034 | Content carries the minimum data necessary; full financial detail, personal data, payroll figures, bank details and credentials are referenced by secure authenticated link rather than embedded |
| NTF-035 | Credentials, tokens, one-time codes and reset links follow the authentication rules in `AUTHENTICATION_AND_PERMISSIONS.md`, with bounded lifetime and single use |
| NTF-036 | Attachments are generated server-side, size-bounded, virus-scanned where applicable under `../05-quality/SECURITY_REQUIREMENTS.md` SEC-008, and authorized for the recipient |
| NTF-037 | Every message identifies the sending tenant or the platform unambiguously so a recipient can judge its origin |
| NTF-038 | Security, billing and regulatory templates require reviewed translations before release in a given language |

## 6. Delivery Semantics

| ID | Requirement |
|---|---|
| NTF-040 | A notification intent is persisted in the same transaction as the authoritative business change and dispatched through the transactional outbox under ADR-010; a failed send never rolls back a committed business fact |
| NTF-041 | A business transaction never blocks on external delivery; dispatch is asynchronous under ADR-009 |
| NTF-042 | Dispatch is idempotent: a retried or replayed task does not produce a duplicate message to the same recipient for the same notification instance |
| NTF-043 | Retries are bounded with backoff and classify outcomes as delivered, permanently failed, or uncertain; an uncertain outcome is never silently treated as delivered |
| NTF-044 | Permanent failure, bounce and complaint feedback updates the recipient address state and suppresses further sends to that address until corrected |
| NTF-045 | Ordering is not guaranteed across channels; a notification whose meaning depends on arrival order declares the dependency and its handling |
| NTF-046 | Background dispatch carries explicit tenant context under the rules in `MULTI_TENANCY.md`; context is never inherited ambiently from a worker process |
| NTF-047 | Scheduled and digest notifications resolve recipients and authorization at dispatch time, not at schedule time |

## 7. Suppression, Rate Control and Environment Safety

| ID | Requirement |
|---|---|
| NTF-050 | Per-recipient, per-tenant and per-notification rate ceilings prevent a loop or bulk operation from generating unbounded messages |
| NTF-051 | High-volume operational and approval notifications are digest-eligible; financial, security and regulatory notifications are not digested by default |
| NTF-052 | A notification storm trips a circuit breaker that suppresses non-mandatory categories, raises an operational alert and records the suppression |
| NTF-053 | Non-production environments must not send messages to real external recipients; outbound delivery is disabled, redirected to an approved sink, or restricted to an allowlist, and the active mode is visible at startup |
| NTF-054 | Production recipient data is never copied into a development or test environment for notification testing, per `../05-quality/TEST_DATA_AND_FIXTURES.md` |
| NTF-055 | A tenant-configurable notification preference never overrides a mandatory category |

## 8. Evidence, Audit and Retention

| ID | Requirement |
|---|---|
| NTF-060 | Each notification instance records its definition ID and version, tenant, resolved recipient reference, channel, language, dispatch time, attempt history, terminal outcome and correlation identifier |
| NTF-061 | Message bodies are not retained in full where they contain sensitive data; a reproducible reference to the template version and the authoritative record is retained instead |
| NTF-062 | Logs, metrics and traces exclude message content, recipient addresses beyond what is operationally required, credentials and one-time secrets, per ADR-018 |
| NTF-063 | Dispatch of a notification that discloses financial, payroll, personal or regulatory data to an external party is auditable under `../03-modules/AUDIT_FOUNDATION.md` |
| NTF-064 | Notification records and delivery evidence follow an assigned retention class in `../05-quality/DATA_PROTECTION_AND_RETENTION.md` and are disposed of accordingly |
| NTF-065 | Delivery evidence is advisory and is never presented as proof of regulatory submission; regulatory acknowledgement evidence remains with the owning integration |

## 9. Acceptance and Tests

| ID | Verification |
|---|---|
| NTF-TST-001 | Every notification sent in reviewed scope has a catalogue definition with a complete contract |
| NTF-TST-002 | Recipient resolution excludes users lacking permission or entitlement, deactivated users and out-of-tenant addresses |
| NTF-TST-003 | No notification, including its subject and preview, discloses a record the recipient is unauthorized to see |
| NTF-TST-004 | A committed business change with a failing notification channel preserves the business change and records a failed dispatch |
| NTF-TST-005 | A replayed or retried dispatch task produces no duplicate message |
| NTF-TST-006 | Uncertain delivery outcomes are classified as uncertain and are not reported as delivered |
| NTF-TST-007 | Bounce and complaint feedback suppresses subsequent sends to the affected address |
| NTF-TST-008 | Language resolution and single-language message consistency hold across channels |
| NTF-TST-009 | Interpolated tenant content is escaped and cannot inject active content |
| NTF-TST-010 | Rate ceilings and circuit-breaker suppression behave as specified under a generated storm |
| NTF-TST-011 | Mandatory categories cannot be disabled by recipient or tenant preference |
| NTF-TST-012 | Non-production configuration sends no message to a real external recipient |
| NTF-TST-013 | Background dispatch carries correct tenant context and produces no cross-tenant delivery |
| NTF-TST-014 | Logs and metrics contain no message content, credential or one-time secret |
| NTF-TST-015 | Notification records and evidence are retained and disposed of per their assigned retention class |

All scenarios are `NOT_RUN` until the owning phase implements the capability.

## 10. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-NTF-001 | Approve the launch channel set, including whether SMS and outbound webhook subscriptions are in initial scope | Product Owner |
| DEC-NTF-002 | Select the transactional email provider, sending domain, authentication records and data-processing terms | Product Owner / DevOps |
| DEC-NTF-003 | Approve the launch notification catalogue, including mandatory categories and opt-out eligibility | Product Owner |
| DEC-NTF-004 | Approve notification record and delivery-evidence retention periods | Product Owner / Privacy reviewer |
| DEC-NTF-005 | Approve whether outbound business-document delivery to customers and suppliers is in initial scope and under what disclosure authorization | Product Owner |

No provider is selected, no spend is authorized and no sending domain is configured by this document. These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`.
