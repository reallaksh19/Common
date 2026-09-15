# Primary Mathematics V2 — Benchmark Specification

## 1. Scope

This specification defines the independent benchmark used to judge a Grade 4–5 Primary Mathematics Core Skills v2 candidate.

The benchmark is **not** a universal Grade 4/5 curriculum. It is a test envelope proving that the engine can correctly support the common Primary Mathematics capability space without conflating question-derived school scope with universal grade truth.

## 2. Primary product contract under test

```text
INPUT
  question_set                    REQUIRED
  student_workout                 OPTIONAL
  topic_hints                     OPTIONAL

OUTPUT
  PrimaryMathCore1StudyGuide
  PrimaryMathCore2Companion
    Appendix A — Practice Batches
    Appendix B — Hint Ladder + Solutions
    Appendix C — Visual Quick Reference
```

The benchmark assumes an intermediate skill model exists. A candidate that renders directly from raw questions fails `RAW_QUESTIONS_RENDERED_DIRECTLY_WITHOUT_SKILL_MODEL`.

## 3. Acceptance assertions

Every benchmark case declares assertions from the following vocabulary:

```text
SCOPE_PROVENANCE
MATH_INVARIANT
REPRESENTATION_REQUIRED
REPRESENTATION_TRANSLATION
WRITTEN_WORK_ALIGNMENT
WORK_PROVENANCE
CORE1_COVERAGE
CORE2_PRACTICE_LINK
HINT_FADE
FRESH_INDEPENDENT_RETRY
SOURCE_FIDELITY
LAYOUT_CUSTODY
LEARNER_SURFACE
```

Assertions are judged from exported evidence. The implementation may use any renderer/backend as long as the exported evidence proves the assertion.

## 4. Scope provenance

The benchmark allows capability scope states such as:

```text
QUESTION_SET_OBSERVED
SCHOOL_CLASSWORK_OBSERVED
CURRICULUM_CONFIRMED
CURRICULUM_OVERLAY
COMMON_G4_5_CAPABILITY
EXTENSION
STRETCH
MAPPING_PENDING
SOURCE_NOT_PROVIDED
```

`CURRICULUM_CONFIRMED` is valid only when the candidate binds an explicit curriculum authority reference/version. The benchmark never infers universal grade scope from one school question.

Blocking falsifier:

```text
QUESTION_OBSERVED_SKILL_PROMOTED_TO_UNIVERSAL_GRADE_SCOPE
```

## 5. Deep benchmark A — Multiplication bridge

Canonical case: `23 × 6 = 138`.

Required truths:

```text
23 = 20 + 3
20 × 6 = 120
3 × 6 = 18
120 + 18 = 138
23 × 6 = 138
```

Required representational bridge:

```text
EQUAL GROUPS
→ ARRAY
→ AREA / DISTRIBUTIVE PARTITION
→ PARTIAL PRODUCTS
→ WRITTEN ALGORITHM
→ ESTIMATE / CHECK
```

The candidate must prove that the written method is connected to place value; a vertical algorithm alone is insufficient for the deep case.

Negative mutations include:

- area model labels `20 × 6` as `12`;
- partial products omit `18`;
- final product does not equal the sum of partial products;
- renderer reports the primitive but supplies no realized representation evidence.

## 6. Deep benchmark B — Division bridge

The Division family must prove four different semantic demands.

### B1 Sharing vs grouping

`24 ÷ 6 = 4` can mean:

```text
24 shared into 6 equal groups → 4 in each group
24 arranged in groups of 6 → 4 groups
```

The numerical equation is identical; the quantity roles are not. A candidate that collapses both meanings into one generic picture fails.

### B2 Internal quotient zero

Canonical cases:

```text
366 ÷ 12 = 30 R6
7843 ÷ 13 = 603 R4
3496 ÷ 23 = 152
```

For `366 ÷ 12` and `7843 ÷ 13`, once quotient construction has begun, an internal place whose current partial dividend is smaller than the divisor must preserve a zero quotient digit when positional continuity requires it. Leading quotient zeros are not required.

The oracle checks:

```text
12 × 30 + 6 = 366
13 × 603 + 4 = 7843
23 × 152 = 3496
0 <= remainder < divisor
```

The contrast exists to distinguish `QUOTIENT_ZERO_REQUIRED` from general long-division difficulty; it is not evidence that the learner is permanently weak in Division.

### B3 Remainder meaning

The same arithmetic remainder may map to different contextual answers:

```text
LEFTOVERS
FULL_GROUPS_ONLY
ROUND_UP_ONE_MORE_GROUP
REPORT_QUOTIENT_AND_REMAINDER
REMAINDER_IS_TARGET
```

The benchmark requires the answer form to be driven by the story quantity structure, not by a generic `q R r` formatter.

### B4 Quantity / unit chain

Canonical structure:

```text
23 dozen eggs
→ 23 × 12 eggs
→ rate per egg
→ money total
```

