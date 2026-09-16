# EXECUTION PROMPT: Physics Adapter

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Define, implement, and validate the Physics Disciplinary Adapter. Formalize Physics-specific extensions (physical models, reference frames, quantities, dimensions, laws, equations, boundary/limiting cases, and experimental verification) while maintaining clean decoupling from the generic SKP kernel.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Extend generic SKP schemas via declared extension points without polluting the domain-neutral core.
- Conform to Grade 9-11 Physics Technical Engineering Gate Registry standards.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Define Physics extension ontology: physical model, reference frame, physical quantity, dimensional formula, fundamental law, governing equation, boundary condition, limiting case, experimental verification.
- Implement Physics-specific validation rules (e.g. dimensional homogeneity, Galilean frame transformations, pseudo-force declarations).
- Implement representations: `KINEMATIC_GRAPH_PLOT`, `FREE_BODY_DIAGRAM`, `VECTOR_POLYGON_DIAGRAM`, `RAY_OPTICS_DIAGRAM`, `CIRCUIT_SCHEMATIC`, `THERMODYNAMIC_PV_CYCLE`, `WAVE_OSCILLATION_PLOT`, `FIELD_LINE_EQUIPOTENTIAL_MAP`.

## 6. Required Deliverables
1. `subject-profiles/physics.json` updated with complete ontology and validation rules.
2. Physics adapter validator module.
3. Golden physics test cases (e.g. Kinematics, Gravitation, Newton's Laws).
4. Standard Execution Report.

## 7. Allowed Changes
- Creation of physics adapter profiles, schemas, and validators.
- Tiers: `SUBJECT_ADAPTER`, `TEST`, `DOC`.

## 8. Prohibited Changes
- NO hardcoding physics concepts into core generic schemas or engines.
- NO relaxing of dimensional or physical conservation invariants.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Standard university and secondary physics references (Halliday-Resnick-Walker, Irodov, Feynman Lectures, NCERT Physics Grades 9-11).

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Formulate physics adapter schema extensions.
3. Implement dimensional analysis and frame transformation validators.
4. Execute test suite on sample physics subtopics.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Falsify dimensional inhomogeneity (e.g. adding velocity to acceleration).
- Falsify non-inertial frame calculation missing pseudo-force term.
- Falsify negative kinetic energy or unphysical mass.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Run Physics adapter test suite and contract validation.

## 14. Acceptance Criteria
- All 10 physics extension concepts formally specified.
- Pre-render visual validators functional for all 8 physics representations.
- Zero generic kernel pollution.

## 15. Stop / Block Conditions
- If the generic SKP kernel cannot accommodate physics concepts without modifying base schemas, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
