# EXECUTION PROMPT: Research-Depth Build

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Construct and validate a RESEARCH-depth overlay for the designated subtopic. Ensure that switching from STANDARD to RESEARCH depth introduces advanced literature claims, extreme limiting cases, and research extensions without silently mutating validated base truth.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Validated foundation and standard truth is immutable.
- Research extensions must be packaged as additive overlays.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Compile claim ledger with peer-reviewed literature citations.
- Build research literature dossier.
- Map conflicting source viewpoints and document conflict resolution receipts.
- Implement advanced exclusions to prevent unverified speculative drift.
- Verify base-claim invariance between STANDARD and RESEARCH tiers.

## 6. Required Deliverables
1. Research-Depth Knowledge Overlay JSON.
2. Literature dossier and peer-reviewed claim ledger.
3. Source conflict resolution audit log.
4. Base-claim invariance verification report.
5. Standard Execution Report.

## 7. Allowed Changes
- Adding research overlay data files and documentation.
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO silent mutation or overwriting of foundational or standard capabilities.
- NO deletion of baseline falsifiers.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Primary peer-reviewed research journals (e.g. Physical Review, Am. J. Phys., J. Chem. Educ.).
- Rigorous academic attribution with DOI, author, and year metadata.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Ingest validated STANDARD package for the subtopic.
3. Build RESEARCH overlay referencing advanced sources.
4. Execute base-invariance differential check: `base(STANDARD) == base(RESEARCH)`.
5. Run research-level falsifiers and compile execution report.

## 12. Mandatory Falsifiers
- Base-claim invariance check: assert that no existing capability definition or formula was altered.
- Source conflict receipt check: assert that every conflicting claim has an explicit resolution receipt.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Execute differential regression tests between STANDARD and RESEARCH packages.

## 14. Acceptance Criteria
- Research overlay attaches cleanly to base subtopic package.
- Base truth is mathematically and textually identical across tiers.
- All research citations pass provenance checks.

## 15. Stop / Block Conditions
- If research depth requires revising validated foundation truths rather than extending them, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
