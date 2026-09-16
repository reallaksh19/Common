# EXECUTION PROMPT: Chemistry Adapter

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Define, implement, and validate the Chemistry Disciplinary Adapter. Formalize Chemistry-specific extensions (Johnstone's macroscopic/submicroscopic/symbolic triad, chemical species, reaction conditions, stoichiometric relations, experimental observations, and mass/charge conservation) while ensuring the common SKP kernel is not diluted.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Extend generic SKP schemas via declared extension points without polluting the domain-neutral core.
- Strictly enforce Johnstone's Triad across chemical concepts.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Define Chemistry extension ontology: macroscopic observation, submicroscopic particulate model, symbolic formulation, chemical species, reaction condition, stoichiometric relation, mass/charge conservation, oxidation number state, thermodynamic potential, phase equilibrium.
- Define Chemistry representations: `ORBITAL_ENERGY_DIAGRAM`, `MOLECULAR_GEOMETRY_VSEPR`, `EQUILIBRIUM_CONCENTRATION_TABLE`, `THERMODYNAMIC_CYCLE_BORN_HABER`, `ORGANIC_REACTION_MECHANISM`, `PERIODIC_TREND_CONTOUR`, `LEWIS_DOT_STRUCTURE`, `REDOX_HALF_REACTION_LANE`.
- Implement conservation and oxidation state balancing validators.

## 6. Required Deliverables
1. `subject-profiles/chemistry.json` updated with formal ontology and validation rules.
2. Chemistry adapter validator module.
3. Golden chemistry test cases (e.g. Redox Reactions, Atomic Structure, Chemical Bonding).
4. Standard Execution Report.

## 7. Allowed Changes
- Creation of chemistry adapter profiles, schemas, and validators under `General/` or declared adapter locations.
- Tiers: `SUBJECT_ADAPTER`, `TEST`, `DOC`.

## 8. Prohibited Changes
- NO touching or modifying `Grade 9/V2/Mathematics/` or `Grade 9/V2/Chemistry/` production directories.
- NO relaxing of mass and charge conservation laws.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Standard chemistry authorities (IUPAC Gold Book, NCERT Chemistry Grades 9-11, Atkins Physical Chemistry).

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Formulate chemistry adapter schemas and conservation invariants.
3. Implement atom ledger and charge balance validation functions.
4. Run tests on sample chemistry topics.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Falsify unbalanced reaction equation (reactant atom count != product atom count).
- Falsify net charge imbalance.
- Falsify ungrounded oxidation numbers violating sum-to-net-charge rule.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Execute Chemistry adapter test battery.

## 14. Acceptance Criteria
- All 10 chemistry extension concepts formally specified.
- Pre-render visual validators functional for all 8 chemistry representations.
- Zero dilution of the common SKP core.

## 15. Stop / Block Conditions
- If the schema system cannot support the Johnstone Triad without corrupting generic domain models, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
