# Physics V2 — Assessment Intake (P-A)

Implements issue #249 under the assessment-first Physics roadmap #248 / programme #234.

## Runtime boundary

Every real Physics generation starts from:

```text
QuestionSet              REQUIRED
AttemptSet               OPTIONAL
DeclaredTopicScope       REQUIRED
```

This directory owns normalization, stable question identity, explicit attempt binding, exact source-content fidelity metadata, exact Physics representation custody, and the deterministic `AssessmentIntakeEnvelope`.

It does **not** own source-integrity/item-validity judgment, scope/capability/model resolution, learner diagnosis, Core (1), Core (2), PCK, or publication.

## Authority status

The intake lifecycle shapes intentionally parallel the Mathematics M-A pilot, but this Physics implementation does not treat the Mathematics folder as shared authority. P-A is the second-subject falsifier needed before any genuinely shared contract promotion. Physics-specific representation semantics remain subject-owned.

## Source digest semantics

Each normalized question carries `source_provenance.source_digest`, the SHA-256 of canonical JSON containing the complete frozen source-facing payload:

```text
question identity/order/marks/stem
subparts
MCQ options
givens
units
figure / graph / option-figure representations
time intervals
stated frame
stated positive direction
stated model assumptions
source answer-key assertion
source locator
```

Each representation also carries its own `representation_digest`. Extraction/review metadata are excluded from source-content identity.

`QuestionSet`, `AttemptSet`, `DeclaredTopicScope`, and `AssessmentIntakeEnvelope` also carry deterministic SHA-256 digests computed over canonical JSON with their own digest field omitted.

## Physics source-shape custody

`source_shape` freezes counts for:

```text
options
subparts
figures / source representations
units
graph axes
vector directions
missing/truncated figures
```

This allows P-A to fail closed on loss or drift before later Physics interpretation.

A graph is source content, not decoration. Its axes, quantities, units, positive directions, scale text and origin text are preserved. A motion/vector diagram preserves vector direction labels. A missing/truncated figure remains explicitly missing/truncated; P-A cannot invent a replacement.

## Attempt binding

Attempts bind only through stable IDs:

```text
question_ref
part_ref?
representation_refs[]
binding_method = EXPLICIT_ID
```

Page order may remain provenance but cannot be the identity mechanism. An attempt that used a graph/diagram may bind that exact source representation.

## Low-confidence extraction

Low confidence is not silently upgraded. The envelope exposes:

```text
minimum_extraction_confidence
low_confidence_question_refs[]
human_correction_event_count
representation_count
graph_representation_count
missing_or_truncated_representation_refs[]
```

The current pilot threshold is `0.90`; this is an intake-quality signal only, never learner diagnosis.

## Fixture

The repository-safe Motion fixture contains 14 public-synthetic Grade-9 items spanning distance/displacement, speed, acceleration, nth-second semantics, gravity, graph reading, relative motion, moving release and multi-phase motion.

It deliberately includes:

- ordinary MCQ options;
- four option figures;
- a velocity-time graph with explicit axes/sign/scale;
- vector-direction source semantics;
- a multi-phase motion strip;
- one missing/truncated graph dependency;
- a three-part item;
- low-confidence source extraction;
- an optional de-identified attempt set with explicit representation bindings.

No item-validity or learner-diagnosis decision is made in P-A.

## Validation

```bash
python -m pip install 'jsonschema>=4.20,<5'
python 'Grade 9/V2/Physics/AssessmentIntake/contracts/validate_contracts.py'
python 'Grade 9/V2/Physics/AssessmentIntake/tests/test_physics_assessment_intake.py'
```

Deterministic replay:

```bash
D='Grade 9/V2/Physics/AssessmentIntake'
python "$D/engine/build_physics_assessment_intake.py" \
  --questions "$D/fixtures/motion-question-set.fixture.json" \
  --topic-scope "$D/fixtures/motion-topic-scope.fixture.json" \
  --attempts "$D/fixtures/motion-attempt-set.fixture.json" \
  --out /tmp/a.json --intake-id DET
python "$D/engine/build_physics_assessment_intake.py" \
  --questions "$D/fixtures/motion-question-set.fixture.json" \
  --topic-scope "$D/fixtures/motion-topic-scope.fixture.json" \
  --attempts "$D/fixtures/motion-attempt-set.fixture.json" \
  --out /tmp/b.json --intake-id DET
cmp /tmp/a.json /tmp/b.json
```
