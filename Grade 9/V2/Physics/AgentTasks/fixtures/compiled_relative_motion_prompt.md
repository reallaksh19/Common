<!-- COMPILED STANDALONE EXECUTION PROMPT -->
<!-- PROMPT_ID: SEP-PHY-RELMOTION-v1 -->
<!-- PROMPT_TEMPLATE_ID: SEP-07 -->
<!-- PROMPT_TEMPLATE_VERSION: 1.0.0 -->
<!-- SUBJECT_PROFILE_VERSION: 1.0.0 -->
<!-- SCHEMA_REGISTRY_VERSION: 1.0.0 -->
<!-- COMPILED_PROMPT_DIGEST: 417cd41e1937a93bdc0183b199201fe3b2565ce3571c1a71d013ef76fe829835 -->

# EXECUTION PROMPT: Subtopic Engineering Build

## 0. Editable Inputs
```yaml
PROMPT_ID: SEP-PHY-RELMOTION-v1
PROMPT_TEMPLATE_ID: SEP-07
PROMPT_TEMPLATE_VERSION: 1.0.0
TASK_INSTANCE_ID: task-relmotion-001

REPOSITORY: reallaksh19/Common
TARGET_BRANCH: v2-physics-gates-gr9-11
BASELINE_PR: 383

SUBJECT: PHYSICS
GRADE: 9
CURRICULUM: CBSE
CURRICULUM_VERSION: 2026-27

TOPIC: Motion
SUBTOPIC: Relative Motion

ENGINEERING_DEPTH: STANDARD
LEARNER_STATE: UNKNOWN

WEB_RESEARCH_ALLOWED: true
LOCAL_QUESTION_BANKS: DISCOVER_FROM_REPOSITORY

WRITE_MODE: IMPLEMENT
EXPECTED_SCOPE:
  - 1D Relative Velocity
  - 2D Relative Velocity in Plane
  - Frame of Reference Transformations
EXPLICIT_EXCLUSIONS:
  - Relativistic velocity addition (Lorentz transformations)
  - Curved spacetime
```

## 1. Mission
Execute the full engineering build for the specified subtopic: discover existing authorities, reconcile curriculum scope, construct candidate Subtopic Knowledge Package (SKP) data, compile prerequisite closures, compile Technical Engineering Gates, compile Readiness artifacts, and execute the complete falsifier battery.

## 2. Repository / Branch Authority
- Target Repository: `reallaksh19/Common`
- Target Branch: `v2-physics-gates-gr9-11`
- Baseline PR: `383`
- Governing Manifests: `AGENTS.md`, `README.md`, `contracts/`
- All actions must be validated against repository HEAD.

## 3. Cold-Start Discovery
# Mandatory Cold-Start Repository Discovery Protocol

Every standalone agent must establish complete repository ground truth before proposing or editing any files.

---

### Pre-Modification Discovery Sequence

Before making any changes, the executing agent must execute the following 10 discovery steps in order:

1. **Resolve Target Branch & Exact HEAD**:
   Identify the active branch, base branch, and exact git commit hash at start. Record this in the execution identity.

2. **Read Governing Manifests & Policies**:
   Locate and read the applicable generation, adoption, and authority manifests (e.g. `AGENTS.md`, `EXIT_GATE.md`, `README.md`, `manifest.json`).

3. **Locate Schema Registries & Normative Architecture**:
   Identify the Draft 2020-12 JSON schemas governing input and output contracts. Confirm which schemas define validation boundaries.

4. **Locate Producers & Consumers**:
   Identify which engine or script generates the target artifact, and which downstream tools or pipelines ingest it.

5. **Locate Existing Tests & CI Workflows**:
   Identify the regression test suites, unit tests, falsifiers, and GitHub Actions workflow definitions associated with the target domain.

6. **Locate Structural Reference Implementations**:
   Identify verified, adjacent implementations that can serve as structural patterns (without treating their case facts as authority).

7. **Search for Deprecated / Legacy Artifacts**:
   Explicitly search for obsolete or retired versions of the concept in the repository to prevent resurrecting superseded paradigms.

8. **Distinguish Canonical vs. Diagnostic Artifacts**:
   Classify existing artifacts into canonical (ground truth data, registries) versus diagnostic/temporary (runtime projections, feedback logs).

9. **Identify Cross-Domain Dependencies**:
   Map dependencies crossing subject boundaries (e.g. Physics depending on Vector Algebra or Calculus in Mathematics) and verify their governing interface contracts.

