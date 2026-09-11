# Primary Mathematics Work Evidence and Quantity Structure

**Status:** v1 canonical extension candidate  
**Authority:** `reallaksh19/Common`  
**Tracking:** Common #162  
**Programme runtime:** Study-Hub #45

## 1. Why this extension exists

A final answer is often too weak an observation for Grade 4–5 mathematics.

A notebook page may show that a child:

- selected the correct or wrong operation;
- generated a useful multiplication table;
- decomposed a number correctly;
- lost a place-value position inside a written algorithm;
- self-corrected one line but not another;
- used a visual or symbolic representation;
- converted, or failed to convert, a unit such as `dozen`;
- understood the concept but made a transient calculation slip.

Therefore Primary Math must preserve **observable mathematical work** separately from the Teacher Runtime judgement formed from that work.

The runtime path is:

```text
CHILD WORK / SOURCE ARTIFACT
        ↓
MATHEMATICAL WORK EVIDENCE
        ↓
ERROR SIGNATURE / STRUCTURAL PATTERN
        ↓
BOUNDED RESPONSE DIAGNOSIS
        ↓
SMALLEST DISCRIMINATING PROBE
        ↓
TEACHER DECISION / MOVE
        ↓
INDEPENDENT RETRY
```

`MathematicalWorkEvidence` is evidence, not diagnosis.

## 2. Canonical boundary

Common owns the semantics of:

- `MathematicalWorkEvidence`;
- `WorkStep`;
- `QuantityStructure`;
- `StrategySupportEvidence`;
- `MathErrorSignature`;
- contrast-based diagnostic evidence.

Study-Hub may ingest notebook/classwork observations and serialize the evidence.

Kani may emit the same evidence fields only when its runtime actually observes them.

Neither renderer may infer durable mastery, misconception, or learner traits from a work trace alone.

## 3. MathematicalWorkEvidence

Recommended semantic shape:

```yaml
mathematical_work_evidence:
  workEvidenceId: MWE-...
  learningObjectIds: []
  sourceRef: optional
  observedAt: ...
  provenance: CHILD_WORK | TEACHER_TRANSCRIPTION | SYSTEM_OBSERVED | SOURCE_RECONSTRUCTED

  finalResponse:
    value: ...
    correctness: CORRECT | INCORRECT | PARTIAL | NOT_SCORED

  selectedOperation: DIVISION | MULTIPLICATION | ADDITION | SUBTRACTION | MIXED | NOT_OBSERVED

  workSteps: []
  quantityStructure: optional
  representations: []
  strategySupports: []
  selfCorrections: []
  teacherAnnotations: []
```

Only directly observable or explicitly reconstructed information belongs here.

If a step cannot be read with confidence, record `AMBIGUOUS`/`NOT_OBSERVED` rather than inventing it.

## 4. WorkStep

A `WorkStep` preserves ordered intermediate evidence.

```yaml
work_step:
  stepId: WS-01
  sequence: 1
  kind: OPERATION_SELECTION | FACT_RETRIEVAL | PARTIAL_PRODUCT | PARTIAL_QUOTIENT |
        SUBTRACTION | BRING_DOWN | PLACE_VALUE_WRITE | UNIT_CONVERSION |
        REPRESENTATION | ESTIMATE | CHECK | OTHER
  observedValue: ...
  status: CORRECT | INCORRECT | PARTIAL | AMBIGUOUS | NOT_SCORED
  sourceRegionRef: optional
```

The evidence model must allow mixed success inside one incorrect solution.

Example:

```text
7843 ÷ 13

✓ identifies divisor 13
✓ uses 13 × 6 = 78
✓ subtracts 78 from 78
✓ brings down 4
✗ does not preserve the zero quotient place reliably
✓ later reasons with 43
```

This should not collapse to `incorrect division`.

## 5. QuantityStructure

Word problems must be representable as relationships among quantities, units, roles, and unknowns before an operation is judged.

Recommended shape:

```yaml
quantity_structure:
  quantities:
    - quantityId: Q1
      value: 23
      unit: DOZEN_EGGS
      role: GIVEN

    - quantityId: Q2
      value: 12
      unit: EGGS_PER_DOZEN
      role: CONVERSION_FACTOR

    - quantityId: Q3
      value: 6
      unit: RUPEES_PER_EGG
      role: RATE

  unknown:
    unit: RUPEES

  requiredRelationships:
    - CONVERT_GROUPED_UNIT
    - MULTIPLY_QUANTITY_BY_RATE
```

The canonical sequence is:

```text
QUANTITY
→ UNIT
→ ROLE
→ RELATIONSHIP
→ UNKNOWN
→ OPERATION / OPERATIONS
```

Do not rely on keywords such as `each`, `shared`, `altogether`, or `per` as operation rules.

## 6. StrategySupportEvidence

A child-created support is not the same thing as conceptual help supplied by a teacher.

```yaml
strategy_support:
  type: MULTIPLES_TABLE | FACT_FAMILY | BAR_MODEL | NUMBER_LINE |
        PARTIAL_PRODUCT_TABLE | PLACE_VALUE_TABLE | DRAWING | OTHER
  role: PROVIDED | CHILD_SELECTED | CHILD_PRODUCED
  value: optional
```

Examples:

```text
teacher gives 13-times table      → PROVIDED
child chooses to use times table  → CHILD_SELECTED
child independently writes it     → CHILD_PRODUCED
```

A `CHILD_PRODUCED` support may be positive strategic evidence even when the final answer is wrong.

