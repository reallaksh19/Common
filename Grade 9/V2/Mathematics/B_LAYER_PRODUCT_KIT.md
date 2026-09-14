# Mathematics Core1B / Core2B — Static Open-Ended Self-Tutoring Kit

This kit is stacked on `v2-math-core1a-textbook-quality` (#351) and implements the B-layer half of the Mathematics self-teaching contract.

## Frozen upstream boundary

Core1A and Core2A remain upstream authorities. B layers do not redefine mathematical legality, learner state or curriculum scope.

```text
Core1A governed teaching output
+ existing upstream learner treatment
        ↓
Core1B static open-ended consolidation compiler
        ↓
fixed self-guided consolidation workbook

Core2A legal practice / challenge output
+ purpose
+ compile-time transfer ceiling supplied upstream
        ↓
Core2B static open-ended transfer compiler
        ↓
fixed self-guided transfer workbook
```

## Governing principle

```text
A = explanation-first / declarative self-teaching
B = elicitation-first / open-ended self-tutoring
```

The learner product does not branch while being used. There is no chatbot loop, live diagnosis, learner-state mutation, attempt ingestion, post-answer escalation or runtime repair routing. Static help is authored into the artifact before publication.

## Core1B job

Governing question:

> Can the learner reconstruct and independently use what was taught?

Core1B starts from a familiar mathematical neighbourhood and removes support while requiring reconstruction.

```text
OPEN QUESTION
→ TRY / PREDICT / SKETCH
→ MEANING HELP
→ REPRESENTATION HELP
→ CONCEPT HELP
→ FIRST-MOVE HELP
→ PROCEDURE HELP
→ ANSWER + EXPLANATORY VERIFICATION
```

Its paper-native objects include method comparison, correct/wrong contrast, controlled variation, completion, fixed fading and close independent consolidation. It cannot add new mathematics.

## Core2B job

Governing question:

> Can the learner recognize, select and transfer the mathematics when the surface changes and the method is not named?

```text
UNFAMILIAR / LESS-CUED QUESTION
→ ATTEMPT
→ RECOGNITION HELP
→ CONCEPT / STRUCTURE HELP
→ REPRESENTATION HELP
→ FIRST-MOVE HELP
→ METHOD HELP
→ ANSWER + EXPLANATORY VERIFICATION
```

Core2B compiles only Core2A-legal items and respects the upstream demand ceiling:

`M0_DIRECT → M1_CONTROLLED_VARIATION → M2_REPRESENTATION_TRANSFER → M3_INVERSE_TARGET → M4_HIDDEN_STRUCTURE → M5_METHOD_DISCRIMINATION → M6_FAMILY_DISCRIMINATION → M7_MULTI_STEP_SYNTHESIS → M8_MIXED_COMPETITIVE`

At method/family discrimination levels, labels are hidden so the learner must identify the structure rather than receive the classification from the page.

## Shared static contract

Both B products declare:

```text
delivery_mode = STATIC
pedagogy_mode = OPEN_ENDED
```

and carry a typed fixed help sequence. The compiler creates opportunities to attempt, reconstruct and transfer; it does not claim that the learner actually attempted, learned, retained or became transfer-ready.

## Validation families

1. `MATH-EQUIDISTANT-POINT-ON-AXIS` — coordinate constraint, equal-distance model, symmetry versus general method.
2. `MATH-LINEAR-SYSTEM-SOLVE` — variable meaning, two-condition modelling, substitution versus elimination.

Using two structurally different families prevents coordinate-geometry details from becoming hidden compiler policy.
