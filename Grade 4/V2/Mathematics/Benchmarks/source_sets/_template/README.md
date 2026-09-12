# Source-set template — scanned Grade 4 Math questions

Copy this entire directory before editing it.

Recommended destination:

```text
Grade 4/V2/Mathematics/Benchmarks/source_sets/<source_set_slug>/
```

Use lowercase `snake_case` for `<source_set_slug>`.

## Inputs

Required:

```text
one or more scanned/photo images containing questions or topic prompts
```

Optional:

```text
topic labels supplied by the user
learner-work scans/transcriptions
teacher corrections/annotations
curriculum/source authority refs
```

## Files

```text
source.json
  faithful transcription/provenance only

build_fixture.py
  explicit semantic extraction into PrimaryMathInput/QuestionEvidence

production_fixture.py
  optional upstream representation-selection refinements discovered by visual QA

study_journey_fixture.py
  document-level teaching synthesis; groups questions into concepts/modules/blocks
```

## Mandatory order

1. Fill `source.json` from the image.
2. Record ambiguity/defects; do not repair the source.
3. Fill `QUESTION_SPECS` in `build_fixture.py` explicitly.
4. Run the authoring/LearningDesign validators.
5. Build `study_journey_fixture.py` by concept synthesis, not source-page order alone.
6. Use `production_fixture.py` only for upstream representation improvements found during QA.
7. Render.
8. Run source-specific acceptance + PDF render/visual QA.

## Source transcription rules

`source.json` is evidence. Keep wording, quantities, choices and visible mathematical notation faithful to the scan.

Do not silently convert:

```text
unclear symbol → assumed symbol
cropped number → guessed number
wrong printed answer → corrected answer
ambiguous diagram mapping → invented mapping
invalid physical story → rewritten valid story
```

Instead attach `source_issue`, for example:

```text
CROPPED_SOURCE: final option is not fully visible
ILLEGIBLE_SOURCE: denominator cannot be read confidently
PHOTO_MAPPING_UNCERTAIN: exact diagram-to-label order is unclear
DEFECTIVE_PRINTED_ITEM: stated quotient/remainder violates the mathematical rule
SEMANTICALLY_INVALID_STORY: source arithmetic intent exists but the physical story is not meaningful
```

## Semantic extraction rules

`build_fixture.py` intentionally starts with an empty `QUESTION_SPECS` mapping and fails closed until every question is explicitly mapped.

For each question provide:

```text
concept_key
concept_title
scope_basis
capability_refs
prerequisite_refs
problem_family_refs
translation_refs
quantity_structure
representation_requirements
learning_support_blueprint
```

Use canonical registry IDs. Do not create a source-local ontology.

A scan normally establishes:

```text
QUESTION_SET_OBSERVED
```

not universal Grade-4 curriculum scope.

## Study-journey rules

`study_journey_fixture.py` also fails closed until an explicit StudyJourney exists.

Do not mechanically create one module per source question.

Ask instead:

```text
Which questions exercise the same underlying concept?
Which prerequisite bridge is necessary to teach that concept?
Where is a worked example justified?
Where must the learner attempt independently?
Which errors deserve explicit contrast?
Where should retrieval/transfer happen later?
```

A high-quality final study guide should normally include a deliberate subset of:

```text
SEE_DISCOVER
NOTICE
CONNECT
WORKED_EXAMPLE
GUIDED_TRY
INDEPENDENT_TRY
ERROR_ANALYSIS
TRANSFER
RETRIEVAL
REFERENCE
SELF_CHECK
```

## Production refinement rule

If QA shows a visual is insufficient, modify the upstream representation selection in `production_fixture.py` or the semantic fixture.

Do not write source-question-specific pedagogy into the PDF renderer.

## Reference implementation

Use this only as an implementation example:

```text
../pupil_pages_97_99/
```

It demonstrates:

- source defect preservation;
- explicit semantic mapping;
- typed visual/support plans;
- production representation refinements;
- concept-level StudyJourney synthesis.

Do not copy its question values, capability selection or teaching sequence into a different source set unless the new source independently supports them.
