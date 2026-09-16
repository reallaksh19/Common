# EXECUTION PROMPT: Source Research Worker

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Produce candidate source records conforming to the Source Ledger schema for defined subtopic evidence intents. Provide complete bibliographic, license, and quote provenance without promoting candidate records to canonical authority.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Output must remain designated as candidate source records.
- Conform strictly to `source-ledger.schema.json`.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Search for authoritative sources matching requested evidence intents.
- Extract verbatim text passages, page numbers, edition details, and ISBN/DOI identifiers.
- Populate candidate source ledger records.

## 6. Required Deliverables
1. Candidate Source Ledger JSON file.
2. Source Quotation and Excerpt Digest in Markdown.
3. Standard Execution Report.

## 7. Allowed Changes
- Writing candidate source records to diagnostic output locations.
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO canonical promotion of sources (`WRITE_MODE: ANALYZE_ONLY`).
- NO editing of schemas or core engines.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Prefer authoritative print and peer-reviewed educational literature over web summaries.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Locate sources corresponding to required evidence intents.
3. Verify citation metadata and licensing terms.
4. Serialize candidate records and run schema validator.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Falsify incomplete bibliographic records (missing edition, year, or page).
- Falsify ungrounded quotations.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Validate candidate source records against `source-ledger.schema.json`.

## 14. Acceptance Criteria
- All requested evidence intents backed by candidate sources.
- Zero schema validation errors.

## 15. Stop / Block Conditions
- If verified authoritative sources cannot be found for core claims, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
