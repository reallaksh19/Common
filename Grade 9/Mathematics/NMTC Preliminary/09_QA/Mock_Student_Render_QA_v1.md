# NMTC Preliminary — Mock Student Render QA v1

## Scope

First actual PDF/render inspection of the **student** Mock A/B/C artifacts.

Teacher-key render QA is not included in this pass.

## Pipeline used

Source:

- live `Mock_A_Student_v1.md`
- live `Mock_B_Student_v1.md`
- live `Mock_C_Student_v1.md`

Production-preview normalization:

1. preserve the explicit `author-created / not official` notice;
2. split compressed A/B/C/D option strings onto separate lines;
3. use XeLaTeX;
4. use DejaVu Sans / DejaVu Sans Mono to avoid missing math glyphs;
5. use compact A4 margins appropriate for a 30-question training paper;
6. render PDFs to PNG and inspect all pages.

## Defects found during first render

### R1 — Mock C congruence glyph

Initial XeLaTeX conversion using the default mono font warned that `≡` was missing from the code font.

Risk:

A modular-congruence question could render with a missing mathematical relation.

Correction:

Use a Unicode-capable DejaVu mono/main font profile for production preview.

Result:

`CORRECTED_IN_PREVIEW`.

### R2 — Mock A pagination

Initial default render produced 6 pages, with the final close-out record occupying an effectively isolated page.

First production normalization reduced it to 5 pages but still left the close-out alone.

Correction:

Use a slightly tighter A4 production margin for Mock A.

Result:

Mock A now renders as 4 pages with the close-out record retained on page 4 and no observed clipping.

### R3 — Mock B/C compressed options

Source Markdown B/C stores many MCQ options on one source line.

Default PDF rendering made those choices visually cramped.

Correction:

Production preprocessor splits option groups onto separate visual lines.

Result:

`CORRECTED_IN_PREVIEW`.

## Page-count result

| Artifact | Production-preview pages | Layout verdict |
|---|---:|---|
| Mock A student | 4 | `PASS_PREVIEW` |
| Mock B student | 4 | `PASS_PREVIEW` |
| Mock C student | 4 | `PASS_PREVIEW` |

## Visual inspection result

Across the 12 rendered student pages:

- no clipped text observed;
- no overlapping blocks observed;
- no black-square/missing-glyph artifact observed after font correction;
- Q01–Q30 numbering remains complete;
- Section A/B separation remains visible;
- student close-out remains visible;
- no teacher answer key or diagnostic tag leaked into the student paper;
- author-created/non-official notice remains visible.

## Notation verdict

The production previews still preserve several authoring-style textual forms such as:

- `sqrt(...)`;
- `floor(...)` / `ceil(...)`;
- `alpha`, `beta`;
- inline exponent/subscript ASCII patterns.

These are mathematically readable, but they do **not yet close the final production-notation contract**.

Therefore:

```text
MOCK_STUDENT_LAYOUT_RENDER_QA = PASS_PREVIEW
MOCK_STUDENT_GLYPH_QA = PASS_PREVIEW
MOCK_STUDENT_LEAKAGE_QA = PASS_PREVIEW
MOCK_STUDENT_FINAL_NOTATION_QA = PARTIAL
MOCK_TEACHER_RENDER_QA = NOT_RUN
FINAL_MOCK_RENDER_QA = NOT_READY
```

## Required next render work

1. convert source-style mathematical tokens to consistent production math typesetting;
2. render/inspect the three teacher keys;
3. retain deterministic page/profile settings;
4. re-run student leakage checks after final math typesetting;
5. only then mark full mock render QA `PASS`.

## Calibration boundary

No timing/readability inference is made from these renders alone.

`CLASSROOM_TIMING_CALIBRATION = NOT_RUN` remains unchanged.
