# NMTC Bhaskara Preliminary — Production Notation & Render Contract v1

## Purpose

Define the deterministic source-to-publication normalization required before student PDFs/exports are called publication-ready.

This file is a **contract**, not evidence that final rendering has already been completed.

## Source notation vs production notation

Authoring Markdown may use compact ASCII forms such as:

- `sqrt(...)`
- `floor(x)` / `ceil(x)`
- `alpha`, `beta`
- `x^2`
- `a_n`
- `mod`
- `degrees`

Production rendering should convert these consistently into readable mathematical notation where the output system supports it, while preserving exact meaning.

## Mandatory mathematical rendering rules

### Exponents and subscripts

- exponent binding must be unambiguous;
- multi-character exponents require grouping;
- sequence indices must not be visually mistaken for multiplication;
- negative exponents/signs must remain attached to the intended base.

### Radicals

- radical scope must be visually explicit;
- nested radicals must not lose inner/outer grouping;
- principal-root meaning must not be changed during beautification.

### Fractions

- numerator/denominator scope must be unambiguous;
- inline slash notation may remain only when there is no grouping ambiguity;
- complex rational expressions should render as stacked fractions where practical.

### Floor and ceiling

Use true floor/ceiling delimiters when supported:

- floor: `⌊x⌋`
- ceiling: `⌈x⌉`

If textual `floor(x)` / `ceil(x)` is retained, it must be used consistently within the artifact.

Half-open interval direction is mathematically significant and must survive line wrapping:

`floor(x)=m <=> m <= x < m+1`

`ceil(x)=m <=> m-1 < x <= m`

### Congruence

Use a consistent form such as:

`a ≡ b (mod n)`

Do not let line breaks separate a modulus from its congruence statement in a way that changes readability.

### Geometry

- degree symbols must render as `°` where supported;
- segment/point labels must remain distinguishable;
- no source-gated historical figure may be silently replaced by an inferred production redraw;
- author-created geometry used in mocks may remain text-complete without a diagram.

## Typography rules

- minus sign must not be confused with a hyphen in displayed mathematics;
- decimal points and negative signs must remain visible at normal print size;
- question numbers must not detach from question text across pages;
- MCQ option labels A–D must remain aligned with their option text;
- tables must not clip mathematical expressions;
- answer keys must not wrap in ways that pair an answer with the wrong question.

## Page-break rules

Avoid, where possible:

- a question stem on one page and all options on the next;
- a displayed equation split across pages;
- a heading orphaned at the bottom of a page;
- a geometry definition separated from the quantity it defines;
- a student answer area separated from its question when the layout requires local working space.

## Student/teacher leakage check

Rendered student artifacts must be searched/reviewed for accidental inclusion of:

- answer keys;
- diagnostic codes;
- `PASS_INTERNAL` / `NOT_RUN` statuses;
- package labels that reveal method in an unlabelled assessment;
- teacher minimum-path notes;
- source-conflict adjudication intended only for authors/teachers.

See `Publication_Artifact_Split_Manifest_v1.md`.

## Static source state for current mock system

For Mock A/B/C source files:

- question numbering: statically complete 1–30 each;
- response-section split: 15 MCQ + 15 numeric each;
- student/teacher files: separated;
- answer vectors: second-pass checked;
- author-created provenance: explicit;
- historical figure dependency: none;
- machine metadata: present in `Mock_Item_Metadata_v1.csv`.

Therefore:

`MOCK_SOURCE_NOTATION_QA = PASS_STATIC`

But:

`MOCK_RENDER_QA = NOT_RUN`

because a final production render has not yet been generated and inspected under this contract.

## Topic-package state

Topic packages retain:

`TOPIC_SOURCE_NOTATION_QA = PARTIAL`

until each final student/teacher production manifest is frozen and the actual output artifacts are rendered/inspected.

## Render QA evidence record

Every final PDF/export should receive a versioned record containing at least:

```text
artifact
source revision
page count
student_or_teacher
notation check
page-break check
clipping/overflow check
answer-leakage check
figure/source-custody check
result = PASS / FAIL
review notes
```

## Current state

```text
PRODUCTION_NOTATION_CONTRACT = DEFINED
MOCK_SOURCE_NOTATION_QA = PASS_STATIC
TOPIC_SOURCE_NOTATION_QA = PARTIAL
FINAL_RENDER_QA = NOT_RUN
```
