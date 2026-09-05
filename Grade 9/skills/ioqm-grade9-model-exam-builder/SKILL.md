---
name: ioqm-grade9-model-exam-builder
description: Build one or more Grade 9 IOQM-style timed model examinations from a supplied reference paper and existing repository study-guide/research assets, with strict format fidelity, original question design, answer-only Appendix A, progressive-support Appendix B, reproducible metadata, and hard PDF QA.
---

# IOQM Grade 9 Model Exam Builder

## Purpose

Use this skill when the user asks for an IOQM-style model paper, mock test, practice exam, two or more exam sets, or an exam that should be "exactly similar" to a supplied IOQM reference paper in structure and presentation.

The governing distinction is:

```text
REFERENCE PAPER -> FORMAT / EXAM CONTRACT
STUDY GUIDES + REPO RESEARCH -> CONTENT COVERAGE / METHOD DEPTH
NEW AUTHORING -> QUESTIONS
```

Do not copy official/reference questions merely because the user asks for a similar paper. Similarity means exam architecture, answer mode, pacing, density, difficulty shape, visual language, and section behavior unless the user explicitly requests reproduction and rights/provenance permit it.

## When this skill takes priority

Use this skill instead of the question-bucket builder when the deliverable is a complete timed exam or a multi-exam package.

Use `skills/grade9-question-bucket-builder/SKILL.md` only as a support skill for source integrity, first-move pedagogy, transfer depth, and PDF preflight rules.

Also consult, when available:

- `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Topic_Taxonomy_v1.md`
- `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Question_Metadata_Schema_v1.csv`
- `Grade 9/Mathematics/IOQM/00_Architecture/IOQM_G9_Method_Selection_and_Transfer_Map_v1.md`
- relevant Number Theory, Algebra, Geometry, and Combinatorics study guides/research streams in the repository
- the supplied reference exam PDF, which is authoritative for the requested paper format

For PDF production, follow the repository PDF layout/preflight contracts and the runtime PDF skill.

## Core execution sequence

```text
INGEST REFERENCE EXAM
  -> EXTRACT EXAM CONTRACT
  -> SEARCH REPO / LOAD SUBJECT ASSETS
  -> BUILD BLUEPRINT
  -> AUTHOR ORIGINAL QUESTIONS
  -> SOLVE + VALIDATE EVERY ANSWER
  -> BUILD TIMED PAPER
  -> BUILD APPENDIX A: ANSWERS ONLY
  -> BUILD APPENDIX B: CONCEPT + HELPER + HINT LADDER
  -> RENDER / INSPECT / PREFLIGHT
  -> DELIVER SEPARATE TIMED + SUPPORTED + COMBINED PACK
```

Never jump from topic selection directly to PDF generation.

## 1. Reference-exam contract is P0

Before authoring questions, extract and freeze the visible contract of the supplied reference paper.

Record at minimum:

```text
exam duration
question count
maximum marks
mark bands / question ranges
answer mode
negative-marking rule
compulsory / optional status
instruction-page behavior
rough-work behavior
page count or density target if user asks "exactly similar"
figure style and placement
whether topic labels are hidden in the timed paper
```

If the supplied reference is the standard 30-question numerical-answer IOQM pattern seen in prior work, the extracted contract may be:

```text
Time: 3 hours
Questions: 30
Max marks: 100
Q1-Q8: 2 marks each
Q9-Q21: 3 marks each
Q22-Q30: 5 marks each
All questions compulsory
No negative marks
Each answer: one- or two-digit number
```

Do not assume those numbers if a newly supplied reference differs. The attachment wins.

### Exact similarity boundary

Match:

- hierarchy and pacing;
- section order;
- question-number/mark structure;
- answer-entry semantics;
- approximate page density;
- rough-work placement;
- restrained olympiad-paper visual style;
- diagram role and scale.

Do not copy:

- exact official questions;
- distinctive wording beyond unavoidable instructions;
- official logos, seals, or claims of official status;
- source diagrams when a newly authored diagram is required.

Label newly authored papers clearly as `IOQM-style model exam` or equivalent.

## 2. Repository-first content planning

Search the repository before external research.

Use existing concept-assimilation guides and topic research as the primary design corpus. The four principal domains are:

