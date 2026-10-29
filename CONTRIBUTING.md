# Contributing

This repository builds a modular, multi-tenant ERP SaaS platform for the United Arab Emirates. Contributions are governed by documents, not convention, because tenant isolation, financial integrity, regulatory accuracy and truthful reporting are product requirements rather than preferences.

## Read these first

1. [AGENTS.md](AGENTS.md) — repository-wide development instructions. Authoritative for every contributor, human or agent.
2. [README.md](README.md) — product overview, repository structure and documentation navigation.
3. [docs/05-quality/DEVELOPER_ONBOARDING_AND_WORKFLOW.md](docs/05-quality/DEVELOPER_ONBOARDING_AND_WORKFLOW.md) — environment prerequisites, the commands that run today, branching, commits, pull requests and the pre-submission checklist.
4. [docs/05-quality/CODING_STANDARDS.md](docs/05-quality/CODING_STANDARDS.md) and [docs/05-quality/DEFINITION_OF_DONE.md](docs/05-quality/DEFINITION_OF_DONE.md).
5. The specification for the phase your task belongs to, under [docs/02-phases/](docs/02-phases/).

## Current state

The repository is in the documentation-controlled stage described in `AGENTS.md` section 19. No Django project, application code, model or migration exists yet, and application implementation requires the `APPR-P01-001` authorization recorded in [docs/07-project-management/DECISIONS_PENDING.md](docs/07-project-management/DECISIONS_PENDING.md).

Do not scaffold an application, create placeholder files or start a new phase because the previous one looks finished.

## Before you submit

Run from the repository root:

```bash
python scripts/quality/run_p00_gates.py --output-dir build/evidence
```

```bash
git diff --check
```

The gate suite runs manifest validation, documentation validation, governance validation, the secret scan and the validator unit tests in one command, so no separate test invocation is needed.

Then work through the pre-submission checklist in [docs/05-quality/DEVELOPER_ONBOARDING_AND_WORKFLOW.md](docs/05-quality/DEVELOPER_ONBOARDING_AND_WORKFLOW.md) section 9.

## Non-negotiables

- Never report an unexecuted check as passed.
- Never commit a secret, credential or production datum.
- Never weaken tenant isolation, authorization or entitlement enforcement for convenience.
- Never delete or silently modify a posted financial record.
- Never claim regulatory compliance, provider accreditation or completed localization without dated evidence.
- Never mark an ADR `ACCEPTED`, approve a phase or record an approval on behalf of a human.
- Record unresolved decisions in `DECISIONS_PENDING.md` and material risks in `RISKS_AND_ISSUES.md` rather than leaving them in prose.

When uncertain, prefer a small, reversible, well-documented change, and escalate the decision.
