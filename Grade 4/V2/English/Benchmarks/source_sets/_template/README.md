# Grade 4 English V2 source-set template

Copy this directory for each new worksheet, exam paper, workbook page, or typed question set.

Required source-set files:

- `source.json` — faithful transcription and source issues only.
- `build_fixture.py` — explicit semantic mapping into SourceModel + QuestionEvidence; no keyword inference.
- `production_fixture.py` — optional learner-facing representation refinements after visual QA. Use only when the semantic plan, not the renderer, needs to change.

## Rules

1. Preserve source wording, categories, rubrics and ambiguity.
2. Do not silently correct source defects.
3. Use registry IDs for capabilities, task families, response structures and representations.
4. Keep optional learner mistakes separate from source truth.
5. Every source obligation must map to Teach, Model, Practice, Hints, Fresh H0 Verify, and Answer/Rubric before publication acceptance can pass.
