# Mathematics V2 — Assessment Intake (M-A)

Implements issue #236 under the assessment-first Mathematics roadmap #235 / programme #234.

## Runtime boundary

Every real Mathematics generation starts from:

```text
QuestionSet              REQUIRED
AttemptSet               OPTIONAL
DeclaredTopicScope       REQUIRED
```

This directory owns normalization, stable question identity, explicit attempt binding, exact source-content fidelity metadata, and the deterministic `AssessmentIntakeEnvelope`.

It does **not** own item-validity judgment, topic/capability resolution, learner diagnosis, Core (1), Core (2), PCK, or publication.

## Authority status

The contract names are deliberately generic because their data shape is not inherently Mathematics-specific, but in M-A they remain **Math-pilot / candidate-shared contracts**. They are not promoted as cross-subject shared authority merely because the Mathematics fixture passes. Generic promotion requires the cross-subject evidence/gates required by #234.

## Source digest semantics

Each normalized question carries `source_provenance.source_digest`.

It is the SHA-256 of canonical JSON containing:

```text
question_id
source_order
section
marks
stem
subparts
options
givens
figure_refs
units
answer_key
source_locator
```

Extraction/review metadata are intentionally excluded from that digest. Mutating source mathematics or source structure without the original evidence digest therefore fails closed.

`QuestionSet`, `AttemptSet`, `DeclaredTopicScope`, and `AssessmentIntakeEnvelope` each also carry deterministic SHA-256 digests computed over canonical JSON with their own digest field omitted.

## Source-shape custody

`source_shape` records the source-observed counts for:

```text
options
subparts
figures
```

This lets the intake gate reject option loss and merged/dropped subparts independently of later semantic interpretation.

## Attempt binding

Attempts may bind only by explicit stable IDs:

```text
question_ref
part_ref?
binding_method = EXPLICIT_ID
```

Page order may be retained as provenance, but it cannot be the identity mechanism.

## Low-confidence extraction

Low confidence is not silently upgraded. The envelope exposes:

```text
minimum_extraction_confidence
low_confidence_question_refs[]
human_correction_event_count
```

The current pilot threshold is `0.90`; this is an intake-quality signal only, not a learner diagnosis.

## Fixture

The repository-safe mixed Grade-9 fixture contains 14 heterogeneous items and an optional de-identified attempt set. It intentionally preserves structures needed by later phases, including MCQ options, short response, and a three-part item. Item validity is **not** decided in this phase.

## Validation

```bash
python -m pip install 'jsonschema>=4.20,<5'
python 'Grade 9/V2/Mathematics/AssessmentIntake/contracts/validate_contracts.py'
python 'Grade 9/V2/Mathematics/AssessmentIntake/tests/test_math_assessment_intake.py'
```

Deterministic replay:

```bash
D='Grade 9/V2/Mathematics/AssessmentIntake'
python "$D/engine/build_math_assessment_intake.py"   --questions "$D/fixtures/mixed-grade9-question-set.fixture.json"   --topic-scope "$D/fixtures/mixed-grade9-topic-scope.fixture.json"   --attempts "$D/fixtures/mixed-grade9-attempt-set.fixture.json"   --out /tmp/a.json   --intake-id DET
python "$D/engine/build_math_assessment_intake.py"   --questions "$D/fixtures/mixed-grade9-question-set.fixture.json"   --topic-scope "$D/fixtures/mixed-grade9-topic-scope.fixture.json"   --attempts "$D/fixtures/mixed-grade9-attempt-set.fixture.json"   --out /tmp/b.json   --intake-id DET
cmp /tmp/a.json /tmp/b.json
```