```text
Number Theory
Algebra
Geometry
Combinatorics
```

Do not make the timed paper look like four chapter blocks. IOQM-style retrieval requires mixed ordering.

Build a question blueprint with at least these fields:

```text
set_id
question_no
mark_value
domain
main_topic_id
mechanism
visible_clue
hidden_invariant
first_move
difficulty_target
answer
answer_digits
figure_required
source_role
originality_status
validation_status
```

For two or more model exams, create separate blueprints and check that the second set is not a numeric reskin of the first.

## 3. Distribution and difficulty design

### Domain balance

Across each 30-question set, distribute all four domains unless the user requests a topic-specific paper.

Do not force equal counts. Prefer a credible olympiad mix driven by the repository taxonomy and reference-paper flavor.

### Mark-band behavior

The three mark bands must differ in cognitive demand, not only arithmetic size.

A useful authoring intent is:

```text
2-mark: fast recognition + one clean execution step
3-mark: method selection, two-stage structure, or a close contrast
5-mark: compound reasoning, representation shift, non-obvious invariant, or multi-concept transfer
```

A 5-mark question must not be a 2-mark question with larger numbers.

### Difficulty shape

Within every mark band include variation. Avoid making Q1-Q8 uniformly trivial or Q22-Q30 uniformly exotic.

Keep the hardest questions solvable with the concepts already present in the Grade 9 IOQM corpus/research unless the user explicitly requests a wider olympiad range.

## 4. Original question authoring contract

Every newly authored item must pass all of these gates:

1. **Mathematical closure** - the data determine the requested numerical answer.
2. **Answer-mode closure** - the final answer obeys the reference paper's answer format; for a one/two-digit exam, validate `0 <= answer <= 99` unless the reference defines another convention.
3. **No hidden ambiguity** - constructions, indexing, orientation, domain, and equality conditions are explicit enough to determine one intended answer.
4. **No accidental dependence** - a question must not rely on a theorem or definition absent from the intended syllabus depth unless it is derivable in-context.
5. **Originality** - not copied from the supplied reference paper or frozen study-guide corpus.
6. **Structural value** - the item tests recognition/representation/method choice, not only computation.
7. **Independent solvability** - no answer requires reading another question.

For geometry, render or inspect the diagram at final size. The diagram must be mathematically consistent; it is not decoration.

For combinatorics, define what counts as the same object and any symmetry identification explicitly.

For number theory, verify positivity/integrality/base/digit restrictions and modular legality.

For algebra, verify domains, extraneous roots, denominator restrictions, and attainability of extrema.

## 5. Solve-and-validate gate

No question enters the paper until a solution record exists privately in the build data.

For each question record:

```text
canonical answer
short derivation or verification route
independent check
answer-format check
ambiguity check
```

Use computation for arithmetic verification when useful, but keep the student paper self-contained and calculator-free.

If two independent methods disagree, the question is blocked until repaired.

Run a final answer sweep across all 30 items:

```text
unique intended answer? PASS/FAIL
answer in allowed range? PASS/FAIL
integer if required? PASS/FAIL
no accidental alternative interpretation? PASS/FAIL
```

## 6. Timed-paper contract

The timed paper must contain **questions only** plus the reference-style front matter and rough-work space.

It must not reveal:

- domain labels;
- concept names;
- difficulty badges;
- first moves;
- hint language;
- answers;
- repository method IDs.

The learner should face an unlabeled retrieval problem, as in the real exam.

When the user asks for two model exams, provide a separate timed PDF for each set.

## 7. Appendix A - answers only

For each question set, Appendix A is intentionally sparse.

Required format:

```text
Appendix A - Answer Key
Q1  <answer>
Q2  <answer>
...
Q30 <answer>
```

Do not include derivations, concept names, hints, or explanations in Appendix A unless the user explicitly asks for worked solutions.

Keep Appendix A after the complete timed paper so it cannot leak during a realistic attempt.

## 8. Appendix B - concept, helper, hints

For every question, provide a support card after Appendix A.

Minimum structure:

```text
Qn
Concept: <readable concept family>
Helper: <one compact representation/method-selection cue>
Notice: <what visible structure should trigger recognition>
Recall: <the theorem/invariant/tool to retrieve>
Start: <the first executable mathematical line/setup>
```

