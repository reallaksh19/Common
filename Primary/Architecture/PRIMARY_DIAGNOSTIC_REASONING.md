# Primary Diagnostic Reasoning

**Status:** canonical v1 companion
**Authority:** `reallaksh19/Common`
**Tracking:** Common #162
**Programme runtime:** Study-Hub #45

## Purpose

This companion makes Primary Teacher Runtime diagnosis explicitly testable rather than model-intuitive.

The required reasoning path is:

```text
OBSERVABLE EVIDENCE
  -> STRUCTURAL FEATURES / CONTRAST SET
  -> 2-3 BOUNDED HYPOTHESES
  -> DIAGNOSTIC PROBE
  -> OBSERVED PROBE RESULT
  -> CONFIDENCE UPDATE
  -> TEACHER DECISION
  -> TEACHER MOVE
  -> INDEPENDENT RETRY
```

A diagnosis must not become a durable learner label merely because an agent can explain it plausibly.

## 1. Strategy production and strategy initiation are orthogonal

`CHILD_PRODUCED` describes who physically produced a representation/support. It does **not** prove that the child independently selected the strategy.

Use separate dimensions:

```yaml
strategy_support_evidence:
  strategyType: MULTIPLES_TABLE
  producedBy: CHILD | TEACHER | SYSTEM | UNKNOWN
  initiation:
    actor: CHILD | TEACHER | SYSTEM | UNKNOWN
    mode: SPONTANEOUS | GENERAL_PROMPT | STRATEGY_PROMPT | EXPLICIT_DIRECTION | UNKNOWN
  conceptualSupport:
    level: H0 | H1 | H2 | H3 | H4 | H5
    type: NONE | PROMPT | HINT | MODEL | THINK_ALOUD | WORKED_EXAMPLE
```

Invariant:

```text
CHILD_PRODUCED != CHILD_INITIATED != INDEPENDENT
```

A child-written multiples table after an explicit teacher direction is useful work evidence, but it is weaker evidence of strategic independence than a spontaneously initiated table.

## 2. Granular provenance belongs on meaningful work steps

Preserve provenance at the smallest **educationally meaningful step**, not at every pen stroke.

```yaml
work_step:
  stepId: WS-04
  kind: PLACE_VALUE_WRITE
  observedValue: "0"
  provenance:
    actor: CHILD | TEACHER | SYSTEM | UNKNOWN
    productionState: ORIGINAL | SELF_CORRECTED | CORRECTED_BY_OTHER | UNKNOWN
    supportState: INDEPENDENT | AFTER_GENERAL_PROMPT | AFTER_STRATEGY_PROMPT | AFTER_EXPLICIT_DIRECTION | UNKNOWN
  certainty:
    transcription: HIGH | MEDIUM | LOW
```

Teacher annotations remain separate objects:

```yaml
annotation:
  relationToStep: WS-04
  actor: TEACHER
  kind: CORRECTION | PROMPT | MARK | COMMENT | MODELLED_STEP | OTHER
  value: ...
```

Rules:

- teacher correction is never child independent evidence;
- child self-correction is still child work, but support context remains visible;
- ambiguous authorship or transcription remains explicit;
- do not create forensic stroke-level semantics when the educational step is sufficient.

## 3. ContrastSet is deliberate controlled comparison

The runtime must not merely compare several examples and discover an arbitrary pattern.

A `ContrastSet` states the intended focal feature and the background structure held substantially constant.

```yaml
contrast_set:
  contrastSetId: CS-DIV-ZERO-001
  targetLearningObjectIds:
    - DIV-M6.6
  focalFeature:
    id: QUOTIENT_ZERO_REQUIRED
  controlledSharedFeatures:
    - TWO_DIGIT_DIVISOR
    - MULTI_DIGIT_DIVIDEND
    - STANDARD_WRITTEN_DIVISION
  cases:
    - evidenceRef: MWE-366-DIV-12
      focalFeatureValue: true
    - evidenceRef: MWE-7843-DIV-13
      focalFeatureValue: true
    - evidenceRef: MWE-3496-DIV-23
      focalFeatureValue: false
```

The portable abstraction is:

```text
same important background structure
+ one deliberately varied diagnostic feature
```

This object is subject-neutral even when the feature vocabulary is subject-specific.

## 4. CompetingHypothesis

Before a discriminating probe, represent plausible alternatives explicitly.

