# Requirement and Evidence Identifier Conventions

| Property | Value |
|---|---|
| Document ID | GOV-ID-001 |
| Status | CANONICAL BASELINE |
| Owner | Documentation / QA / Architecture |

## 1. Purpose

Identifiers are stable references, never recycled labels. Renaming prose does not change an identifier; removal preserves a deprecated record and replacement link. Status and approval are properties of a record, not encoded by changing its ID.

## 2. Namespaces

| Pattern | Owner / use | Example |
|---|---|---|
| `PRD/TEN/IAM/SUB/BILL/CRM/SALES/INV/EIN/ACC/VAT/INVN/HR/PAY/PROJ/EXP/FA/BANK/REP/INT/AUD/OPS/NFR/DEP-NNN` | Product requirement | `SALES-001` |
| `<module>M-NNN` | Module-level control refining product requirements | `SALESM-001` |
| `ADR-NNN` | Architecture decision | `ADR-014` |
| `P00`–`P12` | Canonical phase | `P04` |
| `Pnn-SPEC/TRACE/PROMPTS-NNN` | Phase document | `P03-TRACE-001` |
| `Pnn-Tnn` | Bounded phase task | `P03-T05` |
| `Pnn-AC-NNN` | Phase acceptance criterion | `P03-AC-006` |
| `Pnn-TST-NNN` | Planned/executed test scenario | `P04-TST-021` |
| `Pnn-EV-NNN` | Evidence artifact/index record | `P04-EV-004` |
| `APPR-Pnn-NNN` | Human approval request/gate | `APPR-P04-003` |
| `DEC-*` | Pending product/domain decision | `DEC-REG-002` |
| `RISK-NNN` / `ISSUE-NNN` | Canonical risk/issue | `RISK-053` |
| `ARCH-*`, `QUAL-*`, `DEP-*`, `REG-*`, `GOV-*` | Controlled supporting specification/control/evidence | `ARCH-PINT-AE-002` |

The `INVN-*` legacy product namespace covers both Procurement and Inventory requirements and is retained to avoid breaking references. New requirements should use an approved unambiguous namespace; do not silently rename existing IDs.

## 3. Definition and Reference Rules

1. One canonical owning document defines each ID; other documents reference it.
2. Repeated references are not duplicates. Two conflicting definitions are a defect.
3. Ranges such as `P03-TST-019–040` are compact catalogue references; individual executable tests receive concrete IDs in the implementation manifest before execution.
4. A module control cannot replace its product requirement; it refines it.
5. Evidence IDs identify artifacts, not claims. State is `PLANNED`, `NOT_RUN`, `PARTIAL`, `VERIFIED`, `FAILED`, `BLOCKED`, or an approved equivalent with evidence.
6. Approval IDs require approver role, decision, reviewed version/evidence, exact recording method and blocked scope.
7. Regulatory source IDs record dated evidence; they do not certify compliance.

## 4. Allocation

- Allocate the next unused numeric value in the owning register.
- Never fill a historical gap by reusing an ID.
- Reserve no unpublished blocks unless the register records owner and reason.
- Cross-phase controls retain their source requirement ID and are linked to multiple phases rather than cloned.
- A breaking semantic change creates a new requirement/decision and deprecates or supersedes the old one.

## 5. Validation

Documentation validation must check malformed IDs, duplicate canonical definitions, missing referenced paths, ADR file/register mismatch, noncanonical phase aliases, and evidence status without an artifact. Automated pattern checks supplement—not replace—semantic review.