10. **Record Authority Chain**:
    Formulate and document the explicit chain of authority (Manifest → Policy → Schema → Data → Engine → Test) before initiating modifications.

---

### Non-Negotiable Cold-Start Rule

> **Do not treat a previously seen implementation as authority merely because it resembles the current task.**
>
> Resemblance is not specification. Only schemas, explicit contracts, and documented governing manifests have authority over the task.


## 4. Existing Architecture to Respect
- Respect existing Technical Engineering Gate Registry schemas and invariants.
- Build subtopic content strictly within governed data files without hardcoding case logic in shared engines.
### Subject Disciplinary Rules (PHYSICS v1.0.0)
_Disciplinary ontology, representations, and validation invariants for Grade 9-11 Physics (CBSE, JEE Main, JEE Advanced)._

**Epistemological Rules:**
- Distinguish observer-dependent kinematic quantities (displacement, velocity) from frame-invariant physical laws.
- Enforce dimensional homogeneity: terms added or equated must have identical dimensional powers [M^a L^b T^c I^d].
- Every kinematic model must explicitly declare its inertial or non-inertial reference frame.
- Non-inertial models must explicitly include pseudo-forces (-m*a_frame) with explicit observer declaration.
- Limiting cases (e.g. mass m2 >> m1, velocity v -> 0, angle theta -> 0 or 90 deg) must be mathematically falsified.

**Allowed Representations:**
- `KINEMATIC_GRAPH_PLOT`
- `FREE_BODY_DIAGRAM`
- `VECTOR_POLYGON_DIAGRAM`
- `RAY_OPTICS_DIAGRAM`
- `CIRCUIT_SCHEMATIC`
- `THERMODYNAMIC_PV_CYCLE`
- `WAVE_OSCILLATION_PLOT`
- `FIELD_LINE_EQUIPOTENTIAL_MAP`

## 5. Task Scope
- Reconcile subtopic curriculum scope against declared board and competitive frameworks.
- Construct candidate SKP JSON package (capabilities, relations, representations, problem families, misconceptions).
- Compile prerequisite closure and verify acyclicity.
- Compile and bind Technical Engineering Gate.
- Run comprehensive validation falsifiers.

## 6. Required Deliverables
1. Validated Subtopic Knowledge Package JSON.
2. Technical Engineering Gate entry and registry binding.
3. Prerequisite closure verification artifact.
4. Falsifier execution log.
5. Standard Execution Report (Markdown + Machine JSON).

## 7. Allowed Changes
- Primarily: `DATA_ONLY`.
- Permitted if formally justified: `SCHEMA_EXTENSION`, `SUBJECT_ADAPTER_CHANGE`.
- Rare and suspicious: `GENERIC_ENGINE_CHANGE`.

## 8. Prohibited Changes
- FORBIDDEN without explicit architectural exemption: `BLUEPRINT_CHANGE`.
- If a Blueprint change is contemplated, STOP immediately and output a new-invariant justification document before making any changes.
- NO hardcoded topic branches in shared engines.

## 9. Anti-Drift Invariants
# Universal Anti-Drift Invariants

These invariants govern every execution task across the repository. They are fail-closed, non-negotiable architectural axioms. Any agent execution that violates these rules must be rejected by automated validators and human reviewers.

---

### Invariant A: Repository authority overrides memory
The current git repository state at the designated target commit HEAD is the sole source of architectural truth. Any prior memory, external assumptions, or conversational recollections are strictly advisory and subordinate to repository code, schemas, and manifests.

### Invariant B: Current schemas override examples
When an existing code fixture or legacy example contradicts a schema defined in `contracts/`, the schema is normative. Do not copy deprecated patterns from older files; adhere strictly to the active Draft 2020-12 schema definitions.

### Invariant C: Generated/canonical authority overrides diagnostic projections
Canonical artifacts (authoritative knowledge graphs, validated registries, and published manuscripts) hold authority over runtime diagnostic projections or temporary student-state projections. Diagnostic lenses observe canonical truth; they never dictate or rewrite it.

### Invariant D: Case facts belong in governed data, not global logic
All subject-matter parameters, pedagogical steps, numerical constants, and curriculum bindings belong in governed JSON/data files, never hardcoded as conditional branches (`if topic == '...'`) inside shared engines.

### Invariant E: A normal new subtopic must not require Blueprint case branches
The introduction of an ordinary new subtopic must be achievable entirely via `DATA_ONLY` additions. If an engine or Blueprint requires case-specific code branches to accept a new subtopic, the architecture has suffered case coupling.

