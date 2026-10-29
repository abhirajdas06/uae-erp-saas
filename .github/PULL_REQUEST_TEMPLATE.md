# Pull Request

Required content is defined by `docs/05-quality/DEVELOPER_ONBOARDING_AND_WORKFLOW.md` sections 8 and 9. Delete nothing; state "not applicable" with a reason where a section does not apply.

## Task

- **Task ID / phase:**
- **Authorization:** (the approval that permits this work, for example `APPR-P01-001`; documentation maintenance may cite the standing authorization in `AGENTS.md`)
- **Objective:**
- **Scope changes discovered during the work:**

## Changes

- **Files or components changed:**
- **Specifications read before editing:**
- **Documentation and tracking records updated:** (`PROJECT_STATUS.md`, `PHASE_STATUS.md`, `DECISIONS_PENDING.md`, `RISKS_AND_ISSUES.md`, `CHANGELOG.md`)

## Checks Executed

Report actual results. Never record an unexecuted check as passed.

- [ ] `python scripts/quality/run_p00_gates.py --output-dir build/evidence` — result:
- [ ] `git diff --check` — result:
- [ ] Other checks (application tests, linters, type checks once they exist) — result:
- **Checks not run, and why:**

## Impact Assessment

Answer each explicitly.

| Concern | Affected? | If yes, how it is handled |
|---|---|---|
| Tenant isolation | | |
| Authorization or permissions | | |
| Module entitlement | | |
| Financial integrity or posted records | | |
| Personal, payroll or sensitive data | | |
| A regulatory position or claim | | |
| Database schema or migrations | | |
| Shared interfaces or high-coordination files | | |
| Threats in `docs/05-quality/THREAT_MODEL.md` | | |

## Review Routing

- [ ] Architecture — shared interfaces, data models, ADR impact
- [ ] Security — authentication, authorization, isolation, data handling
- [ ] Finance — monetary, tax or posting behavior
- [ ] Documentation — specification or tracking changes

## Outstanding

- **Known defects or limitations:**
- **Deferred requirements:**
- **Decisions or approvals required, with identifiers:**
- **New ADR required?** (a material architectural change requires an ADR before merge, and no ADR may be marked `ACCEPTED` without explicit human approval)

## Declarations

- [ ] No secret, credential, production datum or generated artifact is committed.
- [ ] No unexecuted check is reported as passed.
- [ ] No approval is recorded on behalf of a human.
- [ ] No regulatory compliance, accessibility conformance, localization completeness or security assurance is claimed without dated evidence.
- [ ] This pull request does not itself constitute a phase transition.
