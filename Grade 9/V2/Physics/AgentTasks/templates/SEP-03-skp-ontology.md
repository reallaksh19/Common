# EXECUTION PROMPT: SKP Ontology Design

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Define the normative semantic ontology of the Subtopic Knowledge Package (SKP). Establish clear mathematical, disciplinary, and pedagogical boundaries for all SKP entities, relations, and lifecycle stages without populating case-specific content.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Treat existing knowledge graphs and assessment registries as structural references.
- Preserve separation between core disciplinary truth and pedagogical delivery.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Define exact semantic boundaries for: topic, subtopic, capability, prerequisite, bridge, concept, relation, validity condition, reasoning sequence, inferential jump, representation, representation translation, learner conception, problem family, assessment binding, source plan, research overlay, maturity.
- Address mandatory adversarial design questions.
- Delineate common kernel ontology versus subject-adapter extensions.

## 6. Required Deliverables
1. Normative SKP Ontology Specification Document in Markdown.
2. Formal answers to mandatory adversarial design questions.
3. Extension-point specification for subject adapters (Physics, Math, Chemistry).
4. Standard Execution Report.

## 7. Allowed Changes
- Creation and modification of architectural design specifications under `DOC`.
- Tier: `DOC`.

## 8. Prohibited Changes
- NO schema modifications or code changes (`WRITE_MODE: ANALYZE_ONLY`).
- NO inclusion of case-specific subject data as global ontology definitions.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Grounding in learning sciences (Bloom, Gagné, Chi, diSessa), cognitive science (Cognitive Load Theory, Dual Coding Theory), and domain epistemology.

## 11. Implementation Procedure
1. Execute cold-start discovery steps.
2. Formulate explicit definitions and boundary conditions for each entity type.
3. Stress-test definitions against adversarial edge cases.
4. Establish clear rules for HARD vs BRIDGEABLE prerequisites.
5. Complete the execution report.

## 12. Mandatory Falsifiers
- Falsify capability splitting: provide formal criterion when one capability must be split into two.
- Falsify prerequisite equivalence: establish non-circular dependency criterion.
- Falsify representation role: prove whether a representation is an engineering requirement or pedagogical option.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Review specification against existing prerequisite graphs and registries.

## 14. Acceptance Criteria
- All 18 core ontological concepts exhaustively defined with inclusion/exclusion boundaries.
- All 8 adversarial questions answered with falsifiable criteria.
- Clear common kernel vs subject adapter boundary established.

## 15. Stop / Block Conditions
- If the ontology requires collapsing distinct disciplinary concepts into ambiguous generic labels, STOP and return `result: "BLOCKED"`.
- BLOCKED with evidence is a valid execution outcome.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
