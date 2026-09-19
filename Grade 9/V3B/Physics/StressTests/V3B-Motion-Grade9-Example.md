# Filled stress-test invocation — Grade 9 relative motion, V3B

Give the production agent this file **and** [the reusable prompt](V3B-Stress-Test-Prompt-Template.md). This configuration overrides its placeholders. It requests actual draft learner outputs; it does not claim this stress test has already run.

```yaml
request_id: STRESS-PHY-RELATIVE-MOTION-G9-V3B
repository: reallaksh19/Common
architecture_pr: 364
architecture_basis: VERIFY_LIVE_HEAD_AND_RECORD
subject: Physics
topic: Motion in two dimensions
subtopics: [Vector representation and subtraction, Relative velocity in a plane]
grade: 9
board: CBSE
academic_year: 2026-27
curriculum_track: ADVANCED
language: English
scope_mode: BOARD_PLUS_LABELLED_EXTENSION
included:
  - Reference object, common clock and coordinate directions
  - Scalar magnitude versus vector and signed components
  - Graphical subtraction as addition of the opposite vector
  - Relative position and relative velocity in translating nonrotating frames
  - Same-direction, opposite-direction and perpendicular motions
  - Reading an observer statement before selecting a relation
  - One boat/current model as a labelled extension with conditions
excluded:
  - Rotating frames and Coriolis terms
  - Relativistic velocity addition
  - Calculus-dependent derivations in the baseline learner products
  - General oblique-angle trigonometry without a separate prerequisite bridge
  - Full projectile-motion chapter
depth_overlay: ADVANCED
research_question: null
intrinsic_badges:
  Vector representation and subtraction: MEDIUM
  Relative velocity in a plane: HARD
products: [CORE1, CORE2, CORE1A, CORE1B, CORE2A, CORE2B]
practice_purpose: COMPETITIVE_PREPARATION
knowledge:
  percentage: null
  provenance: UNKNOWN
  scope: Relative velocity and its prerequisites
  evidence_files: []
owner_waiver:
  enabled: true
  instruction: Start from prerequisite bridges and simple cases, then offer clearly labelled competitive-foundation transfer. Do not claim measured mastery.
sources:
  frozen_core1: []
  frozen_core2: []
  local_references: []
  preferred_web_sources:
    - https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceAd_SecP1_2026-27.pdf
    - https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceSt_SecP1_2026-27.pdf
    - https://ncert.nic.in/textbook/pdf/keph102.pdf
    - https://ncert.nic.in/textbook/pdf/keph103.pdf
    - https://cbseacademic.nic.in/cbe/documents/SAS_Science-Class-9.pdf
    - https://phet.colorado.edu/en/simulations/vector-addition
  corpus_mode: BUILD_REVIEW_CORPUS
  acquisition_allowed: true
question_targets: {core2a: 8, core2b: 6, count_policy: EDITABLE_TARGET_REPORT_SOURCE_OR_PURPOSE_GAPS}
delivery:
  output_root: Grade 9/V3B/Physics/StressTests/runs/relative-motion-g9-V3B
  formats: [HTML, PDF, STRUCTURED_SOURCE]
  audience: SELF_STUDY
  manuscript_status: REVIEW_DRAFT
stress:
  profiles: [LOW_SCOPED_EVIDENCE, HIGH_SCOPED_EVIDENCE, UNKNOWN_WITH_WAIVER]
  one_extension: Add a separate research-oriented model-boundary bucket on when simple relative-velocity subtraction needs frame qualifications; do not add it to Grade 9 assessment claims.
  cold_agent_resume: true
  run_corruption_checks: true
```

Change `curriculum_track` to STANDARD if needed and reclassify the extension. The checked 2026–27 Standard syllabus focuses on one-dimensional kinematics and elementary circular motion; the optional Advanced material includes reference frames, motion relative to an observer and graphical vector operations. This does **not** establish that every quantitative two-dimensional relative-motion or boat/current task is prescribed. Bind each capability to the exact section or mark it as owner-requested enrichment. [Standard syllabus, Motion section](https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceSt_SecP1_2026-27.pdf), [Advanced material, chapter 2](https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceAd_SecP1_2026-27.pdf).

