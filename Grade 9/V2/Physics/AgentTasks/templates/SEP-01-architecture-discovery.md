# EXECUTION PROMPT: Architecture Discovery Audit

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Reconstruct the current system architecture entirely from repository artifacts cold, without relying on conversational memory. Identify architectural contradictions, hidden case coupling, obsolete authorities, and missing production boundaries.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Treat current Draft 2020-12 schemas as normative contracts.
- Respect separation between canonical authoritative artifacts and diagnostic projections.
- Adhere to the established repository directory hierarchy.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Comprehensive cold audit of the repository directory tree, manifests, schemas, and engines.
- Identification of explicit authority chains: Manifest → Policy → Schema → Data → Engine → Test.
- Mapping of producer/consumer dependency graphs.
- Auditing diagnostic versus canonical boundaries.

## 6. Required Deliverables
1. Architectural discovery audit report in Markdown format.
2. Producer/Consumer dependency matrix.
3. Inventory of current Draft 2020-12 schemas and their domains.
4. Identification of deprecated/legacy artifacts and architectural gaps.
5. Standard Execution Report (Markdown + Machine JSON).

## 7. Allowed Changes
- Read-only analysis of repository artifacts.
- Writing audit report to declared output location.
- Tier: `DOC`.

## 8. Prohibited Changes
- NO modifications to canonical data, schemas, or engine code (`WRITE_MODE: ANALYZE_ONLY`).
- NO deletion or restructuring of repository files.
- NO assumption of authority based on resemblance to prior implementations.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Strictly repository-internal discovery; external web research is disallowed unless explicitly enabled in inputs.
- Secondary documentation loses if it contradicts machine schemas or code invariants.

## 11. Implementation Procedure
1. Execute the 10 cold-start discovery steps.
2. Map all active schemas under `contracts/`.
3. Trace data flow from producers to consumers.
4. Contrast documented intentions against executable test assertions.
5. Compile architecture findings and complete the execution report.

## 12. Mandatory Falsifiers
- Check for circular dependencies in authority chains.
- Check for undocumented file dependencies in pipeline scripts.
- Check for schema version mismatches across engines.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Validate all discovered schemas using `Draft202012Validator`.
- Execute relevant test suites to confirm discovered authority chains pass.

## 14. Acceptance Criteria
- Exact authority chain recovered without conversational hints.
- Complete producer/consumer graph established.
- All relevant schemas identified and categorized.
- Diagnostic vs canonical artifacts clearly distinguished.
- Current architectural gaps and case couplings identified.
- No memory dependency detected (`memory_dependency_detected: false`).

## 15. Stop / Block Conditions
- If core authority manifests are missing or irreconcilably contradict schemas, STOP and return `result: "BLOCKED"` with precise evidence.
- BLOCKED with documented receipts is a successful execution outcome. Never guess or fabricate authority.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