It must not automatically increase conceptual-support dependence.

## 7. TeacherAnnotation provenance

Teacher marks visible in a notebook are separate evidence from the child's work.

```yaml
teacher_annotation:
  annotationId: TA-...
  kind: TICK | CROSS | CORRECTION | PROMPT | COMMENT | MODELLED_STEP | OTHER
  value: ...
  provenance: TEACHER
```

Rules:

- never merge teacher-written correction into the child's work trace;
- never treat a teacher's corrected answer as child independent evidence;
- when authorship is uncertain, use `AMBIGUOUS`.

## 8. MathErrorSignature

The Teacher Runtime diagnosis remains generic (`PROCEDURAL_ERROR`, `TASK_INTERPRETATION_ERROR`, etc.).

Math may attach a more precise, non-permanent error signature to evidence:

```text
DIV_QUOTIENT_ZERO_PLACE_VALUE
DIV_BRING_DOWN_SEQUENCE
DIV_PARTIAL_QUOTIENT_SELECTION
DIV_REMAINDER_INTERPRETATION
WORD_PROBLEM_WRONG_OPERATION
WORD_PROBLEM_UNKNOWN_ROLE_CONFUSION
UNIT_GROUP_NOT_EXPANDED
UNIT_RATE_CHAIN_MISSED
MULT_PARTIAL_PRODUCT_PLACE_VALUE
MULT_REGROUPING_ERROR
ROUNDING_PLACE_SELECTION
```

An error signature is an observed/author-classified pattern used to form a diagnosis. It is not itself a durable child label.

## 9. Contrast-based diagnostic evidence

Do not diagnose complex procedural understanding from one item when structurally related work is available.

A contrast set may contain:

```yaml
contrast_set:
  targetLearningObjectId: DIV-M6.6
  evidenceRefs:
    - MWE-366-DIV-12
    - MWE-3496-DIV-23
    - MWE-7843-DIV-13
  contrastDimension: ZERO_IN_QUOTIENT_REQUIRED
```

Example reasoning:

```text
366 ÷ 12   → zero quotient place required
7843 ÷ 13  → zero quotient place required
3496 ÷ 23  → no zero quotient place required
```

If difficulty clusters on the first two while the third is materially stronger, the runtime may raise the hypothesis:

```text
PROCEDURAL_ERROR
  error_signature: DIV_QUOTIENT_ZERO_PLACE_VALUE
```

with stronger confidence than any single item supports.

The runtime must still use an appropriately small probe before treating the hypothesis as established when the evidence is ambiguous.

## 10. Smallest discriminating probe

A diagnostic probe should isolate the suspected mechanism with minimal unrelated load.

For `DIV_QUOTIENT_ZERO_PLACE_VALUE`, suitable probes may include an age/scope-appropriate exact item where a zero quotient place is necessary, or a partially completed algorithm asking only what digit belongs in the next quotient place.

The probe should avoid simultaneously increasing:

- divisor complexity;
- language load;
- multi-step context;
- unfamiliar representation;
- fact-retrieval demand.

The purpose is diagnosis, not difficulty.

## 11. Notebook/classwork evidence rules

When source evidence is a photographed notebook or classwork page:

1. preserve the source artifact reference;
2. separate child writing from teacher annotations where reasonably observable;
3. record only legible/interpretable work steps;
4. record ambiguity rather than guessing;
5. preserve successful substeps as well as errors;
6. compare structurally related items before forming a broad diagnosis;
7. do not infer stable traits from handwriting, neatness, speed, erasures, or one page;
8. do not treat teacher correction as independent child evidence;
9. use source/classroom evidence to refine the school-scope overlay without silently changing universal Grade 4 scope.

## 12. School-scope observation

If classwork repeatedly includes a form that the generic Grade 4 schema marks as source-dependent, represent that as school/source scope evidence.

Example:

```yaml
school_scope_observation:
  learningObjectId: DIV-M6
  feature: MULTI_DIGIT_DIVISOR
  status: OBSERVED_IN_SCHOOL_CLASSWORK
  examples: [12, 13, 15, 23]
```

This does **not** modify the universal Grade 4 canonical scope.

## 13. Required runtime falsifiers

The architecture fails this extension if any of these occur:

- only the final answer is retained when intermediate work is available;
- a mixed-success work trace is collapsed to `weak in division`;
- a child-produced strategy is recorded as teacher-provided conceptual support;
- a wrong word-problem operation triggers algorithm reteaching without checking quantity structure;
- unit conversion/rate structure is ignored when it changes the required operation chain;
- teacher correction is counted as child independent success;
- one incorrect item creates a durable procedural trait;
- structurally contrasting evidence is ignored when forming a diagnosis;
- ambiguity in photographed work is silently reconstructed as fact.

## 14. Notebook regression fixture

The canonical v1 regression fixture should include at least these patterns:

```text
A. division word problem: total + number of groups → find amount in each group
B. division word problem where child chooses multiplication
C. dozen/rate problem requiring grouped-unit conversion before cost
D. multi-digit division requiring zero in quotient
E. contrasting multi-digit division without zero in quotient
F. child-generated multiplication/multiples table
G. successful rounding/estimation evidence preserved alongside other errors
```

Pass condition:

```text
final-answer evidence alone is insufficient
→ work trace preserved
→ quantity structure represented where relevant
→ strengths and errors coexist
→ diagnosis remains bounded
→ next probe targets the suspected mechanism
```
