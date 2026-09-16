# EXECUTION PROMPT: Prerequisite Graph Audit

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Audit the complete prerequisite graph for the designated subtopic across internal capabilities and external subject domains. Prove graph acyclicity, classify edges as HARD vs BRIDGEABLE, and detect unowned external prerequisites.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Respect cross-domain dependency contracts.
- Graph must be a strictly acyclic Directed Acyclic Graph (DAG).
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Trace prerequisite closure for all capabilities in the subtopic.
- Classify prerequisite edges into HARD (strictly unbridgeable within session) versus BRIDGEABLE (bridgeable with micro-learning scaffold).
- Audit cross-domain edges (e.g. Physics depending on Mathematics Vector Algebra).
- Run cycle-detection and reachability analysis.

## 6. Required Deliverables
1. Prerequisite Graph Audit Report in Markdown.
2. Machine-readable Prerequisite Closure JSON.
3. Cycle detection and topological sort receipts.
4. Unowned or dangling prerequisite alerts.
5. Standard Execution Report.

## 7. Allowed Changes
- Read-only audit and generation of prerequisite verification artifacts.
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO deleting prerequisites to artificially bypass prerequisite closures.
- NO unowned external dependencies lacking cross-domain provider contracts.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Strictly repository authority and governing curriculum sequence documents.

## 11. Implementation Procedure
1. Execute cold-start discovery.
2. Ingest all prerequisite edges from candidate SKP and cross-domain registries.
3. Execute Tarjan's or Kahn's topological sort algorithm to verify DAG property.
4. Check reachability and verify that every external prerequisite resolves to a valid provider.
5. Compile execution report.

## 12. Mandatory Falsifiers
- Falsify cyclic graph: inject synthetic back-edge and verify detection.
- Falsify dangling node: inject unknown prerequisite ID and verify detection.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Execute graph closure validator test script.

## 14. Acceptance Criteria
- 100% acyclic prerequisite closure verified.
- All edges categorized as HARD or BRIDGEABLE.
- Zero dangling or unowned cross-domain references.

## 15. Stop / Block Conditions
- If a dependency cycle is discovered in canonical data, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
