# EXECUTION PROMPT: Misconception and PCK Research

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Conduct literature-grounded Pedagogical Content Knowledge (PCK) research to identify, categorize, and model learner conceptions, cognitive obstacles, and systematic errors for the target subtopic. Anchor every misconception in empirical research literature.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Strictly adhere to learner conception taxonomy.
- Ground all claims in published empirical educational research; do not improvise anecdotal student errors.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Research cognitive obstacles and student reasoning patterns in the target subtopic.
- Categorize each conception into:
  - `MISCONCEPTION`: Deep-seated, stable alternative framework (e.g. impetus theory, heavier falls faster).
  - `COMMON_ERROR`: Systematic error arising from faulty rule execution.
  - `CONTEXTUAL_RESOURCE`: Productive intuition that is correct in familiar contexts but overapplied.
  - `REPRESENTATION_ERROR`: Inability to read or translate graphs, diagrams, or signs correctly.
  - `OVERGENERALIZATION`: Applying a valid theorem beyond its validity conditions.
  - `PROCEDURAL_ERROR`: Algorithmic slip in algebraic manipulation.
  - `UNVERIFIED_HYPOTHESIS`: Emerging hypothesis requiring further classroom validation.
- Document learner population, grade level, and empirical citations for each item.

## 6. Required Deliverables
1. Learner Conception Catalog JSON conforming to `learner-conception.schema.json`.
2. Pedagogical Remediation Strategy Document in Markdown.
3. Citation receipts for all empirical studies referenced.
4. Standard Execution Report.

## 7. Allowed Changes
- Adding PCK research artifacts to candidate directories.
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO canonical promotion without empirical literature citations.
- NO alteration of disciplinary truth to accommodate learner misconceptions.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Primary education research databases: PER (Physics Education Research Conference, Phys. Rev. PER), CER, MER literature.

## 11. Implementation Procedure
1. Execute cold-start discovery.
2. Review empirical literature on student understanding of the target subtopic.
3. Catalog conceptions with specific diagnostic triggers and refutation strategies.
4. Validate JSON against schema.
5. Compile execution report.

## 12. Mandatory Falsifiers
- Falsify ungrounded conception: reject any item lacking published literature citation or empirical data.
- Falsify diagnostic validity: ensure refutation strategy does not introduce a secondary misconception.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Schema validation of learner conception records.

## 14. Acceptance Criteria
- All identified conceptions classified into the 7 standard taxonomy types.
- Complete empirical attribution (author, journal, year, sample size where available).

## 15. Stop / Block Conditions
- If peer-reviewed literature is unavailable and claims rely on unverified anecdotal claims, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
