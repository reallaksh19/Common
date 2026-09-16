# EXECUTION PROMPT: Independent Reproduction

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Independently reproduce the candidate Subtopic Knowledge Package (SKP) for the specified subtopic from cold repository truth and official sources, without access to prior agent outputs, conversation transcripts, or memory.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Do not read or inspect existing candidate artifacts for the target subtopic.
- Build independently from primary sources and schemas.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Execute independent cold discovery of the subtopic.
- Author an independent candidate SKP package from scratch.
- Derive independent capabilities, prerequisite edges, representations, and problem families.
- Output candidate package to isolated reproduction directory.

## 6. Required Deliverables
1. Independent Candidate SKP JSON package.
2. Independent Source Quotations Ledger.
3. Independent Reasoning Sequences and Falsifiers.
4. Standard Execution Report.

## 7. Allowed Changes
- Writing only to designated reproduction sandbox directories (`WRITE_MODE: IMPLEMENT`).
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO reading or diffing against prior agent branches or candidate outputs.
- NO modifying canonical files.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Primary textbooks and board curricula as specified in task inputs.

## 11. Implementation Procedure
1. Execute cold-start discovery without consulting prior agent branches.
2. Construct independent candidate knowledge package.
3. Validate against schemas.
4. Execute test falsifiers.
5. Compile completion report with strict no-memory declaration.

## 12. Mandatory Falsifiers
- Digest assertion: ensure output was compiled fresh and not copied from existing paths.
- Self-consistency checks across declared capabilities and problem families.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Schema validation of independent package.

## 14. Acceptance Criteria
- Fully formed candidate SKP produced in isolation.
- Complete independence from prior agent runs verified.

## 15. Stop / Block Conditions
- If isolation cannot be maintained or prior artifacts are accidentally ingested, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
