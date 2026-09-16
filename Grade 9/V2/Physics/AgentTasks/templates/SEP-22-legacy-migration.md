# EXECUTION PROMPT: Legacy Migration

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Migrate an existing legacy topic or subtopic dataset into the modern Subtopic Knowledge Package (SKP) architecture. Ensure complete preservation of academic content while restructuring into schema-compliant, custody-bound modular packages.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Modern SKP schemas and Technical Engineering Gate standards are normative.
- Do not replicate deprecated legacy schema shortcuts.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Ingest legacy topic artifacts (YAML/JSON/Markdown).
- Map legacy fields to modern SKP capability and relation structures.
- Modernize representations to current visual primitive standards.
- Run differential comparison between legacy and modern packages to prove zero loss of core disciplinary content.

## 6. Required Deliverables
1. Modernized SKP JSON Package.
2. Migration Differential Audit Report.
3. Updated Technical Engineering Gate entry.
4. Standard Execution Report.

## 7. Allowed Changes
- Writing modernized package files to modern directories (`WRITE_MODE: IMPLEMENT`).
- Tiers: `DATA_ONLY`, `DOC`.

## 8. Prohibited Changes
- NO retroactive mutation of historical legacy archive files.
- NO silent dropping of legacy assertions or test cases.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Strictly internal repository comparison between legacy artifacts and modern schemas.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Parse legacy topic files.
3. Transform into modern SKP format.
4. Execute validation suite and differential verification.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Falsify content loss: assert that all legacy capabilities map to a modern counterpart.
- Schema validation: ensure modernized output validates against modern Draft 2020-12 schemas.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Run gate validator on migrated package.

## 14. Acceptance Criteria
- Zero validation errors in modernized package.
- Full parity with legacy disciplinary content verified.

## 15. Stop / Block Conditions
- If legacy content contains irreconcilable conceptual contradictions, STOP and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
