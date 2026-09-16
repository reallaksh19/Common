# Mathematics V2 — Core (1A): bucket synthesis + textbook realization

Core (1) is a governed **capability-level semantic teaching plan**. It is not yet the final textbook unit structure. Core (1A) must first identify coherent teaching buckets, using the exact learner-conditioned StudyModel that Core (1) was authored from, and only then realize those buckets as textbook-quality learner content.

```text
M-E LearnerStateSnapshot
        ↓
M-F MathLearnerStudyModel
        ↓
Core (1) MathCore1StudyPlan
        ↓
Core (1A)-B  BUCKET SYNTHESIS
        ↓
Core (1A)-R  TEXTBOOK REALIZATION
        ↓
core1a_student_textbook.pdf
```

## Semantic ownership

- **M-E** owns learner evidence/state: `UNKNOWN | DEVELOPING | READY`, confidence and observation refs.
- **M-F** owns learner-conditioned treatment/priority: `VERIFY_ONLY | ACTIVE_STUDY | REPAIR_BEFORE | REPAIR_IN_UNIT | PROBE_FIRST`.
- **Core (1)** owns complete capability-level instructional authority, PCK/problem-family bindings, representations and verification obligations.
- **Core (1A)-B** owns teaching-bucket synthesis only. It may group capability plans, but it may not diagnose the learner, change treatment, invent mathematical scope or invent bucket invariants.
- **Core (1A)-R** owns learner-facing textbook realization of the governed bucket plan.
- **Core (2)/(2A)** owns original-question transfer and its learner realization.

## Capability != bucket

A `MathCore1Lesson` is capability-centric. A textbook bucket may contain several related capabilities when they share a real mathematical teaching invariant/problem family. Conversely, a prerequisite capability that feeds several unrelated buckets may need its own bridge bucket.

Core (1A) therefore does **not** equate `Core1.lessons[]` with final textbook chapters.

The canonical semantic object is `Core1ABucketPlan`:

```text
Bucket[]
 ├─ bucket_invariant
 ├─ member_capability_refs[]
 ├─ primary_capability_refs[]
 ├─ supporting_capability_refs[]
 ├─ learner_treatment_by_capability[]
 ├─ dependency_edges[]
 ├─ learning_atoms[]
 ├─ representation_requirements[]
 └─ verification_requirements[]
```

`contracts/math-core1a-bucket-plan.schema.json` is the canonical Core (1A) semantic contract. The textbook manuscript is downstream of this object.

## Core (1A) does not invent learner knowledge

For every capability Core (1A) preserves from M-F:

- `learner_state_readiness`;
- `learner_state_confidence`;
- `learner_state_observation_refs`;
- `treatment`;
- `priority_band`.

Core (1A) must **not** invent a second learner-state truth such as `FOUNDATION`, `PARTIAL`, `20% learner`, or `50% learner`.

A single bucket can legitimately contain different treatments:

```text
capability A  READY       → VERIFY_ONLY
capability B  DEVELOPING  → REPAIR_IN_UNIT
capability C  UNKNOWN     → ACTIVE_STUDY
```

The learner product activates A briefly, repairs B, and fully teaches C without relabelling the learner.

## Bucket synthesis policy

The first implementation is deliberately conservative and deterministic:

1. directly assessed capabilities are grouped when they share governed problem-family authority;
2. a prerequisite-only capability is attached to a single dependent bucket when the M-F dependency makes that unambiguous;
3. a prerequisite feeding multiple buckets remains its own bridge bucket so it is taught once rather than duplicated;
4. every Core (1) capability appears in exactly one bucket;
5. bucket order follows approved Core (1) capability order — no invented difficulty ranking;
6. the bucket invariant must be grounded in either a canonical problem-family `target_job` or a bound PCK anchor;
7. if the invariant cannot be grounded, generation fails rather than letting the renderer invent one.

This policy can later become richer, but only through governed semantic rules — never through page-layout heuristics.

## Learning atoms

Core (1A) creates traceable learning atoms from bound PCK. Current atom sources are:

