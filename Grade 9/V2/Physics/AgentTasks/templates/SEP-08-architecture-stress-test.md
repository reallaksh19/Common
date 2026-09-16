# EXECUTION PROMPT: Architecture Stress Test

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Execute a cold-start architecture stress test by taking a standard new subtopic and proving that it can be completely integrated, compiled, and validated without modifying any Blueprint or generic engine code.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- The generic Blueprint and execution pipeline are immutable for this run.
- All adaptation must occur through governed data packages and declared adapter extension points.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Cold ingest of the target subtopic parameters.
- Construction and validation of the subtopic knowledge package.
- Verification that zero lines of Blueprint code were modified or required.
- Verification that all gates and falsifiers pass.

## 6. Required Deliverables
1. Subtopic knowledge package data files (`DATA_ONLY`).
2. Architecture Stress Test Report proving zero Blueprint edits.
3. Falsifier execution log.
4. Standard Execution Report.

## 7. Allowed Changes
- STRICTLY `DATA_ONLY` changes.
- Tier: `DATA_ONLY`.

## 8. Prohibited Changes
- ABSOLUTELY PROHIBITED: Any change to `Blueprint/` or core compilation engines.
- NO hardcoded topic checks or special-case heuristics.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Rely solely on declared repository schemas, source ledgers, and subject profile contracts.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Build candidate data package for the target subtopic.
3. Run complete test and gate verification pipeline.
4. Verify `git diff` confirms zero edits outside data directories.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Git diff assertion: `git diff --name-only | grep -E "Blueprint|engine"` must return empty.
- Subtopic gate execution must pass with exit code 0.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Execute subtopic-specific gate test battery.
- Run generic regression test suite to ensure zero regressions.

## 14. Acceptance Criteria
- Full subtopic functionality demonstrated.
- Zero Blueprint modifications (`changed_files` contains only `DATA_ONLY` entries).
- All tests pass with documented evidence.

## 15. Stop / Block Conditions
- If subtopic requirements cannot be satisfied without editing the Blueprint, STOP immediately and return `result: "BLOCKED"` detailing the exact architectural failure.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
