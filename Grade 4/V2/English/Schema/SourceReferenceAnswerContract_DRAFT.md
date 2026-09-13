# Grade 4 English Source Reference + Answer Contract (DRAFT)

**Status:** production-kit contract for cold-start authoring.  
**Rule:** source identity and answer authority are data, not layout decorations.

## Stable source identity

Every task extracted from a workbook/scan must retain the original source identity.

```yaml
source_reference:
  source_kind: WORKBOOK
  page: 98
  section_label: "I"
  section_title: "Read and map the journey"
  question_number: null
  organizer_box: "5"
  original_label: "Movement to cities (Industrial revolution)"
  display_ref: "Workbook p.98 - I - Box 5"
```

Do not silently renumber source questions. If the workbook says `III. 4)`, all lesson, hint, answer-check and teacher surfaces refer to it as `Worksheet III-4` or an equivalent unambiguous display preserving III and 4.

Generated questions use a separate namespace such as `Fresh A`, `Fresh B`; they never borrow workbook numbers.

## Handwriting is observation, not authority

`observed_student_answer != correct_answer`

Visible handwriting is stored separately and may be used diagnostically, but cannot become the answer merely because it is written on the page.

## Every task has an answer contract

```yaml
answer:
  status: VERIFIED_SOURCE | DERIVED_FROM_SOURCE | VERIFIED_RULE | RUBRIC | SOURCE_UNRESOLVED
  expected_response: ...
  acceptable_answers: []
  explanation: ...
  evidence_refs: []
```

`SOURCE_UNRESOLVED` requires `expected_response: null`. Do not fill a source gap with general knowledge unless the user explicitly requests outside knowledge and that material is labelled separately.

For reading-to-organizer tasks, `DERIVED_FROM_SOURCE` requires source lines plus evidence spans/refs supporting the short answer.

## Release gates

```text
SOURCE_REFERENCE_MISSING
SOURCE_NUMBER_REWRITTEN
GENERATED_ITEM_USING_SOURCE_NUMBER
ANSWER_CONTRACT_MISSING
OBSERVED_HANDWRITING_PROMOTED_TO_ANSWER
SOURCE_UNRESOLVED_WITH_ASSERTED_ANSWER
DERIVED_READING_ANSWER_WITHOUT_EVIDENCE
```
