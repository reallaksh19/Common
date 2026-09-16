<!-- COMPILED STANDALONE EXECUTION PROMPT -->
<!-- PROMPT_ID: SEP-08-PHY-RELMOTION-STRESS-v1 -->
<!-- PROMPT_TEMPLATE_ID: SEP-08 -->
<!-- PROMPT_TEMPLATE_VERSION: 1.0.0 -->
<!-- SUBJECT_PROFILE_VERSION: 1.0.0 -->
<!-- SCHEMA_REGISTRY_VERSION: 1.0.0 -->
<!-- COMPILED_PROMPT_DIGEST: e1be9a4b31a4cd268961884050635e7d0ae3732b14418e9ba4112c2880888688 -->

# EXECUTION PROMPT: Architecture Stress Test

## 0. Editable Inputs
```yaml
PROMPT_ID: SEP-08-PHY-RELMOTION-STRESS-v1
PROMPT_TEMPLATE_ID: SEP-08
PROMPT_TEMPLATE_VERSION: 1.0.0
TASK_INSTANCE_ID: task-sep08-relmotion-stress-001

REPOSITORY: reallaksh19/Common
TARGET_BRANCH: v2-physics-agent-tasks-standalone-prompts-v1
BASELINE_PR: 394

SUBJECT: PHYSICS
GRADE: 9
CURRICULUM: CBSE
CURRICULUM_VERSION: 2026-27

TOPIC: Motion
SUBTOPIC: Relative Motion

ENGINEERING_DEPTH: STANDARD
LEARNER_STATE: UNKNOWN

WEB_RESEARCH_ALLOWED: false
LOCAL_QUESTION_BANKS: DISCOVER_FROM_REPOSITORY

WRITE_MODE: IMPLEMENT
EXPECTED_SCOPE:
  - 1D Relative Motion: collinear velocity addition and subtraction
  - 2D Relative Motion: river-swimmer shortest path and shortest time
  - 2D Relative Motion: rain-umbrella apparent velocity and tilt angle
  - Reference Frame Transformations: Galilean kinematic invariance
  - Relative Kinematic Graphs: x_rel-t slope and v_rel-t area integral
EXPLICIT_EXCLUSIONS:
  - Lorentz transformations / Relativistic velocity addition
  - Accelerated non-inertial frames with Coriolis force (Grade 11 advanced)
  - General relativity
```

## 1. Mission
Execute a cold-start architecture stress test by taking a standard new subtopic and proving that it can be completely integrated, compiled, and validated without modifying any Blueprint or generic engine code.

## 2. Repository / Branch Authority
- Target Repository: `reallaksh19/Common`
- Target Branch: `v2-physics-agent-tasks-standalone-prompts-v1`
- Baseline PR: `394`
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
- The generic Blueprint and execution pipeline are immutable for this run.
- All adaptation must occur through governed data packages and declared adapter extension points.
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
- Cold ingest of the target subtopic parameters.
- Construction and validation of the subtopic knowledge package.
- Verification that zero lines of Blueprint code were modified or required.
- Verification that all gates and falsifiers pass.

## 6. Required Deliverables
1. Subtopic knowledge package data files (`DATA_ONLY`).
2. Architecture Stress Test Report proving zero Blueprint edits.
3. Falsifier execution log.
4. Standard Execution Report.

## 7. Allowed Changes
- STRICTLY `DATA_ONLY` changes.
- Tier: `DATA_ONLY`.

## 8. Prohibited Changes
- ABSOLUTELY PROHIBITED: Any change to `Blueprint/` or core compilation engines.
- NO hardcoded topic checks or special-case heuristics.

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
- Rely solely on declared repository schemas, source ledgers, and subject profile contracts.

## 11. Implementation Procedure
1. Perform cold-start repository discovery.
2. Build candidate data package for the target subtopic.
3. Run complete test and gate verification pipeline.
4. Verify `git diff` confirms zero edits outside data directories.
5. Compile completion report.

## 12. Mandatory Falsifiers
- Git diff assertion: `git diff --name-only | grep -E "Blueprint|engine"` must return empty.
- Subtopic gate execution must pass with exit code 0.
### Subject Mandatory Falsifiers (PHYSICS)
- `DIMENSIONAL_CONSISTENCY_CHECK`
- `LIMITING_CASE_FALSIFICATION`
- `CONSERVATION_LAW_SANITY_CHECK`
- `FRAME_TRANSFORMATION_INVARIANCE`
- `SIGN_CONVENTION_COHERENCE`

## 13. Tests / CI
- Execute subtopic-specific gate test battery.
- Run generic regression test suite to ensure zero regressions.

## 14. Acceptance Criteria
- Full subtopic functionality demonstrated.
- Zero Blueprint modifications (`changed_files` contains only `DATA_ONLY` entries).
- All tests pass with documented evidence.

## 15. Stop / Block Conditions
- If subtopic requirements cannot be satisfied without editing the Blueprint, STOP immediately and return `result: "BLOCKED"` detailing the exact architectural failure.

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

