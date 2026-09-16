# EXECUTION PROMPT: Core Architecture Document

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Synthesize, verify, and update the normative system manual `V2_LEARNING_ENGINEERING_ARCHITECTURE.md` entirely from current repository ground truth and active schemas. Discover schemas and contracts dynamically; never copy stale documentation. In any conflict, machine schemas override documentation.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Machine schemas (`contracts/*.schema.json`) are strictly normative over descriptive prose.
- Where documentation and code/schemas disagree, document the mismatch and rule in favor of schemas.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Reconstruct the comprehensive system manual covering all 21 mandatory sections:
  1. Mission
  2. Authority Hierarchy
  3. Architecture & Data Flow
  4. Schema Registry Inventory
  5. Subtopic Knowledge Package (SKP)
  6. Technical Engineering Gate Registry
  7. Readiness Architecture
  8. Learning Blueprint & Core Composition
  9. Learner Adaptation & Cognitive State
  10. Research Depth (Foundation/Standard/Research)
  11. Source Governance & Provenance
  12. Question Corpus & Problem Families
  13. Subject Adapters (Physics, Mathematics, Chemistry)
  14. Verification & Testing Infrastructure
  15. Agent Cold-Start Protocol & Standalone Execution Prompts
  16. Versioning & Immutability Custody
  17. Known Limitations
  18. Known Issues
  19. Roadmap
  20. Scalability & Modularity Analysis
  21. Definition of Completion

## 6. Required Deliverables
1. Updated `V2_LEARNING_ENGINEERING_ARCHITECTURE.md`.
2. Documentation-Schema Mismatch Audit Log.
3. Standard Execution Report.

## 7. Allowed Changes
- Updating architecture manual and documentation logs.
- Tier: `DOC`.

## 8. Prohibited Changes
- NO changing schemas or engines to match obsolete documentation.
- NO copying unverified architectural assertions from conversational prompts.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Ground truth from repository code, Draft 2020-12 schemas, and executable tests.

## 11. Implementation Procedure
1. Execute cold-start discovery across the entire repository.
2. Inventory all active schemas, engines, and test suites.
3. Check for mismatches between current implementation and existing docs.
4. Author updated architecture manual.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Falsify stale schema list: assert that every schema listed in the document exists on disk.
- Falsify broken links: assert all file links resolve correctly.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Validate markdown link integrity and syntax.

## 14. Acceptance Criteria
- All 21 required sections comprehensively authored from discovered repository truth.
- All documented schemas match disk state.
- Documentation-versus-code mismatches explicitly cataloged.

## 15. Stop / Block Conditions
- If core architecture contracts are contradictory and prevent unambiguous documentation, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
