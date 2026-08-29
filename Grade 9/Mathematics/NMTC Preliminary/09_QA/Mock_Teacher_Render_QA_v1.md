# NMTC Preliminary — Mock Teacher-Key Render QA v1

## Scope

First actual PDF/render inspection of the three teacher keys:

- Mock A teacher key;
- Mock B teacher key;
- Mock C teacher key.

This complements `Mock_Student_Render_QA_v1.md`.

## Render profile

- A4 PDF;
- XeLaTeX;
- Unicode-capable DejaVu Sans / DejaVu Sans Mono;
- compact teacher-key margin profile;
- source Markdown table retained;
- all pages rasterized and visually inspected.

## Page counts

| Artifact | Pages | Verdict |
|---|---:|---|
| Mock A teacher key | 2 | `PASS_PREVIEW` |
| Mock B teacher key | 3 | `PASS_PREVIEW` |
| Mock C teacher key | 3 | `PASS_PREVIEW` |

## Visual findings

### Tables

The 30-row diagnostic tables fit without clipping.

Columns retained:

- Q;
- answer;
- package;
- first useful move;
- likely miss tag.

Some first-move cells wrap over several short lines, especially in B/C. This is dense but readable and does not cross column/page boundaries.

### Minimum-path sections

- headings remain attached to their solution blocks;
- no solution paragraph is visibly clipped;
- no missing congruence glyphs observed under the corrected font profile;
- page transitions do not pair a solution with the wrong question.

### Diagnostic sections

Teacher-only diagnostic language remains clearly in the teacher artifact. This is expected and not a leakage defect.

## Student/teacher boundary

The teacher PDFs contain answers, package codes, first moves and diagnostic tags by design.

The separately rendered student PDFs were inspected independently and did not expose those teacher fields.

Therefore the mock artifact separation now has rendered-preview evidence in both directions.

## Remaining notation issue

Like the student previews, the teacher previews still retain authoring-style forms including:

- `sqrt...` text;
- `floor(...)`;
- ASCII power/subscript forms;
- textual `alpha`, `beta`;
- compact inline congruence/mod expressions.

They are readable, but they are not yet the final mathematical typography required by `Production_Notation_and_Render_Contract_v1.md`.

## Verdict

```text
MOCK_TEACHER_LAYOUT_RENDER_QA = PASS_PREVIEW
MOCK_TEACHER_GLYPH_QA = PASS_PREVIEW
MOCK_TEACHER_TABLE_OVERFLOW_QA = PASS_PREVIEW
MOCK_ARTIFACT_SEPARATION_RENDER_EVIDENCE = PASS_PREVIEW
MOCK_FINAL_NOTATION_QA = PARTIAL
FINAL_MOCK_RENDER_QA = NOT_READY
```

## Next valid render step

Normalize mathematical notation in a deterministic production transform, then re-render all six mock artifacts (3 student + 3 teacher) and repeat layout/glyph/leakage inspection.

Classroom timing/readability remains a separate evidence gate and stays `NOT_RUN`.
