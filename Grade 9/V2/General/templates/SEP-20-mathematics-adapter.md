# EXECUTION PROMPT: Mathematics Adapter

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Define, implement, and validate the Mathematics Disciplinary Adapter. Formalize Mathematics-specific extensions (definitions, objects, axioms, theorems, proof dependencies, geometric constructions, counterexamples, canonical procedures, and proof families) while proving that Physics-only concepts (e.g. mass, dimensions, physical reference frames) are cleanly excluded.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Extend generic SKP schemas via declared extension points without polluting the domain-neutral core.
- Ensure strict acyclicity of theorem proof dependencies.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Define Mathematics extension ontology: mathematical definition, mathematical object, axiom/postulate, formal theorem, proof dependency edge, geometric construction, counterexample, canonical procedure, proof family, existence/uniqueness condition.
- Define Mathematics representations: `COORDINATE_GEOMETRY_PLOT`, `NUMBER_LINE_INTERVAL`, `POLYGON_CONSTRUCTION`, `FUNCTION_GRAPH_TRANSFORMATION`, `VENN_EULER_DIAGRAM`, `TRIGONOMETRIC_UNIT_CIRCLE`.
- Identify and exclude irrelevant physical concepts (e.g. dimensions, velocity, forces).

## 6. Required Deliverables
1. `subject-profiles/mathematics.json` updated with formal ontology.
2. Mathematics adapter validator module.
3. Golden mathematics test cases (e.g. Euclidean Geometry, Quadratic Equations, Trigonometric Identities).
4. Standard Execution Report.

## 7. Allowed Changes
- Creation of mathematics adapter profiles, schemas, and validators under `General/` or declared adapter locations.
- Tiers: `SUBJECT_ADAPTER`, `TEST`, `DOC`.

## 8. Prohibited Changes
- NO touching or modifying `Grade 9/V2/Mathematics/` or `Grade 9/V2/Chemistry/` production directories.
- NO relaxing of deductive proof requirements into empirical/heuristic verification.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Axiomatic mathematics standards (Euclid's Elements, Polya, NCERT Mathematics Grades 9-11, Olympiad IOQM curricula).

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Formulate mathematics adapter schemas and proof dependency rules.
3. Implement proof graph acyclicity and domain validity validators.
4. Run tests on sample mathematical topics.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Falsify circular theorem dependency (e.g. Theorem A requires B, Theorem B requires A).
- Falsify domain violations (e.g. undefined operations, division by zero).
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Execute Mathematics adapter test battery.

## 14. Acceptance Criteria
- All 10 mathematics extension concepts formally specified.
- Deductive proof structures validated without physics assumptions.

## 15. Stop / Block Conditions
- If the schema forces mathematics to declare meaningless physical attributes (like dimensions or units), STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
