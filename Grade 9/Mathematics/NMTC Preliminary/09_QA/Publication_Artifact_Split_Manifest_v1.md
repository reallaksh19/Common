# NMTC Bhaskara Preliminary — Publication Artifact Split Manifest v1

## Purpose

This manifest defines what may enter a **student-facing publication** and what must remain in the **teacher/authoring layer**.

The authoring repository intentionally contains richer provenance, QA and diagnostic material than a student workbook should expose. Publication must therefore be an explicit projection, not a direct dump of the source tree.

## Student-facing content classes

Student exports may include:

- Concept Book student drafts after production copyedit;
- worked examples intended for learning;
- First-Step recognition cards when answers/teacher notes are removed or separately placed;
- practice questions;
- transfer questions;
- mastery tests;
- mock student papers;
- student self-check/attempt record forms;
- concise answer sections when the selected publication format calls for them;
- source references that are meaningful and non-misleading to the student.

## Teacher/authoring-only content classes

The following must not leak into an exam/mock student paper:

- teacher answer keys;
- package labels that reveal the intended method;
- diagnostic tags such as `REC`, `FM`, `REP`, `DOM`, `FIG`;
- first-useful-move answers for an unlabelled assessment;
- minimum-path solutions placed adjacent to the live question;
- internal QA comments;
- source-conflict adjudication notes not needed by the learner;
- historical recurrence percentages presented as weightage;
- machine-custody fields;
- calibration notes tied to individual attempts.

## Mock-system split

The current v1 mock system already satisfies the source-file separation rule:

### Student

- `Mock_A_Student_v1.md`
- `Mock_B_Student_v1.md`
- `Mock_C_Student_v1.md`
- `Mock_Diagnostic_Record_Template_v1.md` may be supplied after or alongside the attempt as designed.

### Teacher

- `Mock_A_Teacher_Key_v1.md`
- `Mock_B_Teacher_Key_v1.md`
- `Mock_C_Teacher_Key_v1.md`
- `Mock_System_Blueprint_v1.md`
- `Mixed_Preliminary_Mock_System_QA.md`
- `Mock_Item_Metadata_v1.csv`

Student mock papers must remain **unlabelled by package/concept**.

## Topic-package production split

For each topic package, create two final manifests before rendering:

### `STUDENT_MANIFEST`

Must list only files/sections authorized for the learner.

### `TEACHER_MANIFEST`

May additionally include:

- solutions;
- teaching notes;
- misconceptions;
- source/QC notes;
- diagnostic routing;
- answer keys;
- calibration notes.

The current source tree is `PARTIAL` for this gate because the conceptual separation exists but final export manifests have not yet been frozen package-by-package.

## Leakage audit

Before any student PDF/export is approved, search the rendered/student artifact for prohibited internal tokens, including where applicable:

```text
PASS_INTERNAL
NOT_RUN
SOURCE_CONFLICT
FIGURE_GATED
AUTHOR_CREATED_TRANSFER
REC
FM
REP
DOM
CASE
COUNT
FIG
LOGIC
QA
teacher key
first useful move
```

A token appearing in legitimate explanatory prose is not automatically a failure, but every occurrence must be reviewed. In particular, diagnostic codes and internal status labels should normally be absent from student assessment papers.

## Answer placement rule

Student-facing learning material may include answers when pedagogically intended, but assessment artifacts must preserve attempt integrity.

For a mock/mastery paper:

`QUESTION PAPER -> ATTEMPT RECORD -> SUBMIT/FINISH -> ANSWER/TEACHER LAYER`

Do not place answer keys in the same immediate visual flow as an active mock.

## Historical-source notes

A student publication may say that a mechanism is inspired/grounded by qualified previous-year evidence only when provenance supports that claim.

It must not:

- assign an NMTC year/question number to author-created material;
- call P1/P2/P3 secondary material official;
- silently repair a conflicted PYQ into a clean-looking historical question;
- redraw an unrecovered historical figure and present it as the original.

## Current status

```text
MOCK_STUDENT_TEACHER_SPLIT = PASS_STATIC
TOPIC_PACKAGE_PRODUCTION_MANIFESTS = NOT_RUN
RENDERED_LEAKAGE_AUDIT = NOT_RUN
FINAL_STUDENT_TEACHER_SEPARATION = NOT_READY
```
