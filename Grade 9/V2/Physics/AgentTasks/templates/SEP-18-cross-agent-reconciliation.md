# EXECUTION PROMPT: Cross-Agent Reconciliation

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Reconcile independent candidate subtopic packages (e.g. Candidate A, B, C) produced by different agents. Structurally classify all points of agreement and disagreement. NEVER resolve domain truth conflicts through majority voting.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Authority derives from schemas, verified sources, and disciplinary invariants—not agent consensus.
- A claim agreed upon by multiple agents remains invalid if unsupported by primary evidence.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Ingest candidate packages A, B, C.
- Compare across: scope, capabilities, prerequisites, relations, validity conditions, sources, problem families, representations.
- Classify disagreements into 10 standard categories:
  - `PURE_WORDING`: Syntactic difference with identical semantics.
  - `ALIAS`: Different naming for identical conceptual entity.
  - `GRANULARITY_DIFFERENCE`: One agent bundled where another split.
  - `SCOPE_DIFFERENCE`: Disagreement on curriculum boundaries.
  - `PREREQUISITE_CONFLICT`: Disagreement on prerequisite edges or HARD/BRIDGEABLE classification.
  - `DOMAIN_TRUTH_CONFLICT`: Contradictory physical/mathematical assertions.
  - `SOURCE_CONFLICT`: Divergent claims based on different source editions.
  - `PEDAGOGICAL_CHOICE`: Alternative valid pedagogical instructional sequences.
  - `EVIDENCE_GAP`: A claim present without sufficient citation backing.
  - `SCHEMA_AMBIGUITY`: Disagreement caused by underspecified schema definitions.

## 6. Required Deliverables
1. Cross-Agent Reconciliation Matrix JSON.
2. Structural Disagreement Taxonomy Report in Markdown.
3. Recommended Reconciled Candidate Package (based strictly on evidence, not votes).
4. Standard Execution Report.

## 7. Allowed Changes
- Creation of reconciliation analysis documents and unified candidate proposals.
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- ABSOLUTELY FORBIDDEN: Resolving domain truth conflicts through majority voting.
- NO papering over genuine mathematical or physical discrepancies as "wording differences".

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Resolve conflicts by returning to primary curriculum sources and benchmark peer-reviewed textbooks.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Compute structural diff across candidate packages.
3. Tag and classify each difference into the 10 disagreement types.
4. Resolve reconcilable items via primary source arbitration.
5. Compile execution report.

## 12. Mandatory Falsifiers
- Falsify majority-rule resolution: reject any reconciliation where an unverified majority claim overrides verified evidence.
- Ensure all domain conflicts have explicit primary source citation arbitrations.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Schema validation of reconciled candidate package.

## 14. Acceptance Criteria
- 100% of candidate diffs categorized into the 10 disagreement categories.
- Zero majority-rule compromises on domain truth.

## 15. Stop / Block Conditions
- If a domain conflict between candidates cannot be resolved by primary sources, mark the conflict as `UNRESOLVED_DOMAIN_CONFLICT` and STOP.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