### Hint discipline

`Notice` may identify structure but must not expose the final answer.

`Recall` retrieves a stable concept/theorem/invariant, not a near-complete solution.

`Start` gives only the legal first move or setup. It may be equation-level but should leave the execution to the student.

Do not turn Appendix B into worked solutions unless asked.

The intended progression is:

```text
attempt unaided
  -> Notice if recognition fails
  -> Recall if memory fails
  -> Start if line 1 still fails
  -> close the appendix and solve
```

For geometry, the Helper may include a small redraw/representation cue if the original figure is cognitively dense.

## 9. Multiple-set anti-duplication gate

For two model exams, compare Set 1 and Set 2 before layout.

Flag and repair if any pair is merely:

- same equation with changed constants;
- same geometry with relabeled vertices;
- same counting skeleton with a different object name;
- same modular cycle with a different exponent;
- same answer path with only cosmetic wording changes.

The two sets may test the same concept, but they should vary representation or method boundary.

Maintain a cross-set matrix:

```text
concept/mechanism | Set 1 question | Set 2 question | transfer difference
```

## 10. Visual and layout contract

When a reference exam is supplied, inspect its rendered pages, not only extracted text.

Match the functional visual behavior:

- compact exam typography;
- clear question numbering;
- restrained use of rules/headers;
- ample white space for rough work;
- figures beside or immediately below the relevant question;
- no decorative illustration;
- no textbook-style concept boxes inside the timed paper.

Appendix B may use a more instructional layout, but it should remain compact enough to scan question-by-question.

For figures:

```text
DRAW -> RENDER AT FINAL SIZE -> INSPECT -> REPAIR -> RERENDER
```

Never accept a mathematically misleading geometry figure just because the text is correct.

## 11. Deliverable package

For `N` model exams, normally deliver:

```text
Set_1_Timed_Paper.pdf
Set_1_with_Appendices.pdf
...
Set_N_Timed_Paper.pdf
Set_N_with_Appendices.pdf
Complete_Pack.pdf
Blueprint / metadata file
QA report
optional ZIP containing the complete reusable package
```

If the user only asks for the final supported booklets, still keep the timed-paper split in the build because it is required for leakage QA.

## 12. QA hard gates

### Content QA

For every set:

- exact question count matches the reference contract;
- mark total recomputes correctly;
- every answer has been solved and checked;
- answer format is valid;
- no timed-paper answer/hint leakage;
- Appendix A contains all and only answers;
- Appendix B has Concept + Helper + Notice + Recall + Start for every question;
- every figure is attached to the correct item;
- all four domains are represented when building a general mixed exam;
- no unresolved source/copyright claim appears in the student paper.

### PDF QA

Before delivery:

1. render every page;
2. inspect instruction page, all figure pages, first/last question pages, Appendix A, and every Appendix B page;
3. verify no clipping, overlap, missing glyphs, broken fractions, black squares, or unreadable diagrams;
4. run PDF preflight;
5. verify timed-paper page count and supported-booklet page count;
6. verify combined pack ordering;
7. open final PDFs from the exact delivery directory.

If any gate fails, repair and rerun the complete affected gate.

## 13. Metadata and provenance language

Use clear status labels internally:

```text
OFFICIAL_REFERENCE_FORMAT
AUTHOR_CREATED_IOQM_STYLE
REPO_SUPPORTED_CONCEPT
```

Do not call an authored question `IOQM 202X Qn` or imply it appeared officially.

The final paper should contain a compact non-intrusive label such as:

```text
IOQM-style Grade 9 Model Examination - Author-created practice paper
```

## 14. Repository behavior

When the user asks to update the repo:

- create a dedicated branch;
- add/update skill or build metadata in reusable text form;
- do not commit bulky generated PDFs unless the repository convention explicitly requires them;
- open a PR against `main`;
- merge only after the requested validation passes or the user explicitly asks to merge immediately.

## Final response checklist

Report:

- number of model exams;
- extracted exam contract;
- timed-paper and supported-booklet page counts;
- Appendix A / Appendix B completeness;
- validation/preflight result;
- branch/PR/merge status when repo changes were requested;
- any NOT_RUN or unresolved items.
