# EXECUTION PROMPT: Question-Bank Miner

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Mine and analyze local assessment corpora and question banks for the target subtopic. Map authentic assessment items to capability vocabulary, cluster candidate problem families, detect duplicates, and isolate unmapped items without fabricating artificial capabilities to force fit questions.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Treat assessment corpus as empirical evidence, not normative capability definitions.
- Respect capability boundaries: NEVER create ad-hoc capabilities merely to fit an outlier question.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Extract raw question items from designated local question banks.
- Map questions to current capability definitions.
- Cluster questions into candidate problem families.
- Identify duplicate or near-duplicate items.
- Report unmapped questions and scope violations.

## 6. Required Deliverables
1. Structured Question Inventory JSON.
2. Capability-to-Question Binding Matrix JSON.
3. Problem Family Clustering Report.
4. Unmapped Questions and Scope Violations Log.
5. Standard Execution Report.

## 7. Allowed Changes
- Creation of mined assessment data in designated diagnostic locations.
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO mutation of existing capability schemas or canonical SKP data.
- FORBIDDEN: Expanding capability vocabulary solely to absorb outlier questions.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Local repository question corpora (e.g. past board papers, official JEE Main/Advanced archives).

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Ingest raw items from repository question banks.
3. Map items against approved capability vocabulary.
4. Flag and quarantine items requiring prerequisite knowledge outside declared scope.
5. Compile report and execution records.

## 12. Mandatory Falsifiers
- Falsify forced mapping: verify unmapped items remain in `unmapped_questions` rather than inventing spurious capabilities.
- Falsify duplicate detection: verify identical items with different IDs are flagged.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Schema validation of question inventory and mapping matrix.

## 14. Acceptance Criteria
- Complete mining of target question corpus.
- Zero invented capabilities; unmapped questions explicitly logged.
- Duplicate questions properly clustered.

## 15. Stop / Block Conditions
- If the question corpus is corrupt or missing source attribution, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
