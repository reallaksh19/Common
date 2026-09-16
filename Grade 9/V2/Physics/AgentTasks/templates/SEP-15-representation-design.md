# EXECUTION PROMPT: Representation Design

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Design, evaluate, and formally select the canonical representations and representation-translation paths for the target subtopic. Produce formal comparison receipts documenting cognitive load, pedagogical trade-offs, and pre-render validation rules.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Respect existing MasterTemplates visual primitives and validation gates.
- Conform strictly to `representation.schema.json`.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Inventory candidate visual, mathematical, and diagrammatic representations for the subtopic.
- Formulate representation-translation pairs (e.g. Kinematic Graph <-> Vector Diagram <-> Algebraic Equation).
- Establish pre-render mathematical validation gates (Gate 1 through Gate 10 standards).
- Document design decision receipts for chosen versus rejected representations.

## 6. Required Deliverables
1. Canonical Representation Specifications JSON.
2. Representation Translation Matrix JSON.
3. Decision Receipts Document in Markdown.
4. Pre-render Validation Criteria and Falsifiers.
5. Standard Execution Report.

## 7. Allowed Changes
- Adding representation specifications to candidate directories.
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO bypass of quantitative pre-render validation checks.
- NO ungrounded decorative visual elements lacking pedagogical function.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Grounding in Dual Coding Theory (Paivio), Mayer's Multimedia Learning Principles, and disciplinary visual conventions.

## 11. Implementation Procedure
1. Execute cold-start discovery.
2. Model candidate representations with exact coordinates, parameters, and labels.
3. Formulate bidirectional translation paths between representations.
4. Write pre-render validation functions.
5. Compile execution report.

## 12. Mandatory Falsifiers
- Falsify visual-numerical discrepancy (assert graph curves match underlying equation values to 1e-4).
- Falsify directional inversions (e.g. vector arrows pointing opposite to calculated velocity).
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Execute visual semantic validator test suite.

## 14. Acceptance Criteria
- Complete mathematical specification of all visual primitives.
- All representation translation paths have bidirectional verification rules.

## 15. Stop / Block Conditions
- If a chosen representation lacks deterministic pre-render validation gates, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
