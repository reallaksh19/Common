# EXECUTION PROMPT: Subtopic Engineering Build

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Execute the full engineering build for the specified subtopic: discover existing authorities, reconcile curriculum scope, construct candidate Subtopic Knowledge Package (SKP) data, compile prerequisite closures, compile Technical Engineering Gates, compile Readiness artifacts, and execute the complete falsifier battery.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Respect existing Technical Engineering Gate Registry schemas and invariants.
- Build subtopic content strictly within governed data files without hardcoding case logic in shared engines.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Reconcile subtopic curriculum scope against declared board and competitive frameworks.
- Construct candidate SKP JSON package (capabilities, relations, representations, problem families, misconceptions).
- Compile prerequisite closure and verify acyclicity.
- Compile and bind Technical Engineering Gate.
- Run comprehensive validation falsifiers.

## 6. Required Deliverables
1. Validated Subtopic Knowledge Package JSON.
2. Technical Engineering Gate entry and registry binding.
3. Prerequisite closure verification artifact.
4. Falsifier execution log.
5. Standard Execution Report (Markdown + Machine JSON).

## 7. Allowed Changes
- Primarily: `DATA_ONLY`.
- Permitted if formally justified: `SCHEMA_EXTENSION`, `SUBJECT_ADAPTER_CHANGE`.
- Rare and suspicious: `GENERIC_ENGINE_CHANGE`.

## 8. Prohibited Changes
- FORBIDDEN without explicit architectural exemption: `BLUEPRINT_CHANGE`.
- If a Blueprint change is contemplated, STOP immediately and output a new-invariant justification document before making any changes.
- NO hardcoded topic branches in shared engines.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Strictly adhere to approved primary curriculum standards and secondary benchmark textbooks.
- Every capability must link to a valid source citation in the source ledger.

## 11. Implementation Procedure
1. Execute cold-start repository discovery.
2. Construct candidate SKP data adhering to `skp.schema.json`.
3. Compute and compile prerequisite closure.
4. Integrate entry into Technical Engineering Gate Registry.
5. Execute full falsifier battery and regression tests.
6. Verify no memory dependency and compile execution report.

## 12. Mandatory Falsifiers
- Prerequisite cycle check (must be acyclic DAG).
- ID uniqueness and reference resolution across all entities.
- Limiting-case mathematical checks for declared formulas.
- Falsify with mutated content to verify digest sensitivity.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Run all subject-specific contract tests and gate tests.
- Verify schema validation with `Draft202012Validator`.

## 14. Acceptance Criteria
- Candidate SKP validates against schema with 0 errors.
- Prerequisite closure is closed and acyclic.
- Technical Engineering Gate passes all 16 technical criteria.
- 100% of falsifier tests pass.
- Changes are strictly `DATA_ONLY` (or justified extensions).

## 15. Stop / Block Conditions
- If constructing the subtopic requires adding conditional branches (`if topic == '...'`) to the generic Blueprint, STOP and return `result: "BLOCKED"`.
- BLOCKED with evidence is a successful outcome. Never hack the engine to pass a subtopic.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
