# Grade 4 Mathematics V2 - StudyDesign

`StudyDesign` is the document-level pedagogy layer above task-level `LearningRepresentationPlan`.

It exists because a correct task page is not automatically a coherent study guide.

```text
QuestionEvidence
  -> CoreSkills authoring
  -> LearningDesign / LearningRepresentationPlan   (task-level support)
  -> StudyDesign / StudyJourneyPlan                (concept + document sequence)
  -> Representation
  -> Publication
  -> Acceptance
```

## Distinct units

```text
QuestionEvidence != TeachingConcept != StudyGuideModule != LearningBlock != Task
```

Several source questions may be synthesized into one teaching concept. A source question may also contribute evidence to more than one concept.

## Learning blocks

The canonical block intents are:

- `SEE_DISCOVER`
- `NOTICE`
- `CONNECT`
- `WORKED_EXAMPLE`
- `GUIDED_TRY`
- `INDEPENDENT_TRY`
- `ERROR_ANALYSIS`
- `TRANSFER`
- `RETRIEVAL`
- `REFERENCE`
- `SELF_CHECK`

Worked examples may intentionally reveal their own solution. Independent, transfer and retrieval tasks must remain answer-free. Hint/fresh-H0 answer-leak rules from LearningDesign remain unchanged.

## Pedagogical bridges

A `PEDAGOGICAL_BRIDGE` may add prerequisite explanation needed to teach an in-scope skill. It does not promote that bridge to curriculum authority and must not erase source ambiguity or defects.

## Publisher rule

The publisher may style and paginate the StudyJourneyPlan. It may not invent, delete, or reorder the teaching journey to repair layout.
