# Developer Onboarding, Local Environment and Contribution Workflow

| Property | Value |
|---|---|
| Document ID | QUAL-DEVWF-001 |
| Status | APPROVED DOCUMENTATION BASELINE — APPLICATION COMMANDS REQUIRE IMPLEMENTATION EVIDENCE |
| Owner | DevOps / Documentation |
| Governing decisions | ADR-015, ADR-016, ADR-017 |
| Related documents | `CODING_STANDARDS.md`, `CI_QUALITY_GATES.md`, `DEFINITION_OF_DONE.md`, `TEST_DATA_AND_FIXTURES.md`, `../06-deployment/ENVIRONMENT_VARIABLES.md` |

## 1. Purpose and Boundary

`AGENTS.md` and `README.md` define what to build and in what order, and `CI_QUALITY_GATES.md` defines the automated gates, but no document tells a new contributor or agent how to set up a working environment, run the checks that exist today, name a branch, structure a commit, or open a reviewable change. This document owns that definition.

This document owns environment prerequisites, the currently runnable verification commands, the planned application environment, branching and commit conventions, pull-request expectations, review routing and the local pre-submission checklist. It does not own coding style, which remains with `CODING_STANDARDS.md`; gate definitions, which remain with `CI_QUALITY_GATES.md`; completion criteria, which remain with `DEFINITION_OF_DONE.md`; or deployment, which remains with `../06-deployment/DEPLOYMENT_GUIDE.md`.

## 2. Current Repository State

The repository is in the documentation-controlled stage described in `AGENTS.md` section 19. A contributor must understand the following before expecting an application to run.

| Fact | Detail |
|---|---|
| Application code | Authorized P01-T01 bootstrap: Django project package, minimal `apps.core`, and no business models or migrations |
| Database | SQLite is bootstrap-only in P01-T01; PostgreSQL configuration remains owned by unauthorized P01-T03 |
| Runnable tooling | P00 validators plus the hash-locked P01-T01 Django/pytest/Ruff toolchain |
| Continuous integration | `.github/workflows/p00-quality.yml` runs the P00 gate suite on pull request, on push to the default branch, and on manual dispatch |
| Pinned runtime | Python 3.14.7, as pinned in the workflow |
| Authorization state | P01 application implementation requires the separate `APPR-P01-001` authorization recorded in `../07-project-management/DECISIONS_PENDING.md` |

| ID | Requirement |
|---|---|
| DWF-001 | A contributor does not scaffold a Django project, settings module, app, model or migration before the owning phase is authorized |
| DWF-002 | A contributor does not create placeholder application files to make the repository look complete, per `AGENTS.md` section 5 |
| DWF-003 | The absence of application code is the expected state, not a defect to be fixed opportunistically |

## 3. Prerequisites

| Requirement | Detail |
|---|---|
| Git | Any currently supported version, with the repository cloned and the default branch tracked |
| Python | 3.14.7 to match the pinned continuous-integration runtime; a different minor version may produce non-comparable results |
| Virtual environment | A project-local virtual environment is used; global installation of project tooling is prohibited |
| Editor configuration | UTF-8 encoding, LF line endings in committed content, and no trailing-whitespace insertion |
| Line endings | Windows contributors must not commit CRLF into Markdown or Python sources; `git diff --check` must report no whitespace error |
| Docker | Required only once the authorized application phase introduces the local service stack; not required for documentation work |

| ID | Requirement |
|---|---|
| DWF-010 | Tooling versions used locally match the pinned continuous-integration versions; a local pass on a different version is not evidence |
| DWF-011 | No contributor commits a virtual environment, build output, cache directory, compiled artifact or editor-local configuration |
| DWF-012 | Secrets are never placed in a tracked file; local configuration uses an untracked environment file derived from the published example template, per ADR-017 |

## 4. Verification Commands Available Today

Run from the repository root.

```bash
python scripts/quality/run_p00_gates.py --output-dir build/evidence
```

```bash
python scripts/quality/validate_docs.py --root docs --format json --output build/evidence/docs-validation.json
```

```bash
python scripts/quality/validate_governance.py --root docs --format json --output build/evidence/governance-validation.json
```

