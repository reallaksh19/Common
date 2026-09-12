# Grade 4 Mathematics V2 — START HERE

Use this file when the only project input is one or more **scanned images of questions/topics**, optionally with learner-work images or topic labels.

The required production path is:

```text
SCANNED SOURCE IMAGES
  ↓ faithful visual transcription; do not repair the source
SOURCE SET (`source.json`)
  ↓ explicit semantic extraction; no keyword guessing
QuestionEvidence / PrimaryMathInput
  ↓ deterministic authoring
Core1/Core2 semantic plans + RepresentationPlan
  ↓ LearningDesign
LearningRepresentationPlan / authoring handoff
  ↓ StudyDesign
StudyJourneyPlan
  ↓ Publication
StudyJourney PDF + Core2 companion
  ↓ Acceptance
machine gates + exact-artifact custody + human review
```

## 1. Do not start in Publication

Do **not** open the PDF composer and invent lessons, diagrams or hints directly from a scan.

Publication is downstream. It may measure, paginate and realize already-validated mathematical/learning objects. It may not decide scope, repair source defects, invent a teaching route, or manufacture mathematical values.

Canonical learner-product namespace:

```text
Grade 4/V2/Mathematics/
```

Reusable Primary/Common dependencies remain under:

```text
Primary/V2/Mathematics/
```

## 2. Create a source-set package

Copy the repository template:

```text
Grade 4/V2/Mathematics/Benchmarks/source_sets/_template/
```

into a new snake_case directory, for example:

```text
Grade 4/V2/Mathematics/Benchmarks/source_sets/my_scan_2026_09_12/
```

The source-set package contains:

```text
source.json
build_fixture.py
production_fixture.py
study_journey_fixture.py
README.md
```

The existing reference implementation is:

```text
Grade 4/V2/Mathematics/Benchmarks/source_sets/pupil_pages_97_99/
```

Read that implementation when a concrete example is needed. Do not copy its mathematics into a different source set.

## 3. Stage A — faithful visual source extraction

Read the uploaded/scanned image directly and transcribe only what can actually be supported by the image.

For every question preserve at least:

```text
question_ref
page / source region
raw_text
answer choices when visible
source_issue when needed
diagram/source observation when needed
```

`raw_text` is source evidence, not edited teaching prose.

### Preserve uncertainty and defects

Never silently repair a scan or workbook item.

Use explicit source notes such as:

```text
CROPPED_SOURCE: ...
ILLEGIBLE_SOURCE: ...
PHOTO_MAPPING_UNCERTAIN: ...
DEFECTIVE_PRINTED_ITEM: ...
SEMANTICALLY_INVALID_STORY: ...
MAPPING_PENDING: ...
SOURCE_NOT_PROVIDED: ...
```

Examples of prohibited behavior:

```text
cropped digit → guessed digit
bad printed remainder → silently corrected remainder
ambiguous diagram order → invented exact order
physically invalid word problem → rewritten into a valid story without a source note
```

A source defect may later be handled pedagogically, but the source record must remain faithful.

## 4. Stage B — semantic extraction

Edit `build_fixture.py` only after `source.json` is complete enough to support mapping.

Each source question must receive explicit evidence for the mathematics actually supported by the source:

```text
concept_key
concept_title
scope_basis
capability_refs[]
problem_family_refs[]
prerequisite_refs[]
translation_refs[]
quantity_structure when relevant
representation_requirements[]
learning_support_blueprint
ambiguity[]
source_refs[]
```

Use the canonical registries; do not invent local IDs:

```text
Grade 4/V2/Mathematics/CoreSkills/registry/
Primary/V2/Mathematics/CoreSkills/registry/
```

The deterministic authoring engine deliberately does not infer full pedagogy from question keywords. If semantic evidence is unresolved, keep it unresolved or fail closed.

### Scope rule

A scanned question proves observed/project scope, not universal Grade-4 curriculum truth.

Default source basis for a scan is normally:

```text
QUESTION_SET_OBSERVED
```

Use `CURRICULUM_CONFIRMED` only when an actual reviewable curriculum authority is bound.

## 5. Stage C — LearningDesign

The semantic fixture must provide or resolve the learner-support blueprint before publication.

The blueprint owns:

```text
learner_prompt
primary visual selection
H1 LOOK
H2 REMEMBER
H3 SHOW IT
thinking path
work-surface requirement
fresh independent retry
solution tokens / answer-leak controls
source note when applicable
```

Canonical contracts and engine:

