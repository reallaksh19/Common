# EXECUTION PROMPT: Library Coverage Audit

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Audit the entire curriculum library for the designated grade and subject to identify missing, partial, outdated, or stale Subtopic Knowledge Packages. Reconcile current coverage against official syllabus specifications.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Rely on official curriculum manifests and syllabus documents as coverage benchmarks.
- Respect maturity levels: CANDIDATE, VALIDATED, RETIRED.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Inventory all existing subtopic packages in the repository.
- Compare against official syllabus topic lists (CBSE, JEE Main, JEE Advanced).
- Classify each syllabus subtopic as: COMPLETE, PARTIAL, MISSING, or STALE.
- Flag packages with outdated schemas or broken prerequisite links.

## 6. Required Deliverables
1. Comprehensive Library Coverage Matrix JSON.
2. Coverage Gap Analysis Report in Markdown.
3. Recommended Prioritized Backlog of missing SKPs.
4. Standard Execution Report.

## 7. Allowed Changes
- Read-only audit and report generation (`WRITE_MODE: ANALYZE_ONLY`).
- Tier: `DOC`.

## 8. Prohibited Changes
- NO modification of existing packages or schemas.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Official CBSE and JEE syllabi.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Extract required subtopic list from syllabus authority.
3. Scan repository for corresponding SKP packages and evaluate maturity.
4. Compile coverage statistics and gap analysis.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Falsify false completeness: ensure packages missing gates are marked PARTIAL, not COMPLETE.
- Falsify unmapped packages: ensure every repository package maps to syllabus or is flagged as orphan.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Validate generated coverage JSON against schema.

## 14. Acceptance Criteria
- Complete coverage percentage calculated across all curriculum tiers.
- Exact gap inventory produced.

## 15. Stop / Block Conditions
- If official syllabus documents cannot be located, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
