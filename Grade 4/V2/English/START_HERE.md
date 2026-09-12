# START HERE — Grade 4 English V2

Do not start from the PDF renderer.

For a new English worksheet, question paper, workbook page, or scan, use this order:

```text
INPUT
scanned questions / typed questions
+ optional topic hints
+ optional child work
+ optional textbook / teacher notes

        ↓

FAITHFUL SOURCE EXTRACTION
preserve wording, categories, rubrics, defects, ambiguity

        ↓

source.json
+ SourceModel
+ QuestionEvidence
+ optional LearnerEvidence

        ↓

CoreSkills authoring

        ↓

LearningRepresentationPlan

        ↓

Student Study Guide / Workbook
Teacher Diagnostic Key

        ↓

Source-coverage acceptance
+ rendered visual QA
```

## New source-set workflow

1. Copy `Benchmarks/source_sets/_template/`.
2. Give the source set a stable ID such as `english_worksheet_09`.
3. Transcribe only what is actually visible into `source.json`.
4. Record uncertainty or defects under `source_issues`; do not silently reconstruct cropped or ambiguous text.
5. Create or reference a `SourceModel` when the source supplies a taxonomy, sequence, rubric, or response rule.
6. In `build_fixture.py`, map each source obligation to canonical capability IDs, task-family IDs, response structures, representations, and an explicit H1/H2/H3 support blueprint.
7. Keep optional child responses in `LearnerEvidence`; never edit source truth because of a child mistake.
8. Run Acceptance before Publication work.

## Hard rules

- Do not infer a complete official syllabus from one question set. Use `QUESTION_SET_OBSERVED` unless curriculum authority is supplied.
- Do not invent grammar categories to force-fit source words.
- Do not turn an open English answer into binary correctness by comparing it with one model sentence.
- Do not treat a supported answer as independent learning evidence. After H1/H2/H3, require a fresh H0 retry.
- Do not solve a pedagogy problem in renderer code.

## First benchmark

`Benchmarks/source_sets/english_worksheet_09/` is the reference implementation for the supplied Grade-4 worksheet covering adjective classification/order, descriptive writing, poetry comprehension, inference, multi-clue synthesis, transfer, and justification.