```yaml
competing_hypotheses:
  - hypothesisId: H-DIV-GENERAL-PROCEDURE
    diagnosisCode: PROCEDURAL_ERROR
    errorSignature: DIV_GENERAL_LONG_DIVISION_PROCEDURE
    confidence: LOW
  - hypothesisId: H-DIV-ZERO-PLACE
    diagnosisCode: PROCEDURAL_ERROR
    errorSignature: DIV_QUOTIENT_ZERO_PLACE_VALUE
    confidence: MEDIUM
```

Keep the set small enough to guide action. Usually 2-3 hypotheses are sufficient for one probe.

## 5. DiagnosticProbe is a first-class runtime object

A diagnostic probe is not simply another practice question. Its purpose is to distinguish competing hypotheses with minimal unrelated load.

```yaml
diagnostic_probe:
  probeId: DP-DIV-ZERO-001
  hypothesisIds:
    - H-DIV-GENERAL-PROCEDURE
    - H-DIV-ZERO-PLACE
  manipulatedFeature:
    id: QUOTIENT_ZERO_REQUIRED
  controlledLoad:
    language: LOW
    representationNovelty: LOW
    factRetrievalDemand: LOW
    stepCount: SMALL
  items:
    - itemId: DP-DIV-NOZERO
      featureValue: false
    - itemId: DP-DIV-ZERO
      featureValue: true
  outcomeRules:
    - when:
        DP-DIV-NOZERO: CORRECT
        DP-DIV-ZERO: INCORRECT
      increasesHypothesis: H-DIV-ZERO-PLACE
    - when:
        DP-DIV-NOZERO: INCORRECT
        DP-DIV-ZERO: INCORRECT
      keepOpen:
        - H-DIV-GENERAL-PROCEDURE
        - H-DIV-ZERO-PLACE
      informationNeeded:
        - FACT_RETRIEVAL
        - PLACE_VALUE
    - when:
        DP-DIV-NOZERO: CORRECT
        DP-DIV-ZERO: CORRECT
      consider:
        - PERFORMANCE_LAPSE
        - RECENT_REPAIR
```

A probe must state:

1. which hypotheses it is intended to discriminate;
2. which feature it manipulates;
3. what load it deliberately holds low;
4. how major response patterns update the reasoning state.

## 6. Probe selection invariant

When multiple explanations remain plausible, choose the smallest probe expected to reduce uncertainty without introducing unnecessary difficulty.

Prefer:

```text
one-step recognition
partial algorithm completion
example/non-example contrast
controlled pair differing in one feature
small prerequisite check
```

over:

```text
longer word problem
harder arithmetic
new representation plus new vocabulary
whole-topic reteach
```

The purpose is information gain, not challenge.

## 7. Evidence families are composable, not universal requirements

Not every renderer observes the same evidence.

```text
LearningEvidence
  |- AttemptEvidence
  |- MathematicalWorkEvidence
  |- OralResponseEvidence
  |- TeacherObservationEvidence
```

A game renderer must not invent work steps it cannot observe. A notebook ingestion path may preserve intermediate work unavailable to the game.

Common owns the educational meaning of these evidence families. Renderers own only what they can faithfully observe and transport.

## 8. Division regression

The canonical regression uses:

```text
366 ÷ 12   -> zero quotient place required
7843 ÷ 13  -> zero quotient place required
3496 ÷ 23  -> comparable long division without the same zero-place feature
```

Expected reasoning:

```text
preserve mixed-success work traces
-> construct ContrastSet around QUOTIENT_ZERO_REQUIRED
-> maintain competing hypotheses
-> issue a small DiagnosticProbe
-> update confidence from the result
-> repair only the confirmed mechanism
-> require a new independent retry
```

The runtime fails if it jumps directly from the three examples to a durable statement such as `weak in division`.

## 9. Required falsifiers

The architecture fails this companion if any of the following occur:

- `CHILD_PRODUCED` is treated as proof of independent strategy selection;
- strategy initiation cannot distinguish spontaneous choice from explicit teacher direction;
- a contrast set lacks an explicit focal feature;
- the runtime compares structurally unrelated examples as if they formed a diagnostic contrast;
- a `DiagnosticProbe` has no competing hypotheses or no outcome interpretation;
- a diagnostic probe increases multiple unrelated loads unnecessarily;
- teacher correction is merged into child-original work;
- ambiguous authorship/transcription is silently resolved;
- a game renderer invents mathematical work steps it did not observe;
- a diagnosis is promoted to a durable learner trait without longitudinal evidence.
