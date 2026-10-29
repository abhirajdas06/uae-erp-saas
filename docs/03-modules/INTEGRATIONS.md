# INTEGRATIONS — Shared Integration Hub Module Specification

| Property | Value |
|---|---|
| Document ID | MOD-INTEGRATIONS-001 |
| Status | APPROVED SPECIFICATION — SHARED CONTRACT AND PROVIDER ACTIVATION REQUIRED |
| Owning phase / app | P10 / `integrations` |

## 1. Purpose and Boundary

Own shared provider-neutral connection metadata, secret references, transport operations, inbox/outbox/webhook evidence, scheduling and health under `INT-001`–`INT-002`. Domain modules retain provider-specific business mapping, validation, authoritative state and reconciliation.

This module is not a universal business-logic layer and does not authorize a provider, regulated activity or production credential.

## 2. Actors and Permissions

Integration administrator, credential provisioner, operator, domain owner, replay/reconciliation approver, auditor and purpose-bound support. Configure, reference/rotate credential, enable, invoke, replay, reconcile, inspect payload evidence and export diagnostics are separate and maker-checker where side effects warrant it.

## 3. Conceptual Model

`IntegrationDefinition`, `IntegrationContractVersion`, `TenantIntegration`, `CredentialReference`, `IntegrationOperation`, `IntegrationAttempt`, `IntegrationEvidence`, `WebhookInbox`, `OutboxMessage`, `IntegrationSchedule`, `IntegrationHealth` and `IntegrationReconciliationFinding`.

## 4. Rules and Verification

| ID | Rule / verification |
|---|---|
| INTM-001 | Exact purpose/provider/capability/environment/contract owner is declared and approved |
| INTM-002 | Tenant configuration is scoped; credentials are secret-backend references only |
| INTM-003 | Domain service authorizes and validates every business effect; transport cannot bypass it |
| INTM-004 | Durable intent/outbox and stable idempotency prevent duplicate effects |
| INTM-005 | Incoming webhook authentication, schema, size, replay and trusted routing fail closed |
| INTM-006 | Timeouts/retries/rate limits/circuit behavior classify permanent/transient/uncertain outcomes |
| INTM-007 | Provider-native evidence and normalized internal status remain separately traceable |
| INTM-008 | Replay/reconciliation is authorized, bounded and cannot duplicate business effects |
| INTM-009 | Logs/health/audit redact secrets and sensitive payloads while preserving correlation |
| INTM-010 | Migration/restore reconciles connections, operations, inbox/outbox and domain references |

## 5. Operations and Decisions

Monitor availability, latency, rate/cutoff, authentication, callbacks, retry/dead-letter age, uncertain operations, contract drift and credential expiry. `DEC-INT-003` governs shared infrastructure behavior; every concrete provider still requires its domain/provider approval.
