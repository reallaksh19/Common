# Core (1A) SBA Agent Runbook

This file is the **normative execution order** for any agent continuing Core (1A). Do not improvise the sequence. If this runbook conflicts with older prose guidance, this runbook and the machine-validated contracts take precedence.

## Start here

Before touching content, read these files in order:

1. `AGENT_RUNBOOK.md`
2. `README.md`
3. `CORE1A_UI_SPEC.md`
4. `SOURCE_COMPLETENESS_SPEC.md`
5. `registry/physics-core1a-motion-in-a-plane-build-state-v1.json`
6. `registry/physics-core1a-motion-in-a-plane-sba-v1.json`
7. `registry/physics-core1a-motion-in-a-plane-sba-publication-index-v1.json`
8. the target bucket profile, if present
9. the target bucket transfer-routine registry, if present
10. `registry/physics-core1a-core2-linkage.json`

Then run `python Grade 9/V2/Physics/Core1A/engine/next_sba.py` to confirm the next active bucket.

## Non-negotiable architecture

Core (1) is semantic authority: **what must be taught**.

Core (1A) is the learner-assimilation layer: **how this bucket must be taught to the declared learner profile so that the learner can independently attempt the linked Core (2) questions**.

Core (1A) is not a prettier Core (1), not a summary sheet, and not a reverse-engineered answer key.

For the current queue, build dedicated PDFs only for buckets with one or more primary Revised Core (2) v2 questions. Buckets with zero primary questions remain in the SBA map but are `SKIP_NO_PRIMARY_CORE2`.

## Mandatory build state machine

Every active SBA bucket passes these gates in this exact order. A later gate must not be marked complete while an earlier gate is incomplete.

### G0 — INDEX_SYNC

Update the published SBA bucket table first.

Required evidence:
- target bucket exists in the canonical SBA registry;
- origin, teaching home, primary Core (2) questions and state match the canonical registry;
- the publication index is the first publication surface for the bucket sequence.

### G1 — SOURCE_AND_CORE2_AUDIT

Read the source/Core (1) basis and every primary Core (2) question plus H1/H2/H3 reveals.

Required outputs:
- exact prerequisite concepts;
- all source equations/illustrations needed;
- every H1/H2/H3 reveal mapped to a proposed learning atom;
- source gaps or QC issues explicitly recorded rather than silently repaired.

### G2 — DIFFICULTY_AND_READINESS

Record intrinsic difficulty separately from learner readiness.

Current priority learner profiles:
- 20% usable prior knowledge;
- 50% usable prior knowledge.

For 20% learners, assume vocabulary, representation choice, sign convention, prerequisite recall and equation selection may all be fragile unless explicitly checked.

### G3 — LEARNING_ATOM_DECOMPOSITION

Decompose the bucket into the smallest meaningful teaching atoms.

Each atom requires:
- purpose;
- prerequisite support;
- staged teaching moves;
- visual-stage count;
- misconception targets;
- at least one check.

Rule: **harder concept or lower readiness = more pictures and fewer inferential jumps, not denser text**.

### G4 — CORE2_HINT_PRETEACH_AUDIT

Every primary Core (2) question must have H1/H2/H3 mapped to earlier Core (1A) teaching evidence.

- H1 = key physics already taught;
- H2 = representation/model already taught;
- H3 = first mathematical move already demonstrated or practised.

If any reveal is new in Core (2), the Core (1A) bucket is incomplete.

Question release may be delayed by another prerequisite bucket.

### G5 — PROBLEM_FAMILY_ASSIMILATION

Do not map many Core (2) questions as one undifferentiated list. Cluster them into **problem families** with distinct recognition and solution routines.

Question-load planning rule:
- 1–2 primary questions: LOW load; at least 1 transfer routine;
- 3–5: MEDIUM; split whenever the recognition signal or first move differs;
- 6–9: HIGH; expanded transfer section, normally at least 3 routines;
- 10+: VERY_HIGH; explicit family map required, normally at least 5 routines.