```bash
git diff --check
```

The P00 gate suite remains the authoritative governance/documentation check. It runs five gates in one command: manifest validation, documentation validation, governance validation, the secret scan and the validator unit tests. P01-T01 now additionally pins pytest, pytest-django, Ruff and pip-audit for the bounded application bootstrap checks below.

For the authorized P01-T01 bootstrap, create a Python 3.14.7 virtual environment and install the verified lock:

```bash
python -m pip install --require-hashes -r requirements-dev.lock
python manage.py check
python -m pytest --collect-only
python -m pytest
python -m ruff format --check .
python -m ruff check .
python -m pip check
python -m pip_audit --local
```

The P01-T01 commands do not authorize later settings, PostgreSQL, tenant, user, audit, container or deployment work.

| ID | Requirement |
|---|---|
| DWF-020 | The P00 gate suite is run before submitting any documentation change, and its result is reported truthfully |
| DWF-021 | Gate evidence is written under `build/` and is not committed unless the owning phase specification requires a recorded evidence artifact |
| DWF-022 | A validator finding is fixed, not suppressed; changing a validator to pass a defective document requires explicit review |
| DWF-023 | An unexecuted check is never reported as passed, per `AGENTS.md` section 12 |

## 5. Planned Application Environment

The following is the intended local stack for the authorized application phase. It does not exist yet and must not be created before authorization.

| Component | Intended local provision |
|---|---|
| Application | Django with Gunicorn only in production-like contexts; the development server locally |
| Database | PostgreSQL in a container, matching the production major version |
| Cache and broker | Redis in a container |
| Background processing | Celery worker and scheduler as separate local processes or containers |
| Asset pipeline | Pinned Tailwind build producing local static assets, with no production content-delivery-network dependency, per `../01-architecture/UI_DESIGN_SYSTEM.md` UIX-060 |
| Orchestration | Docker Compose, per ADR-016 |
| Configuration | Environment variables documented in `../06-deployment/ENVIRONMENT_VARIABLES.md`, loaded from an untracked local file |

| ID | Requirement |
|---|---|
| DWF-030 | The local database major version matches the intended production major version; a mismatch invalidates migration and query evidence |
| DWF-031 | Local development uses synthetic data only, per `TEST_DATA_AND_FIXTURES.md`; production data is never loaded locally |
| DWF-032 | Local outbound communication is disabled or redirected to an approved sink, per `../01-architecture/NOTIFICATIONS_AND_COMMUNICATIONS.md` NTF-053 |
| DWF-033 | Local provider integrations are stubbed by default; a live provider call from a development environment requires an explicit, recorded reason |
| DWF-034 | The first authorized application task delivers a working local setup path and verifies that a new contributor can reach a running application from a clean clone |
| DWF-035 | Required settings are validated at startup so a misconfigured environment fails fast rather than behaving unpredictably |

## 6. Branching

| ID | Requirement |
|---|---|
| DWF-040 | Work happens on a branch; direct commits to the default branch are prohibited |
| DWF-041 | Branch names are lowercase, hyphen-separated and prefixed by their origin and scope, following the established repository pattern of a work-stream prefix and a topic, for example `codex/p00-quality-gates` |
| DWF-042 | A branch carrying authorized phase work names its phase and task identifier in its topic, for example `codex/p01-t01-tenant-model` |
| DWF-043 | One branch addresses one bounded task; unrelated changes are not bundled |
| DWF-044 | Parallel agents working concurrently use separate branches or worktrees, per `AGENTS.md` section 8, and coordinate before touching shared files, migrations, settings, tenancy middleware or authentication |
| DWF-045 | A branch is rebased or merged from the default branch before review when it has diverged materially; shared history is never rewritten after others depend on it |

## 7. Commits

