# EXECUTION PROMPT: Source Governance

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Establish the normative Source Governance framework, source-selection policy, and machine-readable source-ledger schema to govern all empirical and academic citations across knowledge packages.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Respect existing authority tiers: primary curriculum benchmarks override secondary textbooks; peer-reviewed pedagogical literature overrides informal blogs.
- Maintain tamper-evident hash custody of cited sources.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Define normative semantics for: source intent, authority tier, selection reason, claims supported, limitations, population/context, freshness, curriculum version, licensing, corroboration, conflict handling, supersession.
- Produce `source-ledger.schema.json`.
- Author `source-selection-policy.md`.

## 6. Required Deliverables
1. `source-selection-policy.md` defining selection criteria and conflict resolution algorithms.
2. `contracts/source-ledger.schema.json` in Draft 2020-12.
3. Source ledger validation script.
4. Positive and negative test fixtures.
5. Standard Execution Report.

## 7. Allowed Changes
- Creation of policy documents, schemas, and validators.
- Tiers: `POLICY`, `SCHEMA`, `TEST`, `DOC`.

## 8. Prohibited Changes
- NO retroactive modification of historical source hashes or citations.
- NO automatic promotion of lower-tier sources to override primary curriculum authorities.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Primary sources: Official curriculum frameworks (NCERT, CBSE, JEE Advanced Information Brochure).
- Secondary sources: Standard textbooks (Halliday-Resnick-Walker, Irodov, Krotov, NCERT exemplar).
- Tertiary sources: Peer-reviewed PER (Physics Education Research) / CER / MER literature.

## 11. Implementation Procedure
1. Execute cold-start discovery steps.
2. Draft normative source selection policy with tiered hierarchy.
3. Implement `source-ledger.schema.json` with strict validation of metadata.
4. Implement automated integrity and freshness checks.
5. Validate against test cases and compile completion report.

## 12. Mandatory Falsifiers
- Falsify uncorroborated claim promotion.
- Falsify missing license or rights assertion.
- Falsify circular citation dependencies.
- Falsify supersession violations (using superseded edition when newer edition revokes claim).
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Validate schema with `Draft202012Validator`.
- Run source ledger validator on test fixtures.

## 14. Acceptance Criteria
- All 12 source attributes formally specified.
- Clear deterministic algorithm for resolving contradictory claims between sources.
- Complete Draft 2020-12 schema with zero schema lint errors.

## 15. Stop / Block Conditions
- If source copyright or provenance cannot be established for critical base claims, STOP and return `result: "BLOCKED"`.
- BLOCKED with evidence is a valid execution outcome.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
