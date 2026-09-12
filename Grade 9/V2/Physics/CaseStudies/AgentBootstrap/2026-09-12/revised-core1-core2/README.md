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
- All 55 pages were re-rendered after the final layout/figure fixes and representative pages were visually reviewed.

### 3. Newton's Laws of Motion - NEXT

Rebuild Core 1 and Core 2 together. Core 1 should teach the canonical reasoning chain `choose body -> identify interactions -> draw FBD -> choose axes -> resolve forces -> ΣF=ma -> interpret/check`. Core 2 hints must ask open-ended questions about body choice, force ownership, FBD/axes and the first force equation before revealing each rung.

## Existing Motion in 2D case study

The Motion in 2D work remains the principal case study that established the revised Core 2 hint/solution architecture. Its previous PDFs are regression evidence; the topic-by-topic programme applies the same standard consistently across the remaining completed Physics topics.

## Answer requirement

Every learner question must have an explicit answer artifact. Quick checks, verification and rubrics supplement the answer; they do not substitute for it.

## Handoff rule

Every completed topic must leave a README/build contract, QA audit, reproducible generator when practical, and the final learner artifacts or a self-contained handoff bundle. A later agent should be able to continue from the topic folder without reconstructing the design history from chat.
