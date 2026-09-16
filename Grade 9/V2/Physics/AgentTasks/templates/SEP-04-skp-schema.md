# EXECUTION PROMPT: SKP Schema Implementation

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Implement the modular Draft 2020-12 JSON schemas and executable validator falsifiers for the Subtopic Knowledge Package (SKP) architecture based on the approved ontology.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Use strict JSON Schema Draft 2020-12.
- Set `additionalProperties: false` on all closed objects.
- Preserve domain neutrality in common schemas; support discipline-specific attributes via declared extension points.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Implement modular schemas: `skp.schema.json`, `capability.schema.json`, `prerequisite-edge.schema.json`, `relation.schema.json`, `reasoning-sequence.schema.json`, `representation.schema.json`, `learner-conception.schema.json`, `problem-family.schema.json`.
- Implement validator battery testing the 11 mandatory test categories.

## 6. Required Deliverables
1. Modular Draft 2020-12 JSON schema suite.
2. Python schema validator and graph integrity checker.
3. Complete battery of positive golden fixtures and negative falsifier fixtures.
4. Standard Execution Report.

## 7. Allowed Changes
- Creation of schemas under contracts, test fixtures, and validation scripts.
- Tiers: `SCHEMA`, `TEST`, `DOC`.

## 8. Prohibited Changes
- NO subject-specific hardcoding (e.g. "kinematics", "moles", "polynomial") in common schemas.
- NO permissive schemas allowing open undeclared fields.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- JSON Schema Draft 2020-12 normative specification.

## 11. Implementation Procedure
1. Execute cold-start discovery steps.
2. Write modular schemas with explicit `$id` and `$ref` bindings.
3. Implement graph validation (cycle detection, unowned prerequisite detection).
4. Implement falsifier tests covering all 11 failure categories.
5. Run full test suite and compile report.

## 12. Mandatory Falsifiers
Must implement and pass test fixtures for:
1. `valid_minimal`
2. `valid_rich`
3. `not_applicable_handling`
4. `missing_required_rationale`
5. `duplicate_ids`
6. `broken_references`
7. `dependency_cycle`
8. `same_id_mutated_content`
9. `invalid_evidence_class`
10. `unowned_external_prerequisite`
11. `unsupported_source_promotion`
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Run `python -m unittest` on schema test suite.
- Run `validate_contracts.py`.

## 14. Acceptance Criteria
- 100% of positive golden fixtures validate.
- 100% of negative falsifier fixtures are rejected with precise error codes.
- Zero discipline-specific vocabulary in root common schemas.

## 15. Stop / Block Conditions
- If modular schema composition creates circular `$ref` resolution failures in standard tooling, STOP and return `result: "BLOCKED"`.
- BLOCKED with evidence is a valid execution outcome.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