The candidate must make the unit change explicit. `23 × price_per_egg` is invalid when the quantity is 23 dozen.

## 7. Deep benchmark C — Fractions bridge

The candidate must prove that fractions are quantities, not only numerator/denominator strings.

Required cases:

```text
1/2 = 2/4 = 4/8
3/4 > 2/3 only after a valid comparison representation/strategy
1/4 + 2/4 = 3/4
1/2 + 1/4 = 3/4 using valid repartition/equivalent-fraction reasoning
```

Required representation obligations:

```text
EQUAL PARTITION
FRACTION STRIP or AREA MODEL
NUMBER LINE for measure interpretation
EQUIVALENCE BRIDGE
```

Negative mutations include unequal partitions presented as equal fractions and shaded counts inconsistent with the declared fraction.

## 8. Breadth benchmark cases

The corpus includes at least the following independent cases:

1. **Place value** — decomposition and regrouping; digit value must be position-correct.
2. **Decimal hundredths** — hundred-grid and number-line agreement.
3. **Measurement/unit conversion** — source/target units and conversion factor must reconcile.
4. **Perimeter vs area** — boundary measure must not be conflated with covering.
5. **Volume** — cube/layer count must reconcile with dimensions where dimensions are asserted.
6. **Angle** — rendered/declared angle relationship must be geometrically coherent.
7. **Data** — table, chart scale/key and plotted quantities must agree.
8. **Word problem quantity structure** — quantity → unit → role → relationship → unknown → operation(s).
9. **Error analysis** — wrong method must be explicitly marked as the object of comparison, never silently normalized into correct work.
10. **Notebook provenance** — child work, teacher annotation, self-correction and ambiguity remain distinguishable.

## 9. Notebook acceptance

The candidate export must distinguish:

```text
ORIGINAL_SOURCE_IMAGE
FAITHFUL_TRANSCRIPTION
STRUCTURED_REPLAY
AUTHORED_NOTEBOOK_EXAMPLE
```

A structured replay must not claim to be original handwriting.

Alignment invariants include:

```text
place-value columns remain aligned
decimal points remain aligned
fraction bars preserve numerator/denominator association
quotient digits remain associated with their dividend places
teacher correction is not child-original evidence
ambiguous work remains ambiguous
correct intermediate work is not erased by an incorrect final answer
```

## 10. Core 1 acceptance

A deep-case Core 1 module must show a representation bridge, not a text summary followed by exercises.

Expected learner sequence is compatible with:

```text
SEE / DISCOVER
NOTICE
MAKE / DRAW / REPRESENT
CONNECT
WATCH ONE WORKED EXAMPLE
TRY WITH SUPPORT
TRY INDEPENDENTLY
CHECK
```

The benchmark does not require those literal headings; it requires the pedagogical functions.

## 11. Core 2 acceptance

Appendix A must classify practice purpose using an explicit practice role such as:

```text
RECONNECT
BUILD
CHOOSE
MIX
TRANSFER
RETRIEVE
```

Appendix B must preserve:

```text
H0 TRY
H1 NOTICE
H2 REMEMBER
H3 REPRESENT
→ fresh H0 independent retry
```

Supported success is not independent success.

Appendix C is a visual/decision reference, not a prose cram sheet.

Core 2 links to Core 1 through stable semantic references. Hard-coded authored physical page numbers fail acceptance.

## 12. Candidate-export evidence

For each benchmark case the candidate must export enough neutral evidence to allow the oracle to recompute:

- case identity;
- scope basis and authority refs;
- mathematical values/relations used by the representation;
- representation roles realized;
- work provenance when applicable;
- Core1 and Core2 semantic refs;
- hint/retry support state;
- learner-surface text tokens or leak scan result;
- placement/custody evidence IDs;
- artifact digests where PDFs exist.

The benchmark does not accept an unsubstantiated boolean `pass` from the producer as proof.

## 13. Machine vs human acceptance

Machine acceptance may establish:

```text
CORPUS_INTEGRITY
SEMANTIC_CONSISTENCY
SCOPE_PROVENANCE_CONSISTENCY
REPRESENTATION_EVIDENCE_PRESENT
WORK_PROVENANCE_CONSISTENCY
CORE1_CORE2_LINKAGE
HINT_RETRY_CONTRACT
LEARNER_SURFACE_GUARD
ARTIFACT_CUSTODY
```

It does not establish:

```text
SUBJECT_CORRECTNESS_HUMAN_REVIEW
PEDAGOGICAL_DESIGN_HUMAN_REVIEW
ASSESSMENT_DESIGN_HUMAN_REVIEW
VISUAL_USABILITY_HUMAN_REVIEW
CHILD_USABILITY_HUMAN_REVIEW
MATURE_DESIGN_QUALITY_HUMAN_REVIEW
```

Those remain `PENDING` until real review is bound to the exact candidate.