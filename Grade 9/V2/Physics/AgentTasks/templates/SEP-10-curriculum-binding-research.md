# EXECUTION PROMPT: Curriculum Binding Research

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Establish the authoritative curriculum scope for the target subtopic across designated boards and competitive exams (e.g. CBSE, JEE Main, JEE Advanced). Classify all candidate concepts into the standardized scope taxonomy without modifying any Subtopic Knowledge Packages.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Rely exclusively on official board syllabi and official exam brochures.
- Strictly adhere to the scope taxonomy.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Survey official board syllabus (CBSE/ICSE) and competitive guidelines (JEE/NEET/IOQM).
- Classify each candidate concept into:
  - `REQUIRED`: Explicitly mandated by core board syllabus.
  - `DERIVED`: Naturally implied or mathematically necessary deduction from core syllabus.
  - `BRIDGE`: Essential pedagogical scaffolding required to access target concepts.
  - `COMPETITIVE_EXTENSION`: Standard requirement for JEE Main / NEET beyond board syllabus.
  - `RESEARCH_EXTENSION`: Advanced material relevant for JEE Advanced / Olympiad.
  - `OUT_OF_SCOPE`: Explicitly excluded concepts to prevent scope drift.
  - `UNRESOLVED`: Borderline items requiring explicit owner guidance.

## 6. Required Deliverables
1. Machine-readable Curriculum Scope Classification JSON.
2. Curriculum Reconciliation Report in Markdown.
3. Citation receipts linking classifications to official syllabus documents.
4. Standard Execution Report.

## 7. Allowed Changes
- Creating scope classification data and reports.
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO editing of SKP files, engines, or schemas (`WRITE_MODE: ANALYZE_ONLY`).
- NO speculative inclusion of unverified topics as REQUIRED.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Primary authorities: Official NCERT / CBSE curriculum documents, NTA JEE Information Bulletins, IIT JEE syllabi.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Extract official syllabus statements for the topic and subtopic.
3. Apply classification rules to candidate concepts.
4. Validate coverage and completeness.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Falsify misclassification: verify that OUT_OF_SCOPE items are not categorized as REQUIRED.
- Verify that every REQUIRED item has an exact syllabus text quotation.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Schema validation of scope classification output.

## 14. Acceptance Criteria
- 100% of candidate concepts mapped to one of the 7 taxonomy categories.
- Zero ambiguous classifications; all items have documented rationale.

## 15. Stop / Block Conditions
- If official syllabus documents for the specified curriculum year are unavailable, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
