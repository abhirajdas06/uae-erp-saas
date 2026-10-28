# Agent Prompt Library — UAE ERP SaaS

This directory contains reusable prompts for implementing and reviewing the ERP phase by phase and module by module.

Prompts are execution aids, not sources of product requirements. They must link to approved specifications and may not broaden scope, approve phases, invent UAE regulatory rules, or report unexecuted tests as passed.

## Prompt hierarchy

1. `IMPLEMENTATION_TASK_PROMPT_TEMPLATE.md` — required structure for every bounded coding task.
2. `phase-prompts/` — phase-level orchestration prompts.
3. `module-prompts/` — module-specific implementation and review prompts.

Every generated task prompt must identify:

- task and phase IDs;
- objective and non-goals;
- authoritative documents;
- expected files/components;
- dependencies and permissions;
- acceptance criteria and tests;
- security, tenant-isolation, financial, and regulatory considerations;
- evidence and documentation updates;
- reviewers and approvals;
- rollback or recovery expectations.
