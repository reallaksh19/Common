# Primary Math V2 Authoring Flow

This flow is normative for cold-start authoring under #328.

## Stage 0 — load authorities

Load the applicable Common Primary authorities before interpreting inputs:

```text
#163 scope / ontology / ownership
#171 work evidence
#172 evidence-before-diagnosis
#185 contrast / probe semantics
#182 learner publishing
#164 runtime support / fading / evidence dimensions
```

Do not substitute Grade 9 architecture for these meanings.

## Stage 1 — intake

Required logical input:

```text
question_set
```

Optional:

```text
student_workout
topic_hints
```

Validate presence/provenance. Missing optional inputs must not block authoring.

## Stage 2 — resolve observed scope

Extract from the question set:

```text
concept candidates
capabilities / micro-skills
problem families
representation demands
quantity structures
reasoning demands
source references
```

Assign scope basis before teaching decisions.

Do not promote observed question content to universal curriculum scope.

## Stage 3 — build concept/skill graph

Resolve observed material against canonical concepts and prerequisites.

Output:

```text
PrimaryMathSkillModel
```

Unresolved mappings remain explicit:

```text
MAPPING_PENDING
SOURCE_NOT_PROVIDED
AMBIGUOUS
```

## Stage 4 — preserve learner work when present

If `student_workout` exists, build `MathematicalWorkEvidence` before diagnosis.

Preserve correct and incorrect steps, teacher annotations and ambiguity.

No OCR or renderer may invent an unreadable mathematical step.

## Stage 5 — bounded diagnostic reasoning when needed

Use structural contrasts before broad reteach.

```text
work evidence
→ focal feature
→ ContrastSet
→ 2–3 competing hypotheses
→ smallest DiagnosticProbe
```

A diagnostic probe is distinct from ordinary practice.

## Stage 6 — assign ConceptMode

For each active concept/module assign one or more current modes:

```text
INTRODUCE
CONNECT
REPAIR
PROBE
PRACTISE
RETRIEVE
TRANSFER
VERIFY
REFERENCE
```

Mode selection must be justified by scope and/or evidence refs.

## Stage 7 — design Core 1

Produce `PrimaryMathCore1StudyPlan`.

The plan states:

```text
module order
concept refs
mode
representation sequence
worked examples
learner action
support/fading
independent checks
```

It does not contain physical page numbers as canonical identity.

## Stage 8 — design Core 2

Produce `PrimaryMathCore2CompanionPlan`.

Appendix A:

```text
RECONNECT / BUILD / CHOOSE / MIX / TRANSFER / RETRIEVE
```

Appendix B:

```text
H0 TRY
H1 NOTICE
H2 REMEMBER
H3 REPRESENT
→ fresh independent H0
```

Appendix C:

```text
visual first-step / process reference
```

## Stage 9 — representation planning

For each concept, declare required representation roles and translation bridges.

Create a `RepresentationPlan` containing semantic primitive requirements without page placement.

## Stage 10 — visual semantic validation

Every quantitative/structural primitive validates before render.

Fail closed on missing/ungrounded values.

## Stage 11 — publication

The publisher may decide placement and pagination only after validated semantic objects exist.

Required outputs include:

```text
Core1 PDF
Core2 PDF
PhysicalPageMap
page-image review bundle
artifact manifest
```

## Stage 12 — neutral candidate export

Export exact candidate evidence in the neutral contract consumed by #325.

Producer-declared PASS booleans are not independent acceptance evidence.

## Stage 13 — independent benchmark

Run #325 oracle and adversarial corpus.

Semantic/engineering acceptance remains distinct from human educational review.

## Stage 14 — human review

Required exact-artifact review states remain independent:

```text
SUBJECT_CORRECTNESS
PEDAGOGICAL_DESIGN
ASSESSMENT_DESIGN
VISUAL_USABILITY
CHILD_USABILITY
MATURE_DESIGN_QUALITY
```

No maturity claim is allowed while required human gates are pending or failing.