A transfer routine must contain:
1. `LOOK FOR` / recognition signals;
2. numbered STEP 1 → STEP N method;
3. one fully worked or already-taught analogue before independence;
4. **INDEPENDENT PRACTICE** with blank attempt space or equivalent attempt-first presentation;
5. H1/H2/H3 optional hints after the attempt, not pre-exposed as a mini-solution;
6. `READY TO MOVE ON?` gate;
7. exact Core (2) release targets.

### G6 — PAGE_PLAN

The publication plan must be explicit before rendering.

For a 20% learner, use this macro-order unless a documented reason requires otherwise:

`SBA INDEX → FOUNDATION/PRETRAINING → CONCEPT BUILD → PICTORIAL STAGES → PICTURE-TO-MATHS → MISCONCEPTION → WATCH ONE → COMPLETE ONE → PROBLEM-FAMILY ROUTINE(S) → INDEPENDENT PRACTICE → HINTS → READINESS → CORE (2) TRANSFER SUMMARY`

For HIGH/VERY_HIGH question load, the transfer section must grow with the number of distinct problem families; do not compress 10+ questions into one end-page list.

### G7 — RENDER_AND_VISUAL_AUDIT

Render the PDF to page images and inspect all pages.

Reject:
- clipped titles/badges;
- label collisions;
- raw math strings;
- text below font floors;
- unexplained equations;
- hints visible before the independent attempt when the design claims progressive reveal;
- D2/D3 difficult ideas with only static text and no staged representation;
- Core (2) question numbers without an explicit family/method bridge.

### G8 — READINESS_AND_TRANSFER_AUDIT

Each released problem family needs a readiness gate covering four abilities:

1. **RECOGNISE** — identify the family from the question signals;
2. **REPRESENT** — draw/write the correct model without help;
3. **FIRST MOVE** — choose the first useful equation/condition without H2/H3;
4. **FINISH** — solve a fresh analogous problem and check the result.

Recommended release rule: 4/4 without H2/H3. Otherwise route the learner back to the named atom/routine.

### G9 — MACHINE_QA_AND_HANDOFF

Before handing off:
- run all Core1A tests;
- validate JSON files;
- confirm the target build manifest is `COMPLETE`;
- update build-state so `next_active_bucket` points to the next non-skipped bucket;
- add a PR progress comment only after CI passes.

## Required files per active bucket

Each active bucket should eventually have:

- canonical row in `physics-core1a-motion-in-a-plane-sba-v1.json`;
- row in `physics-core1a-motion-in-a-plane-sba-publication-index-v1.json`;
- 20% profile JSON when built for the 20% pathway;
- transfer-routine JSON when Core (2) questions exist;
- build manifest under `registry/build-manifests/`;
- learner PDF + montage during production;
- machine tests that prove primary-question coverage and release rules.

## Gold-standard references

Use these completed buckets as pattern references, but copy the **process**, not their exact page counts:

- `M2D-SBA-03`: LOW question load; one main transfer routine; independent practice + hidden/progressive hints + readiness.
- `M2D-SBA-04`: HIGH load; several distinct velocity-event routines; cross-bucket release for Q14/Q27.
- `M2D-SBA-05`: VERY_HIGH load; family map first; multiple routines; transfer section expands substantially because 13 primary questions are covered.

## Stop conditions

Do not continue rendering if any of these are true:

- primary question ownership is ambiguous;
- a Core (2) hint reveal has no prior teaching home;
- source support is unclear and the bridge would require invented physics;
- a high-load bucket has not been split into problem families;
- independent practice is missing;
- readiness is missing;
- publication index is stale;
- the next bucket cannot be derived unambiguously from build-state and the canonical SBA registry.

The goal is not to guarantee that a future agent never makes a mistake; the goal is to make deviations **visible, testable and build-failing** rather than dependent on memory.