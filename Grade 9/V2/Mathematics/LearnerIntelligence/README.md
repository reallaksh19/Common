# Mathematics V2 — M-E Learner Evidence and Diagnostic Inference

Implements #240 after merged M-A/M-B/M-C/M-D.

M-E is the stateful learner-evidence boundary. It does **not** change assessment scope, mathematical authority, item validity, problem-family semantics, StudyModel treatment, teaching choreography, hints, solutions, or publication.

```text
M-A QuestionSet + optional AttemptSet
        +
M-B diagnostic-use safety
        +
M-C capability authority
        +
M-D item/problem semantics
        ↓
LearnerEvidenceLedger        factual custody
        ↓
ReasoningObservation         reviewed observation, not diagnosis
        ↓
DiagnosticCase               cautious, recomputable inference
        ↓
LearnerStateSnapshot         descriptive current state
```

## Hard boundaries

`EVIDENCE != OBSERVATION != DIAGNOSIS != STATE != TREATMENT`.

The same QuestionSet + DeclaredTopicScope has the same scope fingerprint whether an AttemptSet is absent or present. `NO_ATTEMPT != WEAK`.

A wrong final answer cannot erase demonstrated upstream reasoning. An arithmetic or symbolic execution failure after a correct model is localized to the execution capability. One ordinary failure cannot confirm a misconception or produce `REPAIR_REQUIRED`.

M-B diagnostic-use policy remains authoritative. `POSITIVE_EVIDENCE_ONLY` and `EXCLUDE_FROM_NEGATIVE_INFERENCE` items cannot create negative learner state.

## Confidence

Observation confidence is capped by all available evidence confidence: reviewer observation confidence, M-A attempt extraction confidence, and M-A question extraction confidence. Learner-state confidence cannot exceed the observations supporting that state.

## Pilot acceptance cases

The M-A de-identified AttemptSet is reused directly. A repository-safe reviewed-observation fixture binds to exact attempt/step IDs. It proves that Q12 geometric modelling survives a later binomial-expansion failure, Q14 river-current modelling survives a downstream arithmetic failure, Q9 contributes positive evidence only, and transcription risk is retained as evidence-quality information rather than converted into mathematical weakness.

The observation registry also defines the M-E vocabulary required by #240, including equality-transformation, expression-identity, ordered-pair, slope-orientation, verification, and transcription observations.

## State semantics

M-E v1 emits `UNKNOWN`, `DEVELOPING`, or `READY`. It deliberately does not award `ROBUST` from a single assessment and does not emit `REPAIR_REQUIRED` from ordinary one-paper evidence. Durable transfer/retention and decisive diagnostic probes belong to later evidence updates.

## Non-claims

No psychometric mastery probability. No psychological-cause inference. No real learner identity. No automatic handwriting/OCR diagnosis. No Study Synthesis decision. No hint ladder or lesson sequence. No page/layout instruction.
