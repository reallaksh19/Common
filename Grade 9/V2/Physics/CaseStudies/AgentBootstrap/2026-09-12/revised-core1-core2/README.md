# Motion in a Plane - Revised Core 1 and Core 2

This folder is the current handoff target for the revised Physics learner-product format. The work is now proceeding **topic by topic**, completing Core 1 and Core 2 together before moving to the next chapter.

## Frozen learner format

### Revised Core 1

Each important competency must build the learner's reasoning machinery before transfer:

`physical picture -> What is happening? -> Key idea -> How it works -> Worked example -> Guided try -> Faded try -> Watch out / anti-trigger -> Quick check + answer`

A competency is not considered taught merely because its formula is listed. Core 1 must establish recognition, representation, mechanism, relation construction/selection, validity, execution, interpretation and checking. Spatial competencies require concept-native diagrams.

### Revised Core 2 attempt pages

`question -> problem representation -> H1 -> H2 -> H3 -> exactly two writing lines`

Hints use a **paired prompt + reveal contract**. Each rung contains an open-ended learner question followed by a directly related reveal:

1. **H1 - What is the key physics?** Ask about the decisive event/state/invariant/direction/frame. Reveal only the corresponding physical clarification.
2. **H2 - How would you represent it?** Ask for the axes/components/diagram/graph/frame/geometry. Reveal the matching representation and governing relation/figure.
3. **H3 - What would you write first?** Ask for the first executable mathematical constraint. Reveal that starting equation/construction only; do not solve it.

Every hint must be self-contained when revealed. Prompt/reveal mismatch, later-rung leakage and final-answer leakage are publication failures.

### Revised Core 2 worked pages

`question recap -> exact representation / known state -> reasoning ladder -> Answer -> Quick check -> Check it another way -> Watch out -> Review this idea`

The full reasoning ladder is:

1. UNDERSTAND
2. REPRESENT
3. CONNECT
4. CALCULATE
5. INTERPRET

Step completeness is required: no algebraic, geometric, sign, unit-bearing, state-transition or direction step needed by the learner may be silently skipped. Compactness comes from typography and dynamic layout, not from deleting reasoning.

## Layout and typography gates

- learner-readable font sizes; no microtype to rescue overflow
- proper mathematical symbols, subscripts, superscripts and Greek letters
- content-height cards/ladder rows rather than large fixed empty rectangles
- figures constrained to their semantic pane and large enough to teach
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
- Every final PDF page was re-rendered; representative concept, practice, attempt, key and solution pages were visually reviewed.

### 2. Motion in 1D - NEXT

The next topic should be rebuilt as a Core 1/Core 2 pair using the same frozen contracts. In particular, generic phase diagrams must be replaced by concrete event/state representations, delayed-start problems need dual-track timelines, graph reasoning must be explicit, and the Core 2 hints must use the paired open-question/reveal contract.

## Existing Motion in 2D case study

The Motion in 2D work remains the principal case study that established the revised Core 2 hint/solution architecture. Its previous PDFs are regression evidence; the topic-by-topic programme now applies the same standard consistently across the remaining completed Physics topics.

## Answer requirement

Every learner question must have an explicit answer artifact. Quick checks, verification and rubrics supplement the answer; they do not substitute for it.

## Handoff rule

Every completed topic must leave a README/build contract, QA audit, reproducible generator when available, and the final learner artifacts or a self-contained handoff bundle. A later agent should be able to continue from the topic folder without reconstructing the design history from chat.
