# RUN-NNN — Runbook Title

| Property | Value |
|---|---|
| Owner / backup | TBD |
| Severity / trigger | TBD |
| Applies to release/environment | TBD |
| Required access / approval | TBD |
| Last exercised / evidence | NOT_RUN |
| Next review | TBD |

## Safety and Preconditions

State tenant/customer impact, data/financial risk, required authorization, evidence preservation, secret handling, stop conditions and actions that are forbidden or irreversible.

## Diagnose

List safe read-only signals and commands, expected outcomes, correlation/time window and escalation threshold. Never include real secrets.

## Contain and Recover

Provide ordered, idempotent actions; concurrency/duplicate precautions; migration/task/provider/file consequences; rollback versus forward recovery; and decision authority.

## Verify and Reconcile

Verify service, tenant isolation, authorization, financial/business invariants, queues/providers/files, logs/audit and customer impact. “Process running” is insufficient.

## Communicate and Close

Define internal/external notification authority, status cadence, evidence/artifact location, findings, follow-up owner and post-incident review.
