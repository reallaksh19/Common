# EXECUTION PROMPT: Architecture Falsification

## 0. Editable Inputs
{{EDITABLE_INPUTS_BLOCK}}

## 1. Mission
Execute a dedicated adversarial red-team attack on the core system architecture. Do NOT attempt to fix, polish, or defend the architecture. Systematically stress-test and attempt to break the core assumption that the architecture is general, modular, and subject-neutral across diverse STEM domains.

## 2. Repository / Branch Authority
{{REPOSITORY_BRANCH_AUTHORITY}}

## 3. Cold-Start Discovery
{{COLD_START_DISCOVERY}}

## 4. Existing Architecture to Respect
- Test the architecture against extreme edge cases across Physics, Mathematics, and Chemistry.
- Treat any discovered non-general assumption as a high-value finding.
{{SUBJECT_ARCHITECTURE_GUIDELINES}}

## 5. Task Scope
- Actively search for:
  1. Hidden Physics assumptions baked into shared schemas or engines (e.g. assuming vectors, time dimensions, or kinematics everywhere).
  2. Compulsory schema fields that make no sense in other subjects (e.g. forcing equations in pure geometric proofs or electron counts in mechanics).
  3. Places where learner cognitive state inappropriately alters domain truth.
  4. Implicit web or network assumptions that fail in offline/airgapped environments.
  5. Digest, custody, or tamper-detection vulnerabilities (e.g. ID collisions, hash pre-image weaknesses).
  6. Hardcoded topic-ID or subject-ID conditional branches in generic engines.
  7. Ambiguous schema semantics where two independent agents produce conflicting valid structures.
  8. Impossible cold-start agent reconstruction paths.

## 6. Required Deliverables
1. Architecture Falsification Attack Dossier in Markdown.
2. Catalog of Discovered Abstraction Failures and Hidden Couplings.
3. Minimal Reproducible Counterexample Fixtures.
4. Standard Execution Report.

## 7. Allowed Changes
- Adding red-team attack reports and failure fixtures to diagnostic directories (`WRITE_MODE: ANALYZE_ONLY`).
- Tier: `DOC`.

## 8. Prohibited Changes
- NO fixing or patching the code during this run.
- NO concealing discovered architectural defects.

## 9. Anti-Drift Invariants
{{ANTI_DRIFT_INVARIANTS}}

## 10. Research / Source Policy
- Epistemology of physics, mathematics, and chemistry, and software architectural analysis.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Select contrasting stress cases (e.g. Euclidean Geometry, Chemical Reactions, Thermodynamics, Kinematics).
3. Execute red-team falsification heuristics across all schemas and engines.
4. Document concrete counterexamples where generic assumptions fail.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Reward metric: number of legitimate architectural abstraction failures demonstrated with reproducible evidence.
{{SUBJECT_MANDATORY_FALSIFIERS}}

## 13. Tests / CI
- Verify that reproducible failure fixtures fail as declared.

## 14. Acceptance Criteria
- Concrete evaluation of all 8 vulnerability classes.
- Zero defensive rationalization; rigorous documentation of true systemic limits.

## 15. Stop / Block Conditions
- If the architecture is so brittle that cold discovery crashes basic inspection tools, document the crash and return `result: "BLOCKED"`.

## 16. Exact Completion Report
{{COMPLETION_REPORT_CONTRACT}}