```text
Grade 4/V2/Mathematics/LearningDesign/contracts/
Grade 4/V2/Mathematics/LearningDesign/engine/authoring_handoff.py
Grade 4/V2/Mathematics/LearningDesign/engine/build_learning_representation.py
```

Rules:

```text
H1/H2/H3 do not reveal the final answer
supported success is not independent success
fresh H0 follows support
procedural mathematics gets a typed work surface
required visual mathematics fails closed if no primitive exists
```

## 6. Stage D — StudyDesign

Do not publish a final study guide as `one source question = one page` unless that is genuinely the best learning design.

Create `study_journey_fixture.py` and synthesize the evidence into teaching concepts.

Required distinction:

```text
QuestionEvidence
  != TeachingConcept
  != StudyGuideModule
  != LearningBlock
  != Task
```

Several questions may belong to one teaching concept. One question may exercise several concepts.

The StudyJourney repertoire includes:

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

Use `WORKED_EXAMPLE` when instruction genuinely requires a shown solution. Keep independent/hint/retrieval states answer-free.

Pedagogical bridge content is allowed only when it is needed to teach an in-scope concept and must remain identified as:

```text
PEDAGOGICAL_BRIDGE
```

It does not become curriculum authority merely because it appears in the study guide.

Canonical StudyDesign:

```text
Grade 4/V2/Mathematics/StudyDesign/
```

## 7. Stage E — learner-facing production refinement

`production_fixture.py` exists for a narrow purpose: if visual QA shows that the selected **upstream representation** is insufficient, refine the learning/representation selection there.

Correct pattern:

```text
QA finds concept visual incomplete
→ change representation selection upstream
→ rerun validator
→ rerender
```

Prohibited pattern:

```text
QA finds concept visual incomplete
→ add question-specific drawing hack in PDF composer
```

Renderer-local pedagogy invention remains forbidden.

## 8. Stage F — render

Canonical publication entry points are under:

```text
Grade 4/V2/Mathematics/Publication/engine/
```

For task-level Core1 diagnostics use the authoring handoff route.

For the final teach-first study guide, publish the validated `StudyJourneyPlan` through:

```text
Publication/engine/study_journey_composer.py
```

Core2 remains linked by stable semantic IDs and uses the LearningRepresentationPlan/hint-ladder route.

## 9. Required validation before claiming success

At minimum run the canonical Grade-4 gate:

```bash
python 'Grade 4/V2/Mathematics/CoreSkills/validation/validate_authoring.py'
python 'Grade 4/V2/Mathematics/CoreSkills/validation/validate_semantic_extraction.py'
python 'Grade 4/V2/Mathematics/LearningDesign/validation/validate_learning_representation.py'
python 'Grade 4/V2/Mathematics/LearningDesign/validation/validate_authoring_handoff.py'
pytest -q 'Grade 4/V2/Mathematics/Representation/tests'
pytest -q 'Grade 4/V2/Mathematics/Publication/tests'
```

A new source set also needs a source-specific acceptance script that proves:

```text
all transcribed source questions are accounted for
source defects/ambiguities are preserved
all required visuals are realized
all required work surfaces are realized
worked-example answer visibility is intentional
independent/hint states do not leak solutions
StudyJourney instructional completeness passes
PDF pages render successfully
no clipping / overlap / learner-font-floor failure
artifact hashes/page custody bind the exact outputs
```

Green machine gates do not manufacture human review. Keep these separate:

```text
SUBJECT_CORRECTNESS
PEDAGOGICAL_DESIGN
ASSESSMENT_DESIGN
VISUAL_USABILITY
CHILD_USABILITY
MATURE_DESIGN_QUALITY
```

## 10. What a new agent should read

Read in this order:

```text
1. START_HERE.md                          ← this file
2. CoreSkills/contracts/input_intake.schema.json
3. CoreSkills/contracts/question-evidence.schema.json
4. CoreSkills/engine/README.md
5. CoreSkills/registry/*
6. Benchmarks/source_sets/_template/README.md
7. Benchmarks/source_sets/pupil_pages_97_99/source.json
8. Benchmarks/source_sets/pupil_pages_97_99/build_fixture.py
9. Benchmarks/source_sets/pupil_pages_97_99/study_journey_fixture.py
10. LearningDesign/contracts/authoring-support-blueprint.schema.json
11. StudyDesign/contracts/study-journey.schema.json
12. Publication/engine/study_journey_composer.py
13. Acceptance/Validation/validate_p97_p99_study_journey.py
```

## Final cold-start invariant

> A scan is evidence of what was asked. It is not itself a lesson plan. First preserve the source, then identify the mathematics, then design the learning journey, then realize validated representations, then publish and independently judge the exact artifact.