- selected PCK anchor / ordinary-language bridge;
- each PCK reconstruction step.

Each atom retains its capability and PCK source.

Core (2) H1/H2/H3 → Core (1A) atom binding is **not silently inferred here**. It is the next cross-product closure and must consume the actual Core2TransferPlan. Until that binding is implemented, Core (1A) exposes grounded atoms and exact `core2_question_refs`; it does not claim hint coverage that has not been proven.

## Structure preservation

Preservation applies to **authority and learner-conditioned semantics**, not to old page geometry.

Core (1A) preserves:

- complete Core (1) capability coverage;
- Core (1) capability order as stable ordering basis;
- capability, PCK and problem-family authority;
- M-F learner state, treatment and priority;
- assessment-question bindings;
- prerequisite dependencies;
- representation and verification requirements;
- original-assessment firewall;
- release/provenance class.

Core (1A) may change physical page count, page composition, explanatory depth, number of fresh examples, representation form, worked-example narration, whitespace and typography.

```text
preserve governed semantics != preserve existing pages
capability lesson != textbook bucket
learner treatment != Core1A-invented learner level
```

## Textbook manuscript

`math-core1a-textbook-manuscript.schema.json` is bucket-centric (`schema_version = 2.0.0`). Each bucket contains learner-facing capability units, but the bucket is the visible teaching unit.

Outputs:

```text
core1a_bucket_plan.json
core1a_textbook_manuscript.json
core1a_quality_audit.json
core1a_student_textbook.pdf
```

## Fail-closed behavior

Important falsifiers include:

```text
CORE1A_STUDY_MODEL_REF_MISMATCH
CORE1A_STUDY_MODEL_DIGEST_BINDING_MISMATCH
CORE1A_STUDY_MODEL_SCOPE_COVERAGE_DRIFT
CORE1A_TREATMENT_DRIFT
CORE1A_SCOPE_ROLE_DRIFT
CORE1A_ASSESSMENT_BINDING_DRIFT
CORE1A_BUCKET_COVERAGE_FAILED
CORE1A_BUCKET_INVARIANT_UNGROUNDED
CORE1A_BUCKET_PCK_BINDING_MISSING
CORE1A_BUCKET_LEARNING_ATOMS_MISSING
CORE1A_LEARNER_TREATMENT_DRIFT
CORE1A_FAMILY_GENERATOR_MISSING
CORE1_AUTHORED_INSTANCE_NOT_MATERIALIZED
CORE1A_INTERNAL_JARGON_LEAK
CORE1A_INTERNAL_IDENTIFIER_LEAK
CORE1A_QUALITY_GATE_FAILED
```

## CLI

The exact learner StudyModel is a required input:

```bash
python 'Grade 9/V2/Mathematics/Core1A/engine/realize_math_core1a.py' \
  --core1-plan /path/to/core1_study_plan.json \
  --study-model /path/to/learner_study_model.json \
  --out-dir /tmp/core1a
```

The CLI verifies the Core1→StudyModel digest/ref binding before bucket synthesis.

## CI proof

The workflow runs the real PR #323 cold-start chain and extracts both:

```text
internals['study_model']
internals['core1_plan']
```

It proves the exact binding, synthesizes the bucket plan, verifies exact capability coverage, verifies that `(learner_state_readiness, treatment)` is unchanged for every capability, rejects invented learner-state categories, then realizes and inspects the learner PDF.

## Relation to Core (2A)

```text
Core (1) → Core (1A)-B bucket synthesis → Core (1A)-R teaching PDF
Core (2) → Core (2A) source-transfer/practice PDF
```

Core (2A) preserves original-question authority. Cross-product hint closure will require every Core (2) H1/H2/H3 reveal to bind to a grounded Core (1A) learning atom and fail when a reveal was not genuinely pre-taught.

## Release meaning

Core (1A) inherits the release legality of Core (1) and its upstream StudyModel/PCK authority. Better learner realization cannot upgrade provisional PCK, change learner diagnosis, alter treatment decisions, or bypass human gates.