| ID | Requirement |
|---|---|
| DWF-050 | A commit is a coherent, self-consistent unit; a commit that leaves the repository failing its gates is not submitted |
| DWF-051 | The subject line is imperative, concise and specific; the established repository convention permits an optional type prefix such as `docs:` and that convention is applied consistently within a work stream |
| DWF-052 | The body states what changed and why, and names the task, phase or decision identifier where one applies |
| DWF-053 | A commit touching a regulatory, financial-integrity, tenant-isolation or security concern says so explicitly in its body |
| DWF-054 | Secrets, credentials, production data and large binary artifacts are never committed |
| DWF-055 | A commit never claims an unexecuted check passed, and never records an approval on behalf of a human |
| DWF-056 | An agent-authored commit identifies its co-authorship according to the project's configured attribution convention |

## 8. Pull Requests and Review

| ID | Requirement |
|---|---|
| DWF-060 | A pull request states the task identifier, scope, files changed, checks executed with their actual results, outstanding issues, limitations and required approvals |
| DWF-061 | It explicitly answers whether tenant isolation, financial integrity, authorization, entitlement, personal data or a regulatory position is affected |
| DWF-062 | It lists the documentation records updated, including tracking records required by `AGENTS.md` |
| DWF-063 | A scope change discovered mid-task is recorded in the pull request rather than silently absorbed |
| DWF-064 | Continuous-integration gates must pass; a failing gate is diagnosed, not bypassed, and hooks and signing are never skipped |
| DWF-065 | Review routing follows the owning concern: architecture for shared interfaces and data models, security for authentication, authorization, isolation and data handling, finance for monetary and tax behavior, and documentation for specification changes |
| DWF-066 | A reviewer does not approve a change solely because the author's tests pass, per `AGENTS.md` section 7 |
| DWF-067 | A material architectural change requires an ADR before merge, and an ADR is never marked `ACCEPTED` without explicit human approval |
| DWF-068 | A pull request is not a phase transition; phase progression requires its own approval gate |

## 9. Pre-Submission Checklist

1. The task scope was authorized and is unchanged, or the change is recorded.
2. Relevant specifications were read before editing.
3. The change is the smallest coherent set that satisfies the task.
4. The P00 gate suite was executed, with actual results recorded, including its validator-unit-test gate.
5. `git diff --check` reports no whitespace or line-ending error.
6. No secret, credential, production datum or generated artifact is staged.
7. Internal links and identifiers in changed documents resolve.
8. Related tracking records were updated: `PROJECT_STATUS.md`, `PHASE_STATUS.md` where applicable, `DECISIONS_PENDING.md`, `RISKS_AND_ISSUES.md` and `CHANGELOG.md`.
9. New decisions and risks were registered rather than left in prose.
10. Unverified regulatory statements are marked as unverified with a named owner.
11. The final diff was inspected in full.
12. The completion report distinguishes executed checks from planned ones and names any required human approval.

## 10. Verification

| ID | Verification |
|---|---|
| DWF-TST-001 | A clean clone can run the gate suite and `git diff --check` with no additional undocumented step and no third-party package installation |
| DWF-TST-002 | The documented commands match the commands the continuous-integration workflow executes |
| DWF-TST-003 | The pinned local Python version matches the workflow's pinned version |
| DWF-TST-004 | `git diff --check` is clean on the working tree |
| DWF-TST-005 | The secret scanner reports no finding on the working tree |
| DWF-TST-006 | Once the application phase is authorized, a clean clone reaches a running local application following this document alone |
| DWF-TST-007 | Once the application phase is authorized, the local database major version matches the intended production version |

`DWF-TST-001` to `DWF-TST-005` are executable today. `DWF-TST-006` and `DWF-TST-007` are `NOT_RUN` and blocked by `APPR-P01-001`.

## 11. Pending Decisions

| ID | Decision required | Owner |
|---|---|---|
| DEC-DWF-001 | Approve the commit subject convention, including whether a type prefix is mandatory | Product Owner / Documentation |
| DEC-DWF-002 | Approve the branch protection, required reviewers and merge strategy for the default branch | Product Owner / DevOps |
| DEC-DWF-003 | Approve the local service stack composition and pinned versions at the first authorized application task | DevOps / Architecture |
| DEC-DWF-004 | Approve the formatter, linter and type-checker toolchain and their enforcement point | Architecture / QA |

These decisions are registered in `../07-project-management/DECISIONS_PENDING.md`.
