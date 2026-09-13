# Revised Core 1 and Core 2 - topic-by-topic Physics rebuild

This folder is the current handoff target for the revised Physics learner-product format. The work proceeds **topic by topic**, completing Core 1 and Core 2 together before moving to the next chapter.

## Frozen learner format

### Revised Core 1

Each important competency must build the learner's reasoning machinery before transfer:

`physical picture -> What is happening? -> Key idea -> How it works -> Worked example -> Guided try -> Faded try -> Watch out / anti-trigger -> Quick check + answer`

A competency is not considered taught merely because its formula is listed. Core 1 must establish recognition, representation, mechanism, relation construction/selection, validity, execution, interpretation and checking. Spatial competencies require concept-native diagrams.

### Revised Core 2 attempt pages

`question -> problem representation -> H1 -> H2 -> H3 -> exactly two writing lines`

Hints use a **paired prompt + reveal contract**. Each rung contains an open-ended learner question followed by a directly related reveal:

1. **H1 - What is the key physics?** Ask about the decisive event/state/invariant/direction/frame/body/system. Reveal only the corresponding physical clarification.
2. **H2 - How would you represent it?** Ask for axes/components/FBD/diagram/graph/frame/system boundary/geometry. Reveal the matching representation and governing relation/figure.
3. **H3 - What would you write first?** Ask for the first executable mathematical or logical constraint. Reveal that starting equation/construction only; do not solve it.

Every hint must be self-contained when revealed. Prompt/reveal mismatch, later-rung leakage and final-answer leakage are publication failures.

### Revised Core 2 worked pages

`question recap -> exact representation / known state -> reasoning ladder -> Answer -> Quick check -> Check it another way -> Watch out -> Review this idea`

The full reasoning ladder is:

1. UNDERSTAND
2. REPRESENT
3. CONNECT
4. CALCULATE
5. INTERPRET

Step completeness is required: no algebraic, geometric, sign, unit-bearing, state-transition, force-ownership or direction step needed by the learner may be silently skipped. Compactness comes from typography and dynamic layout, not from deleting reasoning.

## Layout and typography gates

- learner-readable font sizes; no microtype to rescue overflow
- proper mathematical symbols, subscripts, superscripts and Greek letters
- content-height cards/ladder rows rather than large fixed empty rectangles
- figures constrained to their semantic pane and large enough to teach
- exact problem-state figures on Core 2; do not squeeze a generic/full figure into a compact solution pane
- exactly two writing lines on Core 2 attempts
- object/bbox QA plus full PDF re-render after the final edit
- no learner-facing production/audit jargon

## Topic-by-topic status

### 1. Vectors - COMPLETE REVISED PAIR

See `vectors/`.

- Revised Core 1: 25 pages, 11 competency families.
- Revised Core 2: 30 pages, 14 protected transfer attempts, compact answer key and 14 full worked solutions.
- Core 2 uses the paired open-question/reveal hint mechanism.
- Automated final scan: zero out-of-bounds text blocks and zero severe overlap flags.

### 2. Motion in 1D - COMPLETE REVISED PAIR

See `motion-1d/`.

- Revised Core 1: 25 pages, 11 competency families.
- Revised Core 2: 30 pages, 14 protected transfer attempts, compact answer key and 14 full worked solutions.
- Core 1 explicitly teaches equation reconstruction, sign/reversal logic, phase boundaries, vertical-motion states and graph operations before transfer.
- Delayed-start/catch-up uses a concrete dual-track timeline rather than generic `phase 1 / boundary / phase 2` authoring labels.
- Core 2 uses self-contained open-question/reveal hints and problem-specific compact representations.
- Final automated scan: zero out-of-bounds text blocks and zero severe overlap flags in both PDFs.

### 3. Newton's Laws of Motion - COMPLETE REVISED PAIR

See `nlm/`.

- Revised Core 1: 25 pages, 11 competency families.
- Revised Core 2: 42 pages, 20 source-demand-aligned attempts and 20 full worked solutions.
- The Core 1 reasoning spine is `choose body/system -> identify interactions/state -> build FBD/system/graph -> select law -> execute -> check`.
- Core 2 represents all 20 direct Unit 9 demand families already recorded in the NLM reconciliation ledger.
- Q10 remains ambiguity-aware: the source's smooth-floor wording does not justify inventing frictional rolling torque.
- Core 2 figures are state-specific: braking and accelerating vehicle states are separated, frictionless puck pages do not invent horizontal forces, conservation pages show system boundaries, and force/mass tables use the actual problem state.
- Final automated scan: zero out-of-bounds text blocks, zero severe overlap flags, zero hint-pair failures.

### 4. Motion in 2D - NCERT CLASS IX EXEMPLAR SUBSET - COMPLETE

See `motion-2d-ncert/`.

This is deliberately a focused subset rather than a claim of full Motion in a Plane coverage.

- Source pool: Unit 8 Q1/Q6/Q11; Unit 10 Q4/Q16/Q17/Q18/Q22; Unit 9 Q5 as TRANSFER.
- Sample Paper I Q10 is explicitly deduplicated against Unit 8 Q1.
- Revised Core 1: 20 pages, 9 competency families.
- Revised Core 2: 20 pages, 9 protected attempts, compact answer key and 9 full worked solutions.
- Learner questions are paraphrased from source demands; source IDs are retained.
- The source boundary is explicit: no claim of complete oblique-projectile, boat/rain relative-velocity, angular-kinematics or non-uniform circular-motion coverage.
- Final scan: zero out-of-bounds text blocks and zero severe overlap flags in both PDFs.
- All pages were re-rendered after correcting figure geometry and learner-facing math typography.

### Work & Energy - SKIPPED FOR THIS REVISION PASS

Per user instruction, do not revise Work & Energy in this sequence unless explicitly reopened.

## Next topic

**Gravitation** - reconcile the full NCERT Class IX Exemplar Unit 10 demand surface first, then rebuild Core 1 and Core 2 together without double-counting the Motion-in-2D demands already isolated in `motion-2d-ncert/`.

## Answer requirement

Every learner question must have an explicit answer artifact. Quick checks, verification and rubrics supplement the answer; they do not substitute for it.

## Handoff rule

Every completed topic must leave a README/build contract, QA audit, reproducible generator when practical, and the final learner artifacts or a self-contained handoff bundle. A later agent should be able to continue from the topic folder without reconstructing the design history from chat.
