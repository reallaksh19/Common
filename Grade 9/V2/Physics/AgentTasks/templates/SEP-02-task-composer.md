# EXECUTION PROMPT: Task Composer Implementation

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Implement the Task Composer toolchain (CLI compiler, schema validator, and interactive web interface) to generate, validate, and serialize Standalone Execution Prompts deterministically without subject-case logic hardcoded in the engine.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Build upon existing Draft 2020-12 schema infrastructure.
- Adhere to the established repository directory hierarchy.
- Decouple generic engine logic from subject-matter knowledge packages.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Validate input payloads against `execution-task.schema.json`.
- Implement CLI compilation engine `compile_execution_prompt.py`.
- Implement report validation engine `validate_execution_report.py`.
- Build lightweight interactive web UI (pure HTML/JS or lightweight frontend) for composing task parameters and downloading compiled standalone prompts.
- Implement golden and negative test fixtures.

## 6. Required Deliverables
1. `contracts/execution-task.schema.json` and `contracts/execution-report.schema.json`.
2. Python compilation engine: `engine/compile_execution_prompt.py`.
3. Python validation engine: `engine/validate_execution_report.py`.
4. Web UI task composer interface.
5. Unit and regression test suite `tests/test_agent_tasks_engine.py`.
6. Golden compiled prompt fixtures and negative error fixtures.
7. Standard Execution Report.

## 7. Allowed Changes
- Creation of engine scripts, schemas, templates, invariants, and test suites.
- Tiers: `SCHEMA`, `GENERIC_ENGINE`, `TEST`, `DOC`.

## 8. Prohibited Changes
- NO hardcoded subject-specific or topic-specific branching in UI or compiler engine.
- NO alteration of existing production blueprints or learner runtime pipelines.
- NO dependency on external node_modules or unvetted binary dependencies.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Standard library Python 3.10+ and standard browser ECMAScript for UI.
- All template composition rules must be fully specified in markdown and schema contracts.

## 11. Implementation Procedure
1. Verify contract schemas against Draft 2020-12.
2. Implement compiler with SHA-256 digest calculation, placeholder replacement, and anti-leak linter.
3. Implement validator verifying report schema and BLOCKED outcome reasons.
4. Implement web UI using clean vanilla HTML/CSS/JavaScript with client-side validation against schema.
5. Run test suite verifying byte-deterministic equivalence between CLI and web compilation.

## 12. Mandatory Falsifiers
- Falsify compilation with missing required schema fields (must exit non-zero).
- Falsify compilation with unexpanded template variables (must fail linter).
- Falsify compilation with leaked case literals (e.g. topic codes appearing in generic templates).
- Verify byte-equivalent output across multiple runs with identical inputs.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Run `python -m unittest` on `tests/test_agent_tasks_engine.py`.
- Run contract validator on all schema files.

## 14. Acceptance Criteria
- Multi-subject test tasks across Physics, Mathematics, and Chemistry compile deterministically without code modifications.
- Prompt digests are SHA-256 reproducible.
- Zero unhandled exceptions on invalid inputs.

## 15. Stop / Block Conditions
- If the schema system cannot support required disciplinary extensions without adding case branches in the compiler engine, STOP and return `result: "BLOCKED"`.
- BLOCKED with evidence is a valid execution outcome.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