The empty local/frozen lists are deliberate, not fictional file paths. If the owner supplies an existing frozen corpus, switch to FROZEN_SUPPLIED and retain its identities. The CBSE competency bank is a historical question source, not proof of current syllabus alignment or a two-dimensional relative-motion bank. Verify each selected item. NCERT Class XI sources may support advanced teaching semantics; they do not convert an extension into Grade 9 syllabus content.

## Required concept progression

Use these as candidate learning transitions, then refine through sources and review:

1. A position statement needs an origin, directions, reference object and time.
2. An arrow represents a named vector; arrow length is not automatically physical scale.
3. A component is signed along a chosen axis; magnitude is nonnegative.
4. Subtraction means reverse the second vector, then add; translate free vectors without rotating them.
5. Define the order of the subscripts: A relative to B is not B relative to A.
6. Construct relative position from two positions at the same instant.
7. Compare changes over the same interval to obtain relative velocity; explain each subtraction.
8. Reconcile the component calculation with a vector construction and a common-frame motion table.
9. Test limiting cases: equal velocities, stationary observer, reversed observer order.
10. Model a new context only after naming the frames and defining what each speed measures.

Each transition needs a teachable explanation and a way for the student to check understanding. These ten candidates are not a compulsory node count.

## Cross-Core differentiation example

For the shared idea “A relative to B”:

| Core | Intended learner action |
|---|---|
| 1A | Follow the derivation from same-time positions, with a completed vector construction and meanings. |
| 1B | Predict what B observes, reconstruct the subtraction order and explain why reversing the observer reverses the vector. |
| 2A | Solve a traceable quantitative example, inspect the complete reasoning and check its units/direction. |
| 2B | Select the correct frame in a different task, reject a plausible wrong model and justify a representation before calculation. |

A boat question with only different numbers from a worked boat example is same-family practice. It is not automatically new transfer.

## Arithmetic control for the evaluator, not the whole lesson

Use an **author-created benchmark**, not an invented CBSE item. In a fixed east/north Cartesian frame, let A have velocity `(6, 0) m/s` and B `(0, 8) m/s`. Then A relative to B is `(6, -8) m/s`, with magnitude `10 m/s`. It points southeast, with the eastward component positive and northward component negative. Reversing observer order changes the sign of the vector but not its magnitude. An independent same-time position table over one second should give the same relative displacement.

The vector drawing must show B's velocity reversed before addition, preserve a common length scale, and reconcile with the component result. The benchmark is public to the author; passing it alone proves little. A reviewer should also choose different values/orientations and one conceptual case unseen during authoring. Do not use a reviewer holdout as a teaching example before the test.

## Synthetic practice-profile probes

| Profile | Evidence supplied to the test | Expected design response |
|---|---|---|
| Low | Hypothetical learner can read a number line but confuses vector/magnitude and observer order; 30% is a synthetic label only. | Bridge these capabilities, use graphical/perpendicular cases, retain full explanations. |
| High with gap | Hypothetical 85% aggregate; component arithmetic demonstrated, frame naming not demonstrated. | Do not infer frame mastery; include targeted repair before complex model choice. |
| Unknown with waiver | No measured knowledge. Owner requests a simple-to-challenging route. | Keep UNKNOWN visible, offer checks and optional support; avoid personalized-readiness claims. |

Keep Core1A/1B intrinsic coverage fixed across these profiles. The extension and the lower-support practice slice must not silently change their depth contract.

## Required honest result

Produce as much of the six-product draft as supported, and show exactly where missing frozen-source authority, subject evaluation, visual tooling or independent review limits acceptance. A compiler receipt alone is not the learner-product deliverable. This template exercise is separate from PR #391's V2 architecture stress receipt; do not copy its PASS status or blocked prerequisite results into this run.