### Invariant F: Missing evidence remains UNKNOWN/HELD/MISSING; never infer it
If a source, answer derivation, prerequisite edge, or rubric score lacks empirical or repository evidence, it must remain explicitly designated as `UNKNOWN`, `HELD`, or `MISSING`. An agent must never fabricate or heuristically hallucinate missing evidence.

### Invariant G: Learner state may change treatment, not disciplinary truth
Learner cognitive states (e.g., `NOVICE`, `MISCONCEPTION_ACTIVE`) govern pedagogical pacing, scaffolding depth, and representation sequences. Learner state must never alter disciplinary truth, mathematical laws, or physical invariants.

### Invariant H: Research depth may add evidence/depth; it may not silently mutate validated base truth
Switching from `FOUNDATION` or `STANDARD` to `RESEARCH` depth permits richer citations, historical debates, advanced limiting cases, and experimental caveats. It must never alter or invalidate the validated foundation theorems.

### Invariant I: External-domain authority must not be fabricated by the subject adapter
Subject adapters (e.g. Physics, Chemistry, Mathematics) must operate within their declared disciplinary boundaries. Cross-domain prerequisites (e.g. Physics relying on Calculus or Coordinate Geometry) must reference governed cross-domain contracts rather than inventing pseudo-mathematical authority.

### Invariant J: Publication authority must not be inferred from technical readiness
Passing a technical syntax check or schema validation is necessary but insufficient for publication. Final release authorization requires explicit human review clearance, complete provenance ledger binding, and custody seal verification.

### Invariant K: Same-ID mutated content must be rejected through digest/custody validation
Any artifact sharing an existing ID but bearing modified semantic content without an explicit version increment and digest match must be rejected as an integrity violation.

### Invariant L: New workflows/code paths require justification as a new invariant class
Introducing a new engine execution path, CLI flag, or workflow stage requires formal justification showing why existing generic abstractions cannot accommodate the requirement.

### Invariant M: If the requested result cannot be reached honestly, leave the state blocked and report exactly why
`BLOCKED` with precise evidence is a completely valid and successful execution outcome. An agent must never weaken validation rules, fabricate evidence, bypass assertions, or mark unverified tests as `PASS` merely to appear complete.


## 10. Research / Source Policy
- Strictly adhere to approved primary curriculum standards and secondary benchmark textbooks.
- Every capability must link to a valid source citation in the source ledger.

## 11. Implementation Procedure
1. Execute cold-start repository discovery.
2. Construct candidate SKP data adhering to `skp.schema.json`.
3. Compute and compile prerequisite closure.
4. Integrate entry into Technical Engineering Gate Registry.
5. Execute full falsifier battery and regression tests.
6. Verify no memory dependency and compile execution report.

## 12. Mandatory Falsifiers
- Prerequisite cycle check (must be acyclic DAG).
- ID uniqueness and reference resolution across all entities.
- Limiting-case mathematical checks for declared formulas.
- Falsify with mutated content to verify digest sensitivity.
### Subject Mandatory Falsifiers (PHYSICS)
- `DIMENSIONAL_CONSISTENCY_CHECK`
- `LIMITING_CASE_FALSIFICATION`
- `CONSERVATION_LAW_SANITY_CHECK`
- `FRAME_TRANSFORMATION_INVARIANCE`
- `SIGN_CONVENTION_COHERENCE`

## 13. Tests / CI
- Run all subject-specific contract tests and gate tests.
- Verify schema validation with `Draft202012Validator`.

## 14. Acceptance Criteria
- Candidate SKP validates against schema with 0 errors.
- Prerequisite closure is closed and acyclic.
- Technical Engineering Gate passes all 16 technical criteria.
- 100% of falsifier tests pass.
- Changes are strictly `DATA_ONLY` (or justified extensions).

## 15. Stop / Block Conditions
- If constructing the subtopic requires adding conditional branches (`if topic == '...'`) to the generic Blueprint, STOP and return `result: "BLOCKED"`.
- BLOCKED with evidence is a successful outcome. Never hack the engine to pass a subtopic.

## 16. Exact Completion Report
# Standardized Execution Report Contract

Every executing agent must return this exact report structure upon completing or blocking a task. The output consists of a human-readable Markdown section followed by a fenced JSON block complying with `execution-report.schema.json`.

---

## Markdown Report Template

