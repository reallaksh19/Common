# EXECUTION PROMPT: Problem-Family Miner

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Derive and classify candidate problem families for the target subtopic. Define parameter spaces, canonical solution trajectories, boundary limiting conditions, and transfer difficulty levels across competitive tiers (Foundation, Standard, Advanced).

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Conform to the Problem Semantics and Problem Family contracts.
- Maintain parameter independence and explicit mathematical constraints.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Identify canonical problem archetypes for the subtopic.
- Formulate mathematical parameter spaces (ranges, units, boundary points).
- Specify reasoning sequences and multi-step solution paths.
- Classify difficulty: CBSE Direct Formula, JEE Main Multi-Step, JEE Advanced Edge Condition.

## 6. Required Deliverables
1. Candidate Problem Families JSON conforming to `problem-family.schema.json`.
2. Worked exemplar solutions with explicit reasoning sequences.
3. Limiting-case verification proofs.
4. Standard Execution Report.

## 7. Allowed Changes
- Adding problem family data to candidate directories.
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO modification of generic problem engines or schemas.
- NO unverified solutions or unconstrained parameter intervals.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Standard competition problem archives (JEE Advanced archive, Irodov, Krotov, Olympiad benchmarks).

## 11. Implementation Procedure
1. Execute cold-start discovery.
2. Formulate problem family schemas and constraints.
3. Validate parameter intervals against physical/mathematical domain limits.
4. Execute limiting case tests on exemplar solutions.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Falsify negative or unphysical parameter domains (e.g. negative absolute temperature, negative mass).
- Falsify dimensional consistency of derived problem answers.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Schema validation of candidate problem families.

## 14. Acceptance Criteria
- At least 3 canonical problem families defined per tier.
- Complete parameter boundaries and worked steps documented.

## 15. Stop / Block Conditions
- If problem family solutions lack formal mathematical closed forms or proofs, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
