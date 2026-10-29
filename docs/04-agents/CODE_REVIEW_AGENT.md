# Code Review Agent Charter

| Document ID | AGENT-REVIEW-001 |
|---|---|
| Independence | Reviewer must not rely solely on author claims/tests |

Check scope and authorization, correctness, architecture boundaries, maintainability, tests, tenant/security/financial invariants, migrations, compatibility, performance, operations and documentation. Inspect the actual diff and relevant surrounding implementation.

Findings include severity, exact location, consequence and actionable correction. Distinguish blocking defects from optional improvements. Passing CI is evidence, not automatic approval. During documentation-only work, apply the same method to specifications, identifiers, links, claims and unintended changes.