```markdown
# Execution Report

## 1. Execution identity
Prompt ID: <PROMPT_ID>
Task instance: <TASK_INSTANCE_ID>
Repository: <REPOSITORY>
Branch: <TARGET_BRANCH>
Starting HEAD: <START_HEAD>
Ending HEAD: <END_HEAD>

## 2. Mission result
<COMPLETE | PARTIAL | BLOCKED>

## 3. Repository authority discovered
- Manifests: <list of manifests consulted>
- Schemas: <list of Draft 2020-12 schemas enforced>
- Policy: <applicable policy documents>
- Producers: <governing producer scripts/engines>
- Consumers: <downstream consumers/validators>
- CI: <applicable GitHub Actions workflows>

## 4. Changes made
For each changed file:
- Path: <relative path>
- Reason: <justification>
- Tier: <DATA_ONLY | SCHEMA | GENERIC_ENGINE | SUBJECT_ADAPTER | BLUEPRINT | TEST | DOC | SCHEMA_EXTENSION | SUBJECT_ADAPTER_CHANGE | GENERIC_ENGINE_CHANGE | BLUEPRINT_CHANGE>
- Authority impact: <description of custody/authority changes>

## 5. Derived state before
<Description or summary of system/data state prior to execution>

## 6. Derived state after
<Description or summary of system/data state following execution>

## 7. Tests/falsifiers
| Test Name / Command | Result (PASS/FAIL/SKIPPED/NOT_RUN) | Evidence / Exit Code |
|---------------------|------------------------------------|----------------------|
| <test_1>            | <result_1>                         | <evidence_1>         |

## 8. CI status
| Workflow | Run Trigger / ID | Result |
|----------|------------------|--------|
| <wf_1>   | <run_1>          | <res_1>|

## 9. Invariants checked
- Invariant A (Repository authority): <VERIFIED | BLOCKED>
- Invariant B (Current schemas): <VERIFIED | BLOCKED>
- Invariant C (Canonical over diagnostic): <VERIFIED | BLOCKED>
- Invariant D (Case facts in data): <VERIFIED | BLOCKED>
- Invariant E (No Blueprint case branches): <VERIFIED | BLOCKED>
- Invariant F (No inferred evidence): <VERIFIED | BLOCKED>
- Invariant G (Learner state invariant on truth): <VERIFIED | BLOCKED>
- Invariant H (Research depth invariant on base): <VERIFIED | BLOCKED>
- Invariant I (No fabricated cross-domain authority): <VERIFIED | BLOCKED>
- Invariant J (Publication authority separated): <VERIFIED | BLOCKED>
- Invariant K (Anti-mutation custody): <VERIFIED | BLOCKED>
- Invariant L (Justified workflows): <VERIFIED | BLOCKED>
- Invariant M (Fail-closed honest stop): <VERIFIED | BLOCKED>

## 10. Known limitations
- <Declared limitation 1>
- <Declared limitation 2>

## 11. Unresolved issues
- <Unresolved issue or blocker 1>

## 12. Architecture findings
- Reusable improvement discovered: <finding>
- Remaining case coupling: <coupling>
- Scalability concern: <concern>

## 13. No-memory declaration
State whether completion depended on any information not recoverable from repository or declared external sources:
`MEMORY_INDEPENDENCE_VERIFIED: TRUE` (or FALSE if contaminated).

## 14. Recommended next task
<Suggested immediate next task instance or follow-up prompt ID>
```

---

## Machine JSON Contract

Following the Markdown report, the agent must output a single JSON block conforming to `execution-report.schema.json`:

```json
{
  "prompt_id": "<PROMPT_ID>",
  "task_instance_id": "<TASK_INSTANCE_ID>",
  "start_head": "<START_HEAD>",
  "end_head": "<END_HEAD>",
  "result": "COMPLETE",
  "changed_files": [
    {
      "path": "<path>",
      "reason": "<reason>",
      "tier": "DATA_ONLY",
      "authority_impact": "<impact>"
    }
  ],
  "tests": [
    {
      "test": "<test_command>",
      "result": "PASS",
      "evidence": "<output_summary>"
    }
  ],
  "workflows": [
    {
      "workflow": "<workflow_name>",
      "run": "<run_id>",
      "result": "<status>"
    }
  ],
  "blockers": [],
  "limitations": [
    "<limitation_1>"
  ],
  "architecture_findings": [
    "<finding_1>"
  ],
  "memory_dependency_detected": false,
  "recommended_next_task": "<next_task_id>"
}
```

