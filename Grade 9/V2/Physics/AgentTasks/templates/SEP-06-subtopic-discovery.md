# EXECUTION PROMPT: Subtopic Discovery

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Conduct broad preliminary research to discover and map the candidate scope, conceptual landscape, representations, and prerequisite relationships for the target subtopic without promoting any artifacts to canonical status.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Output must remain designated as diagnostic or candidate research.
- Do not modify existing canonical registries.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Survey candidate concepts, laws, definitions, and representations for the target topic and subtopic.
- Identify preliminary candidate prerequisites and problem archetypes.
- Delineate board syllabus boundaries versus competitive extensions.

## 6. Required Deliverables
1. Candidate Subtopic Research Dossier in Markdown.
2. Candidate concept and representation mapping.
3. Candidate source citations ledger.
4. Standard Execution Report.

## 7. Allowed Changes
- Creating research notes in designated diagnostic directories.
- Tier: `DOC`.

## 8. Prohibited Changes
- NO writes to canonical knowledge directories (`WRITE_MODE: ANALYZE_ONLY`).
- NO promotion of candidate data to production blueprints.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Use authorized curriculum textbooks and peer-reviewed educational research.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Extract candidate concepts and relationships from primary sources.
3. Synthesize candidate findings into the dossier.
4. Complete the execution report with no-memory declaration.

## 12. Mandatory Falsifiers
- Check for scope creep beyond declared topic boundaries.
- Flag any claims lacking primary or secondary source citations.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Validate markdown links and structure.

## 14. Acceptance Criteria
- Comprehensive survey produced without mutating repository canonical state.
- Clear separation between candidate findings and canonical truth.

## 15. Stop / Block Conditions
- If primary sources are inaccessible or contradictory without resolution, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
